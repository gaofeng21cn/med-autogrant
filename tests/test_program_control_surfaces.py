from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"
DOMAIN_DESCRIPTOR_CONTRACT = REPO_ROOT / "contracts" / "domain_descriptor.json"


def _contract() -> dict[str, object]:
    return json.loads(CURRENT_PROGRAM_CONTRACT.read_text(encoding="utf-8"))


def test_current_program_tracks_runtime_owner_and_executor_boundary() -> None:
    contract = _contract()
    runtime_binding = contract["runtime_binding"]

    assert set(contract) == {
        "surface_kind",
        "schema_version",
        "program_id",
        "canonical_agent_id",
        "domain_id",
        "runtime_binding",
        "domain_handler",
        "minimal_authority_functions_ref",
        "contract_refs",
    }
    assert contract["surface_kind"] == "mag_current_program_pointer"
    assert contract["schema_version"] == 1
    assert contract["program_id"] == "med-autogrant-mainline"
    assert contract["canonical_agent_id"] == "mag"
    assert contract["domain_id"] == "med-autogrant"
    assert runtime_binding["runtime_provider_owner"] == "configured_family_runtime_provider"
    assert runtime_binding["task_runtime_owner"] == "one-person-lab"
    assert runtime_binding["runtime_substrate"] == "temporal"
    assert runtime_binding["stage_executor"] == "codex_cli"
    assert runtime_binding["domain_authority_owner"] == "med-autogrant"
    assert contract["minimal_authority_functions_ref"] == (
        "contracts/pack_compiler_input.json#/minimal_authority_functions"
    )


def test_current_program_is_a_pointer_not_a_private_platform_snapshot() -> None:
    contract = _contract()
    serialized = json.dumps(contract, sort_keys=True)

    assert "product_entry_manifest" not in serialized
    assert "mag_consumer_thinning_contract" not in serialized
    assert "stage_led_framework_boundary" not in serialized
    assert "phase_map" not in serialized
    assert "ideal_target" not in serialized


def test_repo_tracked_truth_surfaces_use_machine_paths_or_semantic_docs() -> None:
    for surface_ref in _contract()["contract_refs"].values():
        assert (REPO_ROOT / surface_ref).exists(), surface_ref


def test_domain_descriptor_declares_the_opl_hosted_standard_interface() -> None:
    descriptor = json.loads(DOMAIN_DESCRIPTOR_CONTRACT.read_text(encoding="utf-8"))

    assert descriptor["standard_agent_interface"] == {
        "version": "opl_standard_agent_interface.v1",
        "workspace_binding": {
            "locator_surface_kind": "med_autogrant_workspace_input",
            "default_profile_id": "one_off",
            "workspace_kind": "grant_authoring_workspace",
            "project_kind": "grant_project",
            "project_collection_label": "deliverables",
            "default_workspace_id": "grant-workspace",
            "default_project_id": "grant-001",
            "required_locator_fields": ["input_path"],
            "optional_locator_fields": [],
        },
        "runtime": {
            "runtime_domain_id": "medautogrant",
            "registration_ref": (
                "contracts/generated_surface_handoff.json#/domain_handler_targets"
            ),
        },
        "progress": {
            "deliverable_delta_aliases": ["grant_work_progress"],
            "platform_delta_aliases": ["platform_evidence_progress"],
        },
        "routing": {
            "explicit_aliases": ["mag", "medautogrant", "med-autogrant", "grant"],
            "workstream_ids": ["grant_ops"],
            "intent_signals": ["grant", "proposal", "fundability", "grant_application"],
            "ambiguity_policy": "require_explicit_workstream",
        },
    }
