# Packet Workflow

Status: canonical
Last updated: 2026-06-09

## Purpose

The project uses persistent, portable packets so planning, coding, review, and reconciliation can move between local LLM instances. Packets are repo files, not transient chat prompts.

## Current packet set

```text
docs/packets/current/PLANNING_PACKET.md        current project map and roadmap
docs/packets/current/IMPLEMENTATION_PACKET.md  current coding-agent task
docs/packets/current/REVIEW_PACKET.md          current review/adversarial packet
docs/packets/current/RECONCILIATION_PACKET.md  closeout and next-loop packet
docs/packets/current/LOCAL_ICE_PACKET.md       local ICE Connect/Python handoff packet
docs/packets/current/PACKET_MANIFEST.yaml      packet sources and hashes
```

## Authority

Packets are stand-alone handoff artifacts, but not a second source of truth. ADRs, contracts, and `docs/workscope/workscope.yaml` remain canonical.

## Branch Policy

```text
main
  Stable, user-approved project state. Only merge implemented/reviewed/reconciled work here.

codex or codex/<work-item>-<slug>
  Active coding-agent work branch. Branch-local docs/packets/current/* describe this branch's active state and may be ahead of main.

codex/<process-or-subtask-slug>
  Temporary process or subtask branch based on an active codex work branch. Example: codex/workflow-branch-packets based on codex/w-006-calendar-expiry. Merge back into the active codex work branch, not directly to main.

CODEX
  Legacy/local equivalent of codex until renamed. Prefer lowercase codex names in new docs and branches.

review/<work-item>-<slug> or reconcile/<work-item>-<slug>
  Optional review/reconciliation branches. Review should inspect the coding branch or PR head, not main, unless explicitly asked to inspect main.

local working tree
  May contain .ata_local/, local ICE probe outputs, and temporary packet transfers. These remain uncommitted unless intentionally sanitized and added.
```

Current packets must declare branch metadata in frontmatter:

```yaml
repository: sequoia-semp/prometheus
stable_branch: main
working_branch: codex/<work-item>-<slug>
preferred_branch_convention: codex/<work-item>-<slug>
packet_scope: branch-local-current
base_ref: <review-base-ref>
head_ref: <branch-or-pr-head-ref>
```

Planning, coding, review, and reconciliation agents must treat `docs/packets/current/*` as branch-local. If a packet's `head_ref`, `base_ref`, or active work item does not match the branch or PR being reviewed, report packet drift before assessing implementation quality.

## Refresh triggers

Refresh current packets when:

1. the active work item changes;
2. implementation handoff begins;
3. review handoff begins;
4. review findings are reconciled;
5. referenced canonical docs change;
6. a milestone closes;
7. the user asks for a fresh portable snapshot.

Do not regenerate archived packets for minor edits. Current packet mismatch fails; archived packet mismatch warns.

## Loop

```text
Goal/change request
  -> planning packet + ADR/contract/workscope proposal
  -> explicit user approval for architecture/scope/autonomy/trading-control changes
  -> active implementation packet
  -> coding agent implements one work item
  -> coding agent returns JSON + paste-ready review/reconciliation handoff
  -> tests and freshness checks
  -> active review packet plus diff/summary
  -> findings accepted/rejected/deferred
  -> canonical docs updated
  -> packets refreshed or archived
  -> next active work item selected
```

## Moving packets between instances

For a planning instance, pass:

```text
AGENTS.md
docs/packets/current/PLANNING_PACKET.md
docs/packets/current/RECONCILIATION_PACKET.md when closing findings
```

For a coding instance, pass:

```text
AGENTS.md
docs/packets/current/PLANNING_PACKET.md
docs/packets/current/IMPLEMENTATION_PACKET.md
```

For a review instance, pass:

```text
AGENTS.md
docs/packets/current/PLANNING_PACKET.md
docs/packets/current/REVIEW_PACKET.md
coding-agent final JSON/handoff
declared implementation diff or commit range
```

The coding-agent handoff travels with the review packet. The diff should come from the coding branch or PR head named in packet metadata. Do not compare against `main` merely because `main` is the stable branch; use the declared `base_ref`/`head_ref` unless the user asks for a different comparison.

For local ICE work, additionally pass:

```text
docs/packets/current/LOCAL_ICE_PACKET.md
sanitized .ata_local/packets/LOCAL_ICE_OBSERVED_SURFACE.md if available
```
