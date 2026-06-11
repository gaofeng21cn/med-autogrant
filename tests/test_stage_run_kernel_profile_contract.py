from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_profile() -> dict[str, object]:
    return json.loads(
        (REPO_ROOT / "contracts" / "stage_run_kernel_profile.json").read_text(
            encoding="utf-8"
        )
    )


def _read_canary() -> dict[str, object]:
    return json.loads(
        (REPO_ROOT / "contracts" / "stage_run_canary_evidence.json").read_text(
            encoding="utf-8"
        )
    )


def _read_live_progress() -> dict[str, object]:
    return json.loads(
        (REPO_ROOT / "contracts" / "live_stage_run_progress_evidence.json").read_text(
            encoding="utf-8"
        )
    )


def test_stage_run_profile_keeps_mag_thin_and_opl_hosted() -> None:
    profile = _read_profile()

    assert profile["kernel_role"] == "minimal_state_shell_not_domain_controller_system"
    assert profile["transition_authority"]["terminal_transition_authority"] == (
        "owner_receipt_or_typed_blocker"
    )
    assert profile["authority_boundary"]["opl_can_write_domain_truth"] is False
    assert profile["authority_boundary"]["opl_can_sign_domain_owner_receipt"] is False

    thinning = profile["domain_thinning_policy"]
    assert thinning["opl_hosted_runtime_owner"] == "one-person-lab"
    assert thinning["mag_long_term_role"] == (
        "declarative_grant_pack_plus_refs_only_adapter_plus_minimal_authority_functions"
    )
    assert "legacy_scheduler_surface" in thinning["retired_or_thinned_mag_surfaces"]
    assert "workbench_wrapper" in thinning["retired_or_thinned_mag_surfaces"]
    assert "runtime_journal_cadence" in thinning["retired_or_thinned_mag_surfaces"]
    assert thinning["allowed_legacy_roles"] == [
        "migration_input",
        "diagnostic",
        "provenance",
        "refs_only_adapter",
        "tombstone",
    ]
    assert "mag_owned_durable_scheduler" in thinning["forbidden_resurrection"]
    assert "mag_owned_attempt_ledger" in thinning["forbidden_resurrection"]
    assert "no_active_caller" in thinning["physical_delete_gate"]


def test_stage_run_profile_consumes_opl_contract_refs_without_copying_framework_contracts() -> None:
    profile = _read_profile()
    refs = profile["opl_contract_refs"]

    assert refs["owner"] == "one-person-lab"
    assert refs["domain_repo_role"] == "consumer_profile_ref_only"
    assert refs["repo_local_file_required"] is False
    assert refs["local_resolution_policy"] == "do_not_copy_opl_framework_contracts_into_domain_repo"
    assert refs["refs"] == [
        "contracts/opl-framework/stage-run-kernel-contract.json",
        "contracts/opl-framework/stage-manifest.schema.json",
        "contracts/opl-framework/role-artifact-ref.schema.json",
        "contracts/opl-framework/stage-owner-receipt.schema.json",
        "contracts/opl-framework/stage-typed-blocker.schema.json",
    ]


def test_stage_run_profile_points_to_live_progress_owner_answer_contract() -> None:
    profile = _read_profile()
    live_progress = _read_live_progress()

    assert profile["live_stage_run_progress_evidence_ref"] == (
        "contracts/live_stage_run_progress_evidence.json"
    )
    assert profile["owner_chain_live_progress_provenance_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
        "owner_chain_live_progress_evidence_lane"
    )
    assert live_progress["source_of_truth"] is True
    assert live_progress["state"] == "blocked_by_mag_owned_typed_blocker"
    assert (
        live_progress["production_acceptance_tail_policy"][
            "production_acceptance_tail_counts_as_live_progress"
        ]
        is False
    )


def test_stage_run_strategy_canary_does_not_hardcode_workflow() -> None:
    profile = _read_profile()

    strategy = profile["stage_internal_strategy_policy"]
    assert profile["controlled_canary_evidence_ref"] == (
        "contracts/stage_run_canary_evidence.json"
    )
    assert strategy["strategy_refs_are_advisory"] is True
    assert strategy["strategies_are_stage_internal_execution_choices"] is True
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
    canary = strategy["canary"]
    assert canary["controlled_evidence_ref"] == "contracts/stage_run_canary_evidence.json"
    assert (
        canary["candidate_reflection_ranking_revision_meta_review_are_not_workflow_steps"]
        is True
    )
    assert canary["candidate_pool_is_stage_internal_artifact"] is True
    assert canary["reflection_is_stage_internal_evidence_ref"] is True
    assert canary["ranking_is_stage_internal_evidence_ref"] is True
    assert canary["revision_is_stage_internal_strategy_or_domain_stage_ref"] is True
    assert canary["meta_review_is_stage_internal_evidence_ref"] is True


def test_stage_run_controlled_canary_evidence_shape_is_body_free() -> None:
    canary = _read_canary()

    assert canary["surface_kind"] == "opl_stage_run_controlled_canary_evidence"
    assert canary["version"] == "stage-run-controlled-canary.v1"
    assert canary["domain_id"] == "med-autogrant"
    assert canary["canary_id"]
    assert canary["stage_id"] == "specific_aims_and_structure"
    assert canary["evidence_scope"] == "controlled_fixture_not_live_domain_progress"
    assert canary["stage_run_ref"]
    assert canary["stage_manifest_ref"]
    assert canary["current_pointer_ref"]

    strategy_trace = canary["strategy_trace"]
    assert set(strategy_trace) == {
        "candidate_generation",
        "grounded_reflection",
        "comparative_selection",
        "evolution_and_revision",
        "meta_review_learning",
        "independent_quality_gate",
    }
    for trace in strategy_trace.values():
        assert trace["refs"]
        assert all(isinstance(ref, str) and ref for ref in trace["refs"])

    assert set(canary["role_artifact_refs"]) == {
        "candidate_pool_ref",
        "reflection_review_ref",
        "ranking_selection_ref",
        "revision_lineage_ref",
        "meta_review_ref",
        "independent_gate_ref",
    }
    assert all(canary["role_artifact_refs"].values())


def test_stage_run_controlled_canary_operator_summary_stays_scoped() -> None:
    canary = _read_canary()

    summary = canary["operator_summary"]
    assert summary["surface_kind"] == "stage_run_controlled_canary_operator_summary"
    assert summary["status"] == "fixture_closeout_ref_recorded"
    assert summary["read_root"] == "stage_run_current_owner_delta"
    assert summary["progress_delta_classification"] == (
        "controlled_fixture_owner_receipt_ref"
    )
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


def test_stage_run_controlled_canary_overclaim_boundary_is_explicit() -> None:
    canary = _read_canary()

    overclaim = canary["overclaim_boundary"]
    assert overclaim["accepted_evidence_scope"] == canary["evidence_scope"]
    for field in [
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
    ]:
        assert overclaim[field] is False

    assert overclaim["forbidden_claims"] == [
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
    ]


def test_stage_run_controlled_canary_closeout_and_authority_are_fail_closed() -> None:
    canary = _read_canary()

    closeout = canary["closeout"]
    assert closeout["terminal_outcome"] in {"owner_receipt", "typed_blocker"}
    assert closeout["owner_receipt_ref"] or closeout["typed_blocker_ref"]
    assert closeout["same_attempt_self_review"] is False

    assert canary["tool_affordance_boundary"] == {
        "tool_refs_are_affordances": True,
        "tool_refs_define_workflow": False,
        "tool_refs_can_sign_receipt_or_quality_gate": False,
    }
    assert canary["authority_boundary"] == {
        "refs_only": True,
        "controlled_canary_claims_live_domain_progress": False,
        "provider_completion_counts_as_closeout": False,
        "file_presence_counts_as_closeout": False,
        "read_model_counts_as_closeout": False,
        "conformance_pass_counts_as_closeout": False,
        "opl_can_write_domain_truth": False,
        "opl_can_mutate_artifact_body": False,
        "opl_can_sign_owner_receipt": False,
        "opl_can_create_typed_blocker": False,
        "opl_can_authorize_quality_or_export": False,
    }


def test_stage_run_profile_guards_legacy_runtime_residue() -> None:
    profile = _read_profile()

    thinning = profile["domain_thinning_policy"]
    guard = profile["legacy_runtime_residue_guard"]
    assert guard["surface_id"] == "legacy_runtime_residue"
    assert guard["state"] == "active_guard"
    assert guard["default_runtime_owner"] == thinning["opl_hosted_runtime_owner"]
    assert guard["residue_role"] == "history_or_tombstone_only"
    assert guard["guard_scope"] == (
        "stage_run_profile_and_controlled_canary_follow_through"
    )
    assert guard["allowed_remaining_roles"] == thinning["allowed_legacy_roles"]
    assert guard["forbidden_default_active_paths"] == thinning["forbidden_resurrection"]
    assert guard["closeout_gate"]["physical_delete_requires"] == (
        thinning["physical_delete_gate"]
    )
    assert guard["closeout_gate"]["canary_fixture_can_close_residue_retirement"] is False
    assert (
        guard["closeout_gate"]["conformance_pass_can_close_residue_retirement"] is False
    )
    assert all(value is False for value in guard["required_negative_guards"].values())
    assert "legacy_runtime_residue" in guard["source_refs"][1]
