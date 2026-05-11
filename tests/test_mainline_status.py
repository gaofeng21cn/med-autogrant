from __future__ import annotations

import importlib

from med_autogrant.public_cli import public_cli_command
from support.cli import run_json_cli


def test_mainline_status_projects_line_focus_records_and_maintainer_references() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    payload = module.read_mainline_status()

    assert payload["program_id"] == "med-autogrant-mainline"
    assert (
        payload["current_line"]["current_owner_line"]
        == "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers"
    )
    assert payload["current_focus"]["summary"]
    assert payload["current_focus"]["focus_items"]
    assert payload["ideal_target"]["family_top_entry"] == "OPL Codex-first stage-led agent runtime framework"
    assert payload["ideal_target"]["stage_attempt_minimum_execution_unit"] == "Codex CLI"
    assert payload["ideal_target"]["domain_direct_entry"] == "Med Auto Grant Product Entry"
    assert any(item["record_id"] == "P4.B" for item in payload["completed_records"])
    assert any(item["record_id"] == "P4.C" for item in payload["completed_records"])
    assert any(item["record_id"] == "P4.E" for item in payload["completed_records"])
    assert any(item["record_id"] == "P4.F" for item in payload["completed_records"])
    assert any(item["record_id"] == "P4.G" for item in payload["completed_records"])
    maintainer_references = payload["maintainer_references"]
    assert maintainer_references["runtime_owner"]["active_phase"] == "P4 mature direct grant product entry"
    assert (
        maintainer_references["runtime_owner"]["active_tranche"]
        == "P4.G authoring-quality-first completion semantics alignment"
    )
    assert maintainer_references["current_record_detail"]["phase_id"] == "P4"
    assert maintainer_references["current_record_detail"]["status"] == "next"
    assert len(maintainer_references["phase_ladder"]) == 4
    assert maintainer_references["phase_ladder"][0]["phase_id"] == "P1"
    assert maintainer_references["phase_ladder"][3]["phase_id"] == "P4"
    assert any(item["name"] == "grant_user_loop" for item in maintainer_references["phase_ladder"][3]["entry_points"])
    assert any(
        item == "human_doc:2026_04_12_p4c_mainline_status_and_grant_user_loop_current_truth"
        for item in maintainer_references["phase_ladder"][3]["phase_docs"]
    )
    assert any(
        item == "human_doc:2026_04_13_p4e_schema_backed_product_status_and_manifest_current_truth"
        for item in maintainer_references["phase_ladder"][3]["phase_docs"]
    )
    assert any(
        item == "human_doc:2026_04_13_p4f_local_submission_ready_package_current_truth"
        for item in maintainer_references["phase_ladder"][3]["phase_docs"]
    )
    assert any("Web UI" in item for item in payload["remaining_gaps"])
    assert any("官网提交" in item for item in payload["remaining_gaps"])
    assert any("OPL stage-led framework" in item for item in maintainer_references["explicitly_not_now"])
    assert any("官网提交" in item for item in maintainer_references["explicitly_not_now"])
    assert any("product-entry-manifest" in item for item in payload["current_focus"]["focus_items"])
    assert any("family product-entry manifest v2" in item for item in payload["current_focus"]["focus_items"])


def test_mainline_status_cli_json_exposes_structured_contract_surface() -> None:
    payload = run_json_cli("mainline-status", "--format", "json")

    assert payload["schema_version"] == 1
    assert payload["program_id"] == "med-autogrant-mainline"
    assert payload["current_line"]["current_owner_line"]
    assert payload["current_focus"]["summary"]
    assert payload["current_focus"]["focus_items"]
    assert payload["completed_records"]
    assert payload["remaining_gaps"]
    assert payload["maintainer_references"]["runtime_owner"]["active_phase"]
    assert payload["maintainer_references"]["current_record_detail"]["phase_id"] == "P4"


def test_mainline_phase_status_resolves_current_and_next_phase() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    current_payload = module.read_mainline_phase_status("current")
    next_payload = module.read_mainline_phase_status("next")

    assert current_payload["maintainer_reference"]["record_detail"]["phase_id"] == "P4"
    assert current_payload["maintainer_reference"]["record_detail"]["status"] == "next"
    assert any(
        item["name"] == "mainline_status"
        for item in current_payload["maintainer_reference"]["record_detail"]["entry_points"]
    )
    assert next_payload["maintainer_reference"]["record_detail"]["phase_id"] == "P4"
    assert any(
        item["command"]
        == public_cli_command(
            "grant-user-loop",
            "--input",
            "<workspace-path>",
            "--task-intent",
            "<task-intent>",
            "--format",
            "json",
        )
        for item in next_payload["maintainer_reference"]["record_detail"]["entry_points"]
    )
    assert any(
        item["command"]
        == public_cli_command(
            "build-submission-ready-package",
            "--input",
            "<workspace-path>",
            "--output-dir",
            "<submission-ready-output-dir>",
            "--format",
            "json",
        )
        for item in next_payload["maintainer_reference"]["record_detail"]["entry_points"]
    )


def test_mainline_phase_cli_json_exposes_entry_points_and_exit_criteria() -> None:
    payload = run_json_cli("mainline-phase", "--phase", "P4", "--format", "json")
    record_detail = payload["maintainer_reference"]["record_detail"]

    assert payload["schema_version"] == 1
    assert payload["program_id"] == "med-autogrant-mainline"
    assert record_detail["phase_id"] == "P4"
    assert record_detail["phase_name"]
    assert record_detail["status"] == "next"
    assert record_detail["entry_points"]
    assert record_detail["exit_criteria"]
