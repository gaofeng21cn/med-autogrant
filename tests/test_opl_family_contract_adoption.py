from __future__ import annotations

import json
from pathlib import Path

import pytest

from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export
from med_autogrant.product_entry_parts.domain_handler_contract import ALLOWED_ACTIONS


pytestmark = pytest.mark.meta
REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_stage_manifest_keeps_mag_authority_boundary_without_private_compiler() -> None:
    manifest = _read_json("agent/stages/manifest.json")
    authority = manifest["authority_boundary"]
    assert authority["domain_truth_owner"] == "med-autogrant"
    assert authority["fundability_verdict_owner"] == "med-autogrant"
    assert authority["authoring_quality_verdict_owner"] == "med-autogrant"
    assert authority["package_authority_owner"] == "med-autogrant"
    assert authority["submission_ready_export_verdict_owner"] == "med-autogrant"
    assert authority["opl_can_write_grant_truth"] is False
    assert authority["opl_can_authorize_quality_or_export"] is False

    assert len(manifest["stages"]) == 6
    for stage in manifest["stages"]:
        assert stage["prompt_ref"].startswith("agent/prompts/")
        assert stage["policy_ref"].startswith("agent/stages/")
        assert stage["allowed_action_refs"]

    assert not (REPO_ROOT / "contracts" / "stage_control_plane.json").exists()
    assert not (REPO_ROOT / "src" / "med_autogrant" / "stage_control_plane.py").exists()


def test_current_program_and_direct_handler_share_three_actions() -> None:
    current_program = _read_json("contracts/runtime-program/current-program.json")
    configured_actions = current_program["domain_handler"]["allowed_dispatch_actions"]
    expected_actions = sorted(ALLOWED_ACTIONS)
    export = build_domain_handler_export(
        input_path=REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
    )
    assert configured_actions == expected_actions
    assert (
        export["domain_handler_export"]["allowed_dispatch_actions"]
        == expected_actions
    )
    handler_export = export["domain_handler_export"]
    assert "family_stage_control_plane" not in handler_export
    assert handler_export["declarative_stage_manifest_ref"] == "agent/stages/manifest.json"
    assert handler_export["family_stage_control_plane_ref"] == (
        "/product_entry_manifest/family_stage_control_plane"
    )
