#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from med_autogrant.product_entry_parts.source_purity_guard_readback import (
    build_source_purity_guard_readback,
)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check MAG strict source-purity guard readback.")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    payload = build_source_purity_guard_readback()
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            f"{payload['surface_kind']}: {payload['state']} "
            f"({len(payload['failed_checks'])} failed checks)"
        )
    return 0 if payload["state"] == "passed_repo_source_guard_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
