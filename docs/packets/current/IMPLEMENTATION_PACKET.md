---
packet_type: implementation
packet_status: current
active_work_item: W-000B
last_updated: 2026-06-09
repository: sequoia-semp/prometheus
stable_branch: main
working_branch: codex/workflow-branch-packets
preferred_branch_convention: codex/<work-item>-<slug>
packet_scope: branch-local-current
base_ref: codex/w-006-calendar-expiry
head_ref: codex/workflow-branch-packets
canonical_sources:
  - AGENTS.md
  - README.md
  - docs/planning/SOURCE_OF_TRUTH.md
  - docs/planning/PACKET_WORKFLOW.md
  - docs/workscope/workscope.yaml
  - docs/codex/work_items/W-000B-branch-local-packet-workflow-hardening.md
  - docs/packets/current/PLANNING_PACKET.md
  - scripts/check_plan_freshness.py
  - tests/unit/test_packet_workflow.py
---

# Implementation Packet — W-000B Branch-local Packet Workflow Hardening

## Task

Reorient this branch as a process/workflow-hardening branch. Define branch-local packet semantics, update packet metadata, remove stale W-001 active-task language, add W-000B workscope/work-item context, and harden freshness checks so future planning/coding/review/reconciliation instances inspect the correct branch state.

Do not implement W-006 calendar logic or any runtime ICE/PJM/pricing/risk/UI/agent/Nautilus behavior.

## Branch Orientation

Base: `codex/w-006-calendar-expiry`
Head: `codex/workflow-branch-packets`
Merge target: `codex/w-006-calendar-expiry`
Stable branch: `main`

Do not merge this branch directly to `main`.

## Files In Scope

```text
AGENTS.md
README.md
docs/planning/SOURCE_OF_TRUTH.md
docs/planning/PACKET_WORKFLOW.md
docs/workscope/workscope.yaml
docs/codex/work_items/W-000B-branch-local-packet-workflow-hardening.md
docs/packets/current/**
scripts/check_plan_freshness.py
scripts/check_invariants.py if needed
tests/unit/test_packet_workflow.py
```

## Files Out Of Scope

```text
src/ata/calendars/** domain implementation
src/ata/events/** domain implementation
src/ata/instruments/** domain implementation
src/ata/blotter/** domain implementation
src/ata/pricing/** implementation
src/ata/risk/** implementation
src/ata/ice_sidecar/** runtime ICE adapter implementation
src/ata/pjm/** runtime PJM client implementation
src/ata/agent/** runtime agent harness implementation
src/ata/ui_textual/** runtime UI implementation
src/ata/nautilus/** runtime Nautilus adapter implementation
.ata_local/**
credentials/**
tokens/**
secrets/**
data/live/**
```

## Acceptance Criteria

- AGENTS, README, SOURCE_OF_TRUTH, and PACKET_WORKFLOW define main/codex/review/reconcile branch policy.
- Current packet frontmatter includes branch metadata.
- Current packets describe W-000B, not W-006 calendar implementation, on this branch.
- PACKET_MANIFEST.yaml covers all canonical_sources referenced by current packets.
- Freshness checks detect active-work-item mismatch, missing branch metadata, missing canonical source files, missing manifest coverage, and hash mismatches.
- Freshness tests cover active-work-item mismatch, branch metadata mismatch, branch-name mismatch, missing canonical source files, missing manifest coverage, and hash mismatches.
- Stale W-001 active-task language is removed.
- No W-006 calendar domain implementation or runtime behavior is added.

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
  "work_item": "W-000B",
  "base_ref": "codex/w-006-calendar-expiry",
  "head_ref": "codex/workflow-branch-packets",
  "working_branch": "codex/workflow-branch-packets",
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
