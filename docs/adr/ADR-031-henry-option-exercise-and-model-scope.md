# ADR-031 — Henry Option Exercise Style and Pricing-Model Scope

Status: accepted
Date: 2026-06-09

## Decision

v0 binds to European-style Henry option-on-future analytics and prices those options with Black-76. American-style options are explicitly out of scope for v0 and must be rejected by the pricer with a typed unsupported-instrument/model error.

The option's `reference_future_id` must be explicit. The project must not conflate the ICE LD1 financial future, the NYMEX Henry Hub future, and listed option reference contracts.

## Consequences

- `exercise_style` is a required field for options.
- `reference_future_id` is required for options-on-futures.
- American exercise requires a later ADR and a different model family.
- W-003 verifies local ICE fields/symbology; W-014 can proceed with synthetic fixtures.
