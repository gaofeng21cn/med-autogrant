#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO_ROOT / "contracts" / "private_functional_surface_policy.json"


def build_source_purity_guard_readback() -> dict[str, Any]:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    forbidden_paths = policy.get("forbidden_source_paths")
    if not isinstance(forbidden_paths, list) or not all(
        isinstance(path, str) and path for path in forbidden_paths
    ):
        raise SystemExit("private functional surface policy must declare forbidden_source_paths")
    present = sorted(path for path in forbidden_paths if (REPO_ROOT / path).exists())
    return {
        "surface_kind": "mag_source_purity_guard_readback",
        "schema_version": 2,
        "target_domain_id": "med-autogrant",
        "state": "passed_repo_source_guard_only" if not present else "failed",
        "failed_checks": [
            {"check_id": "forbidden_private_platform_path_present", "path": path}
            for path in present
        ],
        "checked_policy_ref": "contracts/private_functional_surface_policy.json",
        "checked_forbidden_path_count": len(forbidden_paths),
        "present_forbidden_paths": present,
        "authority_boundary": {
            "guard_can_sign_owner_receipt": False,
            "guard_can_create_typed_blocker": False,
            "guard_can_claim_external_runtime_ready": False,
            "guard_can_claim_grant_ready": False,
            "guard_can_claim_submission_ready": False,
            "guard_can_claim_production_ready": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check retired MAG private platform paths.")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    args = parser.parse_args(argv)
    payload = build_source_purity_guard_readback()
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{payload['surface_kind']}: {payload['state']}")
    return 0 if payload["state"] == "passed_repo_source_guard_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
