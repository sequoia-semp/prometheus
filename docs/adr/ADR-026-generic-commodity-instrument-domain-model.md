# ADR-026 — Generic Commodity/Instrument Domain Model

Status: accepted
Date: 2026-06-09

## Decision

The project uses a generic commodity/instrument model rather than a gas-only or power-only schema.

## Consequences

- Henry gas futures/options and power delivery-profile placeholders must use the same identity framework.
- Contract multipliers, delivery profiles, option exercise style, reference futures, and quote units are explicit model fields.
- Product-specific conventions are represented by versioned policy objects, not hard-coded branches.
