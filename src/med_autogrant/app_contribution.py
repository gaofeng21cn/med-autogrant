"""MAG-owned shared review projections and revision-bound feedback records."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import uuid
from typing import Any

from opl_framework.app_contribution import (
    AppContributionError,
    sha256_bytes,
    verify_work_item_identity,
)
from opl_framework.review_feedback_store import (
    ReviewFeedbackError,
    list_feedback_notes,
    record_feedback_note,
    resolve_contained_path,
    validate_feedback_id,
)

from med_autogrant.workspace_types import WorkspaceStateError

NOTE_ACTION = "mag.workspace.v1#review.note"
NOTE_SCHEMA = {
    "type": "object",
    "required": ["workspace_file", "workspace_id", "grant_run_id", "revision", "request_id", "note"],
    "properties": {
        **{key: {"type": "string", "readOnly": True, "title": title} for key, title in (
            ("workspace_file", "申请文件"), ("workspace_id", "工作区"),
            ("grant_run_id", "申请任务"), ("revision", "所审版本"), ("request_id", "意见编号"))},
        "note": {"type": "string", "title": "审阅意见", "format": "textarea", "maxLength": 20000},
    },
    "additionalProperties": False,
}


def _snapshot(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise WorkspaceStateError("审阅对象必须是 JSON object。")
    return value, sha256_bytes(raw)


def _object(path: Path) -> dict[str, Any]:
    return _snapshot(path)[0]


def _revision(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _source(input_path: str | Path) -> Path:
    path = Path(input_path).expanduser().resolve(strict=True)
    return (path / "workspace.json").resolve(strict=True) if path.is_dir() else path


def _notes_root(source: Path) -> Path:
    try:
        return resolve_contained_path(
            source.parent,
            "runtime/review-feedback",
            container=source.parent,
            must_exist=False,
        )
    except ReviewFeedbackError as error:
        raise WorkspaceStateError("审阅意见目录必须在申请目录内。") from error


def review_notes(input_path: str | Path, revision: str | None = None) -> list[dict[str, Any]]:
    source = _source(input_path)
    revision = revision or _revision(source)
    root = _notes_root(source)
    try:
        entries = list_feedback_notes(root, revision=revision, revision_field="revision", root=source.parent)
    except ReviewFeedbackError as error:
        if error.reason_code == "path_escape":
            raise WorkspaceStateError("审阅意见文件不能为符号链接。") from error
        raise WorkspaceStateError(str(error)) from error
    notes = []
    for note in entries:
        if note.get("source_ref") == str(source):
            artifact_hash = sha256_bytes(Path(note["artifact_ref"]).read_bytes())
            notes.append({**note, "artifact_hash": artifact_hash})
    return notes


def current_review_feedback(input_path: str | Path, document: dict[str, Any]) -> list[dict[str, Any]]:
    """Existing critique consumes only feedback for its exact source candidate."""
    candidate = Path(input_path).expanduser()
    if not candidate.exists():
        return []
    source = _source(candidate)
    if not _notes_root(source).is_dir():
        return []
    current, revision = _snapshot(source)
    if current != document:
        raise WorkspaceStateError("审阅输入已变化，请重新读取原申请后继续。")
    return [note for note in review_notes(source, revision) if note["matches_current_revision"]
            and note.get("workspace_id") == document.get("workspace_id")
            and note.get("grant_run_id") == document.get("grant_run_id")]


def read_review(*, input_path: str | Path) -> dict[str, Any]:
    source = _source(input_path)
    document, revision = _snapshot(source)
    return {"ok": True, "workspace_id": document.get("workspace_id"),
            "grant_run_id": document.get("grant_run_id"), "source_ref": str(source),
            "revision": revision, "review_notes": review_notes(source, revision)}


def record_review(*, input_path: str | Path, workspace_id: str, grant_run_id: str,
                  revision: str, request_id: str, note: str) -> dict[str, Any]:
    if not isinstance(note, str) or not note.strip() or len(note) > 20000:
        raise WorkspaceStateError("审阅意见必须为 1–20000 字符。")
    try:
        normalized_id = validate_feedback_id(request_id)
    except ReviewFeedbackError as error:
        raise WorkspaceStateError("意见编号必须为 1–100 位字母、数字、下划线或短横线。") from error
    source = _source(input_path)
    document = _object(source)
    for field, expected in (("workspace_id", workspace_id), ("grant_run_id", grant_run_id)):
        if not expected or document.get(field) != expected:
            raise WorkspaceStateError(f"所选申请与 {field} 不一致。")
    root = _notes_root(source)
    identity = {"source_ref": str(source), "workspace_id": workspace_id, "grant_run_id": grant_run_id,
                "revision": revision, "request_id": normalized_id, "note": note}

    def _prepare_fresh_payload() -> dict[str, Any]:
        fresh_document, current_revision = _snapshot(source)
        if current_revision != revision:
            raise WorkspaceStateError("申请或草稿已变化；刷新后针对当前版本记录意见。")
        selection = fresh_document.get("current_selection") or {}
        return {
            "schema": "mag_review_feedback/v1",
            **identity,
            "draft_id": selection.get("active_draft_id"),
            "revision_plan_id": selection.get("active_revision_plan_id"),
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "domain_quality_approved": False,
            "handoff_stage": "review_and_rebuttal",
        }

    try:
        target, saved, _ = record_feedback_note(
            root,
            request_id=normalized_id,
            payload=identity,
            identity_keys=tuple(identity.keys()),
            root=source.parent,
            lock=True,
            before_create=_prepare_fresh_payload,
        )
    except ReviewFeedbackError as error:
        if error.reason_code == "idempotency_conflict":
            raise WorkspaceStateError("意见编号已被不同输入使用。") from error
        if error.reason_code == "symlink_not_allowed":
            raise WorkspaceStateError("审阅意见目标不能为符号链接。") from error
        raise WorkspaceStateError(str(error)) from error
    return {"ok": True, "status": "recorded", "artifact_ref": str(target), "review_note": saved,
            "matches_current_revision": _revision(source) == revision,
            "workspace_id": workspace_id, "grant_run_id": grant_run_id,
            "review_context": {"workspace_id": workspace_id, "grant_run_id": grant_run_id,
                               "draft_id": saved.get("draft_id"), "revision": revision, "source_refs": [str(source)]},
            "continuation": {"source_ref": str(source), "stage_id": "review_and_rebuttal",
                             "review_ref": str(target), "stage_execution_started": False}}


def _selected_source(root: Path, value: dict[str, Any], view: str) -> Path:
    ref = value.get("quality_path" if view == "quality" else "workspace_file") or "workspace.json"
    if not isinstance(ref, str):
        raise WorkspaceStateError("申请文件路径必须为字符串。")
    try:
        source = resolve_contained_path(root, ref, container=root, must_exist=True)
    except ReviewFeedbackError as error:
        raise WorkspaceStateError("申请文件必须位于已登记工作区内。") from error
    if not source.is_file():
        raise WorkspaceStateError("申请文件必须位于已登记工作区内。")
    return source


def read_contribution(root: Path, value: dict[str, Any], view: str) -> dict[str, Any]:
    root = root.resolve(strict=True)
    source = _selected_source(root, value, view)
    document, revision = _snapshot(source)
    raw_identity = value.get("work_item_identity") or {}
    expected_agents = (
        ("mag",) if isinstance(raw_identity, dict) and raw_identity.get("agent_id") is not None else ()
    )
    expected_domains = (
        ("med-autogrant",)
        if isinstance(raw_identity, dict) and raw_identity.get("domain_id") is not None
        else ()
    )
    try:
        identity, work_item = verify_work_item_identity(
            value,
            expected_agent_ids=expected_agents,
            expected_domain_ids=expected_domains,
            require_resolved=False,
        )
    except AppContributionError as error:
        raise WorkspaceStateError("所选任务不属于 MAG。") from error
    if work_item and work_item != document.get("workspace_id"):
        raise WorkspaceStateError("所选任务与申请工作区不一致。")
    ref = str(source.relative_to(root))
    if not document.get("workspace_id") or not document.get("grant_run_id"):
        if view != "quality":
            raise WorkspaceStateError("所选文件不是 MAG 申请工作区。")
        return {"state": "ready", "data": {"items": [{"id": ref, "title": "基金申请质量产物",
                "artifact_ref": str(source), "revision": revision, "status": "available", "source_refs": [str(source)],
                "owner_artifact": document}]}}
    selection = document.get("current_selection") or {}
    drafts = document.get("application_drafts") or []
    active_id = selection.get("active_draft_id")
    active = next((draft for draft in drafts if draft.get("draft_id") == active_id), None)
    gates = document.get("gates") or {}
    stage = document.get("lifecycle_stage", "unknown")
    defaults = {"workspace_file": ref, "workspace_id": document["workspace_id"],
                "grant_run_id": document["grant_run_id"], "revision": revision, "request_id": str(uuid.uuid4())}
    item = {"id": document["workspace_id"], "title": (active or {}).get("project_title") or document["workspace_id"],
            "summary": f"阶段：{stage} · 草稿：{(active or {}).get('version_label', active_id or '未选择')} · 预提交冻结：{'是' if gates.get('presubmission_frozen') else '否'}",
            "status": "completed" if gates.get("presubmission_frozen") else "active", "lifecycle_stage": stage,
            "workspace_id": document["workspace_id"], "grant_run_id": document["grant_run_id"],
            "active_draft_id": active_id, "active_draft": active, "gates": gates,
            "revision": revision, "source_refs": [str(source)], "read_input": {"workspace_file" if view == "route" else "quality_path": ref},
            "artifacts": [{"id": ref, "title": "申请正文与评审", "artifact_ref": str(source), "status": "available", "revision": revision}],
            "review_notes": review_notes(source, revision), "mentor_critiques": document.get("mentor_critiques", []),
            "revision_plans": document.get("revision_plans", []), "actions": [{"action_ref": NOTE_ACTION, "input": defaults}],
            "next_action": {"title": "审阅意见交回当前基金任务", "summary": "记录意见后在原任务继续；下一次 critique 读取当前版本意见。"}}
    if identity:
        item["work_item_identity"] = dict(identity)
        item["read_input"]["work_item_identity"] = dict(identity)
        item["review_context"] = {
            "work_item_identity": dict(identity), "artifact_refs": [ref],
            "artifact_hashes": [revision], "revision": revision, "source_refs": [str(source)],
        }
        for note in item["review_notes"]:
            note_ref = str(Path(note["artifact_ref"]).relative_to(root))
            note["review_context"] = {
                "work_item_identity": dict(identity), "artifact_refs": [ref, note_ref],
                "artifact_hashes": [note["revision"], note["artifact_hash"]],
                "revision": note["revision"], "source_refs": [str(source)],
            }
    return {"state": "ready", "data": {"items": [item], "command_inputs": {NOTE_ACTION: {"input_schema": NOTE_SCHEMA}},
            "domain_quality_approved": False}}
