---
packet_type: implementation
packet_status: current
active_work_item: W-007
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/codex/work_items/W-007-event-envelope-and-bitemporal-store.md
---

# Implementation Packet — W-007 Event Envelope and Bitemporal Store

## Task

Implement append-only event envelopes and a local bitemporal event store. Do not implement ICE, PJM, pricing, risk, Textual screens, Nautilus runtime behavior, or agent business logic yet.

## Files in scope

```text
src/ata/events/**
tests/unit/**event**
tests/integration/**event**
docs/packets/current/** if packet metadata needs refreshing
docs/workscope/workscope.yaml
docs/codex/work_items/W-007-event-envelope-and-bitemporal-store.md
scripts/check_*.py if active-work-item checks need updating
```

## Files out of scope

```text
src/ata/ice_sidecar runtime adapters
src/ata/pjm runtime client
src/ata/pricing implementation
src/ata/risk implementation
src/ata/agent runtime harness
src/ata/ui_textual screens
src/ata/nautilus runtime adapter
.ata_local/**
data/live/**
credentials/**
real ICE/PJM data dumps
```

## Required event boundary

Implement contract-compatible event primitives:

- `EventEnvelope`
- append-only `EventStore`
- `append`
- `iter_stream`
- `query(as_of, known_at)`
- deterministic `snapshot_id`
- JSONL export/import

Keep DTO boundaries JSON/Serde-friendly:

- Decimal payload values serialize as strings.
- Datetimes serialize as timezone-aware RFC3339 UTC.
- No pandas DataFrame, Python object graph, or framework object becomes a canonical boundary.

## Acceptance criteria

- Append-only event API exists.
- Per-stream ordering works.
- Bitemporal query by `as_of` and `known_at` works.
- Snapshot IDs are deterministic.
- Envelope carries `source_system` and `data_scope`.
- JSONL import/export exists for local sidecar/spool compatibility.
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
  "work_item": "W-007",
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
