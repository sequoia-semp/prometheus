# Risk Time Series

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-036

## Purpose

Expose position, PnL, Greeks, and VaR through time as derived batch revaluation snapshots.

## Shape

```python
class RiskTimeSeriesPoint:
    book_id: str
    snapshot_id: str
    as_of: datetime
    known_at: datetime
    resolution: str
    pv: Decimal
    pnl: dict | None
    greeks: dict
    var_p95: Decimal | None
    var_p99: Decimal | None
    market_snapshot_id: str
    book_version: str
    calculation_version: str
```

## Retention policy

- Hot cache: trailing 7 days of intraday batch revaluation snapshots.
- Resolution is configurable per instrument/book.
- One minute is a maximum target, not a global mandate.
- Beyond 7 days: downsample to EoD snapshots anchored to the relevant settlement convention.
- Source events remain immutable and rebuildable.

## Rules

- Every point carries full lineage IDs.
- Live-vs-replay must produce identical points at equal resolution.
- VaR points report both p95 and p99.
