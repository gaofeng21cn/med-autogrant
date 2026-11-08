#!/usr/bin/env python3
"""Project tracked MAG domain resources into its self-contained native carrier."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CARRIER = ROOT / "plugins/med-autogrant"
AREAS = ("agent", "contracts", "schemas", "runtime", "src/med_autogrant", "docs")
FILES = (
    "README.md", "README.zh-CN.md", "LICENSE", "pyproject.toml", "uv.lock",
    "assets/branding/medautogrant-logo.png",
    "assets/branding/medautogrant-overview-v3.png",
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z", "--", *AREAS, *FILES], cwd=ROOT,
    ).decode().split("\0")
    expected = {
        CARRIER / path: ROOT / path
        for path in tracked if path and Path(path).name != ".gitkeep"
    }
    expected[CARRIER / "skills/med-autogrant/SKILL.md"] = ROOT / "agent/primary_skill/SKILL.md"
    expected[CARRIER / "app-contribution-adapter.json"] = ROOT / "app-contribution-adapter.json"
    # Only these generated domain directories are pruned; native metadata stays owned.
    stale = [
        path for area in AREAS for path in (CARRIER / area).rglob("*")
        if (path.is_file() or path.is_symlink()) and path not in expected
    ]
    for destination, source in expected.items():
        if source.is_symlink() or destination.is_symlink() or not source.is_file():
            raise SystemExit(f"Projection requires regular source and destination files: {source}")
    mismatches = [
        path for path, source in expected.items()
        if not path.is_file() or path.read_bytes() != source.read_bytes()
    ]
    if args.check:
        if stale or mismatches:
            raise SystemExit("Carrier resources differ; run python3 scripts/sync_carrier.py")
        print(f"Carrier resources: PASS ({len(expected)} exact files)")
        return
    for destination in mismatches:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(expected[destination], destination)
    for path in stale:
        path.unlink()
    print(f"Projected {len(expected)} source files ({len(mismatches)} updated, {len(stale)} removed)")


if __name__ == "__main__":
    main()
