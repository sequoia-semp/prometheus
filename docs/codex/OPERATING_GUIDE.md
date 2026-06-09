# Coding Agent Operating Guide

Status: canonical
Last updated: 2026-06-09

## Rule

Coding agents consume `AGENTS.md`, `docs/packets/current/PLANNING_PACKET.md`, and `docs/packets/current/IMPLEMENTATION_PACKET.md`. This guide explains conventions; it is not a substitute for the active implementation packet.

## Required final response

```json
{
  "work_item": "W-___",
  "summary": "",
  "files_changed": [],
  "tests_added": [],
  "tests_run": [],
  "acceptance_status": "met | partial | not_met",
  "out_of_scope_changes": [],
  "open_questions": [],
  "risks": []
}
```

## Prohibited without user approval

- Architecture changes.
- New autonomy level.
- Trading execution path.
- Second pricing/revaluation path.
- Changing canonical workscope dependencies.
