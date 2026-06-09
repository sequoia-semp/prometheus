---
packet_type: review
packet_status: current
review_target: W-008
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/workscope/workscope.yaml
---

# Review Packet — W-008 Generic Instrument Model

## Review target

Review the W-008 generic instrument model implementation. The review should verify deterministic identity derivation, contract-compatible serialization, required option fields, multiplier policy lineage, Henry gas support, and power placeholder support without product-specific schema forks.

## Review questions

1. Does `InstrumentIdentity` match `docs/contracts/INSTRUMENT.md`?
2. Is the canonical string ID derived from typed fields rather than treated as source truth?
3. Do Henry LD1 future and European option-on-future examples round-trip deterministically?
4. Are option required fields enforced?
5. Is American-style option representable while clearly unsupported for v0 pricing?
6. Does `MultiplierPolicy` include policy ID, source, and version?
7. Can a power 5x16 placeholder be represented without schema fork?
8. Does the implementation avoid ICE/PJM/pricing/risk/UI/agent/Nautilus runtime behavior?
9. Do `python3 scripts/check_plan_freshness.py` and `python3 scripts/check_invariants.py` pass?
10. Are packets still persistent and current after metadata changes?

## Blocking findings

Flag as blocking:

- Canonical instrument ID depends on process randomness, object identity, or field ordering.
- Option identities can be created without strike/right/expiry/reference future.
- American options are silently treated as supported by v0 pricing.
- Power placeholder requires a separate schema fork.
- Runtime implementation appears outside `src/ata/instruments`.

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
