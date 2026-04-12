from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.hermes_runtime import (
    _build_domain_entry_contract,
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.workspace import WorkspaceFileError, WorkspaceStateError


PRODUCT_ENTRY_VERSION = 1
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
TARGET_DOMAIN_ID = "med-autogrant"
SUPPORTED_ENTRY_MODES = ("direct", "opl-handoff")
GRANT_PROGRESS_PROJECTION_VERSION = 1
GRANT_PROGRESS_PROJECTION_KIND = "grant_progress"
GRANT_COCKPIT_KIND = "grant_cockpit"
REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}


class MedAutoGrantProductEntry:
    """轻量 grant product entry 壳，复用已 landed 的 domain entry 与 Hermes substrate contract。"""

    def __init__(self, *, domain_entry: MedAutoGrantDomainEntry | None = None) -> None:
        self._domain_entry = domain_entry or MedAutoGrantDomainEntry()

    def build(
        self,
        *,
        input_path: str | Path,
        entry_mode: str,
        task_intent: str,
        output_path: str | Path | None = None,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        resolved_entry_mode = _require_entry_mode(entry_mode)
        resolved_task_intent = _require_nonempty_string(task_intent, field_name="task_intent")

        route_report = self._domain_entry.dispatch(
            {
                "command": "stage-route-report",
                "input_path": str(resolved_input_path),
            }
        )
        if route_report.get("ok") is not True:
            raise WorkspaceStateError("product entry 只允许从已验证通过的 workspace 构建。")

        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
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
        verification_checkpoint = _require_mapping(
            route_report,
            "verification_checkpoint",
            context="stage-route-report",
        )
        checkpoint_status = _require_nonempty_string_from_mapping(
            verification_checkpoint,
            "checkpoint_status",
            context="stage-route-report.verification_checkpoint",
        )
        identity = _require_mapping(
            verification_checkpoint,
            "identity",
            context="stage-route-report.verification_checkpoint",
        )
        draft_id = _require_optional_string(identity.get("draft_id"), field_name="draft_id")

        route = _require_mapping(route_report, "route", context="stage-route-report")
        next_step = _require_mapping(route, "next_step", context="stage-route-report.route")
        recommended_next_stage = _require_nonempty_string_from_mapping(
            next_step,
            "recommended_stage",
            context="stage-route-report.route.next_step",
        )

        resolved_funding_call = (
            _require_nonempty_string(funding_call, field_name="funding_call")
            if funding_call is not None
            else _read_funding_call_from_summary(workspace_summary)
        )

        current_program_contract = _read_current_program_contract()
        executor_routing_contract = _build_executor_routing_contract(
            current_stage=lifecycle_stage,
            recommended_next_stage=recommended_next_stage,
            include_route_catalog=True,
        )
        _validate_executor_routing_contract(
            executor_routing_contract,
            current_stage=lifecycle_stage,
            recommended_next_stage=recommended_next_stage,
            include_route_catalog=True,
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
        product_entry = {
            "entry_version": PRODUCT_ENTRY_VERSION,
            "entry_kind": PRODUCT_ENTRY_KIND,
            "target_domain_id": TARGET_DOMAIN_ID,
            "task_intent": resolved_task_intent,
            "entry_mode": resolved_entry_mode,
            "workspace_locator": {
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(resolved_input_path),
            },
            "runtime_session_contract": {
                "grant_run_id": grant_run_id,
                "session_handle_kind": "grant_run_id",
                "start_entry": "run-local",
                "resume_entry": "resume-local",
                "runtime_substrate_contract": _build_runtime_substrate_contract(
                    current_program_contract=current_program_contract,
                ),
                "runtime_state_contract": _build_runtime_state_contract(),
            },
            "return_surface_contract": {
                "entry_adapter": "MedAutoGrantDomainEntry",
                "default_formal_entry": "CLI",
                "supported_entry_modes": list(SUPPORTED_ENTRY_MODES),
                "domain_entry_contract": _build_domain_entry_contract(),
                "checkpoint_aggregation_surface": "stage-route-report",
                "operator_contract": _build_operator_contract(),
            },
            "domain_payload": {
                "workspace_id": workspace_id,
                "draft_id": draft_id,
                "funding_call": resolved_funding_call,
            },
            "stage_snapshot": {
                "lifecycle_stage": lifecycle_stage,
                "checkpoint_status": checkpoint_status,
                "recommended_next_stage": recommended_next_stage,
            },
            "executor_routing_contract": executor_routing_contract,
        }
        _validate_contract_schema(
            product_entry,
            schema_file=PRODUCT_ENTRY_SCHEMA_FILE,
            context="product_entry",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

        resolved_output_path = None
        if output_path is not None:
            resolved_output_path = Path(output_path).expanduser().resolve()
            _write_product_entry_output(resolved_output_path, product_entry)

        return {
            "ok": True,
            "command": "build-product-entry",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
            "output_path": str(resolved_output_path) if resolved_output_path is not None else None,
            "product_entry": product_entry,
        }

    def read_grant_progress(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        context = self._load_projection_context(input_path=input_path)
        route_report = context["route_report"]
        workspace_summary = context["workspace_summary"]
        critique_summary = context["critique_summary"]
        resolved_input_path = context["resolved_input_path"]

        verification_checkpoint = _require_mapping(
            route_report,
            "verification_checkpoint",
            context="stage-route-report",
        )
        identity = _require_mapping(
            verification_checkpoint,
            "identity",
            context="stage-route-report.verification_checkpoint",
        )
        route = _require_mapping(route_report, "route", context="stage-route-report")
        next_step = _require_mapping(route, "next_step", context="stage-route-report.route")

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
        draft_id = _require_optional_string(identity.get("draft_id"), field_name="draft_id")
        checkpoint_status = _require_nonempty_string_from_mapping(
            verification_checkpoint,
            "checkpoint_status",
            context="stage-route-report.verification_checkpoint",
        )
        recommended_next_stage = _require_nonempty_string_from_mapping(
            next_step,
            "recommended_stage",
            context="stage-route-report.route.next_step",
        )
        progress_projection = {
            "projection_version": GRANT_PROGRESS_PROJECTION_VERSION,
            "projection_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "workspace_surface_kind": "nsfc_workspace",
            "current_stage": lifecycle_stage,
            "current_stage_summary": _build_current_stage_summary(
                lifecycle_stage=lifecycle_stage,
                checkpoint_status=checkpoint_status,
                next_step=next_step,
            ),
            "checkpoint_status": checkpoint_status,
            "recommended_next_stage": recommended_next_stage,
            "current_blockers": _read_blocking_issues(critique_summary),
            "next_system_action": _read_next_system_action(next_step),
            "needs_author_decision": bool(next_step.get("requires_human_confirmation")),
            "author_decision_summary": _build_author_decision_summary(next_step),
            "focus": _build_focus_payload(
                workspace_summary=workspace_summary,
                critique_summary=critique_summary,
            ),
            "product_entry_surface": {
                "builder_command": "build-product-entry",
                "target_domain_id": TARGET_DOMAIN_ID,
                "supported_entry_modes": list(SUPPORTED_ENTRY_MODES),
                "task_intent_required": True,
                "workspace_path": str(resolved_input_path),
            },
        }
        payload = {
            "ok": True,
            "command": "grant-progress",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
            "progress_projection": progress_projection,
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_PROGRESS_SCHEMA_FILE,
            context="grant_progress",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
        return payload

    def read_grant_cockpit(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        progress_payload = self.read_grant_progress(input_path=input_path)
        progress_projection = _require_mapping(
            progress_payload,
            "progress_projection",
            context="grant-progress",
        )
        resolved_input_path = Path(progress_payload["input_path"]).expanduser().resolve()
        context = self._load_projection_context(input_path=resolved_input_path)
        workspace_summary = context["workspace_summary"]
        critique_summary = context["critique_summary"]

        blocking_issues = list(progress_projection.get("current_blockers", []))
        needs_author_decision = bool(progress_projection.get("needs_author_decision"))
        workspace_status = _build_workspace_status(
            blockers=blocking_issues,
            needs_author_decision=needs_author_decision,
        )
        workspace_alerts = list(blocking_issues)
        author_decision_summary = progress_projection.get("author_decision_summary")
        if isinstance(author_decision_summary, str) and author_decision_summary.strip():
            workspace_alerts.append(author_decision_summary.strip())

        payload = {
            "ok": True,
            "command": "grant-cockpit",
            "grant_run_id": progress_payload["grant_run_id"],
            "workspace_id": progress_payload["workspace_id"],
            "draft_id": progress_payload["draft_id"],
            "lifecycle_stage": progress_payload["lifecycle_stage"],
            "input_path": str(resolved_input_path),
            "grant_cockpit": {
                "cockpit_kind": GRANT_COCKPIT_KIND,
                "workspace_overview": _build_workspace_overview(
                    workspace_summary=workspace_summary,
                    progress_projection=progress_projection,
                    critique_summary=critique_summary,
                ),
                "workspace_status": workspace_status,
                "workspace_alerts": workspace_alerts,
                "progress_projection": dict(progress_projection),
                "commands": _build_product_command_catalog(resolved_input_path),
            },
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_COCKPIT_SCHEMA_FILE,
            context="grant_cockpit",
            grant_run_id=progress_payload["grant_run_id"],
            workspace_id=progress_payload["workspace_id"],
            lifecycle_stage=progress_payload["lifecycle_stage"],
        )
        return payload

    def _load_projection_context(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        route_report = self._domain_entry.dispatch(
            {
                "command": "stage-route-report",
                "input_path": str(resolved_input_path),
            }
        )
        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
        )
        lifecycle_stage = _require_nonempty_string_from_mapping(
            route_report,
            "lifecycle_stage",
            context="stage-route-report",
        )
        critique_summary = None
        if lifecycle_stage in REVIEW_CONTEXT_STAGES:
            critique_summary = self._domain_entry.dispatch(
                {
                    "command": "critique-summary",
                    "input_path": str(resolved_input_path),
                }
            )
        return {
            "resolved_input_path": resolved_input_path,
            "route_report": route_report,
            "workspace_summary": workspace_summary,
            "critique_summary": critique_summary,
        }


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


def _build_product_command_catalog(input_path: Path) -> dict[str, str]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "grant_progress": (
            f"uv run python -m med_autogrant grant-progress --input {resolved_input_path} --format json"
        ),
        "summarize_workspace": (
            f"uv run python -m med_autogrant summarize-workspace --input {resolved_input_path} --format json"
        ),
        "stage_route_report": (
            f"uv run python -m med_autogrant stage-route-report --input {resolved_input_path} --format json"
        ),
        "critique_summary": (
            f"uv run python -m med_autogrant critique-summary --input {resolved_input_path} --format json"
        ),
        "build_direct_entry": (
            "uv run python -m med_autogrant build-product-entry "
            f"--input {resolved_input_path} --entry-mode direct "
            "--task-intent <describe-task-intent> --format json"
        ),
        "build_opl_handoff": (
            "uv run python -m med_autogrant build-product-entry "
            f"--input {resolved_input_path} --entry-mode opl-handoff "
            "--task-intent <describe-task-intent> --format json"
        ),
    }
