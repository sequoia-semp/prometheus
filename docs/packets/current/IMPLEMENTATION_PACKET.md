---
packet_type: implementation
packet_status: current
active_work_item: W-009
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/codex/work_items/W-009-trade-blotter-and-position-projection.md
---

# Implementation Packet — W-009 Trade Blotter and Position Projection

## Task

Implement append-only trade blotter events and deterministic bitemporal position projection. Do not implement ICE, PJM, pricing, risk, Textual screens, Nautilus runtime behavior, or agent business logic yet.

## Files in scope

```text
src/ata/blotter/**
tests/unit/**blotter**
docs/packets/current/** if packet metadata needs refreshing
docs/workscope/workscope.yaml
docs/codex/work_items/W-009-trade-blotter-and-position-projection.md
scripts/check_*.py if active-work-item checks need updating
```

## Files out of scope

```text
src/ata/pricing implementation
src/ata/risk implementation
src/ata/ice_sidecar runtime adapters
src/ata/pjm runtime client
src/ata/calendars expiry implementation
src/ata/instruments changes beyond use of IDs
src/ata/agent runtime harness
src/ata/ui_textual screens
src/ata/nautilus runtime adapter
```

## Required blotter boundary

Implement contract-compatible blotter primitives:

- `TradeEvent`
- `Position`
- append-only `TradeBlotter`
- `position_as_of(as_of, known_at)`
- deterministic `book_version`

Keep DTO boundaries JSON/Serde-friendly:

- Decimal values serialize as strings.
- Datetimes serialize as timezone-aware RFC3339 UTC.
- No pandas DataFrame, Python object graph, or framework object becomes a canonical boundary.

## Acceptance criteria

- Trade events are append-only; amend/bust are new events referencing prior IDs.
- `position_as_of(as_of, known_at)` returns deterministic fold.
- `book_version` derives from applied trade-event set.
- Positions reproduce from event-store replay.
- Default checks pass without ICE Connect/Python, PJM live data, Nautilus, Textual, GitHub Actions, release automation, or local LLM processes.

## Suggested commands

The command set should be local-first and fast:

```bash
python3 scripts/check_plan_freshness.py
python3 scripts/check_invariants.py
uv run pytest
uv run ruff check .
uv run pyright
```

If the project chooses a different equivalent command, document it in README and AGENTS.

## Coding-agent final response

```json
{
  "work_item": "W-009",
  "summary": "",
  "files_changed": [],
  "tests_added": [],
  "tests_run": [],
  "acceptance_status": "met | partial | not_met",
  "out_of_scope_changes": [],
  "open_questions": [],
  "risks": []
}
```
