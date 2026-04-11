from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from med_autogrant.workspace import (
    WorkspaceStateError,
    _collect_known_ids,
    _require_workspace_context,
    _serialize_reviewed_revision_evidence,
)


ALLOWED_ACTION_TYPES = {
    "rebuild_argument",
    "rewrite_section",
    "add_evidence",
    "tighten_fit",
}
ALLOWED_MUTATION_OPERATION = "replace_draft_section"


def build_revision_execution_document(*, document: dict[str, Any]) -> dict[str, Any]:
    context = _require_workspace_context(document)
    critique = context.active_critique
    revision_plan = context.active_revision_plan
    active_draft = context.active_draft

    _validate_execution_preconditions(document=document, critique=critique, revision_plan=revision_plan)

    section_index = _index_by_section_key(active_draft.get("sections"), scope_name="ApplicationDraft.sections")
    outline_index = _index_by_section_key(active_draft.get("outline"), scope_name="ApplicationDraft.outline")
    known_ids = _collect_known_ids(document)
    executable_items = _collect_executable_items(
        revision_plan=revision_plan,
        section_index=section_index,
        outline_index=outline_index,
        known_ids=known_ids,
    )

    revised_workspace = deepcopy(document)
    revised_draft = _find_active_draft(revised_workspace)
    revised_revision_plan = _find_active_revision_plan(revised_workspace)
    revised_workspace["lifecycle_stage"] = "critique"

    applied_section_keys: list[str] = []
    for executable_item in executable_items:
        target_section_key = executable_item["target_section_key"]
        mutation_payload = executable_item["mutation_payload"]
        section = _resolve_section(revised_draft, target_section_key)
        section["text"] = mutation_payload["replacement_text"]
        section["linked_object_ids"] = list(mutation_payload["linked_object_ids"])

        outline_item = _resolve_outline_item(revised_draft, target_section_key)
        if outline_item is not None:
            outline_item["core_claim"] = mutation_payload["replacement_core_claim"]
            outline_item["linked_object_ids"] = list(mutation_payload["linked_object_ids"])

        applied_section_keys.append(target_section_key)

    comparison_summary = _build_comparison_summary(
        revision_plan_id=revision_plan["revision_plan_id"],
        section_keys=applied_section_keys,
        pre_revision_version_label=revision_plan["pre_revision_version_label"],
        post_revision_version_label=revision_plan["post_revision_version_label"],
    )

    revised_draft["version_label"] = revision_plan["post_revision_version_label"]
    revised_draft["status"] = "revised"
    revised_revision_plan["execution_status"] = "completed"
    revised_revision_plan["comparison_summary"] = comparison_summary

    revision_execution = {
        "active_revision_plan_id": revision_plan["revision_plan_id"],
        "reviewed_revision_plan_id": critique.get("reviewed_revision_plan_id"),
        "source_critique_id": critique["critique_id"],
        "reviewed_revision_evidence": _serialize_reviewed_revision_evidence(context.reviewed_revision_plan),
        "pre_revision_version_label": revision_plan["pre_revision_version_label"],
        "post_revision_version_label": revision_plan["post_revision_version_label"],
        "comparison_summary": comparison_summary,
    }

    return {
        "grant_run_id": revised_workspace["grant_run_id"],
        "workspace_id": revised_workspace["workspace_id"],
        "draft_id": active_draft["draft_id"],
        "active_revision_plan_id": revision_plan["revision_plan_id"],
        "lifecycle_stage": revised_workspace["lifecycle_stage"],
        "revision_execution": revision_execution,
        "revised_workspace": revised_workspace,
    }


def build_revision_execution_payload(
    document: dict[str, Any],
    *,
    output_path: str | Path,
) -> dict[str, Any]:
    revision_document = build_revision_execution_document(document=document)
    resolved_output_path = Path(output_path).expanduser().resolve()
    _guard_output_identity(
        resolved_output_path,
        grant_run_id=revision_document["grant_run_id"],
        workspace_id=revision_document["workspace_id"],
        draft_id=revision_document["draft_id"],
        active_revision_plan_id=revision_document["active_revision_plan_id"],
        lifecycle_stage=revision_document["lifecycle_stage"],
    )
    _write_workspace(resolved_output_path, revision_document["revised_workspace"])
    return {
        "ok": True,
        "command": "execute-revision-pass",
        "grant_run_id": revision_document["grant_run_id"],
        "workspace_id": revision_document["workspace_id"],
        "draft_id": revision_document["draft_id"],
        "lifecycle_stage": revision_document["lifecycle_stage"],
        "output_path": str(resolved_output_path),
        "revision_execution": revision_document["revision_execution"],
        "revised_workspace": revision_document["revised_workspace"],
    }


def _validate_execution_preconditions(
    *,
    document: dict[str, Any],
    critique: dict[str, Any],
    revision_plan: dict[str, Any],
) -> None:
    verdict = critique.get("verdict")
    if critique.get("forced_rollback_stage"):
        raise WorkspaceStateError(
            "forced_rollback_stage 非空时 execute-revision-pass 必须 fail-closed。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    if bool(document.get("gates", {}).get("presubmission_frozen")):
        raise WorkspaceStateError(
            "gates.presubmission_frozen=true 时 execute-revision-pass 必须 fail-closed。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    if verdict not in {"major_revision", "minor_revision"}:
        raise WorkspaceStateError(
            "当前 active MentorCritique.verdict 必须属于 major_revision / minor_revision。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    if revision_plan.get("execution_status") != "planned":
        raise WorkspaceStateError(
            "当前 active RevisionPlan.execution_status 必须为 planned。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    pre_revision_version_label = revision_plan.get("pre_revision_version_label")
    post_revision_version_label = revision_plan.get("post_revision_version_label")
    if not isinstance(pre_revision_version_label, str) or not pre_revision_version_label:
        raise WorkspaceStateError(
            "pre_revision_version_label 缺失，无法执行 revision pass。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )
    if not isinstance(post_revision_version_label, str) or not post_revision_version_label:
        raise WorkspaceStateError(
            "post_revision_version_label 缺失，无法执行 revision pass。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )
    if pre_revision_version_label == post_revision_version_label:
        raise WorkspaceStateError(
            "pre_revision_version_label 与 post_revision_version_label 不得相同。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )


def _collect_executable_items(
    *,
    revision_plan: dict[str, Any],
    section_index: dict[str, dict[str, Any]],
    outline_index: dict[str, dict[str, Any]],
    known_ids: set[str],
) -> list[dict[str, Any]]:
    items = revision_plan.get("items")
    if not isinstance(items, list) or not items:
        raise WorkspaceStateError("当前 active RevisionPlan.items[] 必须为非空 list。")

    executable_items: list[dict[str, Any]] = []
    seen_section_keys: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise WorkspaceStateError("RevisionPlan.items[] 中存在非 object item，无法执行 deterministic mutation。")

        action_type = item.get("action_type")
        if action_type not in ALLOWED_ACTION_TYPES:
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 action_type={action_type} 不属于 section-level executable subset。"
            )

        target_ref = item.get("target_ref")
        if not isinstance(target_ref, str) or not target_ref.startswith("section:"):
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 target_ref 必须形如 section:<section_key>。"
            )
        target_section_key = target_ref.split(":", 1)[1]
        if not target_section_key:
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 target_ref 必须显式携带非空 section_key。"
            )
        if target_section_key in seen_section_keys:
            raise WorkspaceStateError(
                f"发现 duplicate target section: {target_section_key}。"
            )
        if target_section_key not in section_index:
            raise WorkspaceStateError(
                f"target section 不存在: {target_section_key}。"
            )

        mutation_payload = item.get("mutation_payload")
        if not isinstance(mutation_payload, dict):
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 缺少 mutation_payload，无法执行 deterministic mutation。"
            )
        if mutation_payload.get("operation") != ALLOWED_MUTATION_OPERATION:
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 mutation_payload.operation 必须为 {ALLOWED_MUTATION_OPERATION}。"
            )
        if mutation_payload.get("target_section_key") != target_section_key:
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 target_ref 与 mutation_payload.target_section_key 必须一致。"
            )

        replacement_text = mutation_payload.get("replacement_text")
        if not isinstance(replacement_text, str) or not replacement_text.strip():
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 mutation_payload.replacement_text 必须为非空字符串。"
            )

        linked_object_ids = mutation_payload.get("linked_object_ids")
        if (
            not isinstance(linked_object_ids, list)
            or not linked_object_ids
            or any(not isinstance(ref_id, str) or not ref_id for ref_id in linked_object_ids)
        ):
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 mutation_payload.linked_object_ids 必须为非空字符串列表。"
            )

        required_input_ids = item.get("required_input_ids")
        if not isinstance(required_input_ids, list):
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 required_input_ids 必须为 list。"
            )

        missing_required_input_ids = [ref_id for ref_id in required_input_ids if ref_id not in linked_object_ids]
        if missing_required_input_ids:
            raise WorkspaceStateError(
                (
                    f"item {item.get('item_id')} 的 mutation_payload.linked_object_ids "
                    "必须覆盖 required_input_ids。"
                )
            )

        unknown_linked_object_ids = [ref_id for ref_id in linked_object_ids if ref_id not in known_ids]
        if unknown_linked_object_ids:
            raise WorkspaceStateError(
                f"item {item.get('item_id')} 的 linked_object_ids 引用了不存在的对象: {unknown_linked_object_ids}。"
            )

        if target_section_key in outline_index:
            replacement_core_claim = mutation_payload.get("replacement_core_claim")
            if not isinstance(replacement_core_claim, str) or not replacement_core_claim.strip():
                raise WorkspaceStateError(
                    (
                        f"item {item.get('item_id')} 的 target section 已存在 outline 条目，"
                        "因此 mutation_payload.replacement_core_claim 必填。"
                    )
                )

        seen_section_keys.add(target_section_key)
        executable_items.append(
            {
                "item_id": item.get("item_id"),
                "target_section_key": target_section_key,
                "mutation_payload": mutation_payload,
            }
        )

    return executable_items


def _build_comparison_summary(
    *,
    revision_plan_id: str,
    section_keys: list[str],
    pre_revision_version_label: str,
    post_revision_version_label: str,
) -> str:
    section_list = ", ".join(section_keys)
    return (
        f"Applied revision plan {revision_plan_id}: updated sections [{section_list}]; "
        f"draft version {pre_revision_version_label} -> {post_revision_version_label}."
    )


def _find_active_draft(document: dict[str, Any]) -> dict[str, Any]:
    active_draft_id = document.get("current_selection", {}).get("active_draft_id")
    for draft in document.get("application_drafts", []):
        if isinstance(draft, dict) and draft.get("draft_id") == active_draft_id:
            return draft
    raise WorkspaceStateError("未找到 active draft，无法写入 revised workspace。")


def _find_active_revision_plan(document: dict[str, Any]) -> dict[str, Any]:
    active_revision_plan_id = document.get("current_selection", {}).get("active_revision_plan_id")
    for revision_plan in document.get("revision_plans", []):
        if isinstance(revision_plan, dict) and revision_plan.get("revision_plan_id") == active_revision_plan_id:
            return revision_plan
    raise WorkspaceStateError("未找到 active revision plan，无法写入 revised workspace。")


def _resolve_section(draft: dict[str, Any], section_key: str) -> dict[str, Any]:
    for section in draft.get("sections", []):
        if isinstance(section, dict) and section.get("section_key") == section_key:
            return section
    raise WorkspaceStateError(f"target section 不存在: {section_key}。")


def _resolve_outline_item(draft: dict[str, Any], section_key: str) -> dict[str, Any] | None:
    for item in draft.get("outline", []):
        if isinstance(item, dict) and item.get("section_key") == section_key:
            return item
    return None


def _index_by_section_key(items: Any, *, scope_name: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    if not isinstance(items, list):
        return indexed
    for item in items:
        if not isinstance(item, dict):
            raise WorkspaceStateError(f"{scope_name} 中存在非 object item。")
        section_key = item.get("section_key")
        if not isinstance(section_key, str) or not section_key:
            raise WorkspaceStateError(f"{scope_name}.section_key 必须为非空字符串。")
        if section_key in indexed:
            raise WorkspaceStateError(f"{scope_name}.section_key 不能重复: {section_key}。")
        indexed[section_key] = item
    return indexed


def _guard_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    active_revision_plan_id: str,
    lifecycle_stage: str | None,
) -> None:
    from med_autogrant.hermes_runtime import _guard_revision_output_identity as _hermes_guard_revision_output_identity

    _hermes_guard_revision_output_identity(
        output_path,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
        active_revision_plan_id=active_revision_plan_id,
        lifecycle_stage=lifecycle_stage,
    )


def _write_workspace(output_path: Path, revised_workspace: dict[str, Any]) -> None:
    from med_autogrant.hermes_runtime import _write_revised_workspace_output as _hermes_write_revised_workspace_output

    _hermes_write_revised_workspace_output(output_path, revised_workspace)
