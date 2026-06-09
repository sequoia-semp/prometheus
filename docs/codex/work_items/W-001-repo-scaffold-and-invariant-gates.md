# W-001 — Repo Scaffold and Invariant Gates

Status: ready
Depends on: W-000

## Objective

Create the local-first runtime repository scaffold and invariant checks without implementing business logic for ICE, PJM, pricing, event storage, UI screens, Nautilus runtime behavior, or agents.

## Files in scope

```text
pyproject.toml
uv.lock if generated
src/ata/**
apps/**
tests/**
data/fixtures/synthetic/.gitkeep
scripts/check_*.py
scripts/build_packet_bundle.py
.gitignore
README.md
AGENTS.md
docs/packets/current/** only if active packet metadata needs refreshing
```

## Files out of scope

```text
.ata_local/**
data/live/**
credentials/**
real ICE/PJM data dumps
runtime ICE Python adapter business logic
pricing/risk implementation beyond stubs/contracts
agent runtime implementation beyond package placeholders
```

## Required scaffold

Suggested layout:

```text
src/ata/
  __init__.py
  events/
  instruments/
  calendars/
  blotter/
  pricing/
  risk/
  ice_sidecar/
  pjm/
  agent/
  ui_textual/
  nautilus/
apps/ata_cli/
apps/ata_tui/
tests/
  unit/
  integration/
  local_live/
data/fixtures/synthetic/
```

The package boundaries should remain compatible with future Rust/Nautilus integration:

- DTO boundaries are JSON/Serde-friendly.
- Decimal values should be serializable as strings.
- Datetimes should be timezone-aware RFC3339 UTC at boundaries.
- No pandas DataFrame, Python object graph, or framework object should become a canonical boundary.
- Textual-compatible UI packages are presentation/read-model consumers only.
- Local opencode/Ollama agent adapters are read-only and evidence-bound.
- Nautilus packages are placeholders until W-N1; Nautilus must not be required for default local checks.

## Invariant gates

Add checks or tests for:

1. no `icepython` import outside the sidecar package;
2. `.ata_local/`, credentials, tokens, and live data paths are gitignored;
3. packet freshness check runs;
4. no agent write/order/SQL/credential tools in contract files;
5. ADR index has no dead file references;
6. workscope includes the full expected sequence;
7. no release-style planning version tags in active filenames.
8. Textual UI, agent, and Nautilus scaffold packages do not import source adapters or add runtime behavior.

## Acceptance criteria

- Python project scaffold exists and basic commands run.
- `python3 scripts/check_plan_freshness.py` passes.
- `python3 scripts/check_invariants.py` passes.
- Lint/type/test commands exist, even if only placeholder tests run initially.
- Package boundaries are created for events, instruments, calendars, blotter, pricing, risk, ICE sidecar, PJM, and agent harness.
- Package boundaries are created for Textual-compatible UI and Nautilus replay/integration placeholders.
- `.gitignore` protects `.ata_local/`, credentials, tokens, and local live data artifacts.
- Local check path does not require ICE Connect/Python, GitHub Actions, or release automation.
- No runtime implementation for W-003/W-014/W-025 is added.

## Required final response

```json
{
  "work_item": "W-001",
  "summary": "",
  "files_changed": [],
  "tests_added": [],
  "tests_run": [],
  "acceptance_status": "met | partial | not_met",
  "out_of_scope_changes": [],
  "open_questions": [],
  "risks": []
}
```
