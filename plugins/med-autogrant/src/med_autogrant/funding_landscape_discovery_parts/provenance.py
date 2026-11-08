from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any


def _index_existing_sources(existing_snapshot: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(existing_snapshot, dict):
        return {}
    sources = existing_snapshot.get("sources")
    if not isinstance(sources, list):
        return {}
    indexed: dict[str, dict[str, Any]] = {}
    for item in sources:
        if not isinstance(item, dict):
            continue
        source_id = _normalize_string(item.get("source_id"))
        if not source_id:
            continue
        indexed[source_id] = copy.deepcopy(item)
    return indexed


def _dedupe_funding_opportunities(opportunities: Any) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for opportunity in opportunities:
        if not isinstance(opportunity, dict):
            continue
        brief_id = _normalize_string(opportunity.get("brief_id"))
        if not brief_id:
            continue
        deduped[brief_id] = _sanitize_funding_opportunity(opportunity)
    return [deduped[key] for key in sorted(deduped)]


def _opportunity_index(opportunities: Any) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for item in opportunities or []:
        if not isinstance(item, dict):
            continue
        brief_id = _normalize_string(item.get("brief_id"))
        if not brief_id:
            continue
        indexed[brief_id] = _sanitize_funding_opportunity(item)
    return indexed


def _snapshot_funding_opportunity_pool(snapshot: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(snapshot, dict):
        return []
    top_level_pool = snapshot.get("funding_opportunity_pool")
    if isinstance(top_level_pool, list) and top_level_pool:
        return top_level_pool
    sources = snapshot.get("sources")
    if not isinstance(sources, list):
        return []
    return [
        item
        for source in sources
        if isinstance(source, dict)
        for item in source.get("funding_opportunity_pool") or []
        if isinstance(item, dict)
    ]


def _source_map(sources: Any) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for source in sources or []:
        if not isinstance(source, dict):
            continue
        source_id = _normalize_string(source.get("source_id"))
        if not source_id:
            continue
        for item in source.get("funding_opportunity_pool") or []:
            if not isinstance(item, dict):
                continue
            brief_id = _normalize_string(item.get("brief_id"))
            if not brief_id:
                continue
            mapping.setdefault(brief_id, [])
            if source_id not in mapping[brief_id]:
                mapping[brief_id].append(source_id)
    return mapping


def _build_source_entry(
    *,
    source_id: str,
    source_kind: str,
    source_url: str,
    funding_opportunity_pool: list[dict[str, Any]],
) -> dict[str, Any]:
    sanitized_pool = [_sanitize_funding_opportunity(item) for item in funding_opportunity_pool]
    return {
        "source_id": source_id,
        "source_kind": source_kind,
        "source_url": source_url,
        "fetched_at": _utc_now(),
        "item_count": len(sanitized_pool),
        "funding_opportunity_pool": sanitized_pool,
    }


def _build_provenance_records(
    *,
    funding_opportunity_pool: list[dict[str, Any]],
    source_entries: list[dict[str, Any]],
    discovery_source: str,
) -> list[dict[str, Any]]:
    source_map: dict[str, list[str]] = {}
    for entry in source_entries:
        source_id = entry["source_id"]
        for item in entry["funding_opportunity_pool"]:
            brief_id = item["brief_id"]
            source_map.setdefault(brief_id, []).append(source_id)

    provenance_records: list[dict[str, Any]] = []
    for opportunity in funding_opportunity_pool:
        brief_id = opportunity["brief_id"]
        source_ids = sorted(source_map.get(brief_id, []))
        if discovery_source == "catalog_static":
            provenance_status = "repo_catalog_static"
            provenance_score = 50
        elif discovery_source == "official_live":
            provenance_status = (
                "official_live_multi_source" if len(source_ids) >= 2 else "official_live_single_source"
            )
            provenance_score = 100 if len(source_ids) >= 2 else 90
        else:
            provenance_status = (
                "official_cached_multi_source" if len(source_ids) >= 2 else "official_cached_single_source"
            )
            provenance_score = 85 if len(source_ids) >= 2 else 75
        provenance_records.append(
            {
                "brief_id": brief_id,
                "provenance_status": provenance_status,
                "provenance_score": provenance_score,
                "source_ids": source_ids,
            }
        )
    return provenance_records


def _fresh_metadata() -> dict[str, str]:
    timestamp = _utc_now()
    return {
        "schema_version": "v1",
        "created_at": timestamp,
        "updated_at": timestamp,
        "source_mode": "auto",
    }


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
