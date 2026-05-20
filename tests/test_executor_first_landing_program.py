from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAM_PATH = (
    REPO_ROOT
    / "contracts"
    / "production_acceptance"
    / "mag-executor-first-landing.json"
)
ACCEPTANCE_PATH = (
    REPO_ROOT
    / "contracts"
    / "production_acceptance"
    / "mag-production-acceptance.json"
)

REQUIRED_LANES = {
    "stage_pack_enrichment",
    "independent_review_receipt_gate",
    "external_evidence_pack_consumption",
    "real_workspace_receipt_scaleout",
    "physical_morphology_hygiene",
}

LANE_REQUIRED_KEYS = {
    "owner",
    "scope",
    "inputs",
    "refs",
    "deliverables",
    "verification_refs",
    "done_criteria",
    "forbidden_claims",
    "parallelizable",
    "blocks",
    "blocked_by",
}


def _program() -> dict[str, object]:
    return json.loads(PROGRAM_PATH.read_text(encoding="utf-8"))


def _acceptance() -> dict[str, object]:
    return json.loads(ACCEPTANCE_PATH.read_text(encoding="utf-8"))


def _lanes_by_id() -> dict[str, dict[str, object]]:
    return {lane["lane_id"]: lane for lane in _program()["parallel_lanes"]}


def _assert_non_empty_string_list(values: object) -> None:
    assert isinstance(values, list)
    assert values
    assert all(isinstance(value, str) and value for value in values)


def _assert_repo_paths_exist(values: object) -> None:
    assert isinstance(values, list)
    for value in values:
        if not isinstance(value, str):
            continue
        if value.startswith(("/", "cmd:", "human_doc:", "mag://")):
            continue
        if value.startswith(("contracts/", "schemas/", "src/", "tests/", "agent/", "docs/")):
            assert (REPO_ROOT / value).exists(), value


def test_executor_first_landing_program_exists_and_is_evidence_gated() -> None:
    assert PROGRAM_PATH.exists()
    program = _program()

    assert program["surface_kind"] == "mag_executor_first_landing_program.v1"
    assert program["domain_id"] == "med-autogrant"
    assert program["owner"] == "med-autogrant"
    assert program["state"] == "structural_ready_evidence_gated"

    strategy = program["strategy"]
    assert strategy["implementation_mode"] == "executor_first"
    assert strategy["default_executor"] == "codex_cli"
    assert strategy["runtime_model"] == "contract_light"
    assert strategy["parallel_landing_required"] is True
    assert strategy["mag_implements_opl_runtime"] is False
    assert strategy["mag_implements_app_workbench"] is False
    assert strategy["missing_evidence_claimed_complete"] is False

    current = program["current_available_state"]
    assert current["structural_state"] == "structural_ready"
    assert current["evidence_state"] == "evidence_gated"
    assert current["direct_hosted_parity_state"] == "requested_not_proven"
    assert current["external_evidence_pack_state"] == (
        "request_pack_declared_external_evidence_not_claimed"
    )
    assert current["owner_receipt_scaleout_state"] == (
        "production_acceptance_tail_closed_by_domain_owner_receipt_external_scaleout_gated"
    )
    assert current["physical_morphology_state"] == (
        "cleanup_lane_defined_external_evidence_gated"
    )


def test_landing_program_syncs_mag_owned_production_acceptance_tail_closure() -> None:
    program = _program()
    acceptance = _acceptance()
    closure = acceptance["closure_evidence"]

    assert acceptance["evidence_tail_status"] == "closed_by_domain_owned_acceptance_receipt"
    assert closure["accepted_return_shape"] == "domain_owner_receipt_ref"

    refs = program["refs"]
    assert refs["production_acceptance_ref"] == (
        "contracts/production_acceptance/mag-production-acceptance.json"
    )
    assert refs["production_acceptance_owner_receipt_ref"] == closure["owner_receipt_ref"]
    assert refs["production_live_acceptance_receipt_projection_ref"] in acceptance["refs"][
        "owner_receipt_refs"
    ]

    forbidden = program["forbidden_global_claims"]
    assert forbidden["claims_mag_owned_production_acceptance_tail_closed"] is True
    assert (
        forbidden["mag_owned_production_acceptance_tail_closure_scope"]
        == "production_acceptance_tail_only"
    )
    for still_open_claim in (
        "claims_opl_generated_hosted_production_caller_complete",
        "claims_direct_hosted_parity_complete",
        "claims_external_evidence_pack_consumed",
        "claims_live_owner_receipt_scaleout_complete",
        "claims_physical_morphology_cleanup_complete",
        "claims_missing_evidence_complete",
    ):
        assert forbidden[still_open_claim] is False


def test_parallel_lanes_have_required_contract_shape() -> None:
    lanes = _lanes_by_id()
    assert set(lanes) == REQUIRED_LANES

    for lane_id, lane in lanes.items():
        missing = LANE_REQUIRED_KEYS - set(lane)
        assert missing == set(), lane_id
        assert lane["owner"] in {"med-autogrant", "one-person-lab"}
        assert isinstance(lane["scope"], str) and lane["scope"]
        assert isinstance(lane["parallelizable"], bool)
        assert isinstance(lane["blocks"], list)
        assert isinstance(lane["blocked_by"], list)
        for key in (
            "inputs",
            "refs",
            "deliverables",
            "verification_refs",
            "done_criteria",
            "forbidden_claims",
        ):
            _assert_non_empty_string_list(lane[key])
        _assert_repo_paths_exist(lane["inputs"])
        _assert_repo_paths_exist(lane["refs"])

    assert lanes["physical_morphology_hygiene"]["parallelizable"] is False
    for lane_id in REQUIRED_LANES - {"physical_morphology_hygiene"}:
        assert lanes[lane_id]["parallelizable"] is True


def test_global_forbidden_claims_keep_missing_evidence_open() -> None:
    program = _program()
    forbidden = program["forbidden_global_claims"]

    for claim in (
        "claims_opl_provider_completion",
        "claims_opl_generated_hosted_production_caller_complete",
        "claims_direct_hosted_parity_complete",
        "claims_external_evidence_pack_consumed",
        "claims_independent_review_gate_passed",
        "claims_live_owner_receipt_scaleout_complete",
        "claims_physical_morphology_cleanup_complete",
        "claims_missing_evidence_complete",
    ):
        assert forbidden[claim] is False

    authority = program["authority_boundary"]
    for claim in (
        "opl_provider_completion_can_claim_domain_ready",
        "opl_provider_completion_can_claim_fundability_ready",
        "opl_provider_completion_can_claim_export_ready",
        "conformance_can_claim_domain_ready",
        "scorecard_can_claim_fundability_ready",
        "package_existence_can_claim_submission_ready",
        "mag_can_claim_external_evidence_complete",
        "mag_can_claim_direct_hosted_parity_complete",
        "mag_can_claim_owner_receipt_scaleout_complete",
        "mag_can_claim_physical_morphology_cleanup_complete",
    ):
        assert authority[claim] is False


def test_independent_review_gate_keeps_ready_claims_evidence_gated() -> None:
    lane = _lanes_by_id()["independent_review_receipt_gate"]

    assert "med-autogrant" == lane["owner"]
    for forbidden in (
        "provider_completion_is_fundability_ready",
        "quality_scorecard_is_fundability_ready",
        "package_existence_is_submission_ready",
        "conformance_is_domain_ready",
    ):
        assert forbidden in lane["forbidden_claims"]
    assert "real_workspace_receipt_scaleout" in lane["blocks"]


def test_external_evidence_lane_is_request_pack_only() -> None:
    program = _program()
    lane = _lanes_by_id()["external_evidence_pack_consumption"]

    assert lane["owner"] == "one-person-lab"
    assert (
        program["refs"]["external_evidence_request_pack_ref"]
        == "/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack"
    )
    for forbidden in (
        "mag_implements_opl_runtime",
        "mag_implements_app_workbench",
        "mag_claims_external_evidence_exists",
        "external_pack_request_equals_consumed_evidence",
    ):
        assert forbidden in lane["forbidden_claims"]


def test_real_workspace_scaleout_stays_typed_blocker_until_receipts_exist() -> None:
    lane = _lanes_by_id()["real_workspace_receipt_scaleout"]

    assert "independent_review_receipt_gate" in lane["blocked_by"]
    assert "external_evidence_pack_consumption" in lane["blocked_by"]
    for deliverable in (
        "real_workspace_owner_receipt_refs",
        "typed_blocker_refs",
        "memory_accept_reject_receipt_refs",
        "package_export_lifecycle_receipt_refs",
    ):
        assert deliverable in lane["deliverables"]
    assert "typed_blocker_roundtrip_equals_scaleout_complete" in lane["forbidden_claims"]


def test_physical_morphology_cleanup_is_blocked_by_external_evidence() -> None:
    lane = _lanes_by_id()["physical_morphology_hygiene"]

    assert lane["parallelizable"] is False
    for blocker in (
        "stage_pack_enrichment",
        "external_evidence_pack_consumption",
        "real_workspace_receipt_scaleout",
    ):
        assert blocker in lane["blocked_by"]
    for forbidden in (
        "cleanup_plan_equals_cleanup_complete",
        "opl_cleanup_ledger_equals_production_caller_migrated",
        "physical_conformance_equals_no_active_caller",
        "morphology_hygiene_equals_grant_ready",
    ):
        assert forbidden in lane["forbidden_claims"]
