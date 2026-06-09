---
packet_type: local_ice
packet_status: current
last_updated: 2026-06-09
repository: sequoia-semp/prometheus
stable_branch: main
working_branch: codex/w-006-calendar-expiry
preferred_branch_convention: codex/<work-item>-<slug>
packet_scope: branch-local-current
base_ref: main
head_ref: codex/w-006-calendar-expiry
canonical_sources:
  - docs/adr/ADR-015-ice-python-sidecar.md
  - docs/adr/ADR-023-repo-fixture-hygiene-and-local-data-handling.md
  - docs/adr/ADR-032-local-data-scope-and-llm-context-policy.md
  - docs/contracts/ICE_PYTHON_SIDECAR.md
  - docs/local/LOCAL_ICE_CONNECT.md
  - docs/workscope/workscope.yaml
---

# Local ICE Packet

## Purpose

This packet lets a coding agent use a running local ICE Connect/Python instance during W-003 without turning local live data into a repo or CI dependency.

## Assumption

The user may provide a local, licensed, permissioned ICE Connect/Python environment. The coding agent should be able to probe it, build a field map, sample data, normalize events, and produce follow-up work items for unmapped fields.

## Modes

```text
fixture     deterministic, CI-safe, no ICE required
local_live  user-enabled local ICE Connect/Python instance
```

## Local paths

```text
.ata_local/ice/config.yaml
.ata_local/ice/probe.json
.ata_local/ice/field_map.json
.ata_local/ice/spool/*.jsonl
.ata_local/ice/quarantine/*.jsonl
.ata_local/packets/LOCAL_ICE_OBSERVED_SURFACE.md
```

`.ata_local/` is gitignored. A sanitized observed-surface summary may be copied into a packet only when the user wants to hand it to another instance.

## Expected W-003 commands

```bash
ATA_ENABLE_LOCAL_ICE=1 ata ice probe --out .ata_local/ice/probe.json
ATA_ENABLE_LOCAL_ICE=1 ata ice field-map --probe .ata_local/ice/probe.json --out .ata_local/ice/field_map.json
ATA_ENABLE_LOCAL_ICE=1 ata ice sample --symbols <symbol-config> --out .ata_local/ice/spool/sample.jsonl
ata ice normalize --input .ata_local/ice/spool/sample.jsonl --out .ata_local/ice/spool/events.jsonl
```

The exact CLI name may be set during W-001/W-003. The required behavior is stable: probe, field-map, sample, normalize, quarantine.

## Coding-agent obligations during local ICE work

- Do not import `icepython` outside the sidecar package.
- Do not require ICE for normal CI.
- Do not commit `.ata_local/` contents by default.
- Persist raw call metadata and hashes.
- Normalize into `EventEnvelope` with `source_system=ice_python` and `data_scope=local_live` for local live data.
- Quarantine unknown fields and symbols.
- Produce a local observed-surface report listing available modules/functions/fields and unresolved mappings.

## How to move local ICE findings between instances

When a planning/review instance needs local ICE results, pass a sanitized local packet such as:

```text
.ata_local/packets/LOCAL_ICE_OBSERVED_SURFACE.md
```

That packet should contain:

- command run;
- timestamp;
- module/import success or failure;
- available high-level APIs;
- symbol/field categories observed;
- normalized event examples with values redacted or minimized if desired;
- quarantine summary;
- next mapping questions.

Do not include credentials or authentication material.
