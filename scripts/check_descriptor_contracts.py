#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGE_MANIFEST_PATH = REPO_ROOT / "agent" / "stages" / "manifest.json"
LEGACY_STAGE_CONTROL_PLANE_PATH = REPO_ROOT / "contracts" / "stage_control_plane.json"
LEGACY_STAGE_COMPILER_PATH = REPO_ROOT / "src" / "med_autogrant" / "stage_control_plane.py"
FIXED_OPL_CONTRACTS = {
    "pack_compiler_input.json": "opl_domain_pack_compiler_input",
    "generated_surface_handoff.json": "opl_generated_surface_handoff",
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

    try:
        stage_manifest = json.loads(STAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"agent/stages/manifest.json: unreadable JSON: {exc}")
        stage_manifest = {}
    if not isinstance(stage_manifest, dict):
        errors.append("agent/stages/manifest.json: must be a JSON object")
    else:
        if stage_manifest.get("surface_kind") != "mag_declarative_stage_manifest":
            errors.append(
                "agent/stages/manifest.json: surface_kind must be mag_declarative_stage_manifest"
            )
        if stage_manifest.get("target_domain_id") != "med-autogrant":
            errors.append("agent/stages/manifest.json: target_domain_id must be med-autogrant")
        stages = stage_manifest.get("stages")
        if not isinstance(stages, list) or not stages:
            errors.append("agent/stages/manifest.json: stages must be a non-empty list")

    for legacy_path in (LEGACY_STAGE_CONTROL_PLANE_PATH, LEGACY_STAGE_COMPILER_PATH):
        if legacy_path.exists():
            errors.append(
                f"retired private stage compiler surface must remain absent: "
                f"{legacy_path.relative_to(REPO_ROOT)}"
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
