# Local Trading and Portfolio Analytics Platform — Project Start Pack

Date: 2026-06-09

This repository starts from a planning-first, packetized workflow. The project goal is to build a deterministic, auditable local trading and portfolio analytics platform that can ingest ICE desktop data through ICE Python, ingest PJM public/fundamental data through PJM Data Miner, value futures/options/positions, compute portfolio risk, support Textual-compatible operator views, and expose read-only agent tools with evidence-bound answers for a local opencode/Ollama harness.

The first proving product is ICE Henry Hub gas futures and options. PJM remains a featured product vertical and use case, not a dropped scope item.

The current active implementation task is defined by:

- `docs/workscope/workscope.yaml`
- `docs/packets/current/PLANNING_PACKET.md`
- `docs/packets/current/IMPLEMENTATION_PACKET.md`

On coding branches, these files may be ahead of `main`. Inspect the branch or PR head named in packet metadata.

## Start here

Coding agents and review instances should read in this order:

1. `AGENTS.md`
2. `docs/packets/current/PLANNING_PACKET.md`
3. Current task packet:
   - coding: `docs/packets/current/IMPLEMENTATION_PACKET.md`
   - review: `docs/packets/current/REVIEW_PACKET.md`
   - closeout: `docs/packets/current/RECONCILIATION_PACKET.md`
4. Canonical ADRs/contracts referenced by the active packet when editing them.

## Canonical repo design

```text
AGENTS.md                         agent/coding/review rules
README.md                         project entry point
docs/planning/                    durable planning files and source-of-truth rules
docs/adr/                         architecture decisions
docs/contracts/                   typed boundaries and schemas
docs/workscope/workscope.yaml     canonical backlog and dependency graph
docs/packets/current/             portable planning/implementation/review/reconciliation packets
docs/packets/archive/             historical packet snapshots
docs/codex/                       coding-agent operating rules and work-item templates
docs/reviews/                     review process, log, rejected findings
docs/local/                       local integration notes, especially ICE Connect/Python
scripts/check_plan_freshness.py   structural drift check
scripts/build_packet_bundle.py    current packet bundle builder
.ata_local/                       local-only ICE/PJM/live scratch area; gitignored
```

The runtime scaffold lives under `pyproject.toml`, `src/ata/**`, `apps/**`, `tests/**`, CLI/Textual-compatible entrypoints, Nautilus placeholder boundary, and local invariant gates. Current packets identify the active task for the branch being inspected.

## Packet rule

Packets are persistent and portable. They exist so planning, coding, review, and reconciliation can move between local LLM instances without requiring each instance to rediscover the repo. Packets are not a second source of truth: they package current working context from canonical repo docs.

Packets are branch-local working context. `main` is stable, user-approved state; `codex` or `codex/<work-item>-<slug>` branches may carry current packets that are ahead of `main`. Temporary `codex/<process-or-subtask-slug>` branches may be based on an active coding branch and should merge back to that branch, not directly to `main`. External review should inspect the coding branch or PR head together with that branch's packets, not `main` packets, unless the review is explicitly about `main`. `review/<work-item>-<slug>` and `reconcile/<work-item>-<slug>` branches may be used for review and closeout handoffs.

## Local ICE rule

If the user provides a running local ICE Connect/Python instance, W-003 should be able to probe it, build a local field map, sample configured symbols, normalize into event envelopes, and quarantine unmapped fields. Normal CI remains fixture-only and must not require ICE.

## Local checks

Before the runtime packages contain business logic, the fast structural check path is:

```bash
python3 scripts/check_plan_freshness.py
python3 scripts/check_invariants.py
uv run pytest
uv run ruff check .
uv run pyright
```

Default local checks must not require ICE Connect/Python, live PJM data, NautilusTrader, Textual, GitHub Actions, release automation, or a local LLM process.
