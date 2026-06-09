# Adversarial Review Guide

Status: canonical
Last updated: 2026-06-09

## Purpose

Use this guide and the current review packet when sending project plans, packets, or PR diffs to an adversarial reviewer.

## Inputs

- `AGENTS.md`
- `docs/packets/current/PLANNING_PACKET.md`
- `docs/packets/current/REVIEW_PACKET.md`
- Relevant ADRs/contracts if the packet requests them
- PR diff, coding-agent summary, or changed files under review

## Review mandate

Find:

- blockers;
- contradictions;
- stale packets;
- hidden architecture changes;
- under-specified contracts;
- missing tests;
- source-of-truth drift;
- project-invariant violations;
- trading/risk defects;
- agent/autonomy risks.

## Output format

```json
{
  "verdict": "approve | request_changes | block",
  "blockers": [],
  "major_findings": [],
  "minor_findings": [],
  "missing_decisions": [],
  "missing_tests": [],
  "scope_drift_warnings": [],
  "suggested_adr_changes": [],
  "suggested_workscope_changes": [],
  "findings_to_reject_or_defer": [],
  "summary": ""
}
```
