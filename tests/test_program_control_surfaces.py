from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"
RUNTIME_STATE_ROOT = "$CODEX_HOME/projects/med-autogrant/runtime-state/"


def _contract() -> dict[str, object]:
    return json.loads(CURRENT_PROGRAM_CONTRACT.read_text(encoding="utf-8"))


def test_current_program_tracks_runtime_owner_and_executor_boundary() -> None:
    contract = _contract()
    runtime_owner = contract["runtime_owner"]
    framework = runtime_owner["stage_led_framework_boundary"]
    executor_defaults = contract["executor_defaults"]

    assert contract["program_id"] == "med-autogrant-mainline"
    assert contract["formal_entry"]["default_formal_entry"] == "CLI"
    assert runtime_owner["default_task_runtime_owner"] == "one-person-lab"
    assert runtime_owner["default_runtime_substrate"] == "temporal"
    assert runtime_owner["default_stage_executor"] == "codex_cli"
    assert runtime_owner["mag_implements_daemon"] is False
    assert runtime_owner["mag_implements_scheduler"] is False
    assert runtime_owner["mag_implements_attempt_loop"] is False
    assert runtime_owner["mag_owns_attempt_ledger"] is False

    assert framework["production_substrate"] == "Temporal"
    assert framework["task_start_handoff_owner"] == "one-person-lab"
    assert framework["post_start_residency_owner"] == "one-person-lab"
    assert "author-side route truth" in framework["mag_owned_truth"]
    assert "submission-ready export gate" in framework["mag_owned_truth"]
    assert "runtime_control.semantic_closure" in framework["framework_consumed_projection"]
    assert "owner_receipt_contract" in framework["framework_consumed_projection"]
    assert "physical_skeleton_follow_through" in framework["framework_consumed_projection"]
    assert "grant-domain truth owner" in framework["framework_non_goals"]

    assert executor_defaults["default_executor_name"] == "codex_cli"
    assert executor_defaults["canonical_executor_backends"] == [
        "codex_cli",
        "hermes_agent",
        "claude_code",
    ]
    assert executor_defaults["non_default_executor_requires_explicit_selection"] is True
    assert executor_defaults["non_default_executor_forbids_silent_codex_fallback"] is True
    assert contract["machine_local_runtime_state"]["root"] == RUNTIME_STATE_ROOT
    assert contract["machine_local_runtime_state"]["not_repo_tracked"] is True


def test_current_program_consumer_thinning_stays_request_only() -> None:
    contract = _contract()
    thinning = contract["runtime_owner"]["stage_led_framework_boundary"][
        "consumer_thinning_contract"
    ]
    request_pack = thinning["external_evidence_request_pack"]
    taxonomy = thinning["minimal_authority_surface_taxonomy"]

    assert thinning["active_caller_owner"] == "med-autogrant"
    assert thinning["external_evidence_request_pack_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack"
    )
    assert request_pack["state"] == "request_pack_declared_external_evidence_not_claimed"
    assert request_pack["forbidden_completion_claims"]["claims_opl_replacement_exists"] is False
    assert (
        request_pack["forbidden_completion_claims"]["claims_production_long_run_soak_complete"]
        is False
    )
    assert request_pack["authority_boundary"]["mag_implements_opl_runtime"] is False
    assert request_pack["authority_boundary"]["mag_implements_app_workbench"] is False
    assert request_pack["authority_boundary"]["mag_claims_external_evidence_exists"] is False
    assert taxonomy["compatibility_alias_allowed"] is False
    assert "legacy_function_id_compatibility" not in taxonomy


def test_repo_tracked_truth_surfaces_use_machine_paths_or_semantic_docs() -> None:
    for surface_ref in _contract()["repo_tracked_truth_surfaces"]:
        if surface_ref.startswith("human_doc:"):
            assert surface_ref.removeprefix("human_doc:").replace("_", "").isalnum()
        else:
            assert (REPO_ROOT / surface_ref).exists(), surface_ref
