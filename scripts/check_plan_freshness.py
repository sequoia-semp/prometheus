#!/usr/bin/env python3
"""Check active planning packet consistency.

This is intentionally lightweight and stdlib-only so it can run before the full
Python project scaffold exists.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "AGENTS.md",
    "README.md",
    "docs/planning/SOURCE_OF_TRUTH.md",
    "docs/planning/PROJECT_OVERVIEW.md",
    "docs/planning/OPEN_QUESTIONS.md",
    "docs/planning/PACKET_WORKFLOW.md",
    "docs/local/LOCAL_ICE_CONNECT.md",
    "docs/adr/ADR_INDEX.md",
    "docs/contracts/README.md",
    "docs/workscope/workscope.yaml",
    "docs/packets/current/PLANNING_PACKET.md",
    "docs/packets/current/IMPLEMENTATION_PACKET.md",
    "docs/packets/current/REVIEW_PACKET.md",
    "docs/packets/current/RECONCILIATION_PACKET.md",
    "docs/packets/current/LOCAL_ICE_PACKET.md",
    "docs/packets/current/PACKET_MANIFEST.yaml",
    "docs/codex/work_items/W-001-repo-scaffold-and-invariant-gates.md",
]

EXPECTED_WORK_ITEMS = {
    "W-000",
    "W-001",
    "W-007",
    "W-008",
    "W-009",
    "W-006",
    "W-003",
    "W-014",
    "W-026",
    "W-016",
    "W-005",
    "W-015",
    "W-N1",
    "W-025",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def check_required(errors: list[str]) -> None:
    for item in REQUIRED:
        if not (ROOT / item).exists():
            errors.append(f"missing required file: {item}")


def check_adr_index(errors: list[str]) -> None:
    index = ROOT / "docs/adr/ADR_INDEX.md"
    if not index.exists():
        return
    text = index.read_text(encoding="utf-8")
    adr_ids = sorted(set(re.findall(r"\|\s*(ADR-\d{3})\s*\|", text)))
    files: dict[str, Path] = {}
    for path in (ROOT / "docs/adr").glob("ADR-*.md"):
        match = re.match(r"(ADR-\d{3})-", path.name)
        if match:
            files[match.group(1)] = path
    missing = [adr for adr in adr_ids if adr not in files]
    if missing:
        errors.append("ADR_INDEX references missing ADR files: " + ", ".join(missing))


def check_workscope(errors: list[str]) -> None:
    path = ROOT / "docs/workscope/workscope.yaml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    ids = set(re.findall(r"^\s*- id:\s*(W-[A-Z0-9]+)", text, flags=re.MULTILINE))
    missing = sorted(EXPECTED_WORK_ITEMS - ids)
    if missing:
        errors.append("workscope missing expected work items: " + ", ".join(missing))

    if "- id: W-000" in text and "- id: W-001" in text:
        if not re.search(r"- id: W-000\n(?:  .+\n)*?  status: done", text):
            errors.append("W-000 should be marked done in the start pack")
        if not re.search(r"- id: W-001\n(?:  .+\n)*?  status: ready", text):
            errors.append("W-001 should be marked ready in the start pack")

    for packet in ["PLANNING_PACKET.md", "IMPLEMENTATION_PACKET.md"]:
        p = ROOT / "docs/packets/current" / packet
        if p.exists():
            packet_text = p.read_text(encoding="utf-8")
            not_mentioned = sorted(
                EXPECTED_WORK_ITEMS - set(re.findall(r"W-[A-Z0-9]+", packet_text))
            )
            if packet == "PLANNING_PACKET.md" and not_mentioned:
                errors.append(
                    f"{packet} does not mention expected work items: "
                    + ", ".join(not_mentioned)
                )


def parse_manifest_hashes(manifest: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    current_path: str | None = None
    for line in manifest.read_text(encoding="utf-8").splitlines():
        m_path = re.match(r"\s*- path:\s*(.+?)\s*$", line)
        if m_path:
            current_path = m_path.group(1).strip().strip('"\'')
            continue
        m_hash = re.match(r"\s*sha256:\s*([0-9a-f]{64})\s*$", line)
        if m_hash and current_path:
            hashes[current_path] = m_hash.group(1)
            current_path = None
    return hashes


def check_manifest(errors: list[str]) -> None:
    manifest = ROOT / "docs/packets/current/PACKET_MANIFEST.yaml"
    if not manifest.exists():
        return
    for source, expected in parse_manifest_hashes(manifest).items():
        path = ROOT / source
        if not path.exists():
            errors.append(f"manifest source missing: {source}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(
                f"manifest hash mismatch for {source}: expected {expected}, actual {actual}"
            )


def check_active_version_labels(errors: list[str]) -> None:
    # Avoid release-style planning tags in active planning/packet filenames.
    active_paths = list((ROOT / "docs").rglob("*.md")) + [ROOT / "README.md"]
    bad_names = [
        rel(p)
        for p in active_paths
        if re.search(r"[_-]r\d+(?:[_-]|\.)", p.name, re.IGNORECASE)
    ]
    if bad_names:
        errors.append(
            "active filenames contain release-style planning tags: " + ", ".join(bad_names)
        )


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_adr_index(errors)
    check_workscope(errors)
    check_manifest(errors)
    check_active_version_labels(errors)
    if errors:
        print("Planning/packet checks failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Planning/packet checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
