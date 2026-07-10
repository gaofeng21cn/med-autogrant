from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID
from med_autogrant.stage_control_plane_parts.transition_oracle import (
    build_mag_grant_transition_oracle,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
STAGE_MANIFEST_PATH = REPO_ROOT / "agent" / "stages" / "manifest.json"
STAGE_CONTROL_PLANE_PATH = REPO_ROOT / "contracts" / "stage_control_plane.json"
SKILL_REF = "agent/skills/grant_authoring.md"
TOOL_REF = "agent/tools/domain_affordances.md"


def build_mag_family_stage_control_plane(
    *,
    family_action_catalog: Mapping[str, Any],
) -> dict[str, Any]:
    manifest = _load_stage_manifest()
    action_ids = {
        str(action["action_id"])
        for action in family_action_catalog.get("actions", [])
        if isinstance(action, Mapping) and action.get("action_id")
    }
    stages = [_stage_descriptor(stage) for stage in manifest["stages"]]
    missing_actions = sorted(
        {
            action_ref
            for stage in stages
            for action_ref in stage["allowed_action_refs"]
            if action_ref not in action_ids
        }
    )
    if missing_actions:
        raise ValueError(
            "MAG declarative stages reference missing family actions: "
            f"{missing_actions}"
        )
    return {
        "surface_kind": "family_stage_control_plane",
        "version": "family-stage-control-plane.v1",
        "plane_id": "med_autogrant_stage_control_plane",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "authority_boundary": dict(manifest["authority_boundary"]),
        "stages": stages,
        "notes": [
            "Compiled from agent/stages/manifest.json; OPL owns runtime and transition transport.",
            "Descriptor validity cannot authorize a MAG fundability, quality, package, or export verdict.",
        ],
    }


def sync_stage_control_plane(*, output_path: Path = STAGE_CONTROL_PLANE_PATH) -> Path:
    action_catalog = json.loads(
        (REPO_ROOT / "contracts" / "action_catalog.json").read_text(encoding="utf-8")
    )
    payload = build_mag_family_stage_control_plane(
        family_action_catalog=action_catalog
    )
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


def _load_stage_manifest() -> dict[str, Any]:
    payload = json.loads(STAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("agent/stages/manifest.json must be a JSON object")
    if payload.get("target_domain_id") != TARGET_DOMAIN_ID:
        raise ValueError("agent/stages/manifest.json has the wrong target_domain_id")
    stages = payload.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError("agent/stages/manifest.json must declare stages")
    stage_ids = [str(stage.get("stage_id", "")) for stage in stages if isinstance(stage, Mapping)]
    if len(stage_ids) != len(stages) or len(stage_ids) != len(set(stage_ids)) or "" in stage_ids:
        raise ValueError("agent/stages/manifest.json stage_id values must be unique and non-empty")
    if not isinstance(payload.get("authority_boundary"), Mapping):
        raise ValueError("agent/stages/manifest.json must declare authority_boundary")
    return payload


def _stage_descriptor(stage: Mapping[str, Any]) -> dict[str, Any]:
    stage_id = _required_string(stage, "stage_id")
    policy_ref = _required_repo_ref(stage, "policy_ref")
    prompt_ref = _required_repo_ref(stage, "prompt_ref")
    knowledge_refs = [_repo_ref(ref, "stage_knowledge") for ref in _string_list(stage, "knowledge_refs")]
    quality_gate_refs = [
        _repo_ref(ref, "stage_quality_gate") for ref in _string_list(stage, "quality_gate_refs")
    ]
    next_stage_refs = _string_list(stage, "next_stage_refs")
    return {
        "stage_id": stage_id,
        "stage_kind": _required_string(stage, "stage_kind"),
        "title": _required_string(stage, "title"),
        "summary": _required_string(stage, "summary"),
        "goal": _required_string(stage, "goal"),
        "owner": TARGET_DOMAIN_ID,
        "selected_executor": {
            "executor_kind": "codex_cli",
            "default_executor": True,
            "runtime_owner": "one-person-lab",
        },
        "domain_stage_refs": [],
        "inputs": [],
        "knowledge_refs": knowledge_refs,
        "skills": [_repo_ref(SKILL_REF, "domain_skill_declaration")],
        "prompt_refs": [_repo_ref(prompt_ref, "stage_prompt")],
        "tool_refs": [_repo_ref(TOOL_REF, "stage_tool_affordance_catalog")],
        "allowed_action_refs": _string_list(stage, "allowed_action_refs"),
        "outputs": [],
        "evaluation": quality_gate_refs,
        "handoff": {
            "next_owner": "one-person-lab" if next_stage_refs else TARGET_DOMAIN_ID,
            "next_stage_refs": next_stage_refs,
            "closeout_ref_policy": "mag_owner_receipt_typed_blocker_human_gate_or_route_back",
        },
        "source_refs": [_repo_ref(policy_ref, "declarative_stage_policy")],
        "freshness": {
            "source_ref": policy_ref,
            "refresh_policy": "reload_agent_stage_manifest",
        },
        "stage_contract": {
            "requires": _string_list(stage, "requires"),
            "ensures": _string_list(stage, "ensures"),
            "boundary_assumptions": [
                "OPL owns runtime transport; MAG owns grant judgment and owner closeout."
            ],
            "properties": [],
            "runtime_assumptions": [],
            "monitor_refs": [],
            "source_scope_refs": [_repo_ref(policy_ref, "stage_policy_source")],
            "artifact_scope_refs": [],
            "workspace_scope_refs": [],
        },
        "trust_boundary": {
            "lane": _required_string(stage, "trust_lane"),
            "owner_receipt_required": True,
            "human_gate_required": stage_id == "package_and_submit_ready",
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "opl_can_write_grant_truth": False,
            "opl_can_authorize_quality_or_export": False,
            "provider_completion_counts_as_domain_completion": False,
        },
    }


def _repo_ref(ref: str, role: str) -> dict[str, str]:
    _ensure_repo_ref_exists(ref)
    return {"ref": ref, "ref_kind": "repo_path", "role": role}


def _required_repo_ref(stage: Mapping[str, Any], field: str) -> str:
    ref = _required_string(stage, field)
    _ensure_repo_ref_exists(ref)
    return ref


def _ensure_repo_ref_exists(ref: str) -> None:
    path = Path(ref)
    if path.is_absolute() or ".." in path.parts or not (REPO_ROOT / path).is_file():
        raise ValueError(f"declarative stage ref does not resolve to a repo file: {ref}")


def _required_string(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"declarative stage field must be a non-empty string: {field}")
    return value.strip()


def _string_list(payload: Mapping[str, Any], field: str) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"declarative stage field must be a string list: {field}")
    return [item.strip() for item in value]


if __name__ == "__main__":
    print(sync_stage_control_plane())
