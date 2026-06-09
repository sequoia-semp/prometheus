# ADR-030 — Henry MultiplierPolicy and Contract-Unit Reconciliation

Status: accepted
Date: 2026-06-09

## Decision

Henry product exposure must be represented by explicit named multiplier policies. No pricer, blotter, or agent output may infer a multiplier from symbol text alone.

v0 policies:

```text
ICE_HH_LD1_LOT
  unit: MMBtu
  contract_size: 2500
  applies_flow_day_multiplier: false

ICE_HH_LD1_FLOW
  unit: MMBtu
  contract_size: 2500
  applies_flow_day_multiplier: true
  flow_days_in_period: calendar days in contract month

NYMEX_HH_NG
  unit: MMBtu
  contract_size: 10000
  applies_flow_day_multiplier: false
```

## Reconciliation rule

PV, PnL, Greeks, and exposure must reconcile to clearing notional under the selected `MultiplierPolicy`. The policy ID is part of instrument identity and calculation lineage.

## Verification still required

W-003 must confirm local ICE symbol/field conventions. W-014 may use synthetic fixtures while live field mapping is still being proven.
