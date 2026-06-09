# Instrument Model

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-026, ADR-030, ADR-031

## Typed identity

```python
class InstrumentIdentity:
    commodity: str
    market: str
    venue: str
    product: str
    delivery_location: str
    delivery_profile: str
    contract_period: str
    instrument_type: str          # future | option_on_future | swap | physical | observation
    quote_unit: str
    settlement_currency: str
    option_right: str | None      # call | put
    exercise_style: str | None    # european | american | bermudan
    strike: Decimal | None
    expiry: date | None
    reference_future_id: str | None
    multiplier_policy_id: str
```

The canonical string ID is derived from the typed object. The string is not the source of truth.

## Multiplier policy

```python
class MultiplierPolicy:
    policy_id: str
    unit: str
    contract_size: Decimal
    applies_flow_day_multiplier: bool
    flow_days_in_period: int | None
    source: str
    version: str
```

## v0 instruments

- Henry LD1 future.
- European Henry option-on-future with explicit `reference_future_id`.
- Power 5x16 placeholder config to prove the model does not fork by vertical.

## Rules

- Options require `exercise_style`, `option_right`, `strike`, `expiry`, and `reference_future_id`.
- American-style options are rejected in v0 by the pricer/model selector.
- Multiplier policy ID is part of valuation lineage.
