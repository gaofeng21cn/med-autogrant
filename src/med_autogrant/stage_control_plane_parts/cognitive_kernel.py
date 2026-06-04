from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


COGNITIVE_KERNEL_STAGE_PACK_REQUIRED_SECTIONS = [
    "prompt_refs",
    "skill_refs",
    "tool_refs",
    "tool_affordance_boundary",
    "knowledge_refs",
    "quality_gate_refs",
    "strategy_refs",
    "candidate_pool_policy",
    "independent_gate_policy",
    "handoff_policy",
]

DOMAIN_TOOL_AFFORDANCE_REF = {
    "ref": "agent/tools/domain_affordances.md",
    "ref_kind": "repo_path",
    "role": "stage_tool_affordance_catalog",
    "catalog_role": "available_affordance_catalog_not_workflow_script",
}

DOMAIN_PACK_TOOL_AFFORDANCE_REF = {
    "ref": "agent/tools/domain_affordances.md",
    "ref_kind": "repo_path",
    "role": "domain_tool_affordance_catalog",
    "catalog_role": "available_affordance_catalog_not_workflow_script",
}

MAG_COGNITIVE_KERNEL_STRATEGY_REFS = [
    "call_fit_candidate_generation",
    "grant_review_grounded_reflection",
    "specific_aims_comparative_selection",
    "proposal_revision_lineage",
    "submission_package_independent_gate",
]

COGNITIVE_KERNEL_ADOPTION_REF = "contracts/cognitive_kernel_adoption.json"
GOLDEN_PATH_PROFILE_REF = "contracts/golden_path_profile.json"


def _policy_ref(ref: str, role: str) -> dict[str, str]:
    return {"ref": ref, "ref_kind": "policy_ref", "role": role}


MAG_TOOL_AFFORDANCE_BOUNDARY = {
    "catalog_role": "available_affordance_catalog_not_workflow_script",
    "capability_refs": [
        _policy_ref("grant_source_and_applicant_context_reading", "capability_boundary"),
        _policy_ref("grant_authoring_and_revision_workspace_operation", "capability_boundary"),
        _policy_ref("fundability_quality_and_export_review_support", "capability_boundary"),
        _policy_ref("refs_only_receipt_and_stage_artifact_materialization", "capability_boundary"),
    ],
    "permission_scope_refs": [
        _policy_ref("repo_context_read", "permission_scope_boundary"),
        _policy_ref("declared_domain_workspace_read", "permission_scope_boundary"),
        _policy_ref("bounded_domain_artifact_write_when_owner_authorized", "permission_scope_boundary"),
        _policy_ref("receipt_or_typed_blocker_return", "permission_scope_boundary"),
    ],
    "credential_boundary_refs": [
        _policy_ref("no_secret_material_in_stage_pack", "credential_boundary_boundary"),
        _policy_ref("executor_must_request_human_gate_for_missing_credentials", "credential_boundary_boundary"),
    ],
    "write_scope_refs": [
        _policy_ref("grant_workspace_refs_only", "write_scope_boundary"),
        _policy_ref(
            "submission_package_artifact_refs_only_until_package_authority_receipt",
            "write_scope_boundary",
        ),
    ],
    "side_effect_risk_refs": [
        _policy_ref(
            "external_network_or_portal_side_effect_requires_explicit_stage_permission",
            "side_effect_risk_boundary",
        ),
        _policy_ref("artifact_or_package_mutation_requires_domain_owner_receipt", "side_effect_risk_boundary"),
    ],
    "forbidden_authority_refs": [
        _policy_ref("fundability_verdict_without_mag_owner_receipt", "forbidden_authority_boundary"),
        _policy_ref("quality_verdict_without_mag_owner_receipt", "forbidden_authority_boundary"),
        _policy_ref("export_verdict_without_mag_owner_receipt", "forbidden_authority_boundary"),
        _policy_ref("grant_truth_write_by_opl", "forbidden_authority_boundary"),
        _policy_ref("memory_body_write_by_opl", "forbidden_authority_boundary"),
    ],
    "executor_autonomy": {
        "executor_can_choose_tools": True,
        "executor_can_skip_tools": True,
        "executor_can_substitute_tools_within_boundary": True,
        "executor_can_choose_order_and_parallelism": True,
        "executor_can_request_missing_context_or_human_gate": True,
        "tool_catalog_can_prescribe_tool_sequence": False,
        "tool_catalog_can_define_cognitive_strategy": False,
        "tool_catalog_can_override_stage_goal": False,
        "tool_catalog_can_authorize_forbidden_write": False,
    },
    "policy": (
        "med-autogrant tool refs declare available affordances and safety boundaries only; "
        "they do not prescribe executor order, stage strategy, stage goal, or forbidden writes."
    ),
}


def stage_descriptor_cognitive_kernel_fields(
    *,
    stage_id: str,
    gate_ref: str,
) -> dict[str, Any]:
    return {
        "tool_refs": [DOMAIN_TOOL_AFFORDANCE_REF],
        "tool_affordance_boundary_ref": {
            "ref": f"{COGNITIVE_KERNEL_ADOPTION_REF}#/tool_affordance_boundary",
            "ref_kind": "json_pointer",
            "stage_id": stage_id,
            "role": "stage_tool_affordance_boundary",
        },
        "strategy_refs": [
            {"ref": strategy_ref, "ref_kind": "strategy_ref", "role": "cognitive_kernel_strategy"}
            for strategy_ref in MAG_COGNITIVE_KERNEL_STRATEGY_REFS
        ],
        "candidate_pool_policy": {
            "candidate_pool_is_stage_internal_artifact": True,
            "candidate_lineage_required": True,
            "accepted_artifact_mutation_requires_owner_receipt": True,
            "candidate_body_stays_in_domain_workspace": True,
        },
        "independent_gate_policy": {
            "gate_owner": TARGET_DOMAIN_ID,
            "gate_ref": gate_ref,
            "execution_review_separation_required": True,
            "same_attempt_self_review_can_close_quality_gate": False,
            "mechanical_completion_can_close_stage": False,
            "provider_completion_can_claim_domain_ready": False,
            "generated_surface_readiness_can_claim_quality_or_export": False,
            "allowed_closeout_refs": [
                "owner_receipt_ref",
                "typed_blocker_ref",
                "human_gate_ref",
                "route_back_ref",
                "no_regression_evidence_ref",
            ],
        },
        "handoff_policy": {
            "owner_delta_first": True,
            "required_return_shapes": [
                "deliverable_delta_ref",
                "owner_receipt_ref",
                "typed_blocker_ref",
                "human_gate_ref",
                "quality_gate_receipt_ref",
                "no_regression_evidence_ref",
            ],
            "framework_transport_cannot_claim_domain_ready": True,
        },
    }


def plane_cognitive_kernel_refs() -> dict[str, Any]:
    return {
        "cognitive_kernel_adoption_ref": COGNITIVE_KERNEL_ADOPTION_REF,
        "golden_path_profile_ref": GOLDEN_PATH_PROFILE_REF,
        "stage_pack_required_sections": COGNITIVE_KERNEL_STAGE_PACK_REQUIRED_SECTIONS,
    }


def pack_compiler_cognitive_kernel_fields() -> dict[str, Any]:
    return {
        **plane_cognitive_kernel_refs(),
        "tool_refs": [DOMAIN_PACK_TOOL_AFFORDANCE_REF],
        "tool_affordance_boundary": MAG_TOOL_AFFORDANCE_BOUNDARY,
        "cognitive_kernel_policy": {
            "advisory_not_launch_hard_gate": True,
            "strategy_refs_completeness_is_launch_hard_gate": False,
            "independent_gate_receipt_required_for_quality_progression": True,
            "same_attempt_self_review_can_close_quality_gate": False,
            "route_can_execute_without_stage_attempt": False,
        },
    }
