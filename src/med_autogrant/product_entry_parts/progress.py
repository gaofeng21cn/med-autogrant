from __future__ import annotations

from med_autogrant.product_entry_parts.shared import *  # noqa: F401,F403
from med_autogrant.product_entry_parts.loop_contracts import (
    _build_grant_user_loop_commands,
    _build_mainline_snapshot,
    _build_next_action_payload,
    _validate_grant_direct_entry_contract,
    _validate_grant_user_loop_contract,
)
from med_autogrant.product_entry_parts.runtime_surfaces import (
    _build_product_command_catalog,
    _build_runtime_continuity_surfaces,
)



class ProductEntryProgressMixin:
    def read_grant_progress(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        context = self._load_projection_context(input_path=input_path)
        route_report = context["route_report"]
        workspace_summary = context["workspace_summary"]
        critique_summary = context["critique_summary"]
        resolved_input_path = context["resolved_input_path"]

        verification_checkpoint = _require_mapping(
            route_report,
            "verification_checkpoint",
            context="stage-route-report",
        )
        identity = _require_mapping(
            verification_checkpoint,
            "identity",
            context="stage-route-report.verification_checkpoint",
        )
        route = _require_mapping(route_report, "route", context="stage-route-report")
        next_step = _require_mapping(route, "next_step", context="stage-route-report.route")

        grant_run_id = _require_nonempty_string_from_mapping(
            route_report,
            "grant_run_id",
            context="stage-route-report",
        )
        workspace_id = _require_nonempty_string_from_mapping(
            route_report,
            "workspace_id",
            context="stage-route-report",
        )
        lifecycle_stage = _require_nonempty_string_from_mapping(
            route_report,
            "lifecycle_stage",
            context="stage-route-report",
        )
        draft_id = _require_optional_string(identity.get("draft_id"), field_name="draft_id")
        checkpoint_status = _require_nonempty_string_from_mapping(
            verification_checkpoint,
            "checkpoint_status",
            context="stage-route-report.verification_checkpoint",
        )
        recommended_next_stage = _require_nonempty_string_from_mapping(
            next_step,
            "recommended_stage",
            context="stage-route-report.route.next_step",
        )
        progress_projection = {
            "projection_version": GRANT_PROGRESS_PROJECTION_VERSION,
            "projection_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "workspace_surface_kind": "nsfc_workspace",
            "current_stage": lifecycle_stage,
            "current_stage_summary": _build_current_stage_summary(
                lifecycle_stage=lifecycle_stage,
                checkpoint_status=checkpoint_status,
                next_step=next_step,
            ),
            "checkpoint_status": checkpoint_status,
            "recommended_next_stage": recommended_next_stage,
            "current_blockers": _read_projection_blockers(
                workspace_summary=workspace_summary,
                critique_summary=critique_summary,
            ),
            "next_system_action": _read_next_system_action(next_step),
            "needs_author_decision": bool(next_step.get("requires_human_confirmation")),
            "author_decision_summary": _build_author_decision_summary(next_step),
            "focus": _build_focus_payload(
                workspace_summary=workspace_summary,
                critique_summary=critique_summary,
            ),
            "product_entry_surface": {
                "builder_command": public_command_label("build-product-entry"),
                "target_domain_id": TARGET_DOMAIN_ID,
                "supported_entry_modes": list(SUPPORTED_ENTRY_MODES),
                "task_intent_required": True,
                "workspace_path": str(resolved_input_path),
            },
        }
        progress_projection["status_narration_contract"] = build_status_narration_contract(
            contract_id=f"grant-progress::{workspace_id}",
            surface_kind="grant_progress",
            stage={
                "current_stage": lifecycle_stage,
                "recommended_next_stage": recommended_next_stage,
                "checkpoint_status": checkpoint_status,
            },
            readiness={
                "needs_author_decision": bool(next_step.get("requires_human_confirmation")),
            },
            current_blockers=(progress_projection.get("current_blockers") or [])[:8],
            latest_update=str(progress_projection.get("current_stage_summary") or "").strip() or None,
            next_step=str(progress_projection.get("next_system_action") or "").strip() or None,
            facts={
                "workspace_id": workspace_id,
                "grant_run_id": grant_run_id,
            },
            answer_checklist=PROGRESS_ANSWER_CHECKLIST,
        )
        family_orchestration = _build_family_orchestration_companion(
            current_route_id=lifecycle_stage,
            recommended_route_id=recommended_next_stage,
            recommended_route_status=_route_status_from_route_id(recommended_next_stage),
            needs_author_decision=bool(next_step.get("requires_human_confirmation")),
            workspace_summary=workspace_summary,
            review_surface_ref="/progress_projection/product_entry_surface",
            event_envelope_surface_ref="/progress_projection/next_system_action",
            checkpoint_lineage_surface_ref="/progress_projection/checkpoint_status",
            resume_surface_kind=GRANT_USER_LOOP_KIND,
        )
        payload = {
            "ok": True,
            "command": "grant-progress",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
            "grant_intake_audit": dict(
                _require_mapping(workspace_summary, "grant_intake_audit", context="summarize-workspace")
            ),
            "grant_evidence_grounding": dict(
                _require_mapping(workspace_summary, "grant_evidence_grounding", context="summarize-workspace")
            ),
            "progress_projection": progress_projection,
            "family_orchestration": family_orchestration,
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_PROGRESS_SCHEMA_FILE,
            context="grant_progress",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
        return payload

    def read_grant_cockpit(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        progress_payload = self.read_grant_progress(input_path=input_path)
        progress_projection = _require_mapping(
            progress_payload,
            "progress_projection",
            context="grant-progress",
        )
        resolved_input_path = Path(progress_payload["input_path"]).expanduser().resolve()
        context = self._load_projection_context(input_path=resolved_input_path)
        workspace_summary = context["workspace_summary"]
        critique_summary = context["critique_summary"]

        blocking_issues = list(progress_projection.get("current_blockers", []))
        needs_author_decision = bool(progress_projection.get("needs_author_decision"))
        workspace_status = _build_workspace_status(
            blockers=blocking_issues,
            needs_author_decision=needs_author_decision,
        )
        workspace_alerts = list(blocking_issues)
        author_decision_summary = progress_projection.get("author_decision_summary")
        if isinstance(author_decision_summary, str) and author_decision_summary.strip():
            workspace_alerts.append(author_decision_summary.strip())
        current_stage = _require_nonempty_string_from_mapping(
            progress_projection,
            "current_stage",
            context="grant-progress.progress_projection",
        )
        recommended_next_stage = _require_nonempty_string_from_mapping(
            progress_projection,
            "recommended_next_stage",
            context="grant-progress.progress_projection",
        )
        family_orchestration = _build_family_orchestration_companion(
            current_route_id=current_stage,
            recommended_route_id=recommended_next_stage,
            recommended_route_status=_route_status_from_route_id(recommended_next_stage),
            needs_author_decision=bool(progress_projection.get("needs_author_decision")),
            workspace_summary=workspace_summary,
            review_surface_ref="/grant_cockpit/commands/build_direct_entry",
            event_envelope_surface_ref="/grant_cockpit/progress_projection/next_system_action",
            checkpoint_lineage_surface_ref="/grant_cockpit/progress_projection/checkpoint_status",
            resume_surface_kind=GRANT_USER_LOOP_KIND,
        )

        payload = {
            "ok": True,
            "command": "grant-cockpit",
            "grant_run_id": progress_payload["grant_run_id"],
            "workspace_id": progress_payload["workspace_id"],
            "draft_id": progress_payload["draft_id"],
            "lifecycle_stage": progress_payload["lifecycle_stage"],
            "input_path": str(resolved_input_path),
            "grant_intake_audit": dict(
                _require_mapping(progress_payload, "grant_intake_audit", context="grant-progress")
            ),
            "grant_evidence_grounding": dict(
                _require_mapping(progress_payload, "grant_evidence_grounding", context="grant-progress")
            ),
            "grant_cockpit": {
                "cockpit_kind": GRANT_COCKPIT_KIND,
                "workspace_overview": _build_workspace_overview(
                    workspace_summary=workspace_summary,
                    progress_projection=progress_projection,
                    critique_summary=critique_summary,
                ),
                "workspace_status": workspace_status,
                "workspace_alerts": workspace_alerts,
                "progress_projection": dict(progress_projection),
                "commands": _build_product_command_catalog(resolved_input_path),
            },
            "family_orchestration": family_orchestration,
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_COCKPIT_SCHEMA_FILE,
            context="grant_cockpit",
            grant_run_id=progress_payload["grant_run_id"],
            workspace_id=progress_payload["workspace_id"],
            lifecycle_stage=progress_payload["lifecycle_stage"],
        )
        return payload

    def build_grant_direct_entry(
        self,
        *,
        input_path: str | Path,
        task_intent: str,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        resolved_task_intent = _require_nonempty_string(task_intent, field_name="task_intent")
        direct_payload = self.build(
            input_path=resolved_input_path,
            entry_mode="direct",
            task_intent=resolved_task_intent,
            funding_call=funding_call,
        )
        opl_handoff_payload = self.build(
            input_path=resolved_input_path,
            entry_mode="opl-handoff",
            task_intent=resolved_task_intent,
            funding_call=funding_call,
        )
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
        cockpit_payload = self.read_grant_cockpit(input_path=resolved_input_path)

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
        workspace_overview = _require_mapping(
            cockpit,
            "workspace_overview",
            context="grant_direct_entry.grant_cockpit",
        )
        command_catalog = _build_product_command_catalog(resolved_input_path)
        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
        )
        mainline_payload = read_mainline_status()
        current_line = _require_mapping(
            mainline_payload,
            "current_line",
            context="mainline_status",
        )
        runtime_summary = {
            "current_owner_line": _require_nonempty_string_from_mapping(
                current_line,
                "current_owner_line",
                context="mainline_status.current_line",
            ),
            "runtime_owner": "upstream_hermes_agent",
        }
        managed_runtime_contract = _build_managed_runtime_contract()
        grant_run_id = _require_nonempty_string_from_mapping(
            direct_payload,
            "grant_run_id",
            context="grant_direct_entry",
        )
        workspace_id = _require_nonempty_string_from_mapping(
            direct_payload,
            "workspace_id",
            context="grant_direct_entry",
        )
        lifecycle_stage = _require_nonempty_string_from_mapping(
            direct_payload,
            "lifecycle_stage",
            context="grant_direct_entry",
        )
        continuity_surfaces = _build_runtime_continuity_surfaces(
            progress_projection=progress_projection,
            workspace_summary=workspace_summary,
            runtime_summary=runtime_summary,
            managed_runtime_contract=managed_runtime_contract,
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
        direct_executor_routing_contract = _require_mapping(
            direct_entry,
            "executor_routing_contract",
            context="grant_direct_entry.direct_entry",
        )
        grant_direct_entry = {
            "entry_version": GRANT_DIRECT_ENTRY_VERSION,
            "entry_kind": GRANT_DIRECT_ENTRY_KIND,
            "target_domain_id": TARGET_DOMAIN_ID,
            "workspace_surface_kind": "nsfc_workspace",
            "task_intent": resolved_task_intent,
            "workspace_overview": dict(workspace_overview),
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
        current_stage_route_id = _require_nonempty_string_from_mapping(
            grant_direct_entry["current_stage_route"],
            "route_id",
            context="grant_direct_entry.current_stage_route",
        )
        recommended_route_id = _require_nonempty_string_from_mapping(
            grant_direct_entry["recommended_executor_route"],
            "route_id",
            context="grant_direct_entry.recommended_executor_route",
        )
        recommended_route_status = _require_nonempty_string_from_mapping(
            grant_direct_entry["recommended_executor_route"],
            "route_status",
            context="grant_direct_entry.recommended_executor_route",
        )
        needs_author_decision = bool(progress_projection.get("needs_author_decision"))
        family_orchestration = _build_family_orchestration_companion(
            current_route_id=current_stage_route_id,
            recommended_route_id=recommended_route_id,
            recommended_route_status=recommended_route_status,
            needs_author_decision=needs_author_decision,
            intake_evidence_companion=_optional_mapping(
                _require_mapping(cockpit_payload, "family_orchestration", context="grant_direct_entry.grant_cockpit"),
                "intake_evidence_companion",
            ),
            project_profile_companion=_optional_mapping(
                _require_mapping(cockpit_payload, "family_orchestration", context="grant_direct_entry.grant_cockpit"),
                "project_profile_companion",
            ),
            review_surface_ref="/grant_direct_entry/recommended_executor_route",
            event_envelope_surface_ref="/grant_direct_entry/progress_projection/next_system_action",
            checkpoint_lineage_surface_ref="/grant_direct_entry/progress_projection/checkpoint_status",
            resume_surface_kind=GRANT_USER_LOOP_KIND,
        )
        payload = {
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
            "grant_direct_entry": grant_direct_entry,
            "session_continuity": dict(continuity_surfaces["session_continuity"]),
            "progress_projection": dict(continuity_surfaces["progress_projection"]),
            "artifact_inventory": dict(continuity_surfaces["artifact_inventory"]),
            "runtime_control": dict(continuity_surfaces["runtime_control"]),
            "family_orchestration": family_orchestration,
        }
        _validate_grant_direct_entry_contract(
            payload,
            grant_run_id=direct_payload["grant_run_id"],
            workspace_id=direct_payload["workspace_id"],
            lifecycle_stage=direct_payload["lifecycle_stage"],
        )
        return payload

    def build_grant_user_loop(
        self,
        *,
        input_path: str | Path,
        task_intent: str,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        resolved_task_intent = _require_nonempty_string(task_intent, field_name="task_intent")
        direct_entry_payload = self.build_grant_direct_entry(
            input_path=resolved_input_path,
            task_intent=resolved_task_intent,
            funding_call=funding_call,
        )
        grant_direct_entry = _require_mapping(
            direct_entry_payload,
            "grant_direct_entry",
            context="grant_user_loop.grant_direct_entry",
        )
        mainline_status = read_mainline_status()
        mainline_snapshot = _build_mainline_snapshot(mainline_status)
        recommended_executor_route = _require_mapping(
            grant_direct_entry,
            "recommended_executor_route",
            context="grant_user_loop.grant_direct_entry",
        )
        grant_run_id = _require_nonempty_string_from_mapping(
            direct_entry_payload,
            "grant_run_id",
            context="grant_user_loop",
        )
        workspace_id = _require_nonempty_string_from_mapping(
            direct_entry_payload,
            "workspace_id",
            context="grant_user_loop",
        )
        draft_id = _optional_string_from_mapping(direct_entry_payload, "draft_id")
        next_action = _build_next_action_payload(
            recommended_executor_route=recommended_executor_route,
            input_path=resolved_input_path,
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        user_loop = _build_grant_user_loop_commands(
            input_path=resolved_input_path,
            task_intent=resolved_task_intent,
            run_recommended_route=next_action.get("command"),
        )
        grant_user_loop = {
            "entry_version": GRANT_USER_LOOP_VERSION,
            "entry_kind": GRANT_USER_LOOP_KIND,
            "target_domain_id": TARGET_DOMAIN_ID,
            "workspace_surface_kind": "nsfc_workspace",
            "task_intent": resolved_task_intent,
            "mainline_snapshot": mainline_snapshot,
            "grant_direct_entry": dict(grant_direct_entry),
            "next_action": next_action,
            "user_loop": user_loop,
        }
        session_continuity = _require_mapping(
            direct_entry_payload,
            "session_continuity",
            context="grant_user_loop.grant_direct_entry",
        )
        progress_surface = _require_mapping(
            direct_entry_payload,
            "progress_projection",
            context="grant_user_loop.grant_direct_entry",
        )
        artifact_inventory = _require_mapping(
            direct_entry_payload,
            "artifact_inventory",
            context="grant_user_loop.grant_direct_entry",
        )
        runtime_control = _require_mapping(
            direct_entry_payload,
            "runtime_control",
            context="grant_user_loop.grant_direct_entry",
        )
        grant_user_loop["session_continuity"] = dict(session_continuity)
        grant_user_loop["progress_projection"] = dict(progress_surface)
        grant_user_loop["artifact_inventory"] = dict(artifact_inventory)
        grant_user_loop["runtime_control"] = dict(runtime_control)
        current_stage_route = _require_mapping(
            grant_direct_entry,
            "current_stage_route",
            context="grant_user_loop.grant_direct_entry",
        )
        progress_projection = _require_mapping(
            grant_direct_entry,
            "progress_projection",
            context="grant_user_loop.grant_direct_entry",
        )
        current_route_id = _require_nonempty_string_from_mapping(
            current_stage_route,
            "route_id",
            context="grant_user_loop.grant_direct_entry.current_stage_route",
        )
        recommended_route_id = _require_nonempty_string_from_mapping(
            next_action,
            "route_id",
            context="grant_user_loop.next_action",
        )
        recommended_route_status = _require_nonempty_string_from_mapping(
            next_action,
            "route_status",
            context="grant_user_loop.next_action",
        )
        needs_author_decision = bool(progress_projection.get("needs_author_decision"))
        family_orchestration = _build_family_orchestration_companion(
            current_route_id=current_route_id,
            recommended_route_id=recommended_route_id,
            recommended_route_status=recommended_route_status,
            needs_author_decision=needs_author_decision,
            intake_evidence_companion=_optional_mapping(
                _require_mapping(direct_entry_payload, "family_orchestration", context="grant_user_loop.grant_direct_entry"),
                "intake_evidence_companion",
            ),
            project_profile_companion=_optional_mapping(
                _require_mapping(direct_entry_payload, "family_orchestration", context="grant_user_loop.grant_direct_entry"),
                "project_profile_companion",
            ),
            review_surface_ref="/grant_user_loop/next_action",
            event_envelope_surface_ref="/grant_user_loop/next_action",
            checkpoint_lineage_surface_ref=(
                "/grant_user_loop/grant_direct_entry/progress_projection/checkpoint_status"
            ),
            resume_surface_kind=GRANT_USER_LOOP_KIND,
        )
        payload = {
            "ok": True,
            "command": "grant-user-loop",
            "grant_run_id": direct_entry_payload["grant_run_id"],
            "workspace_id": direct_entry_payload["workspace_id"],
            "draft_id": direct_entry_payload["draft_id"],
            "lifecycle_stage": direct_entry_payload["lifecycle_stage"],
            "input_path": direct_entry_payload["input_path"],
            "grant_user_loop": grant_user_loop,
            "family_orchestration": family_orchestration,
        }
        _validate_grant_user_loop_contract(
            payload,
            grant_run_id=direct_entry_payload["grant_run_id"],
            workspace_id=direct_entry_payload["workspace_id"],
            lifecycle_stage=direct_entry_payload["lifecycle_stage"],
        )
        return payload
