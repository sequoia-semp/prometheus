# Local ICE Connect/Python

Status: canonical
Last updated: 2026-06-09

## Purpose

Define how a coding agent can use a running local ICE Connect/Python instance without making CI or the repo depend on live ICE access.

## Local-only directory

```text
.ata_local/ice/
  config.yaml
  probe.json
  field_map.json
  spool/
    sample.jsonl
    events.jsonl
  quarantine/
  logs/
.ata_local/packets/
  LOCAL_ICE_OBSERVED_SURFACE.md
```

`.ata_local/` is gitignored.

## Opt-in environment

```text
ATA_ENABLE_LOCAL_ICE=1
ATA_ICE_MODE=local_live
ATA_ICE_CONFIG=.ata_local/ice/config.yaml
```

## Intended local commands

```text
uv run ata ice probe --out .ata_local/ice/probe.json
uv run ata ice field-map --probe .ata_local/ice/probe.json --out .ata_local/ice/field_map.json
uv run ata ice sample --symbols <configured-symbols> --out .ata_local/ice/spool/sample.jsonl
uv run ata ice normalize --input .ata_local/ice/spool/sample.jsonl --out .ata_local/ice/spool/events.jsonl
```

W-001 may choose the final CLI entrypoint name. The behavior must remain: probe, field-map, sample, normalize, quarantine.

## Coding-agent responsibility

When ICE is available locally, the coding agent should:

- inspect the available ICE Python module/API shape through `probe`;
- infer or build field maps;
- sample configured symbols;
- normalize into canonical event envelopes;
- quarantine unknown fields;
- keep local raw artifacts out of Git;
- convert repeatable discoveries into tests using synthetic/minimized fixtures;
- write a sanitized observed-surface packet only when the user wants to transfer findings to another instance.

## CI responsibility

CI uses fixture mode only. Local-live tests are skipped unless explicitly enabled.
