# Open Questions

Status: canonical
Last updated: 2026-06-09

Open questions are unresolved items that require user approval, market-data observation, or a later implementation spike. Accepted architecture decisions belong in ADRs, not here.

| ID | Priority | Topic | Current treatment | Blocks |
|---|---:|---|---|---|
| Q-001 | P0 | ICE Python live field surface and symbol/field mapping | Coding agent should probe the local ICE Connect/Python instance during W-003 and produce a field map. Fixture mode remains CI-safe. | Live normalization quality, not W-000/W-001 |
| Q-002 | P0 | Exact Henry option symbols and vol fields in local ICE entitlement | Probe in W-003; use synthetic fixtures for W-014 if live fields are incomplete. | Live option data, not golden-book math |
| Q-003 | P1 | Advanced VaR variants | v0 uses historical simulation, 1-day, p95/p99, 250bd lookback, absolute price-change basis, options full revaluation with v0 vol held constant. Later vol-shock models require ADR. | Later model expansion |
| Q-004 | P1 | NautilusTrader adoption | W-N1 must prove replay compatibility and strategy portability before Nautilus becomes binding. | Nautilus integration |
| Q-005 | P1 | Power vertical product shape | W-015 will bind exact PJM/ICE power instruments, delivery profiles, and settlement joins after PJM client and revaluation loop exist. | W-015 |
| Q-006 | P1 | Textual application shape | W-001 should reserve a Textual-compatible app boundary; concrete screens and widgets should be chosen after read models exist. | Textual UI beyond scaffold |
| Q-007 | P1 | opencode/Ollama runtime boundary | v0 targets local opencode/Ollama through read-only tools; exact transport, prompt context window policy, and model selection remain implementation details for the agent work items. | W-026/W-025 |
