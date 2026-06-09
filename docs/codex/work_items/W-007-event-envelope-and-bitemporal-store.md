# W-007 — Event Envelope and Bitemporal Store

Status: active
Depends on: W-000, W-001

## Objective

Implement append-only event envelopes and a local bitemporal event store without adding ICE, PJM, pricing, risk, UI, Nautilus, or agent runtime behavior.

## Files in scope

```text
src/ata/events/**
tests/unit/**event**
tests/integration/**event**
docs/packets/current/**
docs/workscope/workscope.yaml
scripts/check_*.py if packet/status checks need active-work-item updates
```

## Files out of scope

```text
src/ata/ice_sidecar runtime adapters
src/ata/pjm runtime client
src/ata/pricing implementation
src/ata/risk implementation
src/ata/agent runtime harness
src/ata/ui_textual screens
src/ata/nautilus runtime adapter
.ata_local/**
data/live/**
```

## Required behavior

- Append-only event API.
- Per-stream monotonic ordering.
- Bitemporal query by `as_of` and `known_at`.
- Deterministic snapshot IDs from event hashes plus version lineage.
- Event envelopes carry `source_system` and `data_scope`.
- JSONL import/export for local sidecar/spool compatibility.
- Decimal payload values serialize as strings.
- Datetimes serialize as timezone-aware UTC RFC3339.

## Acceptance criteria

- Append-only event API exists.
- Per-stream ordering works.
- Bitemporal query by `as_of` and `known_at` works.
- Snapshot IDs are deterministic.
- Envelope carries `source_system` and `data_scope`.
- JSONL import/export exists for local sidecar/spool compatibility.
- Default checks pass without ICE, PJM, Nautilus, Textual, or local LLM processes.
