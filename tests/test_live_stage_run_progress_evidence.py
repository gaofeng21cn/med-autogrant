from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
LIVE_PROGRESS_PATH = REPO_ROOT / "contracts" / "live_stage_run_progress_evidence.json"
LEDGER_PATH = REPO_ROOT / "contracts" / "external_evidence" / "mag-evidence-receipt-ledger.json"


def _live_progress() -> dict[str, object]:
    return json.loads(LIVE_PROGRESS_PATH.read_text(encoding="utf-8"))


def _ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def test_live_stage_run_progress_evidence_is_mag_source_of_truth_blocker() -> None:
    payload = _live_progress()

    assert payload["surface_kind"] == "mag_live_stage_run_progress_evidence.v1"
    assert payload["owner"] == "med-autogrant"
    assert payload["source_of_truth"] is True
    assert payload["state"] == "blocked_by_mag_owned_typed_blocker"
    assert payload["evidence_scope"] == "live_stage_run_progress_owner_answer_or_blocker"

    live_stage_run = payload["live_stage_run"]
    assert live_stage_run["runtime_owner"] == "one-person-lab"
    assert live_stage_run["executor"] == "codex_cli"
    assert live_stage_run["domain_owner"] == "med-autogrant"
    assert live_stage_run["progress_delta_classification"] == "typed_blocker"
    assert live_stage_run["payload_body_included"] is False
    assert live_stage_run["production_acceptance_tail_is_live_progress"] is False

    owner_answer = payload["owner_answer"]
    assert owner_answer["accepted_return_shape"] == "typed_blocker_ref"
    assert owner_answer["accepted_return_shapes"] == [
        "domain_owner_receipt_ref",
        "typed_blocker_ref",
        "human_gate_ref",
        "quality_or_export_receipt_ref",
        "no_regression_ref",
        "long_soak_ref",
    ]
    assert owner_answer["typed_blocker_ref"] == payload["typed_blocker"]["typed_blocker_ref"]


def test_live_stage_run_progress_refs_use_standard_owner_answer_fields() -> None:
    payload = _live_progress()
    refs = payload["refs"]

    assert set(refs) == {
        "owner_receipt_refs",
        "typed_blocker_refs",
        "human_gate_refs",
        "quality_or_export_receipt_refs",
        "no_regression_refs",
        "long_soak_refs",
    }
    for ref_key, values in refs.items():
        assert isinstance(values, list)
        assert values, ref_key
        assert all(isinstance(value, str) and value for value in values), ref_key

    assert payload["typed_blocker"]["typed_blocker_ref"] in refs["typed_blocker_refs"]
    assert "human_gate:submission_ready_export_gate" in refs["human_gate_refs"]
    assert any(ref.startswith("no-regression:mag/") for ref in refs["no_regression_refs"])
    assert any(ref.startswith("typed-blocker:mag/manifest-sustained-consumption/") for ref in refs["long_soak_refs"])


def test_live_stage_run_progress_typed_blocker_has_lineage_budget_and_next_delta() -> None:
    payload = _live_progress()
    typed_blocker = payload["typed_blocker"]

    assert typed_blocker["owner"] == "med-autogrant"
    assert typed_blocker["blocker_kind"] == "missing_real_live_stage_run_progress_prerequisites"
    assert typed_blocker["blocker_state"] == "current_live_progress_blocked_no_ready_claim"
    assert typed_blocker["lineage"] == [
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/owner_chain_live_progress_evidence_lane",
        "contracts/production_acceptance/mag-production-acceptance.json#/closure_evidence",
    ]
    assert typed_blocker["repeat_budget"]["max_repeat_without_new_evidence"] == 1
    assert typed_blocker["next_forced_delta"]["owner"] == "med-autogrant_or_app_live_operator"
    assert typed_blocker["next_forced_delta"]["required_shape"] == (
        "real_owner_receipt_or_typed_blocker_or_no_regression_evidence_ref"
    )
    assert typed_blocker["escalation_owner"] == "med-autogrant"


def test_live_stage_run_progress_lists_missing_real_prerequisites_without_success_claims() -> None:
    payload = _live_progress()
    prerequisites = {
        item["prerequisite_id"]: item for item in payload["missing_real_progress_prerequisites"]
    }

    assert set(prerequisites) == {
        "sustained_opl_hosted_grant_stage_attempts",
        "submission_ready_human_gate_receipt",
        "sustained_app_operator_or_default_caller_consumption",
        "temporal_provider_long_soak_window_evidence",
        "production_success_rate_or_no_regression_followthrough",
    }
    for prerequisite_id, prerequisite in prerequisites.items():
        assert prerequisite["current_ref_is_success_evidence"] is False, prerequisite_id
        assert prerequisite["state"] in {"open", "blocked_by_existing_human_gate_typed_blocker"}
        assert prerequisite["current_refs"]
        assert prerequisite["required_evidence"]


def test_live_stage_run_progress_binds_existing_canary_as_provenance_only() -> None:
    payload = _live_progress()
    ledger = _ledger()
    canary = ledger["owner_chain_live_progress_evidence_lane"]["canary_attempts"][-1]

    assert payload["refs"]["typed_blocker_refs"][1] == (
        canary["mag_owned_typed_blocker"]["typed_blocker_ref"]
    )
    assert payload["refs"]["no_regression_refs"][0] == (
        canary["mag_owned_no_regression"]["no_regression_evidence_ref"]
    )
    assert payload["refs"]["quality_or_export_receipt_refs"][0] == (
        canary["quality_export_package_evidence"]["quality_receipt_ref"]
    )
    assert payload["refs"]["quality_or_export_receipt_refs"][1] == (
        canary["quality_export_package_evidence"]["export_receipt_ref"]
    )
    assert payload["production_acceptance_tail_policy"] == {
        "production_acceptance_tail_ref": "contracts/production_acceptance/mag-production-acceptance.json",
        "production_acceptance_tail_counts_as_live_progress": False,
        "production_acceptance_tail_role": (
            "historical_acceptance_provenance_not_live_stage_progress_source_of_truth"
        ),
    }


def test_live_stage_run_progress_authority_boundary_has_no_ready_claims() -> None:
    payload = _live_progress()

    assert payload["authority_boundary"]["mag_owns_live_progress_owner_answer"] is True
    assert payload["authority_boundary"]["opl_records_refs_only"] is True
    for forbidden in (
        "opl_can_write_grant_truth",
        "opl_can_mutate_artifact_body",
        "opl_can_sign_owner_receipt",
        "opl_can_create_typed_blocker",
        "opl_can_authorize_quality_or_export",
        "opl_can_declare_grant_ready",
        "opl_can_declare_submission_ready",
        "provider_completion_counts_as_readiness",
        "file_presence_counts_as_readiness",
        "read_model_counts_as_readiness",
        "production_acceptance_tail_counts_as_live_progress",
    ):
        assert payload["authority_boundary"][forbidden] is False, forbidden

    for claim_name, value in payload["claims"].items():
        assert value is False, claim_name

