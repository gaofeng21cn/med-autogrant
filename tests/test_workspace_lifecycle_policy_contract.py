from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def _workspace_lifecycle_policy() -> dict[str, object]:
    return json.loads((REPO_ROOT / "contracts" / "workspace_lifecycle_policy.json").read_text(encoding="utf-8"))


def test_workspace_lifecycle_policy_is_opl_owned_and_mag_refs_only() -> None:
    policy = _workspace_lifecycle_policy()

    assert policy["surface_kind"] == "opl_domain_workspace_file_lifecycle_policy"
    assert policy["policy_owner"] == "one-person-lab"
    assert policy["domain_id"] == "med-autogrant"
    assert policy["structural_gate_only"] is True

    source_boundary = policy["repo_source_boundaries"]
    assert source_boundary["runtime_artifacts_live_in_source_repo"] is False
    assert source_boundary["developer_checkout_may_define_app_runtime_without_explicit_override"] is False
    assert {
        "artifacts/",
        "workspaces/",
        "workspace/",
        "runtime/artifacts/",
        "runtime/workspaces/",
    } <= set(source_boundary["forbidden_runtime_artifact_roots"])

    artifact_roots = policy["workspace_runtime_artifact_roots"]
    assert artifact_roots["externalized"] is True
    assert artifact_roots["repo_source_policy"] == "locator_index_schema_receipt_refs_only"
    assert {
        "workspace_root_ref",
        "runtime_artifact_root_ref",
        "artifact_locator_ref",
        "restore_or_retention_receipt_ref",
    } <= set(artifact_roots["required_locator_refs"])


def test_workspace_lifecycle_policy_uses_mag_grant_authority_vocabulary() -> None:
    policy = _workspace_lifecycle_policy()
    split = policy["lifecycle_authority_split"]

    assert split["opl_owned_primitives"] == [
        "workspace_lifecycle",
        "file_lifecycle",
        "artifact_locator_index",
        "retention_restore_ledger",
        "migration_ledger",
        "operator_projection",
    ]
    assert split["domain_owned_authority"] == [
        "domain_truth",
        "fundability_quality_export_submission_verdict",
        "artifact_body_authority",
        "memory_body_accept_reject",
        "owner_receipt",
    ]
    assert "quality_export_visual_verdict" not in split["domain_owned_authority"]

    boundary = policy["authority_boundary"]
    assert boundary == {
        "policy_can_claim_domain_ready_or_artifact_authority": False,
        "opl_can_write_domain_truth": False,
        "opl_can_write_memory_body": False,
        "opl_can_mutate_domain_artifact_body": False,
        "opl_can_authorize_quality_or_export": False,
    }
