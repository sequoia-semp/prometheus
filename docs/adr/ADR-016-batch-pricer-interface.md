# ADR-016 — Batch Pricer Interface

Status: accepted
Date: 2026-06-09

## Decision

The authoritative valuation interface is a batch pricer/risk call over explicit inputs: `as_of`, `known_at`, market snapshot, book version, positions, model configuration, and scenarios.

## Consequences

- No calculation may use unconstrained “latest.”
- Every output carries lineage IDs.
- Greeks are bump-and-revalue in v0 unless a later ADR approves an analytic path.
- Option pricing v0 uses Black-76 for European options-on-futures.
