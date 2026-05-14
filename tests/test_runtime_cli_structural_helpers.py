from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import med_autogrant.cli as cli
import med_autogrant.domain_runtime_parts.runtime_ops as runtime_ops
from med_autogrant.cli_rendering import _render_text as public_render_text
from med_autogrant.cli_rendering_parts import _TEXT_RENDERERS, _render_text as parts_render_text
from med_autogrant.grant_autonomy_request import validate_grant_autonomy_request
from med_autogrant.product_entry_parts.domain_entry_loader import build_default_domain_entry
from med_autogrant.workspace_stage_validation import _find_active_draft, _validate_active_draft_sections


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"


def _valid_autonomy_request() -> dict[str, object]:
    return {
        "request_id": "autonomy-req-structure",
        "start": {
            "mode": "workspace",
            "workspace": {
                "workspace_id": "ws-structure",
                "lifecycle_stage": "critique",
            },
        },
        "goal": {
            "target_status": "near_submission_candidate",
            "summary": "maintain near-submission trajectory",
        },
        "max_rounds_or_cycles": 2,
        "budget": {"max_total_steps": 5},
        "stop_conditions": {
            "require_zero_blockers": True,
            "require_zero_evidence_gaps": True,
        },
        "blocker_queue": [],
        "evidence_gap_queue": [],
        "reselection_policy": {
            "enabled": True,
            "max_reselections": -2,
        },
        "rollback_policy": {
            "enabled": True,
            "max_rollbacks": "invalid",
        },
    }


def test_grant_autonomy_request_validator_sanitizes_policy_counts() -> None:
    state = validate_grant_autonomy_request(_valid_autonomy_request())

    assert state["ok"] is True
    assert state["max_reselections"] == 0
    assert state["max_rollbacks"] == 0
    assert state["start_mode"] == "workspace"
    assert state["goal_target"] == "near_submission_candidate"


def test_grant_autonomy_request_validator_fail_closes_invalid_budget() -> None:
    request = _valid_autonomy_request()
    request["budget"] = {"max_total_steps": 0}

    state = validate_grant_autonomy_request(request)

    assert state["ok"] is False
    assert state["report"]["controller_status"] == "failed_closed"
    assert state["report"]["termination_reason"] == "invalid_budget"


def test_cli_rendering_preserves_public_render_text_export() -> None:
    assert public_render_text is parts_render_text
    assert _TEXT_RENDERERS["validate-workspace"] is not parts_render_text

    rendered = public_render_text(
        "validate-workspace",
        {
            "grant_run_id": "grant-structure",
            "workspace_id": "ws-structure",
            "lifecycle_stage": "critique",
            "ok": False,
            "error_count": 1,
            "errors": [{"path": "drafts.0", "message": "missing section"}],
        },
    )

    assert "当前 grant run: grant-structure" in rendered
    assert "当前 workspace: ws-structure" in rendered
    assert "- drafts.0: missing section" in rendered


def test_cli_module_does_not_hold_entry_classes_as_patch_surfaces() -> None:
    assert not hasattr(cli, "MedAutoGrantDomainEntry")
    assert not hasattr(cli, "MedAutoGrantProductEntry")


def test_domain_runtime_parts_do_not_depend_on_facade_patch_bridge() -> None:
    runtime_parts_root = SRC_ROOT / "med_autogrant" / "domain_runtime_parts"
    offenders = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in sorted(runtime_parts_root.glob("*.py"))
        if "resolve_runtime_patch_target" in path.read_text(encoding="utf-8")
    ]

    assert offenders == []


def test_autonomy_quality_evaluator_uses_owner_module_quality_builders() -> None:
    sentinel_scorecard = {
        "surface_kind": "grant_quality_scorecard",
        "overall_status": "submission_grade_candidate",
        "ai_reviewer_required": False,
        "unresolved_hard_issues": [],
        "tracked_issues": [],
        "dimensions": [],
        "evidence_supply_queue": [],
    }
    sentinel_dossier = {"surface_kind": "grant_quality_closure_dossier"}

    with patch.object(runtime_ops, "build_grant_quality_scorecard", return_value=sentinel_scorecard) as scorecard, patch.object(
        runtime_ops,
        "build_grant_quality_closure_dossier",
        return_value=sentinel_dossier,
    ) as dossier:
        payload = runtime_ops.build_autonomy_quality_evaluator_output({"workspace_id": "ws-structure"})

    assert payload["quality_status"] == "submission_grade_candidate"
    assert payload["blocker_report"] is sentinel_scorecard
    assert payload["quality_closure_dossier"] is sentinel_dossier
    scorecard.assert_called_once_with({"workspace_id": "ws-structure"})
    dossier.assert_called_once_with({"workspace_id": "ws-structure"})


def test_product_entry_default_domain_entry_loader_is_lazy() -> None:
    domain_entry = object()
    domain_entry_module = Mock()
    domain_entry_module.MedAutoGrantDomainEntry.return_value = domain_entry

    with patch(
        "med_autogrant.product_entry_parts.domain_entry_loader.import_module",
        return_value=domain_entry_module,
    ) as import_module:
        loaded = build_default_domain_entry()

    assert loaded is domain_entry
    import_module.assert_called_once_with("med_autogrant.domain_entry")


def test_workspace_stage_validation_helpers_keep_active_draft_lookup_and_section_errors() -> None:
    active_draft = {
        "draft_id": "draft-1",
        "sections": [{"linked_object_ids": ["question-1", "argument-1"]}],
    }
    document = {
        "current_selection": {"active_draft_id": "draft-1"},
        "application_drafts": [active_draft],
    }
    issues = []

    assert _find_active_draft(document, document["current_selection"]) is active_draft
    _validate_active_draft_sections(
        stage="drafting",
        active_draft=active_draft,
        selected_question_id="question-1",
        active_argument_chain_id="argument-1",
        active_fit_mapping_id="fit-1",
        issues=issues,
    )

    assert len(issues) == 1
    assert issues[0].path == "application_drafts.sections"
    assert "ApplicantFitMapping" in issues[0].message
