"""Compatibility facade for the authoring stage builders."""

from __future__ import annotations

from .argument_building import build_argument_building_execution_document
from .direction_screening import build_direction_screening_execution_document
from .drafting import build_drafting_execution_document
from .fit_alignment import build_fit_alignment_execution_document
from .outline import build_outline_execution_document
from .question_refinement import build_question_refinement_execution_document

__all__ = [
    "build_argument_building_execution_document",
    "build_direction_screening_execution_document",
    "build_drafting_execution_document",
    "build_fit_alignment_execution_document",
    "build_outline_execution_document",
    "build_question_refinement_execution_document",
]
