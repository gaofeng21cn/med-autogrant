from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_DIRECTION_STAGES = {
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
}
_QUESTION_STAGES = {
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
}
_ARGUMENT_CHAIN_STAGES = {
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
}
_FIT_MAPPING_STAGES = {"fit_alignment", "outline", "drafting", "critique", "revision", "frozen"}
_DRAFT_STAGES = {"outline", "drafting", "critique", "revision", "frozen"}
_REVISION_PLAN_STAGES = {"critique", "revision", "frozen"}
_DIRECTION_COUNT_STAGES = {"direction_screening", "question_refinement"}


@dataclass(frozen=True)
class _WorkspaceRuntimeRequirements:
    direction: bool
    question: bool
    argument_chain: bool
    fit_mapping: bool
    draft: bool
    revision_plan: bool
    direction_count: bool


def _requirements_for_stage(stage: Any) -> _WorkspaceRuntimeRequirements:
    return _WorkspaceRuntimeRequirements(
        direction=stage in _DIRECTION_STAGES,
        question=stage in _QUESTION_STAGES,
        argument_chain=stage in _ARGUMENT_CHAIN_STAGES,
        fit_mapping=stage in _FIT_MAPPING_STAGES,
        draft=stage in _DRAFT_STAGES,
        revision_plan=stage in _REVISION_PLAN_STAGES,
        direction_count=stage in _DIRECTION_COUNT_STAGES,
    )


__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
