# ICE Python Sidecar

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-015, ADR-023, ADR-032

## Scope

The sidecar is the only package allowed to import `icepython`. It runs locally on the ICE-authenticated machine and writes raw calls plus normalized events.

## Modes

```text
fixture     deterministic CI-safe fixture adapter
local_live  local licensed ICE Connect/Python adapter, never required in CI
```

## Suggested package surface

```text
packages/ice_sidecar/
  adapter.py
  fixture_adapter.py
  local_ice_adapter.py
  probe.py
  normalize.py
  spool.py
  cli.py
```

## Local commands to implement

```bash
ata ice probe --out .ata_local/ice/probe.json
ata ice field-map --probe .ata_local/ice/probe.json --out .ata_local/ice/field_map.json
ata ice sample --symbols <symbol-config> --out .ata_local/ice/spool/sample.jsonl
ata ice normalize --input .ata_local/ice/spool/sample.jsonl --out .ata_local/ice/spool/events.jsonl
```

## Loops

### Quote loop

- Start publisher/subscription.
- Subscribe to configured symbols/fields.
- Poll deltas or fetch refreshed values.
- Persist raw call records and normalized quote events.

### Trade/time-and-sales loop

- Poll time-and-sales with rolling cursor.
- Use overlap windows.
- Dedupe conservatively.
- Persist raw call records and normalized trade events.

### Settlement/vol loop

- Fetch settlement, option, and volatility-related fields where available.
- Persist raw call records even when normalization fails.
- Quarantine unknown or unexpected fields.

## Events

```text
RawIcePythonCall
QuoteEvent
TradeEvent
SettlementEvent
VolObservationEvent
IceSidecarHeartbeat
IceSidecarError
IceFieldMapObserved
IceNormalizationQuarantine
```

## Rules

- `.ata_local/ice/**` is gitignored by default.
- CI uses fixture mode only.
- Local live mode requires an explicit environment flag such as `ATA_ENABLE_LOCAL_ICE=1`.
- Unknown fields are quarantined rather than silently dropped.
- Raw payload hashes may be stored; raw payload bodies should remain local unless intentionally promoted.
