# ADR-035 — Trade Blotter to Position Projection

Status: accepted
Date: 2026-06-09

## Decision

The trade blotter is append-only. Current position is a deterministic fold over trade events, not a separately maintained mutable balance.

## Consequences

- Amendments and busts are new events referencing prior trade IDs.
- `position_as_of(as_of, known_at)` is the bitemporal fold.
- `book_version` derives from applied trade-event IDs and is an input to pricing/risk.
