"""Generic commodity instrument identities and multiplier policies."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Literal, TypeAlias, cast

InstrumentType: TypeAlias = Literal[
    "future",
    "option_on_future",
    "swap",
    "physical",
    "observation",
]
OptionRight: TypeAlias = Literal["call", "put"]
ExerciseStyle: TypeAlias = Literal["european", "american", "bermudan"]
PricingSupport: TypeAlias = Literal["supported", "unsupported_v0"]


def _decimal_to_json(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value)


def _decimal_from_json(value: object, field_name: str) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a decimal string or null")
    return Decimal(value)


def _date_to_json(value: date | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def _date_from_json(value: object, field_name: str) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO date string or null")
    return date.fromisoformat(value)


def _required_str(data: dict[str, object], key: str) -> str:
    value = data[key]
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _optional_str(data: dict[str, object], key: str) -> str | None:
    value = data[key]
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string or null")
    return value


def _required_bool(data: dict[str, object], key: str) -> bool:
    value = data[key]
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be a bool")
    return value


def _optional_int(data: dict[str, object], key: str) -> int | None:
    value = data[key]
    if value is None:
        return None
    if not isinstance(value, int):
        raise ValueError(f"{key} must be an integer or null")
    return value


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _slug(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("/", "-")


@dataclass(frozen=True, slots=True)
class MultiplierPolicy:
    """Contract multiplier and flow-day policy with explicit lineage."""

    policy_id: str
    unit: str
    contract_size: Decimal
    applies_flow_day_multiplier: bool
    flow_days_in_period: int | None
    source: str
    version: str

    def __post_init__(self) -> None:
        for field_name in ["policy_id", "unit", "source", "version"]:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")
        if self.contract_size <= 0:
            raise ValueError("contract_size must be positive")
        if self.applies_flow_day_multiplier and self.flow_days_in_period is None:
            raise ValueError("flow_days_in_period is required when flow-day multiplier applies")
        if self.flow_days_in_period is not None and self.flow_days_in_period <= 0:
            raise ValueError("flow_days_in_period must be positive when provided")

    def to_json_dict(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "unit": self.unit,
            "contract_size": str(self.contract_size),
            "applies_flow_day_multiplier": self.applies_flow_day_multiplier,
            "flow_days_in_period": self.flow_days_in_period,
            "source": self.source,
            "version": self.version,
        }

    def to_json_line(self) -> str:
        return _canonical_json(self.to_json_dict())

    @classmethod
    def from_json_dict(cls, data: dict[str, object]) -> MultiplierPolicy:
        contract_size = _decimal_from_json(data["contract_size"], "contract_size")
        if contract_size is None:
            raise ValueError("contract_size is required")
        return cls(
            policy_id=_required_str(data, "policy_id"),
            unit=_required_str(data, "unit"),
            contract_size=contract_size,
            applies_flow_day_multiplier=_required_bool(data, "applies_flow_day_multiplier"),
            flow_days_in_period=_optional_int(data, "flow_days_in_period"),
            source=_required_str(data, "source"),
            version=_required_str(data, "version"),
        )

    @classmethod
    def from_json_line(cls, line: str) -> MultiplierPolicy:
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError("multiplier policy JSON must contain an object")
        return cls.from_json_dict(cast(dict[str, object], data))


@dataclass(frozen=True, slots=True)
class InstrumentIdentity:
    """Typed commodity instrument identity.

    The canonical string ID is derived from these typed fields and is never the
    source of truth.
    """

    commodity: str
    market: str
    venue: str
    product: str
    delivery_location: str
    delivery_profile: str
    contract_period: str
    instrument_type: InstrumentType
    quote_unit: str
    settlement_currency: str
    option_right: OptionRight | None
    exercise_style: ExerciseStyle | None
    strike: Decimal | None
    expiry: date | None
    reference_future_id: str | None
    multiplier_policy_id: str

    def __post_init__(self) -> None:
        required = [
            "commodity",
            "market",
            "venue",
            "product",
            "delivery_location",
            "delivery_profile",
            "contract_period",
            "instrument_type",
            "quote_unit",
            "settlement_currency",
            "multiplier_policy_id",
        ]
        for field_name in required:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")

        if self.instrument_type == "option_on_future":
            missing = [
                field_name
                for field_name in [
                    "option_right",
                    "exercise_style",
                    "strike",
                    "expiry",
                    "reference_future_id",
                ]
                if getattr(self, field_name) is None
            ]
            if missing:
                raise ValueError("option_on_future missing required fields: " + ", ".join(missing))
        elif any(
            value is not None
            for value in [
                self.option_right,
                self.exercise_style,
                self.strike,
                self.expiry,
                self.reference_future_id,
            ]
        ):
            raise ValueError("non-option instruments cannot carry option-specific fields")

    @property
    def canonical_id(self) -> str:
        semantic = ":".join(
            [
                _slug(self.commodity),
                _slug(self.market),
                _slug(self.venue),
                _slug(self.product),
                _slug(self.delivery_location),
                _slug(self.delivery_profile),
                _slug(self.contract_period),
                _slug(self.instrument_type),
            ]
        )
        digest = hashlib.sha256(self.to_json_line().encode("utf-8")).hexdigest()[:16]
        return f"inst:{semantic}:{digest}"

    @property
    def pricing_support(self) -> PricingSupport:
        if self.instrument_type == "option_on_future" and self.exercise_style != "european":
            return "unsupported_v0"
        return "supported"

    def to_json_dict(self) -> dict[str, object]:
        return {
            "commodity": self.commodity,
            "market": self.market,
            "venue": self.venue,
            "product": self.product,
            "delivery_location": self.delivery_location,
            "delivery_profile": self.delivery_profile,
            "contract_period": self.contract_period,
            "instrument_type": self.instrument_type,
            "quote_unit": self.quote_unit,
            "settlement_currency": self.settlement_currency,
            "option_right": self.option_right,
            "exercise_style": self.exercise_style,
            "strike": _decimal_to_json(self.strike),
            "expiry": _date_to_json(self.expiry),
            "reference_future_id": self.reference_future_id,
            "multiplier_policy_id": self.multiplier_policy_id,
        }

    def to_json_line(self) -> str:
        return _canonical_json(self.to_json_dict())

    @classmethod
    def from_json_dict(cls, data: dict[str, object]) -> InstrumentIdentity:
        return cls(
            commodity=_required_str(data, "commodity"),
            market=_required_str(data, "market"),
            venue=_required_str(data, "venue"),
            product=_required_str(data, "product"),
            delivery_location=_required_str(data, "delivery_location"),
            delivery_profile=_required_str(data, "delivery_profile"),
            contract_period=_required_str(data, "contract_period"),
            instrument_type=cast(InstrumentType, _required_str(data, "instrument_type")),
            quote_unit=_required_str(data, "quote_unit"),
            settlement_currency=_required_str(data, "settlement_currency"),
            option_right=cast(OptionRight | None, _optional_str(data, "option_right")),
            exercise_style=cast(ExerciseStyle | None, _optional_str(data, "exercise_style")),
            strike=_decimal_from_json(data["strike"], "strike"),
            expiry=_date_from_json(data["expiry"], "expiry"),
            reference_future_id=_optional_str(data, "reference_future_id"),
            multiplier_policy_id=_required_str(data, "multiplier_policy_id"),
        )

    @classmethod
    def from_json_line(cls, line: str) -> InstrumentIdentity:
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError("instrument identity JSON must contain an object")
        return cls.from_json_dict(cast(dict[str, Any], data))
