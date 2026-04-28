from __future__ import annotations

from typing import Any

from med_autogrant.workspace import WorkspaceStateError


REQUIRED_ARTIFACT_BUNDLE_OBJECT_FIELDS = (
    "selection",
    "manifest",
    "lineage",
    "bundle_summary",
    "artifacts",
)
REQUIRED_ARTIFACT_BUNDLE_NESTED_FIELDS = {
    "selection": (
        "selected_direction_id",
        "selected_question_id",
        "active_fit_mapping_id",
        "active_draft_id",
    ),
    "manifest": (
        "direction_id",
        "question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
        "draft_version_label",
        "draft_status",
    ),
    "lineage": (
        "frozen_question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
    ),
    "bundle_summary": (
        "outline_count",
        "section_count",
    ),
    "artifacts": (
        "selected_direction",
        "selected_question",
        "argument_chain",
        "fit_mapping",
        "draft_outline",
        "draft_sections",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_STRING_NESTED_FIELDS = {
    "selection": (
        "selected_direction_id",
        "selected_question_id",
        "active_fit_mapping_id",
        "active_draft_id",
    ),
    "manifest": (
        "direction_id",
        "question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
        "draft_version_label",
        "draft_status",
    ),
    "lineage": (
        "frozen_question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_NONNEGATIVE_INT_NESTED_FIELDS = {
    "bundle_summary": (
        "outline_count",
        "section_count",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_LIST_NESTED_FIELDS = {
    "artifacts": (
        "draft_outline",
        "draft_sections",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_FIELDS = {
    "draft_outline": (
        "section_key",
        "section_title",
        "core_claim",
        "linked_object_ids",
    ),
    "draft_sections": (
        "section_key",
        "section_title",
        "text",
        "linked_object_ids",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_STRING_FIELDS = {
    "draft_outline": (
        "section_key",
        "section_title",
        "core_claim",
    ),
    "draft_sections": (
        "section_key",
        "section_title",
        "text",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_LIST_FIELDS = {
    "draft_outline": (
        "linked_object_ids",
    ),
    "draft_sections": (
        "linked_object_ids",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_LIST_ELEMENT_STRING_FIELDS = {
    "draft_outline": (
        "linked_object_ids",
    ),
    "draft_sections": (
        "linked_object_ids",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_DICT_NESTED_FIELDS = {
    "artifacts": (
        "selected_direction",
        "selected_question",
        "argument_chain",
        "fit_mapping",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS = {
    "selected_direction": "direction_id",
    "selected_question": "question_id",
    "argument_chain": "argument_chain_id",
    "fit_mapping": "fit_mapping_id",
}
REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS = {
    "selected_question": (
        "parent_direction_id",
    ),
    "argument_chain": (
        "scientific_question_id",
    ),
    "fit_mapping": (
        "scientific_question_id",
        "argument_chain_id",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS = {
    "selected_direction": (
        "title",
        "rationale",
        "knowledge_gap_summary",
        "applicant_fit_summary",
        "novelty_angle",
        "risk_summary",
        "decision_status",
    ),
    "selected_question": (
        "phenomenon",
        "knowledge_boundary",
        "unknown_mechanism",
        "core_question",
        "falsifiable_statement",
        "proposed_breakthrough_angle",
        "why_not_engineering",
        "why_now",
    ),
    "argument_chain": (
        "background_claim",
        "field_gap",
        "necessity_claim",
        "uniqueness_claim",
        "route_justification",
        "non_arbitrary_route_reason",
        "if_not_done_loss",
    ),
    "fit_mapping": (
        "applicant_fit_summary",
        "unique_advantage",
        "methods_readiness",
        "resource_readiness",
        "risk_mitigation",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_LIST_FIELDS = {
    "selected_direction": (
        "required_evidence_ids",
    ),
    "selected_question": (
        "subquestions",
        "linked_evidence_ids",
    ),
    "argument_chain": (
        "linked_evidence_ids",
    ),
    "fit_mapping": (
        "linked_evidence_ids",
    ),
}


def _validate_required_artifact_bundle_fields(
    artifact_bundle: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str | None,
) -> None:
    bundle_lifecycle_stage = artifact_bundle.get("lifecycle_stage")
    if not isinstance(bundle_lifecycle_stage, str) or not bundle_lifecycle_stage:
        raise WorkspaceStateError(
            "artifact bundle 缺少必填字段: lifecycle_stage",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    for field in REQUIRED_ARTIFACT_BUNDLE_OBJECT_FIELDS:
        value = artifact_bundle.get(field)
        if not isinstance(value, dict):
            raise WorkspaceStateError(
                f"artifact bundle 缺少必填字段: {field}",
                errors=[],
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            if required_field not in nested_payload:
                raise WorkspaceStateError(
                    f"artifact bundle {object_field} 缺少字段: {required_field}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_STRING_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, str) or not value:
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_NONNEGATIVE_INT_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_LIST_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, list):
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    artifacts_payload = artifact_bundle["artifacts"]
    for list_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_FIELDS.items():
        for index, value in enumerate(artifacts_payload[list_field]):
            if not isinstance(value, dict):
                raise WorkspaceStateError(
                    f"artifact bundle artifacts.{list_field}[{index}] 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )
            for required_field in required_fields:
                if required_field not in value:
                    raise WorkspaceStateError(
                        f"artifact bundle artifacts.{list_field}[{index}] 缺少字段: {required_field}",
                        errors=[],
                        grant_run_id=grant_run_id,
                        workspace_id=workspace_id,
                        lifecycle_stage=lifecycle_stage,
                    )

    for list_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_STRING_FIELDS.items():
        for index, value in enumerate(artifacts_payload[list_field]):
            for required_field in required_fields:
                field_value = value.get(required_field)
                if not isinstance(field_value, str) or not field_value:
                    raise WorkspaceStateError(
                        f"artifact bundle artifacts.{list_field}[{index}].{required_field} 非法: {field_value}",
                        errors=[],
                        grant_run_id=grant_run_id,
                        workspace_id=workspace_id,
                        lifecycle_stage=lifecycle_stage,
                    )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_DICT_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, dict):
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for list_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_LIST_FIELDS.items():
        for index, value in enumerate(artifacts_payload[list_field]):
            for required_field in required_fields:
                field_value = value.get(required_field)
                if not isinstance(field_value, list):
                    raise WorkspaceStateError(
                        f"artifact bundle artifacts.{list_field}[{index}].{required_field} 非法: {field_value}",
                        errors=[],
                        grant_run_id=grant_run_id,
                        workspace_id=workspace_id,
                        lifecycle_stage=lifecycle_stage,
                    )

    for list_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_LIST_ELEMENT_STRING_FIELDS.items():
        for index, value in enumerate(artifacts_payload[list_field]):
            for required_field in required_fields:
                field_value = value.get(required_field)
                for nested_index, nested_value in enumerate(field_value):
                    if not isinstance(nested_value, str) or not nested_value:
                        raise WorkspaceStateError(
                            (
                                f"artifact bundle artifacts.{list_field}[{index}]."
                                f"{required_field}[{nested_index}] 非法: {nested_value}"
                            ),
                            errors=[],
                            grant_run_id=grant_run_id,
                            workspace_id=workspace_id,
                            lifecycle_stage=lifecycle_stage,
                        )

    for object_field, nested_field in REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS.items():
        value = artifacts_payload[object_field].get(nested_field)
        if not isinstance(value, str) or not value:
            raise WorkspaceStateError(
                f"artifact bundle artifacts.{object_field}.{nested_field} 非法: {value}",
                errors=[],
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )

    for object_field, nested_fields in REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS.items():
        for nested_field in nested_fields:
            value = artifacts_payload[object_field].get(nested_field)
            if not isinstance(value, str) or not value:
                raise WorkspaceStateError(
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, nested_fields in REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS.items():
        for nested_field in nested_fields:
            value = artifacts_payload[object_field].get(nested_field)
            if not isinstance(value, str) or not value:
                raise WorkspaceStateError(
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, nested_fields in REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_LIST_FIELDS.items():
        for nested_field in nested_fields:
            value = artifacts_payload[object_field].get(nested_field)
            if not isinstance(value, list):
                raise WorkspaceStateError(
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )
            for index, nested_value in enumerate(value):
                if not isinstance(nested_value, str) or not nested_value:
                    raise WorkspaceStateError(
                        f"artifact bundle artifacts.{object_field}.{nested_field}[{index}] 非法: {nested_value}",
                        errors=[],
                        grant_run_id=grant_run_id,
                        workspace_id=workspace_id,
                        lifecycle_stage=lifecycle_stage,
                    )

