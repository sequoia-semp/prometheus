---
packet_type: planning
packet_status: current
active_work_item: W-008
last_updated: 2026-06-09
canonical_sources:
  - AGENTS.md
  - README.md
  - docs/planning/SOURCE_OF_TRUTH.md
  - docs/planning/PROJECT_OVERVIEW.md
  - docs/planning/OPEN_QUESTIONS.md
  - docs/planning/PACKET_WORKFLOW.md
  - docs/adr/ADR_INDEX.md
  - docs/contracts/README.md
  - docs/workscope/workscope.yaml
---

# Planning Packet — Local Trading and Portfolio Analytics Platform

## Purpose

This is the portable stand-alone project-state packet. It is intended to move between local planning, coding, review, and reconciliation instances so each instance sees the current project architecture and work loop without scanning scattered files.

Canonical docs remain authoritative. This packet packages them for handoff; it does not override them.

## Mission

Build a deterministic, auditable local trading and portfolio analytics platform with:

- ICE Python sidecar ingestion from local ICE Connect/Python;
- PJM Data Miner ingestion;
- append-only bitemporal event storage;
- generic commodity/instrument modeling;
- Henry Hub ICE gas futures/options proving book;
- one authoritative pricing/risk engine;
- batch portfolio revaluation and risk time series;
- Textual-compatible operator views over read models;
- read-only evidence-bound agent tools;
- local opencode/Ollama agent harness target;
- scaffolded but spike-gated Nautilus replay boundary.

Henry Hub gas is the first demo/proving product for simplicity. PJM remains a featured product vertical and use case for power fundamentals, settlement analysis, topology-aware analytics, and PJM/ICE power joins.

## Architecture

```text
Local ICE Connect/Python
  -> ICE Python Sidecar
  -> RawIcePythonCall records
  -> Normalized market events
  -> Append-only bitemporal Event Store
  -> Instruments + Calendars + Multiplier Policies + Blotter Fold
  -> Authoritative Batch Pricer/Risk Engine
  -> Portfolio Revaluation Snapshots + Risk Time Series
  -> Textual-Compatible Operator Views / Read Models
  -> Read-only Agent Tools
  -> Local opencode/Ollama Harness
  -> Scaffolded Nautilus Replay Adapter/Spike
```

```text
PJM Data Miner
  -> RawPjmCall records
  -> Revision-aware PjmObservationEvent records
  -> Event Store
  -> Power features / reference reconstruction / settlement analysis
  -> Future PJM/ICE power vertical
```

## Non-negotiable invariants

1. ICE integration is through the ICE Python sidecar only in v0.
2. No Excel RTD workbook polling, RTD formula parsing, screen scraping, or UI automation in v0.
3. The event store is append-only and bitemporal.
4. No calculation uses unconstrained latest data. Analytics carry `as_of`, `known_at`, and snapshot/version lineage.
5. One domain pricing/risk engine is authoritative. Batch/read-model loops call that engine rather than implementing another path.
6. Henry Hub ICE gas futures/options are the first proving portfolio.
7. PJM Data Miner remains first-class and PJM remains a featured product vertical.
8. Textual UI code is presentation/read-model only and must not call source adapters directly.
9. Agent v0 is read-only. It may narrate and explain through opencode/Ollama-backed local reasoning; it may not submit orders or mutate state.
10. NautilusTrader may be scaffolded, but remains proposed/gated by W-N1 before runtime adoption.
11. Local licensed ICE data may be used locally by the operator. The repo still prevents committed credentials, secrets, and raw live data dumps.
12. Architecture, scope, autonomy, and trading-control changes require explicit user approval.

## Current ADR spine

- ADR-014: Nautilus proposed, gated by W-N1.
- ADR-015: ICE Python sidecar only.
- ADR-016: Batch pricer interface.
- ADR-019: One revaluation engine.
- ADR-021: Versioned calendars/expiry.
- ADR-023: Repo fixture hygiene/local data handling.
- ADR-024: Workscope source of truth and packet workflow.
- ADR-025: Agent autonomy ladder.
- ADR-026: Generic commodity/instrument model.
- ADR-027: Append-only bitemporal event store/data plane.
- ADR-028: Henry futures/options proving portfolio.
- ADR-029: PJM Data Miner first-class.
- ADR-030: Henry multiplier policy.
- ADR-031: European option-on-future v0; American deferred.
- ADR-032: Local data scope and LLM context policy.
- ADR-033: Live portfolio revaluation is batch read-model.
- ADR-034: Agent evidence binding.
- ADR-035: Blotter to position fold.
- ADR-036: Risk time-series retention.
- ADR-037: Broad platform scope, Henry-first demo product, PJM featured vertical, Textual compatibility, opencode/Ollama target, Nautilus scaffold boundary.

## Contract map

- `EVENT_ENVELOPE.md`: append-only bitemporal envelope with provenance/data scope.
- `ICE_PYTHON_SIDECAR.md`: fixture/local_live modes, probe/sample/normalize/spool path.
- `INSTRUMENT.md`: typed identity, reference future, exercise style, multiplier policy.
- `BLOTTER.md`: append-only trade events and `position_as_of`.
- `PRICER.md`: batch request/result and lineage.
- `RISK.md`: historical simulation VaR defaults.
- `PORTFOLIO_REVALUATION.md`: live view as batch revaluation read-model.
- `PJM_DATAMINER.md`: direct PJM client, raw calls, revision-aware observations.
- `AGENT_TOOLS.md` and `AGENT_LOOP.md`: read-only tools and evidence-bound conclusions.

## Current workscope sequence

```text
W-000  Planning-system reconciliation and packet workflow — done in this start pack
W-001  Repo scaffold and invariant gates — done
W-007  Event envelope and bitemporal store — done
W-008  Generic instrument model — active
W-009  Trade blotter and position projection
W-006  Calendars and expiry service
W-003  ICE Python sidecar fixture/local-live boundary
W-014  Henry futures/options golden book: PV, Greeks, PnL, VaR
W-026  Fixture-backed read-only agent loop
W-016  Batch revaluation loop, risk time-series, retention
W-005  PJM Data Miner direct client
W-015  PJM/ICE power vertical
W-N1   Nautilus replay go/no-go spike
W-025  Full read-only semantic agent harness
```

## Why this order

- W-001 created the repo substrate, CI/checks, invariant gates, Textual/agent/Nautilus placeholders, and package boundaries before runtime work.
- W-007 and W-008 establish event and instrument primitives.
- W-009 comes before W-014 so positions come from a deterministic blotter fold.
- W-006 supports Henry expiry and future power delivery calendars.
- W-003 can use a local ICE instance to probe and normalize real local data while fixture mode keeps CI deterministic.
- W-014 proves the math before the live-style revaluation loop.
- W-026 pulls agent evidence-binding forward against deterministic fixtures.
- W-016 adds batch live/read-model behavior after the math and event model are proven.
- W-005 and W-015 retain PJM as a featured product vertical and power-market use case.
- W-N1 evaluates Nautilus after the project already has replayable events and pricing/risk outputs; scaffold placeholders before W-N1 are allowed but non-authoritative.

## Packet workflow

Current packets persist under `docs/packets/current/`:

- `PLANNING_PACKET.md` — project state and roadmap;
- `IMPLEMENTATION_PACKET.md` — active coding task;
- `REVIEW_PACKET.md` — active adversarial review packet;
- `RECONCILIATION_PACKET.md` — closeout and next-loop packet;
- `LOCAL_ICE_PACKET.md` — local ICE Connect/Python handoff packet;
- `PACKET_MANIFEST.yaml` — sources and hashes.

Move packets between instances this way:

- planning: `AGENTS.md` + `PLANNING_PACKET.md`;
- coding: `AGENTS.md` + `PLANNING_PACKET.md` + `IMPLEMENTATION_PACKET.md`;
- review: `AGENTS.md` + `PLANNING_PACKET.md` + `REVIEW_PACKET.md` + coding summary/diff;
- closeout: `AGENTS.md` + `PLANNING_PACKET.md` + `RECONCILIATION_PACKET.md` + review findings;
- local ICE: add `LOCAL_ICE_PACKET.md` and a sanitized `.ata_local/packets/LOCAL_ICE_OBSERVED_SURFACE.md` if available.

Active packet drift fails `python3 scripts/check_plan_freshness.py`. Archived packet drift only warns.

## Open questions

The active open questions are local ICE field/symbology discovery, exact live vol observations, Textual app shape, opencode/Ollama runtime boundary, Nautilus fit, power vertical details, and W-016 cold archive format. They do not block W-001.
