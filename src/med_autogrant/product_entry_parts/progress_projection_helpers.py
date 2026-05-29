from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _optional_mapping,
    _optional_string_from_mapping,
    _read_nonempty_string_list,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)


def _read_blocking_issues(critique_summary: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(critique_summary, Mapping):
        return []
    blocking_issues = critique_summary.get("blocking_issues")
    if not isinstance(blocking_issues, list):
        return []
    return [item for item in blocking_issues if isinstance(item, str) and item.strip()]


def _read_projection_blockers(
    *,
    workspace_summary: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> list[str]:
    critique_blockers = _read_blocking_issues(critique_summary)
    if critique_blockers:
        return critique_blockers

    blockers: list[str] = []
    intake_audit = _optional_mapping(workspace_summary, "grant_intake_audit")
    evidence_grounding = _optional_mapping(workspace_summary, "grant_evidence_grounding")
    if isinstance(intake_audit, Mapping):
        blockers.extend(_read_nonempty_string_list(intake_audit.get("blocking_gaps"), context="grant_intake_audit"))
    if isinstance(evidence_grounding, Mapping):
        blockers.extend(
            _read_nonempty_string_list(
                evidence_grounding.get("evidence_gaps"),
                context="grant_evidence_grounding",
            )
        )
    seen: set[str] = set()
    ordered: list[str] = []
    for blocker in blockers:
        if blocker not in seen:
            seen.add(blocker)
            ordered.append(blocker)
    return ordered


def _read_next_system_action(next_step: Mapping[str, Any]) -> str:
    actions = next_step.get("actions")
    if isinstance(actions, list):
        for item in actions:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return _require_nonempty_string_from_mapping(
        next_step,
        "reason",
        context="stage-route-report.route.next_step",
    )


def _build_current_stage_summary(
    *,
    lifecycle_stage: str,
    checkpoint_status: str,
    next_step: Mapping[str, Any],
) -> str:
    if lifecycle_stage == "frozen" and checkpoint_status == "submission_frozen":
        reason = "送审前冻结 gate 已闭合，可保持当前阶段继续推进。"
    else:
        reason = _require_nonempty_string_from_mapping(
            next_step,
            "reason",
            context="stage-route-report.route.next_step",
        )
    return f"当前 grant 已进入 {lifecycle_stage} 阶段；{reason}"


def _build_author_decision_summary(next_step: Mapping[str, Any]) -> str | None:
    if not bool(next_step.get("requires_human_confirmation")):
        return None
    return _require_nonempty_string_from_mapping(
        next_step,
        "reason",
        context="stage-route-report.route.next_step",
    )


def _build_focus_payload(
    *,
    workspace_summary: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> dict[str, Any]:
    intake_snapshot = _require_mapping(
        workspace_summary,
        "intake_snapshot",
        context="summarize-workspace",
    )
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
        context="summarize-workspace",
    )
    selected_direction = _optional_mapping(workspace_summary, "selected_direction")
    selected_question = _optional_mapping(workspace_summary, "selected_question")
    active_draft = _optional_mapping(workspace_summary, "active_draft")
    active_critique = _optional_mapping(workspace_summary, "active_critique")
    critique_verdict = _optional_string_from_mapping(active_critique, "verdict")
    if isinstance(critique_summary, Mapping):
        critique_verdict = _optional_string_from_mapping(critique_summary, "verdict") or critique_verdict
    return {
        "applicant_name": _require_nonempty_string_from_mapping(
            intake_snapshot,
            "applicant_name",
            context="summarize-workspace.intake_snapshot",
        ),
        "funding_program": _require_nonempty_string_from_mapping(
            intake_snapshot,
            "funding_program",
            context="summarize-workspace.intake_snapshot",
        ),
        "project_profile_label": _require_nonempty_string_from_mapping(
            project_profile,
            "profile_label",
            context="summarize-workspace.project_profile",
        ),
        "template_label": _require_nonempty_string_from_mapping(
            project_profile,
            "template_label",
            context="summarize-workspace.project_profile",
        ),
        "critique_policy_id": _require_nonempty_string_from_mapping(
            project_profile,
            "critique_policy_id",
            context="summarize-workspace.project_profile",
        ),
        "selected_direction_title": _optional_string_from_mapping(selected_direction, "title"),
        "selected_question": _optional_string_from_mapping(selected_question, "core_question"),
        "active_draft_title": _optional_string_from_mapping(active_draft, "project_title"),
        "critique_verdict": critique_verdict,
    }


def _build_workspace_overview(
    *,
    workspace_summary: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> dict[str, Any]:
    focus = _build_focus_payload(
        workspace_summary=workspace_summary,
        critique_summary=critique_summary,
    )
    return {
        "applicant_name": focus["applicant_name"],
        "funding_program": focus["funding_program"],
        "project_profile_label": focus["project_profile_label"],
        "template_label": focus["template_label"],
        "critique_policy_id": focus["critique_policy_id"],
        "lifecycle_stage": _require_nonempty_string_from_mapping(
            progress_projection,
            "current_stage",
            context="grant-progress.progress_projection",
        ),
        "checkpoint_status": _require_nonempty_string_from_mapping(
            progress_projection,
            "checkpoint_status",
            context="grant-progress.progress_projection",
        ),
        "selected_direction_title": focus["selected_direction_title"],
        "selected_question": focus["selected_question"],
        "active_draft_title": focus["active_draft_title"],
        "critique_verdict": focus["critique_verdict"],
    }


def _build_workspace_status(*, blockers: list[str], needs_author_decision: bool) -> str:
    if blockers or needs_author_decision:
        return "attention_required"
    return "on_track"


def _build_progress_first_currentness_resolver(
    *,
    current_program_contract: Mapping[str, Any],
    route_report: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
    resolved_input_path: Any,
    progress_projection: Mapping[str, Any],
) -> dict[str, Any]:
    program_id = _require_nonempty_string_from_mapping(
        current_program_contract,
        "program_id",
        context="CURRENT_PROGRAM",
    )
    grant_run_id = _require_nonempty_string_from_mapping(
        route_report,
        "grant_run_id",
        context="stage-route-report",
    )
    workspace_id = _require_nonempty_string_from_mapping(
        route_report,
        "workspace_id",
        context="stage-route-report",
    )
    lifecycle_stage = _require_nonempty_string_from_mapping(
        route_report,
        "lifecycle_stage",
        context="stage-route-report",
    )
    return {
        "surface_kind": "mag_progress_first_currentness_resolver",
        "version": "mag-progress-currentness.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "current_program": {
            "program_id": program_id,
            "ref": "contracts/runtime-program/current-program.json",
            "default_task_runtime_owner": _runtime_owner_field(
                current_program_contract,
                "default_task_runtime_owner",
            ),
            "default_runtime_substrate": _runtime_owner_field(
                current_program_contract,
                "default_runtime_substrate",
            ),
            "default_stage_executor": _runtime_owner_field(
                current_program_contract,
                "default_stage_executor",
            ),
        },
        "workspace_truth": {
            "workspace_path": str(resolved_input_path),
            "workspace_id": workspace_id,
            "grant_run_id": grant_run_id,
            "lifecycle_stage": lifecycle_stage,
            "checkpoint_status": _require_nonempty_string_from_mapping(
                progress_projection,
                "checkpoint_status",
                context="grant-progress.progress_projection",
            ),
            "summary_source": "summarize-workspace",
        },
        "last_receipt_or_blocker": {
            "owner": TARGET_DOMAIN_ID,
            "ref": f"receipt:mag/grant-stage-controlled-attempt/{lifecycle_stage}/owner-receipt-or-typed-blocker",
            "required_return_shapes": [
                "domain_owner_receipt_ref",
                "typed_blocker_ref",
                "no_regression_evidence_ref",
            ],
            "source_ref": (
                "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
                "grant_stage_controlled_attempt_closeout"
            ),
            "body_free_payload_required": True,
        },
        "stage_refs": {
            "stage_control_plane_ref": "/product_entry_manifest/family_stage_control_plane",
            "current_stage": lifecycle_stage,
            "recommended_next_stage": _require_nonempty_string_from_mapping(
                progress_projection,
                "recommended_next_stage",
                context="grant-progress.progress_projection",
            ),
            "domain_stage_refs": _domain_stage_refs_for_lifecycle_stage(lifecycle_stage),
        },
        "manifest_refs": {
            "progress_projection_ref": "/product_entry_manifest/progress_projection",
            "product_entry_manifest_ref": "/product_entry_manifest",
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "runtime_control_ref": "/product_entry_manifest/runtime_control",
        },
        "authority_boundary": {
            "resolver_role": "refs_only_currentness_projection",
            "workspace_body_read": True,
            "grant_truth_owner": TARGET_DOMAIN_ID,
            "can_write_grant_truth": False,
            "can_write_runtime_state": False,
        },
    }


def _build_opl_progress_delta_mapping(
    *,
    progress_projection: Mapping[str, Any],
) -> dict[str, Any]:
    current_stage = _require_nonempty_string_from_mapping(
        progress_projection,
        "current_stage",
        context="grant-progress.progress_projection",
    )
    recommended_next_stage = _require_nonempty_string_from_mapping(
        progress_projection,
        "recommended_next_stage",
        context="grant-progress.progress_projection",
    )
    return {
        "surface_kind": "opl_progress_first_delta_mapping",
        "version": "mag-progress-first-delta.v1",
        "progress_delta_classification": "mixed",
        "deliverable_progress_delta": {
            "count": 1,
            "refs": [
                "/progress_projection/current_stage_summary",
                "/progress_projection/focus",
                "/progress_projection/next_system_action",
            ],
            "domain_alias": "grant_work_progress",
            "current_stage": current_stage,
            "recommended_next_stage": recommended_next_stage,
            "changed_surfaces": [
                "/progress_projection/current_stage_summary",
                "/progress_projection/focus",
                "/progress_projection/next_system_action",
            ],
        },
        "platform_repair_delta": {
            "count": 1,
            "refs": [
                "/progress_projection/currentness_resolver/last_receipt_or_blocker",
                "/progress_projection/currentness_resolver/stage_refs",
                "/progress_projection/currentness_resolver/manifest_refs",
            ],
            "domain_alias": "platform_evidence_progress",
            "evidence_surfaces": [
                "/progress_projection/currentness_resolver/last_receipt_or_blocker",
                "/progress_projection/currentness_resolver/stage_refs",
                "/progress_projection/currentness_resolver/manifest_refs",
            ],
        },
        "grant_work_progress": {
            "maps_to": "opl_deliverable_delta",
            "owner": TARGET_DOMAIN_ID,
            "current_stage": current_stage,
            "recommended_next_stage": recommended_next_stage,
            "changed_surfaces": [
                "/progress_projection/current_stage_summary",
                "/progress_projection/focus",
                "/progress_projection/next_system_action",
            ],
            "can_claim_grant_ready": False,
            "can_claim_submission_ready": False,
        },
        "platform_evidence_progress": {
            "maps_to": "opl_platform_delta",
            "owner": "one-person-lab",
            "evidence_surfaces": [
                "/progress_projection/currentness_resolver/last_receipt_or_blocker",
                "/progress_projection/currentness_resolver/stage_refs",
                "/progress_projection/currentness_resolver/manifest_refs",
            ],
            "can_claim_grant_ready": False,
            "can_claim_fundability_ready": False,
            "can_claim_export_ready": False,
        },
    }


def _runtime_owner_field(current_program_contract: Mapping[str, Any], field_name: str) -> str:
    runtime_owner = _require_mapping(
        current_program_contract,
        "runtime_owner",
        context="CURRENT_PROGRAM",
    )
    return _require_nonempty_string_from_mapping(
        runtime_owner,
        field_name,
        context="CURRENT_PROGRAM.runtime_owner",
    )


def _domain_stage_refs_for_lifecycle_stage(lifecycle_stage: str) -> list[str]:
    if lifecycle_stage in {"input_intake", "direction_screening"}:
        return ["discover-funding-opportunities", "select-project-profile", "initialize-intake-workspace", "input_intake"]
    if lifecycle_stage in {"question_refinement", "argument_building", "fit_alignment", "outline"}:
        return ["question_refinement", "argument_building", "outline"]
    if lifecycle_stage in {"drafting", "revision"}:
        return ["drafting", "revision", "grant-progress", "grant-user-loop"]
    if lifecycle_stage == "critique":
        return ["critique", "review", "grant_quality_closure_dossier", "quality-diff"]
    if lifecycle_stage == "frozen":
        return ["freeze", "frozen", "package submission-ready", "submission-ready export gate"]
    return [lifecycle_stage]


__all__ = [name for name in globals() if not name.startswith("__")]
