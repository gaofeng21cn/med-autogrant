from __future__ import annotations

from typing import Any


DEFAULT_NSFC_CRITIQUE_POLICY: dict[str, Any] = {
    "policy_id": "nsfc_mentor_critique_v1",
    "persona": {
        "role": "NSFC mentor reviewer",
        "style": "diagnostic, science-first, fail-closed",
    },
    "weighted_dimensions": [
        {
            "field": "necessity_scientific_value",
            "weight": 60,
            "focus": "diagnose necessity and scientific question first",
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
        f"- weight split: {weight_split}",
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
