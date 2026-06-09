from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPO_ROOT / "contracts" / "external_evidence" / "mag-evidence-receipt-ledger.json"
KERNEL_PROFILE_PATH = REPO_ROOT / "contracts" / "stage_run_kernel_profile.json"


def _ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def _kernel_profile() -> dict[str, object]:
    return json.loads(KERNEL_PROFILE_PATH.read_text(encoding="utf-8"))


def test_owner_chain_live_progress_evidence_lane_records_all_mag_owned_ref_shapes() -> None:
    lane = _ledger()["owner_chain_live_progress_evidence_lane"]

    assert lane["surface_kind"] == "mag_owner_chain_live_progress_evidence_lane.v1"
    assert lane["evidence_scope"] == "live_progress_refs_only_not_readiness"
    assert lane["stage_id"] == "specific_aims_and_structure"
    assert lane["opl_hosted_path"]["runtime_owner"] == "one-person-lab"
    assert lane["opl_hosted_path"]["executor"] == "codex_cli"
    assert lane["opl_hosted_path"]["domain_owner"] == "med-autogrant"
    assert lane["opl_hosted_path"]["payload_body_included"] is False

    assert lane["accepted_return_shapes"] == [
        "domain_owner_receipt_ref",
        "typed_blocker_ref",
        "quality_receipt_ref",
        "export_receipt_ref",
        "package_receipt_ref",
        "no_regression_evidence_ref",
    ]

    refs = lane["accepted_ref_shapes"]
    assert refs["domain_owner_receipt_ref"].startswith("receipt:mag/owner-chain-live-progress/")
    assert refs["typed_blocker_ref"].startswith("typed-blocker:mag/owner-chain-live-progress/")
    assert refs["quality_receipt_ref"].startswith("receipt:mag/grant-quality/")
    assert refs["export_receipt_ref"].startswith("receipt:mag/export-verdict/")
    assert refs["package_receipt_ref"].startswith("receipt:mag/package-lifecycle/")
    assert refs["no_regression_evidence_ref"].startswith("no-regression:mag/owner-chain-live-progress/")

    evidence = lane["machine_readable_evidence"]
    assert evidence["owner_receipt"]["owner"] == "med-autogrant"
    assert evidence["typed_blocker"]["owner"] == "med-autogrant"
    assert evidence["quality_export_package_receipts"]["owner"] == "med-autogrant"
    assert evidence["no_regression"]["owner"] == "med-autogrant"
    assert evidence["quality_export_package_receipts"]["body_included"] is False
    assert evidence["no_regression"]["body_included"] is False


def test_owner_chain_live_progress_evidence_lane_keeps_false_authority_flags_closed() -> None:
    lane = _ledger()["owner_chain_live_progress_evidence_lane"]

    assert lane["false_authority_flags"] == {
        "claims_live_domain_progress": True,
        "claims_grant_ready": False,
        "claims_fundability_ready": False,
        "claims_authoring_quality_ready": False,
        "claims_export_ready": False,
        "claims_package_fresh": False,
        "claims_submission_ready": False,
        "claims_production_ready": False,
        "claims_external_submission_authorized": False,
    }

    boundary = lane["authority_boundary"]
    assert boundary["mag_owns_owner_receipt_and_typed_blocker"] is True
    assert boundary["mag_owns_quality_export_package_receipts"] is True
    assert boundary["opl_records_refs_only"] is True
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
    ):
        assert boundary[forbidden] is False, forbidden


def test_owner_chain_live_progress_canary_records_command_backed_typed_blocker() -> None:
    lane = _ledger()["owner_chain_live_progress_evidence_lane"]
    attempts = lane["canary_attempts"]

    assert isinstance(attempts, list)
    attempt = attempts[-1]
    assert attempt["attempt_id"] == "mag-owner-chain-live-progress-canary-2026-06-09"
    assert attempt["state"] == "blocked_by_mag_owned_typed_blocker_with_runtime_receipt_refs"
    assert attempt["repo_tracks_runtime_receipt_instance_body"] is False

    commands = {item["command_ref"]: item for item in attempt["commands"]}
    assert set(commands) == {
        "cmd:mag-owner-chain-canary-quality-scorecard-20260609",
        "cmd:mag-owner-chain-canary-quality-closure-dossier-20260609",
        "cmd:mag-owner-chain-canary-package-20260609",
        "cmd:mag-owner-chain-canary-typed-blocker-receipt-20260609",
        "cmd:mag-owner-chain-canary-no-regression-receipt-20260609",
    }
    assert commands["cmd:mag-owner-chain-canary-quality-scorecard-20260609"]["result"][
        "overall_status"
    ] == "blocked"
    assert commands["cmd:mag-owner-chain-canary-package-20260609"]["result"]["ok"] is False
    assert commands["cmd:mag-owner-chain-canary-package-20260609"]["result"][
        "output_dir_created"
    ] is False

    typed_blocker = attempt["mag_owned_typed_blocker"]
    assert typed_blocker["owner"] == "med-autogrant"
    assert typed_blocker["typed_blocker_ref"].startswith(
        "typed-blocker:mag/owner-chain-live-progress/"
    )
    assert typed_blocker["runtime_receipt_instance_ref"].startswith("/private/tmp/")
    assert typed_blocker["body_included"] is False
    assert attempt["mag_owned_no_regression"]["no_regression_evidence_ref"].startswith(
        "no-regression:mag/owner-chain-live-progress/"
    )

    package_refs = attempt["quality_export_package_evidence"]
    assert package_refs["quality_receipt_ref"].startswith("receipt:mag/grant-quality/")
    assert package_refs["export_receipt_ref"].startswith("receipt:mag/export-verdict/")
    assert package_refs["package_receipt_ref"].startswith("receipt:mag/package-lifecycle/")
    assert package_refs["body_included"] is False

    forbidden_write = attempt["forbidden_write_proof"]
    for field_name, value in forbidden_write.items():
        assert value is False, field_name


def test_owner_chain_live_progress_canary_keeps_readiness_claims_closed() -> None:
    lane = _ledger()["owner_chain_live_progress_evidence_lane"]
    attempt = lane["canary_attempts"][-1]

    assert attempt["claims"]["claims_live_domain_progress"] is True
    for claim_name in (
        "claims_grant_ready",
        "claims_fundability_ready",
        "claims_authoring_quality_ready",
        "claims_quality_ready",
        "claims_export_ready",
        "claims_package_fresh",
        "claims_submission_ready",
        "claims_submission_ready_export",
        "claims_production_ready",
        "claims_external_submission_authorized",
    ):
        assert attempt["claims"][claim_name] is False, claim_name

    boundary = attempt["authority_boundary"]
    assert boundary["mag_owns_typed_blocker"] is True
    assert boundary["mag_owns_no_regression_evidence"] is True
    assert boundary["mag_owns_quality_export_package_refs"] is True
    assert boundary["opl_records_refs_only"] is True
    for forbidden in (
        "opl_can_write_grant_truth",
        "opl_can_mutate_artifact_body",
        "opl_can_sign_owner_receipt",
        "opl_can_create_typed_blocker",
        "opl_can_authorize_quality_or_export",
        "human_gate_approval_recorded",
    ):
        assert boundary[forbidden] is False, forbidden


def test_kernel_profile_points_to_owner_chain_live_progress_evidence_lane() -> None:
    profile = _kernel_profile()

    assert profile["owner_chain_live_progress_evidence_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
        "owner_chain_live_progress_evidence_lane"
    )
