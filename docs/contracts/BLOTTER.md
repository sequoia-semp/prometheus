# Blotter

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-035

## Purpose

The trade blotter is the append-only record of trade events. Current position is a deterministic fold over the blotter, never a separately maintained mutable balance.

## Shape

```python
class TradeEvent:
    event_id: str
    stream_id: str
    stream_sequence: int
    instrument_id: str
    quantity: Decimal
    price: Decimal
    trade_time: datetime
    known_at: datetime
    kind: str                    # new | amend | bust
    amends_event_id: str | None
    source_event_ids: list[str]

class Position:
    instrument_id: str
    quantity: Decimal
    book_version: str
    as_of: datetime
    known_at: datetime
    source_event_ids: list[str]
```

## Rules

- Amendments and busts are new events referencing prior `event_id`.
- `position_as_of(as_of, known_at)` folds events with `trade_time <= as_of` and `known_at <= known_at`.
- `book_version` derives from applied trade-event IDs.
- Positions are inputs to portfolio revaluation, risk time series, and agent tools.
