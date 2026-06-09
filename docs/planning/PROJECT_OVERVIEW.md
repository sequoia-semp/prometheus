# Project Overview

Status: canonical
Last updated: 2026-06-09

## Mission

Build a deterministic, auditable local trading and portfolio analytics platform for commodity trading. The platform should ingest ICE desktop data through ICE Python, ingest PJM public data through PJM Data Miner, value futures/options/positions, compute live/replay PV, Greeks, PnL, VaR, expose Textual-compatible operator views, and expose a typed read-only semantic/agent layer with evidence-bound answers for a local opencode/Ollama harness.

The first proving product is ICE Henry Hub gas futures and options. PJM remains a featured product vertical and use case for power fundamentals, settlement analysis, topology-aware workflows, and PJM/ICE power joins after the shared event, instrument, pricing, risk, and agent contracts are stable.

## Architecture spine

```text
ICE Connect / ICE Python Sidecar
    -> RawIcePythonCall
    -> QuoteEvent / TradeEvent / SettlementEvent / VolObservationEvent
    -> Append-only bitemporal Event Store
    -> Instrument Model + Calendars + Curves + Vol Surfaces
    -> Trade Blotter -> Position Fold
    -> One Authoritative Batch Pricer/Risk Engine
    -> Portfolio Revaluation Snapshots + Risk Time Series
    -> Textual-Compatible Operator Views / Read Models
    -> Read-only Agent Tools / Semantic Layer
    -> Local opencode/Ollama Harness
    -> Optional Nautilus Replay Spike
    -> Later staged execution path, never direct LLM execution
```

PJM path:

```text
PJM Data Miner Client
    -> RawPjmDataMinerCall
    -> PjmObservationEvent / PjmRevisionEvent
    -> Append-only Event Store
    -> Power features / settlement analysis / PJM-ICE power vertical
```

## Binding decisions

- v0 ICE integration uses ICE Python only.
- No Excel RTD workbook polling, RTD formula parser, or screen scraping in v0.
- ICE Python is isolated to the sidecar package.
- The first proving book is Henry Hub ICE gas futures/options.
- PJM Data Miner remains first-class and PJM remains a featured product vertical.
- Textual compatibility is required for operator views, but UI code may not become a business-logic layer.
- The local LLM target is opencode/Ollama through read-only evidence-bound tools.
- NautilusTrader remains a proposed/spike-gated runtime integration, not the project source of truth.
- The event store is append-only and bitemporal.
- The domain pricer/risk engine is the single authoritative valuation path.
- Agent v0 is read-only narration and analysis only.

## Implementation sequence

The canonical sequence is in `docs/workscope/workscope.yaml`. Current high-level order:

```text
W-000  planning-system reconciliation and packet workflow
W-001  repo scaffold, CI, invariant gates, local-first substrate
W-007  event envelope and bitemporal store
W-008  generic instrument model
W-009  trade blotter and position projection
W-006  calendars and expiry service
W-003  ICE Python sidecar fixture/local-live boundary
W-014  Henry futures/options golden book: PV, Greeks, PnL, VaR
W-026  fixture-backed read-only agent loop
W-016  batch revaluation loop, risk time-series, retention
W-005  PJM Data Miner direct client
W-015  PJM/ICE power vertical
W-N1   Nautilus replay go/no-go spike
W-025  full read-only semantic agent harness
```

## Local-first engineering posture

The first implementation should run locally. Python is the initial implementation language, but contracts and event logs should remain language-neutral and Rust/Serde-friendly so that Rust components or NautilusTrader adapters can be added later.

Recommended substrate for W-001:

- `uv` workspace and lockfile;
- `ruff` formatting/lint;
- `pyright` or equivalent strict type checking;
- `pytest` plus targeted property tests;
- package placeholders for Textual-compatible UI, local LLM agent adapters, and Nautilus replay integration;
- deterministic JSON serialization;
- Decimal values serialized as strings;
- timezone-aware UTC RFC3339 timestamps with exchange timezone metadata where needed;
- append-only local store with JSONL import/export and SQLite indexes for v0.

## Non-goals for the first tranche

- Autonomous order submission.
- A second valuation engine.
- Direct ICE Python imports outside sidecar.
- Premature Nautilus runtime adoption before the replay spike.
- Full PJM/ICE power vertical before the Henry proving book and revaluation loop are stable.
