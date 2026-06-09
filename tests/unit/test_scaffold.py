from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_expected_packages_import() -> None:
    packages = [
        "ata",
        "ata.events",
        "ata.instruments",
        "ata.calendars",
        "ata.blotter",
        "ata.pricing",
        "ata.risk",
        "ata.ice_sidecar",
        "ata.pjm",
        "ata.agent",
        "ata.ui_textual",
        "ata.nautilus",
    ]
    for package in packages:
        importlib.import_module(package)


def test_invariant_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_invariants.py"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
