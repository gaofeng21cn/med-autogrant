from __future__ import annotations

from typing import Any

from med_autogrant.funding_landscape_discovery_parts.core import (
    FUNDING_OPPORTUNITY_CATALOG,
    REQUIRED_DISCOVERY_INPUT_FIELDS,
    SUPPORTED_DISCOVERY_SOURCES,
    _FIXED_CATALOG_TIMESTAMP,
    _apply_catalog_filters,
    _build_direction_tokens,
    _evaluate_opportunity_rules,
    _evaluate_single_rule,
    _normalize_optional_string_list,
    _require_cache_snapshot,
    _validate_discovery_input,
    build_funding_landscape_diff_report,
    discover_funding_landscape as _discover_funding_landscape,
)
from med_autogrant.funding_landscape_discovery_parts.core import (
    build_funding_landscape_cache as _build_funding_landscape_cache,
)
from med_autogrant.funding_landscape_discovery_parts.providers import (
    FetchText,
    OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL,
    OFFICIAL_NSFC_GUIDE_LIST_URL,
    OFFICIAL_NSFC_MEDICAL_GUIDE_URL,
    _build_cached_catalog,
    _build_official_live_catalog,
    _fetch_url_text as _provider_fetch_url_text,
    _nih_project_types_from_title,
    _parse_nih_r21_parent_announcements,
    _parse_nsfc_medical_guide,
    _year_from_code_or_now,
    fetch_source_text,
)
from med_autogrant.funding_landscape_discovery_parts.provenance import (
    _build_provenance_records,
    _build_source_entry,
    _dedupe_funding_opportunities,
    _fresh_metadata,
    _index_existing_sources,
    _normalize_string,
    _opportunity_index,
    _sanitize_funding_opportunity,
    _snapshot_funding_opportunity_pool,
    _source_map,
    _utc_now,
)


def discover_funding_landscape(
    discovery_input: dict[str, Any],
    *,
    fetch_text: FetchText | None = None,
    cached_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _discover_funding_landscape(
        discovery_input,
        fetch_text=fetch_text,
        default_fetch_text=_fetch_url_text,
        cached_snapshot=cached_snapshot,
    )


def build_funding_landscape_cache(
    discovery_input: dict[str, Any],
    *,
    fetch_text: FetchText | None = None,
    existing_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _build_funding_landscape_cache(
        discovery_input,
        fetch_text=fetch_text,
        default_fetch_text=_fetch_url_text,
        existing_snapshot=existing_snapshot,
    )


def _fetch_url_text(url: str) -> str:
    return _provider_fetch_url_text(url, transport=fetch_source_text)
