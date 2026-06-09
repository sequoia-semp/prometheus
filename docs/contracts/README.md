# Contracts Index

Status: canonical
Last updated: 2026-06-09

Contracts define boundaries coding agents must implement against.

| Contract | Purpose |
|---|---|
| EVENT_ENVELOPE.md | Common envelope for raw and normalized events |
| INSTRUMENT.md | Typed commodity/instrument identity and multiplier policies |
| ICE_PYTHON_SIDECAR.md | ICE sidecar events, local-live/fixture modes, isolation rules |
| PJM_DATAMINER.md | PJM API ingestion and revision semantics |
| BLOTTER.md | Append-only trade blotter to deterministic position projection |
| PRICER.md | Batch pricer/risk interface and lineage |
| RISK.md | Portfolio-level VaR and risk outputs |
| PORTFOLIO_REVALUATION.md | Live portfolio view as batch revaluation read-model |
| RISK_TIMESERIES.md | Position/PnL/Greeks/VaR through time and retention policy |
| AGENT_TOOLS.md | Read-only semantic/agent tool whitelist |
| AGENT_LOOP.md | Agent reasoning loop, evidence binding, and guardrails |
| TRADE_INTENT.md | Later structured trade proposal contract; never direct execution |
