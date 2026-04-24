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
from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.hermes_runtime import (
    _build_author_side_route_contract,
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_DIRECT_ENTRY_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    GRANT_USER_LOOP_SCHEMA_FILE,
    PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    PRODUCT_FRONTDESK_SCHEMA_FILE,
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


def _validate_grant_direct_entry_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_contract_schema(
        payload,
        schema_file=GRANT_DIRECT_ENTRY_SCHEMA_FILE,
        context="grant_direct_entry",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    grant_direct_entry = _require_mapping(
        payload,
        "grant_direct_entry",
        context="grant_direct_entry",
    )
    direct_entry = _require_mapping(
        grant_direct_entry,
        "direct_entry",
        context="grant_direct_entry.direct_entry",
    )
    opl_handoff_entry = _require_mapping(
        grant_direct_entry,
        "opl_handoff_entry",
        context="grant_direct_entry.opl_handoff_entry",
    )
    if (
        _require_nonempty_string_from_mapping(
            direct_entry,
            "entry_mode",
            context="grant_direct_entry.direct_entry",
        )
        != "direct"
    ):
        raise WorkspaceStateError(
            "grant_direct_entry.direct_entry.entry_mode 必须为 direct。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            opl_handoff_entry,
            "entry_mode",
            context="grant_direct_entry.opl_handoff_entry",
        )
        != "opl-handoff"
    ):
        raise WorkspaceStateError(
            "grant_direct_entry.opl_handoff_entry.entry_mode 必须为 opl-handoff。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    direct_task_intent = _require_nonempty_string_from_mapping(
        direct_entry,
        "task_intent",
        context="grant_direct_entry.direct_entry",
    )
    opl_handoff_task_intent = _require_nonempty_string_from_mapping(
        opl_handoff_entry,
        "task_intent",
        context="grant_direct_entry.opl_handoff_entry",
    )
    task_intent = _require_nonempty_string_from_mapping(
        grant_direct_entry,
        "task_intent",
        context="grant_direct_entry",
    )
    if direct_task_intent != task_intent:
        raise WorkspaceStateError(
            "grant_direct_entry.direct_entry.task_intent 与顶层 direct entry contract 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_handoff_task_intent != task_intent:
        raise WorkspaceStateError(
            "grant_direct_entry.opl_handoff_entry.task_intent 与顶层 direct entry contract 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    current_stage_route = _require_mapping(
        grant_direct_entry,
        "current_stage_route",
        context="grant_direct_entry",
    )
    recommended_executor_route = _require_mapping(
        grant_direct_entry,
        "recommended_executor_route",
        context="grant_direct_entry",
    )
    direct_executor_routing_contract = _require_mapping(
        direct_entry,
        "executor_routing_contract",
        context="grant_direct_entry.direct_entry",
    )
    opl_executor_routing_contract = _require_mapping(
        opl_handoff_entry,
        "executor_routing_contract",
        context="grant_direct_entry.opl_handoff_entry",
    )
    if direct_executor_routing_contract.get("current_stage_route") != current_stage_route:
        raise WorkspaceStateError(
            "grant_direct_entry.current_stage_route 与 direct entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if direct_executor_routing_contract.get("recommended_executor_route") != recommended_executor_route:
        raise WorkspaceStateError(
            "grant_direct_entry.recommended_executor_route 与 direct entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_executor_routing_contract.get("current_stage_route") != current_stage_route:
        raise WorkspaceStateError(
            "grant_direct_entry.current_stage_route 与 opl_handoff entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_executor_routing_contract.get("recommended_executor_route") != recommended_executor_route:
        raise WorkspaceStateError(
            "grant_direct_entry.recommended_executor_route 与 opl_handoff entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    _validate_runtime_continuity_alignment(
        session_continuity=_require_mapping(
            payload,
            "session_continuity",
            context="grant_direct_entry",
        ),
        progress_surface=_require_mapping(
            payload,
            "progress_projection",
            context="grant_direct_entry",
        ),
        artifact_inventory=_require_mapping(
            payload,
            "artifact_inventory",
            context="grant_direct_entry",
        ),
        runtime_control=_require_mapping(
            payload,
            "runtime_control",
            context="grant_direct_entry",
        ),
        projection_truth=_require_mapping(
            grant_direct_entry,
            "progress_projection",
            context="grant_direct_entry",
        ),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        context_prefix="grant_direct_entry",
    )


def _build_mainline_snapshot(mainline_status: Mapping[str, Any]) -> dict[str, Any]:
    current_line = _require_mapping(
        mainline_status,
        "current_line",
        context="mainline_status",
    )
    current_focus = _require_mapping(
        mainline_status,
        "current_focus",
        context="mainline_status",
    )
    maintainer_references = _require_mapping(
        mainline_status,
        "maintainer_references",
        context="mainline_status",
    )
    current_runtime_owner = _require_mapping(
        maintainer_references,
        "runtime_owner",
        context="mainline_status.maintainer_references",
    )
    phase_ladder = maintainer_references.get("phase_ladder")
    if not isinstance(phase_ladder, list):
        raise WorkspaceStateError("mainline_status.maintainer_references.phase_ladder 必须为 list。")
    return {
        "current_owner_line": _require_nonempty_string_from_mapping(
            current_line,
            "current_owner_line",
            context="mainline_status.current_line",
        ),
        "active_phase": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_phase",
            context="mainline_status.maintainer_references.runtime_owner",
        ),
        "active_tranche": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_tranche",
            context="mainline_status.maintainer_references.runtime_owner",
        ),
        "phase_map": [
            {
                "phase_id": _require_nonempty_string_from_mapping(item, "phase_id", context="mainline_status.phase_ladder"),
                "phase_name": _require_nonempty_string_from_mapping(item, "phase_name", context="mainline_status.phase_ladder"),
                "status": _require_nonempty_string_from_mapping(item, "status", context="mainline_status.phase_ladder"),
            }
            for item in phase_ladder
            if isinstance(item, Mapping)
        ],
        "next_focus": _read_nonempty_string_list(
            current_focus.get("focus_items"),
            context="mainline_status.current_focus.focus_items",
        ),
        "remaining_gaps": _read_nonempty_string_list(
            mainline_status.get("remaining_gaps"),
            context="mainline_status.remaining_gaps",
        ),
    }


def _build_next_action_payload(
    *,
    recommended_executor_route: Mapping[str, Any],
    input_path: Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> dict[str, Any]:
    route_id = _require_nonempty_string_from_mapping(
        recommended_executor_route,
        "route_id",
        context="grant_user_loop.recommended_executor_route",
    )
    route_status = _require_nonempty_string_from_mapping(
        recommended_executor_route,
        "route_status",
        context="grant_user_loop.recommended_executor_route",
    )
    if route_status == "landed":
        return {
            "action_kind": "execute_landed_route",
            "route_id": route_id,
            "route_status": route_status,
            "summary": f"当前推荐 route {route_id} 已 landed，可直接调用现有 author-side executor surface。",
            "command": _build_route_execution_command(
                route_id=route_id,
                input_path=input_path,
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
            ),
            "handoff_surfaces": None,
        }

    raise WorkspaceStateError(
        f"grant_user_loop 只接受已 landed 的 route contract，收到 {route_id}({route_status})。",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=route_id,
    )


def _build_route_execution_command(
    *,
    route_id: str,
    input_path: Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> str:
    resolved_input_path = input_path.expanduser().resolve()
    output_path = _build_runtime_route_output_path(
        route_id=route_id,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
    )
    if route_id == "direction_screening":
        return public_cli_command(
            "execute-direction-screening-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "question_refinement":
        return public_cli_command(
            "execute-question-refinement-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "argument_building":
        return public_cli_command(
            "execute-argument-building-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "fit_alignment":
        return public_cli_command(
            "execute-fit-alignment-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "outline":
        return public_cli_command(
            "execute-outline-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "drafting":
        return public_cli_command(
            "execute-drafting-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "critique":
        return public_cli_command(
            "execute-critique-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "revision":
        return public_cli_command(
            "execute-revision-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "frozen":
        return public_cli_command(
            "execute-freeze-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "artifact_bundle":
        return public_cli_command(
            "build-artifact-bundle",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "final_package":
        artifact_bundle_path = _build_runtime_route_output_path(
            route_id="artifact_bundle",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            "build-final-package",
            "--input",
            str(resolved_input_path),
            "--artifact-bundle",
            str(artifact_bundle_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "hosted_contract_bundle":
        final_package_path = _build_runtime_route_output_path(
            route_id="final_package",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            "build-hosted-contract-bundle",
            "--final-package",
            str(final_package_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    raise WorkspaceStateError(f"grant_user_loop 不支持 landed route command: {route_id}")


def _build_runtime_route_output_path(
    *,
    route_id: str,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> Path:
    output_file = {
        "direction_screening": "direction-screening-workspace.json",
        "question_refinement": "question-refinement-workspace.json",
        "argument_building": "argument-building-workspace.json",
        "fit_alignment": "fit-alignment-workspace.json",
        "outline": "outline-workspace.json",
        "drafting": "drafting-workspace.json",
        "critique": "critique-workspace.json",
        "revision": "revision-workspace.json",
        "frozen": "frozen-workspace.json",
        "artifact_bundle": "artifact-bundle.json",
        "final_package": "final-package.json",
        "hosted_contract_bundle": "hosted-contract-bundle.json",
    }.get(route_id)
    if output_file is None:
        raise WorkspaceStateError(f"grant_user_loop 不支持 runtime output path route: {route_id}")

    program_id = _require_runtime_path_segment(read_program_id(), field_name="program_id")
    return (
        resolve_runtime_state_root()
        / "reports"
        / program_id
        / _require_runtime_path_segment(grant_run_id, field_name="grant_run_id")
        / _require_runtime_path_segment(workspace_id, field_name="workspace_id")
        / _require_runtime_path_segment(draft_id or "no-draft", field_name="draft_id")
        / output_file
    ).resolve()


def _require_runtime_path_segment(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"grant_user_loop runtime output path 缺少合法字段: {field_name}")
    resolved_value = value.strip()
    if resolved_value in {".", ".."} or "/" in resolved_value or "\\" in resolved_value:
        raise WorkspaceStateError(f"grant_user_loop runtime output path 字段不能包含路径分隔符: {field_name}")
    return resolved_value


def _build_grant_user_loop_commands(
    *,
    input_path: Path,
    task_intent: str,
    run_recommended_route: Any,
) -> dict[str, Any]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "mainline_status": public_cli_command("mainline-status", "--format", "json"),
        "phase_status_current": public_cli_command("mainline-phase", "--phase", "current", "--format", "json"),
        "phase_status_next": public_cli_command("mainline-phase", "--phase", "next", "--format", "json"),
        "open_grant_cockpit": public_cli_command(
            "grant-cockpit", "--input", str(resolved_input_path), "--format", "json"
        ),
        "open_grant_direct_entry": public_cli_command(
            "grant-direct-entry",
            "--input",
            str(resolved_input_path),
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        "run_recommended_route": (
            _require_nonempty_string(run_recommended_route, field_name="run_recommended_route")
            if run_recommended_route is not None
            else None
        ),
        "build_direct_entry": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "direct",
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        "build_opl_handoff": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "opl-handoff",
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
    }


def _validate_grant_user_loop_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_contract_schema(
        payload,
        schema_file=GRANT_USER_LOOP_SCHEMA_FILE,
        context="grant_user_loop",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    grant_user_loop = _require_mapping(
        payload,
        "grant_user_loop",
        context="grant_user_loop",
    )
    grant_direct_entry = _require_mapping(
        grant_user_loop,
        "grant_direct_entry",
        context="grant_user_loop.grant_direct_entry",
    )
    if (
        _require_nonempty_string_from_mapping(
            grant_user_loop,
            "task_intent",
            context="grant_user_loop",
        )
        != _require_nonempty_string_from_mapping(
            grant_direct_entry,
            "task_intent",
            context="grant_user_loop.grant_direct_entry",
        )
    ):
        raise WorkspaceStateError(
            "grant_user_loop.task_intent 与 grant_direct_entry.task_intent 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    next_action = _require_mapping(
        grant_user_loop,
        "next_action",
        context="grant_user_loop.next_action",
    )
    recommended_executor_route = _require_mapping(
        grant_direct_entry,
        "recommended_executor_route",
        context="grant_user_loop.grant_direct_entry",
    )
    _validate_runtime_continuity_alignment(
        session_continuity=_require_mapping(
            grant_user_loop,
            "session_continuity",
            context="grant_user_loop.session_continuity",
        ),
        progress_surface=_require_mapping(
            grant_user_loop,
            "progress_projection",
            context="grant_user_loop.progress_projection",
        ),
        artifact_inventory=_require_mapping(
            grant_user_loop,
            "artifact_inventory",
            context="grant_user_loop.artifact_inventory",
        ),
        runtime_control=_require_mapping(
            grant_user_loop,
            "runtime_control",
            context="grant_user_loop.runtime_control",
        ),
        projection_truth=_require_mapping(
            grant_direct_entry,
            "progress_projection",
            context="grant_user_loop.grant_direct_entry",
        ),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        context_prefix="grant_user_loop",
    )
    if next_action.get("route_id") != recommended_executor_route.get("route_id"):
        raise WorkspaceStateError(
            "grant_user_loop.next_action.route_id 与 grant_direct_entry.recommended_executor_route.route_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if next_action.get("route_status") != recommended_executor_route.get("route_status"):
        raise WorkspaceStateError(
            "grant_user_loop.next_action.route_status 与 grant_direct_entry.recommended_executor_route.route_status 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    action_kind = _require_nonempty_string_from_mapping(
        next_action,
        "action_kind",
        context="grant_user_loop.next_action",
    )
    command = next_action.get("command")
    handoff_surfaces = next_action.get("handoff_surfaces")
    if action_kind == "execute_landed_route":
        if not isinstance(command, str) or not command.strip():
            raise WorkspaceStateError(
                "grant_user_loop.next_action.command 必须在 landed route 时非空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
        if handoff_surfaces is not None:
            raise WorkspaceStateError(
                "grant_user_loop.next_action.handoff_surfaces 必须在 landed route 时为空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
    elif action_kind != "execute_landed_route":
        raise WorkspaceStateError(
            f"grant_user_loop.next_action.action_kind 非法: {action_kind}",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _validate_product_entry_manifest_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_shared_family_product_entry_manifest(
        payload["product_entry_manifest"],
        require_contract_bundle=True,
        require_runtime_companions=True,
    )
    _validate_contract_schema(
        _schema_payload_without_contract_bundle(payload, surface_key="product_entry_manifest"),
        schema_file=PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
        context="product_entry_manifest",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _validate_product_frontdesk_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_shared_family_product_frontdesk(
        payload["product_frontdesk"],
        require_contract_bundle=True,
        require_runtime_companions=True,
    )
    _validate_contract_schema(
        _schema_payload_without_contract_bundle(payload, surface_key="product_frontdesk"),
        schema_file=PRODUCT_FRONTDESK_SCHEMA_FILE,
        context="product_frontdesk",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    product_frontdesk = _require_mapping(
        payload,
        "product_frontdesk",
        context="product_frontdesk",
    )
    manifest = _require_mapping(
        product_frontdesk,
        "product_entry_manifest",
        context="product_frontdesk.product_entry_manifest",
    )
    for surface_key in ("session_continuity", "progress_projection", "artifact_inventory", "runtime_control"):
        if product_frontdesk.get(surface_key) != manifest.get(surface_key):
            raise WorkspaceStateError(
                f"product_frontdesk.{surface_key} 与 product_entry_manifest.{surface_key} 不一致。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )


def _validate_runtime_continuity_alignment(
    *,
    session_continuity: Mapping[str, Any],
    progress_surface: Mapping[str, Any],
    artifact_inventory: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    projection_truth: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    context_prefix: str,
) -> None:
    if progress_surface.get("projection") != projection_truth:
        raise WorkspaceStateError(
            f"{context_prefix}.progress_projection 与 continuity progress surface 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            session_continuity,
            "session_id",
            context=f"{context_prefix}.session_continuity",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.session_continuity.session_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            progress_surface,
            "grant_run_id",
            context=f"{context_prefix}.progress_projection",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.progress_projection.grant_run_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            artifact_inventory,
            "grant_run_id",
            context=f"{context_prefix}.artifact_inventory",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.artifact_inventory.grant_run_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    runtime_control_session_locator = _require_mapping(
        runtime_control,
        "session_locator",
        context=f"{context_prefix}.runtime_control",
    )
    if (
        _require_nonempty_string_from_mapping(
            runtime_control_session_locator,
            "locator_value",
            context=f"{context_prefix}.runtime_control.session_locator",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.runtime_control.session_locator.locator_value 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    runtime_control_restore_point = _require_mapping(
        runtime_control,
        "restore_point",
        context=f"{context_prefix}.runtime_control",
    )
    if (
        _require_nonempty_string_from_mapping(
            runtime_control_restore_point,
            "session_id",
            context=f"{context_prefix}.runtime_control.restore_point",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.runtime_control.restore_point.session_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _schema_payload_without_contract_bundle(
    payload: Mapping[str, Any],
    *,
    surface_key: str,
) -> dict[str, Any]:
    normalized_payload = dict(payload)
    surface = dict(
        _require_mapping(
            payload,
            surface_key,
            context=f"{surface_key}_schema_validation",
        )
    )
    _strip_contract_bundle_fields(surface)
    nested_manifest = surface.get("product_entry_manifest")
    if isinstance(nested_manifest, Mapping):
        normalized_manifest = dict(nested_manifest)
        _strip_contract_bundle_fields(normalized_manifest)
        surface["product_entry_manifest"] = normalized_manifest
    normalized_payload[surface_key] = surface
    return normalized_payload


def _build_runtime_continuity_surfaces(
    *,
    progress_projection: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
    runtime_summary: Mapping[str, Any],
    managed_runtime_contract: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
    funding_call: str,
    grant_progress_command: str,
    summarize_workspace_command: str,
    stage_route_report_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
) -> dict[str, dict[str, Any]]:
    session_continuity = _build_session_continuity_surface(
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
    )
    progress_surface = _build_progress_projection_surface(
        projection=dict(progress_projection),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
        inspect_progress_command=grant_progress_command,
        summarize_workspace_command=summarize_workspace_command,
        stage_route_report_command=stage_route_report_command,
    )
    artifact_inventory = _build_artifact_inventory_surface(
        workspace_summary=workspace_summary,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
    )
    runtime_control = _build_runtime_control_surface(
        runtime_summary=runtime_summary,
        managed_runtime_contract=managed_runtime_contract,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        journal_path=_require_nonempty_string_from_mapping(
            session_continuity,
            "journal_path",
            context="session_continuity",
        ),
        runtime_resume_command=_require_nonempty_string_from_mapping(
            _require_mapping(
                _require_mapping(
                    session_continuity,
                    "runtime_entries",
                    context="session_continuity",
                ),
                "runtime_resume",
                context="session_continuity.runtime_entries",
            ),
            "command",
            context="session_continuity.runtime_entries.runtime_resume",
        ),
        funding_call=funding_call,
        grant_progress_command=grant_progress_command,
        summarize_workspace_command=summarize_workspace_command,
        grant_user_loop_command=grant_user_loop_command,
        grant_direct_entry_command=grant_direct_entry_command,
    )
    return {
        "session_continuity": session_continuity,
        "progress_projection": progress_surface,
        "artifact_inventory": artifact_inventory,
        "runtime_control": runtime_control,
    }


def _build_skill_runtime_continuity_envelope(
    *,
    session_continuity: Mapping[str, Any],
    progress_surface: Mapping[str, Any],
    artifact_inventory: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
) -> dict[str, Any]:
    if (
        _require_nonempty_string_from_mapping(
            progress_surface,
            "surface_kind",
            context="progress_surface",
        )
        != "progress_projection"
    ):
        raise WorkspaceStateError("progress_surface 必须是 progress_projection。")
    if (
        _require_nonempty_string_from_mapping(
            artifact_inventory,
            "surface_kind",
            context="artifact_inventory",
        )
        != "artifact_inventory"
    ):
        raise WorkspaceStateError("artifact_inventory 必须是 artifact_inventory。")
    runtime_control_restore_point = _require_mapping(
        runtime_control,
        "restore_point",
        context="runtime_control",
    )
    runtime_control_progress_surface = _require_mapping(
        runtime_control,
        "progress_surface",
        context="runtime_control",
    )
    runtime_control_artifact_surface = _require_mapping(
        runtime_control,
        "artifact_pickup_surface",
        context="runtime_control",
    )
    progress_surface_ref = _require_nonempty_string_from_mapping(
        runtime_control_progress_surface,
        "ref",
        context="runtime_control.progress_surface",
    )
    artifact_surface_ref = _require_nonempty_string_from_mapping(
        runtime_control_artifact_surface,
        "ref",
        context="runtime_control.artifact_pickup_surface",
    )
    semantic_closure = _require_mapping(
        runtime_control,
        "semantic_closure",
        context="runtime_control",
    )
    return {
        "surface_kind": "skill_runtime_continuity",
        "runtime_owner": _require_nonempty_string_from_mapping(
            runtime_control,
            "runtime_owner",
            context="runtime_control",
        ),
        "domain_owner": _require_nonempty_string_from_mapping(
            runtime_control,
            "domain_owner",
            context="runtime_control",
        ),
        "executor_owner": _require_nonempty_string_from_mapping(
            runtime_control,
            "executor_owner",
            context="runtime_control",
        ),
        "authoring_continuity": _require_nonempty_string_from_mapping(
            semantic_closure,
            "authoring_continuity",
            context="runtime_control.semantic_closure",
        ),
        "funding_call_lock": _require_nonempty_string_from_mapping(
            semantic_closure,
            "funding_call_lock",
            context="runtime_control.semantic_closure",
        ),
        "quality_closure_surface": _require_nonempty_string_from_mapping(
            semantic_closure,
            "quality_closure_surface",
            context="runtime_control.semantic_closure",
        ),
        "submission_ready_gate": _require_nonempty_string_from_mapping(
            semantic_closure,
            "submission_ready_gate",
            context="runtime_control.semantic_closure",
        ),
        "session_locator_field": _require_nonempty_string_from_mapping(
            session_continuity,
            "session_locator_field",
            context="session_continuity",
        ),
        "session_surface_ref": "/product_entry_manifest/session_continuity",
        "progress_surface_ref": progress_surface_ref,
        "artifact_surface_ref": artifact_surface_ref,
        "restore_point_surface_ref": "/product_entry_manifest/runtime_control/restore_point",
        "recommended_resume_command": _require_nonempty_string_from_mapping(
            runtime_control_restore_point,
            "resume_command",
            context="runtime_control.restore_point",
        ),
        "recommended_progress_command": _require_nonempty_string_from_mapping(
            runtime_control_progress_surface,
            "command",
            context="runtime_control.progress_surface",
        ),
        "recommended_artifact_command": _require_nonempty_string_from_mapping(
            runtime_control_artifact_surface,
            "command",
            context="runtime_control.artifact_pickup_surface",
        ),
    }


def _build_session_continuity_surface(
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
) -> dict[str, Any]:
    runtime_state_contract = _build_runtime_state_contract()
    session_journal_root = _require_nonempty_string_from_mapping(
        runtime_state_contract,
        "session_journal_root",
        context="runtime_state_contract",
    )
    journal_path = f"{session_journal_root}{grant_run_id}.json"
    runtime_run_command = public_cli_command(
        "runtime-run",
        "--input",
        input_path,
        "--journal",
        journal_path,
        "--format",
        "json",
    )
    runtime_resume_command = public_cli_command(
        "runtime-resume",
        "--journal",
        journal_path,
        "--format",
        "json",
    )
    return {
        "surface_kind": "session_continuity",
        "version": 1,
        "summary": "显式锚定 session locator 与 journal durable anchor，避免依赖默认 journal 推断。",
        "session_locator_field": "grant_run_id",
        "session_handle_kind": "grant_run_id",
        "session_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "runtime_state_contract": dict(runtime_state_contract),
        "journal_path": journal_path,
        "runtime_entries": {
            "runtime_run": {
                "command": runtime_run_command,
                "surface_kind": "runtime_run",
                "summary": "用显式 --journal 启动或继续当前 workspace 的 runtime run。",
            },
            "runtime_resume": {
                "command": runtime_resume_command,
                "surface_kind": "runtime_resume",
                "summary": "用显式 --journal 恢复当前 session。",
            },
        },
        "repo_owned_truth": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": input_path,
            "truth_owner": TARGET_DOMAIN_ID,
        },
    }


def _build_runtime_control_surface(
    *,
    runtime_summary: Mapping[str, Any],
    managed_runtime_contract: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    journal_path: str,
    runtime_resume_command: str,
    funding_call: str,
    grant_progress_command: str,
    summarize_workspace_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "runtime_control",
        "version": 2,
        "summary": (
            "repo-owned runtime control reference：显式导出 owner 语义、restore point、"
            "progress/artifact/approval surface 与 direct-entry locator。"
        ),
        "runtime_owner": _require_nonempty_string_from_mapping(
            runtime_summary,
            "runtime_owner",
            context="runtime_summary",
        ),
        "domain_owner": _require_nonempty_string_from_mapping(
            managed_runtime_contract,
            "domain_owner",
            context="managed_runtime_contract",
        ),
        "executor_owner": _require_nonempty_string_from_mapping(
            managed_runtime_contract,
            "executor_owner",
            context="managed_runtime_contract",
        ),
        "session_locator": {
            "locator_field": "grant_run_id",
            "locator_value": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "restore_point": {
            "session_id": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "journal_path": journal_path,
            "resume_command": runtime_resume_command,
            "resume_surface_kind": "runtime_resume",
        },
        "semantic_closure": {
            "surface_kind": "runtime_control_semantic_closure",
            "authoring_continuity": "same_funding_call_task",
            "funding_call_lock": _require_nonempty_string(funding_call, field_name="funding_call"),
            "quality_closure_surface": "grant-quality-closure-dossier",
            "submission_ready_gate": "package_submission_ready_strict_export_gate",
            "closure_ref": "/product_entry_manifest/grant_authoring_readiness",
        },
        "progress_surface": {
            "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "command": grant_progress_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/progress_projection",
            "summary": "当前 grant progress projection surface。",
        },
        "artifact_pickup_surface": {
            "surface_kind": "artifact_inventory",
            "command": summarize_workspace_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/artifact_inventory",
            "summary": "当前 workspace artifact pickup index surface。",
        },
        "approval_control_surface": {
            "surface_kind": GRANT_USER_LOOP_KIND,
            "command": grant_user_loop_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/operator_loop_surface",
            "summary": "当前人工 gate / control action 入口。",
        },
        "direct_entry": {
            "surface_kind": GRANT_DIRECT_ENTRY_KIND,
            "command": grant_direct_entry_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/product_entry_shell/grant_direct_entry",
            "summary": "直接导出当前 grant direct-entry command 与 locator。",
        },
    }


def _build_progress_projection_surface(
    *,
    projection: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
    inspect_progress_command: str,
    summarize_workspace_command: str,
    stage_route_report_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "progress_projection",
        "version": 1,
        "summary": "repo-owned workspace truth 上的 grant progress projection。",
        "workspace_surface_kind": "nsfc_workspace",
        "workspace_path": input_path,
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "projection_kind": _require_nonempty_string_from_mapping(
            projection,
            "projection_kind",
            context="grant-progress.progress_projection",
        ),
        "projection": dict(projection),
        "truth_anchors": {
            "workspace_document": {
                "ref_kind": "path",
                "ref": input_path,
                "label": "workspace JSON (repo-owned truth)",
            },
            "stage_route_report": {
                "ref_kind": "command",
                "ref": stage_route_report_command,
                "label": "stage-route-report (derives from workspace truth)",
            },
            "summarize_workspace": {
                "ref_kind": "command",
                "ref": summarize_workspace_command,
                "label": "summarize-workspace (derives from workspace truth)",
            },
            "inspect_progress": {
                "ref_kind": "command",
                "ref": inspect_progress_command,
                "label": "grant-progress (projection surface)",
            },
        },
    }


def _build_artifact_inventory_surface(
    *,
    workspace_summary: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = [
        {
            "artifact_kind": "workspace_document",
            "label": "workspace JSON (repo-owned truth)",
            "ref": {
                "ref_kind": "path",
                "ref": input_path,
            },
        }
    ]

    def _append_workspace_ref(*, artifact_kind: str, label: str, ref: str) -> None:
        artifacts.append(
            {
                "artifact_kind": artifact_kind,
                "label": label,
                "ref": {
                    "ref_kind": "workspace_locator",
                    "ref": ref,
                },
            }
        )

    active_draft = _optional_mapping(workspace_summary, "active_draft")
    if isinstance(active_draft, Mapping):
        draft_id = _optional_string_from_mapping(active_draft, "id")
        if draft_id is not None:
            _append_workspace_ref(
                artifact_kind="active_draft",
                label=f"active draft: {draft_id}",
                ref=f"grant_workspace::{workspace_id}::application_drafts::{draft_id}",
            )

    active_revision_plan = _optional_mapping(workspace_summary, "active_revision_plan")
    if isinstance(active_revision_plan, Mapping):
        revision_plan_id = _optional_string_from_mapping(active_revision_plan, "id")
        if revision_plan_id is not None:
            _append_workspace_ref(
                artifact_kind="active_revision_plan",
                label=f"active revision plan: {revision_plan_id}",
                ref=f"grant_workspace::{workspace_id}::revision_plans::{revision_plan_id}",
            )

    active_critique = _optional_mapping(workspace_summary, "active_critique")
    if isinstance(active_critique, Mapping):
        critique_id = _optional_string_from_mapping(active_critique, "id")
        if critique_id is not None:
            _append_workspace_ref(
                artifact_kind="active_critique",
                label=f"active critique: {critique_id}",
                ref=f"grant_workspace::{workspace_id}::mentor_critiques::{critique_id}",
            )

    selected_direction = _optional_mapping(workspace_summary, "selected_direction")
    if isinstance(selected_direction, Mapping):
        direction_id = _optional_string_from_mapping(selected_direction, "id")
        if direction_id is not None:
            _append_workspace_ref(
                artifact_kind="selected_direction",
                label=f"selected direction: {direction_id}",
                ref=f"grant_workspace::{workspace_id}::direction_hypotheses::{direction_id}",
            )

    selected_question = _optional_mapping(workspace_summary, "selected_question")
    if isinstance(selected_question, Mapping):
        question_id = _optional_string_from_mapping(selected_question, "id")
        if question_id is not None:
            _append_workspace_ref(
                artifact_kind="selected_question",
                label=f"selected question: {question_id}",
                ref=f"grant_workspace::{workspace_id}::scientific_question_cards::{question_id}",
            )

    return {
        "surface_kind": "artifact_inventory",
        "version": 1,
        "summary": "汇总 workspace 内当前被选中的主要对象与 draft 工件，作为 repo-owned continuity truth 的索引。",
        "workspace_surface_kind": "nsfc_workspace",
        "workspace_path": input_path,
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "artifacts": artifacts,
    }


def _strip_contract_bundle_fields(surface: dict[str, Any]) -> None:
    surface.pop("schema_ref", None)
    surface.pop("domain_entry_contract", None)
    surface.pop("gateway_interaction_contract", None)


def _build_product_command_catalog(input_path: Path) -> dict[str, str]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "grant_progress": public_cli_command(
            "grant-progress", "--input", str(resolved_input_path), "--format", "json"
        ),
        "grant_intake_audit": public_cli_command(
            "grant-intake-audit", "--input", str(resolved_input_path), "--format", "json"
        ),
        "grant_evidence_grounding": public_cli_command(
            "grant-evidence-grounding", "--input", str(resolved_input_path), "--format", "json"
        ),
        "summarize_workspace": public_cli_command(
            "summarize-workspace", "--input", str(resolved_input_path), "--format", "json"
        ),
        "stage_route_report": public_cli_command(
            "stage-route-report", "--input", str(resolved_input_path), "--format", "json"
        ),
        "critique_summary": public_cli_command(
            "critique-summary", "--input", str(resolved_input_path), "--format", "json"
        ),
        "build_direct_entry": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "direct",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
        "build_opl_handoff": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "opl-handoff",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
        "build_submission_ready_package": public_cli_command(
            "build-submission-ready-package",
            "--input",
            str(resolved_input_path),
            "--output-dir",
            "<submission-ready-output-dir>",
            "--format",
            "json",
        ),
    }

__all__ = [name for name in globals() if not name.startswith("__")]
