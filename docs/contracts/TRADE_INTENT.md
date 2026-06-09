# Trade Intent

Status: future_contract
Last updated: 2026-06-09
Backing ADR: ADR-025

## Purpose

A later-stage structured object for trade proposals. It is not executable by an LLM.

```python
class TradeIntent:
    intent_id: str
    hypothesis: str
    instruments: list[str]
    side: str
    quantity: Decimal
    max_entry_price: Decimal | None
    required_market_snapshot_id: str
    required_data_freshness_seconds: int
    risk_budget: dict
    scenario_results: dict
    var_impact: Decimal
    evidence_tool_calls: list[str]
```

## Rule

A `TradeIntent` may be staged only after deterministic validation. It may not be submitted directly by an LLM.
