#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

DEFAULT_LIMIT = 1000
CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".mts",
    ".cts",
    ".sh",
    ".bash",
    ".zsh",
    ".rs",
    ".go",
}
IGNORED_PARTS = {"node_modules", "dist", "build", "coverage", ".venv", "__pycache__"}
IGNORED_SUFFIXES = (".min.js",)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail when tracked code files exceed the line budget.")
    parser.add_argument("--list", action="store_true", help="list tracked code files over the default budget")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    tracked_files = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()

    oversize: list[tuple[str, int]] = []
    for relative_path in tracked_files:
        if not is_code_file(relative_path):
            continue
        absolute_path = repo_root / relative_path
        if not absolute_path.is_file():
            continue
        line_count = count_lines(absolute_path)
        if line_count <= DEFAULT_LIMIT:
            continue
        oversize.append((relative_path, line_count))

    oversize.sort(key=lambda item: (-item[1], item[0]))
    if args.list:
        for relative_path, line_count in oversize:
            print(f"{line_count:6d} {relative_path}")
        return 0

    if oversize:
        print(f"line budget check failed ({len(oversize)} issue{'s' if len(oversize) != 1 else ''}):")
        for relative_path, line_count in oversize:
            print(f"- {relative_path}: {line_count} lines exceeds {DEFAULT_LIMIT} line budget")
        return 1
    return 0


def is_code_file(relative_path: str) -> bool:
    path = Path(relative_path)
    if any(part in IGNORED_PARTS for part in path.parts):
        return False
    if relative_path.endswith(IGNORED_SUFFIXES):
        return False
    return path.suffix in CODE_EXTENSIONS


def count_lines(path: Path) -> int:
    content = path.read_text(encoding="utf-8")
    if not content:
        return 0
    return len(content.splitlines())


if __name__ == "__main__":
    raise SystemExit(main())
