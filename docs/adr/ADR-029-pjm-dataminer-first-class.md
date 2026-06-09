# ADR-029 — PJM Data Miner Remains First-Class

Status: accepted
Date: 2026-06-09

## Decision

PJM Data Miner remains a first-class integration and should be implemented after the core event-store/instrument/pricer loop is stable enough to support deterministic replay.

## Consequences

- The Henry proving book is a first proving slice, not a scope reduction.
- PJM direct API ingestion must preserve raw calls, pagination/checkpointing, and revision/repost semantics.
- The later power vertical joins public PJM fundamentals with ICE market data through the event store.
