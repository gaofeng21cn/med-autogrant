from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch

import med_autogrant.cli as cli
from med_autogrant.cli_rendering import _render_text as public_render_text
from med_autogrant.cli_rendering_parts import _TEXT_RENDERERS, _render_text as parts_render_text
from med_autogrant.grant_autonomy_request import validate_grant_autonomy_request
from med_autogrant.domain_runtime_parts.patch_targets import resolve_runtime_patch_target
from med_autogrant.product_entry_parts.domain_entry_loader import build_default_domain_entry
from med_autogrant.workspace_stage_validation import _find_active_draft, _validate_active_draft_sections


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


def test_runtime_patch_target_resolver_uses_current_mag_ledger_facade_when_loaded() -> None:
    sentinel = object()
    with patch("med_autogrant.domain_runtime.MagGrantRunLedger", sentinel, create=True):
        assert resolve_runtime_patch_target("MagGrantRunLedger", object()) is sentinel


def test_runtime_patch_target_resolver_ignores_retired_runtime_facade_module() -> None:
    default = object()
    retired_only_target = object()
    retired_name = "med_autogrant." + "hermes" + "_runtime"
    with patch.dict(sys.modules, {retired_name: SimpleNamespace(RetiredOnlyTarget=retired_only_target)}):
        assert resolve_runtime_patch_target("RetiredOnlyTarget", default) is default


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
