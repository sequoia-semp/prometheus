---
packet_type: reconciliation
packet_status: current
active_work_item: W-006
reconciliation_target: W-006
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
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/packets/current/REVIEW_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/reviews/REVIEW_LOG.md
  - docs/codex/work_items/W-006-calendar-and-expiry-service.md
  - scripts/check_plan_freshness.py
  - tests/unit/test_packet_workflow.py
---

# Reconciliation Packet — W-006 Calendar and Expiry Service

## Purpose

Use this packet after W-006 coding and review outputs are available. Its job is to close the calendar and expiry service work item, disposition review findings, and select the next active packet set.

The next active item after W-006 will normally be W-003 unless review or reconciliation chooses otherwise.

## Required Closeout Inputs

A reconciliation instance should receive:

- `AGENTS.md`;
- `docs/packets/current/PLANNING_PACKET.md`;
- `docs/packets/current/RECONCILIATION_PACKET.md`;
- coding-agent final JSON/handoff;
- review JSON/result;
- human/user dispositions.

If the coding-agent handoff lacks branch, commit range, changed files, tests, or packet paths, record that as a process finding and decide whether it blocks closeout.

## Required Inputs

```text
AGENTS.md
docs/packets/current/PLANNING_PACKET.md
docs/packets/current/IMPLEMENTATION_PACKET.md
Coding-agent final JSON/handoff
Review JSON result
Human/user dispositions
```

## Reconciliation Steps

1. Identify whether W-006 met acceptance criteria.
2. Convert review findings into `accepted`, `rejected`, or `deferred` rows.
3. For accepted findings, update the relevant canonical file: ADR, contract, workscope, packet workflow, tests/checks, or README/AGENTS.
4. For rejected findings, add rationale to `docs/reviews/REJECTED_FINDINGS.md`.
5. For deferred findings, create or update a work item or `OPEN_QUESTIONS.md` row.
6. Update `docs/reviews/REVIEW_LOG.md`.
7. Update `docs/workscope/workscope.yaml` status for W-006.
8. Refresh current packet metadata and manifest if referenced sources changed.
9. Select the next active work item, normally W-003.

## W-006 Closeout Rule

Do not mark W-006 done unless:

- Henry last-trading-day/expiry rule is represented reproducibly;
- settlement anchors are explicit versioned inputs;
- power 5x16 delivery profiles can be represented without schema fork;
- relevant outputs carry `calendar_version`;
- dates serialize deterministically;
- packet freshness, invariant, unit, lint, and type checks pass;
- no ICE/PJM/pricing/risk/UI/agent/Nautilus runtime behavior was added.

## Disposition Table Template

| Finding ID | Source | Summary | Disposition | Canonical update | Follow-up |
|---|---|---|---|---|---|
| F-001 | review |  | accepted/rejected/deferred |  |  |

## Required Reconciliation Output

```json
{
  "closed_work_item": "W-006",
  "acceptance_status": "met | partial | not_met",
  "findings_dispositioned": [],
  "canonical_files_updated": [],
  "packets_refreshed": [],
  "workscope_status_changes": [],
  "next_active_work_item": "W-003",
  "merge_target": "main",
  "remaining_blockers": [],
  "summary": ""
}
```
