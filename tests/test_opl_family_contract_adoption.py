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
        "notification/receipt",
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

    assert attempt["opl_hosted_controlled_grant_stage_attempt_proof_surface"] == (
        "/product_entry_manifest/controlled_stage_attempt_projection/"
        "opl_hosted_controlled_grant_stage_attempt_proof"
    )
    assert attempt["controlled_memory_proof_refs"] == [
        "/product_entry_manifest/domain_memory_descriptor_locator/controlled_consumed_memory_proof",
        "/product_entry_manifest/domain_memory_descriptor_locator/writeback_receipt_proof",
    ]
    assert "opl_hosted_controlled_grant_stage_attempt_proof" in attempt["opl_consumption"]
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
