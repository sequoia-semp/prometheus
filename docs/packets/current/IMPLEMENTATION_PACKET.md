---
packet_type: implementation
packet_status: current
active_work_item: W-001
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - docs/packets/current/PLANNING_PACKET.md
  - docs/workscope/workscope.yaml
  - docs/codex/work_items/W-001-repo-scaffold-and-invariant-gates.md
---

# Implementation Packet — W-001 Repo Scaffold and Invariant Gates

## Task

Create the local-first runtime repository scaffold and invariant checks. Do not implement ICE, PJM, pricing, event storage, risk, Textual screens, Nautilus runtime behavior, or agent business logic yet.

## Files in scope

```text
pyproject.toml
uv.lock if generated
src/ata/**
apps/ata_cli/**
apps/ata_tui/**
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

Package boundaries must remain Rust/Nautilus-compatible:

- DTO boundaries are JSON/Serde-friendly.
- Decimal values serialize as strings once DTOs are implemented.
- Datetimes serialize as timezone-aware RFC3339 UTC once DTOs are implemented.
- No pandas DataFrame, Python object graph, or framework object becomes a canonical boundary.
- Textual-compatible UI packages are read-model/presentation consumers only.
- Local opencode/Ollama agent adapters are read-only and evidence-bound.
- Nautilus packages are placeholders until W-N1; Nautilus must not be required for default local checks.

## Required invariant gates

Add checks or tests for:

1. no `icepython` import outside the sidecar package;
2. `.ata_local/`, credentials, tokens, and live data paths are gitignored;
3. packet freshness check runs;
4. no agent write/order/SQL/credential tools in contract files;
5. ADR index has no dead file references;
6. workscope includes the expected sequence;
7. no release-style planning version tags in active filenames.
8. no Textual, agent, or Nautilus scaffold package imports source adapters or implements runtime behavior.

## Acceptance criteria

- Python project scaffold exists and basic commands run.
- `python3 scripts/check_plan_freshness.py` passes.
- `python3 scripts/check_invariants.py` passes.
- Lint/type/test commands exist, even if only placeholder tests run initially.
- Package boundaries exist for events, instruments, calendars, blotter, pricing, risk, ICE sidecar, PJM, and agent harness.
- Package boundaries exist for Textual-compatible UI and Nautilus replay/integration placeholders.
- `.gitignore` protects `.ata_local/`, credentials, tokens, and local live data artifacts.
- Local checks do not require ICE Connect/Python, GitHub Actions, or release automation.
- No runtime implementation for W-003/W-014/W-025 is added.

## Suggested commands

The exact command set may be chosen during W-001, but it should be local-first and fast. Expected shape:

```bash
python3 scripts/check_plan_freshness.py
python3 scripts/check_invariants.py
uv run pytest
uv run ruff check .
uv run pyright
```

If the project chooses a different equivalent command, document it in README and AGENTS.

## Coding-agent final response

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
