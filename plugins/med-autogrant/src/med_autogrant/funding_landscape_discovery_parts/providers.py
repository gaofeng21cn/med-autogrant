from __future__ import annotations

import copy
import html
import re
from datetime import UTC, datetime
from typing import Any, Callable

from opl_framework.source_transport import fetch_text as fetch_source_text

from med_autogrant.funding_landscape_discovery_parts.provenance import (
    _build_source_entry,
    _fresh_metadata,
    _normalize_string,
)

FetchText = Callable[[str], str]

OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL = (
    "https://grants.nih.gov/funding/explore-nih-opportunities/parent-announcements"
)
OFFICIAL_NSFC_GUIDE_LIST_URL = "https://www.nsfc.gov.cn/p1/3381/2824/zntg.html"
OFFICIAL_NSFC_MEDICAL_GUIDE_URL = "https://www.nsfc.gov.cn/p1/2931/3971/3975/3991/yxkxb22222.html"


def _build_official_live_catalog(
    *,
    fetch_text: FetchText,
    include_funders: list[str] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    allowed_funders = {item.casefold() for item in include_funders} if include_funders else None
    catalog: list[dict[str, Any]] = []
    source_entries: list[dict[str, Any]] = []

    if allowed_funders is None or "nih" in allowed_funders:
        nih_html = fetch_text(OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL)
        nih_items = _parse_nih_r21_parent_announcements(nih_html)
        catalog.extend(nih_items)
        source_entries.append(
            _build_source_entry(
                source_id="nih_parent_announcements",
                source_kind="official_html",
                source_url=OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL,
                funding_opportunity_pool=nih_items,
            )
        )

    if allowed_funders is None or "nsfc" in allowed_funders:
        nsfc_list_html = fetch_text(OFFICIAL_NSFC_GUIDE_LIST_URL)
        nsfc_medical_html = fetch_text(OFFICIAL_NSFC_MEDICAL_GUIDE_URL)
        nsfc_items = _parse_nsfc_medical_guide(nsfc_list_html, nsfc_medical_html)
        catalog.extend(nsfc_items)
        source_entries.append(
            _build_source_entry(
                source_id="nsfc_project_guide_listing",
                source_kind="official_html",
                source_url=OFFICIAL_NSFC_GUIDE_LIST_URL,
                funding_opportunity_pool=nsfc_items,
            )
        )
        source_entries.append(
            _build_source_entry(
                source_id="nsfc_medical_sciences_guide",
                source_kind="official_html",
                source_url=OFFICIAL_NSFC_MEDICAL_GUIDE_URL,
                funding_opportunity_pool=nsfc_items,
            )
        )

    return catalog, source_entries


def _build_cached_catalog(
    *,
    cached_snapshot: dict[str, Any],
    include_funders: list[str] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    allowed_funders = {item.casefold() for item in include_funders} if include_funders else None
    source_entries: list[dict[str, Any]] = []
    catalog: list[dict[str, Any]] = []
    for entry in cached_snapshot["sources"]:
        if allowed_funders is not None:
            entry_funders = {
                _normalize_string(item.get("funder")).casefold()
                for item in entry.get("funding_opportunity_pool", [])
                if _normalize_string(item.get("funder"))
            }
            if not (entry_funders & allowed_funders):
                continue
        normalized_entry = {
            "source_id": entry["source_id"],
            "source_kind": "official_cached",
            "source_url": entry["source_url"],
            "fetched_at": entry["fetched_at"],
            "item_count": entry["item_count"],
            "funding_opportunity_pool": [copy.deepcopy(item) for item in entry["funding_opportunity_pool"]],
        }
        source_entries.append(normalized_entry)
        catalog.extend(normalized_entry["funding_opportunity_pool"])
    return catalog, source_entries


def _parse_nih_r21_parent_announcements(page_html: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"(?P<title>NIH Exploratory/Developmental Research Project Grant \(Parent R21[^<]+)"
        r".*?<a href=\"(?P<url>https://simpler\.grants\.gov/opportunity/\d+)\"[^>]*>(?P<foa>PA-\d{2}-\d{3})</a>",
        re.S,
    )
    matches = list(pattern.finditer(page_html))
    if not matches:
        raise ValueError("未能从 NIH Parent Announcements 官方页面解析出 R21 opportunities。")

    opportunities: list[dict[str, Any]] = []
    for match in matches:
        title = html.unescape(" ".join(match.group("title").split()))
        foa_code = match.group("foa")
        simpler_url = match.group("url")
        opportunities.append(
            {
                "metadata": _fresh_metadata(),
                "brief_id": f"nih-r21-{foa_code.lower()}",
                "funder": "NIH",
                "program_family": "NIH R21 Parent",
                "project_types": _nih_project_types_from_title(title),
                "application_year": _year_from_code_or_now(foa_code),
                "mandatory_sections": [
                    "Significance",
                    "Innovation",
                    "Approach",
                    "Investigator",
                    "Environment",
                ],
                "formal_constraints": [
                    f"Official NIH parent announcement title: {title}",
                    f"Official funding opportunity code: {foa_code}",
                    f"Official opportunity URL: {simpler_url}",
                ],
                "evaluation_notes": [
                    "Significance and innovation carry major review weight",
                    title,
                ],
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
            }
        )
    return opportunities


def _parse_nsfc_medical_guide(list_html: str, medical_html: str) -> list[dict[str, Any]]:
    guide_match = re.search(
        r"href=\"(?P<href>/p1/2931/3971/3972/qy(?P<year>\d{4})\.html)\">(?P<title>\d{4}年度国家自然科学基金项目指南)</a>",
        list_html,
    )
    if guide_match is None:
        raise ValueError("未能从 NSFC 项目指南列表页解析出年度项目指南。")
    if "医学科学部" not in medical_html:
        raise ValueError("未能从 NSFC 医学科学部指南页面确认医学科学部入口。")

    notice_match = re.search(
        r"href=\"(?P<href>/p1/3381/2824/\d+\.html)\">(?P<title>关于\d{4}年度国家自然科学基金项目申请与结题等有关事项的通告)</a>",
        list_html,
    )
    year = int(guide_match.group("year"))
    guide_title = guide_match.group("title")
    guide_url = f"https://www.nsfc.gov.cn{guide_match.group('href')}"
    formal_constraints = [
        f"Official NSFC guide title: {guide_title}",
        f"Official NSFC medical guide URL: {OFFICIAL_NSFC_MEDICAL_GUIDE_URL}",
        f"Official NSFC annual guide URL: {guide_url}",
    ]
    if notice_match is not None:
        formal_constraints.append(
            f"Official NSFC notice: {html.unescape(notice_match.group('title'))}"
        )

    return [
        {
            "metadata": _fresh_metadata(),
            "brief_id": f"nsfc-{year}-general-medical-live",
            "funder": "NSFC",
            "program_family": "医学科学部",
            "project_types": ["general", "young_scientist"],
            "application_year": year,
            "mandatory_sections": ["立项依据", "研究内容", "研究方案", "创新点", "研究基础"],
            "formal_constraints": formal_constraints,
            "evaluation_notes": ["必要性与科学价值优先", guide_title],
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
        }
    ]


def _fetch_url_text(
    url: str,
    *,
    transport: Callable[..., str] | None = None,
) -> str:
    fetcher = transport or fetch_source_text
    return fetcher(
        url,
        allowed_urls=(
            OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL,
            OFFICIAL_NSFC_GUIDE_LIST_URL,
            OFFICIAL_NSFC_MEDICAL_GUIDE_URL,
        ),
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; MedAutoGrant/1.0; +https://www.nsfc.gov.cn/)",
        },
        timeout=20,
    )


def _year_from_code_or_now(value: str) -> int:
    match = re.search(r"(\d{2})", value)
    if match is None:
        return datetime.now(UTC).year
    year_suffix = int(match.group(1))
    return 2000 + year_suffix


def _nih_project_types_from_title(title: str) -> list[str]:
    normalized = title.casefold()
    project_types = ["exploratory_developmental", "parent_announcement"]
    if "clinical trial not allowed" in normalized:
        project_types.append("clinical_trial_not_allowed")
    if "clinical trial required" in normalized:
        project_types.append("clinical_trial_required")
    if "basic experimental studies with humans required" in normalized:
        project_types.append("basic_experimental_studies_with_humans_required")
    return project_types
