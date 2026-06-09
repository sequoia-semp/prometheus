---
packet_type: implementation
packet_status: current
active_work_item: W-006
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/codex/work_items/W-006-calendar-and-expiry-service.md
---

# Implementation Packet — W-006 Calendar and Expiry Service

## Task

Implement versioned calendars, expiry rules, delivery periods, delivery profiles, and settlement anchors. Do not implement ICE, PJM, pricing, risk, Textual screens, Nautilus runtime behavior, or agent business logic yet.

## Files in scope

```text
src/ata/calendars/**
tests/unit/**calendar**
docs/packets/current/** if packet metadata needs refreshing
docs/workscope/workscope.yaml
docs/codex/work_items/W-006-calendar-and-expiry-service.md
scripts/check_*.py if active-work-item checks need updating
```

## Files out of scope

```text
src/ata/pricing implementation
src/ata/risk implementation
src/ata/ice_sidecar runtime adapters
src/ata/pjm runtime client
src/ata/instruments changes beyond use of IDs
src/ata/blotter implementation changes
src/ata/agent runtime harness
src/ata/ui_textual screens
src/ata/nautilus runtime adapter
```

## Required calendar boundary

Implement contract-compatible calendar primitives:

- versioned calendar object
- Henry last-trading-day/expiry rule representation
- settlement anchors as versioned inputs
- delivery periods for contract months
- power 5x16 delivery profile representation
- outputs carrying `calendar_version`

Keep DTO boundaries JSON/Serde-friendly:

- Dates serialize as ISO dates.
- No pandas DataFrame, Python object graph, or framework object becomes a canonical boundary.

## Acceptance criteria

- Henry last-trading-day/expiry rule is represented.
- Settlement anchors are versioned inputs.
- Power calendars and 5x16 delivery profiles can be versioned.
- `calendar_version` is emitted into relevant outputs.
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
  "work_item": "W-006",
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
