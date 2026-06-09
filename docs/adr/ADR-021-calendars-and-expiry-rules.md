# ADR-021 — Calendars and Expiry Rules

Status: accepted
Date: 2026-06-09

## Decision

Calendars, expiry rules, delivery-period rules, and settlement anchors are versioned domain inputs.

## Consequences

- Pricing, risk, and snapshot IDs include `calendar_version` where calendar rules affect outputs.
- Henry expiry/settlement rules are implemented before the Henry golden book is trusted.
- Power calendars must support versioned delivery profiles such as 5x16 without schema forks.
