from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"


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
