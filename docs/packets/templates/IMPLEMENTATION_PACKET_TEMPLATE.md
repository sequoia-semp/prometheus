---
packet_type: implementation
packet_status: draft
active_work_item: W-XXX
last_updated: YYYY-MM-DD
canonical_sources: []
---

# Implementation Packet — W-XXX

## Task

## Files in scope

## Files out of scope

## Required design to preserve

## Acceptance criteria

## Required commands

## Coding-agent final response

Return both structured JSON and a human-readable handoff.

### Structured JSON

```json
{
  "work_item": "W-XXX",
  "repository": "sequoia-semp/prometheus",
  "base_ref": "",
  "head_ref": "",
  "working_branch": "",
  "implementation_base_commit": "",
  "implementation_head_commit": "",
  "summary": "",
  "changed_files": [],
  "files_changed": [],
  "tests_added": [],
  "tests_run": [],
  "tests_not_run": [],
  "acceptance_status": "met | partial | not_met",
  "out_of_scope_changes": [],
  "open_questions": [],
  "risks": [],
  "review_packet_path": "docs/packets/current/REVIEW_PACKET.md",
  "planning_packet_path": "docs/packets/current/PLANNING_PACKET.md",
  "implementation_packet_path": "docs/packets/current/IMPLEMENTATION_PACKET.md",
  "reconciliation_packet_path": "docs/packets/current/RECONCILIATION_PACKET.md"
}
```

### Human handoff

```text
Implementation pass complete.

Repository: sequoia-semp/prometheus
Work item: <WORK_ITEM>
Working branch: <WORKING_BRANCH>
Review base: <BASE_REF>
Review head: <HEAD_REF>
Implementation commit range: <BASE_COMMIT>..<HEAD_COMMIT>

Files changed:
- <file>

Tests/checks run:
- <command>: <pass/fail/not run>

Acceptance status:
- <met | partial | not_met>
- Notes: <brief notes>

Out-of-scope changes:
- <none or list>

Known risks / open questions:
- <none or list>

Reviewer read order:
1. AGENTS.md
2. docs/packets/current/PLANNING_PACKET.md
3. docs/packets/current/REVIEW_PACKET.md
4. This coding-agent handoff
5. The implementation diff for the commit range above

Paste this to the adversarial reviewer:

---
Please review the implementation pass for <WORK_ITEM>.

Repository: sequoia-semp/prometheus
Working branch: <WORKING_BRANCH>
Review base: <BASE_REF or BASE_COMMIT>
Review head: <HEAD_REF or HEAD_COMMIT>
Implementation commit range: <BASE_COMMIT>..<HEAD_COMMIT>

Read in this order:
1. AGENTS.md
2. docs/packets/current/PLANNING_PACKET.md
3. docs/packets/current/REVIEW_PACKET.md
4. Coding-agent handoff below
5. Diff for the commit range above

Review against the packet's declared scope and blocking findings. First verify packet branch metadata. Do not compare against unrelated main state or stale packets.
---

After review, paste this to the reconciliation/planning instance:

---
Please reconcile the completed review for <WORK_ITEM>.

Repository: sequoia-semp/prometheus
Working branch: <WORKING_BRANCH>
Review base: <BASE_REF or BASE_COMMIT>
Review head: <HEAD_REF or HEAD_COMMIT>

Read in this order:
1. AGENTS.md
2. docs/packets/current/PLANNING_PACKET.md
3. docs/packets/current/RECONCILIATION_PACKET.md
4. Coding-agent handoff
5. Review JSON/result
6. Human/user dispositions

Close the loop by dispositioning findings, updating canonical docs if needed, updating workscope status, refreshing packets and manifest, and selecting the next active work item.
---
```
