# ADR-014 — Nautilus Runtime Spine

Status: proposed
Date: 2026-06-09

## Decision

NautilusTrader is a candidate runtime/replay spine, not the v0 source of truth. W-001 may create a placeholder package boundary for future Nautilus replay/integration code, but Nautilus is not a required dependency or runtime path before W-N1.

## Requirement before adoption

W-N1 must demonstrate that normalized project events replay into a Nautilus-compatible adapter without making strategy code call ICE or PJM directly, and without replacing the project event store, instrument model, pricer, or risk engine as authoritative.

## Consequences

- Core contracts must remain language-neutral and event-driven.
- The event store and pricing/risk engine remain project-owned.
- Nautilus adapters may be added after the spike passes.
