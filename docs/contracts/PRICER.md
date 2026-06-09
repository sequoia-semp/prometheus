# Pricer

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-016, ADR-019, ADR-031

## Batch pricer interface

```python
class PricingRequest:
    as_of: datetime
    known_at: datetime
    market_snapshot_id: str
    book_version: str
    positions: list[Position]
    scenarios: list[Scenario] | None

class PricingResult:
    request_id: str
    market_snapshot_id: str
    book_version: str
    calculation_version: str
    pv: Decimal
    greeks: dict
    pnl: dict | None
    source_event_ids: list[str]
    warnings: list[str]
```

## Rules

- One revaluation engine is authoritative.
- Greeks v0 are bump-and-revalue unless otherwise approved by ADR.
- All numbers carry snapshot/version identifiers.
- Option pricing v0 uses Black-76 for European options-on-futures.
- American-style options are rejected in v0 by a typed unsupported-model error.
