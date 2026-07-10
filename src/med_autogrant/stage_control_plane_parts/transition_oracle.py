from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


GRANT_TRANSITION_ORACLE_FIXTURES: tuple[dict[str, Any], ...] = (
    {
        "fixture_id": "call_intake_ready_to_fundability_strategy",
        "source_stage_id": "call_and_candidate_intake",
        "input_state": {
            "call_materials_status": "complete",
            "candidate_profile_status": "selected",
            "human_gate": "not_required",
        },
        "expected_transition_id": "call_intake_complete_to_fundability_strategy",
    },
    {
        "fixture_id": "fundability_strategy_ready_to_specific_aims",
        "source_stage_id": "fundability_strategy",
        "input_state": {
            "fundability_verdict": "proceed",
            "strategy_status": "accepted",
            "human_gate": "not_required",
        },
        "expected_transition_id": "fundability_strategy_accepted_to_specific_aims",
    },
    {
        "fixture_id": "fundability_requires_human_gate",
        "source_stage_id": "fundability_strategy",
        "input_state": {
            "fundability_verdict": "human_decision_required",
            "decision_gap": "funder_fit_owner_choice",
            "human_gate": "required",
        },
        "expected_transition_id": "fundability_human_decision_to_human_gate",
    },
    {
        "fixture_id": "specific_aims_ready_to_authoring",
        "source_stage_id": "specific_aims_and_structure",
        "input_state": {
            "specific_aims_status": "accepted",
            "argument_structure_status": "ready",
            "human_gate": "not_required",
        },
        "expected_transition_id": "specific_aims_accepted_to_proposal_authoring",
    },
    {
        "fixture_id": "proposal_draft_ready_to_review",
        "source_stage_id": "proposal_authoring",
        "input_state": {
            "draft_status": "complete",
            "authoring_quality_gate": "ready_for_review",
            "human_gate": "not_required",
        },
        "expected_transition_id": "proposal_draft_complete_to_review",
    },
    {
        "fixture_id": "review_blocked_to_repair",
        "source_stage_id": "review_and_rebuttal",
        "input_state": {
            "review_verdict": "blocked",
            "repair_target_status": "available",
            "human_gate": "not_required",
        },
        "expected_transition_id": "review_blocked_to_proposal_repair",
    },
    {
        "fixture_id": "quality_closed_to_package",
        "source_stage_id": "review_and_rebuttal",
        "input_state": {
            "review_verdict": "closed",
            "quality_dossier_status": "accepted",
            "human_gate": "not_required",
        },
        "expected_transition_id": "review_closed_to_package_and_submit_ready",
    },
    {
        "fixture_id": "package_ready_to_portal_human_gate",
        "source_stage_id": "package_and_submit_ready",
        "input_state": {
            "submission_ready_verdict": "ready",
            "portal_action_status": "human_action_required",
            "human_gate": "required",
        },
        "expected_transition_id": "package_ready_to_portal_human_gate",
    },
)


GRANT_TRANSITION_TABLE: tuple[dict[str, Any], ...] = (
    {
        "transition_id": "call_intake_complete_to_fundability_strategy",
        "from_stage_id": "call_and_candidate_intake",
        "to_stage_id": "fundability_strategy",
        "guard_id": "call_materials_and_profile_selected",
        "owner_action": "open_grant_user_loop",
        "return_shape": "owner_receipt_ref",
        "receipt_requirement": "intake_handoff_receipt",
        "blocked_shape": "typed_blocker_ref",
    },
    {
        "transition_id": "fundability_strategy_accepted_to_specific_aims",
        "from_stage_id": "fundability_strategy",
        "to_stage_id": "specific_aims_and_structure",
        "guard_id": "fundability_verdict_and_strategy_accepted",
        "owner_action": "open_grant_user_loop",
        "return_shape": "owner_receipt_ref",
        "receipt_requirement": "fundability_strategy_handoff_receipt",
        "blocked_shape": "typed_blocker_ref",
    },
    {
        "transition_id": "fundability_human_decision_to_human_gate",
        "from_stage_id": "fundability_strategy",
        "to_stage_id": "fundability_strategy",
        "guard_id": "fundability_human_decision_required",
        "owner_action": "open_grant_user_loop",
        "return_shape": "human_gate_ref",
        "receipt_requirement": "human_gate_receipt",
    },
    {
        "transition_id": "specific_aims_accepted_to_proposal_authoring",
        "from_stage_id": "specific_aims_and_structure",
        "to_stage_id": "proposal_authoring",
        "guard_id": "specific_aims_and_argument_structure_accepted",
        "owner_action": "open_grant_user_loop",
        "return_shape": "owner_receipt_ref",
        "receipt_requirement": "specific_aims_handoff_receipt",
        "blocked_shape": "typed_blocker_ref",
    },
    {
        "transition_id": "proposal_draft_complete_to_review",
        "from_stage_id": "proposal_authoring",
        "to_stage_id": "review_and_rebuttal",
        "guard_id": "proposal_draft_complete_and_reviewable",
        "owner_action": "open_grant_user_loop",
        "return_shape": "owner_receipt_ref",
        "receipt_requirement": "draft_review_handoff_receipt",
        "blocked_shape": "typed_blocker_ref",
    },
    {
        "transition_id": "review_blocked_to_proposal_repair",
        "from_stage_id": "review_and_rebuttal",
        "to_stage_id": "proposal_authoring",
        "guard_id": "review_blocked_with_repair_target",
        "owner_action": "open_grant_user_loop",
        "return_shape": "route_back_ref",
        "receipt_requirement": "repair_target_receipt",
        "blocked_shape": "typed_blocker_ref",
    },
    {
        "transition_id": "review_closed_to_package_and_submit_ready",
        "from_stage_id": "review_and_rebuttal",
        "to_stage_id": "package_and_submit_ready",
        "guard_id": "review_quality_closed",
        "owner_action": "build_submission_ready_package",
        "return_shape": "owner_receipt_ref",
        "receipt_requirement": "quality_closure_receipt",
        "blocked_shape": "typed_blocker_ref",
    },
    {
        "transition_id": "package_ready_to_portal_human_gate",
        "from_stage_id": "package_and_submit_ready",
        "to_stage_id": "package_and_submit_ready",
        "guard_id": "package_ready_and_external_portal_action_required",
        "owner_action": "open_grant_user_loop",
        "return_shape": "human_gate_ref",
        "receipt_requirement": "human_gate_receipt",
    },
)


def build_mag_grant_transition_oracle(
    *,
    family_stage_control_plane: Mapping[str, Any],
    family_action_catalog: Mapping[str, Any],
) -> dict[str, Any]:
    stage_ids = {
        str(stage["stage_id"])
        for stage in family_stage_control_plane["stages"]
        if isinstance(stage, Mapping)
    }
    action_ids = {
        str(action["action_id"])
        for action in family_action_catalog["actions"]
        if isinstance(action, Mapping)
    }
    transition_ids = {str(transition["transition_id"]) for transition in GRANT_TRANSITION_TABLE}

    missing_stage_refs = sorted(
        {
            stage_id
            for transition in GRANT_TRANSITION_TABLE
            for stage_id in (transition["from_stage_id"], transition["to_stage_id"])
            if stage_id not in stage_ids
        }
    )
    missing_action_refs = sorted(
        {
            str(transition["owner_action"])
            for transition in GRANT_TRANSITION_TABLE
            if transition["owner_action"] not in action_ids
        }
    )
    missing_fixture_refs = sorted(
        {
            str(fixture["expected_transition_id"])
            for fixture in GRANT_TRANSITION_ORACLE_FIXTURES
            if fixture["expected_transition_id"] not in transition_ids
        }
    )
    if missing_stage_refs or missing_action_refs or missing_fixture_refs:
        raise ValueError(
            "MAG transition oracle references unresolved stage/action/transition ids: "
            f"stages={missing_stage_refs}, actions={missing_action_refs}, fixtures={missing_fixture_refs}"
        )

    return {
        "surface_kind": "mag_grant_transition_oracle",
        "version": "mag-grant-transition-oracle.v1",
        "oracle_id": "mag.grant_transition.oracle.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "state": "domain_spec_landed_external_runner_gate",
        "runner_owner": "one-person-lab",
        "runner_contract_ref": "contracts/opl-framework/family-transition-runner-contract.json",
        "transition_table_status": "landed",
        "oracle_fixture_status": "landed",
        "stage_control_plane_ref": "/product_entry_manifest/family_stage_control_plane",
        "action_catalog_ref": "/product_entry_manifest/family_action_catalog",
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "authoring_quality_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
            "opl_role": "generic_transition_runner_only",
            "opl_can_infer_fundability_ready": False,
            "opl_can_infer_authoring_quality_ready": False,
            "opl_can_infer_submission_ready_export_ready": False,
            "opl_can_write_grant_truth": False,
        },
        "transition_table": [dict(transition) for transition in GRANT_TRANSITION_TABLE],
        "oracle_fixtures": [dict(fixture) for fixture in GRANT_TRANSITION_ORACLE_FIXTURES],
        "validation": {
            "status": "ready_for_opl_runner_ingestion",
            "transition_count": len(GRANT_TRANSITION_TABLE),
            "oracle_fixture_count": len(GRANT_TRANSITION_ORACLE_FIXTURES),
            "checked_stage_count": len(stage_ids),
            "checked_action_count": len(action_ids),
            "missing_stage_refs": missing_stage_refs,
            "missing_action_refs": missing_action_refs,
            "missing_fixture_transition_refs": missing_fixture_refs,
        },
        "notes": [
            "MAG declares grant transition semantics; OPL may only run the generic transition contract.",
            "Transition closeout uses OPL standard owner_receipt_ref, typed_blocker_ref, human_gate_ref, or route_back_ref fields.",
            "Human decisions return human_gate_ref; typed blockers are reserved for real semantic or authority gaps.",
            "Provider completion must not be treated as fundability, quality, or export readiness.",
        ],
    }
