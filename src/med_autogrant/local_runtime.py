from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from med_autogrant.route_report import build_stage_route_report
from med_autogrant.workspace import WorkspaceError, WorkspaceFileError, load_workspace_document, validate_workspace_document


DEFAULT_JOURNAL_ROOT = Path.home() / ".med-autogrant" / "runs"
JOURNAL_VERSION = 1


class LocalRuntimeStateError(WorkspaceError):
    """Local runtime journal/state mismatch。"""


def run_local_runtime(
    *,
    input_path: str | Path,
    journal_path: str | Path | None = None,
    trigger: str = "run-local",
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    document = load_workspace_document(resolved_input_path)
    validation = validate_workspace_document(document)
    resolved_journal_path = _resolve_journal_path(document=document, journal_path=journal_path)
    journal = _load_or_initialize_journal(
        journal_path=resolved_journal_path,
        document=document,
        input_path=resolved_input_path,
    )

    if validation.ok:
        route_report = build_stage_route_report(document)
        stop_reason = derive_stop_reason(route_report)
        stage_action_envelope = derive_stage_action_envelope(
            route_report=route_report,
            stop_reason=stop_reason,
            journal_path=resolved_journal_path,
        )
        draft_id = route_report["verification_checkpoint"]["identity"]["draft_id"]
        lifecycle_stage = route_report["lifecycle_stage"]
    else:
        route_report = {
            "ok": False,
            "grant_run_id": document.get("grant_run_id"),
            "workspace_id": document.get("workspace_id"),
            "lifecycle_stage": document.get("lifecycle_stage"),
            "validation": validation.to_dict(document),
            "verification_checkpoint": None,
        }
        stop_reason = {
            "code": "validation_failed",
            "reason": validation.errors[0].message,
            "current_stage": document.get("lifecycle_stage"),
            "recommended_next_stage": document.get("lifecycle_stage"),
            "checkpoint_status": None,
            "requires_human_confirmation": False,
            "forced_rollback_stage": None,
            "forced_rollback_reason": None,
        }
        stage_action_envelope = None
        draft_id = None
        lifecycle_stage = document.get("lifecycle_stage")

    journal = _append_attempt(
        journal=journal,
        trigger=trigger,
        lifecycle_stage=lifecycle_stage,
        route_report=route_report,
        stop_reason=stop_reason,
        stage_action_envelope=stage_action_envelope,
    )
    _write_journal(resolved_journal_path, journal)

    payload = {
        "ok": validation.ok,
        "command": trigger,
        "grant_run_id": document.get("grant_run_id"),
        "workspace_id": document.get("workspace_id"),
        "draft_id": draft_id,
        "lifecycle_stage": lifecycle_stage,
        "input_path": str(resolved_input_path),
        "journal_path": str(resolved_journal_path),
        "attempt_index": journal["attempts"][-1]["attempt_index"],
        "stop_reason": stop_reason,
        "stage_action_envelope": stage_action_envelope,
        "route_report": route_report,
        "resume": {
            "command": "resume-local",
            "journal_path": str(resolved_journal_path),
        },
    }
    if not validation.ok:
        payload["error"] = f"validation_failed: {validation.errors[0].path}: {validation.errors[0].message}"
        payload["errors"] = validation.to_dict(document)["errors"]
    return payload


def resume_local_runtime(*, journal_path: str | Path) -> dict[str, Any]:
    resolved_journal_path = Path(journal_path).expanduser().resolve()
    journal = _read_journal(resolved_journal_path)
    input_path = journal.get("input_path")
    if not isinstance(input_path, str) or not input_path:
        raise LocalRuntimeStateError(f"journal 缺少 input_path: {resolved_journal_path}")
    return run_local_runtime(input_path=input_path, journal_path=resolved_journal_path, trigger="resume-local")


def derive_stop_reason(route_report: dict[str, Any]) -> dict[str, Any]:
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    checkpoint_status = checkpoint["checkpoint_status"]
    route_alignment = checkpoint["route_alignment"]
    forced_rollback_stage = route_alignment.get("forced_rollback_stage")
    forced_rollback_reason = route_alignment.get("forced_rollback_reason")
    requires_human_confirmation = bool(next_step.get("requires_human_confirmation"))

    if checkpoint_status == "submission_frozen":
        code = "presubmission_frozen"
    elif forced_rollback_stage or checkpoint_status == "rollback_required":
        code = "rollback_required"
    elif checkpoint_status == "freeze_ready":
        code = "freeze_ready"
    elif requires_human_confirmation:
        code = "human_confirmation_required"
    else:
        code = "stage_action_required"

    return {
        "code": code,
        "reason": next_step["reason"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint_status,
        "requires_human_confirmation": requires_human_confirmation,
        "forced_rollback_stage": forced_rollback_stage,
        "forced_rollback_reason": forced_rollback_reason,
    }


def derive_stage_action_envelope(
    *,
    route_report: dict[str, Any],
    stop_reason: dict[str, Any],
    journal_path: Path,
) -> dict[str, Any] | None:
    if stop_reason.get("code") != "stage_action_required":
        return None

    summary = route_report["route"]["summarize_workspace"]
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    selection = summary.get("current_selection") or {}
    actions = next_step.get("actions") or []

    return {
        "envelope_version": 1,
        "status": "action_required",
        "grant_run_id": route_report["grant_run_id"],
        "workspace_id": route_report["workspace_id"],
        "draft_id": checkpoint["identity"]["draft_id"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint["checkpoint_status"],
        "requires_human_confirmation": bool(next_step.get("requires_human_confirmation")),
        "selection": {
            "selected_direction_id": selection.get("selected_direction_id"),
            "selected_question_id": selection.get("selected_question_id"),
            "active_fit_mapping_id": selection.get("active_fit_mapping_id"),
            "active_draft_id": selection.get("active_draft_id"),
            "active_revision_plan_id": selection.get("active_revision_plan_id"),
        },
        "action_items": [
            {
                "index": index,
                "instruction": instruction,
            }
            for index, instruction in enumerate(actions, start=1)
        ],
        "route_reason": next_step["reason"],
        "resume_decision": {
            "command": "resume-local",
            "journal_path": str(journal_path),
            "append_attempt": True,
            "reuse_grant_run_id": True,
        },
    }


def _resolve_journal_path(*, document: dict[str, Any], journal_path: str | Path | None) -> Path:
    if journal_path is not None:
        return Path(journal_path).expanduser().resolve()
    grant_run_id = document.get("grant_run_id")
    if not isinstance(grant_run_id, str) or not grant_run_id:
        raise LocalRuntimeStateError("workspace 缺少 grant_run_id，无法推导默认 journal 路径。")
    return (DEFAULT_JOURNAL_ROOT / f"{grant_run_id}.json").resolve()


def _read_journal(journal_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(journal_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 journal 文件: {journal_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"journal JSON 解析失败: {journal_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceFileError(f"journal 顶层必须是 JSON object: {journal_path}")
    return payload


def _load_or_initialize_journal(
    *,
    journal_path: Path,
    document: dict[str, Any],
    input_path: Path,
) -> dict[str, Any]:
    if not journal_path.exists():
        return {
            "journal_version": JOURNAL_VERSION,
            "grant_run_id": document.get("grant_run_id"),
            "workspace_id": document.get("workspace_id"),
            "input_path": str(input_path),
            "latest_stop_reason": None,
            "latest_stage_action_envelope": None,
            "latest_route_report": None,
            "attempts": [],
        }

    journal = _read_journal(journal_path)
    if journal.get("grant_run_id") != document.get("grant_run_id"):
        raise LocalRuntimeStateError(
            f"journal grant_run_id 不匹配: {journal_path} -> {journal.get('grant_run_id')} != {document.get('grant_run_id')}"
        )
    if journal.get("workspace_id") != document.get("workspace_id"):
        raise LocalRuntimeStateError(
            f"journal workspace_id 不匹配: {journal_path} -> {journal.get('workspace_id')} != {document.get('workspace_id')}"
        )
    if journal.get("input_path") != str(input_path):
        raise LocalRuntimeStateError(
            f"journal input_path 不匹配: {journal_path} -> {journal.get('input_path')} != {input_path}"
        )
    attempts = journal.get("attempts")
    if not isinstance(attempts, list):
        raise LocalRuntimeStateError(f"journal attempts 不是 list: {journal_path}")
    return journal


def _append_attempt(
    *,
    journal: dict[str, Any],
    trigger: str,
    lifecycle_stage: str | None,
    route_report: dict[str, Any],
    stop_reason: dict[str, Any],
    stage_action_envelope: dict[str, Any] | None,
) -> dict[str, Any]:
    attempts = journal.setdefault("attempts", [])
    attempt_index = len(attempts) + 1
    checkpoint_status = stop_reason.get("checkpoint_status")
    attempts.append(
        {
            "attempt_index": attempt_index,
            "trigger": trigger,
            "timestamp": datetime.now(UTC).isoformat(),
            "lifecycle_stage": lifecycle_stage,
            "checkpoint_status": checkpoint_status,
            "stop_reason": stop_reason,
            "stage_action_envelope": stage_action_envelope,
        }
    )
    journal["latest_stop_reason"] = stop_reason
    journal["latest_stage_action_envelope"] = stage_action_envelope
    journal["latest_route_report"] = route_report
    return journal


def _write_journal(journal_path: Path, journal: dict[str, Any]) -> None:
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    journal_path.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
