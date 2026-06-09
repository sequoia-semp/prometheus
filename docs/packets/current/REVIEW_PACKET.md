---
packet_type: review
packet_status: current
review_target: W-006
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
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/workscope/workscope.yaml
---

# Review Packet — W-006 Calendar and Expiry Service

## Review target

Review the W-006 calendar and expiry implementation. The review should verify versioned calendar inputs, Henry expiry representation, settlement anchors, delivery periods, power 5x16 profile support, and calendar version lineage.

## Review questions

1. Are calendars, expiry rules, delivery profiles, and settlement anchors versioned domain inputs?
2. Is Henry last-trading-day/expiry rule represented without hardcoding in pricing/UI code?
3. Are settlement anchors explicit and versioned?
4. Can power 5x16 delivery profiles be represented without schema fork?
5. Do relevant outputs include `calendar_version`?
6. Are dates serialized deterministically?
7. Does the implementation avoid premature holiday-source or external calendar dependencies?
8. Does the implementation avoid ICE/PJM/pricing/risk/UI/agent/Nautilus runtime behavior?
9. Do `python3 scripts/check_plan_freshness.py` and `python3 scripts/check_invariants.py` pass?
10. Are packets still persistent and current after metadata changes?

## Blocking findings

Flag as blocking:

- Calendar rules are hidden constants without version IDs.
- Henry expiry cannot be reproduced from versioned inputs.
- Power 5x16 requires a separate schema fork.
- Calendar output omits `calendar_version`.
- Runtime implementation appears outside `src/ata/calendars`.

## Output format

```json
{
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
