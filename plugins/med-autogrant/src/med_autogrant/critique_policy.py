from __future__ import annotations

from copy import deepcopy
from typing import Any


DEFAULT_NSFC_CRITIQUE_POLICY: dict[str, Any] = {
    "policy_id": "nsfc_mentor_critique_v1",
    "persona": {
        "role": "NSFC mentor reviewer",
        "style": "diagnostic, evidence-grounded, independent",
    },
    "weighted_dimensions": [
        {
            "field": "necessity_scientific_value",
            "weight": 60,
            "focus": "diagnose necessity and scientific value in relation to the whole proposal",
        },
        {
            "field": "applicant_fit",
            "weight": 30,
            "focus": "assess applicant-to-question fit and evidence support",
        },
        {
            "field": "feasibility",
            "weight": 10,
            "focus": "assess execution feasibility as a supporting criterion",
        },
    ],
    "hard_rules": [
        "clearly separate scientific question framing from engineering task decomposition",
    ],
    "required_outputs": [
        {"field": "overall_diagnosis", "description": "global diagnosis of draft readiness"},
        {"field": "suggested_question", "description": "scientific question reshape recommendation"},
        {"field": "logic_chain_repairs", "description": "logic-chain repair actions"},
        {"field": "applicant_fit_repairs", "description": "applicant-fit alignment actions"},
    ],
}

DEFAULT_NIH_R21_CRITIQUE_POLICY: dict[str, Any] = {
    "policy_id": "nih_r21_significance_innovation_v1",
    "persona": {
        "role": "NIH R21 scientific reviewer",
        "style": "translational, evidence-grounded, independent",
    },
    "weighted_dimensions": [
        {
            "field": "significance",
            "weight": 45,
            "focus": "diagnose whether the project addresses an important translational problem",
        },
        {
            "field": "innovation",
            "weight": 35,
            "focus": "assess whether the approach creates a credible conceptual or technical jump",
        },
        {
            "field": "investigator_environment_fit",
            "weight": 20,
            "focus": "assess whether the team and environment can execute the proposed work",
        },
    ],
    "hard_rules": [
        "separate near-term exploratory aims from long-term mechanistic claims",
    ],
    "required_outputs": [
        {"field": "overall_diagnosis", "description": "global diagnosis of draft readiness"},
        {"field": "significance_repairs", "description": "repairs for significance framing and unmet need"},
        {"field": "innovation_repairs", "description": "repairs for innovation framing and novelty claim"},
        {"field": "investigator_environment_repairs", "description": "repairs for execution fit and environment"},
    ],
}


CRITIQUE_POLICY_PRESET_REGISTRY: dict[str, dict[str, Any]] = {
    DEFAULT_NSFC_CRITIQUE_POLICY["policy_id"]: DEFAULT_NSFC_CRITIQUE_POLICY,
    DEFAULT_NIH_R21_CRITIQUE_POLICY["policy_id"]: DEFAULT_NIH_R21_CRITIQUE_POLICY,
}


def build_weight_contract(policy: dict[str, Any]) -> dict[str, int]:
    weighted_dimensions = policy.get("weighted_dimensions")
    if not isinstance(weighted_dimensions, list):
        raise ValueError("critique policy 缺少 weighted_dimensions 列表。")
    contract: dict[str, int] = {}
    for item in weighted_dimensions:
        if not isinstance(item, dict):
            raise ValueError("critique policy weighted_dimensions 必须是 object 列表。")
        field = item.get("field")
        weight = item.get("weight")
        if not isinstance(field, str) or not field.strip():
            raise ValueError("critique policy weighted_dimensions.field 必须是非空字符串。")
        if not isinstance(weight, int):
            raise ValueError("critique policy weighted_dimensions.weight 必须是整数。")
        contract[field] = weight
    return contract


def resolve_critique_policy_from_document(document: dict[str, Any]) -> dict[str, Any]:
    project_profile = document.get("project_profile")
    if not isinstance(project_profile, dict):
        raise ValueError("workspace 缺少 project_profile。")
    critique_policy = project_profile.get("critique_policy")
    if not isinstance(critique_policy, dict):
        raise ValueError("project_profile 缺少 critique_policy。")

    preset_id = critique_policy.get("preset_id")
    declared_policy_id = critique_policy.get("policy_id")
    if not isinstance(preset_id, str) or not preset_id.strip():
        raise ValueError("project_profile.critique_policy.preset_id 必须是非空字符串。")
    if not isinstance(declared_policy_id, str) or not declared_policy_id.strip():
        raise ValueError("project_profile.critique_policy.policy_id 必须是非空字符串。")

    policy = CRITIQUE_POLICY_PRESET_REGISTRY.get(preset_id)
    if policy is None:
        raise ValueError(f"未知 critique policy preset: {preset_id}")
    if policy["policy_id"] != declared_policy_id:
        raise ValueError(
            "project_profile.critique_policy.policy_id 与 preset registry 不一致："
            f"{declared_policy_id} != {policy['policy_id']}"
        )
    return deepcopy(policy)


def build_policy_prompt_lines(policy: dict[str, Any]) -> list[str]:
    persona = policy.get("persona", {})
    role = persona.get("role", "NSFC mentor reviewer")
    style = persona.get("style", "diagnostic")
    weighted_dimensions = policy.get("weighted_dimensions", [])
    weight_contract = build_weight_contract(policy)
    weight_split = ", ".join(f"{field}={weight}" for field, weight in weight_contract.items())
    hard_rules = policy.get("hard_rules", [])
    required_outputs = policy.get("required_outputs", [])
    output_fields = [
        item["field"]
        for item in required_outputs
        if isinstance(item, dict) and isinstance(item.get("field"), str)
    ]

    lines = [
        f"- policy_id: {policy.get('policy_id', 'unknown')}",
        f"- persona role: {role}",
        f"- persona style: {style}",
        f"- reporting weight fields required by the current workspace schema: {weight_split}",
        "- Use the weights only to report the selected profile consistently; inspect the proposal holistically and do not force your review order from the numeric split.",
    ]
    for item in weighted_dimensions:
        if not isinstance(item, dict):
            continue
        field = item.get("field")
        focus = item.get("focus")
        if isinstance(field, str) and field and isinstance(focus, str) and focus.strip():
            lines.append(f"- weighted focus [{field}]: {focus}")
    lines.extend(f"- hard rule: {rule}" for rule in hard_rules if isinstance(rule, str) and rule.strip())
    if output_fields:
        lines.append(f"- required critique outputs: {', '.join(output_fields)}")
    return lines
