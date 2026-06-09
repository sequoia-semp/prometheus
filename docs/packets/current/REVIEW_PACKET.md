---
packet_type: review
packet_status: current
review_target: W-000B
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
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - scripts/check_plan_freshness.py
  - tests/unit/test_packet_workflow.py
---

# Review Packet — W-000B Branch-local Packet Workflow Hardening

## Review Target

Review the W-000B branch-local packet workflow hardening implementation.

Review diff:

Base: `codex/w-006-calendar-expiry`
Head: `codex/workflow-branch-packets`

Do not compare this branch to `main` unless explicitly instructed.

## Review Questions

1. Does the branch policy clearly distinguish main, codex, codex/<work-item>, review, reconcile, and local working tree states?
2. Do all current packets include branch metadata?
3. Do current packets describe W-000B rather than W-006 implementation on this branch?
4. Is W-006 clearly preserved as the next/returned active domain item after W-000B merges?
5. Does PACKET_MANIFEST.yaml cover every canonical_source referenced by every current packet?
6. Does check_plan_freshness.py fail on active-work-item mismatch?
7. Does check_plan_freshness.py fail on missing branch metadata?
8. Does check_plan_freshness.py fail on missing canonical source files?
9. Does check_plan_freshness.py fail when a canonical source is absent from PACKET_MANIFEST.yaml?
10. Does check_plan_freshness.py fail on manifest hash mismatch?
11. Do tests cover branch-name mismatch and detached/override branch-check behavior?
12. Is stale W-001 active-task language removed?
13. Does this branch avoid W-006 calendar domain implementation and all runtime ICE/PJM/pricing/risk/UI/agent/Nautilus behavior?

## Blocking Findings

Flag as blocking:

- Current packets describe W-006 as active on this branch.
- Branch metadata is missing or mismatched.
- Review packet points reviewers at `main` instead of the declared base/head diff.
- Manifest does not cover every canonical_source referenced by current packets.
- Freshness checks pass despite active-work-item, branch metadata, canonical_source, or hash drift.
- Branch-name mismatch is not detected, except when intentionally skipped for detached-head or override contexts.
- Runtime/domain implementation appears in this process branch.

## Output Format

```json
{
  "review_target": "W-000B",
  "base_ref": "codex/w-006-calendar-expiry",
  "head_ref": "codex/workflow-branch-packets",
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
