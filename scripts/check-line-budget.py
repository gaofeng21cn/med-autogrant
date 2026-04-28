#!/usr/bin/env python3
from __future__ import annotations

import runpy
from pathlib import Path


def main() -> int:
    canonical_script = Path(__file__).resolve().with_name("line_budget.py")
    namespace = runpy.run_path(str(canonical_script))
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
