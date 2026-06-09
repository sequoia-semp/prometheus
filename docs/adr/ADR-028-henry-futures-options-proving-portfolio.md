# ADR-028 — Henry Futures/Options Proving Portfolio

Status: accepted
Date: 2026-06-09

## Decision

Use a Henry futures/options proving book as the first deterministic live/replay analytics slice.

## Purpose

The proving book validates:

- position aggregation;
- futures and European option-on-futures valuation;
- Black-76 option pricing;
- bump-and-revalue Greeks;
- PnL explain;
- p95/p99 VaR;
- market snapshot IDs and version propagation;
- replay equivalence between event-store runs and local-live style runs.

## Scope

The Henry proving book does not remove PJM or power from the project. It creates a simpler ICE/pricer/event-store loop before the PJM/ICE power vertical.
