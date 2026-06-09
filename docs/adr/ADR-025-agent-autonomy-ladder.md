# ADR-025 — Agent Autonomy Ladder

Status: accepted
Date: 2026-06-09

## Decision

v0 agent autonomy is read-only narration and analysis. The initial local LLM target is opencode/Ollama behind typed tool wrappers. Later stages may draft `TradeIntent` objects, but no LLM may submit, modify, or cancel orders directly.

## Consequences

- Agent v0 tools are read-only and whitelisted.
- Local model backends cannot bypass the tool whitelist or evidence-binding checks.
- No arbitrary SQL tool is exposed.
- Trade execution requires deterministic validation and a later explicit user-approved ADR.
