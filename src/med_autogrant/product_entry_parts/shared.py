from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from med_autogrant.control_plane import read_program_id, resolve_runtime_state_root
from med_autogrant.domain_entry_contract import (
    build_domain_entry_contract,
    build_gateway_interaction_contract,
    build_shared_handoff,
)
from med_autogrant.product_entry_parts.runtime_contracts import (
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_DIRECT_ENTRY_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    GRANT_USER_LOOP_SCHEMA_FILE,
    PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    PRODUCT_FRONTDESK_SCHEMA_FILE,
    _build_author_side_route_contract,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.public_cli import public_cli_command, public_command_label
from med_autogrant.workspace import (
    WorkspaceFileError,
    WorkspaceStateError,
    load_workspace_document,
    validate_workspace_document,
)

from opl_harness_shared.managed_runtime import build_managed_runtime_contract as _build_shared_managed_runtime_contract
from opl_harness_shared.family_orchestration import (
    buildFamilyIntakeEvidenceCompanion as _build_shared_family_intake_evidence_companion,
    build_family_product_entry_orchestration as _build_shared_family_product_entry_orchestration,
)
from opl_harness_shared.automation_companions import (
    build_automation_catalog as _build_shared_automation_catalog,
    build_automation_descriptor as _build_shared_automation_descriptor,
)
from opl_harness_shared.product_entry_companions import (
    build_family_product_frontdesk_from_manifest as _build_shared_family_product_frontdesk_from_manifest,
    build_family_product_entry_manifest as _build_shared_family_product_entry_manifest,
    build_operator_loop_action_catalog as _build_shared_operator_loop_action_catalog,
    build_product_entry_start as _build_shared_product_entry_start,
    build_product_entry_overview as _build_shared_product_entry_overview,
    build_product_entry_quickstart as _build_shared_product_entry_quickstart,
    build_product_entry_readiness as _build_shared_product_entry_readiness,
    build_product_entry_resume_surface as _build_shared_product_entry_resume_surface,
    build_product_entry_shell_catalog as _build_shared_product_entry_shell_catalog,
    build_product_entry_shell_linked_surface as _build_shared_product_entry_shell_linked_surface,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
    validate_family_product_frontdesk as _validate_shared_family_product_frontdesk,
    validate_family_product_entry_manifest as _validate_shared_family_product_entry_manifest,
)
from opl_harness_shared.product_entry_program_companions import (
    build_detailed_readiness as _build_shared_detailed_readiness,
    build_product_entry_preflight as _build_shared_product_entry_preflight,
    build_workflow_coverage_item as _build_shared_workflow_coverage_item,
)
from opl_harness_shared.runtime_task_companions import (
    build_runtime_inventory as _build_shared_runtime_inventory,
    build_task_lifecycle as _build_shared_task_lifecycle,
)
from opl_harness_shared.status_narration import (
    PROGRESS_ANSWER_CHECKLIST,
    build_status_narration_contract,
)
from opl_harness_shared.skill_catalog import (
    build_skill_catalog as _build_shared_skill_catalog,
    build_skill_descriptor as _build_shared_skill_descriptor,
)


PRODUCT_ENTRY_VERSION = 1
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
PRODUCT_ENTRY_MANIFEST_KIND = "med_auto_grant_product_entry_manifest"
PRODUCT_FRONTDESK_KIND = "product_frontdesk"
TARGET_DOMAIN_ID = "med-autogrant"
SUPPORTED_ENTRY_MODES = ("direct", "opl-handoff")
GRANT_PROGRESS_PROJECTION_VERSION = 1
GRANT_PROGRESS_PROJECTION_KIND = "grant_progress"
GRANT_COCKPIT_KIND = "grant_cockpit"
GRANT_DIRECT_ENTRY_VERSION = 1
GRANT_DIRECT_ENTRY_KIND = "grant_direct_entry"
GRANT_USER_LOOP_VERSION = 1
GRANT_USER_LOOP_KIND = "grant_user_loop"
REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}


def _build_managed_runtime_contract() -> dict[str, Any]:
    return _build_shared_managed_runtime_contract(
        domain_owner=TARGET_DOMAIN_ID,
        executor_owner="med-autogrant",
        supervision_status_surface=GRANT_PROGRESS_PROJECTION_KIND,
        attention_queue_surface=GRANT_USER_LOOP_KIND,
        recovery_contract_surface=GRANT_USER_LOOP_KIND,
    )


def _build_product_entry_start(
    *,
    product_frontdesk_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
) -> dict[str, Any]:
    return _build_shared_product_entry_start(
        summary=(
            "先进入 direct grant frontdesk；需要继续当前写作主线时恢复 grant user loop，"
            "需要把用户意图显式装配成入口合同时再构建 direct entry。"
        ),
        recommended_mode_id="open_frontdesk",
        modes=[
            {
                "mode_id": "open_frontdesk",
                "title": "Open grant frontdesk",
                "command": product_frontdesk_command,
                "surface_kind": PRODUCT_FRONTDESK_KIND,
                "summary": "打开当前 direct grant frontdoor。",
                "requires": [],
            },
            {
                "mode_id": "continue_grant_loop",
                "title": "Continue current grant loop",
                "command": grant_user_loop_command,
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": _require_nonempty_string_from_mapping(
                    operator_loop_actions["open_loop"],
                    "summary",
                    context="operator_loop_actions.open_loop",
                ),
                "requires": ["task_intent"],
            },
            {
                "mode_id": "build_direct_entry",
                "title": "Build direct entry",
                "command": grant_direct_entry_command,
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                "summary": _require_nonempty_string_from_mapping(
                    operator_loop_actions["build_direct_entry"],
                    "summary",
                    context="operator_loop_actions.build_direct_entry",
                ),
                "requires": list(
                    _require_mapping(
                        operator_loop_actions,
                        "build_direct_entry",
                        context="operator_loop_actions",
                    ).get("requires")
                    or []
                ),
            },
        ],
        resume_surface=dict(
            _require_mapping(
                family_orchestration,
                "resume_contract",
                context="family_orchestration",
            )
        ),
        human_gate_ids=_collect_family_human_gate_ids(family_orchestration),
    )





def _read_funding_call_from_summary(summary: Mapping[str, Any]) -> str:
    intake_snapshot = _require_mapping(summary, "intake_snapshot", context="summarize-workspace")
    return _require_nonempty_string_from_mapping(
        intake_snapshot,
        "funding_program",
        context="summarize-workspace.intake_snapshot",
    )


def _require_entry_mode(entry_mode: str) -> str:
    resolved_entry_mode = _require_nonempty_string(entry_mode, field_name="entry_mode")
    if resolved_entry_mode not in SUPPORTED_ENTRY_MODES:
        raise WorkspaceStateError(
            f"entry_mode 不支持: {resolved_entry_mode}。只允许 {', '.join(SUPPORTED_ENTRY_MODES)}。"
        )
    return resolved_entry_mode


def _require_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> Mapping[str, Any]:
    value = payload.get(field_name)
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field_name}")
    return value


def _require_nonempty_string_from_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> str:
    value = payload.get(field_name)
    return _require_nonempty_string(value, field_name=field_name, context=context)


def _require_nonempty_string(
    value: Any,
    *,
    field_name: str,
    context: str = "product entry",
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field_name}")
    return value.strip()


def _require_optional_string(value: Any, *, field_name: str) -> str | None:
    if value is None:
        return None
    return _require_nonempty_string(value, field_name=field_name)


def _optional_mapping(payload: Mapping[str, Any], field_name: str) -> Mapping[str, Any] | None:
    value = payload.get(field_name)
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"product entry 缺少合法字段: {field_name}")
    return value


def _optional_string_from_mapping(payload: Mapping[str, Any] | None, field_name: str) -> str | None:
    if not isinstance(payload, Mapping):
        return None
    value = payload.get(field_name)
    if value is None:
        return None
    return _require_nonempty_string(value, field_name=field_name)


def _read_nonempty_string_list(value: Any, *, context: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context} 缺少合法字段: workspace_alerts")
    return [item for item in value if isinstance(item, str) and item.strip()]


def _route_status_from_route_id(route_id: str) -> str:
    resolved_route_id = _require_nonempty_string(route_id, field_name="route_id")
    route_contract = _build_author_side_route_contract(
        resolved_route_id,
        source_stage=resolved_route_id,
    )
    return _require_nonempty_string_from_mapping(
        route_contract,
        "route_status",
        context="author_side_route_contract",
    )


def _build_family_orchestration_companion(
    *,
    current_route_id: str,
    recommended_route_id: str,
    recommended_route_status: str,
    needs_author_decision: bool,
    workspace_summary: Mapping[str, Any] | None = None,
    intake_evidence_companion: Mapping[str, Any] | None = None,
    project_profile_companion: Mapping[str, Any] | None = None,
    review_surface_ref: str,
    event_envelope_surface_ref: str,
    checkpoint_lineage_surface_ref: str,
    resume_surface_kind: str,
) -> dict[str, Any]:
    resolved_current_route_id = _require_nonempty_string(current_route_id, field_name="current_route_id")
    resolved_recommended_route_id = _require_nonempty_string(
        recommended_route_id,
        field_name="recommended_route_id",
    )
    resolved_review_surface_ref = _require_nonempty_string(
        review_surface_ref,
        field_name="review_surface_ref",
    )
    resolved_event_envelope_surface_ref = _require_nonempty_string(
        event_envelope_surface_ref,
        field_name="event_envelope_surface_ref",
    )
    resolved_checkpoint_lineage_surface_ref = _require_nonempty_string(
        checkpoint_lineage_surface_ref,
        field_name="checkpoint_lineage_surface_ref",
    )
    resolved_resume_surface_kind = _require_nonempty_string(
        resume_surface_kind,
        field_name="resume_surface_kind",
    )
    route_status = _require_nonempty_string(
        recommended_route_status,
        field_name="recommended_route_status",
    )
    if route_status not in {"landed", "pending"}:
        raise WorkspaceStateError("family_orchestration.recommended_route_status 只允许 landed 或 pending。")

    gate_status = "requested" if needs_author_decision or route_status == "pending" else "approved"
    gate_id = f"mag_route_gate_{resolved_recommended_route_id}"
    current_node_id = f"route:{resolved_current_route_id}"
    recommended_node_id = f"route:{resolved_recommended_route_id}"
    edge_on = "decision" if gate_status == "requested" else "success"
    resolved_intake_evidence_companion = (
        dict(intake_evidence_companion)
        if isinstance(intake_evidence_companion, Mapping)
        else _build_intake_evidence_companion(workspace_summary)
    )
    resolved_project_profile_companion = (
        dict(project_profile_companion)
        if isinstance(project_profile_companion, Mapping)
        else _build_project_profile_companion(workspace_summary)
    )
    payload = _build_shared_family_product_entry_orchestration(
        graph_id=f"mag_{resolved_current_route_id}_to_{resolved_recommended_route_id}_graph",
        target_domain_id=TARGET_DOMAIN_ID,
        graph_kind="grant_route_orchestration",
        graph_version="2026-04-13",
        nodes=[
            {
                "node_id": current_node_id,
                "node_kind": _route_to_action_node_kind(resolved_current_route_id),
                "title": f"Current route: {resolved_current_route_id}",
                "produces_checkpoint": True,
            },
            {
                "node_id": recommended_node_id,
                "node_kind": _route_to_action_node_kind(resolved_recommended_route_id),
                "title": f"Recommended route: {resolved_recommended_route_id}",
                "produces_checkpoint": True,
            },
        ],
        edges=[
            {
                "from": current_node_id,
                "to": recommended_node_id,
                "on": edge_on,
            }
        ],
        entry_nodes=[current_node_id],
        exit_nodes=[recommended_node_id],
        human_gates=[
            {
                "gate_id": gate_id,
                "trigger_nodes": [recommended_node_id],
                "blocking": gate_status == "requested",
            }
        ],
        checkpoint_nodes=[current_node_id, recommended_node_id],
        human_gate_previews=[
            {
                "gate_id": gate_id,
                "title": f"确认 {resolved_recommended_route_id} route 执行决策",
                "status": gate_status,
                "review_surface": {
                    "ref_kind": "json_pointer",
                    "ref": resolved_review_surface_ref,
                    "label": "route review surface",
                },
            }
        ],
        action_graph_ref={
            "ref_kind": "json_pointer",
            "ref": "/family_orchestration/action_graph",
            "label": "mag family action graph",
        },
        resume_surface_kind=resolved_resume_surface_kind,
        session_locator_field="grant_run_id",
        checkpoint_locator_field="lifecycle_stage",
        event_envelope_surface={
            "ref_kind": "json_pointer",
            "ref": resolved_event_envelope_surface_ref,
            "label": "family event envelope surface",
        },
        checkpoint_lineage_surface={
            "ref_kind": "json_pointer",
            "ref": resolved_checkpoint_lineage_surface_ref,
            "label": "family checkpoint lineage surface",
        },
        intake_evidence_companion=resolved_intake_evidence_companion,
    )
    if resolved_project_profile_companion is not None:
        payload["project_profile_companion"] = resolved_project_profile_companion
    return payload


def _route_to_action_node_kind(route_id: str) -> str:
    if route_id in {"critique", "revision", "frozen"}:
        return "review"
    if route_id in {"artifact_bundle", "final_package", "hosted_contract_bundle"}:
        return "publish"
    return "authoring"


def _write_product_entry_output(output_path: Path, product_entry: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(product_entry, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 product entry 输出失败: {output_path}") from exc


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


def _build_intake_evidence_companion(workspace_summary: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(workspace_summary, Mapping):
        return None
    intake_audit = _optional_mapping(workspace_summary, "grant_intake_audit")
    evidence_grounding = _optional_mapping(workspace_summary, "grant_evidence_grounding")
    intake_snapshot = _optional_mapping(workspace_summary, "intake_snapshot")
    if not isinstance(intake_audit, Mapping) or not isinstance(evidence_grounding, Mapping):
        return None
    trust_ranked_evidence = [
        entry
        for entry in evidence_grounding.get("trust_ranked_evidence", [])
        if isinstance(entry, Mapping)
    ]
    if not trust_ranked_evidence:
        return None

    workspace_id = _require_nonempty_string_from_mapping(
        workspace_summary,
        "workspace_id",
        context="summarize-workspace",
    )
    funding_program = (
        _require_nonempty_string_from_mapping(
            intake_snapshot,
            "funding_program",
            context="summarize-workspace.intake_snapshot",
        )
        if isinstance(intake_snapshot, Mapping)
        else _require_nonempty_string_from_mapping(
            evidence_grounding,
            "funding_program",
            context="grant_evidence_grounding",
        )
    )
    return _build_shared_family_intake_evidence_companion(
        target_domain_id=TARGET_DOMAIN_ID,
        intake_audit={
            "summary": _require_nonempty_string_from_mapping(
                intake_audit,
                "summary",
                context="grant_intake_audit",
            ),
            "verdict": _require_nonempty_string_from_mapping(
                intake_audit,
                "overall_readiness",
                context="grant_intake_audit",
            ),
            "summary_ref": {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::grant_intake_audit",
                "label": "grant intake audit",
            },
        },
        trust_ranked_evidence_refs=[
            {
                "ref_kind": _require_nonempty_string_from_mapping(
                    entry,
                    "ref_kind",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "ref": _require_nonempty_string_from_mapping(
                    entry,
                    "ref",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "label": _require_nonempty_string_from_mapping(
                    entry,
                    "label",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "trust_rank": int(entry["trust_rank"]),
                "trust_note": _optional_string_from_mapping(entry, "trust_note"),
                "supports": list(entry.get("supports") or []),
            }
            for entry in trust_ranked_evidence
        ],
        grounding_scope={
            "scope_kind": _require_nonempty_string_from_mapping(
                evidence_grounding,
                "scope_kind",
                context="grant_evidence_grounding",
            ),
            "summary": _require_nonempty_string_from_mapping(
                evidence_grounding,
                "summary",
                context="grant_evidence_grounding",
            ),
            "scope_refs": [
                {
                    "ref_kind": "workspace_locator",
                    "ref": f"grant_workspace::{workspace_id}::grant_evidence_grounding",
                    "label": "grant evidence grounding",
                },
                {
                    "ref_kind": "workspace_locator",
                    "ref": f"grant_workspace::{workspace_id}::funding_opportunity_brief::{funding_program}",
                    "label": "funding opportunity brief",
                },
            ],
        },
        human_gate_refs=[
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::family_human_gate",
                "label": "grant route gate",
            }
        ],
        checkpoint_lineage_refs=[
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::checkpoint_lineage",
                "label": "grant checkpoint lineage",
            }
        ],
    )


def _build_project_profile_companion(workspace_summary: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(workspace_summary, Mapping):
        return None
    workspace_id = _require_nonempty_string_from_mapping(
        workspace_summary,
        "workspace_id",
        context="summarize-workspace",
    )
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
        context="summarize-workspace",
    )
    profile_id = _require_nonempty_string_from_mapping(
        project_profile,
        "profile_id",
        context="summarize-workspace.project_profile",
    )
    funding_program = _require_nonempty_string_from_mapping(
        project_profile,
        "funding_program",
        context="summarize-workspace.project_profile",
    )
    return {
        "surface_kind": "project_profile_companion",
        "version": 1,
        "profile_id": profile_id,
        "preset_id": _require_nonempty_string_from_mapping(
            project_profile,
            "preset_id",
            context="summarize-workspace.project_profile",
        ),
        "profile_label": _require_nonempty_string_from_mapping(
            project_profile,
            "profile_label",
            context="summarize-workspace.project_profile",
        ),
        "funding_program": funding_program,
        "funder": _require_nonempty_string_from_mapping(
            project_profile,
            "funder",
            context="summarize-workspace.project_profile",
        ),
        "program_family": _require_nonempty_string_from_mapping(
            project_profile,
            "program_family",
            context="summarize-workspace.project_profile",
        ),
        "template_profile": {
            "template_id": _require_nonempty_string_from_mapping(
                project_profile,
                "template_id",
                context="summarize-workspace.project_profile",
            ),
            "template_label": _require_nonempty_string_from_mapping(
                project_profile,
                "template_label",
                context="summarize-workspace.project_profile",
            ),
        },
        "collaboration_preferences": {
            "collaboration_mode": _require_nonempty_string_from_mapping(
                project_profile,
                "collaboration_mode",
                context="summarize-workspace.project_profile",
            ),
            "author_touchpoints": list(project_profile.get("author_touchpoints") or []),
            "evidence_policy": _require_nonempty_string_from_mapping(
                project_profile,
                "evidence_policy",
                context="summarize-workspace.project_profile",
            ),
            "drafting_voice": _require_nonempty_string_from_mapping(
                project_profile,
                "drafting_voice",
                context="summarize-workspace.project_profile",
            ),
        },
        "critique_policy": {
            "preset_id": _require_nonempty_string_from_mapping(
                project_profile,
                "critique_policy_preset_id",
                context="summarize-workspace.project_profile",
            ),
            "policy_id": _require_nonempty_string_from_mapping(
                project_profile,
                "critique_policy_id",
                context="summarize-workspace.project_profile",
            ),
        },
        "profile_ref": {
            "ref_kind": "workspace_locator",
            "ref": f"grant_workspace::{workspace_id}::project_profile::{profile_id}",
            "label": "project profile",
        },
        "funding_opportunity_ref": {
            "ref_kind": "workspace_locator",
            "ref": f"grant_workspace::{workspace_id}::funding_opportunity_brief::{funding_program}",
            "label": "funding opportunity brief",
        },
    }


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


def _require_matching_top_level_identity(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    *,
    context: str,
) -> None:
    for field_name in ("grant_run_id", "workspace_id", "draft_id", "lifecycle_stage", "input_path"):
        if left.get(field_name) != right.get(field_name):
            raise WorkspaceStateError(f"{context} 与当前 direct entry identity 不一致: {field_name}")


def _assert_entry_mode(
    payload: Mapping[str, Any],
    *,
    expected_entry_mode: str,
    context: str,
) -> None:
    resolved_entry_mode = _require_nonempty_string_from_mapping(
        payload,
        "entry_mode",
        context=context,
    )
    if resolved_entry_mode != expected_entry_mode:
        raise WorkspaceStateError(f"{context}.entry_mode 必须为 {expected_entry_mode}。")









































__all__ = [name for name in globals() if not name.startswith("__")]
