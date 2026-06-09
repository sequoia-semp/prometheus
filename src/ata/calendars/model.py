"""Versioned calendars, expiry rules, delivery periods, and settlement anchors."""

from __future__ import annotations

import calendar as calendar_lib
import json
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Literal, TypeAlias, cast

ExpiryRuleName: TypeAlias = Literal["henry_ld1_third_business_day_prior"]
SettlementAnchorName: TypeAlias = Literal["contract_month", "exchange_settlement"]
DeliveryProfileName: TypeAlias = Literal["baseload", "5x16"]


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _date_to_json(value: date) -> str:
    return value.isoformat()


def _date_from_json(value: object, field_name: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO date string")
    return date.fromisoformat(value)


def _required_str(data: dict[str, object], key: str) -> str:
    value = data[key]
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _required_str_list(data: dict[str, object], key: str) -> list[str]:
    value = data[key]
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list of strings")
    items = cast(list[object], value)
    if not all(isinstance(item, str) for item in items):
        raise ValueError(f"{key} must be a list of strings")
    return [cast(str, item) for item in items]


def _required_int_list(data: dict[str, object], key: str) -> list[int]:
    value = data[key]
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list of integers")
    items = cast(list[object], value)
    if not all(isinstance(item, int) for item in items):
        raise ValueError(f"{key} must be a list of integers")
    return [cast(int, item) for item in items]


@dataclass(frozen=True, slots=True)
class CalendarResult:
    """A dated calendar output with lineage."""

    calendar_version: str
    value_date: date

    def to_json_dict(self) -> dict[str, object]:
        return {
            "calendar_version": self.calendar_version,
            "value_date": _date_to_json(self.value_date),
        }


@dataclass(frozen=True, slots=True)
class VersionedCalendar:
    """Versioned business calendar input."""

    calendar_id: str
    version: str
    timezone: str
    weekend_days: tuple[int, ...]
    holidays: frozenset[date]
    source: str

    @property
    def calendar_version(self) -> str:
        return f"{self.calendar_id}:{self.version}"

    def __post_init__(self) -> None:
        for field_name in ["calendar_id", "version", "timezone", "source"]:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")
        for weekday in self.weekend_days:
            if weekday < 0 or weekday > 6:
                raise ValueError("weekend_days must use Python weekday values 0..6")

    def is_business_day(self, value: date) -> bool:
        return value.weekday() not in self.weekend_days and value not in self.holidays

    def add_business_days(self, value: date, days: int) -> date:
        if days == 0:
            return value
        step = 1 if days > 0 else -1
        remaining = abs(days)
        current = value
        while remaining:
            current += timedelta(days=step)
            if self.is_business_day(current):
                remaining -= 1
        return current

    def to_json_dict(self) -> dict[str, object]:
        return {
            "calendar_id": self.calendar_id,
            "version": self.version,
            "timezone": self.timezone,
            "weekend_days": list(self.weekend_days),
            "holidays": [_date_to_json(item) for item in sorted(self.holidays)],
            "source": self.source,
        }

    def to_json_line(self) -> str:
        return _canonical_json(self.to_json_dict())

    @classmethod
    def from_json_dict(cls, data: dict[str, object]) -> VersionedCalendar:
        return cls(
            calendar_id=_required_str(data, "calendar_id"),
            version=_required_str(data, "version"),
            timezone=_required_str(data, "timezone"),
            weekend_days=tuple(_required_int_list(data, "weekend_days")),
            holidays=frozenset(
                _date_from_json(item, "holidays[]")
                for item in _required_str_list(data, "holidays")
            ),
            source=_required_str(data, "source"),
        )

    @classmethod
    def from_json_line(cls, line: str) -> VersionedCalendar:
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError("calendar JSON must contain an object")
        return cls.from_json_dict(cast(dict[str, Any], data))


@dataclass(frozen=True, slots=True)
class DeliveryPeriod:
    """Inclusive/exclusive delivery period with calendar lineage."""

    calendar_version: str
    delivery_start: date
    delivery_end: date

    @classmethod
    def contract_month(cls, *, calendar: VersionedCalendar, contract_period: str) -> DeliveryPeriod:
        year_text, month_text = contract_period.split("-")
        year = int(year_text)
        month = int(month_text)
        start = date(year, month, 1)
        last_day = calendar_lib.monthrange(year, month)[1]
        end = date(year, month, last_day) + timedelta(days=1)
        return cls(
            calendar_version=calendar.calendar_version,
            delivery_start=start,
            delivery_end=end,
        )

    def to_json_dict(self) -> dict[str, object]:
        return {
            "calendar_version": self.calendar_version,
            "delivery_start": _date_to_json(self.delivery_start),
            "delivery_end": _date_to_json(self.delivery_end),
        }


@dataclass(frozen=True, slots=True)
class DeliveryProfile:
    """Versioned delivery profile such as baseload or 5x16."""

    profile_id: str
    version: str
    name: DeliveryProfileName
    active_weekdays: tuple[int, ...]
    active_hour_start: int
    active_hour_end: int

    @property
    def profile_version(self) -> str:
        return f"{self.profile_id}:{self.version}"

    def __post_init__(self) -> None:
        if not self.profile_id or not self.version:
            raise ValueError("profile_id and version are required")
        if not 0 <= self.active_hour_start <= 24 or not 0 <= self.active_hour_end <= 24:
            raise ValueError("active hours must be 0..24")
        if self.active_hour_start >= self.active_hour_end:
            raise ValueError("active_hour_start must be before active_hour_end")
        for weekday in self.active_weekdays:
            if weekday < 0 or weekday > 6:
                raise ValueError("active_weekdays must use Python weekday values 0..6")

    @classmethod
    def baseload(cls, *, profile_id: str, version: str) -> DeliveryProfile:
        return cls(
            profile_id=profile_id,
            version=version,
            name="baseload",
            active_weekdays=(0, 1, 2, 3, 4, 5, 6),
            active_hour_start=0,
            active_hour_end=24,
        )

    @classmethod
    def power_5x16(cls, *, profile_id: str, version: str) -> DeliveryProfile:
        return cls(
            profile_id=profile_id,
            version=version,
            name="5x16",
            active_weekdays=(0, 1, 2, 3, 4),
            active_hour_start=7,
            active_hour_end=23,
        )

    def active_days(self, period: DeliveryPeriod, calendar: VersionedCalendar) -> list[date]:
        days: list[date] = []
        current = period.delivery_start
        while current < period.delivery_end:
            if current.weekday() in self.active_weekdays and calendar.is_business_day(current):
                days.append(current)
            current += timedelta(days=1)
        return days

    def to_json_dict(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "version": self.version,
            "name": self.name,
            "active_weekdays": list(self.active_weekdays),
            "active_hour_start": self.active_hour_start,
            "active_hour_end": self.active_hour_end,
        }


@dataclass(frozen=True, slots=True)
class ExpiryRule:
    """Versioned expiry rule input."""

    rule_id: str
    version: str
    name: ExpiryRuleName

    @property
    def rule_version(self) -> str:
        return f"{self.rule_id}:{self.version}"

    def expiry_for_contract_month(
        self,
        *,
        contract_period: str,
        calendar: VersionedCalendar,
    ) -> CalendarResult:
        if self.name != "henry_ld1_third_business_day_prior":
            raise ValueError(f"unsupported expiry rule: {self.name}")
        year_text, month_text = contract_period.split("-")
        first_delivery_day = date(int(year_text), int(month_text), 1)
        expiry = calendar.add_business_days(first_delivery_day, -3)
        return CalendarResult(calendar_version=calendar.calendar_version, value_date=expiry)

    def to_json_dict(self) -> dict[str, object]:
        return {"rule_id": self.rule_id, "version": self.version, "name": self.name}


@dataclass(frozen=True, slots=True)
class SettlementAnchor:
    """Versioned settlement anchor input."""

    anchor_id: str
    version: str
    name: SettlementAnchorName
    calendar_version: str

    @property
    def anchor_version(self) -> str:
        return f"{self.anchor_id}:{self.version}"

    def to_json_dict(self) -> dict[str, object]:
        return {
            "anchor_id": self.anchor_id,
            "version": self.version,
            "name": self.name,
            "calendar_version": self.calendar_version,
        }
