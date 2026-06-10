from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def _manifest() -> dict[str, object]:
    return json.loads(
        (REPO_ROOT / "contracts/foundry-agent-os-domain-kernel-manifest.json").read_text(
            encoding="utf-8"
        )
    )


def test_mag_foundry_agent_os_kernel_manifest_declares_grant_authority() -> None:
    manifest = _manifest()

    assert manifest["surface_kind"] == "foundry_agent_os_domain_kernel_manifest"
    assert manifest["domain_id"] == "med-autogrant"
    assert manifest["domain_agent_id"] == "mag"
    assert manifest["owner"] == "Med Auto Grant"

    kernel = manifest["domain_authority_kernel"]
    retained = set(kernel["retained_surfaces"])
    assert {
        "grant_truth",
        "funding_call_interpretation",
        "profile_task_lock",
        "fundability_strategy",
        "specific_aims_and_proposal_route_truth",
        "fundability_quality_export_submission_verdict",
        "submission_package_authority",
        "manual_portal_boundary",
        "grant_strategy_memory_accept_reject_or_blocker",
        "owner_receipt_signer",
        "typed_blocker_materializer",
    } <= retained
    assert kernel["owner_receipt_signer"] == "med-autogrant_authority_kernel"
    assert kernel["typed_blocker_signer"] == "med-autogrant_authority_kernel"
    assert "fundability_quality_export_submission_verdict" in kernel[
        "quality_export_publication_review_verdict_signers"
    ]
    assert "mag_owner_receipt_ref" in kernel["accepted_answer_shapes"]
    assert "mag_typed_blocker_ref" in kernel["accepted_answer_shapes"]


def test_mag_foundry_agent_os_kernel_manifest_upcollects_generic_surfaces_to_opl() -> None:
    manifest = _manifest()

    assert manifest["default_read_root"]["surface"] == "current_owner_delta"
    assert manifest["default_read_root"]["ordinary_operator_root"] is True
    assert manifest["default_read_root"]["projection_can_be_owner_answer"] is False
    assert set(manifest["opl_upcollect_surfaces"]) >= {
        "generic_runtime",
        "pack_compiler",
        "generated_cli_mcp_app_status_workbench_surfaces",
        "workspace_source_package_shell",
        "quality_readiness_projection",
        "console_current_owner_delta_projection",
        "refs_only_vault_lineage",
        "capability_registry_abi",
    }


def test_mag_foundry_agent_os_kernel_manifest_forbids_false_authority() -> None:
    manifest = _manifest()

    for surface in ["opl", "vault", "console", "runway", "pack", "capability_registry"]:
        flags = manifest["forbidden_authority_flags"][surface]
        assert flags == {
            "can_write_domain_truth": False,
            "can_sign_owner_receipt": False,
            "can_create_domain_typed_blocker": False,
            "can_authorize_quality_export_publication_or_review_verdict": False,
        }

    non_claims = manifest["non_claims"]
    for claim in [
        "grant_ready",
        "fundability_ready",
        "quality_ready",
        "export_ready",
        "submission_ready",
        "production_ready",
        "physical_delete_authorized",
    ]:
        assert non_claims[claim] is False
