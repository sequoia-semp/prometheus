# ADR-024 — Workscope Source of Truth and Packet Workflow

Status: accepted
Date: 2026-06-09

## Decision

`docs/workscope/workscope.yaml` is the canonical implementation backlog and dependency graph. Persistent packets under `docs/packets/current/` are the handoff mechanism between planning, coding, review, and reconciliation instances.

## Consequences

- Packets must be complete enough to move between LLM instances.
- Packets must list source files and freshness metadata.
- Packet drift is a failed check for current packets.
- Archived packets may be stale but must be marked archived.
- Coding agents receive the current implementation packet, not a broad unscoped mandate.
