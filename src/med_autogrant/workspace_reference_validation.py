from __future__ import annotations

from typing import Any

from med_autogrant.workspace_types import ValidationIssue

def _validate_reference_sets(document: dict[str, Any], issues: list[ValidationIssue]) -> None:
    known_ids = _collect_known_ids(document)
    fields_to_scan = [
        ("direction_hypotheses", "required_evidence_ids"),
        ("scientific_question_cards", "linked_evidence_ids"),
        ("argument_chains", "linked_evidence_ids"),
        ("applicant_fit_mappings", "linked_evidence_ids"),
        ("application_drafts", "outline", "linked_object_ids"),
        ("application_drafts", "sections", "linked_object_ids"),
        ("revision_plans", "items", "required_input_ids"),
        ("preliminary_evidence_pack", "evidence_items", "supports"),
    ]
    for spec in fields_to_scan:
        if len(spec) == 2:
            collection_name, field_name = spec
            for index, item in enumerate(document.get(collection_name, [])):
                if not isinstance(item, dict):
                    continue
                _validate_reference_list(
                    item.get(field_name),
                    known_ids,
                    f"{collection_name}[{index}].{field_name}",
                    issues,
                )
            continue

        parent_name, collection_name, field_name = spec
        parent = document.get(parent_name)
        if isinstance(parent, list):
            parents = parent
        elif isinstance(parent, dict):
            parents = [parent]
        else:
            parents = []
        for parent_index, parent_item in enumerate(parents):
            nested_items = parent_item.get(collection_name, []) if isinstance(parent_item, dict) else []
            for index, item in enumerate(nested_items):
                if not isinstance(item, dict):
                    continue
                _validate_reference_list(
                    item.get(field_name),
                    known_ids,
                    f"{parent_name}[{parent_index}].{collection_name}[{index}].{field_name}",
                    issues,
                )

def _validate_reference_list(
    values: Any,
    known_ids: set[str],
    path: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(values, list):
        return
    for index, ref_id in enumerate(values):
        if isinstance(ref_id, str) and ref_id not in known_ids:
            issues.append(
                ValidationIssue(
                    path=f"{path}[{index}]",
                    message="引用了不存在的对象或证据 ID。",
                )
            )

def _collect_known_ids(document: dict[str, Any]) -> set[str]:
    known_ids: set[str] = set()

    def add_id(value: Any) -> None:
        if isinstance(value, str) and value:
            known_ids.add(value)

    collections = [
        ("direction_hypotheses", "direction_id"),
        ("scientific_question_cards", "question_id"),
        ("argument_chains", "argument_chain_id"),
        ("applicant_fit_mappings", "fit_mapping_id"),
        ("application_drafts", "draft_id"),
        ("mentor_critiques", "critique_id"),
        ("revision_plans", "revision_plan_id"),
    ]
    for collection_name, key in collections:
        for item in document.get(collection_name, []):
            if isinstance(item, dict):
                add_id(item.get(key))

    for output in document.get("track_record", {}).get("representative_outputs", []):
        if isinstance(output, dict):
            add_id(output.get("output_id"))
            evidence = output.get("evidence")
            if isinstance(evidence, dict):
                add_id(evidence.get("evidence_id"))

    for project in document.get("active_project_set", {}).get("projects", []):
        if isinstance(project, dict):
            add_id(project.get("project_id"))
            for evidence in project.get("linked_evidence", []):
                if isinstance(evidence, dict):
                    add_id(evidence.get("evidence_id"))

    for evidence_item in document.get("preliminary_evidence_pack", {}).get("evidence_items", []):
        if isinstance(evidence_item, dict):
            add_id(evidence_item.get("item_id"))
            evidence = evidence_item.get("evidence")
            if isinstance(evidence, dict):
                add_id(evidence.get("evidence_id"))

    return known_ids

def _draft_links_argument_chain(draft: dict[str, Any], argument_chain_id: str) -> bool:
    for section_group in ("outline", "sections"):
        for item in draft.get(section_group, []):
            if not isinstance(item, dict):
                continue
            linked_ids = item.get("linked_object_ids", [])
            if isinstance(linked_ids, list) and argument_chain_id in linked_ids:
                return True
    return False

def _draft_links_fit_mapping(draft: dict[str, Any], fit_mapping_id: str) -> bool:
    for section_group in ("outline", "sections"):
        for item in draft.get(section_group, []):
            if not isinstance(item, dict):
                continue
            linked_ids = item.get("linked_object_ids", [])
            if isinstance(linked_ids, list) and fit_mapping_id in linked_ids:
                return True
    return False

def _draft_sections_link_object(draft: dict[str, Any], object_id: str) -> bool:
    for item in draft.get("sections", []):
        if not isinstance(item, dict):
            continue
        linked_ids = item.get("linked_object_ids", [])
        if isinstance(linked_ids, list) and object_id in linked_ids:
            return True
    return False


__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
