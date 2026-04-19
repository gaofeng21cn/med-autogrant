from __future__ import annotations

import importlib

from med_autogrant.public_cli import public_cli_command


def test_mainline_status_projects_line_focus_records_and_maintainer_references() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    payload = module.read_mainline_status()

    assert payload["program_id"] == "med-autogrant-mainline"
    assert payload["current_line"]["current_owner_line"] == "CLI-first with real upstream Hermes-Agent runtime substrate"
    assert payload["current_focus"]["summary"]
    assert payload["current_focus"]["focus_items"]
    assert payload["ideal_target"]["family_top_entry"] == "OPL Gateway"
    assert payload["ideal_target"]["domain_direct_entry"] == "Med Auto Grant Product Entry"
    assert any(item["record_id"] == "P4.B" for item in payload["completed_records"])
    assert any(item["record_id"] == "P4.C" for item in payload["completed_records"])
    assert any(item["record_id"] == "P4.E" for item in payload["completed_records"])
    assert any(item["record_id"] == "P4.F" for item in payload["completed_records"])
    maintainer_references = payload["maintainer_references"]
    assert maintainer_references["runtime_owner"]["active_phase"] == "P4 mature direct grant product entry"
    assert maintainer_references["runtime_owner"]["active_tranche"] == "P4.F local submission-ready package landing"
    assert maintainer_references["current_record_detail"]["phase_id"] == "P4"
    assert maintainer_references["current_record_detail"]["status"] == "next"
    assert len(maintainer_references["phase_ladder"]) == 4
    assert maintainer_references["phase_ladder"][0]["phase_id"] == "P1"
    assert maintainer_references["phase_ladder"][3]["phase_id"] == "P4"
    assert any(item["name"] == "grant_user_loop" for item in maintainer_references["phase_ladder"][3]["entry_points"])
    assert any(
        item.endswith("2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md")
        for item in maintainer_references["phase_ladder"][3]["phase_docs"]
    )
    assert any(
        item.endswith("2026-04-13-p4e-schema-backed-frontdesk-and-manifest-current-truth.md")
        for item in maintainer_references["phase_ladder"][3]["phase_docs"]
    )
    assert any(
        item.endswith("2026-04-13-p4f-local-submission-ready-package-current-truth.md")
        for item in maintainer_references["phase_ladder"][3]["phase_docs"]
    )
    assert any("Web UI" in item for item in payload["remaining_gaps"])
    assert any("官网提交" in item for item in payload["remaining_gaps"])
    assert any("OPL Gateway" in item for item in maintainer_references["explicitly_not_now"])
    assert any("官网提交" in item for item in maintainer_references["explicitly_not_now"])
    assert any("product-entry-manifest" in item for item in payload["current_focus"]["focus_items"])
    assert any("family product-entry manifest v2" in item for item in payload["current_focus"]["focus_items"])


def test_render_mainline_status_markdown_surfaces_line_focus_records_and_references() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    markdown = module.render_mainline_status_markdown(module.read_mainline_status())

    assert "# Mainline Status" in markdown
    assert "- 当前 program:" in markdown
    assert "- 当前 line:" in markdown
    assert "- 当前 focus:" in markdown
    assert "P4" in markdown
    assert "Ideal Target" in markdown
    assert "Current Focus Items" in markdown
    assert "Completed Records" in markdown
    assert "Remaining Gaps" in markdown
    assert "Maintainer References" in markdown
    assert "program_id:" not in markdown


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


def test_render_mainline_phase_markdown_surfaces_entry_points_and_exit_criteria() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    markdown = module.render_mainline_phase_markdown(module.read_mainline_phase_status("P4"))

    assert "# Mainline Maintainer Reference" in markdown
    assert "- 维护参考记录:" in markdown
    assert "- 记录名称:" in markdown
    assert "- 记录状态:" in markdown
    assert "- 当前摘要:" in markdown
    assert "P4" in markdown
    assert "Entry Points" in markdown
    assert "Exit Criteria" in markdown
    assert "phase_id:" not in markdown
    assert "phase_name:" not in markdown
    assert "status:" not in markdown
    assert "summary:" not in markdown
