# ADR-034 — Agent Reasoning Loop and Evidence Binding

Status: accepted
Date: 2026-06-09

## Decision

The agent harness uses a read-only perceive/retrieve/reason/bind/guardrail loop. Every numerical claim must bind to tool results and lineage identifiers before it is emitted.

## Consequences

- v0 agent tools are typed, read-only, and whitelisted.
- No arbitrary SQL or write-capable tools.
- No autonomous order submission.
- Unsupported numerical claims are rejected by the harness before user output.
- A fixture-backed early slice (W-026) proves this before the full agent harness (W-025).
