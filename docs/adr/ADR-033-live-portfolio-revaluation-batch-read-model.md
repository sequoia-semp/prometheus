# ADR-033 — Live Portfolio Revaluation as Batch Read-Model

Status: accepted
Date: 2026-06-09

## Decision

The live portfolio view is a batch revaluation read-model over the append-only event store and the one authoritative pricer/risk engine. It is not a second pricing path.

While live, market-data refreshes trigger periodic/coalesced revaluation runs. The target cadence is approximately one minute where the data source supports it, but the correctness requirement is replay identity, not exact tick-level streaming.

## Consequences

- Live-style and replay runs must produce identical snapshots for identical inputs.
- Corrections emit superseding snapshots; prior snapshots are never mutated.
- Transport is an implementation detail: polling, files, local HTTP, SSE, WebSocket, or Nautilus bus may be added later without changing valuation authority.
- Snapshot outputs carry full lineage.
