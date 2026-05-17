from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = "contracts/runtime-program/opl-family-contract-adoption.json"


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _contract() -> dict[str, object]:
    return json.loads(_read(CONTRACT_PATH))


def _domain_memory_seed_fixture() -> dict[str, object]:
    return json.loads(_read("contracts/runtime-program/domain-memory-seed-fixture.json"))


def test_mag_declares_thin_opl_family_contract_adoption() -> None:
    contract = _contract()

    assert contract["contract_kind"] == "mag_opl_family_contract_adoption.v1"
    assert contract["domain_id"] == "med-autogrant"
    assert contract["opl_role"] == "family-level projection consumer only"


def test_current_program_sidecar_actions_include_domain_memory_writeback_dispatch() -> None:
    current_program = json.loads(_read("contracts/runtime-program/current-program.json"))
    adapter = current_program["runtime_owner"]["stage_led_framework_boundary"]["product_sidecar_adapter"]

    assert adapter["allowed_dispatch_actions"] == [
        "autonomy-controller/dry-run",
        "autonomy-controller/guarded-run",
        "domain-memory/decide",
        "domain-memory/propose",
        "lifecycle/receipt",
        "notification/receipt",
        "stage-attempt/closeout",
        "status/read",
        "user-loop/wakeup",
    ]


def test_current_program_sidecar_actions_match_implemented_sidecar_export() -> None:
    from med_autogrant.product_entry import MedAutoGrantProductEntry

    current_program = json.loads(_read("contracts/runtime-program/current-program.json"))
    adapter = current_program["runtime_owner"]["stage_led_framework_boundary"]["product_sidecar_adapter"]
    export = MedAutoGrantProductEntry().build_sidecar_export(
        input_path=REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
    )

    assert adapter["allowed_dispatch_actions"] == export["sidecar_export"]["opl_control_plane"][
        "allowed_dispatch_actions"
    ]


def test_mag_runtime_projection_maps_to_grant_runtime_truth_surfaces() -> None:
    contract = _contract()
    attempt = contract["attempt_projection"]

    for surface in (
        "runtime_control",
        "runtime_continuity",
        "grant-autonomy-controller-report",
        "workspace progress",
    ):
        assert surface in attempt["source_surfaces"]
    assert attempt["maps_to_opl_contract"] == "opl_family_runtime_attempt_contract.v1"
    assert "MAG owns grant authoring runtime" in attempt["owner_boundary"]


def test_mag_quality_projection_keeps_grant_quality_owner_and_excludes_other_domain_gates() -> None:
    contract = _contract()
    quality = contract["quality_projection"]

    for surface in (
        "grant_quality_scorecard",
        "grant_quality_closure_dossier",
        "grant review",
        "fundability gate",
        "submission-ready export gate",
    ):
        assert surface in quality["source_surfaces"]
    assert quality["maps_to_opl_contract"] == "opl_family_domain_quality_projection_contract.v1"
    assert quality["claim_only_ready_forbidden"] is True


def test_mag_operator_and_incident_projection_require_source_refs_and_mag_closure() -> None:
    contract = _contract()
    incident = contract["incident_projection"]
    operator = contract["operator_projection"]

    assert incident["maps_to_opl_contract"] == "opl_family_incident_learning_loop.v1"
    assert "MAG-owned closure ref" in incident["closure_rule"]
    for field in ("source_refs", "freshness", "owner_split", "next_surface_ref", "human_gate_reason"):
        assert field in operator["required_fields"]
    for non_goal in (
        "OPL owns grant truth",
        "OPL bypasses submission-ready export gate",
        "OPL owns grant stage truth",
        "medical publication gate",
        "visual render/export proof gate",
    ):
        assert non_goal in contract["non_goals"]


def test_mag_stage_control_projection_is_descriptor_only_and_maps_existing_stage_surfaces() -> None:
    contract = _contract()
    stage_projection = contract["stage_control_projection"]

    assert stage_projection["surface_kind"] == "mag_opl_family_stage_control_projection.v1"
    assert stage_projection["projection_role"] == "descriptor_only_stage_pack"
    assert stage_projection["maps_to_opl_contract"] == "opl_family_stage_control_plane_stage_pack.v1"
    assert stage_projection["maps_existing_surfaces_only"] is True
    assert stage_projection["owner_boundary"] == {
        "domain_truth_owner": "med-autogrant",
        "fundability_judgment_owner": "med-autogrant",
        "submission_ready_export_gate_owner": "med-autogrant",
        "opl_role": "stage descriptor/projection consumer only",
    }

    pack = {entry["opl_stage"]: entry for entry in stage_projection["stage_pack"]}
    assert list(pack) == [
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
        "review_and_rebuttal",
        "package_and_submit_ready",
    ]
    expected_surfaces = {
        "call_and_candidate_intake": {
            "discover-funding-opportunities",
            "select-project-profile",
            "initialize-intake-workspace",
            "input_intake",
        },
        "fundability_strategy": {
            "direction_screening",
            "fit_alignment",
            "grant_quality_scorecard",
            "fundability gate",
        },
        "specific_aims_and_structure": {
            "question_refinement",
            "argument_building",
            "outline",
        },
        "proposal_authoring": {
            "drafting",
            "revision",
            "grant-progress",
            "grant-user-loop",
        },
        "review_and_rebuttal": {
            "critique",
            "review",
            "grant_quality_closure_dossier",
            "quality-diff",
        },
        "package_and_submit_ready": {
            "freeze",
            "frozen",
            "package submission-ready",
            "submission-ready export gate",
        },
    }
    for stage, surfaces in expected_surfaces.items():
        assert set(pack[stage]["mag_surfaces"]) == surfaces
        assert pack[stage]["truth_owner"] == "med-autogrant"
        assert pack[stage]["authority"]


def test_mag_adoption_contract_declares_lifecycle_adapter_mapping() -> None:
    contract = _contract()
    adapter = contract["lifecycle_adapter"]
    operator = contract["operator_projection"]

    assert adapter["surface_kind"] == "opl_family_lifecycle_adapter_contract"
    assert adapter["adapter_id"] == "mag.opl_family.lifecycle_adapter.v1"
    assert adapter["maps_existing_surfaces_only"] is True
    assert adapter["sqlite_migration_required"] is False
    assert adapter["persistence_projection"]["maps_existing_surfaces"] == [
        "session_continuity",
        "runtime_control.restore_point",
        "artifact_inventory",
        "runtime_continuity",
    ]
    assert adapter["persistence_projection"]["write_policy"] == "opl_index_only_no_domain_truth_writes"
    assert adapter["lifecycle_projection"]["maps_to_opl_contract"] == "opl_family_runtime_attempt_contract.v1"
    for field in ("attempt_state", "workspace_boundary", "owner_repo", "last_observed_projection"):
        assert field in adapter["lifecycle_projection"]["required_projection_fields"]
    assert adapter["owner_route_discovery"]["route_truth_owner"] == "med-autogrant"
    assert adapter["owner_route_discovery"]["discovery_surface_ref"] == (
        "/skill_catalog/skills/0/domain_projection/opl_stage_runtime_registration"
    )
    assert adapter["adoption_projection"]["maps_to_opl_contract"] == "opl_family_product_operator_projection.v1"
    assert adapter["adoption_projection"]["required_operator_fields"] == operator["required_fields"]


def test_mag_adoption_contract_declares_domain_memory_locator_without_opl_content_or_verdict_authority() -> None:
    contract = _contract()
    memory = contract["domain_memory_descriptor_locator"]

    assert memory["surface_kind"] == "domain_memory_descriptor_locator"
    assert memory["descriptor_id"] == "mag.domain_memory_descriptor_locator.v1"
    assert memory["manifest_surface_ref"] == "/product_entry_manifest/domain_memory_descriptor_locator"
    assert memory["policy_ref"] == "docs/references/grant_strategy_memory_policy.md"
    assert memory["maps_to_opl_contract"] == "opl_family_domain_memory_locator_contract.v1"
    assert memory["memory_owner"] == "med-autogrant"
    assert memory["memory_content_owner"] == "med-autogrant"
    assert memory["truth_owner"] == "med-autogrant"
    assert memory["fundability_verdict_owner"] == "med-autogrant"
    assert memory["locator_policy"] == "repo_tracked_descriptor_and_locator_refs_only"
    assert memory["stage_memory_refs"] == [
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
        "review_and_rebuttal",
        "package_and_submit_ready",
    ]
    assert set(memory["opl_consumption"]) == {
        "descriptor",
        "policy_ref",
        "stage_descriptor_refs",
        "memory_locator",
        "writeback_receipt_refs",
    }
    for forbidden in (
        "memory_content",
        "fundability_verdict",
        "authoring_quality_verdict",
        "submission_ready_export_verdict",
        "canonical_grant_artifact_content",
    ):
        assert forbidden in memory["opl_non_consumption"]
    assert memory["writeback_policy"] == (
        "opl_may_route_writeback_receipt_refs_but_mag_accepts_or_rejects_memory_content"
    )
    migration_plan = memory["migration_plan"]
    assert migration_plan["surface_kind"] == "domain_memory_migration_plan"
    assert migration_plan["plan_id"] == "mag.domain_memory_migration_plan.v1"
    assert migration_plan["manifest_surface_ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/migration_plan"
    )
    assert migration_plan["migration_state"] == "runtime_apply_contract_landed"
    assert migration_plan["seed_fixture_ref"] == "contracts/runtime-program/domain-memory-seed-fixture.json"
    assert migration_plan["migration_steps"] == [
        "discover_candidates",
        "mag_review",
        "persist_acceptance",
    ]
    assert "domain_memory_seed_fixture" in migration_plan["landed_surfaces"]
    assert "writeback_proposal_generator" in migration_plan["landed_surfaces"]
    assert migration_plan["runtime_apply_surfaces"] == [
        "writeback proposal generator",
        "MAG memory acceptance command",
        "runtime receipt evidence writer",
        "operator projection of accepted/rejected writeback receipts",
    ]
    assert migration_plan["pending_runtime_work"] == []
    assert migration_plan["target_store"]["owner"] == "med-autogrant"
    assert migration_plan["target_store"]["repo_tracked"] is False

    proposal_generator = memory["writeback_proposal_generator"]
    assert proposal_generator["surface_kind"] == "domain_memory_writeback_proposal_generator"
    assert proposal_generator["output_surface_kind"] == "mag_domain_memory_writeback_proposal"
    assert proposal_generator["write_policy"] == "runtime_store_only_no_repo_write"

    accept_reject = memory["accept_reject_command"]
    assert accept_reject["surface_kind"] == "domain_memory_accept_reject_command"
    assert accept_reject["decision_owner"] == "med-autogrant"
    assert accept_reject["requires_mag_decision_before_store_mutation"] is True

    receipt_writer = memory["runtime_receipt_evidence_writer"]
    assert receipt_writer["surface_kind"] == "domain_memory_runtime_receipt_evidence_writer"
    assert receipt_writer["output_surface_kind"] == "mag_domain_memory_runtime_receipt_evidence"
    assert receipt_writer["write_policy"] == "runtime_receipt_instance_only_no_repo_write"

    operator_projection = memory["operator_receipt_projection"]
    assert operator_projection["surface_kind"] == "mag_domain_memory_operator_receipt_projection"
    assert operator_projection["receipt_content_policy"] == "receipt_refs_and_decision_metadata_only_no_memory_body"

    receipt_locator = memory["receipt_locator"]
    assert receipt_locator["surface_kind"] == "domain_memory_receipt_locator"
    assert receipt_locator["locator_id"] == "mag.domain_memory_receipt_locator.v1"
    assert receipt_locator["manifest_surface_ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator"
    )
    assert receipt_locator["receipt_content_policy"] == "locator_and_decision_metadata_only_no_memory_body"
    assert receipt_locator["repo_tracked"] is False

    authority = memory["authority_boundary"]
    assert authority["opl_role"] == "memory_locator_ref_and_receipt_ref_consumer_only"
    assert authority["can_hold_memory_content"] is False
    assert authority["can_issue_fundability_verdict"] is False
    assert authority["can_issue_authoring_quality_verdict"] is False
    assert authority["can_issue_export_verdict"] is False
    assert authority["can_mutate_domain_memory_store"] is False


def test_mag_adoption_contract_declares_standard_family_domain_memory_ref_adapter() -> None:
    contract = _contract()
    descriptor = contract["domain_memory_descriptor"]
    locator = contract["domain_memory_descriptor_locator"]

    assert descriptor["surface_kind"] == "family_domain_memory_ref"
    assert descriptor["version"] == "family-domain-memory-ref.v1"
    assert descriptor["memory_ref_id"] == "mag_grant_strategy_memory"
    assert descriptor["target_domain_id"] == "med-autogrant"
    assert descriptor["owner"] == "Med Auto Grant"
    assert descriptor["memory_family"] == "grant_strategy_memory"
    assert descriptor["manifest_surface_ref"] == "/product_entry_manifest/domain_memory_descriptor"
    assert descriptor["memory_pack_ref"]["ref"] == "docs/references/grant_strategy_memory_policy.md"
    assert descriptor["memory_pack_ref"]["runtime_locator_ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/memory_locator"
    )
    assert descriptor["stage_applicability"] == locator["stage_memory_refs"]
    assert descriptor["retrieval_contract_ref"]["ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/memory_locator"
    )
    assert descriptor["writeback_contract_ref"]["ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/writeback_proposal_generator"
    )
    assert descriptor["writeback_contract_ref"]["accept_reject_ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/accept_reject_command"
    )
    assert descriptor["receipt_contract_ref"]["ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/operator_receipt_projection"
    )
    assert descriptor["recall_projection_ref"]["ref"] == (
        "/product_entry_manifest/domain_memory_descriptor_locator/stage_descriptor_refs"
    )
    assert descriptor["migration_plan_ref"]["ref"] == locator["migration_plan"]["manifest_surface_ref"]
    assert descriptor["seed_corpus_ref"]["ref"] == locator["migration_plan"]["seed_fixture_ref"]
    assert descriptor["writeback_receipt_locator_ref"]["ref"] == locator["receipt_locator"]["manifest_surface_ref"]
    assert descriptor["freshness"]["refresh_policy"] == "rebuild_product_entry_manifest_before_opl_discovery"
    assert descriptor["migration_readiness"]["status"] == "migration_plan_ready_descriptor_only"
    assert descriptor["migration_readiness"]["memory_body_migration"] == "domain_owned_runtime_apply_required"
    assert descriptor["migration_readiness"]["opl_apply_allowed"] is False

    authority = descriptor["authority_boundary"]
    assert authority["opl_role"] == "locator_projection_owner"
    assert authority["domain_memory_owner"] == "med-autogrant"
    assert "memory_store_owner" in authority["forbidden_opl_authority"]
    assert "fundability_verdict_owner" in authority["forbidden_opl_authority"]
    assert "submission_ready_export_verdict_owner" in authority["forbidden_opl_authority"]
    assert "memory_accept_reject_owner" in authority["forbidden_opl_authority"]
    assert authority["can_write_domain_truth"] is False
    assert authority["can_authorize_quality_verdict"] is False
    assert authority["can_authorize_fundability_verdict"] is False
    assert authority["can_authorize_submission_readiness"] is False
    assert authority["can_write_artifacts"] is False
    assert authority["can_accept_or_reject_memory_writeback"] is False


def test_mag_adoption_contract_declares_opl_substrate_adapter_as_index_only_export() -> None:
    contract = _contract()
    adapter = contract["opl_substrate_adapter_export"]

    assert adapter["surface_kind"] == "mag_opl_substrate_adapter_export"
    assert adapter["adapter_id"] == "mag.opl_substrate_adapter.export.v1"
    assert adapter["manifest_surface_ref"] == "/product_entry_manifest/opl_substrate_adapter_export"
    assert adapter["sidecar_surface_ref"] == "/sidecar_export/opl_substrate_adapter_export"
    assert adapter["export_policy"] == "opaque_index_only_refs_no_domain_truth_payloads"
    assert adapter["workspace_ref_index"].endswith("/workspace_ref_index")
    assert adapter["source_ref_index"].endswith("/source_ref_index")
    assert adapter["artifact_ref_index"].endswith("/artifact_ref_index")
    assert adapter["memory_ref_index"].endswith("/memory_ref_index")
    assert adapter["lifecycle_ref_index"].endswith("/lifecycle_ref_index")
    assert adapter["projection_ref_index"].endswith("/projection_ref_index")
    assert adapter["body_exposure_policy"] == {
        "workspace": "opaque_ref_and_locator_ref_only",
        "source": "json_pointer_refs_only",
        "artifact": "locator_index_only_no_package_body",
        "memory": "locator_receipt_refs_only_no_memory_body",
        "owner_receipt": "receipt_ref_only_no_authority_transfer",
    }
    authority = adapter["authority_boundary"]
    assert authority["domain_truth_owner"] == "med-autogrant"
    assert authority["package_body_owner"] == "med-autogrant"
    assert authority["memory_body_owner"] == "med-autogrant"
    assert authority["owner_receipt_authority_owner"] == "med-autogrant"
    assert authority["opl_role"] == "opaque_index_and_locator_ref_consumer_only"
    assert authority["opl_can_write_grant_truth"] is False
    assert authority["opl_can_read_package_body"] is False
    assert authority["opl_can_read_memory_body"] is False
    assert authority["opl_can_issue_owner_receipt"] is False


def test_domain_memory_seed_fixture_is_template_only_and_points_to_landed_surfaces() -> None:
    fixture = _domain_memory_seed_fixture()
    contract = _contract()
    memory = contract["domain_memory_descriptor_locator"]

    assert fixture["fixture_kind"] == "mag_domain_memory_seed_fixture.v1"
    assert fixture["state"] == "seed_fixture_no_real_memory_entries"
    assert fixture["policy_ref"] == memory["policy_ref"]
    assert fixture["descriptor_surface_ref"] == memory["manifest_surface_ref"]
    assert fixture["migration_plan_ref"] == memory["migration_plan"]["manifest_surface_ref"]
    assert fixture["receipt_locator_ref"] == memory["receipt_locator"]["manifest_surface_ref"]
    assert fixture["stage_ids"] == memory["stage_memory_refs"]
    assert fixture["repo_source_policy"]["repo_contains_real_memory_entries"] is False
    assert fixture["repo_source_policy"]["repo_contains_real_grant_artifacts"] is False
    assert fixture["repo_source_policy"]["repo_contains_receipt_instances"] is False

    forbidden_scan = fixture["candidate_template"]["forbidden_content_scan"]
    assert forbidden_scan == {
        "contains_workspace_private_evidence": False,
        "contains_canonical_grant_artifact_content": False,
        "contains_fundability_verdict": False,
        "contains_authoring_quality_verdict": False,
        "contains_submission_ready_export_verdict": False,
    }
    receipt_template = fixture["acceptance_receipt_template"]
    assert receipt_template["contains_memory_body"] is False
    assert receipt_template["contains_grant_artifact_content"] is False
    assert receipt_template["contains_quality_or_export_verdict"] is False

    consumed_template = fixture["controlled_consumed_memory_template"]
    assert consumed_template["surface_kind"] == "domain_memory_controlled_consumed_memory_proof"
    assert consumed_template["stage_attempt_ref"] == "/product_entry_manifest/controlled_stage_attempt_projection"
    assert consumed_template["contains_memory_body"] is False
    assert consumed_template["repo_tracked"] is False

    receipt_proof_template = fixture["writeback_receipt_proof_template"]
    assert receipt_proof_template["surface_kind"] == "domain_memory_writeback_receipt_proof"
    assert receipt_proof_template["proposal_surface_kind"] == "mag_domain_memory_writeback_proposal"
    assert receipt_proof_template["decision_surface_kind"] == "mag_domain_memory_writeback_decision"
    assert receipt_proof_template["mag_accept_reject_required"] is True
    assert receipt_proof_template["contains_memory_body"] is False
    assert receipt_proof_template["repo_tracked"] is False


def test_mag_adoption_contract_declares_controlled_memory_and_opl_hosted_attempt_proofs() -> None:
    contract = _contract()
    attempt = contract["controlled_stage_attempt_projection"]
    memory = contract["domain_memory_descriptor_locator"]
    apply_proof = contract["controlled_domain_memory_apply_proof"]

    assert attempt["opl_hosted_controlled_grant_stage_attempt_proof_surface"] == (
        "/product_entry_manifest/controlled_stage_attempt_projection/"
        "opl_hosted_controlled_grant_stage_attempt_proof"
    )
    assert attempt["controlled_memory_proof_refs"] == [
        "/product_entry_manifest/domain_memory_descriptor_locator/controlled_consumed_memory_proof",
        "/product_entry_manifest/domain_memory_descriptor_locator/writeback_receipt_proof",
    ]
    assert "opl_hosted_controlled_grant_stage_attempt_proof" in attempt["opl_consumption"]
    assert "owner_receipt_runtime_evidence_ref" in attempt["opl_consumption"]
    assert "controlled_consumed_memory_ref" in attempt["opl_consumption"]
    assert "writeback_receipt_ref" in attempt["opl_consumption"]
    assert "fundability_verdict" in attempt["opl_non_consumption"]
    assert "submission_ready_export_verdict" in attempt["opl_non_consumption"]

    consumed = memory["controlled_consumed_memory_proof"]
    assert consumed["surface_kind"] == "domain_memory_controlled_consumed_memory_proof"
    assert consumed["maps_to_opl_contract"] == "opl_family_consumed_memory_proof.v1"
    assert consumed["projection_policy"] == "locator_and_stage_context_only_no_memory_body"
    assert consumed["repo_tracked_real_memory_body"] is False
    assert consumed["opl_role"] == "consumed_memory_ref_consumer_only"

    receipt = memory["writeback_receipt_proof"]
    assert receipt["surface_kind"] == "domain_memory_writeback_receipt_proof"
    assert receipt["maps_to_opl_contract"] == "opl_family_memory_writeback_receipt_proof.v1"
    assert receipt["receipt_content_policy"] == "decision_metadata_and_refs_only_no_memory_body"
    assert receipt["receipt_instance_repo_tracked"] is False
    assert receipt["mag_accept_reject_required"] is True
    assert receipt["opl_role"] == "writeback_receipt_ref_router_only"

    assert apply_proof["surface_kind"] == "controlled_grant_stage_domain_memory_apply_proof"
    assert apply_proof["manifest_surface_ref"] == "/product_entry_manifest/controlled_domain_memory_apply_proof"
    assert apply_proof["proof_state"] == "repo_source_audit_landed_no_runtime_artifact_write"
    assert apply_proof["maps_to_opl_contract"] == "opl_controlled_domain_memory_apply_proof.v1"
    assert apply_proof["consumed_refs_surface"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "consumed_grant_strategy_memory_refs"
    )
    assert apply_proof["writeback_proposal_surface"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "writeback_proposal_projection"
    )
    assert apply_proof["accept_reject_decision_surface"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "accept_reject_decision_projection"
    )
    assert apply_proof["runtime_receipt_evidence_surface"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "runtime_receipt_evidence_projection"
    )
    assert apply_proof["controlled_receipt_instances_state"] == "runtime_receipt_evidence_path_verified"
    assert apply_proof["runtime_receipt_instance_writable"] is True
    assert apply_proof["operator_receipt_projection_surface"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "operator_receipt_projection"
    )
    assert apply_proof["controlled_receipt_instances_surface"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "controlled_receipt_instances"
    )
    assert apply_proof["repo_source_layout_audit_surface"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "repo_source_layout_audit"
    )
    assert apply_proof["repo_payload_policy"] == {
        "repo_tracked_real_memory_body": False,
        "repo_tracked_real_receipt_instance": False,
        "repo_tracked_real_grant_artifact": False,
        "repo_contains_contracts_locators_and_seed_fixture_only": True,
    }
    assert apply_proof["authority_boundary"]["can_write_fundability_verdict"] is False
    assert apply_proof["authority_boundary"]["can_write_authoring_quality_verdict"] is False
    assert apply_proof["authority_boundary"]["can_write_submission_ready_export_verdict"] is False
    assert apply_proof["authority_boundary"]["can_write_grant_artifact"] is False


def test_mag_adoption_contract_declares_repo_source_layout_audit_for_memory_skeleton() -> None:
    contract = _contract()
    audit = contract["repo_source_layout_audit"]

    assert audit["surface_kind"] == "mag_repo_source_layout_audit"
    assert audit["manifest_surface_ref"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/"
        "repo_source_layout_audit"
    )
    assert audit["layout_state"] == "physical_skeleton_follow_through_landed_minimum_anchors"
    assert audit["boundary_keys"] == ["agent", "contracts", "runtime", "docs"]
    assert audit["physical_move_required"] == (
        "low_risk_source_moves_only_after_direct_hosted_parity_restore_provenance_and_no_active_caller_proof"
    )
    assert audit["retired_active_path_policy"] == "physically_removed_or_history_tombstone_only"
    assert audit["forbidden_active_path_residue"] == []
    assert {entry["path_family"]: entry["state"] for entry in audit["legacy_active_path_residue"]} == {
        "default Hermes active path": "tombstone_only",
        "default Gateway active path": "physically_removed_from_active_source",
        "default local-manager active path": "physically_removed_from_active_source",
        "repo-local host-agent runtime as product owner": "physically_removed_from_active_source",
    }
    for boundary in audit["boundary_keys"]:
        assert (REPO_ROOT / boundary).is_dir()
        assert boundary in audit["source_refs_by_boundary"]
        assert audit["source_refs_by_boundary"][boundary]
    for anchor_ref in (
        "agent/README.md",
        "contracts/README.md",
        "runtime/README.md",
        "src/med_autogrant/product_entry_parts/functional_closure.py",
    ):
        assert any(
            anchor_ref in refs
            for refs in audit["source_refs_by_boundary"].values()
        )
        assert (REPO_ROOT / anchor_ref).exists()


def test_mag_adoption_contract_declares_owner_receipt_lifecycle_and_skeleton_follow_through() -> None:
    contract = _contract()
    skeleton = contract["standard_domain_agent_skeleton"]
    owner_receipt = contract["owner_receipt_contract"]
    lifecycle = contract["lifecycle_guarded_apply_proof"]
    follow_through = contract["physical_skeleton_follow_through"]

    assert skeleton["mapping_state"] == "minimum_physical_skeleton_follow_through_landed"
    assert skeleton["controlled_domain_memory_apply_proof_ref"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof"
    )
    assert skeleton["owner_receipt_contract_ref"] == "/product_entry_manifest/owner_receipt_contract"
    assert skeleton["lifecycle_guarded_apply_proof_ref"] == "/product_entry_manifest/lifecycle_guarded_apply_proof"
    assert skeleton["physical_skeleton_follow_through_ref"] == (
        "/product_entry_manifest/physical_skeleton_follow_through"
    )
    assert skeleton["repo_source_layout_audit_ref"] == (
        "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit"
    )

    assert owner_receipt["surface_kind"] == "mag_owner_receipt_contract"
    assert owner_receipt["manifest_surface_ref"] == "/product_entry_manifest/owner_receipt_contract"
    assert owner_receipt["contract_id"] == "mag.owner_receipt.contract.v1"
    assert owner_receipt["maps_to_opl_contract"] == "opl_domain_owner_receipt_envelope.v1"
    assert owner_receipt["allowed_return_shapes"] == [
        "domain_owner_receipt",
        "typed_blocker",
        "no_regression_evidence",
    ]
    assert owner_receipt["opl_role"] == "owner_receipt_ref_consumer_only"
    assert owner_receipt["runtime_receipt_evidence_command"] == "product owner-receipt-evidence"
    assert owner_receipt["runtime_receipt_evidence_surface_kind"] == "mag_owner_receipt_evidence"
    assert owner_receipt["runtime_receipt_instance_writable"] is True
    assert owner_receipt["receipt_instance_repo_tracked"] is False
    assert "fundability_verdict_owner" in owner_receipt["forbidden_opl_authority"]
    assert "grant_artifact_writer" in owner_receipt["forbidden_opl_authority"]
    assert "memory_body_writer" in owner_receipt["forbidden_opl_authority"]

    assert lifecycle["surface_kind"] == "mag_lifecycle_guarded_apply_proof"
    assert lifecycle["manifest_surface_ref"] == "/product_entry_manifest/lifecycle_guarded_apply_proof"
    assert lifecycle["owner_receipt_contract_ref"] == "/product_entry_manifest/owner_receipt_contract"
    assert lifecycle["operations"] == ["cleanup", "restore", "retention"]
    assert lifecycle["opl_apply_scope"] == "opl_owned_ledger_and_locator_only"
    assert lifecycle["domain_mutation_policy"] == "requires_mag_owner_receipt"
    assert lifecycle["typed_blocker_kind"] == "mag_domain_artifact_owner_receipt_required"
    assert lifecycle["runtime_receipt_evidence_command"] == "product lifecycle-receipt-evidence"
    assert lifecycle["runtime_receipt_evidence_surface_kind"] == "mag_lifecycle_receipt_evidence"
    assert lifecycle["runtime_receipt_instance_writable"] is True
    assert lifecycle["receipt_instance_repo_tracked"] is False

    assert follow_through["surface_kind"] == "mag_physical_skeleton_follow_through"
    assert follow_through["manifest_surface_ref"] == "/product_entry_manifest/physical_skeleton_follow_through"
    assert follow_through["state"] == "minimum_repo_source_anchors_landed"
    assert follow_through["repo_source_boundary"] == ["agent", "contracts", "runtime", "docs"]
    assert follow_through["anchor_refs"] == [
        "agent/README.md",
        "contracts/README.md",
        "runtime/README.md",
        "docs/status.md",
    ]
    assert follow_through["moves_workspace_artifacts"] is False
    assert follow_through["moves_runtime_receipt_instances"] is False
    assert follow_through["moves_memory_body"] is False


def test_mag_adoption_contract_consumes_opl_scheduler_replacement_without_generic_owner() -> None:
    contract = _contract()
    thinning = contract["mag_consumer_thinning_contract"]

    assert thinning["surface_kind"] == "mag_consumer_thinning_contract"
    assert thinning["manifest_surface_ref"] == "/product_entry_manifest/mag_consumer_thinning_contract"
    assert thinning["consumes_opl_family_primitive"] == "family_scheduler_replacement"
    assert thinning["adapter_role"] == "domain_authority_pack_with_thin_program_surface"
    assert thinning["mag_owned_outputs"] == [
        "grant_owned_refs",
        "owner_receipt",
        "typed_blocker",
        "verdict_refs",
        "domain_action_metadata",
    ]
    assert thinning["forbidden_mag_generic_owner_roles"] == [
        "generic_scheduler_owner",
        "generic_daemon_owner",
        "generic_lifecycle_owner",
        "generic_queue_owner",
        "generic_attempt_ledger_owner",
        "generic_state_machine_runner_owner",
        "generic_workspace_source_intake_owner",
        "generic_memory_transport_owner",
        "generic_artifact_gallery_owner",
        "generic_operator_workbench_owner",
        "generic_observability_slo_owner",
    ]
    assert thinning["thin_surface_output_guard_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard"
    )
    assert thinning["standard_agent_scaffold_alignment_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/standard_agent_scaffold_alignment"
    )
    assert thinning["opl_family_conflict_blocker_projection_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/opl_family_conflict_blocker_projection"
    )
    assert thinning["opl_runtime_observability_consumption_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/opl_runtime_observability_consumption"
    )
    assert thinning["privatized_functional_module_audit_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/privatized_functional_module_audit"
    )
    assert thinning["consumed_opl_projection_surfaces"] == [
        "family_conflict_envelope",
        "stage_attempt_usage_projection",
        "stage_attempt_control_loop_projection",
        "runtime_observability_export",
        "family_product_operator_projection",
    ]
    audit = thinning["privatized_functional_module_audit"]
    assert audit["state"] == "manifest_projected_for_opl_unified_audit"
    assert audit["classification_buckets"] == [
        "declarative_pack_surface",
        "refs_only_adapter",
        "minimal_authority_function",
        "legacy_proof_tombstone",
    ]
    assert len(audit["declarative_pack_surfaces"]) == 3
    assert len(audit["refs_only_adapter_surfaces"]) == 5
    assert len(audit["mag_owned_grant_authority_surfaces"]) == 6
    assert len(audit["retire_or_tombstone_surfaces"]) == 6
    assert audit["domain_authority_do_not_retire"] == [
        "grant_lifecycle_stage",
        "package_readiness_submission_ready",
        "fundability_verdict",
        "authoring_quality_verdict",
        "submission_ready_export_verdict",
        "grant_transition_oracle",
        "owner_receipt",
        "grant_strategy_memory_accept_reject",
    ]
    assert "workspace_source_intake_shell" in audit["opl_must_absorb_code_surfaces"]
    assert "generic_scheduler_daemon" in audit["opl_must_absorb_code_surfaces"]
    assert audit["mag_thin_adapter_code_surfaces"] == [
        "product_entry_manifest_builder",
        "product_sidecar_adapter",
        "domain_entry",
        "receipt_schema_and_writer",
        "grant_transition_oracle",
        "refs_only_projection_builders",
        "focused_contract_tests",
    ]
    assert audit["representative_private_functional_surfaces"] == {
        "local_runtime_journal_attempt_ledger": {
            "module_ref": "local_runtime_journal_attempt_ledger",
            "active_caller_status": "legacy_local_journal_attempt_ledger_no_active_caller",
            "migration_action": "OPL_owns_session_attempt_ledger_MAG_keeps_safe_action_refs",
        },
        "sidecar_dispatch_product_shell": {
            "module_ref": "sidecar_product_status_shell",
            "active_caller_status": "active_refs_only_domain_sidecar_adapter",
            "migration_action": "OPL_generates_product_operator_shell_MAG_keeps_guarded_domain_adapter_refs",
        },
        "optional_hermes_state_db": {
            "module_ref": "default_hermes_gateway_local_manager_runtime_owner",
            "active_caller_status": "legacy_proof_tombstone_no_active_default_caller",
            "migration_action": "OPL_owns_generic_executor_adapter_MAG_keeps_legacy_proof_refs_only",
        },
    }
    assert thinning["sidecar_output_policy"] == "grant_refs_and_receipts_only_no_generic_runtime_state"
    assert thinning["private_functional_state_output_classes_forbidden"] == [
        "local_runtime_journal_state",
        "local_attempt_ledger_state",
        "attention_queue_state",
        "stage_attempt_ledger_state",
        "package_lifecycle_state",
        "source_intake_state",
        "operator_workbench_state",
        "scheduler_daemon_state",
        "hermes_state_db_runtime_state",
    ]
    assert thinning["knowledge_only_repository"] is False
    assert thinning["retains_domain_program_surfaces"] is True
    assert thinning["authority_boundary"] == {
        "grant_truth_owner": "med-autogrant",
        "grant_memory_body_owner": "med-autogrant",
        "quality_verdict_owner": "med-autogrant",
        "export_authority_owner": "med-autogrant",
        "owner_receipt_authority": "med-autogrant",
        "safe_action_refs_owner": "med-autogrant",
        "opl_family_scheduler_replacement_owner": "one-person-lab",
        "mag_implements_generic_scheduler": False,
        "mag_implements_generic_daemon": False,
        "mag_implements_generic_lifecycle_owner": False,
        "mag_implements_generic_queue": False,
        "mag_implements_generic_attempt_ledger": False,
        "mag_implements_generic_runner": False,
        "mag_implements_app_workbench": False,
        "mag_implements_generic_workspace_source_intake": False,
        "mag_implements_generic_memory_transport": False,
        "mag_implements_generic_artifact_gallery": False,
        "mag_implements_generic_operator_workbench": False,
        "mag_implements_generic_observability_slo": False,
        "mag_can_emit_private_functional_state": False,
        "mag_can_emit_local_attempt_ledger_state": False,
        "mag_can_emit_source_intake_state": False,
        "mag_can_emit_package_lifecycle_state": False,
        "mag_can_emit_hermes_state_db_runtime_state": False,
        "provider_completion_is_grant_ready": False,
        "mag_executes_opl_repair": False,
    }
    assert thinning["claims_opl_replacement_exists"] is False
    assert thinning["claims_production_long_run_soak_complete"] is False
    assert thinning["mag_rebuilds_opl_runtime"] is False


def test_mag_controlled_soak_deferred_without_descriptor_index_skeleton_regression() -> None:
    contract = _contract()
    skeleton = contract["standard_domain_agent_skeleton"]
    controlled_soak = skeleton["controlled_soak"]

    assert controlled_soak["state"] == "deferred"
    assert controlled_soak["required_opl_substrate"] == "Temporal production online runtime"
    assert controlled_soak["no_regression_surfaces"] == [
        "family_action_catalog",
        "family_stage_control_plane",
        "standard_domain_agent_skeleton",
        "artifact_locator_contract",
        "controlled_stage_attempt_projection",
        "controlled_domain_memory_apply_proof",
        "owner_receipt_contract",
        "lifecycle_guarded_apply_proof",
        "physical_skeleton_follow_through",
        "domain_memory_descriptor_locator",
        "repo_source_layout_audit",
    ]
    assert "provider_hosted_controlled_grant_stage_soak_completed" in controlled_soak["forbidden_deferred_claims"]
    assert "accepted_or_rejected_receipt_instance_repo_tracked" in controlled_soak["forbidden_deferred_claims"]
    assert "OPL_holds_fundability_or_submission_ready_export_verdict" in controlled_soak["forbidden_deferred_claims"]
