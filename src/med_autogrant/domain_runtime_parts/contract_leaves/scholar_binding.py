from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from med_autogrant.workspace_types import WorkspaceStateError


SCHOLAR_SKILL_BINDING_CONTRACT_RELATIVE_PATH = Path(
    "contracts/scholar_skill_binding_contract.json"
)
SCHOLAR_SKILL_REQUIRED_NON_USABLE_OBSERVATIONS = frozenset(
    {
        "missing",
        "incompatible",
        "disabled",
        "unmaterialized",
        "unobserved",
    }
)
SCHOLAR_SKILL_REQUIRED_BLOCK_FIELDS = frozenset(
    {
        "blocks_mag_install",
        "blocks_stage_launch",
        "blocks_stage_route",
        "blocks_operational_readiness",
        "blocks_grant_core",
        "blocks_fundability_core",
        "blocks_quality_core",
        "blocks_export_core",
    }
)


def read_scholar_skill_binding_contract(
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    resolved_repo_root = (repo_root or Path(__file__).resolve().parents[4]).resolve()
    contract_path = resolved_repo_root / SCHOLAR_SKILL_BINDING_CONTRACT_RELATIVE_PATH
    try:
        payload = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkspaceStateError(
            f"无法读取 MAG Scholar Skill binding contract: {contract_path}"
        ) from exc
    if (
        not isinstance(payload, dict)
        or payload.get("surface_kind") != "mag_scholar_skill_binding_contract"
        or payload.get("version") != "mag-scholar-skill-binding.v3"
        or payload.get("consumer_agent_id") != "mag"
        or payload.get("provider_package_id") != "mas-scholar-skills"
        or payload.get("consumer_profile_id") != "mag-medical-grant.v1"
    ):
        raise WorkspaceStateError(
            "MAG Scholar Skill binding contract identity is invalid."
        )
    eligible_export_ids = payload.get("eligible_export_ids")
    direct_route_bindings = payload.get("direct_route_bindings")
    invocation_policy = payload.get("invocation_policy")
    availability_policy = payload.get("availability_policy")
    authority_boundary = payload.get("authority_boundary")
    known_non_usable_observations = (
        availability_policy.get("known_non_usable_observations")
        if isinstance(availability_policy, dict)
        else None
    )
    if (
        payload.get("enhancement_kind") != "required_dependency"
        or payload.get("handoff_mode") != "refs_only"
        or payload.get("provider_required") is not True
        or not isinstance(eligible_export_ids, list)
        or not eligible_export_ids
        or not all(isinstance(item, str) and item for item in eligible_export_ids)
        or not isinstance(direct_route_bindings, dict)
        or not isinstance(invocation_policy, dict)
        or invocation_policy.get("provider_completion_is_mag_completion") is not False
        or invocation_policy.get("provider_gap_is_hard_stop") is not True
        or invocation_policy.get("provider_gap_can_create_typed_blocker") is not False
        or invocation_policy.get("provider_gap_can_select_stage_route") is not False
        or not isinstance(availability_policy, dict)
        or availability_policy.get("usable_observation") != "available_compatible"
        or not isinstance(known_non_usable_observations, list)
        or not all(
            isinstance(item, str) and item
            for item in known_non_usable_observations
        )
        or not SCHOLAR_SKILL_REQUIRED_NON_USABLE_OBSERVATIONS.issubset(
            set(known_non_usable_observations)
        )
        or "available_compatible" in known_non_usable_observations
        or availability_policy.get("available_compatible_action")
        != "select_required_declared_skills"
        or availability_policy.get("other_observation_action")
        != "fail_closed_mag_dependency"
        or availability_policy.get("accepted_gap_outputs")
        != ["diagnostic", "typed_blocker_ref"]
        or availability_policy.get("quality_hint_is_advisory") is not False
        or availability_policy.get("creates_typed_blocker") is not False
        or any(
            availability_policy.get(field) is not True
            for field in SCHOLAR_SKILL_REQUIRED_BLOCK_FIELDS
        )
        or not isinstance(authority_boundary, dict)
        or not authority_boundary
        or any(value is not False for value in authority_boundary.values())
    ):
        raise WorkspaceStateError(
            "MAG Scholar Skill binding contract boundary is invalid."
        )
    return payload


def scholar_skill_ids_for_direct_route(route_id: str) -> list[str]:
    contract = read_scholar_skill_binding_contract()
    bindings = contract["direct_route_bindings"]
    selected = bindings.get(route_id)
    if (
        not isinstance(selected, list)
        or not selected
        or not all(isinstance(item, str) and item for item in selected)
    ):
        raise WorkspaceStateError(
            f"MAG direct route 缺少 Scholar Skill binding: {route_id}"
        )
    eligible_export_ids = set(contract["eligible_export_ids"])
    undeclared = [
        skill_id for skill_id in selected if skill_id not in eligible_export_ids
    ]
    if undeclared:
        raise WorkspaceStateError(
            "MAG direct route 引用了 consumer profile 之外的 Scholar Skill: "
            + ", ".join(undeclared)
        )
    return selected


def build_direct_scholar_skill_prompt_lines(route_id: str) -> list[str]:
    selected_skill_ids = scholar_skill_ids_for_direct_route(route_id)
    return [
        "",
        "Required refs-only professional Skill dependency:",
        f"- Consumer profile: mag-medical-grant.v1; required Skill ids for this route: {', '.join(selected_skill_ids)}.",
        "- Resolve the required provider identity and callability before this MAG route, using the current grant artifact ref, source_pack_ref, and epistemic scope.",
        "- Missing, incompatible, disabled, unmaterialized, unobserved, or otherwise non-usable provider state is a MAG dependency blocker: fail closed before install, Stage launch, Stage route, operational readiness, grant work, fundability, quality, or export.",
        "- Shared Skill outputs are refs-only professional candidates: source_pack_ref, candidate_refs, owner_gate_handoff_ref, or route_back_candidate.",
        "- MAG must consume, reject, or route back each candidate against current sources before changing grant truth.",
        "- Candidate refs, provider gaps, and provider completion cannot authorize fundability, quality, export, grant-ready, submission-ready, operational-readiness, owner-receipt, route, or typed-blocker claims.",
    ]
