# ADR-027 — Event Store and Data Plane

Status: accepted
Date: 2026-06-09

## Decision

The event store is append-only, bitemporal, and the project source of truth for raw and normalized observations.

## Consequences

- Corrections, amendments, busts, and reposts are new events.
- Per-stream ordering is required; no global sequence invariant is assumed.
- Replay must support `as_of` and `known_at` queries without look-ahead.
- Snapshot IDs are deterministic over source events, normalization version, calendar version, and calculation version.
