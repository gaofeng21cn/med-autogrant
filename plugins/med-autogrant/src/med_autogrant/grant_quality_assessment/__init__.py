from __future__ import annotations

from typing import Any, TypeAlias

from med_autogrant.grant_quality_parts import REVIEW_CONTEXT_STAGES

QualityContext: TypeAlias = dict[str, Any]

_QUALITY_DIMENSION_SPECS: tuple[dict[str, str], ...] = (
    {
        "dimension_id": "scientific_question_validity",
        "label": "科学问题成立性",
        "rollback_stage": "question_refinement",
    },
    {
        "dimension_id": "necessity_value_closure",
        "label": "必要性与科学价值闭合度",
        "rollback_stage": "argument_building",
    },
    {
        "dimension_id": "applicant_fit",
        "label": "申请人适配度",
        "rollback_stage": "fit_alignment",
    },
    {
        "dimension_id": "technical_feasibility",
        "label": "技术路线可行性",
        "rollback_stage": "fit_alignment",
    },
    {
        "dimension_id": "claim_evidence_coverage",
        "label": "claim-evidence coverage",
        "rollback_stage": "argument_building",
    },
    {
        "dimension_id": "unresolved_hard_issues",
        "label": "未关闭硬伤",
        "rollback_stage": "revision",
    },
    {
        "dimension_id": "version_issue_closure",
        "label": "版本间问题关闭情况",
        "rollback_stage": "revision",
    },
)

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
from med_autogrant.grant_quality_assessment.dimensions import (
    _assess_applicant_fit,
    _assess_claim_evidence_coverage,
    _assess_necessity_value_closure,
    _assess_scientific_question_validity,
    _assess_technical_feasibility,
    _assess_unresolved_hard_issues,
    _assess_version_issue_closure,
    _build_dimension_assessment,
)
from med_autogrant.grant_quality_assessment.finalization import (
    _build_loop_gate,
    _build_scorecard_summary,
    _finalize_dimension,
    _resolve_dimension_status,
    _resolve_overall_status,
    _resolve_quality_progression,
)
from med_autogrant.grant_quality_assessment.issue_lineage import (
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
