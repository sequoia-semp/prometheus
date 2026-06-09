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
CURRENT_PACKET_PATHS = CHECK_PLAN_FRESHNESS.CURRENT_PACKET_PATHS
canonical_sources_by_packet = CHECK_PLAN_FRESHNESS.canonical_sources_by_packet
parse_manifest_hashes = CHECK_PLAN_FRESHNESS.parse_manifest_hashes
validate_active_packet_metadata = CHECK_PLAN_FRESHNESS.validate_active_packet_metadata
validate_branch_metadata = CHECK_PLAN_FRESHNESS.validate_branch_metadata
validate_handoff_contract_text = CHECK_PLAN_FRESHNESS.validate_handoff_contract_text
validate_manifest_coverage = CHECK_PLAN_FRESHNESS.validate_manifest_coverage


def branch_metadata() -> dict[str, str]:
    return {
        "repository": "sequoia-semp/prometheus",
        "stable_branch": "main",
        "working_branch": "codex/w-006-calendar-expiry",
        "preferred_branch_convention": "codex/<work-item>-<slug>",
        "packet_scope": "branch-local-current",
        "base_ref": "main",
        "head_ref": "codex/w-006-calendar-expiry",
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
            "reconciliation_target": active_work_item,
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


def test_packet_metadata_validation_rejects_reconciliation_target_mismatch() -> None:
    packets = packet_metadata()
    packets["RECONCILIATION_PACKET.md"]["reconciliation_target"] = "W-000B"
    manifest = {**branch_metadata(), "active_work_item": "W-006"}

    errors = validate_active_packet_metadata(packets, manifest)

    assert any("RECONCILIATION_PACKET.md reconciliation_target" in error for error in errors)


def test_packet_metadata_validation_rejects_missing_branch_metadata() -> None:
    packets = packet_metadata()
    del packets["IMPLEMENTATION_PACKET.md"][BRANCH_METADATA_KEYS[0]]
    manifest = {**branch_metadata(), "active_work_item": "W-006"}

    errors = validate_active_packet_metadata(packets, manifest)

    assert any("IMPLEMENTATION_PACKET.md missing branch metadata" in error for error in errors)


def test_manifest_covers_all_packet_canonical_sources() -> None:
    manifest = parse_manifest_hashes(ROOT / "docs/packets/current/PACKET_MANIFEST.yaml")

    errors = validate_manifest_coverage(canonical_sources_by_packet(), manifest, "W-006")

    assert errors == []


def test_missing_canonical_source_file_is_rejected() -> None:
    manifest = parse_manifest_hashes(ROOT / "docs/packets/current/PACKET_MANIFEST.yaml")
    packet_sources = {
        "docs/packets/current/PLANNING_PACKET.md": ["docs/nope/MISSING.md"],
    }

    errors = validate_manifest_coverage(packet_sources, manifest, "W-006")

    assert any(
        "canonical source missing on disk: docs/nope/MISSING.md" in error for error in errors
    )


def test_canonical_source_absent_from_manifest_is_rejected() -> None:
    manifest = parse_manifest_hashes(ROOT / "docs/packets/current/PACKET_MANIFEST.yaml")
    manifest.pop("AGENTS.md", None)
    packet_sources = {
        "docs/packets/current/PLANNING_PACKET.md": ["AGENTS.md"],
    }

    errors = validate_manifest_coverage(packet_sources, manifest, "W-006")

    assert any("canonical source absent from manifest: AGENTS.md" in error for error in errors)


def test_manifest_hash_mismatch_is_rejected() -> None:
    manifest = parse_manifest_hashes(ROOT / "docs/packets/current/PACKET_MANIFEST.yaml")
    manifest["AGENTS.md"] = "0" * 64
    packet_sources = {
        "docs/packets/current/PLANNING_PACKET.md": ["AGENTS.md"],
    }

    errors = validate_manifest_coverage(packet_sources, manifest, "W-006")

    assert any("manifest hash mismatch for canonical source AGENTS.md" in error for error in errors)


def test_current_packet_files_are_manifest_sources() -> None:
    manifest = parse_manifest_hashes(ROOT / "docs/packets/current/PACKET_MANIFEST.yaml")

    missing = [path for path in CURRENT_PACKET_PATHS if path not in manifest]

    assert missing == []


def test_branch_check_allows_expected_branch() -> None:
    errors = validate_branch_metadata("codex/w-006-calendar-expiry", branch_metadata())

    assert errors == []


def test_branch_check_rejects_mismatch() -> None:
    errors = validate_branch_metadata("codex/workflow-branch-packets", branch_metadata())

    assert errors == [
        "current branch 'codex/workflow-branch-packets' does not match packet working_branch "
        "'codex/w-006-calendar-expiry'"
    ]


def test_branch_check_skips_when_override_set() -> None:
    errors = validate_branch_metadata(
        "codex/workflow-branch-packets",
        branch_metadata(),
        skip=True,
    )

    assert errors == []


def test_branch_check_skips_detached_head() -> None:
    errors = validate_branch_metadata(None, branch_metadata())

    assert errors == []


def test_implementation_packet_contains_review_handoff_fields() -> None:
    text = (ROOT / "docs/packets/current/IMPLEMENTATION_PACKET.md").read_text(
        encoding="utf-8"
    )

    assert "implementation_base_commit" in text
    assert "implementation_head_commit" in text
    assert "changed_files" in text
    assert "Paste this to the adversarial reviewer" in text


def test_implementation_packet_contains_reconciliation_handoff_fields() -> None:
    text = (ROOT / "docs/packets/current/IMPLEMENTATION_PACKET.md").read_text(
        encoding="utf-8"
    )

    assert "After review, paste this to the reconciliation/planning instance" in text
    assert "reconciliation_packet_path" in text


def test_review_packet_requires_coding_agent_handoff() -> None:
    text = (ROOT / "docs/packets/current/REVIEW_PACKET.md").read_text(encoding="utf-8")

    assert "coding-agent final JSON/handoff" in text
    assert "the declared implementation diff or commit range" in text


def test_reconciliation_packet_requires_coding_agent_handoff() -> None:
    text = (ROOT / "docs/packets/current/RECONCILIATION_PACKET.md").read_text(
        encoding="utf-8"
    )

    assert "coding-agent final JSON/handoff" in text
    assert "review JSON/result" in text


def test_handoff_contract_text_validation_passes_current_packets() -> None:
    assert validate_handoff_contract_text(ROOT) == []


def test_packet_freshness_script_passes_current_repo_packets() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_plan_freshness.py"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
