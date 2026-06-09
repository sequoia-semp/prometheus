---
packet_type: review
packet_status: current
review_target: W-001
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/packets/current/IMPLEMENTATION_PACKET.md
  - docs/workscope/workscope.yaml
---

# Review Packet — W-001 Repo Scaffold and Invariant Gates

## Review target

Review the W-001 scaffold and invariant-gate implementation. The review should verify that the repo can support the later event/pricing/ICE/PJM/Textual/agent/Nautilus work without prematurely implementing business logic or narrowing the architecture.

## Review questions

1. Does the scaffold preserve the full plan: ICE sidecar, Henry Hub gas proving book, PJM featured vertical, event store, instrument model, blotter, pricing/risk, revaluation, Textual-compatible views, opencode/Ollama agent loop, Nautilus spike?
2. Are package boundaries present and language-neutral enough for future Rust/Nautilus integration?
3. Does CI/local testing avoid requiring ICE Connect/Python?
4. Is `.ata_local/` and live/local data protected by `.gitignore`?
5. Does the `icepython` import ban exist and target only non-sidecar code?
6. Does `python3 scripts/check_plan_freshness.py` still pass?
7. Does `python3 scripts/check_invariants.py` still pass?
8. Are placeholder tests/lint/type commands documented and runnable?
9. Did W-001 avoid implementing W-003 ICE logic, W-014 pricing/risk, W-025 agent runtime, or other future work?
10. Are packets still persistent and current after any metadata changes?
11. Are any hidden architecture decisions embedded in code/config without ADR/workscope linkage?
12. Are Textual, opencode/Ollama, and Nautilus packages scaffolded as boundaries rather than runtime dependencies?

## Blocking findings

Flag as blocking:

- No persistent packet workflow after scaffold changes.
- Runtime implementation added outside W-001 scope.
- ICE required for CI/default tests.
- `icepython` import allowed broadly.
- Live data, credentials, or local ICE artifacts not protected by gitignore.
- Package boundaries couple canonical contracts to pandas/DataFrame/framework-specific objects.
- A second pricing path, write-capable agent tool, or order-submission path appears.
- Textual UI code imports source adapters directly or embeds business logic.
- Nautilus becomes required for default CI or replaces the project event/pricing/risk spine before W-N1.

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
