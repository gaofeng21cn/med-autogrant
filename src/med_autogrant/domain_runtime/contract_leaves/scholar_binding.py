from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from med_autogrant._opl_helpers.capability_binding import (
    REQUIRED_NON_USABLE_OBSERVATIONS as SCHOLAR_SKILL_REQUIRED_NON_USABLE_OBSERVATIONS,
    CapabilityBindingError,
    select_direct_route_exports,
    validate_required_capability_binding_contract,
)

from med_autogrant.workspace_types import WorkspaceStateError


SCHOLAR_SKILL_BINDING_CONTRACT_RELATIVE_PATH = Path(
    "contracts/scholar_skill_binding_contract.json"
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
    try:
        return validate_required_capability_binding_contract(
            payload,
            expected_surface_kind="mag_scholar_skill_binding_contract",
            expected_version="mag-scholar-skill-binding.v3",
            expected_consumer_agent_id="mag",
            expected_provider_package_id="mas-scholar-skills",
            expected_consumer_profile_id="mag-medical-grant.v1",
            provider_completion_field="provider_completion_is_mag_completion",
            required_block_fields=SCHOLAR_SKILL_REQUIRED_BLOCK_FIELDS,
            non_usable_action="fail_closed_mag_dependency",
            identity_error="MAG Scholar Skill binding contract identity is invalid.",
            boundary_error="MAG Scholar Skill binding contract boundary is invalid.",
        )
    except CapabilityBindingError as exc:
        raise WorkspaceStateError(str(exc)) from exc


def scholar_skill_ids_for_direct_route(route_id: str) -> list[str]:
    contract = read_scholar_skill_binding_contract()
    try:
        return select_direct_route_exports(
            contract,
            route_id,
            missing_route_error=f"MAG direct route 缺少 Scholar Skill binding: {route_id}",
            undeclared_export_error_prefix="MAG direct route 引用了 consumer profile 之外的 Scholar Skill: ",
        )
    except CapabilityBindingError as exc:
        raise WorkspaceStateError(str(exc)) from exc


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
