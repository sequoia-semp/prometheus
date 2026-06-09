# W-000B — Branch-local packet workflow hardening

## Objective

Clarify and enforce branch-local packet semantics so planning, coding, review, and reconciliation instances inspect the correct branch state and do not compare active `codex/*` packets against stale `main` state.

## Branch orientation

Base: `codex/w-006-calendar-expiry`
Head: `codex/workflow-branch-packets`
Merge target: `codex/w-006-calendar-expiry`
Stable branch: `main`

Do not merge directly to `main`.

## Files in scope

- AGENTS.md
- README.md
- docs/planning/SOURCE_OF_TRUTH.md
- docs/planning/PACKET_WORKFLOW.md
- docs/workscope/workscope.yaml
- docs/packets/current/**
- docs/codex/work_items/W-000B-branch-local-packet-workflow-hardening.md
- scripts/check_plan_freshness.py
- tests/unit/test_packet_workflow.py

## Files out of scope

- src/ata/calendars/** domain implementation
- runtime ICE/PJM/pricing/risk/UI/agent/Nautilus implementation
- .ata_local/**
- live data, credentials, tokens, secrets

## Acceptance

- Branch policy is documented in AGENTS, README, SOURCE_OF_TRUTH, and PACKET_WORKFLOW.
- Current packets include branch metadata.
- Current packets describe W-000B, not W-006 calendar implementation, on this branch.
- Packet manifest covers all canonical_sources referenced by current packets.
- Freshness checks detect active-work-item mismatch, missing branch metadata, missing canonical source files, missing manifest coverage, and hash mismatches.
- Stale W-001 active-task language is removed.
- No W-006 calendar domain implementation is added.
