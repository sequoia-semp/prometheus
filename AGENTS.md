# AGENTS.md

## Required read order

Before editing, a coding or review agent must read:

1. `AGENTS.md`
2. `docs/packets/current/PLANNING_PACKET.md`
3. The active phase packet:
   - `docs/packets/current/IMPLEMENTATION_PACKET.md` for coding;
   - `docs/packets/current/REVIEW_PACKET.md` for review;
   - `docs/packets/current/RECONCILIATION_PACKET.md` for closeout;
   - `docs/packets/current/LOCAL_ICE_PACKET.md` for local ICE work.
4. Canonical ADRs/contracts/workscope rows referenced by the active packet.

## Scope discipline

- Implement exactly one active work item unless the user explicitly changes scope.
- Do not make architecture, scope, autonomy, or trading-control changes without explicit user approval.
- Do not treat packet text as overriding ADRs, contracts, or `docs/workscope/workscope.yaml`.
- When a packet and canonical file disagree, report the drift and update or regenerate the packet.

## Branch and packet policy

- `main` is stable, user-approved project state. Only merge implemented, reviewed, and reconciled work there.
- `codex` or `codex/<work-item>-<slug>` is the preferred coding-agent branch convention. Branch-local `docs/packets/current/*` files describe that branch's active state and may be ahead of `main`.
- An existing local branch named `CODEX` should be treated as equivalent to `codex` until it can be renamed.
- `review/<work-item>-<slug>` and `reconcile/<work-item>-<slug>` may be used for external review or closeout. Review agents should inspect the coding branch or PR head, not `main`, unless explicitly asked to inspect `main`.
- Local working trees may contain `.ata_local/`, local ICE probe outputs, and temporary packet transfers. These remain uncommitted unless intentionally sanitized and added.
- Before reviewing or coding, verify the packet frontmatter `working_branch`, `base_ref`, `head_ref`, and `packet_scope`. If these disagree with the branch or PR under review, stop and report packet drift.

## Project invariants

- The project is a broad local trading and portfolio analytics platform. Henry Hub ICE gas futures/options are the first proving product; PJM remains a featured first-class vertical.
- ICE integration is through the ICE Python sidecar only in v0.
- Do not implement Excel RTD workbook polling, RTD formula parsing, screen scraping, or UI automation.
- The event store is append-only and bitemporal.
- Analytics must carry `as_of`, `known_at`, and snapshot/version lineage.
- Use one authoritative pricing/risk engine. Do not create a second pricing path in live/read-model code.
- Textual UI code must be presentation-only and read derived views/read models, not source adapters directly.
- Agent v0 is read-only. Do not add order-submission, write, credential, arbitrary SQL, or shell-execution tools to the agent.
- No numerical agent output without evidence binding and lineage.
- The local LLM target is opencode/Ollama, reached through read-only evidence-bound tools.
- NautilusTrader may have scaffold placeholders, but remains spike-gated by W-N1 before runtime adoption.

## Local data and ICE hygiene

- `.ata_local/`, credentials, tokens, raw local data dumps, and live spool artifacts are not committed.
- Synthetic or minimized fixtures may be committed under `data/fixtures/synthetic/` once W-001 creates the runtime scaffold.
- ICE Python imports are allowed only inside the sidecar package once it exists.
- Default local checks must pass without ICE Connect/Python, GitHub Actions, or release automation.

## Local checks

Run the targeted checks for W-001-style scaffold changes:

```bash
python3 scripts/check_plan_freshness.py
python3 scripts/check_invariants.py
uv run pytest
uv run ruff check .
uv run pyright
```

## Expected coding-agent response

Use structured JSON in final responses for implementation tasks:

```json
{
  "work_item": "",
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
