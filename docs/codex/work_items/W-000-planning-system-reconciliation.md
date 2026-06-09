# Work Item: W-000 — Planning-System Reconciliation and Packet Workflow

Status: ready
Owner: coding agent
Type: documentation/contracts/scaffold only
Runtime code: forbidden

## Objective

Install and reconcile the repo-persistent planning, review, implementation, reconciliation, and local ICE packet workflow. This work item starts the project by making the repository itself coherent and LLM-transferable.

## Files in scope

```text
README.md
AGENTS.md
docs/planning/**
docs/adr/**
docs/contracts/**
docs/reviews/**
docs/codex/**
docs/packets/**
docs/workscope/workscope.yaml
scripts/check_plan_freshness.py
scripts/build_packet_bundle.py
.gitignore
```

## Files out of scope

```text
packages/**
src/**
apps/**
tests/live/**
credentials/**
data/live/**
.ata_local/**
```

## Requirements

1. Use stable filenames; no release-style planning version tags in active filenames.
2. Persist the current packet set under `docs/packets/current/`.
3. Preserve the full architecture plan: ICE sidecar, PJM, event store, instrument model, blotter, pricing/risk, revaluation, agent loop, and Nautilus spike.
4. Make packets stand-alone enough to move between planning, coding, and review instances.
5. Add or maintain a manifest and freshness check so packet/source mismatch is flagged.
6. Do not implement runtime ICE, pricing, event-store, PJM, Nautilus, or agent code.

## Acceptance criteria

- [ ] `docs/packets/current/PLANNING_PACKET.md` exists.
- [ ] `docs/packets/current/IMPLEMENTATION_PACKET.md` exists.
- [ ] `docs/packets/current/REVIEW_PACKET.md` exists.
- [ ] `docs/packets/current/RECONCILIATION_PACKET.md` exists.
- [ ] `docs/packets/current/LOCAL_ICE_PACKET.md` exists.
- [ ] `docs/packets/current/PACKET_MANIFEST.yaml` exists.
- [ ] `docs/workscope/workscope.yaml` includes the complete current work sequence.
- [ ] `ADR_INDEX.md` references only ADR files that exist.
- [ ] `EVENT_ENVELOPE.md` uses local data-scope/provenance fields.
- [ ] `INSTRUMENT.md` includes exercise style, reference future, and multiplier policy linkage.
- [ ] `RISK.md` closes v0 VaR details.
- [ ] `AGENTS.md` instructs agents to read packets in the correct order.
- [ ] `scripts/check_plan_freshness.py` fails on current packet/source mismatch.
- [ ] No runtime code is added.

## Required commands

```bash
python3 scripts/check_plan_freshness.py
```

## Final response required

```json
{
  "work_item": "W-000",
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
