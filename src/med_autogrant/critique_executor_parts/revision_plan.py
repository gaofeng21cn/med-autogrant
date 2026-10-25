from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from med_autogrant.workspace_types import WorkspaceStateError


EXECUTABLE_REVISION_OPERATIONS = ("replace_draft_section", "replace_draft_sections")


def normalize_revision_plan(
    *,
    critique_context: dict[str, Any],
    critique: dict[str, Any],
    payload: dict[str, Any],
    validate_revision_item: Callable[..., None],
    validate_schema_payload: Callable[..., None],
) -> dict[str, Any]:
    revision_plan = deepcopy(payload)
    revision_plan["revision_plan_id"] = critique_context["next_revision_plan_id"]
    revision_plan["draft_id"] = critique_context["draft_id"]
    revision_plan["critique_id"] = critique["critique_id"]
    revision_plan["execution_status"] = "planned"
    revision_plan["pre_revision_version_label"] = critique_context["draft_version_label"]
    revision_plan.pop("comparison_summary", None)
    post_revision_version_label = revision_plan.get("post_revision_version_label")
    if (
        not isinstance(post_revision_version_label, str)
        or not post_revision_version_label.strip()
        or post_revision_version_label == critique_context["draft_version_label"]
    ):
        raise WorkspaceStateError(
            "critique pass 生成的 post_revision_version_label 必须为新的非空版本号。",
            errors=[],
            grant_run_id=critique_context["grant_run_id"],
            workspace_id=critique_context["workspace_id"],
            lifecycle_stage=critique_context["lifecycle_stage"],
        )
    items = revision_plan.get("items")
    if not isinstance(items, list) or not items:
        raise WorkspaceStateError(
            "critique pass 生成的 RevisionPlan.items 必须为非空列表。",
            errors=[],
            grant_run_id=critique_context["grant_run_id"],
            workspace_id=critique_context["workspace_id"],
            lifecycle_stage=critique_context["lifecycle_stage"],
        )
    for item in items:
        validate_revision_item(
            item,
            section_keys=set(critique_context["section_keys"]),
            known_ids=set(critique_context["known_ids"]),
            grant_run_id=critique_context["grant_run_id"],
            workspace_id=critique_context["workspace_id"],
            lifecycle_stage=critique_context["lifecycle_stage"],
        )
    validate_schema_payload(
        revision_plan,
        schema_file="revision-plan.schema.json",
        grant_run_id=critique_context["grant_run_id"],
        workspace_id=critique_context["workspace_id"],
        lifecycle_stage=critique_context["lifecycle_stage"],
    )
    return revision_plan


def validate_revision_item(
    item: Any,
    *,
    section_keys: set[str],
    known_ids: set[str],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    executable_revision_operations: tuple[str, ...] = EXECUTABLE_REVISION_OPERATIONS,
) -> None:
    if not isinstance(item, dict):
        raise WorkspaceStateError(
            "critique pass 生成的 RevisionPlan.items[] 必须都是 object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    action_type = item.get("action_type")
    if not isinstance(action_type, str) or not action_type.strip():
        raise WorkspaceStateError(
            "critique pass 的 revision item.action_type 必须为非空专业修订标签。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    target_ref = item.get("target_ref")
    if not isinstance(target_ref, str) or not target_ref.strip():
        raise WorkspaceStateError(
            "critique pass 的 revision item.target_ref 必须为非空 artifact ref。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    mutation_payload = item.get("mutation_payload")
    if not isinstance(mutation_payload, dict):
        raise WorkspaceStateError(
            "critique pass 的 revision item 必须包含 mutation_payload。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    operation = mutation_payload.get("operation")
    if operation not in executable_revision_operations:
        raise WorkspaceStateError(
            f"critique pass 的 mutation_payload.operation 必须属于 {executable_revision_operations}。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if operation == "replace_draft_section":
        if not target_ref.startswith("section:"):
            raise WorkspaceStateError("section repair 的 target_ref 必须形如 section:<section_key>。")
        section_key = target_ref.split(":", 1)[1]
        if section_key not in section_keys:
            raise WorkspaceStateError(f"critique pass 不能把 revision item 指向不存在的 section: {section_key}")
        if mutation_payload.get("target_section_key") != section_key:
            raise WorkspaceStateError("mutation_payload.target_section_key 必须与 section target_ref 一致。")
        if not isinstance(mutation_payload.get("replacement_text"), str) or not mutation_payload["replacement_text"].strip():
            raise WorkspaceStateError("section repair 必须提供 replacement_text。")
    else:
        if not target_ref.startswith("draft:"):
            raise WorkspaceStateError("whole-draft repair 的 target_ref 必须形如 draft:<draft_id>。")
        replacement_sections = mutation_payload.get("replacement_sections")
        if not isinstance(replacement_sections, list) or not replacement_sections:
            raise WorkspaceStateError("whole-draft repair 必须提供非空 replacement_sections。")
    linked_object_ids = mutation_payload.get("linked_object_ids")
    required_input_ids = item.get("required_input_ids")
    if not isinstance(linked_object_ids, list) or not isinstance(required_input_ids, list):
        raise WorkspaceStateError(
            "critique pass 的 linked_object_ids / required_input_ids 必须为列表。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    unknown_ids = [
        ref_id
        for ref_id in linked_object_ids
        if not isinstance(ref_id, str) or not ref_id or ref_id not in known_ids
    ]
    if unknown_ids:
        raise WorkspaceStateError(
            f"critique pass 的 linked_object_ids 引用了未知对象: {unknown_ids}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    missing_required_inputs = [
        ref_id for ref_id in required_input_ids if ref_id not in linked_object_ids
    ]
    if missing_required_inputs:
        raise WorkspaceStateError(
            "critique pass 的 linked_object_ids 必须覆盖 required_input_ids。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
