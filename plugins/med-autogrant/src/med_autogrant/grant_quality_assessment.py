from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.grant_quality_parts import (
    _dedupe_preserve_order,
    _ensure_mapping,
    _flatten_to_strings,
    _nonempty_string,
    _read_nested_string_list,
    _read_nonempty_string_list,
    _safe_int,
    _stable_digest,
)
from med_autogrant.grant_quality_assessment_parts import (
    REVIEW_CONTEXT_STAGES,
    _QUALITY_DIMENSION_SPECS,
)
from med_autogrant.grant_quality_assessment_parts.dimensions import (
    _assess_applicant_fit,
    _assess_claim_evidence_coverage,
    _assess_necessity_value_closure,
    _assess_scientific_question_validity,
    _assess_technical_feasibility,
    _assess_unresolved_hard_issues,
    _assess_version_issue_closure,
    _build_dimension_assessment,
)
from med_autogrant.grant_quality_assessment_parts.finalization import (
    _build_loop_gate,
    _build_scorecard_summary,
    _finalize_dimension,
    _resolve_dimension_status,
    _resolve_overall_status,
    _resolve_quality_progression,
)
from med_autogrant.grant_quality_assessment_parts.issue_lineage import (
    _active_revision_plan,
    _build_issue,
    _build_issue_evidence_obligations,
    _build_issue_lineage_basis,
    _build_issue_lineage_id,
    _build_recommended_closure_action,
    _default_obligation_input_ids,
    _dimension_repair_summaries,
    _read_object_id,
    _relevant_revision_items,
    _required_input_anchor_ref,
)
