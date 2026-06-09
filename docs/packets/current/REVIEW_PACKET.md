---
packet_type: review
packet_status: current
review_target: W-009
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/workscope/workscope.yaml
---

# Review Packet — W-009 Trade Blotter and Position Projection

## Review target

Review the W-009 trade blotter implementation. The review should verify append-only event behavior, amendment/bust semantics, deterministic bitemporal position folds, deterministic book versions, and replay equivalence.

## Review questions

1. Does `TradeEvent`/`Position` match `docs/contracts/BLOTTER.md`?
2. Are trade events append-only with no mutation/delete path?
3. Are amendments and busts represented as new events referencing prior IDs?
4. Does `position_as_of(as_of, known_at)` filter both trade time and known time?
5. Is `book_version` deterministic and based on applied trade-event IDs?
6. Do positions reproduce from replaying events into a fresh blotter?
7. Are Decimal and datetime values serialized deterministically?
8. Does the implementation avoid ICE/PJM/pricing/risk/UI/agent/Nautilus runtime behavior?
9. Do `python3 scripts/check_plan_freshness.py` and `python3 scripts/check_invariants.py` pass?
10. Are packets still persistent and current after metadata changes?

## Blocking findings

Flag as blocking:

- Trade amendments/busts mutate or delete existing events.
- `position_as_of` ignores either `as_of` or `known_at`.
- `book_version` depends on insertion order, object identity, or wall-clock time.
- Replay into a fresh blotter cannot reproduce positions.
- Runtime implementation appears outside `src/ata/blotter`.

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
