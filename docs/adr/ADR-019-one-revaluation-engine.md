# ADR-019 — One Revaluation Engine

Status: accepted
Date: 2026-06-09

## Decision

The domain pricing/risk engine is the single authoritative path for PV, Greeks, PnL, VaR, and derived portfolio revaluation snapshots.

## Consequences

- Live portfolio views call the same engine as replay/batch runs.
- Nautilus, UI layers, and agent tools may display or route results, but they do not independently compute authoritative valuation numbers.
- A second valuation path is a blocking review finding.
