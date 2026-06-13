from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.product_entry_parts.loop_contracts import (
    _validate_grant_direct_entry_contract,
)
from med_autogrant.product_entry_parts.orchestration_companions import (
    _build_family_orchestration_companion,
    _build_managed_runtime_contract,
)
from med_autogrant.product_entry_parts.primitives import (
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_DIRECT_ENTRY_VERSION,
    GRANT_USER_LOOP_KIND,
    TARGET_DOMAIN_ID,
    _assert_entry_mode,
    _optional_mapping,
    _read_funding_call_from_summary,
    _read_nonempty_string_list,
    _require_mapping,
    _require_matching_top_level_identity,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.runtime_surfaces import (
    _build_product_command_catalog,
    _build_runtime_continuity_surfaces,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.runtime_defaults import build_default_runtime_summary


def build_grant_direct_entry_payload(
    *,
    resolved_input_path: Path,
    resolved_task_intent: str,
    direct_payload: Mapping[str, Any],
    opl_handoff_payload: Mapping[str, Any],
    cockpit_payload: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
) -> dict[str, Any]:
    direct_entry, opl_handoff_entry = _read_entry_mode_payloads(
        direct_payload=direct_payload,
        opl_handoff_payload=opl_handoff_payload,
    )
    _require_matching_top_level_identity(
        direct_payload,
        opl_handoff_payload,
        context="grant_direct_entry.opl_handoff_entry",
    )
    _require_matching_top_level_identity(
        direct_payload,
        cockpit_payload,
        context="grant_direct_entry.grant_cockpit",
    )

    cockpit = _require_mapping(
        cockpit_payload,
        "grant_cockpit",
        context="grant_direct_entry.grant_cockpit",
    )
    progress_projection = _require_mapping(
        cockpit,
        "progress_projection",
        context="grant_direct_entry.grant_cockpit",
    )
    identity = _read_grant_direct_entry_identity(direct_payload)
    continuity_surfaces = _build_grant_direct_entry_runtime_surfaces(
        resolved_input_path=resolved_input_path,
        resolved_task_intent=resolved_task_intent,
        progress_projection=progress_projection,
        workspace_summary=workspace_summary,
        grant_run_id=identity["grant_run_id"],
        workspace_id=identity["workspace_id"],
        lifecycle_stage=identity["lifecycle_stage"],
    )
    grant_direct_entry = _build_grant_direct_entry_surface(
        resolved_task_intent=resolved_task_intent,
        cockpit=cockpit,
        progress_projection=progress_projection,
        direct_entry=direct_entry,
        opl_handoff_entry=opl_handoff_entry,
    )
    family_orchestration = _build_grant_direct_entry_family_orchestration(
        cockpit_payload=cockpit_payload,
        grant_direct_entry=grant_direct_entry,
        progress_projection=progress_projection,
    )
    payload = _build_grant_direct_entry_top_level_payload(
        direct_payload=direct_payload,
        cockpit_payload=cockpit_payload,
        grant_direct_entry=grant_direct_entry,
        continuity_surfaces=continuity_surfaces,
        family_orchestration=family_orchestration,
    )
    _validate_grant_direct_entry_contract(
        payload,
        grant_run_id=identity["grant_run_id"],
        workspace_id=identity["workspace_id"],
        lifecycle_stage=identity["lifecycle_stage"],
    )
    return payload


def _read_entry_mode_payloads(
    *,
    direct_payload: Mapping[str, Any],
    opl_handoff_payload: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    direct_entry = _require_mapping(
        direct_payload,
        "product_entry",
        context="grant_direct_entry.direct_entry",
    )
    opl_handoff_entry = _require_mapping(
        opl_handoff_payload,
        "product_entry",
        context="grant_direct_entry.opl_handoff_entry",
    )
    _assert_entry_mode(
        direct_entry,
        expected_entry_mode="direct",
        context="grant_direct_entry.direct_entry",
    )
    _assert_entry_mode(
        opl_handoff_entry,
        expected_entry_mode="opl-handoff",
        context="grant_direct_entry.opl_handoff_entry",
    )
    return direct_entry, opl_handoff_entry


def _read_grant_direct_entry_identity(payload: Mapping[str, Any]) -> dict[str, str]:
    return {
        "grant_run_id": _require_nonempty_string_from_mapping(
            payload,
            "grant_run_id",
            context="grant_direct_entry",
        ),
        "workspace_id": _require_nonempty_string_from_mapping(
            payload,
            "workspace_id",
            context="grant_direct_entry",
        ),
        "lifecycle_stage": _require_nonempty_string_from_mapping(
            payload,
            "lifecycle_stage",
            context="grant_direct_entry",
        ),
    }


def _build_grant_direct_entry_runtime_surfaces(
    *,
    resolved_input_path: Path,
    resolved_task_intent: str,
    progress_projection: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> dict[str, dict[str, Any]]:
    command_catalog = _build_product_command_catalog(resolved_input_path)
    mainline_payload = read_mainline_status()
    current_line = _require_mapping(
        mainline_payload,
        "current_line",
        context="mainline_status",
    )
    runtime_summary = build_default_runtime_summary(
        current_owner_line=_require_nonempty_string_from_mapping(
            current_line,
            "current_owner_line",
            context="mainline_status.current_line",
        )
    )
    return _build_runtime_continuity_surfaces(
        progress_projection=progress_projection,
        workspace_summary=workspace_summary,
        runtime_summary=runtime_summary,
        managed_runtime_contract=_build_managed_runtime_contract(),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=str(resolved_input_path),
        funding_call=_read_funding_call_from_summary(workspace_summary),
        grant_progress_command=command_catalog["grant_progress"],
        summarize_workspace_command=command_catalog["summarize_workspace"],
        stage_route_report_command=command_catalog["stage_route_report"],
        grant_user_loop_command=public_cli_command(
            "grant-user-loop",
            "--input",
            str(resolved_input_path),
            "--task-intent",
            resolved_task_intent,
            "--format",
            "json",
        ),
        grant_direct_entry_command=public_cli_command(
            "grant-direct-entry",
            "--input",
            str(resolved_input_path),
            "--task-intent",
            resolved_task_intent,
            "--format",
            "json",
        ),
    )


def _build_grant_direct_entry_surface(
    *,
    resolved_task_intent: str,
    cockpit: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    direct_entry: Mapping[str, Any],
    opl_handoff_entry: Mapping[str, Any],
) -> dict[str, Any]:
    direct_executor_routing_contract = _require_mapping(
        direct_entry,
        "executor_routing_contract",
        context="grant_direct_entry.direct_entry",
    )
    return {
        "entry_version": GRANT_DIRECT_ENTRY_VERSION,
        "entry_kind": GRANT_DIRECT_ENTRY_KIND,
        "target_domain_id": TARGET_DOMAIN_ID,
        "workspace_surface_kind": "nsfc_workspace",
        "task_intent": resolved_task_intent,
        "workspace_overview": dict(
            _require_mapping(
                cockpit,
                "workspace_overview",
                context="grant_direct_entry.grant_cockpit",
            )
        ),
        "workspace_status": _require_nonempty_string_from_mapping(
            cockpit,
            "workspace_status",
            context="grant_direct_entry.grant_cockpit",
        ),
        "workspace_alerts": _read_nonempty_string_list(
            cockpit.get("workspace_alerts"),
            context="grant_direct_entry.grant_cockpit",
        ),
        "progress_projection": dict(progress_projection),
        "current_stage_route": dict(
            _require_mapping(
                direct_executor_routing_contract,
                "current_stage_route",
                context="grant_direct_entry.direct_entry.executor_routing_contract",
            )
        ),
        "recommended_executor_route": dict(
            _require_mapping(
                direct_executor_routing_contract,
                "recommended_executor_route",
                context="grant_direct_entry.direct_entry.executor_routing_contract",
            )
        ),
        "direct_entry": dict(direct_entry),
        "opl_handoff_entry": dict(opl_handoff_entry),
    }


def _build_grant_direct_entry_family_orchestration(
    *,
    cockpit_payload: Mapping[str, Any],
    grant_direct_entry: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
) -> dict[str, Any]:
    current_stage_route_id = _require_nonempty_string_from_mapping(
        _require_mapping(
            grant_direct_entry,
            "current_stage_route",
            context="grant_direct_entry",
        ),
        "route_id",
        context="grant_direct_entry.current_stage_route",
    )
    recommended_executor_route = _require_mapping(
        grant_direct_entry,
        "recommended_executor_route",
        context="grant_direct_entry",
    )
    cockpit_family_orchestration = _require_mapping(
        cockpit_payload,
        "family_orchestration",
        context="grant_direct_entry.grant_cockpit",
    )
    return _build_family_orchestration_companion(
        current_route_id=current_stage_route_id,
        recommended_route_id=_require_nonempty_string_from_mapping(
            recommended_executor_route,
            "route_id",
            context="grant_direct_entry.recommended_executor_route",
        ),
        recommended_route_status=_require_nonempty_string_from_mapping(
            recommended_executor_route,
            "route_status",
            context="grant_direct_entry.recommended_executor_route",
        ),
        needs_author_decision=bool(progress_projection.get("needs_author_decision")),
        intake_evidence_companion=_optional_mapping(
            cockpit_family_orchestration,
            "intake_evidence_companion",
        ),
        project_profile_companion=_optional_mapping(
            cockpit_family_orchestration,
            "project_profile_companion",
        ),
        review_surface_ref="/grant_direct_entry/recommended_executor_route",
        event_envelope_surface_ref="/grant_direct_entry/progress_projection/next_system_action",
        checkpoint_lineage_surface_ref="/grant_direct_entry/progress_projection/checkpoint_status",
        resume_surface_kind=GRANT_USER_LOOP_KIND,
    )


def _build_grant_direct_entry_top_level_payload(
    *,
    direct_payload: Mapping[str, Any],
    cockpit_payload: Mapping[str, Any],
    grant_direct_entry: Mapping[str, Any],
    continuity_surfaces: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "ok": True,
        "command": "grant-direct-entry",
        "grant_run_id": direct_payload["grant_run_id"],
        "workspace_id": direct_payload["workspace_id"],
        "draft_id": direct_payload["draft_id"],
        "lifecycle_stage": direct_payload["lifecycle_stage"],
        "input_path": direct_payload["input_path"],
        "grant_intake_audit": dict(
            _require_mapping(cockpit_payload, "grant_intake_audit", context="grant-cockpit")
        ),
        "grant_evidence_grounding": dict(
            _require_mapping(cockpit_payload, "grant_evidence_grounding", context="grant-cockpit")
        ),
        "grant_direct_entry": dict(grant_direct_entry),
        "session_continuity": dict(continuity_surfaces["session_continuity"]),
        "progress_projection": dict(continuity_surfaces["progress_projection"]),
        "artifact_inventory": dict(continuity_surfaces["artifact_inventory"]),
        "runtime_control": dict(continuity_surfaces["runtime_control"]),
        "family_orchestration": dict(family_orchestration),
    }
