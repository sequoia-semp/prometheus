from __future__ import annotations

import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = spec_from_file_location(
    "check_plan_freshness",
    ROOT / "scripts/check_plan_freshness.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load check_plan_freshness.py")
CHECK_PLAN_FRESHNESS = module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_PLAN_FRESHNESS)
BRANCH_METADATA_KEYS = CHECK_PLAN_FRESHNESS.BRANCH_METADATA_KEYS
validate_active_packet_metadata = CHECK_PLAN_FRESHNESS.validate_active_packet_metadata


def branch_metadata() -> dict[str, str]:
    return {
        "repository": "sequoia-semp/prometheus",
        "stable_branch": "main",
        "working_branch": "codex/workflow-branch-packets",
        "preferred_branch_convention": "codex/<work-item>-<slug>",
        "packet_scope": "branch-local-current",
        "base_ref": "codex/w-006-calendar-expiry",
        "head_ref": "codex/workflow-branch-packets",
    }


def packet_metadata(active_work_item: str = "W-006") -> dict[str, dict[str, str]]:
    shared = branch_metadata()
    return {
        "PLANNING_PACKET.md": {
            **shared,
            "active_work_item": active_work_item,
        },
        "IMPLEMENTATION_PACKET.md": {
            **shared,
            "active_work_item": active_work_item,
        },
        "REVIEW_PACKET.md": {
            **shared,
            "review_target": active_work_item,
        },
        "RECONCILIATION_PACKET.md": {
            **shared,
            "active_work_item": active_work_item,
            "closed_work_item": active_work_item,
        },
        "LOCAL_ICE_PACKET.md": shared,
    }


def test_packet_metadata_validation_accepts_consistent_branch_local_packets() -> None:
    manifest = {**branch_metadata(), "active_work_item": "W-006"}

    assert validate_active_packet_metadata(packet_metadata(), manifest) == []


def test_packet_metadata_validation_rejects_active_work_item_mismatch() -> None:
    packets = packet_metadata()
    packets["REVIEW_PACKET.md"]["review_target"] = "W-001"
    manifest = {**branch_metadata(), "active_work_item": "W-006"}

    errors = validate_active_packet_metadata(packets, manifest)

    assert any("REVIEW_PACKET.md review_target" in error for error in errors)


def test_packet_metadata_validation_rejects_missing_branch_metadata() -> None:
    packets = packet_metadata()
    del packets["IMPLEMENTATION_PACKET.md"][BRANCH_METADATA_KEYS[0]]
    manifest = {**branch_metadata(), "active_work_item": "W-006"}

    errors = validate_active_packet_metadata(packets, manifest)

    assert any("IMPLEMENTATION_PACKET.md missing branch metadata" in error for error in errors)


def test_packet_freshness_script_passes_current_repo_packets() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_plan_freshness.py"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
