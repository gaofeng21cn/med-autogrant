#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from med_autogrant.stage_control_plane import build_mag_family_stage_control_plane


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXED_OPL_CONTRACTS = {
    "pack_compiler_input.json": "opl_domain_pack_compiler_input",
    "generated_surface_handoff.json": "opl_generated_surface_handoff",
    "stage_control_plane.json": "family_stage_control_plane",
    "functional_privatization_audit.json": "functional_privatization_audit",
}


def main() -> int:
    errors: list[str] = []
    contracts: dict[str, dict[str, object]] = {}
    for filename, surface_kind in FIXED_OPL_CONTRACTS.items():
        path = REPO_ROOT / "contracts" / filename
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{filename}: unreadable JSON: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{filename}: must be a JSON object")
            continue
        if payload.get("surface_kind") != surface_kind:
            errors.append(f"{filename}: surface_kind must be {surface_kind}")
        contracts[filename] = payload

    action_catalog = json.loads(
        (REPO_ROOT / "contracts" / "action_catalog.json").read_text(encoding="utf-8")
    )
    expected_stage_plane = build_mag_family_stage_control_plane(
        family_action_catalog=action_catalog
    )
    if contracts.get("stage_control_plane.json") != expected_stage_plane:
        errors.append(
            "stage_control_plane.json: stale; run "
            "scripts/run-python-clean.sh -m med_autogrant.stage_control_plane"
        )

    pack = contracts.get("pack_compiler_input.json", {})
    listed_paths = pack.get("required_domain_pack_paths")
    if not isinstance(listed_paths, list):
        errors.append("pack_compiler_input.json: required_domain_pack_paths must be a list")
    else:
        for relative_path in listed_paths:
            if not isinstance(relative_path, str) or not (REPO_ROOT / relative_path).is_file():
                errors.append(f"pack_compiler_input.json: missing pack path: {relative_path!r}")

    audit = contracts.get("functional_privatization_audit.json", {})
    modules = audit.get("modules")
    if not isinstance(modules, list) or not modules:
        errors.append("functional_privatization_audit.json: modules must be a non-empty list")
    else:
        forbidden_classes = {"opl_owned_replacement", "temporary_migration_bridge", "retire_tombstone"}
        for module in modules:
            if isinstance(module, dict) and module.get("classification") in forbidden_classes:
                errors.append(
                    "functional_privatization_audit.json: unresolved private platform residue: "
                    f"{module.get('module_id')}"
                )

    if errors:
        print("descriptor contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("descriptor contract check ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
