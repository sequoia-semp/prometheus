# ADR-015 — ICE Python Sidecar

Status: accepted
Date: 2026-06-09

## Decision

Use ICE Python as the only v0 ICE integration path.

The ICE integration runs as a local sidecar process and emits:

- `RawIcePythonCall`
- `QuoteEvent`
- `TradeEvent`
- `SettlementEvent`
- `VolObservationEvent`
- `IceSidecarHeartbeat`
- `IceSidecarError`

## Explicit non-decisions

The project will not build these in v0:

- Excel RTD workbook polling.
- RTD formula parsing.
- Screen scraping.
- In-process ICE Python calls from strategy, pricing, risk, or agent code.

## Consequences

- `icepython` import is allowed only in the sidecar package.
- All other services consume normalized events, event-store data, or fixtures.
- CI blocks accidental ICE imports outside the sidecar.
- Tests use fixture mode and do not require live ICE.
- Local live mode is enabled only on the user's licensed machine.
