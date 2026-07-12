from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = REPO_ROOT / "contracts" / "stage_run_kernel_profile.json"
CANARY_PATH = REPO_ROOT / "contracts" / "stage_run_canary_evidence.json"
LIVE_PROGRESS_PATH = REPO_ROOT / "contracts" / "live_stage_run_progress_evidence.json"


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_stage_run_profile_keeps_mag_thin_and_opl_hosted() -> None:
    profile = read_json(PROFILE_PATH)
    thinning = profile["domain_thinning_policy"]
    admission = profile["default_entry_admission_policy"]

    assert profile["kernel_role"] == "minimal_state_shell_not_domain_controller_system"
    route_policy = profile["codex_semantic_route_policy"]
    assert route_policy["semantic_owner"] == "codex_cli"
    assert route_policy["readable_artifact_allows_any_declared_stage"] is True
    assert route_policy["quality_budget_exhaustion_blocks_route"] is False
    assert route_policy["owner_receipt_required_for_quality_or_ready_claim"] is True
    assert route_policy["framework_can_accept_reject_rank_or_override_route"] is False
    assert profile["authority_boundary"]["opl_can_write_domain_truth"] is False
    assert profile["authority_boundary"]["opl_can_sign_domain_owner_receipt"] is False
    assert thinning["opl_hosted_runtime_owner"] == "one-person-lab"
    assert thinning["mag_long_term_role"] == "declarative_grant_pack_plus_refs_only_adapter_plus_minimal_authority_functions"
    assert {"legacy_scheduler_surface", "workbench_wrapper", "runtime_journal_cadence"} <= set(
        thinning["retired_or_thinned_mag_surfaces"]
    )
    assert {"mag_owned_durable_scheduler", "mag_owned_attempt_ledger"} <= set(thinning["forbidden_resurrection"])
    assert admission["required_runtime_owner"] == "one-person-lab"
    assert admission["required_executor_kind"] == "codex_cli"
    assert admission["required_caller_role_field"] == "caller_role"
    assert admission["required_caller_role"] == "opl_owner_chain_default_caller"
    assert admission["allowed_entry_surface_role"] == "stage_run_owner_chain_role_policy"
    assert admission["required_owner_chain_ref_marker"] == "owner-chain-default-caller"
    assert admission["required_stage_run_ref_fields"] == ["stage_run_ref", "temporal_stage_run_ref"]
    assert admission["accepted_stage_run_ref_sources"] == [
        "stage_run_ref",
        "temporal_stage_run_ref",
        "attempt_lease_ref",
        "lease_ref",
        "receipt_ref",
        "stage_attempt_receipt_ref",
    ]
    assert admission["accepted_owner_chain_default_caller_sources"] == [
        "caller_role",
        "attempt_lease_ref",
        "lease_ref",
        "receipt_ref",
        "stage_attempt_receipt_ref",
    ]
    assert admission["rejects_caller_roles"] == [
        "repo_local_runner",
        "private_wrapper",
        "default_caller_without_owner_chain",
        "named_legacy_guard",
    ]
    assert admission["mag_can_start_repo_local_runner"] is False
    assert admission["mag_can_use_private_wrapper_as_default"] is False
    assert admission["mag_can_name_legacy_guard_as_default"] is False


def test_stage_run_profile_consumes_exact_opl_contract_refs() -> None:
    profile = read_json(PROFILE_PATH)
    refs = profile["opl_contract_refs"]

    assert refs["owner"] == "one-person-lab"
    assert refs["domain_repo_role"] == "consumer_profile_ref_only"
    assert refs["repo_local_file_required"] is False
    assert refs["refs"] == [
        "contracts/opl-framework/stage-run-kernel-contract.json",
        "contracts/opl-framework/stage-manifest.schema.json",
        "contracts/opl-framework/role-artifact-ref.schema.json",
        "contracts/opl-framework/stage-owner-receipt.schema.json",
        "contracts/opl-framework/stage-typed-blocker.schema.json",
    ]


def test_controlled_canary_keeps_strategy_refs_body_free() -> None:
    profile = read_json(PROFILE_PATH)
    canary = read_json(CANARY_PATH)
    strategy = profile["stage_internal_strategy_policy"]

    assert profile["controlled_canary_evidence_ref"] == "contracts/stage_run_canary_evidence.json"
    assert strategy["strategies_are_stage_internal_execution_choices"] is True
    assert strategy["strategy_refs_are_advisory"] is True
    assert strategy["strategy_artifacts_are_refs_only_evidence"] is True
    assert strategy["strategy_artifacts_can_define_stage_transition"] is False
    assert strategy["hard_coded_workflow_allowed"] is False
    assert strategy["stage_internal_strategy_refs"] == [
        "candidate_generation",
        "reflection",
        "ranking",
        "revision",
        "meta_review",
    ]
    assert canary["surface_kind"] == "opl_stage_run_controlled_canary_evidence"
    assert canary["version"] == "stage-run-controlled-canary.v1"
    assert canary["domain_id"] == "med-autogrant"
    assert canary["canary_id"]
    assert canary["stage_id"] == "specific_aims_and_structure"
    assert canary["evidence_scope"] == "controlled_fixture_not_live_domain_progress"
    assert canary["stage_run_ref"] and canary["stage_manifest_ref"] and canary["current_pointer_ref"]
    assert set(canary["strategy_trace"]) == {
        "candidate_generation",
        "grounded_reflection",
        "comparative_selection",
        "evolution_and_revision",
        "meta_review_learning",
        "independent_quality_gate",
    }
    assert all(trace["refs"] for trace in canary["strategy_trace"].values())
    assert set(canary["role_artifact_refs"]) == {
        "candidate_pool_ref",
        "reflection_review_ref",
        "ranking_selection_ref",
        "revision_lineage_ref",
        "meta_review_ref",
        "independent_gate_ref",
    }
    assert all(canary["role_artifact_refs"].values())


def test_controlled_canary_operator_summary_stays_fixture_scoped() -> None:
    canary = read_json(CANARY_PATH)
    summary = canary["operator_summary"]

    assert summary["surface_kind"] == "stage_run_controlled_canary_operator_summary"
    assert summary["status"] == "fixture_closeout_ref_recorded"
    assert summary["read_root"] == "stage_run_current_owner_delta"
    assert summary["progress_delta_classification"] == "controlled_fixture_owner_receipt_ref"
    assert summary["stage_run_ref"] == canary["stage_run_ref"]
    assert summary["stage_manifest_ref"] == canary["stage_manifest_ref"]
    assert summary["current_owner_delta_ref"] == canary["current_pointer_ref"]
    assert summary["closeout_ref"] == canary["closeout"]["owner_receipt_ref"]
    assert summary["accepted_claims"] == [
        "controlled_fixture_shape_declared",
        "strategy_trace_refs_present",
        "role_artifact_refs_present",
        "owner_receipt_ref_present",
    ]
    assert summary["operator_action"] == "audit_fixture_boundary_only"


def test_controlled_canary_cannot_claim_authority_or_closeout() -> None:
    canary = read_json(CANARY_PATH)
    overclaim = canary["overclaim_boundary"]
    closeout = canary["closeout"]

    assert all(
        overclaim[field] is False
        for field in (
            "can_claim_live_domain_progress",
            "can_claim_stage_complete",
            "can_claim_grant_ready",
            "can_claim_fundability_ready",
            "can_claim_authoring_quality_ready",
            "can_claim_artifact_ready",
            "can_claim_package_fresh",
            "can_claim_submission_ready",
            "can_claim_production_ready",
            "can_authorize_external_submission",
        )
    )
    assert set(overclaim["forbidden_claims"]) == {
        "live_domain_progress",
        "stage_complete",
        "grant_ready",
        "fundability_ready",
        "authoring_quality_ready",
        "artifact_ready",
        "package_fresh",
        "submission_ready",
        "production_ready",
        "external_submission_authorized",
    }
    assert closeout["terminal_outcome"] in {"owner_receipt", "typed_blocker"}
    assert closeout["owner_receipt_ref"] or closeout["typed_blocker_ref"]
    assert closeout["same_attempt_self_review"] is False
    assert canary["tool_affordance_boundary"] == {
        "tool_refs_are_affordances": True,
        "tool_refs_define_workflow": False,
        "tool_refs_can_sign_receipt_or_quality_gate": False,
    }
    authority = canary["authority_boundary"]
    assert authority["refs_only"] is True
    for field in (
        "controlled_canary_claims_live_domain_progress",
        "provider_completion_counts_as_closeout",
        "file_presence_counts_as_closeout",
        "read_model_counts_as_closeout",
        "conformance_pass_counts_as_closeout",
        "opl_can_write_domain_truth",
        "opl_can_mutate_artifact_body",
        "opl_can_sign_owner_receipt",
        "opl_can_create_typed_blocker",
        "opl_can_authorize_quality_or_export",
    ):
        assert authority[field] is False


def test_live_progress_and_legacy_residue_remain_fail_closed() -> None:
    profile = read_json(PROFILE_PATH)
    live_progress = read_json(LIVE_PROGRESS_PATH)
    thinning = profile["domain_thinning_policy"]
    guard = profile["legacy_runtime_residue_guard"]

    assert live_progress["source_of_truth"] is True
    assert live_progress["state"] == "blocked_by_mag_owned_typed_blocker"
    assert live_progress["production_acceptance_tail_policy"]["production_acceptance_tail_counts_as_live_progress"] is False
    assert profile["live_stage_run_progress_evidence_ref"] == "contracts/live_stage_run_progress_evidence.json"
    assert profile["owner_chain_live_progress_provenance_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
        "owner_chain_live_progress_evidence_lane"
    )
    assert guard["default_runtime_owner"] == thinning["opl_hosted_runtime_owner"]
    assert guard["surface_id"] == "legacy_runtime_residue"
    assert guard["state"] == "active_guard"
    assert guard["residue_role"] == "history_or_tombstone_only"
    assert guard["allowed_remaining_roles"] == thinning["allowed_legacy_roles"]
    assert guard["forbidden_default_active_paths"] == thinning["forbidden_resurrection"]
    assert guard["closeout_gate"]["physical_delete_requires"] == thinning["physical_delete_gate"]
    assert guard["closeout_gate"]["canary_fixture_can_close_residue_retirement"] is False
    assert guard["closeout_gate"]["conformance_pass_can_close_residue_retirement"] is False
    assert all(value is False for value in guard["required_negative_guards"].values())
