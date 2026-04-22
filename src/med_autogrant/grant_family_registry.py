from __future__ import annotations

import copy
from typing import Any


_PROJECT_PROFILE_PRESET_REGISTRY: dict[str, dict[str, Any]] = {
    "nsfc_general_medical_v1": {
        "grant_family": {
            "family_id": "nsfc_general_medical_family_v1",
            "family_label": "NSFC general medical grant family",
            "funder": "NSFC",
            "admission_status": "admitted",
        },
        "profile_id": "profile-nsfc-general-medical",
        "preset_id": "nsfc_general_medical_v1",
        "profile_label": "NSFC general medical grant profile",
        "project_kind": "medical_grant_application",
        "template_family": "nsfc_general_medical_grant",
        "selection_mode": "preset_aligned_to_funding_opportunity",
        "summary": "面向 NSFC 医学口申请，强调科学问题提纯、立项必要性与申请人前期基础适配。",
        "template_id": "nsfc_general_grant_template_v1",
        "template_label": "NSFC general medical grant template",
        "collaboration_mode": "applicant_led_agent_copilot",
        "author_touchpoints": (
            "direction_confirmation",
            "scientific_question_lock",
            "presubmission_freeze",
        ),
        "drafting_voice": "mentor_style_precise_academic_chinese",
        "common_grant_grammar": {
            "template_strategy": {
                "required_section_strategy": "mirror_funding_brief_mandatory_sections",
                "narrative_style": "science_first_mechanism_driven",
            },
            "review_grammar": {
                "review_focus": "scientific_rigor_and_project_feasibility",
                "critique_policy": {
                    "preset_id": "nsfc_mentor_critique_v1",
                    "policy_id": "nsfc_mentor_critique_v1",
                },
            },
            "evidence_policy": {
                "policy_id": "claim_must_bind_to_track_record_or_preliminary_evidence",
            },
            "governance_policy": {
                "default_tranche": "direction_screening_to_argument_closure",
                "preferred_stop_target": "fit_alignment_locked_before_outline",
                "quality_bar": {
                    "minimum_score": 85,
                    "blocker_policy": "zero_blocking_issues_required",
                    "required_signal_coverage": (
                        "scientific_question_clarity",
                        "mechanistic_rationale",
                        "applicant_track_record_fit",
                    ),
                },
                "rollback_bias": {
                    "default_rollback_stage": "argument_building",
                    "trigger_mode": "mechanism_first_strict",
                },
                "evidence_escalation_policy": {
                    "trigger": "mechanistic_claim_without_preliminary_support",
                    "escalation_action": "require_preliminary_validation_or_scope_downgrade",
                    "required_evidence_types": (
                        "publication",
                        "project",
                        "preliminary_result",
                    ),
                },
            },
            "family_compatibility_hooks": (
                {
                    "rule_id": "rule.funder",
                    "opportunity_field": "funder",
                    "allowed_values": ("NSFC",),
                },
                {
                    "rule_id": "rule.program_family",
                    "opportunity_field": "program_family",
                    "allowed_values": ("医学科学部",),
                },
            ),
        },
    },
    "nih_r21_translational_v1": {
        "grant_family": {
            "family_id": "nih_r21_translational_family_v1",
            "family_label": "NIH R21 translational family",
            "funder": "NIH",
            "admission_status": "admitted",
        },
        "profile_id": "profile-nih-r21-translational",
        "preset_id": "nih_r21_translational_v1",
        "profile_label": "NIH R21 translational profile",
        "project_kind": "translational_grant_application",
        "template_family": "nih_r21_exploratory_grant",
        "selection_mode": "preset_aligned_to_funding_opportunity",
        "summary": "面向 NIH R21 exploratory/developmental grant，强调 significance、innovation 与可落地的 exploratory aims。",
        "template_id": "nih_r21_template_v1",
        "template_label": "NIH R21 exploratory grant template",
        "collaboration_mode": "agent_led_author_checkpoints",
        "author_touchpoints": (
            "aims_lock",
            "innovation_claim_lock",
            "presubmission_freeze",
        ),
        "drafting_voice": "reviewer_facing_translational_grant_style",
        "common_grant_grammar": {
            "template_strategy": {
                "required_section_strategy": "mirror_funding_brief_mandatory_sections",
                "narrative_style": "significance_innovation_translational",
            },
            "review_grammar": {
                "review_focus": "significance_and_innovation_weighted_review",
                "critique_policy": {
                    "preset_id": "nih_r21_significance_innovation_v1",
                    "policy_id": "nih_r21_significance_innovation_v1",
                },
            },
            "evidence_policy": {
                "policy_id": "significance_and_innovation_claims_require_direct_grounding",
            },
            "governance_policy": {
                "default_tranche": "aims_significance_innovation_loop",
                "preferred_stop_target": "ready_for_submission_after_significance_innovation_lock",
                "quality_bar": {
                    "minimum_score": 78,
                    "blocker_policy": "critical_blockers_must_close",
                    "required_signal_coverage": (
                        "significance",
                        "innovation",
                        "approach_feasibility",
                    ),
                },
                "rollback_bias": {
                    "default_rollback_stage": "fit_alignment",
                    "trigger_mode": "innovation_gap_sensitive",
                },
                "evidence_escalation_policy": {
                    "trigger": "significance_or_innovation_claim_unbounded",
                    "escalation_action": "tighten_aim_scope_and_add_translational_anchor",
                    "required_evidence_types": (
                        "publication",
                        "preliminary_result",
                    ),
                },
            },
            "family_compatibility_hooks": (
                {
                    "rule_id": "rule.funder",
                    "opportunity_field": "funder",
                    "allowed_values": ("NIH",),
                },
                {
                    "rule_id": "rule.program_family",
                    "opportunity_field": "program_family",
                    "allowed_values": ("NHLBI R21", "NIH R21 Parent"),
                },
                {
                    "rule_id": "rule.project_types",
                    "opportunity_field": "project_types",
                    "allowed_values": ("exploratory_developmental",),
                },
            ),
        },
    },
}


_FAMILY_PROFILE_PLACEHOLDERS: tuple[dict[str, Any], ...] = (
    {
        "family_id": "wellcome_discovery_placeholder_v1",
        "family_label": "Wellcome discovery placeholder",
        "funder": "Wellcome",
        "status": "placeholder",
        "common_grant_grammar": {
            "template_strategy": {
                "required_section_strategy": "mirror_funding_brief_mandatory_sections",
                "narrative_style": "high_risk_high_gain_problem_focused",
            },
            "review_grammar": {
                "review_focus": "transformative_potential_and_execution_readiness",
                "critique_policy": {
                    "preset_id": "wellcome_discovery_placeholder_critique_v1",
                    "policy_id": "wellcome_discovery_placeholder_critique_v1",
                },
            },
            "evidence_policy": {
                "policy_id": "claims_require_milestone_linked_evidence",
            },
            "governance_policy": {
                "default_tranche": "discovery_framing_first",
                "preferred_stop_target": "transformative_hypothesis_locked",
                "quality_bar": {
                    "minimum_score": 80,
                    "blocker_policy": "transformative_value_and_execution_risk_balanced",
                    "required_signal_coverage": (
                        "transformative_potential",
                        "execution_readiness",
                    ),
                },
                "rollback_bias": {
                    "default_rollback_stage": "question_refinement",
                    "trigger_mode": "novelty_execution_balance",
                },
                "evidence_escalation_policy": {
                    "trigger": "high_risk_claim_without_milestone_anchor",
                    "escalation_action": "add_milestone_guardrails_or_reduce_scope",
                    "required_evidence_types": (
                        "publication",
                        "project",
                    ),
                },
            },
            "family_compatibility_hooks": (
                {
                    "rule_id": "rule.funder",
                    "opportunity_field": "funder",
                    "allowed_values": ("Wellcome",),
                },
            ),
        },
    },
)


def iter_project_profile_presets() -> tuple[dict[str, Any], ...]:
    return tuple(copy.deepcopy(preset) for preset in _PROJECT_PROFILE_PRESET_REGISTRY.values())


def get_project_profile_preset(preset_id: str) -> dict[str, Any]:
    preset = _PROJECT_PROFILE_PRESET_REGISTRY.get(preset_id)
    if preset is None:
        raise KeyError(f"未知 project profile preset: {preset_id}")
    return copy.deepcopy(preset)


def list_family_profile_placeholders() -> tuple[dict[str, Any], ...]:
    return tuple(copy.deepcopy(item) for item in _FAMILY_PROFILE_PLACEHOLDERS)
