from __future__ import annotations

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from med_autogrant.workspace_types import WorkspaceStateError

NonEmptyStr = Annotated[str, Field(strict=True, min_length=1)]
NonNegativeStrictInt = Annotated[int, Field(strict=True, ge=0)]
NonEmptyStrList = Annotated[list[NonEmptyStr], Field(strict=True)]


class _StrictClosedModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class _StrictOpenModel(BaseModel):
    model_config = ConfigDict(extra="allow", strict=True)


class ArtifactBundleSelection(_StrictClosedModel):
    selected_direction_id: NonEmptyStr
    selected_question_id: NonEmptyStr
    active_fit_mapping_id: NonEmptyStr
    active_draft_id: NonEmptyStr


class ArtifactBundleManifest(_StrictOpenModel):
    direction_id: NonEmptyStr
    question_id: NonEmptyStr
    argument_chain_id: NonEmptyStr
    fit_mapping_id: NonEmptyStr
    draft_id: NonEmptyStr
    draft_version_label: NonEmptyStr
    draft_status: NonEmptyStr


class ArtifactBundleLineage(_StrictClosedModel):
    frozen_question_id: NonEmptyStr
    argument_chain_id: NonEmptyStr
    fit_mapping_id: NonEmptyStr
    draft_id: NonEmptyStr


class ArtifactBundleSummary(_StrictClosedModel):
    outline_count: NonNegativeStrictInt
    section_count: NonNegativeStrictInt


class DraftOutlineItem(_StrictOpenModel):
    section_key: NonEmptyStr
    section_title: NonEmptyStr
    core_claim: NonEmptyStr
    linked_object_ids: NonEmptyStrList


class DraftSectionItem(_StrictOpenModel):
    section_key: NonEmptyStr
    section_title: NonEmptyStr
    text: NonEmptyStr
    linked_object_ids: NonEmptyStrList


class SelectedDirectionArtifact(_StrictOpenModel):
    direction_id: NonEmptyStr
    title: NonEmptyStr
    rationale: NonEmptyStr
    knowledge_gap_summary: NonEmptyStr
    applicant_fit_summary: NonEmptyStr
    novelty_angle: NonEmptyStr
    risk_summary: NonEmptyStr
    decision_status: NonEmptyStr
    required_evidence_ids: NonEmptyStrList


class SelectedQuestionArtifact(_StrictOpenModel):
    question_id: NonEmptyStr
    parent_direction_id: NonEmptyStr
    phenomenon: NonEmptyStr
    knowledge_boundary: NonEmptyStr
    unknown_mechanism: NonEmptyStr
    core_question: NonEmptyStr
    falsifiable_statement: NonEmptyStr
    proposed_breakthrough_angle: NonEmptyStr
    why_not_engineering: NonEmptyStr
    why_now: NonEmptyStr
    subquestions: NonEmptyStrList
    linked_evidence_ids: NonEmptyStrList


class ArgumentChainArtifact(_StrictOpenModel):
    argument_chain_id: NonEmptyStr
    scientific_question_id: NonEmptyStr
    background_claim: NonEmptyStr
    field_gap: NonEmptyStr
    necessity_claim: NonEmptyStr
    uniqueness_claim: NonEmptyStr
    route_justification: NonEmptyStr
    non_arbitrary_route_reason: NonEmptyStr
    if_not_done_loss: NonEmptyStr
    linked_evidence_ids: NonEmptyStrList


class FitMappingArtifact(_StrictOpenModel):
    fit_mapping_id: NonEmptyStr
    scientific_question_id: NonEmptyStr
    argument_chain_id: NonEmptyStr
    applicant_fit_summary: NonEmptyStr
    unique_advantage: NonEmptyStr
    methods_readiness: NonEmptyStr
    resource_readiness: NonEmptyStr
    risk_mitigation: NonEmptyStr
    linked_evidence_ids: NonEmptyStrList


class ArtifactBundleArtifacts(_StrictClosedModel):
    selected_direction: SelectedDirectionArtifact
    selected_question: SelectedQuestionArtifact
    argument_chain: ArgumentChainArtifact
    fit_mapping: FitMappingArtifact
    draft_outline: Annotated[list[DraftOutlineItem], Field(strict=True)]
    draft_sections: Annotated[list[DraftSectionItem], Field(strict=True)]


class ArtifactBundleRequiredPayload(_StrictOpenModel):
    lifecycle_stage: NonEmptyStr
    selection: ArtifactBundleSelection
    manifest: ArtifactBundleManifest
    lineage: ArtifactBundleLineage
    bundle_summary: ArtifactBundleSummary
    artifacts: ArtifactBundleArtifacts


def _format_loc(loc: tuple[int | str, ...]) -> str:
    parts: list[str] = []
    for segment in loc:
        if isinstance(segment, int):
            parts[-1] = f"{parts[-1]}[{segment}]"
        else:
            parts.append(segment)
    return ".".join(parts)


def _format_bundle_validation_error(error: dict[str, Any]) -> str:
    loc = tuple(error.get("loc", ()))
    err_type = error.get("type", "")
    if len(loc) == 1:
        return f"artifact bundle 缺少必填字段: {loc[0]}"
    if err_type == "missing" and (
        len(loc) == 2 or (len(loc) == 4 and isinstance(loc[2], int))
    ):
        return f"artifact bundle {_format_loc(loc[:-1])} 缺少字段: {loc[-1]}"
    observed = None if err_type == "missing" else error.get("input")
    return f"artifact bundle {_format_loc(loc)} 非法: {observed}"


def _validate_required_artifact_bundle_fields(
    artifact_bundle: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str | None,
) -> None:
    try:
        ArtifactBundleRequiredPayload.model_validate(artifact_bundle)
    except ValidationError as exc:
        first_error = exc.errors()[0]
        raise WorkspaceStateError(
            _format_bundle_validation_error(first_error),
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
