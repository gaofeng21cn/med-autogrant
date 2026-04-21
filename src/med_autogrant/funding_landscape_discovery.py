from __future__ import annotations

import copy
from typing import Any


REQUIRED_DISCOVERY_INPUT_FIELDS: tuple[str, ...] = (
    "applicant_profile",
    "track_record",
    "rough_direction_hint",
)


FUNDING_OPPORTUNITY_CATALOG: tuple[dict[str, Any], ...] = (
    {
        "metadata": {
            "schema_version": "v1",
            "created_at": "2026-04-21T12:00:00Z",
            "updated_at": "2026-04-21T12:00:00Z",
            "source_mode": "auto"
        },
        "brief_id": "nsfc-2026-general",
        "funder": "NSFC",
        "program_family": "医学科学部",
        "project_types": ["general", "young_scientist"],
        "application_year": 2026,
        "mandatory_sections": ["立项依据", "研究内容", "研究方案", "创新点", "研究基础"],
        "evaluation_notes": ["必要性与科学价值优先"],
        "formal_constraints": ["题目需与核心科学问题一致"],
        "discovery_rules": {
            "all_of": (
                {
                    "rule_id": "nsfc.direction.fit",
                    "source_field": "rough_direction_tokens",
                    "operator": "contains_any",
                    "allowed_values": (
                        "医学",
                        "medical",
                        "心血管",
                        "cardiovascular",
                        "炎症",
                        "inflammation",
                        "纤维化",
                        "fibrosis",
                        "免疫",
                        "immun",
                    ),
                },
            ),
        },
    },
    {
        "metadata": {
            "schema_version": "v1",
            "created_at": "2026-04-21T12:00:00Z",
            "updated_at": "2026-04-21T12:00:00Z",
            "source_mode": "auto"
        },
        "brief_id": "nih-r21-2026-nhlbi",
        "funder": "NIH",
        "program_family": "NHLBI R21",
        "project_types": ["exploratory_developmental"],
        "application_year": 2026,
        "mandatory_sections": ["Significance", "Innovation", "Approach", "Investigator", "Environment"],
        "evaluation_notes": ["Significance and innovation carry major review weight"],
        "formal_constraints": ["Exploratory aims should stay scoped to R21 expectations"],
        "discovery_rules": {
            "all_of": (
                {
                    "rule_id": "nih_r21.direction.fit",
                    "source_field": "rough_direction_tokens",
                    "operator": "contains_any",
                    "allowed_values": (
                        "转化",
                        "translational",
                        "exploratory",
                        "innovation",
                        "心血管",
                        "cardiovascular",
                        "炎症",
                        "inflammation",
                        "intervention",
                    ),
                },
            ),
        },
    },
)


def discover_funding_landscape(discovery_input: dict[str, Any]) -> dict[str, Any]:
    _validate_discovery_input(discovery_input)
    include_funders = _normalize_optional_string_list(discovery_input.get("include_funders"))
    program_family_hints = _normalize_optional_string_list(discovery_input.get("program_family_hints"))

    direction_tokens = _build_direction_tokens(discovery_input)
    context = {
        "direction_tokens": direction_tokens,
        "rough_direction_tokens": _normalize_string(discovery_input["rough_direction_hint"]).casefold(),
    }

    catalog_filtered = _apply_catalog_filters(
        catalog=FUNDING_OPPORTUNITY_CATALOG,
        include_funders=include_funders,
        program_family_hints=program_family_hints,
    )

    matched: list[dict[str, Any]] = []
    blocked_count = 0
    for opportunity in catalog_filtered:
        rule_evaluation = _evaluate_opportunity_rules(opportunity=opportunity, context=context)
        if rule_evaluation["matched"]:
            matched.append(_sanitize_funding_opportunity(opportunity))
        else:
            blocked_count += 1

    if not matched:
        raise ValueError("未发现兼容的 funding opportunities；discovery fail-closed。")

    matched.sort(key=lambda item: (item["funder"], item["program_family"], item["brief_id"]))
    applied_filters: dict[str, list[str]] = {}
    if include_funders is not None:
        applied_filters["include_funders"] = include_funders
    if program_family_hints is not None:
        applied_filters["program_family_hints"] = program_family_hints

    return {
        "funding_opportunity_pool": matched,
        "candidate_count": len(matched),
        "discovery_summary": {
            "decision": "discovered",
            "evaluated_catalog_count": len(FUNDING_OPPORTUNITY_CATALOG),
            "post_filter_catalog_count": len(catalog_filtered),
            "blocked_by_rules_count": blocked_count,
            "applied_filters": applied_filters,
            "required_input_fields": list(REQUIRED_DISCOVERY_INPUT_FIELDS),
        },
    }


def _validate_discovery_input(discovery_input: dict[str, Any]) -> None:
    if not isinstance(discovery_input, dict):
        raise ValueError("discovery_input 必须是 object。")
    for field in REQUIRED_DISCOVERY_INPUT_FIELDS:
        if field not in discovery_input:
            raise ValueError(f"discovery_input 缺少必填字段: {field}")

    if not isinstance(discovery_input["applicant_profile"], dict):
        raise ValueError("discovery_input.applicant_profile 必须是 object。")
    if not isinstance(discovery_input["track_record"], dict):
        raise ValueError("discovery_input.track_record 必须是 object。")

    rough_direction_hint = discovery_input["rough_direction_hint"]
    if not isinstance(rough_direction_hint, str) or not rough_direction_hint.strip():
        raise ValueError("discovery_input.rough_direction_hint 必须是非空字符串。")

    _normalize_optional_string_list(discovery_input.get("include_funders"))
    _normalize_optional_string_list(discovery_input.get("program_family_hints"))


def _normalize_optional_string_list(value: Any) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError("可选过滤字段必须是字符串列表。")
    normalized = [_normalize_string(item) for item in value if _normalize_string(item)]
    if not normalized:
        raise ValueError("可选过滤字段若提供，必须包含至少一个非空字符串。")
    return normalized


def _apply_catalog_filters(
    *,
    catalog: tuple[dict[str, Any], ...],
    include_funders: list[str] | None,
    program_family_hints: list[str] | None,
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    include_funders_norm = {item.casefold() for item in include_funders} if include_funders else None
    program_family_hints_norm = {item.casefold() for item in program_family_hints} if program_family_hints else None

    for opportunity in catalog:
        funder = _normalize_string(opportunity.get("funder"))
        program_family = _normalize_string(opportunity.get("program_family"))
        if include_funders_norm is not None and funder.casefold() not in include_funders_norm:
            continue
        if program_family_hints_norm is not None and not any(hint in program_family.casefold() for hint in program_family_hints_norm):
            continue
        filtered.append(opportunity)
    return filtered


def _build_direction_tokens(discovery_input: dict[str, Any]) -> str:
    applicant_profile = discovery_input["applicant_profile"]
    track_record = discovery_input["track_record"]
    segments: list[str] = [
        discovery_input["rough_direction_hint"],
    ]

    for field in ("research_domains", "clinical_domains", "methods_stack"):
        values = applicant_profile.get(field)
        if isinstance(values, list):
            segments.extend(_normalize_string(item) for item in values if _normalize_string(item))

    representative_outputs = track_record.get("representative_outputs")
    if isinstance(representative_outputs, list):
        for output in representative_outputs:
            if not isinstance(output, dict):
                continue
            for field in ("title", "relevance_summary", "output_type"):
                value = _normalize_string(output.get(field))
                if value:
                    segments.append(value)

    return " ".join(segment.casefold() for segment in segments if segment)


def _evaluate_opportunity_rules(*, opportunity: dict[str, Any], context: dict[str, str]) -> dict[str, Any]:
    rules = opportunity["discovery_rules"]["all_of"]
    results = [_evaluate_single_rule(rule, context) for rule in rules]
    return {
        "matched": all(result["matched"] for result in results),
        "rule_results": results,
    }


def _evaluate_single_rule(rule: dict[str, Any], context: dict[str, str]) -> dict[str, Any]:
    source = context.get(rule["source_field"], "")
    operator = rule["operator"]
    if operator != "contains_any":
        raise ValueError(f"不支持的 rule.operator: {operator}")
    allowed_values = [item.casefold() for item in rule["allowed_values"]]
    matched = any(value in source for value in allowed_values)
    return {
        "rule_id": rule["rule_id"],
        "matched": matched,
    }


def _normalize_string(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _sanitize_funding_opportunity(opportunity: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": copy.deepcopy(opportunity["metadata"]),
        "brief_id": opportunity["brief_id"],
        "funder": opportunity["funder"],
        "program_family": opportunity["program_family"],
        "project_types": list(opportunity["project_types"]),
        "application_year": opportunity["application_year"],
        "mandatory_sections": list(opportunity["mandatory_sections"]),
        "formal_constraints": list(opportunity.get("formal_constraints") or []),
        "evaluation_notes": list(opportunity.get("evaluation_notes") or []),
    }
