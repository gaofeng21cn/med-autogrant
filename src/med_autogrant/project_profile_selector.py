from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any

from med_autogrant.workspace import materialize_workspace_surfaces


REQUIRED_SELECTION_INPUT_FIELDS: tuple[str, ...] = (
    "selection_input_id",
    "applicant_profile",
    "track_record",
    "active_project_set",
    "preliminary_evidence_pack",
    "funding_opportunity_pool",
)


PROJECT_PROFILE_PRESET_REGISTRY: dict[str, dict[str, Any]] = {
    "nsfc_general_medical_v1": {
        "profile_id": "profile-nsfc-general-medical",
        "preset_id": "nsfc_general_medical_v1",
        "profile_label": "NSFC general medical grant profile",
        "project_kind": "medical_grant_application",
        "template_family": "nsfc_general_medical_grant",
        "selection_mode": "preset_aligned_to_funding_opportunity",
        "summary": "面向 NSFC 医学口申请，强调科学问题提纯、立项必要性与申请人前期基础适配。",
        "template_profile": {
            "template_id": "nsfc_general_grant_template_v1",
            "template_label": "NSFC general medical grant template",
            "required_section_strategy": "mirror_funding_brief_mandatory_sections",
            "narrative_style": "science_first_mechanism_driven",
        },
        "collaboration_preferences": {
            "collaboration_mode": "applicant_led_agent_copilot",
            "author_touchpoints": [
                "direction_confirmation",
                "scientific_question_lock",
                "presubmission_freeze",
            ],
            "evidence_policy": "claim_must_bind_to_track_record_or_preliminary_evidence",
            "drafting_voice": "mentor_style_precise_academic_chinese",
        },
        "critique_policy": {
            "preset_id": "nsfc_mentor_critique_v1",
            "policy_id": "nsfc_mentor_critique_v1",
        },
        "compatibility_rules": (
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
    "nih_r21_translational_v1": {
        "profile_id": "profile-nih-r21-translational",
        "preset_id": "nih_r21_translational_v1",
        "profile_label": "NIH R21 translational profile",
        "project_kind": "translational_grant_application",
        "template_family": "nih_r21_exploratory_grant",
        "selection_mode": "preset_aligned_to_funding_opportunity",
        "summary": "面向 NIH R21 exploratory/developmental grant，强调 significance、innovation 与可落地的 exploratory aims。",
        "template_profile": {
            "template_id": "nih_r21_template_v1",
            "template_label": "NIH R21 exploratory grant template",
            "required_section_strategy": "mirror_funding_brief_mandatory_sections",
            "narrative_style": "significance_innovation_translational",
        },
        "collaboration_preferences": {
            "collaboration_mode": "agent_led_author_checkpoints",
            "author_touchpoints": [
                "aims_lock",
                "innovation_claim_lock",
                "presubmission_freeze",
            ],
            "evidence_policy": "significance_and_innovation_claims_require_direct_grounding",
            "drafting_voice": "reviewer_facing_translational_grant_style",
        },
        "critique_policy": {
            "preset_id": "nih_r21_significance_innovation_v1",
            "policy_id": "nih_r21_significance_innovation_v1",
        },
        "compatibility_rules": (
            {
                "rule_id": "rule.funder",
                "opportunity_field": "funder",
                "allowed_values": ("NIH",),
            },
            {
                "rule_id": "rule.program_family",
                "opportunity_field": "program_family",
                "allowed_values": ("NHLBI R21",),
            },
            {
                "rule_id": "rule.project_types",
                "opportunity_field": "project_types",
                "allowed_values": ("exploratory_developmental",),
            },
        ),
    },
}


def select_project_profile(selection_input: dict[str, Any]) -> dict[str, Any]:
    _validate_selection_input(selection_input)
    funding_opportunity_pool = selection_input["funding_opportunity_pool"]

    candidate_profiles: list[dict[str, Any]] = []
    compatible_candidates: list[dict[str, Any]] = []
    for preset in PROJECT_PROFILE_PRESET_REGISTRY.values():
        candidate = _build_candidate_profile(
            preset=preset,
            funding_opportunity_pool=funding_opportunity_pool,
        )
        candidate_profiles.append(candidate)
        if candidate["compatible_funding_opportunities"]:
            compatible_candidates.append(candidate)

    if not compatible_candidates:
        raise ValueError("未找到兼容的 project profile preset；selector fail-closed。")

    compatible_candidates.sort(
        key=lambda item: (
            -item["best_match_score"],
            item["preset_id"],
        )
    )
    selected_candidate = compatible_candidates[0]
    selected_opportunity = copy.deepcopy(selected_candidate["compatible_funding_opportunities"][0])
    recommended_project_profile = _build_project_profile_document(
        preset=PROJECT_PROFILE_PRESET_REGISTRY[selected_candidate["preset_id"]],
    )

    return {
        "surface_kind": "project_profile_selection",
        "selection_version": 1,
        "selection_input_id": selection_input["selection_input_id"],
        "selection_summary": {
            "decision": "selected",
            "selected_profile_preset_id": selected_candidate["preset_id"],
            "selected_funding_opportunity_id": selected_opportunity["brief_id"],
            "reason_codes": [reason["rule_id"] for reason in selected_opportunity["reasons"]],
            "evaluated_profile_preset_count": len(PROJECT_PROFILE_PRESET_REGISTRY),
            "evaluated_funding_opportunity_count": len(funding_opportunity_pool),
        },
        "recommended_project_profile": recommended_project_profile,
        "recommended_funding_opportunity": selected_opportunity["funding_opportunity"],
        "candidate_profiles": candidate_profiles,
    }


def build_initialized_intake_workspace(selection_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    selection = select_project_profile(selection_input)
    selection_input_id = _normalize_string(selection_input["selection_input_id"])
    funding_brief = copy.deepcopy(selection["recommended_funding_opportunity"])
    project_profile = copy.deepcopy(selection["recommended_project_profile"])
    workspace = {
        "metadata": _build_metadata(source_mode=_normalize_string(selection_input.get("mode")) or "auto"),
        "grant_run_id": f"grant-run-{selection_input_id}-001",
        "workspace_id": selection_input_id,
        "mode": _normalize_string(selection_input.get("mode")) or "auto",
        "lifecycle_stage": "input_intake",
        "applicant_profile": copy.deepcopy(selection_input["applicant_profile"]),
        "track_record": copy.deepcopy(selection_input["track_record"]),
        "active_project_set": copy.deepcopy(selection_input["active_project_set"]),
        "preliminary_evidence_pack": copy.deepcopy(selection_input["preliminary_evidence_pack"]),
        "project_profile": project_profile,
        "funding_opportunity_brief": funding_brief,
        "direction_hypotheses": [],
        "scientific_question_cards": [],
        "current_selection": {},
        "gates": {
            "direction_frozen": False,
            "scientific_question_frozen": False,
            "argument_chain_frozen": False,
            "fit_alignment_frozen": False,
            "outline_frozen": False,
            "presubmission_frozen": False,
        },
    }
    return materialize_workspace_surfaces(workspace), selection


def _build_candidate_profile(
    *,
    preset: dict[str, Any],
    funding_opportunity_pool: list[dict[str, Any]],
) -> dict[str, Any]:
    compatible: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    best_match_score = 0
    for opportunity in funding_opportunity_pool:
        normalized_opportunity = _normalize_funding_opportunity(opportunity)
        reasons = [
            _evaluate_rule(normalized_opportunity, rule)
            for rule in preset["compatibility_rules"]
        ]
        match_score = sum(1 for reason in reasons if reason["matched"])
        candidate = {
            "brief_id": normalized_opportunity["brief_id"],
            "match_score": match_score,
            "reasons": reasons,
            "funding_opportunity": copy.deepcopy(opportunity),
        }
        if all(reason["matched"] for reason in reasons):
            compatible.append(candidate)
            best_match_score = max(best_match_score, match_score)
        else:
            blocked.append(candidate)
    return {
        "preset_id": preset["preset_id"],
        "profile_id": preset["profile_id"],
        "profile_label": preset["profile_label"],
        "best_match_score": best_match_score,
        "compatible_funding_opportunities": compatible,
        "blocked_funding_opportunities": blocked,
    }


def _evaluate_rule(opportunity: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any]:
    observed = opportunity.get(rule["opportunity_field"])
    allowed_values = list(rule["allowed_values"])
    if isinstance(observed, list):
        matched = any(item in allowed_values for item in observed)
        observed_payload: object = list(observed)
    else:
        matched = observed in allowed_values
        observed_payload = observed
    return {
        "rule_id": rule["rule_id"],
        "field": rule["opportunity_field"],
        "matched": matched,
        "observed": observed_payload,
        "expected_any_of": allowed_values,
    }


def _build_project_profile_document(*, preset: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": _build_metadata(source_mode="auto"),
        "profile_id": preset["profile_id"],
        "preset_id": preset["preset_id"],
        "profile_label": preset["profile_label"],
        "project_kind": preset["project_kind"],
        "template_family": preset["template_family"],
        "selection_mode": preset["selection_mode"],
        "summary": preset["summary"],
        "template_profile": copy.deepcopy(preset["template_profile"]),
        "collaboration_preferences": copy.deepcopy(preset["collaboration_preferences"]),
        "critique_policy": copy.deepcopy(preset["critique_policy"]),
    }


def _build_metadata(*, source_mode: str) -> dict[str, str]:
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": "v1",
        "created_at": timestamp,
        "updated_at": timestamp,
        "source_mode": source_mode,
    }


def _validate_selection_input(selection_input: dict[str, Any]) -> None:
    if not isinstance(selection_input, dict):
        raise ValueError("selection_input 必须是 object。")
    for field in REQUIRED_SELECTION_INPUT_FIELDS:
        if field not in selection_input:
            raise ValueError(f"selection_input 缺少必填字段: {field}")
    for field in REQUIRED_SELECTION_INPUT_FIELDS[1:-1]:
        if not isinstance(selection_input[field], dict):
            raise ValueError(f"selection_input.{field} 必须是 object。")
    if not isinstance(selection_input["funding_opportunity_pool"], list) or not selection_input["funding_opportunity_pool"]:
        raise ValueError("selection_input.funding_opportunity_pool 必须是非空 object 列表。")
    for index, opportunity in enumerate(selection_input["funding_opportunity_pool"]):
        if not isinstance(opportunity, dict):
            raise ValueError(f"selection_input.funding_opportunity_pool[{index}] 必须是 object。")


def _normalize_funding_opportunity(opportunity: dict[str, Any]) -> dict[str, Any]:
    brief_id = _normalize_string(opportunity.get("brief_id"))
    if not brief_id:
        raise ValueError("funding_opportunity_pool[*].brief_id 必须是非空字符串。")
    project_types = opportunity.get("project_types") or []
    normalized_project_types = [
        _normalize_string(item)
        for item in project_types
        if _normalize_string(item)
    ]
    return {
        "brief_id": brief_id,
        "funder": _normalize_string(opportunity.get("funder")),
        "program_family": _normalize_string(opportunity.get("program_family")),
        "project_types": normalized_project_types,
    }


def _normalize_string(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()
