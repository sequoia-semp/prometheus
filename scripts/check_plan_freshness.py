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
    "docs/codex/work_items/W-006-calendar-and-expiry-service.md",
    "docs/codex/work_items/W-007-event-envelope-and-bitemporal-store.md",
    "docs/codex/work_items/W-008-generic-instrument-model.md",
    "docs/codex/work_items/W-009-trade-blotter-and-position-projection.md",
]

CURRENT_PACKET_PATHS = [
    "docs/packets/current/PLANNING_PACKET.md",
    "docs/packets/current/IMPLEMENTATION_PACKET.md",
    "docs/packets/current/REVIEW_PACKET.md",
    "docs/packets/current/RECONCILIATION_PACKET.md",
    "docs/packets/current/LOCAL_ICE_PACKET.md",
]

BRANCH_METADATA_KEYS = [
    "repository",
    "stable_branch",
    "working_branch",
    "preferred_branch_convention",
    "packet_scope",
    "base_ref",
    "head_ref",
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


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if not line or line.startswith(" ") or line.startswith("-"):
            continue
        match = re.match(r"([A-Za-z0-9_]+):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("'\"")
    return values


def parse_manifest_metadata(manifest: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line == "source_files:":
            break
        match = re.match(r"([A-Za-z0-9_]+):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("'\"")
    return values


def validate_active_packet_metadata(
    packet_metadata: dict[str, dict[str, str]],
    manifest_metadata: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    planning = packet_metadata.get("PLANNING_PACKET.md", {})
    implementation = packet_metadata.get("IMPLEMENTATION_PACKET.md", {})
    review = packet_metadata.get("REVIEW_PACKET.md", {})
    reconciliation = packet_metadata.get("RECONCILIATION_PACKET.md", {})

    active_work_item = planning.get("active_work_item")
    if not active_work_item:
        errors.append("PLANNING_PACKET.md missing active_work_item")
        return errors

    comparisons = {
        "IMPLEMENTATION_PACKET.md active_work_item": implementation.get("active_work_item"),
        "REVIEW_PACKET.md review_target": review.get("review_target"),
        "RECONCILIATION_PACKET.md active_work_item": reconciliation.get("active_work_item"),
        "RECONCILIATION_PACKET.md closed_work_item": reconciliation.get("closed_work_item"),
        "PACKET_MANIFEST.yaml active_work_item": manifest_metadata.get("active_work_item"),
    }
    for label, value in comparisons.items():
        if value != active_work_item:
            errors.append(f"{label} {value!r} does not match active work item {active_work_item!r}")

    for packet_name, metadata in packet_metadata.items():
        missing = [key for key in BRANCH_METADATA_KEYS if not metadata.get(key)]
        if missing:
            errors.append(f"{packet_name} missing branch metadata: " + ", ".join(missing))
        if metadata.get("packet_scope") != "branch-local-current":
            errors.append(f"{packet_name} packet_scope must be branch-local-current")

    missing_manifest = [key for key in BRANCH_METADATA_KEYS if not manifest_metadata.get(key)]
    if missing_manifest:
        errors.append(
            "PACKET_MANIFEST.yaml missing branch metadata: " + ", ".join(missing_manifest)
        )
    if manifest_metadata.get("packet_scope") != "branch-local-current":
        errors.append("PACKET_MANIFEST.yaml packet_scope must be branch-local-current")

    shared_keys = ["repository", "stable_branch", "working_branch", "base_ref", "head_ref"]
    for key in shared_keys:
        expected = manifest_metadata.get(key)
        for packet_name, metadata in packet_metadata.items():
            if metadata.get(key) != expected:
                errors.append(
                    f"{packet_name} {key} {metadata.get(key)!r} "
                    f"does not match manifest {expected!r}"
                )

    return errors


def check_packet_metadata(errors: list[str]) -> None:
    packet_metadata: dict[str, dict[str, str]] = {}
    for packet_path in CURRENT_PACKET_PATHS:
        path = ROOT / packet_path
        if path.exists():
            packet_metadata[path.name] = parse_frontmatter(path)
    manifest_path = ROOT / "docs/packets/current/PACKET_MANIFEST.yaml"
    manifest_metadata = parse_manifest_metadata(manifest_path) if manifest_path.exists() else {}
    errors.extend(validate_active_packet_metadata(packet_metadata, manifest_metadata))


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
    check_packet_metadata(errors)
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
