from __future__ import annotations

from datetime import date

from ata.calendars import (
    DeliveryPeriod,
    DeliveryProfile,
    ExpiryRule,
    SettlementAnchor,
    VersionedCalendar,
)


def exchange_calendar() -> VersionedCalendar:
    return VersionedCalendar(
        calendar_id="ice-us-business",
        version="2026a",
        timezone="America/New_York",
        weekend_days=(5, 6),
        holidays=frozenset({date(2026, 5, 25), date(2026, 7, 3)}),
        source="fixture",
    )


def test_calendar_round_trips_with_versioned_inputs() -> None:
    calendar = exchange_calendar()
    round_tripped = VersionedCalendar.from_json_line(calendar.to_json_line())

    assert calendar.calendar_version == "ice-us-business:2026a"
    assert round_tripped.to_json_line() == calendar.to_json_line()
    assert not calendar.is_business_day(date(2026, 5, 25))


def test_henry_last_trading_day_rule_is_represented() -> None:
    calendar = exchange_calendar()
    rule = ExpiryRule(
        rule_id="henry-ld1-expiry",
        version="v1",
        name="henry_ld1_third_business_day_prior",
    )

    result = rule.expiry_for_contract_month(contract_period="2026-06", calendar=calendar)

    assert result.value_date == date(2026, 5, 27)
    assert result.calendar_version == calendar.calendar_version


def test_contract_month_delivery_period_emits_calendar_version() -> None:
    calendar = exchange_calendar()

    period = DeliveryPeriod.contract_month(calendar=calendar, contract_period="2026-06")

    assert period.delivery_start == date(2026, 6, 1)
    assert period.delivery_end == date(2026, 7, 1)
    assert period.to_json_dict()["calendar_version"] == "ice-us-business:2026a"


def test_settlement_anchor_is_versioned_input() -> None:
    calendar = exchange_calendar()

    anchor = SettlementAnchor(
        anchor_id="henry-settle",
        version="v1",
        name="exchange_settlement",
        calendar_version=calendar.calendar_version,
    )

    assert anchor.anchor_version == "henry-settle:v1"
    assert anchor.to_json_dict()["calendar_version"] == calendar.calendar_version


def test_power_5x16_profile_is_versioned_without_schema_fork() -> None:
    calendar = exchange_calendar()
    profile = DeliveryProfile.power_5x16(profile_id="pjm-5x16", version="v0")
    period = DeliveryPeriod.contract_month(calendar=calendar, contract_period="2026-07")

    active_days = profile.active_days(period, calendar)

    assert profile.profile_version == "pjm-5x16:v0"
    assert profile.name == "5x16"
    assert all(day.weekday() < 5 for day in active_days)
    assert date(2026, 7, 3) not in active_days
    assert date(2026, 7, 6) in active_days


def test_baseload_profile_includes_weekends_when_calendar_allows() -> None:
    calendar = VersionedCalendar(
        calendar_id="all-days",
        version="v1",
        timezone="UTC",
        weekend_days=(),
        holidays=frozenset(),
        source="fixture",
    )
    profile = DeliveryProfile.baseload(profile_id="all-hours", version="v1")
    period = DeliveryPeriod(
        calendar_version=calendar.calendar_version,
        delivery_start=date(2026, 6, 6),
        delivery_end=date(2026, 6, 8),
    )

    assert profile.active_days(period, calendar) == [date(2026, 6, 6), date(2026, 6, 7)]
