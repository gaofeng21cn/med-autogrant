from __future__ import annotations

import copy
from typing import Any

from med_autogrant.funding_landscape_discovery_parts.providers import (
    FetchText,
    _build_cached_catalog,
    _build_official_live_catalog,
    _fetch_url_text,
)
from med_autogrant.funding_landscape_discovery_parts.provenance import (
    _build_provenance_records,
    _dedupe_funding_opportunities,
    _index_existing_sources,
    _normalize_string,
    _opportunity_index,
    _sanitize_funding_opportunity,
    _snapshot_funding_opportunity_pool,
    _source_map,
    _utc_now,
)

REQUIRED_DISCOVERY_INPUT_FIELDS: tuple[str, ...] = (
    "applicant_profile",
    "track_record",
    "rough_direction_hint",
)
SUPPORTED_DISCOVERY_SOURCES: tuple[str, ...] = (
    "catalog_static",
    "official_live",
    "official_cached",
)

_FIXED_CATALOG_TIMESTAMP = "2026-04-21T12:00:00Z"

FUNDING_OPPORTUNITY_CATALOG: tuple[dict[str, Any], ...] = (
    {
        "metadata": {
            "schema_version": "v1",
            "created_at": _FIXED_CATALOG_TIMESTAMP,
            "updated_at": _FIXED_CATALOG_TIMESTAMP,
            "source_mode": "auto",
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
            "created_at": _FIXED_CATALOG_TIMESTAMP,
            "updated_at": _FIXED_CATALOG_TIMESTAMP,
            "source_mode": "auto",
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


def discover_funding_landscape(
    discovery_input: dict[str, Any],
    *,
    fetch_text: FetchText | None = None,
    cached_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _validate_discovery_input(discovery_input)
    discovery_source = _normalize_string(discovery_input.get("discovery_source")) or "catalog_static"
    if discovery_source not in SUPPORTED_DISCOVERY_SOURCES:
        raise ValueError(
            "discovery_input.discovery_source 不受支持："
            f"{discovery_source}。当前只允许 {', '.join(SUPPORTED_DISCOVERY_SOURCES)}。"
        )

    include_funders = _normalize_optional_string_list(discovery_input.get("include_funders"))
    program_family_hints = _normalize_optional_string_list(discovery_input.get("program_family_hints"))

    context = {
        "rough_direction_tokens": _normalize_string(discovery_input["rough_direction_hint"]).casefold(),
        "combined_direction_tokens": _build_direction_tokens(discovery_input),
    }
    if discovery_source == "official_live":
        catalog, source_entries = _build_official_live_catalog(
            fetch_text=fetch_text or _fetch_url_text,
            include_funders=include_funders,
        )
    elif discovery_source == "official_cached":
        catalog, source_entries = _build_cached_catalog(
            cached_snapshot=_require_cache_snapshot(cached_snapshot),
            include_funders=include_funders,
        )
    else:
        catalog = list(FUNDING_OPPORTUNITY_CATALOG)
        source_entries = []

    catalog_filtered = _apply_catalog_filters(
        catalog=catalog,
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

    matched.sort(key=lambda item: (item["funder"], item["program_family"], item["brief_id"]))
    applied_filters: dict[str, list[str]] = {}
    if include_funders is not None:
        applied_filters["include_funders"] = include_funders
    if program_family_hints is not None:
        applied_filters["program_family_hints"] = program_family_hints

    source_receipts = [
        {
            "source_id": entry["source_id"],
            "source_kind": entry["source_kind"],
            "source_url": entry["source_url"],
            "fetched_at": entry["fetched_at"],
            "item_count": entry["item_count"],
        }
        for entry in source_entries
    ]

    return {
        "funding_opportunity_pool": matched,
        "funding_opportunity_provenance": _build_provenance_records(
            funding_opportunity_pool=matched,
            source_entries=source_entries,
            discovery_source=discovery_source,
        ),
        "candidate_count": len(matched),
        "source_receipts": source_receipts,
        "discovery_summary": {
            "decision": "discovered" if matched else "completed_with_quality_debt",
            "discovery_source": discovery_source,
            "evaluated_catalog_count": len(catalog),
            "post_filter_catalog_count": len(catalog_filtered),
            "blocked_by_rules_count": blocked_count,
            "source_receipt_count": len(source_entries),
            "applied_filters": applied_filters,
            "required_input_fields": list(REQUIRED_DISCOVERY_INPUT_FIELDS),
            "next_stage_may_start": True,
            "route_back_selection_owner": "decisive_codex_attempt",
            "quality_debt": (
                None
                if matched
                else {
                    "code": "no_compatible_funding_opportunity",
                    "blocks_stage_transition": False,
                    "blocks_fundability_submission_export_or_ready_claims": True,
                }
            ),
        },
    }


def build_funding_landscape_cache(
    discovery_input: dict[str, Any],
    *,
    fetch_text: FetchText | None = None,
    existing_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _validate_discovery_input(discovery_input)
    include_funders = _normalize_optional_string_list(discovery_input.get("include_funders"))
    catalog, source_entries = _build_official_live_catalog(
        fetch_text=fetch_text or _fetch_url_text,
        include_funders=include_funders,
    )
    existing_sources = _index_existing_sources(existing_snapshot)
    for entry in source_entries:
        existing_sources[entry["source_id"]] = copy.deepcopy(entry)
    merged_sources = sorted(existing_sources.values(), key=lambda item: item["source_id"])
    merged_pool = _dedupe_funding_opportunities(
        opportunity
        for entry in merged_sources
        for opportunity in entry["funding_opportunity_pool"]
    )
    return {
        "cache_version": 1,
        "cache_kind": "funding_landscape_cache",
        "discovery_input_id": discovery_input.get("discovery_input_id") or "unknown_discovery_input",
        "refreshed_at": _utc_now(),
        "source_count": len(merged_sources),
        "sources": merged_sources,
        "funding_opportunity_pool": merged_pool,
    }


def build_funding_landscape_diff_report(
    *,
    previous_snapshot: dict[str, Any] | None,
    current_snapshot: dict[str, Any],
) -> dict[str, Any]:
    previous_snapshot = previous_snapshot if isinstance(previous_snapshot, dict) else None
    previous_pool = _opportunity_index(_snapshot_funding_opportunity_pool(previous_snapshot))
    current_pool = _opportunity_index(_snapshot_funding_opportunity_pool(current_snapshot))
    previous_sources = _source_map(previous_snapshot.get("sources") if previous_snapshot else [])
    current_sources = _source_map(current_snapshot.get("sources") or [])

    added_count = 0
    updated_count = 0
    withdrawn_count = 0
    unchanged_count = 0
    changes: list[dict[str, Any]] = []

    all_brief_ids = sorted(set(previous_pool) | set(current_pool))
    for brief_id in all_brief_ids:
        previous_item = previous_pool.get(brief_id)
        current_item = current_pool.get(brief_id)
        previous_source_ids = sorted(previous_sources.get(brief_id, []))
        current_source_ids = sorted(current_sources.get(brief_id, []))
        if previous_item is None and current_item is not None:
            added_count += 1
            changes.append(
                {
                    "brief_id": brief_id,
                    "change_status": "added",
                    "previous_source_ids": previous_source_ids,
                    "current_source_ids": current_source_ids,
                }
            )
            continue
        if previous_item is not None and current_item is None:
            withdrawn_count += 1
            changes.append(
                {
                    "brief_id": brief_id,
                    "change_status": "withdrawn_or_not_listed",
                    "previous_source_ids": previous_source_ids,
                    "current_source_ids": current_source_ids,
                }
            )
            continue
        if previous_item != current_item:
            updated_count += 1
            changes.append(
                {
                    "brief_id": brief_id,
                    "change_status": "updated",
                    "previous_source_ids": previous_source_ids,
                    "current_source_ids": current_source_ids,
                }
            )
            continue
        unchanged_count += 1

    return {
        "report_version": 1,
        "report_kind": "funding_landscape_diff_report",
        "previous_refreshed_at": previous_snapshot.get("refreshed_at") if previous_snapshot else None,
        "current_refreshed_at": current_snapshot["refreshed_at"],
        "added_count": added_count,
        "updated_count": updated_count,
        "withdrawn_count": withdrawn_count,
        "unchanged_count": unchanged_count,
        "changes": changes,
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
    discovery_source = _normalize_string(discovery_input.get("discovery_source"))
    if discovery_source and discovery_source not in SUPPORTED_DISCOVERY_SOURCES:
        raise ValueError(
            "discovery_input.discovery_source 不受支持："
            f"{discovery_source}。当前只允许 {', '.join(SUPPORTED_DISCOVERY_SOURCES)}。"
        )


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
    catalog: list[dict[str, Any]] | tuple[dict[str, Any], ...],
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
    segments: list[str] = [discovery_input["rough_direction_hint"]]

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
    discovery_rules = opportunity.get("discovery_rules")
    if not isinstance(discovery_rules, dict):
        return {
            "matched": True,
            "rule_results": [],
        }
    rules = discovery_rules["all_of"]
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


def _require_cache_snapshot(cached_snapshot: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(cached_snapshot, dict):
        raise ValueError("official_cached 模式要求提供 cache snapshot。")
    if cached_snapshot.get("cache_kind") != "funding_landscape_cache":
        raise ValueError("缓存快照缺少 cache_kind=funding_landscape_cache。")
    sources = cached_snapshot.get("sources")
    if not isinstance(sources, list):
        raise ValueError("缓存快照缺少合法 sources 列表。")
    return cached_snapshot
