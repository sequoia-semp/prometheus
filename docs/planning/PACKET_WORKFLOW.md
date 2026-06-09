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
coding-agent JSON summary or diff
```

For local ICE work, additionally pass:

```text
docs/packets/current/LOCAL_ICE_PACKET.md
sanitized .ata_local/packets/LOCAL_ICE_OBSERVED_SURFACE.md if available
```
