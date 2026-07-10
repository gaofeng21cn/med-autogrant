#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGE_MANIFEST_PATH = REPO_ROOT / "agent" / "stages" / "manifest.json"
LEGACY_STAGE_CONTROL_PLANE_PATH = REPO_ROOT / "contracts" / "stage_control_plane.json"
LEGACY_STAGE_COMPILER_PATH = REPO_ROOT / "src" / "med_autogrant" / "stage_control_plane.py"
FIXED_OPL_CONTRACTS = {
    "action_catalog.json": "family_action_catalog",
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
        if stage_manifest.get("version") != "mag-declarative-stage-manifest.v1":
            errors.append("agent/stages/manifest.json: version is missing or invalid")
        if stage_manifest.get("target_domain_id") != "med-autogrant":
            errors.append("agent/stages/manifest.json: target_domain_id must be med-autogrant")
        if stage_manifest.get("owner") != stage_manifest.get("target_domain_id"):
            errors.append("agent/stages/manifest.json: owner must match target_domain_id")
        authority = stage_manifest.get("authority_boundary")
        required_authority = {
            "domain_truth_owner": "med-autogrant",
            "fundability_verdict_owner": "med-autogrant",
            "authoring_quality_verdict_owner": "med-autogrant",
            "submission_ready_export_verdict_owner": "med-autogrant",
            "package_authority_owner": "med-autogrant",
            "opl_role": "descriptor_runtime_and_transition_carrier",
            "opl_can_write_grant_truth": False,
            "opl_can_authorize_quality_or_export": False,
        }
        if not isinstance(authority, dict) or any(
            authority.get(field) != value for field, value in required_authority.items()
        ):
            errors.append("agent/stages/manifest.json: authority_boundary is missing or invalid")
        stages = stage_manifest.get("stages")
        if not isinstance(stages, list) or not stages:
            errors.append("agent/stages/manifest.json: stages must be a non-empty list")
        else:
            actions = contracts.get("action_catalog.json", {}).get("actions")
            action_ids = {
                action.get("action_id")
                for action in actions
                if isinstance(action, dict)
                and isinstance(action.get("action_id"), str)
            } if isinstance(actions, list) else set()
            valid_stages: list[tuple[int, dict[str, object]]] = []
            for index, stage in enumerate(stages):
                if not isinstance(stage, dict):
                    errors.append(f"agent/stages/manifest.json: stage[{index}] must be an object")
                else:
                    valid_stages.append((index, stage))
            stage_ids = [stage.get("stage_id") for _, stage in valid_stages]
            for stage_id in {
                value
                for value in stage_ids
                if isinstance(value, str) and stage_ids.count(value) > 1
            }:
                errors.append(
                    f"agent/stages/manifest.json: duplicate stage_id: {stage_id!r}"
                )
            known_stage_ids = {value for value in stage_ids if isinstance(value, str)}
            repo_root = REPO_ROOT.resolve()
            for index, stage in valid_stages:
                for field in (
                    "stage_id",
                    "stage_kind",
                    "title",
                    "summary",
                    "goal",
                    "policy_ref",
                    "prompt_ref",
                    "trust_lane",
                ):
                    value = stage.get(field)
                    if not isinstance(value, str) or not value.strip():
                        errors.append(
                            f"agent/stages/manifest.json: stage[{index}].{field} "
                            "must be a non-empty string"
                        )
                for field in (
                    "knowledge_refs",
                    "quality_gate_refs",
                    "allowed_action_refs",
                    "requires",
                    "ensures",
                    "next_stage_refs",
                ):
                    values = stage.get(field)
                    if not isinstance(values, list) or any(
                        not isinstance(value, str) or not value.strip() for value in values
                    ):
                        errors.append(
                            f"agent/stages/manifest.json: stage[{index}].{field} "
                            "must be a list of non-empty strings"
                        )
                for field in (
                    "policy_ref",
                    "prompt_ref",
                    "knowledge_refs",
                    "quality_gate_refs",
                ):
                    refs = stage.get(field)
                    if isinstance(refs, str):
                        refs = [refs]
                    if not isinstance(refs, list):
                        continue
                    for ref in refs:
                        if not isinstance(ref, str) or not ref.strip():
                            continue
                        resolved = (REPO_ROOT / ref).resolve()
                        if not resolved.is_relative_to(repo_root):
                            errors.append(
                                f"agent/stages/manifest.json: stage[{index}].{field}: "
                                f"unsafe repo ref: {ref!r}"
                            )
                        elif not resolved.is_file():
                            errors.append(
                                f"agent/stages/manifest.json: stage[{index}].{field}: "
                                f"missing repo ref: {ref!r}"
                            )
                allowed_action_refs = stage.get("allowed_action_refs")
                if isinstance(allowed_action_refs, list):
                    for action_ref in allowed_action_refs:
                        if isinstance(action_ref, str) and action_ref not in action_ids:
                            errors.append(
                                f"agent/stages/manifest.json: stage[{index}]: "
                                f"unknown allowed_action_ref: {action_ref!r}"
                            )
                next_stage_refs = stage.get("next_stage_refs")
                if isinstance(next_stage_refs, list):
                    for next_stage_ref in next_stage_refs:
                        if isinstance(next_stage_ref, str) and next_stage_ref not in known_stage_ids:
                            errors.append(
                                f"agent/stages/manifest.json: stage[{index}]: "
                                f"unknown next_stage_ref: {next_stage_ref!r}"
                            )

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
