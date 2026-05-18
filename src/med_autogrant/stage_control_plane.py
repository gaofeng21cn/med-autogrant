from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


STAGE_PACK: tuple[dict[str, Any], ...] = (
    {
        "stage_id": "call_and_candidate_intake",
        "stage_kind": "intake",
        "title": "Call and candidate intake",
        "goal": "Read call guidance, applicant/team context, candidate directions, and eligibility constraints.",
        "domain_stage_refs": [
            "discover-funding-opportunities",
            "select-project-profile",
            "initialize-intake-workspace",
            "input_intake",
        ],
        "allowed_action_refs": ["inspect_progress", "inspect_cockpit"],
        "requires": ["grant_request_received"],
        "ensures": ["call_candidate_intake_ready"],
        "next_stage_refs": ["fundability_strategy"],
        "trust_lane": "domain_agent",
    },
    {
        "stage_id": "fundability_strategy",
        "stage_kind": "planning",
        "title": "Fundability strategy",
        "goal": "Evaluate topic competitiveness, innovation, risk, fit, and funder-specific strategy.",
        "domain_stage_refs": [
            "direction_screening",
            "fit_alignment",
            "grant_quality_scorecard",
            "fundability gate",
        ],
        "allowed_action_refs": ["open_grant_user_loop", "inspect_progress"],
        "requires": ["call_candidate_intake_ready"],
        "ensures": ["fundability_strategy_gate_recorded"],
        "next_stage_refs": ["specific_aims_and_structure"],
        "trust_lane": "ai_decision",
        "independent_gate_receipt_required": True,
    },
    {
        "stage_id": "specific_aims_and_structure",
        "stage_kind": "planning",
        "title": "Specific aims and structure",
        "goal": "Shape research question, aims, technical route, innovation, and argument structure.",
        "domain_stage_refs": ["question_refinement", "argument_building", "outline"],
        "allowed_action_refs": ["open_grant_user_loop", "inspect_progress"],
        "requires": ["fundability_strategy_gate_recorded"],
        "ensures": ["specific_aims_structure_accepted"],
        "next_stage_refs": ["proposal_authoring"],
        "trust_lane": "ai_decision",
        "independent_gate_receipt_required": True,
    },
    {
        "stage_id": "proposal_authoring",
        "stage_kind": "creation",
        "title": "Proposal authoring",
        "goal": "Draft and revise the proposal body within the locked funding-call context.",
        "domain_stage_refs": ["drafting", "revision", "grant-progress", "grant-user-loop"],
        "allowed_action_refs": ["open_grant_user_loop", "build_direct_entry"],
        "requires": ["specific_aims_structure_accepted"],
        "ensures": ["proposal_draft_reviewable"],
        "next_stage_refs": ["review_and_rebuttal"],
        "trust_lane": "codex_executor",
    },
    {
        "stage_id": "review_and_rebuttal",
        "stage_kind": "review",
        "title": "Review and rebuttal",
        "goal": "Run reviewer-style critique, issue closure, rebuttal planning, and quality-diff checks.",
        "domain_stage_refs": ["critique", "review", "grant_quality_closure_dossier", "quality-diff"],
        "allowed_action_refs": ["open_grant_user_loop", "inspect_progress"],
        "requires": ["proposal_draft_reviewable"],
        "ensures": ["grant_review_gate_receipt_recorded"],
        "next_stage_refs": ["package_and_submit_ready"],
        "trust_lane": "ai_decision",
        "independent_gate_receipt_required": True,
    },
    {
        "stage_id": "package_and_submit_ready",
        "stage_kind": "packaging",
        "title": "Package and submit-ready",
        "goal": "Freeze final local delivery package and run submission-ready export checks.",
        "domain_stage_refs": ["freeze", "frozen", "package submission-ready", "submission-ready export gate"],
        "allowed_action_refs": ["build_submission_ready_package", "inspect_progress"],
        "requires": ["grant_review_gate_receipt_recorded"],
        "ensures": ["submission_ready_package_receipt_recorded"],
        "next_stage_refs": [],
        "trust_lane": "domain_agent",
        "independent_gate_receipt_required": True,
    },
)

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
        "fixture_id": "fundability_blocked_requests_human_gate",
        "source_stage_id": "fundability_strategy",
        "input_state": {
            "fundability_verdict": "blocked",
            "blocking_gap": "funder_fit_unclear",
            "human_gate": "required",
        },
        "expected_transition_id": "fundability_blocked_to_human_gate",
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
        "fixture_id": "package_missing_portal_material_to_human_gate",
        "source_stage_id": "package_and_submit_ready",
        "input_state": {
            "submission_ready_verdict": "blocked",
            "missing_material_kind": "external_portal_field",
            "human_gate": "required",
        },
        "expected_transition_id": "package_blocked_to_human_gate",
    },
)

GRANT_TRANSITION_TABLE: tuple[dict[str, Any], ...] = (
    {
        "transition_id": "call_intake_complete_to_fundability_strategy",
        "from_stage_id": "call_and_candidate_intake",
        "to_stage_id": "fundability_strategy",
        "guard_id": "call_materials_and_profile_selected",
        "owner_action": "open_grant_user_loop",
        "return_shape": "domain_owner_receipt",
        "receipt_requirement": "intake_handoff_receipt",
        "blocked_shape": "typed_blocker",
    },
    {
        "transition_id": "fundability_blocked_to_human_gate",
        "from_stage_id": "fundability_strategy",
        "to_stage_id": "fundability_strategy",
        "guard_id": "fundability_blocker_requires_human_gate",
        "owner_action": "open_grant_user_loop",
        "return_shape": "typed_blocker",
        "receipt_requirement": "human_gate_receipt",
        "blocked_shape": "typed_blocker",
    },
    {
        "transition_id": "specific_aims_accepted_to_proposal_authoring",
        "from_stage_id": "specific_aims_and_structure",
        "to_stage_id": "proposal_authoring",
        "guard_id": "specific_aims_and_argument_structure_accepted",
        "owner_action": "open_grant_user_loop",
        "return_shape": "domain_owner_receipt",
        "receipt_requirement": "specific_aims_handoff_receipt",
        "blocked_shape": "typed_blocker",
    },
    {
        "transition_id": "proposal_draft_complete_to_review",
        "from_stage_id": "proposal_authoring",
        "to_stage_id": "review_and_rebuttal",
        "guard_id": "proposal_draft_complete_and_reviewable",
        "owner_action": "open_grant_user_loop",
        "return_shape": "domain_owner_receipt",
        "receipt_requirement": "draft_review_handoff_receipt",
        "blocked_shape": "typed_blocker",
    },
    {
        "transition_id": "review_blocked_to_proposal_repair",
        "from_stage_id": "review_and_rebuttal",
        "to_stage_id": "proposal_authoring",
        "guard_id": "review_blocked_with_repair_target",
        "owner_action": "open_grant_user_loop",
        "return_shape": "typed_blocker",
        "receipt_requirement": "repair_target_receipt",
        "blocked_shape": "typed_blocker",
    },
    {
        "transition_id": "review_closed_to_package_and_submit_ready",
        "from_stage_id": "review_and_rebuttal",
        "to_stage_id": "package_and_submit_ready",
        "guard_id": "review_quality_closed",
        "owner_action": "build_submission_ready_package",
        "return_shape": "domain_owner_receipt",
        "receipt_requirement": "quality_closure_receipt",
        "blocked_shape": "typed_blocker",
    },
    {
        "transition_id": "package_blocked_to_human_gate",
        "from_stage_id": "package_and_submit_ready",
        "to_stage_id": "package_and_submit_ready",
        "guard_id": "package_missing_external_portal_material",
        "owner_action": "open_grant_user_loop",
        "return_shape": "typed_blocker",
        "receipt_requirement": "human_gate_receipt",
        "blocked_shape": "typed_blocker",
    },
)


def _stage_descriptor(stage: dict[str, Any]) -> dict[str, Any]:
    runtime_event_refs = _runtime_event_refs(stage)
    return {
        **stage,
        "owner": TARGET_DOMAIN_ID,
        "stage_goal": stage["goal"],
        "summary": f"{stage['title']} projected from MAG-owned grant authoring surfaces for OPL discovery.",
        "inputs": [
            {"ref_kind": "json_pointer", "ref": "/family_action_catalog", "role": "allowed_action_catalog"},
            {"ref_kind": "json_pointer", "ref": "/progress_projection", "role": "grant_progress_read_model"},
            {"ref_kind": "json_pointer", "ref": "/runtime_control", "role": "runtime_control_projection"},
        ],
        "skills": [
            {"ref_kind": "skill_id", "ref": "med-autogrant", "role": "domain_skill"},
            {"ref_kind": "skill_id", "ref": "officecli-docx", "role": "optional_document_helper"},
        ],
        "prompt_refs": [
            {
                "ref_kind": "repo_path",
                "ref": f"agent/prompts/{stage['stage_id']}.md",
                "role": "stage_prompt",
            }
        ],
        "outputs": [
            {"ref_kind": "json_pointer", "ref": "/progress_projection", "role": "stage_status"},
            {"ref_kind": "json_pointer", "ref": "/artifact_inventory", "role": "artifact_inventory"},
        ],
        "evaluation": [
            {"ref_kind": "json_pointer", "ref": "/grant_authoring_readiness", "role": "authoring_readiness"},
            {"ref_kind": "json_pointer", "ref": "/runtime_control", "role": "runtime_control"},
            {"ref_kind": "json_pointer", "ref": "/owner_receipt_contract", "role": "owner_receipt_gate"},
        ],
        "handoff": {
            "next_owner": TARGET_DOMAIN_ID,
            "next_stage_refs": list(stage.get("next_stage_refs", [])),
            "provides": list(stage.get("ensures", [])),
            "resume_surface_ref": "/operator_loop_surface",
            "progress_surface_ref": "/progress_projection",
            "shared_handoff_ref": "/shared_handoff",
        },
        "stage_contract": {
            "requires": list(stage.get("requires", [])),
            "ensures": list(stage.get("ensures", [])),
            "runtime_event_refs": runtime_event_refs,
            "boundary_assumptions": [
                "MAG owns grant truth, fundability judgment, authoring quality, package authority, and submission-ready export gate.",
                "OPL admission only checks descriptor composition; it cannot authorize fundability-ready, quality-ready, or export-ready states.",
            ],
        },
        "trust_boundary": {
            "lane": stage.get("trust_lane", "domain_agent"),
            "static_check_eligible": False,
            "effect_boundary": stage.get("trust_lane") == "ai_decision",
            "records_runtime_events": True,
            "runtime_event_refs": runtime_event_refs,
            "owner_receipt_required": True,
            "human_gate_required": False,
            "runtime_guard_required": True,
        },
        "source_refs": [
            {"ref_kind": "json_pointer", "ref": "/family_action_catalog", "role": "action_authority"},
            {"ref_kind": "json_pointer", "ref": "/progress_projection", "role": "stage_progress"},
            {"ref_kind": "json_pointer", "ref": "/task_lifecycle", "role": "checkpoint_status"},
            {"ref_kind": "json_pointer", "ref": "/runtime_control", "role": "runtime_boundary"},
            {"ref_kind": "json_pointer", "ref": "/grant_authoring_readiness", "role": "authoring_gate"},
        ],
        "freshness": {
            "freshness_kind": "product_entry_manifest_projection",
            "source_observed_at_ref": "/product_entry_manifest/task_lifecycle/checkpoint_summary",
            "refresh_policy": "rebuild_product_entry_manifest_before_opl_discovery",
            "stale_if_source_refs_missing": True,
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_judgment_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_gate_owner": TARGET_DOMAIN_ID,
            "opl_role": "projection_consumer_only",
            "maps_existing_surfaces_only": True,
            "independent_gate_receipt_required": bool(stage.get("independent_gate_receipt_required", False)),
            "can_write_grant_truth": False,
            "can_override_fundability_judgment": False,
            "can_bypass_submission_ready_gate": False,
        },
    }


def _runtime_event_refs(stage: Mapping[str, Any]) -> list[str]:
    stage_id = str(stage["stage_id"])
    if stage.get("trust_lane") == "ai_decision":
        return [f"runtime_event:{stage_id}.ai_decision_gate_recorded"]
    return [f"runtime_event:{stage_id}.owner_receipt_recorded"]


def build_mag_family_stage_control_plane(
    *,
    family_action_catalog: Mapping[str, Any],
) -> dict[str, Any]:
    action_ids = {
        str(action["action_id"])
        for action in family_action_catalog["actions"]
        if isinstance(action, Mapping)
    }
    stages = [_stage_descriptor(stage) for stage in STAGE_PACK]
    missing_refs = sorted(
        {
            action_ref
            for stage in stages
            for action_ref in stage["allowed_action_refs"]
            if action_ref not in action_ids
        }
    )
    if missing_refs:
        raise ValueError(f"MAG stage control plane allowed_action_refs missing from family_action_catalog: {missing_refs}")

    return {
        "surface_kind": "family_stage_control_plane",
        "version": "family-stage-control-plane.v1",
        "plane_id": "med_autogrant_stage_control_plane",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "discovery_smoke": {
            "surface_kind": "family_stage_control_plane_discovery_smoke",
            "status": "ready",
            "consumer": "opl_family_manifest_discovery_smoke",
            "required_stage_fields": [
                "stage_id",
                "stage_goal",
                "owner",
                "skills",
                "allowed_action_refs",
                "handoff",
                "source_refs",
                "freshness",
                "authority_boundary",
                "stage_contract",
                "trust_boundary",
            ],
            "allowed_action_catalog_ref": "/product_entry_manifest/family_action_catalog",
        },
        "source_refs": [
            {"ref_kind": "json_pointer", "ref": "/product_entry_manifest/family_action_catalog", "role": "action_catalog"},
            {"ref_kind": "json_pointer", "ref": "/product_entry_manifest/progress_projection", "role": "progress_read_model"},
            {"ref_kind": "json_pointer", "ref": "/product_entry_manifest/task_lifecycle", "role": "checkpoint_read_model"},
            {"ref_kind": "json_pointer", "ref": "/product_entry_manifest/runtime_control", "role": "authority_boundary"},
            {"ref_kind": "json_pointer", "ref": "/product_entry_manifest/shared_handoff", "role": "handoff_contract"},
        ],
        "freshness": {
            "freshness_kind": "product_entry_manifest_projection",
            "source_observed_at_ref": "/product_entry_manifest/task_lifecycle/checkpoint_summary",
            "refresh_policy": "rebuild_product_entry_manifest_before_opl_discovery",
            "stale_if_source_refs_missing": True,
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_judgment_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_gate_owner": TARGET_DOMAIN_ID,
            "opl_role": "projection_consumer_only",
            "write_policy": "no_grant_truth_writes",
            "can_write_grant_truth": False,
            "can_override_fundability_judgment": False,
            "can_bypass_submission_ready_gate": False,
        },
        "parity": {
            "status": "aligned",
            "allowed_action_catalog_ref": "/product_entry_manifest/family_action_catalog",
            "checked_action_count": len(action_ids),
        },
        "stages": stages,
        "notes": [
            "Descriptor-only projection over existing MAG grant authoring surfaces.",
            "OPL discovery must not own grant truth, fundability judgment, or submission-ready export authority.",
        ],
    }


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
            "Transition output is a domain owner receipt, typed blocker, or no-regression evidence ref.",
            "Provider completion must not be treated as fundability, quality, or export readiness.",
        ],
    }
