---
packet_type: review
packet_status: current
review_target: W-006
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
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - scripts/check_plan_freshness.py
  - tests/unit/test_packet_workflow.py
---

# Review Packet — W-006 Calendar and Expiry Service

## Review Target

Review the W-006 implementation on the declared branch or PR head.

Review diff:

Base: `main`
Head: `codex/w-006-calendar-expiry`

Do not compare against unrelated `main` state or stale packet metadata. First verify packet `working_branch`, `base_ref`, `head_ref`, and `packet_scope`.

## Review Questions

1. Are calendars, expiry rules, delivery profiles, and settlement anchors represented as versioned domain inputs?
2. Is Henry last-trading-day/expiry represented reproducibly?
3. Are settlement anchors explicit and versioned?
4. Can power 5x16 delivery profiles be represented without a schema fork?
5. Do relevant outputs carry `calendar_version`?
6. Do dates serialize deterministically?
7. Does the implementation avoid premature holiday-source or external calendar dependencies unless explicitly approved?
8. Does the implementation avoid ICE/PJM/pricing/risk/UI/agent/Nautilus runtime behavior?
9. Do packet freshness and invariant checks pass?

## Blocking Findings

Flag as blocking:

- Packet branch metadata points anywhere other than `codex/w-006-calendar-expiry` for this W-006 review.
- Calendar/expiry behavior is not versioned.
- Henry expiry cannot be reproduced deterministically.
- Settlement anchors are implicit, unversioned, or hardcoded into screens.
- Power delivery profiles require a schema fork.
- Outputs that depend on calendars omit `calendar_version`.
- Runtime ICE/PJM/pricing/risk/UI/agent/Nautilus behavior appears in this work item.
- Packet freshness, invariant, unit, lint, or type checks fail due to implementation issues.

## Output Format

```json
{
  "review_target": "W-006",
  "base_ref": "main",
  "head_ref": "codex/w-006-calendar-expiry",
  "branch_metadata_checked": true,
  "verdict": "approve | request_changes | block",
  "blockers": [],
  "major_findings": [],
  "minor_findings": [],
  "missing_decisions": [],
  "missing_tests": [],
  "scope_drift_warnings": [],
  "suggested_adr_changes": [],
  "suggested_workscope_changes": [],
  "findings_to_reject_or_defer": [],
  "summary": ""
}
```
