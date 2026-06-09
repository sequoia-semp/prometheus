# W-006 — Calendar and Expiry Service

Status: active
Depends on: W-008

## Objective

Implement versioned calendars, expiry rules, delivery periods, delivery profiles, and settlement anchors without adding pricing, risk, source adapters, UI screens, Nautilus runtime behavior, or agent runtime behavior.

## Files in scope

```text
src/ata/calendars/**
tests/unit/**calendar**
docs/packets/current/**
docs/workscope/workscope.yaml
docs/codex/work_items/W-006-calendar-and-expiry-service.md
scripts/check_*.py if active-work-item checks need updating
```

## Required behavior

- Versioned calendar object.
- Henry last-trading-day/expiry rule representation.
- Settlement anchors as versioned domain inputs.
- Delivery periods for contract months.
- Power 5x16 delivery profile representation without schema fork.
- Outputs include `calendar_version`.

## Acceptance criteria

- Henry last-trading-day/expiry rule is represented.
- Settlement anchors are versioned inputs.
- Power calendars and 5x16 delivery profiles can be versioned.
- `calendar_version` is emitted into relevant outputs.
- Default checks pass without ICE Connect/Python, PJM live data, Nautilus, Textual, GitHub Actions, release automation, or local LLM processes.
