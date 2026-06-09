from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from ata.instruments import InstrumentIdentity, MultiplierPolicy


def henry_multiplier() -> MultiplierPolicy:
    return MultiplierPolicy(
        policy_id="henry-ld1-10000-mmbtu-v1",
        unit="MMBtu",
        contract_size=Decimal("10000"),
        applies_flow_day_multiplier=False,
        flow_days_in_period=None,
        source="ICE",
        version="v1",
    )


def henry_future() -> InstrumentIdentity:
    return InstrumentIdentity(
        commodity="natural_gas",
        market="henry_hub",
        venue="ICE",
        product="LD1",
        delivery_location="Henry Hub",
        delivery_profile="baseload",
        contract_period="2026-06",
        instrument_type="future",
        quote_unit="USD/MMBtu",
        settlement_currency="USD",
        option_right=None,
        exercise_style=None,
        strike=None,
        expiry=None,
        reference_future_id=None,
        multiplier_policy_id=henry_multiplier().policy_id,
    )


def test_multiplier_policy_has_explicit_lineage_and_round_trips() -> None:
    policy = henry_multiplier()
    round_tripped = MultiplierPolicy.from_json_line(policy.to_json_line())

    assert policy.policy_id == "henry-ld1-10000-mmbtu-v1"
    assert policy.source == "ICE"
    assert policy.version == "v1"
    assert policy.to_json_line() == round_tripped.to_json_line()


def test_henry_ld1_future_identity_round_trips_deterministically() -> None:
    future = henry_future()
    round_tripped = InstrumentIdentity.from_json_line(future.to_json_line())

    assert future.instrument_type == "future"
    assert future.pricing_support == "supported"
    assert future.canonical_id == round_tripped.canonical_id
    assert future.to_json_line() == round_tripped.to_json_line()
    assert future.canonical_id.startswith("inst:natural_gas:henry_hub:ice:ld1:")


def test_european_henry_option_on_future_is_supported() -> None:
    future = henry_future()
    option = InstrumentIdentity(
        commodity="natural_gas",
        market="henry_hub",
        venue="ICE",
        product="LD1_option",
        delivery_location="Henry Hub",
        delivery_profile="baseload",
        contract_period="2026-06",
        instrument_type="option_on_future",
        quote_unit="USD/MMBtu",
        settlement_currency="USD",
        option_right="call",
        exercise_style="european",
        strike=Decimal("3.000"),
        expiry=date(2026, 5, 26),
        reference_future_id=future.canonical_id,
        multiplier_policy_id=henry_multiplier().policy_id,
    )

    assert option.reference_future_id == future.canonical_id
    assert option.pricing_support == "supported"
    round_tripped = InstrumentIdentity.from_json_line(option.to_json_line())
    assert round_tripped.canonical_id == option.canonical_id


def test_american_option_is_representable_but_unsupported_for_v0_pricing() -> None:
    future = henry_future()
    option = InstrumentIdentity(
        commodity="natural_gas",
        market="henry_hub",
        venue="ICE",
        product="LD1_option",
        delivery_location="Henry Hub",
        delivery_profile="baseload",
        contract_period="2026-06",
        instrument_type="option_on_future",
        quote_unit="USD/MMBtu",
        settlement_currency="USD",
        option_right="put",
        exercise_style="american",
        strike=Decimal("2.500"),
        expiry=date(2026, 5, 26),
        reference_future_id=future.canonical_id,
        multiplier_policy_id=henry_multiplier().policy_id,
    )

    assert option.pricing_support == "unsupported_v0"


def test_option_requires_option_specific_fields() -> None:
    with pytest.raises(ValueError, match="option_on_future missing required fields"):
        InstrumentIdentity(
            commodity="natural_gas",
            market="henry_hub",
            venue="ICE",
            product="LD1_option",
            delivery_location="Henry Hub",
            delivery_profile="baseload",
            contract_period="2026-06",
            instrument_type="option_on_future",
            quote_unit="USD/MMBtu",
            settlement_currency="USD",
            option_right="call",
            exercise_style="european",
            strike=None,
            expiry=None,
            reference_future_id=None,
            multiplier_policy_id=henry_multiplier().policy_id,
        )


def test_power_5x16_placeholder_uses_same_identity_schema() -> None:
    power_policy = MultiplierPolicy(
        policy_id="pjm-westhub-5x16-v0",
        unit="MWh",
        contract_size=Decimal("1"),
        applies_flow_day_multiplier=True,
        flow_days_in_period=21,
        source="placeholder",
        version="v0",
    )
    power = InstrumentIdentity(
        commodity="power",
        market="PJM",
        venue="ICE",
        product="financial_power",
        delivery_location="PJM West Hub",
        delivery_profile="5x16",
        contract_period="2026-07",
        instrument_type="swap",
        quote_unit="USD/MWh",
        settlement_currency="USD",
        option_right=None,
        exercise_style=None,
        strike=None,
        expiry=None,
        reference_future_id=None,
        multiplier_policy_id=power_policy.policy_id,
    )

    assert power.delivery_profile == "5x16"
    assert power_policy.applies_flow_day_multiplier is True
    assert power.canonical_id.startswith("inst:power:pjm:ice:financial_power:")
    round_tripped = InstrumentIdentity.from_json_line(power.to_json_line())
    assert round_tripped.canonical_id == power.canonical_id
