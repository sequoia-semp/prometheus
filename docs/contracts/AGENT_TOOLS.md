# Agent Tools

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-025, ADR-034

## v0 tools

Read-only only. These tools are the boundary available to local opencode/Ollama-backed reasoning:

```text
resolve_instrument
get_market_snapshot
value_book
compute_greeks
explain_pnl
get_positions
get_blotter
get_var
get_risk_timeseries
get_ice_sidecar_status
get_pjm_observations
describe_data_quality
```

## Forbidden in v0

```text
arbitrary_sql
filesystem_write
submit_order
modify_order
delete_market_data
mutate_book
access_credentials
```

## Answer invariant

No numerical claim without a tool result carrying:

```text
as_of
known_at
market_snapshot_id
book_version
calculation_version
source_event_ids
warnings
```

VaR and risk-time-series claims must additionally carry method, horizon, confidence levels, lookback, and return basis.
