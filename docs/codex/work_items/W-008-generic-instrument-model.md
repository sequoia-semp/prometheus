# W-008 — Generic Instrument Model

Status: active
Depends on: W-000, W-001

## Objective

Implement generic commodity instrument identities and multiplier policies without adding pricing, risk, source adapters, UI screens, Nautilus runtime behavior, or agent runtime behavior.

## Files in scope

```text
src/ata/instruments/**
tests/unit/**instrument**
docs/packets/current/**
docs/workscope/workscope.yaml
docs/codex/work_items/W-008-generic-instrument-model.md
scripts/check_*.py if active-work-item checks need updating
```

## Files out of scope

```text
src/ata/pricing implementation
src/ata/risk implementation
src/ata/ice_sidecar runtime adapters
src/ata/pjm runtime client
src/ata/calendars expiry implementation
src/ata/agent runtime harness
src/ata/ui_textual screens
src/ata/nautilus runtime adapter
```

## Required behavior

- `InstrumentIdentity` typed object.
- `MultiplierPolicy` typed object.
- Deterministic canonical string ID derived from typed fields.
- Deterministic JSON round-trip.
- Henry LD1 future can be modeled.
- European Henry option-on-future can be modeled with explicit `reference_future_id`.
- American option is representable but can be detected as unsupported by v0 pricing.
- Power 5x16 placeholder identity can be represented without schema fork.

## Acceptance criteria

- Henry LD1 future modeled.
- European Henry option-on-future modeled with exercise_style and reference_future_id.
- American-style option is representable but rejected by v0 pricing model marker.
- Power 5x16 placeholder config works without schema fork.
- MultiplierPolicy has explicit policy_id and source/version.
- Instrument identity round-trips deterministically.
- Default checks pass without ICE Connect/Python, PJM live data, Nautilus, Textual, GitHub Actions, release automation, or local LLM processes.
