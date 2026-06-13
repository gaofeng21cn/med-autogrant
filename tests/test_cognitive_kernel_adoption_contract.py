from __future__ import annotations

import json
from pathlib import Path

import pytest

from med_autogrant import opl_standard_pack as opl_standard_pack_module
from med_autogrant import stage_control_plane as stage_control_plane_module
from med_autogrant.stage_control_plane_parts.cognitive_kernel import (
    COGNITIVE_KERNEL_ADOPTION_REF,
    COGNITIVE_KERNEL_STAGE_PACK_REQUIRED_SECTIONS,
    DOMAIN_PACK_TOOL_AFFORDANCE_REF,
    GOLDEN_PATH_PROFILE_REF,
    MAG_TOOL_AFFORDANCE_BOUNDARY,
    pack_compiler_cognitive_kernel_fields,
    plane_cognitive_kernel_refs,
    stage_descriptor_cognitive_kernel_fields,
)


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_STAGE_PACK_SECTIONS = COGNITIVE_KERNEL_STAGE_PACK_REQUIRED_SECTIONS


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def _refs(entries: list[dict[str, object]]) -> set[str]:
    return {str(entry["ref"]) for entry in entries}


def test_mag_pack_declares_advisory_cognitive_kernel_contracts() -> None:
    pack = _read_json("contracts/pack_compiler_input.json")
    adoption = _read_json("contracts/cognitive_kernel_adoption.json")
    golden = _read_json("contracts/golden_path_profile.json")

    assert opl_standard_pack_module.pack_compiler_cognitive_kernel_fields is pack_compiler_cognitive_kernel_fields
    assert pack["stage_pack_required_sections"] == REQUIRED_STAGE_PACK_SECTIONS
    assert pack["cognitive_kernel_adoption_ref"] == COGNITIVE_KERNEL_ADOPTION_REF
    assert pack["golden_path_profile_ref"] == GOLDEN_PATH_PROFILE_REF
    assert "tool_affordance_catalog" in pack["declarative_domain_pack"]
    assert "agent/tools/domain_affordances.md" in pack["required_domain_pack_paths"]
    assert (REPO_ROOT / "agent/tools/domain_affordances.md").is_file()

    tool_refs = pack["tool_refs"]
    assert tool_refs == [DOMAIN_PACK_TOOL_AFFORDANCE_REF]

    boundary = pack["tool_affordance_boundary"]
    assert boundary["catalog_role"] == MAG_TOOL_AFFORDANCE_BOUNDARY["catalog_role"]
    assert boundary["executor_autonomy"]["executor_can_choose_order_and_parallelism"] is True
    assert boundary["executor_autonomy"]["tool_catalog_can_prescribe_tool_sequence"] is False
    assert "fundability_verdict_without_mag_owner_receipt" in _refs(boundary["forbidden_authority_refs"])

    assert adoption["state"] == "advisory_current_contract"
    assert adoption["domain_id"] == "med-autogrant"
    assert adoption["stage_pack_required_sections"] == REQUIRED_STAGE_PACK_SECTIONS
    assert adoption["adoption_policy"]["advisory_not_launch_hard_gate"] is True
    assert adoption["authority_boundary"]["opl_can_claim_domain_ready"] is False
    assert adoption["authority_boundary"]["same_attempt_self_review_can_close_quality_gate"] is False

    assert golden["default_outer_loop"] == "current_owner_delta"
    assert golden["stage_attempt_strategy"] == "cognitive_kernel_stage_internal"
    assert "owner_receipt_ref_or_typed_blocker_ref" in golden["required_closeout_refs"]
    assert "tool_catalog_prescribes_executor_sequence" in golden["forbidden_claims"]


def test_mag_stage_control_plane_declares_tool_boundaries_and_independent_gates() -> None:
    plane = _read_json("contracts/stage_control_plane.json")
    adoption = _read_json("contracts/cognitive_kernel_adoption.json")
    adoption_boundary = adoption["tool_affordance_boundary"]

    assert stage_control_plane_module.plane_cognitive_kernel_refs is plane_cognitive_kernel_refs
    assert (
        stage_control_plane_module.stage_descriptor_cognitive_kernel_fields
        is stage_descriptor_cognitive_kernel_fields
    )
    assert plane["cognitive_kernel_adoption_ref"] == COGNITIVE_KERNEL_ADOPTION_REF
    assert plane["golden_path_profile_ref"] == GOLDEN_PATH_PROFILE_REF
    assert plane["stage_pack_required_sections"] == REQUIRED_STAGE_PACK_SECTIONS

    default_route_stage_ids = [
        stage["stage_id"]
        for stage in plane["stages"]
        if stage["selected_executor"]["default_executor"] is True
    ]
    assert default_route_stage_ids == ["call_and_candidate_intake"]

    for stage in plane["stages"]:
        stage_id = stage["stage_id"]
        assert stage["selected_executor"]["executor_kind"] == "codex_cli"
        assert stage["selected_executor"]["executor_binding_ref"] == "default_codex_cli"
        assert stage["selected_executor"]["default_executor"] is (
            stage_id == "call_and_candidate_intake"
        )
        assert stage["tool_refs"][0]["ref"] == "agent/tools/domain_affordances.md"
        assert stage["tool_refs"][0]["catalog_role"] == "available_affordance_catalog_not_workflow_script"

        boundary_ref = stage["tool_affordance_boundary_ref"]
        assert boundary_ref["stage_id"] == stage_id
        assert boundary_ref["ref"] == f"{COGNITIVE_KERNEL_ADOPTION_REF}#/tool_affordance_boundary"
        assert "grant_source_and_applicant_context_reading" in _refs(adoption_boundary["capability_refs"])
        assert adoption_boundary["executor_autonomy"]["executor_can_choose_tools"] is True
        assert adoption_boundary["executor_autonomy"]["tool_catalog_can_define_cognitive_strategy"] is False
        assert adoption_boundary["executor_autonomy"]["tool_catalog_can_authorize_forbidden_write"] is False

        assert stage["candidate_pool_policy"]["candidate_pool_is_stage_internal_artifact"] is True
        assert stage["candidate_pool_policy"]["accepted_artifact_mutation_requires_owner_receipt"] is True
        assert len(stage["strategy_refs"]) > 0
        assert stage["handoff_policy"]["owner_delta_first"] is True
        assert stage["handoff_policy"]["framework_transport_cannot_claim_domain_ready"] is True

        gate = stage["independent_gate_policy"]
        declared_gate_refs = {entry["ref"] for entry in stage["evaluation"]}
        assert gate["gate_ref"] in declared_gate_refs
        assert gate["gate_owner"] == "med-autogrant"
        assert gate["execution_review_separation_required"] is True
        assert gate["same_attempt_self_review_can_close_quality_gate"] is False
        assert gate["mechanical_completion_can_close_stage"] is False
        assert gate["provider_completion_can_claim_domain_ready"] is False
        assert gate["generated_surface_readiness_can_claim_quality_or_export"] is False
