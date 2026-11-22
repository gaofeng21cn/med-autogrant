from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.workspace_types import WorkspaceFileError

from .contracts import validate_schema_payload as _validate_schema_payload
from .io import _load_json_object
from .shared import FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE


def _default_funding_landscape_cache_path() -> Path:
    return resolve_runtime_state_root() / "funding-landscape" / "cache" / "latest.json"


def _derive_funding_landscape_diff_report_path(cache_path: Path) -> Path:
    return cache_path.with_name(f"{cache_path.stem}.diff.json")


def _load_existing_cache_snapshot(cache_path: Path) -> dict[str, Any] | None:
    if not cache_path.exists():
        return None
    return _load_json_object(cache_path, context="funding landscape cache")


def _load_funding_landscape_cache_if_needed(discovery_input: dict[str, Any]) -> dict[str, Any] | None:
    if discovery_input.get("discovery_source") != "official_cached":
        return None
    cache_path_value = discovery_input.get("cache_path")
    cache_path = (
        Path(str(cache_path_value)).expanduser().resolve()
        if isinstance(cache_path_value, str) and cache_path_value.strip()
        else _default_funding_landscape_cache_path()
    )
    if not cache_path.exists():
        raise WorkspaceFileError(f"official_cached 模式缺少 funding cache: {cache_path}")
    snapshot = _load_json_object(cache_path, context="funding landscape cache")
    _validate_schema_payload(
        snapshot,
        schema_file=FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE,
        context="funding_landscape_cache",
    )
    return snapshot


def _build_selection_input_from_discovery(
    *,
    discovery_input: dict[str, Any],
    funding_opportunity_pool: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "metadata": dict(discovery_input["metadata"]),
        "selection_input_id": discovery_input["discovery_input_id"],
        "mode": discovery_input.get("mode", "auto"),
        "rough_direction_hint": discovery_input.get("rough_direction_hint"),
        "applicant_profile": dict(discovery_input["applicant_profile"]),
        "track_record": dict(discovery_input["track_record"]),
        "active_project_set": dict(
            discovery_input.get("active_project_set")
            or {
                "metadata": dict(discovery_input["metadata"]),
                "project_set_id": f"{discovery_input['discovery_input_id']}-projects",
                "projects": [],
            }
        ),
        "preliminary_evidence_pack": dict(
            discovery_input.get("preliminary_evidence_pack")
            or {
                "metadata": dict(discovery_input["metadata"]),
                "evidence_pack_id": f"{discovery_input['discovery_input_id']}-prelim",
                "evidence_items": [],
            }
        ),
        "funding_opportunity_pool": [dict(item) for item in funding_opportunity_pool],
    }
