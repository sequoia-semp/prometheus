---
packet_type: review
packet_status: current
review_target: W-007
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/workscope/workscope.yaml
---

# Review Packet — W-007 Event Envelope and Bitemporal Store

## Review target

Review the W-007 event envelope and bitemporal store implementation. The review should verify append-only behavior, deterministic ordering, bitemporal query semantics, JSONL compatibility, snapshot ID determinism, and contract-compatible serialization.

## Review questions

1. Does the event envelope match `docs/contracts/EVENT_ENVELOPE.md`?
2. Are updates/deletes impossible through the public event-store API?
3. Is `stream_sequence` monotonic per `stream_id` without assuming a global sequence?
4. Do `as_of` and `known_at` queries return deterministic bitemporal results?
5. Are snapshot IDs deterministic and based on event hashes plus version lineage?
6. Do JSONL import/export round-trip without losing Decimal string values or UTC timestamp semantics?
7. Do events carry `source_system` and `data_scope`?
8. Does the implementation avoid ICE/PJM/pricing/risk/UI/agent/Nautilus runtime behavior?
9. Do `python3 scripts/check_plan_freshness.py` and `python3 scripts/check_invariants.py` pass?
10. Are packets still persistent and current after metadata changes?

## Blocking findings

Flag as blocking:

- Event-store API can mutate or delete accepted events.
- Bitemporal query ignores either `as_of` or `known_at`.
- Per-stream ordering is not enforced.
- Snapshot IDs depend on insertion order, process randomness, or wall-clock time.
- JSONL output cannot be reimported deterministically.
- Runtime implementation appears outside `src/ata/events`.

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
