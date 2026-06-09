# Risk

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-016, ADR-019, ADR-036

## Purpose

Portfolio-level risk outputs computed by the single authoritative engine alongside PV, Greeks, and PnL.

## VaR

```python
class VarConfig:
    method: str                  # v0: historical_simulation
    horizon_days: int            # v0: 1
    confidence_levels: list[float]   # v0: [0.95, 0.99]
    lookback: str                # v0: 250bd
    return_basis: str            # v0: absolute_price_change
    option_scenario_policy: str  # v0: full_revalue_static_vol

class VarResult:
    market_snapshot_id: str
    book_version: str
    calculation_version: str
    as_of: datetime
    known_at: datetime
    method: str
    horizon_days: int
    confidence_levels: list[float]
    var_p95: Decimal
    var_p99: Decimal
    lookback: str
    return_basis: str
    option_scenario_policy: str
    source_event_ids: list[str]
    warnings: list[str]
```

## v0 policy

- Report both p95 and p99 1-day VaR.
- Use historical simulation over `known_at`-consistent market series.
- Default lookback is trailing 250 business days.
- Use absolute price-change scenarios for v0 commodity futures/options.
- Options are fully repriced under Black-76 using shocked underlying prices and static v0 vol.
- Vol-shock VaR models are deferred to a later ADR.
- VaR is reported as a positive loss number.
- VaR carries the same lineage IDs as every other numerical output.
