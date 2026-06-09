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
  - docs/packets/templates/IMPLEMENTATION_PACKET_TEMPLATE.md
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

## Coding-agent final response

Return both structured JSON and a human-readable handoff.

### Structured JSON

```json
{
  "work_item": "W-006",
  "repository": "sequoia-semp/prometheus",
  "base_ref": "main",
  "head_ref": "codex/w-006-calendar-expiry",
  "working_branch": "codex/w-006-calendar-expiry",
  "implementation_base_commit": "",
  "implementation_head_commit": "",
  "summary": "",
  "changed_files": [],
  "files_changed": [],
  "tests_added": [],
  "tests_run": [],
  "tests_not_run": [],
  "acceptance_status": "met | partial | not_met",
  "out_of_scope_changes": [],
  "open_questions": [],
  "risks": [],
  "review_packet_path": "docs/packets/current/REVIEW_PACKET.md",
  "planning_packet_path": "docs/packets/current/PLANNING_PACKET.md",
  "implementation_packet_path": "docs/packets/current/IMPLEMENTATION_PACKET.md",
  "reconciliation_packet_path": "docs/packets/current/RECONCILIATION_PACKET.md"
}
```

### Human handoff

```text
Implementation pass complete.

Repository: sequoia-semp/prometheus
Work item: W-006
Working branch: codex/w-006-calendar-expiry
Review base: main
Review head: codex/w-006-calendar-expiry
Implementation commit range: <base_commit>..<head_commit>

Files changed:
- <file>

Tests/checks run:
- <command>: <pass/fail/not run>

Acceptance status:
- <met | partial | not_met>
- Notes: <brief notes>

Out-of-scope changes:
- <none or list>

Known risks / open questions:
- <none or list>

Reviewer read order:
1. AGENTS.md
2. docs/packets/current/PLANNING_PACKET.md
3. docs/packets/current/REVIEW_PACKET.md
4. This coding-agent handoff
5. The implementation diff for the commit range above

Paste this to the adversarial reviewer:

---
Please review the implementation pass for <WORK_ITEM>.

Repository: sequoia-semp/prometheus
Working branch: <WORKING_BRANCH>
Review base: <BASE_REF or BASE_COMMIT>
Review head: <HEAD_REF or HEAD_COMMIT>
Implementation commit range: <BASE_COMMIT>..<HEAD_COMMIT>

Read in this order:
1. AGENTS.md
2. docs/packets/current/PLANNING_PACKET.md
3. docs/packets/current/REVIEW_PACKET.md
4. Coding-agent handoff below
5. Diff for the commit range above

Review against the packet's declared scope and blocking findings. First verify packet branch metadata. Do not compare against unrelated main state or stale packets.
---

After review, paste this to the reconciliation/planning instance:

---
Please reconcile the completed review for <WORK_ITEM>.

Repository: sequoia-semp/prometheus
Working branch: <WORKING_BRANCH>
Review base: <BASE_REF or BASE_COMMIT>
Review head: <HEAD_REF or HEAD_COMMIT>

Read in this order:
1. AGENTS.md
2. docs/packets/current/PLANNING_PACKET.md
3. docs/packets/current/RECONCILIATION_PACKET.md
4. Coding-agent handoff
5. Review JSON/result
6. Human/user dispositions

Close the loop by dispositioning findings, updating canonical docs if needed, updating workscope status, refreshing packets and manifest, and selecting the next active work item.
---
```
