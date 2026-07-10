from __future__ import annotations

import json
from pathlib import Path

import pytest

from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export


pytestmark = pytest.mark.meta
REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DOMAIN_HANDLER_ACTIONS = [
    "domain-memory/decide",
    "domain-memory/propose",
    "stage-attempt/closeout",
]


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_stage_control_plane_keeps_mag_authority_boundary() -> None:
    plane = _read_json("contracts/stage_control_plane.json")
    authority = plane["authority_boundary"]
    assert authority["domain_truth_owner"] == "med-autogrant"
    assert authority["fundability_verdict_owner"] == "med-autogrant"
    assert authority["authoring_quality_verdict_owner"] == "med-autogrant"
    assert authority["package_authority_owner"] == "med-autogrant"
    assert authority["submission_ready_export_verdict_owner"] == "med-autogrant"
    assert authority["opl_can_write_grant_truth"] is False
    assert authority["opl_can_authorize_quality_or_export"] is False

    for stage in plane["stages"]:
        stage_authority = stage["authority_boundary"]
        assert stage_authority["domain_truth_owner"] == "med-autogrant"
        assert stage_authority["opl_can_write_grant_truth"] is False
        assert stage_authority["opl_can_authorize_quality_or_export"] is False
        assert stage_authority["provider_completion_counts_as_domain_completion"] is False


def test_current_program_and_direct_handler_share_three_actions() -> None:
    current_program = _read_json("contracts/runtime-program/current-program.json")
    configured_actions = current_program["runtime_owner"]["stage_led_framework_boundary"][
        "domain_handler_adapter"
    ]["allowed_dispatch_actions"]
    export = build_domain_handler_export(
        input_path=REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
    )
    assert configured_actions == EXPECTED_DOMAIN_HANDLER_ACTIONS
    assert (
        export["domain_handler_export"]["allowed_dispatch_actions"]
        == EXPECTED_DOMAIN_HANDLER_ACTIONS
    )
