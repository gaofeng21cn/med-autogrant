#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CODE_SUFFIXES = {".py", ".sh", ".js", ".ts", ".tsx", ".jsx"}
TARGET_LINE_COUNT = 1000
HARD_LINE_LIMIT = 1500
LEGACY_OVER_TARGET_BUDGETS = {
    "src/med_autogrant/grant_autonomy_controller.py": 1055,
}


def tracked_code_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        REPO_ROOT / relative_path
        for relative_path in completed.stdout.splitlines()
        if (REPO_ROOT / relative_path).suffix in CODE_SUFFIXES
    ]


def main() -> int:
    over_target: list[str] = []
    over_limit: list[str] = []
    new_or_grown_over_target: list[str] = []
    for path in tracked_code_files():
        line_count = sum(1 for _ in path.open(encoding="utf-8"))
        relative_path = path.relative_to(REPO_ROOT).as_posix()
        if line_count > HARD_LINE_LIMIT:
            over_limit.append(f"{line_count:5d} {relative_path}")
        elif line_count > TARGET_LINE_COUNT:
            over_target.append(f"{line_count:5d} {relative_path}")
            allowed_line_count = LEGACY_OVER_TARGET_BUDGETS.get(relative_path)
            if allowed_line_count is None or line_count > allowed_line_count:
                budget = allowed_line_count or TARGET_LINE_COUNT
                new_or_grown_over_target.append(f"{line_count:5d} {relative_path} (budget {budget})")

    if over_limit or new_or_grown_over_target:
        if over_limit:
            print(f"tracked code files over hard limit ({HARD_LINE_LIMIT} lines):", file=sys.stderr)
            print("\n".join(over_limit), file=sys.stderr)
        if new_or_grown_over_target:
            print(
                f"tracked code files newly over target or above registered budget ({TARGET_LINE_COUNT} lines):",
                file=sys.stderr,
            )
            print("\n".join(new_or_grown_over_target), file=sys.stderr)
        return 1
    if over_target:
        print(f"tracked code files over target ({TARGET_LINE_COUNT} lines), within registered budgets:")
        print("\n".join(over_target))
    print(f"line budget ok: all tracked code files <= {HARD_LINE_LIMIT} hard-limit lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
