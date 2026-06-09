---
packet_type: implementation
packet_status: current
active_work_item: W-008
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/codex/work_items/W-008-generic-instrument-model.md
---

# Implementation Packet — W-008 Generic Instrument Model

## Task

Implement generic commodity instrument identities and multiplier policies. Do not implement ICE, PJM, pricing, risk, Textual screens, Nautilus runtime behavior, or agent business logic yet.

## Files in scope

```text
src/ata/instruments/**
tests/unit/**instrument**
docs/packets/current/** if packet metadata needs refreshing
docs/workscope/workscope.yaml
docs/codex/work_items/W-008-generic-instrument-model.md
scripts/check_*.py if active-work-item checks need updating
```

## Files out of scope

```text
src/ata/pricing implementation
src/ata/risk implementation
src/ata/ice_sidecar runtime adapters
src/ata/pjm runtime client
src/ata/calendars expiry implementation
src/ata/agent runtime harness
src/ata/ui_textual screens
src/ata/nautilus runtime adapter
```

## Required instrument boundary

Implement contract-compatible instrument primitives:

- `InstrumentIdentity`
- `MultiplierPolicy`
- deterministic canonical string ID derived from typed fields
- deterministic JSON round-trip
- v0 unsupported-model marker for American options

Keep DTO boundaries JSON/Serde-friendly:

- Decimal payload values serialize as strings.
- Datetimes serialize as timezone-aware RFC3339 UTC.
- No pandas DataFrame, Python object graph, or framework object becomes a canonical boundary.

## Acceptance criteria

- Henry LD1 future modeled.
- European Henry option-on-future modeled with exercise_style and reference_future_id.
- American-style option is representable but rejected by v0 pricing model marker.
- Power 5x16 placeholder config works without schema fork.
- MultiplierPolicy has explicit policy_id and source/version.
- Instrument identity round-trips deterministically.
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
  "work_item": "W-008",
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
