# Repo Inspection Guide

Status: canonical
Last updated: 2026-06-09

## Purpose

Use this when inspecting a live repository, branch, or PR.

## Inspection workflow

1. Read `AGENTS.md`.
2. Read `docs/packets/current/PLANNING_PACKET.md`.
3. Read `docs/packets/current/REVIEW_PACKET.md`.
4. Read changed ADRs/contracts/workscope rows.
5. Inspect changed files and PR diff.
6. Check packet freshness and source-of-truth drift.
7. Produce a structured repo state report.

## Repo state report format

```json
{
  "repo": "",
  "branch": "",
  "commit": "",
  "work_item": "",
  "files_changed": [],
  "adr_impacts": [],
  "contract_impacts": [],
  "workscope_impacts": [],
  "tests_seen": [],
  "tests_missing": [],
  "drift_findings": [],
  "verdict": "approve | request_changes | block"
}
```

## Invariants to check on every PR

- No credentials or accidental raw live data dumps.
- No `icepython` import outside sidecar.
- No second pricing path.
- No mutable event updates/deletes.
- No agent write tools, arbitrary SQL, or order tools.
- Numerical outputs carry lineage.
- Work-item acceptance criteria are tested.
- Current packets match their source files.
