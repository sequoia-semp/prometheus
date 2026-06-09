# W-009 — Trade Blotter and Position Projection

Status: active
Depends on: W-007, W-008

## Objective

Implement append-only trade blotter events and deterministic bitemporal position projection without adding pricing, risk, source adapters, UI screens, Nautilus runtime behavior, or agent runtime behavior.

## Files in scope

```text
src/ata/blotter/**
tests/unit/**blotter**
docs/packets/current/**
docs/workscope/workscope.yaml
docs/codex/work_items/W-009-trade-blotter-and-position-projection.md
scripts/check_*.py if active-work-item checks need updating
```

## Required behavior

- Append-only trade event API.
- Trade amendments and busts are new events referencing prior event IDs.
- `position_as_of(as_of, known_at)` folds events with `trade_time <= as_of` and `known_at <= known_at`.
- `book_version` derives deterministically from applied trade-event IDs.
- Positions reproduce from replaying trade events.

## Acceptance criteria

- Trade events are append-only; amend/bust are new events referencing prior IDs.
- `position_as_of(as_of, known_at)` returns deterministic fold.
- `book_version` derives from applied trade-event set.
- Positions reproduce from event-store replay.
- Default checks pass without ICE Connect/Python, PJM live data, Nautilus, Textual, GitHub Actions, release automation, or local LLM processes.
