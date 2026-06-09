#!/usr/bin/env python3
"""Check scaffold-level architecture invariants.

This script is intentionally stdlib-only so it can run before optional dev tools
or local market-data integrations are installed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_WORK_ITEMS = [
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
]

PROTECTED_GITIGNORE_PATTERNS = [
    ".ata_local/",
    "credentials/",
    "tokens/",
    "secrets/",
    "data/live/",
    "data/local_live/",
    "*.env",
    "*.pem",
    "*.key",
    "*.token",
]

FORBIDDEN_AGENT_TOOL_NAMES = [
    "arbitrary_sql",
    "filesystem_write",
    "submit_order",
    "modify_order",
    "delete_market_data",
    "mutate_book",
    "access_credentials",
]

SOURCE_ADAPTER_IMPORT_RE = re.compile(
    r"^\s*(?:from\s+ata\.(?:ice_sidecar|pjm)\b|import\s+ata\.(?:ice_sidecar|pjm)\b)",
    re.MULTILINE,
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def iter_python_files() -> list[Path]:
    ignored_parts = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
    return [
        path
        for path in ROOT.rglob("*.py")
        if not any(part in ignored_parts for part in path.relative_to(ROOT).parts)
    ]


def check_icepython_import_boundary(errors: list[str]) -> None:
    import_re = re.compile(r"^\s*(?:import\s+icepython\b|from\s+icepython\b)", re.MULTILINE)
    allowed_root = ROOT / "src/ata/ice_sidecar"
    for path in iter_python_files():
        if not import_re.search(path.read_text(encoding="utf-8")):
            continue
        if allowed_root not in path.parents and path != allowed_root / "__init__.py":
            errors.append(f"icepython import outside sidecar: {path.relative_to(ROOT)}")


def check_gitignore_protects_local_data(errors: list[str]) -> None:
    patterns = set(read(".gitignore").splitlines())
    missing = [pattern for pattern in PROTECTED_GITIGNORE_PATTERNS if pattern not in patterns]
    if missing:
        errors.append("missing gitignore protections: " + ", ".join(missing))


def check_agent_tool_contract(errors: list[str]) -> None:
    text = read("docs/contracts/AGENT_TOOLS.md")
    match = re.search(r"## v0 tools(?P<body>.*?)## Forbidden in v0", text, flags=re.S)
    if not match:
        errors.append("AGENT_TOOLS.md missing v0/forbidden section boundary")
        return
    v0_body = match.group("body")
    forbidden_present = [name for name in FORBIDDEN_AGENT_TOOL_NAMES if name in v0_body]
    if forbidden_present:
        errors.append("forbidden agent tools listed as v0 tools: " + ", ".join(forbidden_present))


def check_adr_index(errors: list[str]) -> None:
    text = read("docs/adr/ADR_INDEX.md")
    indexed = sorted(set(re.findall(r"\|\s*(ADR-\d{3})\s*\|", text)))
    files: set[str] = set()
    for path in (ROOT / "docs/adr").glob("ADR-*.md"):
        match = re.match(r"(ADR-\d{3})-", path.name)
        if match:
            files.add(match.group(1))
    missing = [adr for adr in indexed if adr not in files]
    if missing:
        errors.append("ADR_INDEX references missing ADR files: " + ", ".join(missing))


def check_workscope_sequence(errors: list[str]) -> None:
    text = read("docs/workscope/workscope.yaml")
    missing = [
        item
        for item in EXPECTED_WORK_ITEMS
        if not re.search(rf"^\s*- id:\s*{item}$", text, re.M)
    ]
    if missing:
        errors.append("workscope missing expected work items: " + ", ".join(missing))


def check_active_filename_labels(errors: list[str]) -> None:
    active_paths = list((ROOT / "docs").rglob("*.md")) + [ROOT / "README.md"]
    bad_names = [
        str(path.relative_to(ROOT))
        for path in active_paths
        if re.search(r"[_-]r\d+(?:[_-]|\.)", path.name, re.IGNORECASE)
    ]
    if bad_names:
        errors.append(
            "active filenames contain release-style planning tags: " + ", ".join(bad_names)
        )


def check_scaffold_boundaries(errors: list[str]) -> None:
    boundary_roots = [
        ROOT / "src/ata/agent",
        ROOT / "src/ata/ui_textual",
        ROOT / "src/ata/nautilus",
        ROOT / "apps/ata_tui",
    ]
    forbidden_terms = re.compile(
        r"\b(?:icepython|nautilus_trader|submit_order|modify_order|mutate_book|arbitrary_sql)\b"
    )
    for root in boundary_roots:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if SOURCE_ADAPTER_IMPORT_RE.search(text):
                errors.append(f"scaffold boundary imports source adapter: {path.relative_to(ROOT)}")
            match = forbidden_terms.search(text)
            if match:
                errors.append(
                    f"scaffold boundary contains runtime/forbidden term "
                    f"{match.group(0)!r}: {path.relative_to(ROOT)}"
                )


def main() -> int:
    errors: list[str] = []
    check_icepython_import_boundary(errors)
    check_gitignore_protects_local_data(errors)
    check_agent_tool_contract(errors)
    check_adr_index(errors)
    check_workscope_sequence(errors)
    check_active_filename_labels(errors)
    check_scaffold_boundaries(errors)
    if errors:
        print("Invariant checks failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Invariant checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
