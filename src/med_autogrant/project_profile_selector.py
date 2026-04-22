from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any

from med_autogrant.grant_family_registry import (
    get_project_profile_preset,
    iter_project_profile_presets,
)
from med_autogrant.workspace import materialize_workspace_surfaces


REQUIRED_SELECTION_INPUT_FIELDS: tuple[str, ...] = (
    "selection_input_id",
    "applicant_profile",
    "track_record",
    "active_project_set",
    "preliminary_evidence_pack",
    "funding_opportunity_pool",
)
GOVERNANCE_ENTRY_POINTS: tuple[str, ...] = (
    "grant-quality-scorecard",
    "grant-quality-diff",
    "execute-grant-autonomy-controller",
)


def select_project_profile(selection_input: dict[str, Any]) -> dict[str, Any]:
    _validate_selection_input(selection_input)
    funding_opportunity_pool = selection_input["funding_opportunity_pool"]
    preset_registry = iter_project_profile_presets()

    candidate_profiles: list[dict[str, Any]] = []
    compatible_candidates: list[dict[str, Any]] = []
    for preset in preset_registry:
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
    selected_preset = get_project_profile_preset(selected_candidate["preset_id"])
    recommended_project_profile = _build_project_profile_document(preset=selected_preset)

    return {
        "surface_kind": "project_profile_selection",
        "selection_version": 1,
        "selection_input_id": selection_input["selection_input_id"],
        "selection_summary": {
            "decision": "selected",
            "selected_profile_preset_id": selected_candidate["preset_id"],
            "selected_funding_opportunity_id": selected_opportunity["brief_id"],
            "reason_codes": [reason["rule_id"] for reason in selected_opportunity["reasons"]],
            "evaluated_profile_preset_count": len(preset_registry),
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
    compatibility_hooks = preset["common_grant_grammar"]["family_compatibility_hooks"]
    for opportunity in funding_opportunity_pool:
        normalized_opportunity = _normalize_funding_opportunity(opportunity)
        reasons = [
            _evaluate_rule(normalized_opportunity, rule)
            for rule in compatibility_hooks
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
    common_grammar = preset["common_grant_grammar"]
    template_strategy = common_grammar["template_strategy"]
    review_grammar = common_grammar["review_grammar"]
    evidence_policy = common_grammar["evidence_policy"]
    return {
        "metadata": _build_metadata(source_mode="auto"),
        "profile_id": preset["profile_id"],
        "preset_id": preset["preset_id"],
        "profile_label": preset["profile_label"],
        "project_kind": preset["project_kind"],
        "template_family": preset["template_family"],
        "selection_mode": preset["selection_mode"],
        "summary": preset["summary"],
        "grant_family_grammar": _build_grant_family_grammar(preset),
        "family_grammar_trace": _build_family_grammar_trace(preset),
        "template_profile": {
            "template_id": preset["template_id"],
            "template_label": preset["template_label"],
            "required_section_strategy": template_strategy["required_section_strategy"],
            "narrative_style": template_strategy["narrative_style"],
        },
        "collaboration_preferences": {
            "collaboration_mode": preset["collaboration_mode"],
            "author_touchpoints": list(preset["author_touchpoints"]),
            "evidence_policy": evidence_policy["policy_id"],
            "drafting_voice": preset["drafting_voice"],
        },
        "critique_policy": copy.deepcopy(review_grammar["critique_policy"]),
    }


def _build_grant_family_grammar(preset: dict[str, Any]) -> dict[str, Any]:
    family_trace = _build_family_grammar_trace(preset)
    family_trace["governance_entry_points"] = list(GOVERNANCE_ENTRY_POINTS)
    return family_trace


def _build_family_grammar_trace(preset: dict[str, Any]) -> dict[str, Any]:
    grant_family = preset["grant_family"]
    common_grammar = preset["common_grant_grammar"]
    review_grammar = common_grammar["review_grammar"]
    return {
        "family_id": grant_family["family_id"],
        "family_label": grant_family["family_label"],
        "funder": grant_family["funder"],
        "admission_status": grant_family["admission_status"],
        "template_strategy": copy.deepcopy(common_grammar["template_strategy"]),
        "review_grammar": {
            "review_focus": review_grammar["review_focus"],
            "critique_policy": copy.deepcopy(review_grammar["critique_policy"]),
        },
        "evidence_policy": copy.deepcopy(common_grammar["evidence_policy"]),
        "governance_policy": _build_governance_policy(common_grammar["governance_policy"]),
        "family_compatibility_hooks": [
            {
                "rule_id": item["rule_id"],
                "opportunity_field": item["opportunity_field"],
                "allowed_values": list(item["allowed_values"]),
            }
            for item in common_grammar["family_compatibility_hooks"]
        ],
        "governance_entry_points": list(GOVERNANCE_ENTRY_POINTS),
    }


def _build_governance_policy(governance_policy: dict[str, Any]) -> dict[str, Any]:
    quality_bar = governance_policy["quality_bar"]
    evidence_escalation_policy = governance_policy["evidence_escalation_policy"]
    return {
        "default_tranche": _normalize_string(governance_policy["default_tranche"]),
        "preferred_stop_target": _normalize_string(governance_policy["preferred_stop_target"]),
        "quality_bar": {
            "minimum_score": int(quality_bar["minimum_score"]),
            "blocker_policy": _normalize_string(quality_bar["blocker_policy"]),
            "required_signal_coverage": [
                _normalize_string(item)
                for item in quality_bar["required_signal_coverage"]
                if _normalize_string(item)
            ],
        },
        "rollback_bias": {
            "default_rollback_stage": _normalize_string(governance_policy["rollback_bias"]["default_rollback_stage"]),
            "trigger_mode": _normalize_string(governance_policy["rollback_bias"]["trigger_mode"]),
        },
        "evidence_escalation_policy": {
            "trigger": _normalize_string(evidence_escalation_policy["trigger"]),
            "escalation_action": _normalize_string(evidence_escalation_policy["escalation_action"]),
            "required_evidence_types": [
                _normalize_string(item)
                for item in evidence_escalation_policy["required_evidence_types"]
                if _normalize_string(item)
            ],
        },
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
