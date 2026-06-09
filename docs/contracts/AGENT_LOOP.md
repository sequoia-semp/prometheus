# Agent Loop

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-034

## Purpose

Define the reasoning loop for the local LLM harness that analyzes commodity-trading problems using typed, read-only, whitelisted tools. The target local model backends are opencode/Ollama, but model transport is not allowed to bypass tool guardrails or evidence binding.

## Loop

```text
perceive question + context policy
  -> retrieve with whitelisted read-only tools
  -> reason with LLM
  -> bind evidence to claims
  -> guardrail check
  -> emit AgentConclusion or rejection
```

## Shapes

```python
class AgentSession:
    session_id: str
    autonomy_level: str          # narrate | draft_intent, never execute
    context_policy_id: str
    model_backend: str | None    # e.g. opencode | ollama
    created_at: datetime

class AgentTurn:
    turn_id: str
    session_id: str
    question: str
    tool_calls: list[ToolCallRecord]
    conclusion: AgentConclusion | None
    rejected_reason: str | None

class ToolCallRecord:
    tool_name: str
    args: dict
    result_ref: str
    market_snapshot_id: str | None
    source_event_ids: list[str]

class EvidenceBinding:
    claim: str
    tool_call_ids: list[str]
    as_of: datetime
    known_at: datetime
    market_snapshot_id: str
    book_version: str
    calculation_version: str
    source_event_ids: list[str]
    warnings: list[str]
    var_method: str | None
    var_horizon_days: int | None
    var_confidence: list[float] | None
    var_lookback: str | None
    var_return_basis: str | None

class AgentConclusion:
    turn_id: str
    narrative: str
    numerical_claims: list[EvidenceBinding]
    proposed_trade_intent: dict | None
```

## Guardrails

1. No number without complete evidence binding.
2. Tool calls must be in the v0 whitelist.
3. No arbitrary SQL, filesystem write, order mutation, credential access, or source-data deletion.
4. v0 autonomy is `narrate` only. `draft_intent` is future and still non-executable.
5. Every turn persists tool-call records and result IDs for replay/review.
6. The harness should validate the rendered narrative for unsupported numbers, not only the structured `numerical_claims` field.
7. Local model backends receive bounded tool outputs and context policy summaries, not unrestricted raw local data dumps.

## Early proving slice

W-026 runs a fixture-backed read-only loop against the Henry proving book to test evidence binding before the full W-025 agent harness.
