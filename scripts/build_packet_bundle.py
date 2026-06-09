#!/usr/bin/env python3
"""Build a portable packet bundle zip from the current repo packet set."""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "dist"
OUT = OUT_DIR / "ata_current_packet_bundle.zip"
INCLUDE = [
    "AGENTS.md",
    "README.md",
    "docs/packets/current/PLANNING_PACKET.md",
    "docs/packets/current/IMPLEMENTATION_PACKET.md",
    "docs/packets/current/REVIEW_PACKET.md",
    "docs/packets/current/RECONCILIATION_PACKET.md",
    "docs/packets/current/LOCAL_ICE_PACKET.md",
    "docs/packets/current/PACKET_MANIFEST.yaml",
    "docs/workscope/workscope.yaml",
    "docs/planning/SOURCE_OF_TRUTH.md",
    "docs/planning/PROJECT_OVERVIEW.md",
    "docs/planning/OPEN_QUESTIONS.md",
    "docs/planning/PACKET_WORKFLOW.md",
    "docs/local/LOCAL_ICE_CONNECT.md",
    "docs/adr/ADR_INDEX.md",
    "docs/contracts/README.md",
]


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in INCLUDE:
            path = ROOT / item
            if path.exists():
                zf.write(path, item)
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
