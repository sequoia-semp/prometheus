# Packets

Status: canonical
Last updated: 2026-06-09

Packets are persistent handoff artifacts for moving the project between planning, coding, review, and reconciliation instances.

```text
current/PLANNING_PACKET.md        current project state and roadmap
current/IMPLEMENTATION_PACKET.md  active coding-agent task
current/REVIEW_PACKET.md          active review/adversarial task
current/RECONCILIATION_PACKET.md  post-review closeout workflow
current/LOCAL_ICE_PACKET.md       local ICE Connect/Python workflow
current/PACKET_MANIFEST.yaml      source files, hashes, and freshness metadata
archive/                          stale or historical packets
```

Current packets should be kept fresh against their source files. Archived packets may be stale if marked archived.

## Regeneration policy

Do not regenerate every packet after every tiny edit. Regenerate the current packet set when one of these occurs:

1. a new work item becomes active;
2. a current packet source file changes;
3. a review is requested;
4. review findings are dispositioned;
5. architecture/contracts/workscope change after user approval;
6. a milestone closes;
7. the user asks for a fresh standalone handoff.
