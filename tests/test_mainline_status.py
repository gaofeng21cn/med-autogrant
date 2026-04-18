from __future__ import annotations

import importlib

from med_autogrant.public_cli import public_cli_command


def test_mainline_status_projects_ideal_target_phase_ladder_and_remaining_gaps() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    payload = module.read_mainline_status()

    assert payload["program_id"] == "med-autogrant-mainline"
    assert payload["current_runtime_owner"]["active_phase"] == "P4 mature direct grant product entry"
    assert (
        payload["current_runtime_owner"]["active_tranche"]
        == "P4.F local submission-ready package landing"
    )
    assert payload["ideal_target"]["family_top_entry"] == "OPL Gateway"
    assert payload["ideal_target"]["domain_direct_entry"] == "Med Auto Grant Product Entry"
    assert payload["current_phase"]["phase_id"] == "P4"
    assert payload["current_phase"]["status"] == "next"
    assert len(payload["phase_ladder"]) == 4
    assert payload["phase_ladder"][0]["phase_id"] == "P1"
    assert payload["phase_ladder"][3]["phase_id"] == "P4"
    assert any(item["name"] == "grant_user_loop" for item in payload["phase_ladder"][3]["entry_points"])
    assert any(item["tranche_id"] == "P4.B" for item in payload["completed_tranches"])
    assert any(item["tranche_id"] == "P4.C" for item in payload["completed_tranches"])
    assert any(item["tranche_id"] == "P4.E" for item in payload["completed_tranches"])
    assert any(item["tranche_id"] == "P4.F" for item in payload["completed_tranches"])
    assert any(
        item.endswith("2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md")
        for item in payload["phase_ladder"][3]["phase_docs"]
    )
    assert any(
        item.endswith("2026-04-13-p4e-schema-backed-frontdesk-and-manifest-current-truth.md")
        for item in payload["phase_ladder"][3]["phase_docs"]
    )
    assert any(
        item.endswith("2026-04-13-p4f-local-submission-ready-package-current-truth.md")
        for item in payload["phase_ladder"][3]["phase_docs"]
    )
    assert any("Web UI" in item for item in payload["remaining_gaps"])
    assert any("官网提交" in item for item in payload["remaining_gaps"])
    assert any("OPL Gateway" in item for item in payload["explicitly_not_now"])
    assert any("官网提交" in item for item in payload["explicitly_not_now"])
    assert any("product-entry-manifest" in item for item in payload["next_focus"])
    assert any("family product-entry manifest v2" in item for item in payload["next_focus"])


def test_render_mainline_status_markdown_surfaces_phase_ladder_and_next_focus() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    markdown = module.render_mainline_status_markdown(module.read_mainline_status())

    assert "# Mainline Status" in markdown
    assert "P4" in markdown
    assert "Ideal Target" in markdown
    assert "Phase Ladder" in markdown
    assert "Completed Tranches" in markdown
    assert "Remaining Gaps" in markdown
    assert "Next Focus" in markdown


def test_mainline_phase_status_resolves_current_and_next_phase() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    current_payload = module.read_mainline_phase_status("current")
    next_payload = module.read_mainline_phase_status("next")

    assert current_payload["phase"]["phase_id"] == "P4"
    assert current_payload["phase"]["status"] == "next"
    assert any(item["name"] == "mainline_status" for item in current_payload["phase"]["entry_points"])
    assert next_payload["phase"]["phase_id"] == "P4"
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
        for item in next_payload["phase"]["entry_points"]
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
        for item in next_payload["phase"]["entry_points"]
    )


def test_render_mainline_phase_markdown_surfaces_entry_points_and_exit_criteria() -> None:
    module = importlib.import_module("med_autogrant.mainline_status")

    markdown = module.render_mainline_phase_markdown(module.read_mainline_phase_status("P4"))

    assert "# Mainline Phase" in markdown
    assert "P4" in markdown
    assert "Entry Points" in markdown
    assert "Exit Criteria" in markdown
