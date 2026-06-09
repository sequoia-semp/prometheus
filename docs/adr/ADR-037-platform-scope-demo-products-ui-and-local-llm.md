# ADR-037 — Platform Scope, Demo Products, UI, and Local LLM

Status: accepted
Date: 2026-06-09

## Decision

The project is a broad local trading and portfolio analytics platform, not a PJM-only workbench. Henry Hub ICE gas futures and options are the first proving product because they are simpler and well suited to validating instruments, blotter folds, pricing, risk, revaluation, and agent evidence binding.

PJM remains a featured product vertical and use case. PJM public/fundamental data, PJM/ICE power joins, topology-aware analytics, and future PJM-focused workflows must stay first-class in the roadmap and package boundaries.

The v0 scaffold must preserve compatibility with a Textual terminal UI and a local LLM harness targeting opencode/Ollama. NautilusTrader should be present as a scaffolded integration boundary, but it remains spike-gated by W-N1 before it can become a runtime dependency or authoritative spine.

## Consequences

- Package boundaries must support gas, power, portfolio analytics, UI read models, and agent tools without product-specific forks.
- The first golden book is Henry Hub gas futures/options; PJM work follows after event, instrument, sidecar, revaluation, and risk contracts are stable enough to reuse.
- Textual UI code is presentation-only and must read from derived views/read models rather than directly from source adapters.
- Local LLM integration is read-only in v0 and must use evidence-bound tool outputs rather than raw unrestricted data dumps.
- Nautilus-related files may exist in the scaffold, but no production path may depend on Nautilus before W-N1 produces an accepted go/no-go decision.
