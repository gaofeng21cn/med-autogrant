from __future__ import annotations

from typing import Any

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
    },
    {
        "stage_id": "specific_aims_and_structure",
        "stage_kind": "planning",
        "title": "Specific aims and structure",
        "goal": "Shape research question, aims, technical route, innovation, and argument structure.",
        "domain_stage_refs": ["question_refinement", "argument_building", "outline"],
        "allowed_action_refs": ["open_grant_user_loop", "inspect_progress"],
    },
    {
        "stage_id": "proposal_authoring",
        "stage_kind": "creation",
        "title": "Proposal authoring",
        "goal": "Draft and revise the proposal body within the locked funding-call context.",
        "domain_stage_refs": ["drafting", "revision", "grant-progress", "grant-user-loop"],
        "allowed_action_refs": ["open_grant_user_loop", "build_direct_entry"],
    },
    {
        "stage_id": "review_and_rebuttal",
        "stage_kind": "review",
        "title": "Review and rebuttal",
        "goal": "Run reviewer-style critique, issue closure, rebuttal planning, and quality-diff checks.",
        "domain_stage_refs": ["critique", "review", "grant_quality_closure_dossier", "quality-diff"],
        "allowed_action_refs": ["open_grant_user_loop", "inspect_progress"],
    },
    {
        "stage_id": "package_and_submit_ready",
        "stage_kind": "packaging",
        "title": "Package and submit-ready",
        "goal": "Freeze final local delivery package and run submission-ready export checks.",
        "domain_stage_refs": ["freeze", "frozen", "package submission-ready", "submission-ready export gate"],
        "allowed_action_refs": ["build_submission_ready_package", "inspect_progress"],
    },
)


def _stage_descriptor(stage: dict[str, Any]) -> dict[str, Any]:
    return {
        **stage,
        "owner": TARGET_DOMAIN_ID,
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
            {"ref_kind": "repo_path", "ref": "docs/references/opl_family_contract_adoption.md", "role": "stage_pack_reference"}
        ],
        "outputs": [
            {"ref_kind": "json_pointer", "ref": "/progress_projection", "role": "stage_status"},
            {"ref_kind": "json_pointer", "ref": "/artifact_inventory", "role": "artifact_inventory"},
        ],
        "evaluation": [
            {"ref_kind": "json_pointer", "ref": "/grant_authoring_readiness", "role": "authoring_readiness"},
            {"ref_kind": "json_pointer", "ref": "/runtime_control", "role": "runtime_control"},
        ],
        "handoff": {
            "next_owner": TARGET_DOMAIN_ID,
            "resume_surface_ref": "/operator_loop_surface",
            "progress_surface_ref": "/progress_projection",
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_judgment_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_gate_owner": TARGET_DOMAIN_ID,
            "opl_role": "projection_consumer_only",
            "maps_existing_surfaces_only": True,
        },
    }


def build_mag_family_stage_control_plane() -> dict[str, Any]:
    return {
        "surface_kind": "family_stage_control_plane",
        "version": "family-stage-control-plane.v1",
        "plane_id": "med_autogrant_stage_control_plane",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_judgment_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_gate_owner": TARGET_DOMAIN_ID,
            "opl_role": "projection_consumer_only",
            "write_policy": "no_grant_truth_writes",
        },
        "stages": [_stage_descriptor(stage) for stage in STAGE_PACK],
        "notes": [
            "Descriptor-only projection over existing MAG grant authoring surfaces.",
            "OPL discovery must not own grant truth, fundability judgment, or submission-ready export authority.",
        ],
    }
