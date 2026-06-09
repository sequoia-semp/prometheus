# Source of Truth

Status: canonical
Last updated: 2026-06-09

## Authority order

1. **ADRs** — durable architecture decisions.
2. **Contracts** — typed system boundaries and schema expectations.
3. **workscope.yaml** — canonical backlog, dependencies, and implementation order.
4. **Planning docs** — human-readable synthesis and unresolved questions.
5. **Packets** — persistent handoff bundles for planning, coding, review, and reconciliation.
6. **Review logs/findings** — not binding until dispositioned.

## Packet rule

Packets are repo-persistent and intentionally stand-alone enough to move between LLM instances. They package canonical source material for a specific phase:

```text
PLANNING_PACKET.md        project state and roadmap
IMPLEMENTATION_PACKET.md  current coding-agent handoff
REVIEW_PACKET.md          current review/adversarial handoff
RECONCILIATION_PACKET.md  post-review closeout and status update
LOCAL_ICE_PACKET.md       local ICE Connect/Python workflow and hygiene
```

Packets are not a second source of truth. If a packet contradicts an ADR, contract, or workscope row, the packet is stale and must be regenerated or corrected.

## Branch-local authority

Canonical docs are canonical within the branch being inspected. On `codex` or `codex/<work-item>-<slug>` branches, ADRs, contracts, workscope rows, and current packets may describe work that has not yet been merged to `main`.

`main` is stable only after user-approved reconciliation and merge. External review should inspect the coding branch or PR head and its branch-local packets unless the user explicitly asks to inspect `main`.

Packet frontmatter and `PACKET_MANIFEST.yaml` must identify `stable_branch`, `working_branch`, `packet_scope`, `base_ref`, and `head_ref` so planning and review infrastructure can distinguish stable project state from branch-local coding context.

## User gate

Architecture, scope, autonomy-level, and trading-execution changes require explicit user approval. LLMs, coding agents, and reviewers may propose changes, but they do not make them binding.

## Status vocabulary

Use the smallest practical status set:

```text
ADR: proposed | accepted | superseded | rejected
Work item: planned | ready | active | review | done | blocked
Review finding: open | accepted | rejected | deferred
Packet: current | stale | archived
```

## Git hygiene

- Do not commit credentials, tokens, or raw accidental live data dumps.
- Checked-in fixtures should be synthetic, public, or deliberately minimized examples.
- Local data and local ICE probe outputs live under `.ata_local/` or another gitignored path.
- Sanitized local summaries may be copied into packets only when explicitly useful for implementation or review.
