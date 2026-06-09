---
packet_type: reconciliation
packet_status: current
active_work_item: W-000B
reconciliation_target: W-000B
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
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/packets/current/REVIEW_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/reviews/REVIEW_LOG.md
  - scripts/check_plan_freshness.py
  - tests/unit/test_packet_workflow.py
---

# Reconciliation Packet — W-000B Closeout and Return to W-006

## Purpose

Use this packet after W-000B coding and review outputs are available. Its job is to close the branch-local packet workflow hardening task without losing decisions in chat transcripts.

## Required Inputs

```text
AGENTS.md
docs/packets/current/PLANNING_PACKET.md
docs/packets/current/IMPLEMENTATION_PACKET.md
Coding-agent JSON summary
Review JSON result
Human/user dispositions
```

## Reconciliation Steps

1. Identify whether W-000B met acceptance criteria.
2. Convert review findings into `accepted`, `rejected`, or `deferred` rows.
3. For accepted findings, update the relevant canonical file: ADR, contract, workscope, packet workflow, tests/checks, or README/AGENTS.
4. For rejected findings, add rationale to `docs/reviews/REJECTED_FINDINGS.md`.
5. For deferred findings, create or update a work item or `OPEN_QUESTIONS.md` row.
6. Update `docs/reviews/REVIEW_LOG.md`.
7. Update `docs/workscope/workscope.yaml` status for W-000B.
8. Refresh current packet metadata and manifest if referenced sources changed.
9. Merge into `codex/w-006-calendar-expiry`, not `main`.
10. After merge, refresh the W-006 branch packets so W-006 is active again.

## W-000B Closeout Rule

Do not mark W-000B done unless:

- branch-local packet policy is documented;
- current packets carry branch metadata;
- implementation/review/reconciliation packets are W-000B-specific on this branch;
- manifest coverage includes every current packet canonical_source;
- freshness checks and tests pass;
- stale W-001 active-task language is removed;
- no W-006 calendar domain implementation or runtime behavior was added.

## Disposition Table Template

| Finding ID | Source | Summary | Disposition | Canonical update | Follow-up |
|---|---|---|---|---|---|
| F-001 | review |  | accepted/rejected/deferred |  |  |

## Required Reconciliation Output

```json
{
  "closed_work_item": "W-000B",
  "acceptance_status": "met | partial | not_met",
  "findings_dispositioned": [],
  "canonical_files_updated": [],
  "packets_refreshed": [],
  "workscope_status_changes": [],
  "next_active_work_item": "W-006",
  "merge_target": "codex/w-006-calendar-expiry",
  "post_merge_refresh_required": true,
  "remaining_blockers": [],
  "summary": ""
}
```
