# ADR-023 — Repo Fixture Hygiene and Local Data Handling

Status: accepted
Date: 2026-06-09

## Decision

This is a local licensed-user system. Local live data may be used during development on the user's machine. The repository still must not accidentally commit credentials, authentication material, or raw live data dumps.

## Consequences

- `.ata_local/`, `data/live/`, local ICE probe outputs, and credentials are gitignored.
- Checked-in fixtures should be synthetic, public, or intentionally minimized examples.
- CI uses fixture mode only.
- Sanitized local probe summaries may be copied into packets when helpful, but raw local payloads should stay local unless the user explicitly chooses otherwise.
