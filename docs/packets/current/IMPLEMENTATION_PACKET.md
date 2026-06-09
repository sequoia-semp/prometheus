---
packet_type: implementation
packet_status: current
active_work_item: W-006
last_updated: 2026-06-09
repository: sequoia-semp/prometheus
stable_branch: main
working_branch: codex/w-006-calendar-expiry
preferred_branch_convention: codex/<work-item>-<slug>
packet_scope: branch-local-current
base_ref: main
head_ref: codex/w-006-calendar-expiry
canonical_sources:
  - AGENTS.md
  - README.md
  - docs/planning/SOURCE_OF_TRUTH.md
  - docs/planning/PACKET_WORKFLOW.md
  - docs/workscope/workscope.yaml
  - docs/codex/work_items/W-006-calendar-and-expiry-service.md
  - docs/adr/ADR-021-calendars-and-expiry-rules.md
  - docs/contracts/INSTRUMENT.md
  - docs/packets/current/PLANNING_PACKET.md
  - scripts/check_plan_freshness.py
  - tests/unit/test_packet_workflow.py
---

# Implementation Packet — W-006 Calendar and Expiry Service

## Task

Implement only W-006 calendar and expiry work:

- implement versioned calendars, expiry rules, delivery periods, delivery profiles, and settlement anchors;
- represent Henry last-trading-day/expiry reproducibly;
- represent power 5x16 delivery profiles without a schema fork;
- emit `calendar_version` into relevant outputs;
- keep date serialization deterministic.

Do not implement ICE, PJM, pricing, risk, Textual screens, Nautilus runtime behavior, or agent business logic.

## Branch Orientation

Base: `main`
Head: `codex/w-006-calendar-expiry`
Stable branch: `main`

## Files In Scope

```text
src/ata/calendars/**
tests/unit/**calendar**
docs/packets/current/** only if metadata needs refreshing
docs/workscope/workscope.yaml only for active-item status/metadata alignment
docs/codex/work_items/W-006-calendar-and-expiry-service.md
scripts/check_*.py only if active-work-item checks need updating
```

## Files Out Of Scope

```text
src/ata/pricing/** implementation
src/ata/risk/** implementation
src/ata/ice_sidecar/** runtime adapters
src/ata/pjm/** runtime client
src/ata/instruments/** changes beyond use of existing IDs/contracts
src/ata/blotter/** implementation changes
src/ata/agent/** runtime harness
src/ata/ui_textual/** screens
src/ata/nautilus/** runtime adapter
.ata_local/**
credentials/**
tokens/**
secrets/**
data/live/**
```

## Acceptance Criteria

- Henry last-trading-day/expiry rule is represented.
- Settlement anchors are versioned inputs.
- Power calendars and 5x16 delivery profiles can be versioned.
- `calendar_version` is emitted into relevant outputs.
- Default checks pass without ICE Connect/Python, PJM live data, Nautilus, Textual, GitHub Actions, release automation, or local LLM processes.
- No ICE/PJM/pricing/risk/UI/agent/Nautilus runtime behavior is added.

## Suggested Commands

```bash
git branch --show-current
git status --short
python3 scripts/check_plan_freshness.py
python3 scripts/check_invariants.py
uv run pytest
uv run ruff check .
uv run pyright
```

## Coding-agent Final Response

```json
{
  "work_item": "W-006",
  "base_ref": "main",
  "head_ref": "codex/w-006-calendar-expiry",
  "working_branch": "codex/w-006-calendar-expiry",
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
