from __future__ import annotations

SHARED_POLICY_RELEASE = {
    "policy_release_contract_ref": (
        "contracts/opl-framework/foundry-agent-series-policy-release.json"
    ),
    "policy_bundle_fingerprint": (
        "sha256:5d77102e99e6e49acd88714cd94dcafe0969b8f2a5529928d753002ac3d4619d"
    ),
    "fingerprint_algorithm": "sha256:stable-json",
    "domain_contract_policy_release_pin_required": True,
    "domain_adapter_must_not_copy_policy_body_as_authority": True,
    "consumer_alignment_check": "foundry:policy-release",
}

SERIES_DESIGN_PROFILE = {
    "surface_kind": "opl_foundry_agent_series_design_profile",
    "version": "foundry-agent-series-design-profile.v1",
    "profile_id": "opl_foundry_agent_series_design_profile.v1",
    "profile_summary": (
        "All Foundry Agents share the same OPL domain-pack to stage-led execution "
        "to gate/receipt to handoff lifecycle; domain inputs, outputs, aliases, "
        "and authority functions vary by agent."
    ),
    "shared_lifecycle_pipeline": [
        "domain_material_intake",
        "domain_pack_interpretation",
        "stage_led_agent_execution",
        "independent_quality_gate_or_owner_review",
        "owner_receipt_or_typed_blocker_closeout",
        "artifact_or_deliverable_handoff",
        "opl_refs_only_projection_and_recovery",
    ],
    "domain_io_profile": {
        "input_slot": "domain_materials_or_task_request",
        "output_slot": "domain_deliverable_or_owner_handoff",
        "input_is_domain_specific": True,
        "output_is_domain_specific": True,
        "shared_runtime_interpretation": (
            "OPL treats input/output as opaque domain refs and projects identity, "
            "stage, progress, closeout, evidence, and recovery metadata only."
        ),
    },
    "stage_pack_sections": [
        "prompts",
        "stages",
        "skills",
        "knowledge",
        "quality_gates",
    ],
    "shared_closeout_contract": {
        "success_shape": "domain_owner_receipt_ref",
        "blocked_shape": "domain_owned_typed_blocker_ref",
        "route_back_shape": "route_back_or_human_gate_ref",
        "provider_completion_is_closeout": False,
    },
    "authority_invariants": {
        "opl_can_infer_domain_output": False,
        "opl_can_read_domain_body": False,
        "opl_can_write_domain_truth": False,
        "opl_can_authorize_quality_or_export": False,
        "domain_owns_input_truth_and_output_authority": True,
    },
}

DOMAIN_SPECIFIC_PROFILE = {
    "profile_id": "mag_domain_specific_series_profile.v1",
    "series_members": ["MAS", "MAG", "RCA", "OMA"],
    "shared_opl_agent_lifecycle": [
        "domain_pack",
        "stage_led_execution",
        "independent_quality_gate",
        "owner_receipt_or_typed_blocker",
        "handoff",
    ],
    "mag_domain_input_profile": {
        "domain_pack_kind": "declarative_grant_pack",
        "primary_inputs": [
            "funding_call_refs",
            "applicant_profile_refs",
            "grant_strategy_memory_refs",
            "source_material_refs",
        ],
    },
    "mag_domain_output_profile": {
        "primary_outputs": [
            "grant_proposal_refs",
            "revision_package_refs",
            "submission_ready_package_refs",
            "owner_receipt_or_typed_blocker_refs",
        ],
        "domain_specific_gate": "independent_fundability_quality_export_and_submission_gate",
    },
    "series_variation_policy": (
        "MAG differs from MAS/RCA/OMA by grant and fund-material inputs plus grant proposal "
        "and package outputs, not by lifecycle ownership."
    ),
    "opl_scope": "refs_projection_runtime_only",
    "mag_authority_retained": [
        "grant_truth",
        "fundability_verdict",
        "authoring_quality_verdict",
        "export_verdict",
        "submission_verdict",
        "artifact_authority",
        "memory_accept_reject",
        "owner_receipt",
    ],
    "forbidden_series_drift": [
        "mag_specific_lifecycle_fork",
        "mag_specific_sqlite_or_state_index_kernel_owner",
        "opl_claims_grant_truth",
        "opl_claims_quality_or_submission_verdict",
        "generated_surface_signs_owner_receipt",
    ],
}

WORKSPACE_TOPOLOGY_PROFILE = {
    "surface_kind": "opl_workspace_topology_profile",
    "version": "workspace-topology-profile.v1",
    "profile_id": "opl.workspace_topology_profile.v1",
    "topology_model": [
        "workspace_group",
        "project_unit",
        "stage_artifact_unit",
        "owner_receipt_or_typed_blocker",
    ],
    "workspace_modes": ["one_off", "series", "portfolio"],
    "default_project_stage_outputs_root": "artifacts/stage_outputs",
    "default_profiles": {
        "one_off": {
            "workspace_mode": "one_off",
            "project_collection_path": "projects",
            "series_capable_skeleton": True,
            "shared_resource_roots": [
                "shared/sources",
                "shared/memory",
                "shared/style_system",
            ],
            "project_stage_outputs_root": "artifacts/stage_outputs",
        },
        "rca_series": {
            "workspace_mode": "series",
            "project_collection_path": "projects",
            "shared_resource_roots": [
                "shared/sources",
                "shared/brand",
                "shared/visual_memory",
                "shared/style_system",
                "shared/material_inventory",
            ],
            "project_stage_outputs_root": "artifacts/stage_outputs",
        },
        "mas_portfolio": {
            "workspace_mode": "portfolio",
            "project_collection_path": "projects",
            "shared_resource_roots": [
                "data",
                "literature",
                "memory",
                "shared/sources",
            ],
            "project_stage_outputs_root": "artifacts/stage_outputs",
        },
    },
    "domain_profile_defaults": {
        "mas": "mas_portfolio",
        "mag": "one_off",
        "rca": "rca_series",
        "oma": "one_off",
    },
    "default_user_inspection_surface": {
        "ordinary_user_default_surface": "workspace_local_project_stage_outputs",
        "project_stage_outputs_pattern": "<project-root>/artifacts/stage_outputs/<stage-id>/",
        "runtime_state_is_default_user_surface": False,
        "product_views_are_stage_outputs": False,
    },
    "runtime_state_boundary": {
        "role": "provider_backing_provenance_restore_audit",
        "runtime_state_can_be_canonical_project_root": False,
        "runtime_state_can_close_stage": False,
        "runtime_state_can_replace_owner_receipt_or_typed_blocker": False,
    },
    "authority_boundary": {
        "opl_can_define_topology_contract": True,
        "opl_can_project_workspace_refs": True,
        "opl_can_write_domain_truth": False,
        "opl_can_mutate_artifact_body": False,
        "opl_can_create_owner_receipt": False,
        "opl_can_create_typed_blocker": False,
        "runtime_state_counts_as_user_default_surface": False,
    },
    "workspace_initialization_policy": {
        "default_workspace_mode": "one_off",
        "infer_series_when_user_requests_multiple_related_deliverables": True,
        "infer_portfolio_when_user_requests_shared_research_workspace_with_multiple_studies": True,
        "upgrading_one_off_to_series_must_not_move_existing_project_roots": True,
        "explicit_workspace_mode_declaration_preferred": True,
        "default_project_collection_path": "projects",
        "legacy_project_collection_aliases": [
            "deliverables",
            "studies",
        ],
    },
    "example_project_layouts": {
        "one_off": {
            "project_collection_path": "projects",
            "project_root_pattern": "projects/<project-id>",
            "project_stage_outputs_pattern": (
                "projects/<project-id>/artifacts/stage_outputs/<stage-id>/"
            ),
            "legacy_project_collection_aliases": ["deliverables"],
        },
        "rca_series": {
            "shared_roots": [
                "shared/sources",
                "shared/brand",
                "shared/visual_memory",
                "shared/style_system",
                "shared/material_inventory",
            ],
            "project_collection_path": "projects",
            "project_root_pattern": "projects/<deck-id>",
            "project_stage_outputs_pattern": (
                "projects/<deck-id>/artifacts/stage_outputs/<stage-id>/"
            ),
            "legacy_project_collection_aliases": ["deliverables"],
        },
        "mas_portfolio": {
            "shared_roots": [
                "data",
                "literature",
                "memory",
            ],
            "project_collection_path": "projects",
            "project_root_pattern": "projects/<study-id>",
            "project_stage_outputs_pattern": (
                "projects/<study-id>/artifacts/stage_outputs/<stage-id>/"
            ),
            "legacy_project_collection_aliases": ["studies"],
        },
    },
}
