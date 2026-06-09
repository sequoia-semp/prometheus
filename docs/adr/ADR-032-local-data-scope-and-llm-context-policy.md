# ADR-032 — Local Data Scope and LLM Context Policy

Status: accepted
Date: 2026-06-09

## Decision

The system is intended for local licensed/permissioned users. The architecture should not block local ICE/PJM development on legal/entitlement gates. It should still maintain data provenance, repo hygiene, and explicit context policy.

## Data scopes

Use `data_scope` on event envelopes and local artifacts:

```text
synthetic      deterministic test/fixture data
public         public source data, such as PJM public API observations
derived        calculated outputs derived from stored observations
local_live     local licensed-user data captured on the user's machine
```

## Context policy

The agent harness may use local data in model context when the user intentionally runs the local workflow. Credentials, tokens, authentication material, and secrets never enter model context.

## Consequences

- `EVENT_ENVELOPE.md` carries `source_system` and `data_scope`.
- CI does not require local live data.
- Local ICE outputs live under `.ata_local/` by default.
- No legal/entitlement blocker prevents W-003 implementation when a local ICE Connect/Python instance is available.
