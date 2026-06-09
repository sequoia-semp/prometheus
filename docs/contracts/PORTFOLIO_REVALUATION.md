# Portfolio Revaluation

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-033

## Purpose

Define the live portfolio view as a batch revaluation read-model over the append-only event store and the single authoritative pricer/risk engine.

## Core principle

Each market-data refresh creates or coalesces into a run of the one engine, published with full lineage. Same inputs must produce the same numbers under live-style run and replay.

## Snapshot

```python
class PortfolioRevaluationSnapshot:
    snapshot_id: str
    book_id: str
    book_version: str
    market_snapshot_id: str
    calculation_version: str
    as_of: datetime
    known_at: datetime
    knowledge_time: datetime
    positions: list[PositionView]
    pv: Decimal
    greeks: dict
    pnl: dict | None
    var: dict | None
    source_event_ids: list[str]
    warnings: list[str]
    supersedes_snapshot_id: str | None

class PositionView:
    instrument_id: str
    quantity: Decimal
    multiplier_policy_id: str
    pv: Decimal
    greeks: dict

class RevaluationCheckpoint:
    book_id: str
    last_stream_sequence_by_stream: dict
    last_snapshot_id: str
    knowledge_time: datetime
```

## Loop semantics

- Trigger: market-data refresh while live, target around one minute when practical.
- Bursts may be coalesced, but the converged snapshot must equal the uncoalesced deterministic result.
- Transport is an implementation detail.
- The view never mutates orders, positions, source events, or valuation inputs.

## Correctness rules

1. Every snapshot carries `market_snapshot_id`, `book_version`, `calculation_version`, and `source_event_ids`.
2. Live-style and replay runs produce identical snapshots for identical inputs.
3. Corrections emit superseding snapshots; past snapshots are never mutated.
4. The loop calls the authoritative pricer/risk engine only.
5. Out-of-order events are ordered per `stream_id`; no global sequence assumption.
