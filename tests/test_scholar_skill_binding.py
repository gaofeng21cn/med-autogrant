from __future__ import annotations

import json
from pathlib import Path

from med_autogrant.authoring_executor_parts import _build_direction_screening_prompt
from med_autogrant.domain_runtime_parts.contracts import (
    build_direct_scholar_skill_prompt_lines,
    build_hosted_authoring_contract,
    read_scholar_skill_binding_contract,
    scholar_skill_ids_for_direct_route,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
BINDING_REF = "contracts/scholar_skill_binding_contract.json"


def _read_json(ref: str) -> dict:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def test_package_dependency_matches_mag_consumer_profile() -> None:
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
    assert dependency["required_export_ids"] == binding["required_export_ids"]
    assert dependency["required_module_ids"] == binding["required_module_ids"]
    assert dependency["required"] is True
    assert not any(dependency["authority_boundary"].values())


def test_every_stage_uses_resolvable_mag_overlay_and_declared_shared_skills() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    manifest = _read_json("agent/stages/manifest.json")
    stages = {stage["stage_id"]: stage for stage in manifest["stages"]}

    assert set(stages) == set(binding["stage_bindings"])
    required_export_ids = set(binding["required_export_ids"])
    for stage_id, shared_skill_ids in binding["stage_bindings"].items():
        stage = stages[stage_id]
        assert shared_skill_ids
        assert set(shared_skill_ids) <= required_export_ids
        assert len(stage["skill_refs"]) == 1
        for skill_ref in stage["skill_refs"]:
            assert (REPO_ROOT / skill_ref).is_file()
        prompt = (REPO_ROOT / stage["prompt_ref"]).read_text(encoding="utf-8")
        for skill_id in shared_skill_ids:
            assert f"`{skill_id}`" in prompt
        assert "`candidate_refs`" in prompt
        assert "refs-only" in prompt


def test_capability_map_indexes_provider_binding_without_copying_skills() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    capability_map = _read_json("contracts/capability_map.json")
    entries = [
        capability
        for capability in capability_map["capabilities"]
        if capability["surface_role"] == "dependency_professional_skill_bundle"
    ]

    assert len(entries) == 1
    entry = entries[0]
    assert entry["physical_source_ref"]["ref"] == BINDING_REF
    assert entry["provider_package_id"] == binding["provider_package_id"]
    assert entry["consumer_profile_id"] == binding["consumer_profile_id"]
    assert entry["exported_skill_ids"] == binding["required_export_ids"]
    assert not any(entry["authority_boundary"].values())
    assert not any(
        (REPO_ROOT / "agent/professional_skills" / skill_id).exists()
        for skill_id in binding["required_export_ids"]
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


def test_candidate_refs_have_no_mag_verdict_or_readiness_authority() -> None:
    binding = read_scholar_skill_binding_contract(repo_root=REPO_ROOT)
    expected_forbidden_claims = {
        "fundability_verdict",
        "quality_verdict",
        "export_verdict",
        "submission_ready",
        "grant_ready",
        "owner_receipt",
        "typed_blocker",
    }

    assert binding["invocation_policy"]["provider_completion_is_mag_completion"] is False
    assert binding["invocation_policy"]["candidate_consumption"] == (
        "mag_owner_surface_must_consume_reject_or_route_back"
    )
    assert not any(binding["authority_boundary"].values())
    assert set(binding["forbidden_candidate_claims"]) == expected_forbidden_claims
