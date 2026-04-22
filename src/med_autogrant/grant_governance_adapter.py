from __future__ import annotations

from copy import deepcopy
from typing import Any


_BASE_STAGE_PRIORITY = {
    "direction_screening": 0,
    "question_refinement": 1,
    "argument_building": 2,
    "fit_alignment": 3,
    "outline": 4,
    "drafting": 5,
    "critique": 6,
    "revision": 7,
    "frozen": 8,
}
_CLOSURE_ACTION_PRIORITY = {
    "fail_closed": 0,
    "reselect_project_profile": 1,
    "rollback_upstream": 2,
    "continue_mainline": 3,
}


def build_family_governance_surface(workspace: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(workspace, dict):
        return {}
    project_profile = workspace.get("project_profile")
    if not isinstance(project_profile, dict):
        return {}
    family_grammar = project_profile.get("grant_family_grammar")
    if not isinstance(family_grammar, dict):
        return {}
    governance_policy = family_grammar.get("governance_policy")
    if not isinstance(governance_policy, dict):
        return {}
    controller_defaults = governance_policy.get("controller_defaults")
    quality_bar = governance_policy.get("quality_bar")
    rollback_bias = governance_policy.get("rollback_bias")
    evidence_escalation_policy = governance_policy.get("evidence_escalation_policy")
    return {
        "surface_kind": "grant_family_governance_surface",
        "family_id": _normalized_string(family_grammar.get("family_id")),
        "family_label": _normalized_string(family_grammar.get("family_label")),
        "funder": _normalized_string(family_grammar.get("funder")),
        "admission_status": _normalized_string(family_grammar.get("admission_status")) or "unknown",
        "governance_policy_id": _normalized_string(governance_policy.get("policy_id"))
        or _normalized_string(family_grammar.get("family_id"))
        or "unknown_governance_policy",
        "default_tranche": _normalized_string(governance_policy.get("default_tranche")),
        "preferred_stop_target": _normalized_string(governance_policy.get("preferred_stop_target")),
        "preferred_rollback_stage": _normalized_string(
            rollback_bias.get("default_rollback_stage") if isinstance(rollback_bias, dict) else None
        ),
        "controller_defaults": deepcopy(controller_defaults) if isinstance(controller_defaults, dict) else {},
        "quality_bar": deepcopy(quality_bar) if isinstance(quality_bar, dict) else {},
        "rollback_bias": deepcopy(rollback_bias) if isinstance(rollback_bias, dict) else {},
        "evidence_escalation_policy": (
            deepcopy(evidence_escalation_policy)
            if isinstance(evidence_escalation_policy, dict)
            else {}
        ),
        "governance_entry_points": _string_list(family_grammar.get("governance_entry_points")) or [],
    }


def apply_family_governance_to_controller_plan(
    controller_plan: dict[str, Any],
    *,
    workspace: dict[str, Any] | None,
    explicit_controller_plan: bool,
) -> dict[str, Any]:
    if explicit_controller_plan:
        return deepcopy(controller_plan)
    governance_surface = build_family_governance_surface(workspace)
    if not governance_surface:
        return deepcopy(controller_plan)

    hydrated = deepcopy(controller_plan)
    default_tranche = governance_surface["default_tranche"]
    if default_tranche:
        hydrated["current_tranche"] = default_tranche

    controller_defaults = governance_surface["controller_defaults"]
    target_status = _normalized_string(controller_defaults.get("target_status"))
    if target_status not in {"submission_grade_candidate", "near_submission_candidate"}:
        target_status = governance_surface["preferred_stop_target"]
    if target_status in {"submission_grade_candidate", "near_submission_candidate"}:
        hydrated["tranche_success_gate"]["target_status"] = target_status

    if "require_zero_blockers" in controller_defaults:
        hydrated["tranche_success_gate"]["requires_zero_blockers"] = bool(
            controller_defaults["require_zero_blockers"]
        )
    if "require_zero_evidence_gaps" in controller_defaults:
        hydrated["tranche_success_gate"]["requires_zero_evidence_gaps"] = bool(
            controller_defaults["require_zero_evidence_gaps"]
        )
    acceptance = controller_defaults.get("acceptance_criteria")
    if isinstance(acceptance, list):
        normalized_acceptance = [item for item in (_normalized_string(v) for v in acceptance) if item]
        if normalized_acceptance:
            hydrated["tranche_success_gate"]["acceptance_criteria"] = normalized_acceptance
    return hydrated


def prioritize_closure_package_queue(
    closure_packages: list[dict[str, Any]] | None,
    *,
    workspace: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    packages = [deepcopy(item) for item in closure_packages or [] if isinstance(item, dict)]
    governance_surface = build_family_governance_surface(workspace)
    preferred_rollback_stage = governance_surface.get("preferred_rollback_stage")
    enumerated = list(enumerate(packages))
    enumerated.sort(
        key=lambda item: (
            _CLOSURE_ACTION_PRIORITY.get(_normalized_string(item[1].get("action")), 99),
            0 if _normalized_string(item[1].get("severity")) == "hard" else 1,
            0
            if preferred_rollback_stage
            and _normalized_string(item[1].get("target_stage")) == preferred_rollback_stage
            else 1,
            _BASE_STAGE_PRIORITY.get(_normalized_string(item[1].get("target_stage")), 99),
            item[0],
        )
    )
    return [deepcopy(item[1]) for item in enumerated]


def _normalized_string(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list):
        return None
    normalized: list[str] = []
    for item in value:
        item_text = _normalized_string(item)
        if not item_text:
            return None
        normalized.append(item_text)
    return normalized
