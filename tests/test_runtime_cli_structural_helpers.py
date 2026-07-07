from __future__ import annotations

import sys
from pathlib import Path

import med_autogrant.cli as cli
import med_autogrant.hosted_contract_bundle as hosted_contract_bundle
from med_autogrant.domain_runtime_parts.shared import (
    DOMAIN_AUTHORITY_SURFACE_REF,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
)
from med_autogrant.grant_autonomy_request import validate_grant_autonomy_request
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


def test_hosted_contract_bundle_exports_runtime_shared_surface_refs() -> None:
    assert hosted_contract_bundle.DOMAIN_AUTHORITY_SURFACE_REF == DOMAIN_AUTHORITY_SURFACE_REF
    assert (
        hosted_contract_bundle.GENERATED_SESSION_RESUME_SURFACE_REF
        == GENERATED_SESSION_RESUME_SURFACE_REF
    )
    assert hosted_contract_bundle.GENERATED_SESSION_SURFACE_REF == GENERATED_SESSION_SURFACE_REF


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
