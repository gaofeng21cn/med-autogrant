from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FOUNDRY_SERIES_PATH = REPO_ROOT / "contracts" / "foundry_agent_series.json"

LEGACY_POLICY_BODY_FIELDS = {
    "agent_membership_projection_policy",
    "app_projection_policy",
    "contract_version_policy",
    "domain_adapter_policy",
    "required_identity_fields",
    "required_stage_packets",
    "series_design_profile",
    "shared_progress_projection_fields",
    "standard_feedback_self_evolution_trigger_policy",
    "standard_public_projection_policy",
    "workspace_topology_profile",
}


def _series() -> dict[str, object]:
    return json.loads(FOUNDRY_SERIES_PATH.read_text(encoding="utf-8"))


def test_foundry_series_is_a_thin_current_opl_consumer() -> None:
    series = _series()

    assert series["surface_kind"] == "opl_foundry_agent_series_consumer"
    assert series["version"] == "foundry-agent-series-consumer.v1"
    assert series["canonical_policy_export"] == "opl-framework/foundry-agent-series-policy"
    assert series["canonical_series_contract_ref"] == (
        "contracts/opl-framework/foundry-agent-series-contract.json"
    )
    assert series["canonical_skeleton_contract_ref"] == (
        "contracts/opl-framework/standard-domain-agent-skeleton-contract.json"
    )
    assert series["domain_id"] == "mag"
    assert series["foundry_agent_id"] == "mag"
    assert series["authority_owner"] == "med-autogrant"
    assert series["stage_manifest_ref"] == "agent/stages/manifest.json"
    assert series["stage_control_plane_ref"] == "opl-generated:family_stage_control_plane"
    assert series["stage_control_plane_target_domain_id"] == "med-autogrant"

    policy_release = series["shared_policy_release"]
    assert policy_release == {
        "policy_release_contract_ref": "contracts/opl-framework/foundry-agent-series-policy-release.json",
        "policy_bundle_fingerprint": "sha256:11dae4f01d2647ba77b5bee332ceda0004be62984daab26903abe85f61e36722",
        "fingerprint_algorithm": "sha256:stable-json",
        "domain_contract_policy_release_pin_required": True,
        "domain_adapter_must_not_copy_policy_body_as_authority": True,
        "consumer_alignment_check": "foundry:policy-release",
    }

    assert not LEGACY_POLICY_BODY_FIELDS.intersection(series)
    assert series["authority_boundary"] == {
        "opl_can_write_grant_truth": False,
        "opl_can_write_memory_body": False,
        "opl_can_authorize_quality_or_export": False,
        "opl_can_sign_owner_receipt": False,
        "opl_can_create_typed_blocker": False,
        "consumer_contract_can_replace_canonical_policy": False,
        "generated_surface_can_claim_domain_ready": False,
        "domain_can_write_other_domain_truth": False,
        "domain_can_write_other_domain_memory_body": False,
        "domain_can_mutate_other_domain_artifact_body": False,
        "domain_can_authorize_other_domain_quality_or_export": False,
    }


def test_foundry_series_keeps_mag_domain_authority_as_refs_only_delta() -> None:
    series = _series()
    profile = series["domain_specific_profile"]

    assert profile == {
        "profile_id": "mag_domain_specific_series_profile.v1",
        "domain_pack_kind": "declarative_grant_pack",
        "domain_input_refs": [
            "funding_call_refs",
            "applicant_profile_refs",
            "grant_strategy_memory_refs",
            "source_material_refs",
        ],
        "domain_output_refs": [
            "grant_proposal_refs",
            "revision_package_refs",
            "submission_ready_package_refs",
            "owner_receipt_or_typed_blocker_refs",
        ],
        "minimal_authority_functions_ref": "contracts/pack_compiler_input.json#/minimal_authority_functions",
    }

    pack_compiler_input = json.loads(
        (REPO_ROOT / "contracts" / "pack_compiler_input.json").read_text(encoding="utf-8")
    )
    assert pack_compiler_input["minimal_authority_functions"] == [
        "fundability_verdict",
        "quality_verdict",
        "export_verdict",
        "package_authority",
        "memory_accept_reject",
        "owner_receipt_signer",
        "grant_native_helper",
    ]


def test_physical_delete_gate_does_not_reference_a_removed_foundry_policy_body() -> None:
    audit = json.loads(
        (REPO_ROOT / "contracts" / "functional_privatization_audit.json").read_text(encoding="utf-8")
    )

    assert audit["bridge_exit_gate"]["physical_delete_authorization_refs"] == [
        "contracts/stage_run_kernel_profile.json#/legacy_runtime_residue_guard/closeout_gate/physical_delete_requires"
    ]
