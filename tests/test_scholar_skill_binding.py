from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from med_autogrant.authoring_executor_parts import _build_direction_screening_prompt
from med_autogrant.domain_runtime_parts.contracts import (
    build_direct_scholar_skill_prompt_lines,
    build_hosted_authoring_contract,
    read_scholar_skill_binding_contract,
    scholar_skill_ids_for_direct_route,
)
from med_autogrant.workspace_types import WorkspaceStateError


REPO_ROOT = Path(__file__).resolve().parents[1]
BINDING_REF = "contracts/scholar_skill_binding_contract.json"
EXPECTED_FAIL_OPEN_BLOCK_FIELDS = {
    "blocks_mag_install",
    "blocks_stage_launch",
    "blocks_stage_route",
    "blocks_operational_readiness",
    "blocks_grant_core",
    "blocks_fundability_core",
    "blocks_quality_core",
    "blocks_export_core",
}


def _read_json(ref: str) -> dict:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def test_package_declares_optional_enhancement_without_install_or_runtime_gate() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    manifest = _read_json("contracts/opl_agent_package_manifest.json")

    assert manifest["version"] == "0.3.5"
    assert manifest["codex_surface"]["bundled_capability_package_ids"] == [
        "mas-scholar-skills"
    ]
    assert len(manifest["capability_dependencies"]) == 1
    dependency = manifest["capability_dependencies"][0]
    assert dependency["package_id"] == binding["provider_package_id"]
    assert dependency["consumer_profile_id"] == binding["consumer_profile_id"]
    assert dependency["capability_abi"] == binding["capability_abi"]
    assert dependency["version_requirement"] == ">=0.2.19 <0.3.0"
    assert dependency["required_export_ids"] == binding["eligible_export_ids"]
    assert dependency["required_module_ids"] == binding["eligible_module_ids"]
    assert dependency["required"] is False
    assert dependency["dependency_kind"] == "optional_enhancement"
    assert dependency["activation_materialization"]["required"] is False
    assert dependency["activation_materialization"]["receipt_required"] is False
    assert dependency["availability_policy_ref"] == (
        "contracts/scholar_skill_binding_contract.json#/availability_policy"
    )
    assert dependency["missing_or_incompatible_policy"] == (
        binding["availability_policy"]["other_observation_action"]
    )
    assert dependency["provider_completion_is_mag_completion"] is False
    assert not any(dependency["blocking_policy"].values())
    assert not any(dependency["authority_boundary"].values())


def test_every_stage_uses_resolvable_overlay_and_single_binding_contract() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    manifest = _read_json("agent/stages/manifest.json")
    stages = {stage["stage_id"]: stage for stage in manifest["stages"]}

    assert set(stages) == set(binding["stage_bindings"])
    eligible_export_ids = set(binding["eligible_export_ids"])
    for stage_id, shared_skill_ids in binding["stage_bindings"].items():
        stage = stages[stage_id]
        assert shared_skill_ids
        assert set(shared_skill_ids) <= eligible_export_ids
        assert len(stage["skill_refs"]) == 1
        for skill_ref in stage["skill_refs"]:
            assert (REPO_ROOT / skill_ref).is_file()
        prompt = (REPO_ROOT / stage["prompt_ref"]).read_text(encoding="utf-8")
        assert "`contracts/scholar_skill_binding_contract.json`" in prompt
        assert all(f"`{skill_id}`" not in prompt for skill_id in shared_skill_ids)
        assert "`candidate_refs`" in prompt
        assert "refs-only" in prompt


def test_capability_map_indexes_provider_binding_without_copying_skills() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    capability_map = _read_json("contracts/capability_map.json")
    entries = [
        capability
        for capability in capability_map["capabilities"]
        if capability["surface_role"] == "optional_professional_skill_enhancement"
    ]

    assert len(entries) == 1
    entry = entries[0]
    assert entry["physical_source_ref"]["ref"] == BINDING_REF
    assert entry["provider_package_id"] == binding["provider_package_id"]
    assert entry["consumer_profile_id"] == binding["consumer_profile_id"]
    assert entry["eligible_skill_ids"] == binding["eligible_export_ids"]
    assert entry["availability_policy_ref"] == (
        "contracts/scholar_skill_binding_contract.json#/availability_policy"
    )
    assert not any(entry["authority_boundary"].values())
    assert not any(
        (REPO_ROOT / "agent/professional_skills" / skill_id).exists()
        for skill_id in binding["eligible_export_ids"]
    )


def test_hosted_and_direct_authoring_consume_the_same_binding_contract() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    hosted = build_hosted_authoring_contract()

    assert hosted["scholar_skill_binding_contract"] == binding
    for route_id, expected_skill_ids in binding["direct_route_bindings"].items():
        assert scholar_skill_ids_for_direct_route(route_id) == expected_skill_ids
        prompt_lines = build_direct_scholar_skill_prompt_lines(route_id)
        assert all(
            skill_id in "\n".join(prompt_lines) for skill_id in expected_skill_ids
        )

    prompt = _build_direction_screening_prompt(
        input_path=REPO_ROOT / "examples/nsfc_workspace_p2a_input_intake.json",
        known_ids=[],
    )
    assert "Consumer profile: mag-medical-grant.v1" in prompt
    assert "medical-research-lit" in prompt
    assert "candidate_refs" in prompt
    assert "cannot authorize fundability, quality, export" in prompt
    assert "Optional refs-only professional Skill enhancement" in prompt
    assert "continue the MAG owner core" in prompt
    assert "Unless the provider is observed available-compatible" in prompt
    assert "Do not block install, Stage launch, Stage route" in prompt


def test_every_non_usable_or_unknown_provider_observation_is_fail_open() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    availability = binding["availability_policy"]
    expected_known_non_usable = {
        "missing",
        "incompatible",
        "disabled",
        "unmaterialized",
        "unobserved",
    }

    assert binding["enhancement_kind"] == "optional_enhancement"
    assert binding["handoff_mode"] == "refs_only"
    assert binding["provider_required"] is False
    assert availability["usable_observation"] == "available_compatible"
    assert expected_known_non_usable <= set(
        availability["known_non_usable_observations"]
    )
    assert "available_compatible" not in availability["known_non_usable_observations"]
    assert availability["other_observation_action"] == (
        "continue_with_consumer_core_and_record_diagnostic"
    )
    for observation in [*expected_known_non_usable, "future_provider_observation"]:
        assert observation != availability["usable_observation"]
        assert availability["other_observation_action"] == (
            "continue_with_consumer_core_and_record_diagnostic"
        )
    assert availability["accepted_gap_outputs"] == ["diagnostic", "quality_hint"]
    assert availability["quality_hint_is_advisory"] is True
    assert availability["creates_typed_blocker"] is False
    assert {
        key for key in availability if key.startswith("blocks_")
    } == EXPECTED_FAIL_OPEN_BLOCK_FIELDS
    assert not any(
        value
        for key, value in availability.items()
        if key.startswith("blocks_")
    )
    assert binding["invocation_policy"]["provider_gap_is_hard_stop"] is False
    assert binding["invocation_policy"]["provider_gap_can_create_typed_blocker"] is False
    assert binding["invocation_policy"]["provider_gap_can_select_stage_route"] is False


def test_binding_reader_rejects_incomplete_or_drifted_fail_open_policy(
    tmp_path: Path,
) -> None:
    binding = _read_json(BINDING_REF)
    missing_block = deepcopy(binding)
    del missing_block["availability_policy"]["blocks_operational_readiness"]
    non_advisory_hint = deepcopy(binding)
    non_advisory_hint["availability_policy"]["quality_hint_is_advisory"] = False
    drifted_available_action = deepcopy(binding)
    drifted_available_action["availability_policy"]["available_compatible_action"] = (
        "gate_consumer_readiness"
    )

    for case_id, payload in [
        ("missing-block", missing_block),
        ("non-advisory-hint", non_advisory_hint),
        ("drifted-available-action", drifted_available_action),
    ]:
        case_root = tmp_path / case_id
        contract_path = case_root / BINDING_REF
        contract_path.parent.mkdir(parents=True)
        contract_path.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises(WorkspaceStateError):
            read_scholar_skill_binding_contract(repo_root=case_root)


def test_candidate_refs_have_no_mag_verdict_or_readiness_authority() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    expected_forbidden_claims = {
        "fundability_verdict",
        "quality_verdict",
        "export_verdict",
        "submission_ready",
        "grant_ready",
        "operational_readiness",
        "stage_route_decision",
        "owner_receipt",
        "typed_blocker",
    }

    assert binding["invocation_policy"]["provider_completion_is_mag_completion"] is False
    assert binding["invocation_policy"]["candidate_consumption"] == (
        "mag_owner_surface_must_consume_reject_or_route_back"
    )
    assert not any(binding["authority_boundary"].values())
    assert set(binding["forbidden_candidate_claims"]) == expected_forbidden_claims
