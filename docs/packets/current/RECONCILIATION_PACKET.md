---
packet_type: reconciliation
packet_status: current
active_work_item: W-008
last_updated: 2026-06-09
canonical_sources:
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/packets/current/REVIEW_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/reviews/REVIEW_LOG.md
---

# Reconciliation Packet — W-008 Closeout and Next Loop

## Purpose

Use this packet after the coding agent and reviewer have produced outputs. Its job is to close the loop without losing decisions in chat transcripts.

## Required inputs

```text
AGENTS.md
docs/packets/current/PLANNING_PACKET.md
docs/packets/current/IMPLEMENTATION_PACKET.md
Coding-agent JSON summary
Review JSON result
Human/user dispositions
```

## Reconciliation steps

1. Identify whether W-001 met acceptance criteria.
2. Convert review findings into `accepted`, `rejected`, or `deferred` rows.
3. For accepted findings, update the relevant canonical file: ADR, contract, workscope, packet workflow, tests/checks, or README/AGENTS.
4. For rejected findings, add rationale to `docs/reviews/REJECTED_FINDINGS.md`.
5. For deferred findings, create or update a work item or `OPEN_QUESTIONS.md` row.
6. Update `docs/reviews/REVIEW_LOG.md`.
7. Update `docs/workscope/workscope.yaml` status for W-001.
8. Refresh current packet metadata and manifest if referenced sources changed.
9. Select the next active implementation packet, normally W-009 after W-008 closes.

## W-008 closeout rule

Do not mark W-008 done unless:

- Henry LD1 future is modeled and tested;
- European Henry option-on-future is modeled and tested;
- American option is representable but marked unsupported for v0 pricing;
- power 5x16 placeholder uses the same identity schema;
- multiplier policy lineage is explicit and tested;
- instrument identity JSON and canonical IDs round-trip deterministically;
- no source-adapter, pricing, risk, UI, Nautilus, or agent runtime behavior was added.

## Disposition table template

| Finding ID | Source | Summary | Disposition | Canonical update | Follow-up |
|---|---|---|---|---|---|
| F-001 | review |  | accepted/rejected/deferred |  |  |

## Required reconciliation output

```json
{
  "closed_work_item": "W-008",
  "acceptance_status": "met | partial | not_met",
  "findings_dispositioned": [],
  "canonical_files_updated": [],
  "packets_refreshed": [],
  "workscope_status_changes": [],
  "next_active_work_item": "W-009 | W-006 | other",
  "remaining_blockers": [],
  "summary": ""
}
```
