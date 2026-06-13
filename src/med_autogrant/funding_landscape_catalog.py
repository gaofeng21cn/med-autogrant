from __future__ import annotations

from typing import Any


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

OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL = (
    "https://grants.nih.gov/funding/explore-nih-opportunities/parent-announcements"
)
OFFICIAL_NSFC_GUIDE_LIST_URL = "https://www.nsfc.gov.cn/p1/3381/2824/zntg.html"
OFFICIAL_NSFC_MEDICAL_GUIDE_URL = "https://www.nsfc.gov.cn/p1/2931/3971/3975/3991/yxkxb22222.html"

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
