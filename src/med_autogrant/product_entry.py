from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.hermes_runtime import (
    _build_domain_entry_contract,
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_DIRECT_ENTRY_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    GRANT_USER_LOOP_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.workspace import WorkspaceFileError, WorkspaceStateError


PRODUCT_ENTRY_VERSION = 1
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
PRODUCT_ENTRY_MANIFEST_KIND = "med_auto_grant_product_entry_manifest"
PRODUCT_ENTRY_MANIFEST_VERSION = 2
PRODUCT_FRONTDESK_KIND = "product_frontdesk"
TARGET_DOMAIN_ID = "med-autogrant"
SUPPORTED_ENTRY_MODES = ("direct", "opl-handoff")
GRANT_PROGRESS_PROJECTION_VERSION = 1
GRANT_PROGRESS_PROJECTION_KIND = "grant_progress"
GRANT_COCKPIT_KIND = "grant_cockpit"
GRANT_DIRECT_ENTRY_VERSION = 1
GRANT_DIRECT_ENTRY_KIND = "grant_direct_entry"
GRANT_USER_LOOP_VERSION = 1
GRANT_USER_LOOP_KIND = "grant_user_loop"
REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}
LANDED_ROUTE_IDS = {"critique", "revision", "artifact_bundle", "final_package", "hosted_contract_bundle"}


class MedAutoGrantProductEntry:
    """轻量 grant product entry 壳，复用已 landed 的 domain entry 与 Hermes substrate contract。"""

    def __init__(self, *, domain_entry: MedAutoGrantDomainEntry | None = None) -> None:
        self._domain_entry = domain_entry or MedAutoGrantDomainEntry()

    def build(
        self,
        *,
        input_path: str | Path,
        entry_mode: str,
        task_intent: str,
        output_path: str | Path | None = None,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        resolved_entry_mode = _require_entry_mode(entry_mode)
        resolved_task_intent = _require_nonempty_string(task_intent, field_name="task_intent")

        route_report = self._domain_entry.dispatch(
            {
                "command": "stage-route-report",
                "input_path": str(resolved_input_path),
            }
        )
        if route_report.get("ok") is not True:
            raise WorkspaceStateError("product entry 只允许从已验证通过的 workspace 构建。")

        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
        )

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
        verification_checkpoint = _require_mapping(
            route_report,
            "verification_checkpoint",
            context="stage-route-report",
        )
        checkpoint_status = _require_nonempty_string_from_mapping(
            verification_checkpoint,
            "checkpoint_status",
            context="stage-route-report.verification_checkpoint",
        )
        identity = _require_mapping(
            verification_checkpoint,
            "identity",
            context="stage-route-report.verification_checkpoint",
        )
        draft_id = _require_optional_string(identity.get("draft_id"), field_name="draft_id")

        route = _require_mapping(route_report, "route", context="stage-route-report")
        next_step = _require_mapping(route, "next_step", context="stage-route-report.route")
        recommended_next_stage = _require_nonempty_string_from_mapping(
            next_step,
            "recommended_stage",
            context="stage-route-report.route.next_step",
        )

        resolved_funding_call = (
            _require_nonempty_string(funding_call, field_name="funding_call")
            if funding_call is not None
            else _read_funding_call_from_summary(workspace_summary)
        )

        current_program_contract = _read_current_program_contract()
        executor_routing_contract = _build_executor_routing_contract(
            current_stage=lifecycle_stage,
            recommended_next_stage=recommended_next_stage,
            include_route_catalog=True,
        )
        _validate_executor_routing_contract(
            executor_routing_contract,
            current_stage=lifecycle_stage,
            recommended_next_stage=recommended_next_stage,
            include_route_catalog=True,
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
        product_entry = {
            "entry_version": PRODUCT_ENTRY_VERSION,
            "entry_kind": PRODUCT_ENTRY_KIND,
            "target_domain_id": TARGET_DOMAIN_ID,
            "task_intent": resolved_task_intent,
            "entry_mode": resolved_entry_mode,
            "workspace_locator": {
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(resolved_input_path),
            },
            "runtime_session_contract": {
                "grant_run_id": grant_run_id,
                "session_handle_kind": "grant_run_id",
                "start_entry": "run-local",
                "resume_entry": "resume-local",
                "runtime_substrate_contract": _build_runtime_substrate_contract(
                    current_program_contract=current_program_contract,
                ),
                "runtime_state_contract": _build_runtime_state_contract(),
            },
            "return_surface_contract": {
                "entry_adapter": "MedAutoGrantDomainEntry",
                "default_formal_entry": "CLI",
                "supported_entry_modes": list(SUPPORTED_ENTRY_MODES),
                "domain_entry_contract": _build_domain_entry_contract(),
                "checkpoint_aggregation_surface": "stage-route-report",
                "operator_contract": _build_operator_contract(),
            },
            "domain_payload": {
                "workspace_id": workspace_id,
                "draft_id": draft_id,
                "funding_call": resolved_funding_call,
            },
            "stage_snapshot": {
                "lifecycle_stage": lifecycle_stage,
                "checkpoint_status": checkpoint_status,
                "recommended_next_stage": recommended_next_stage,
            },
            "executor_routing_contract": executor_routing_contract,
        }
        _validate_contract_schema(
            product_entry,
            schema_file=PRODUCT_ENTRY_SCHEMA_FILE,
            context="product_entry",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

        resolved_output_path = None
        if output_path is not None:
            resolved_output_path = Path(output_path).expanduser().resolve()
            _write_product_entry_output(resolved_output_path, product_entry)

        return {
            "ok": True,
            "command": "build-product-entry",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
            "output_path": str(resolved_output_path) if resolved_output_path is not None else None,
            "product_entry": product_entry,
        }

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
            "current_blockers": _read_blocking_issues(critique_summary),
            "next_system_action": _read_next_system_action(next_step),
            "needs_author_decision": bool(next_step.get("requires_human_confirmation")),
            "author_decision_summary": _build_author_decision_summary(next_step),
            "focus": _build_focus_payload(
                workspace_summary=workspace_summary,
                critique_summary=critique_summary,
            ),
            "product_entry_surface": {
                "builder_command": "build-product-entry",
                "target_domain_id": TARGET_DOMAIN_ID,
                "supported_entry_modes": list(SUPPORTED_ENTRY_MODES),
                "task_intent_required": True,
                "workspace_path": str(resolved_input_path),
            },
        }
        family_orchestration = _build_family_orchestration_companion(
            current_route_id=lifecycle_stage,
            recommended_route_id=recommended_next_stage,
            recommended_route_status=_route_status_from_route_id(recommended_next_stage),
            needs_author_decision=bool(next_step.get("requires_human_confirmation")),
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
        resolved_task_intent = _require_nonempty_string(task_intent, field_name="task_intent")
        direct_payload = self.build(
            input_path=input_path,
            entry_mode="direct",
            task_intent=resolved_task_intent,
            funding_call=funding_call,
        )
        opl_handoff_payload = self.build(
            input_path=input_path,
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
        cockpit_payload = self.read_grant_cockpit(input_path=input_path)

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
            "grant_direct_entry": grant_direct_entry,
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
        next_action = _build_next_action_payload(
            recommended_executor_route=recommended_executor_route,
            input_path=resolved_input_path,
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
        needs_author_decision = bool(progress_projection.get("needs_author_decision")) or (
            _require_nonempty_string_from_mapping(
                next_action,
                "action_kind",
                context="grant_user_loop.next_action",
            )
            == "prepare_pending_handoff"
        )
        family_orchestration = _build_family_orchestration_companion(
            current_route_id=current_route_id,
            recommended_route_id=recommended_route_id,
            recommended_route_status=recommended_route_status,
            needs_author_decision=needs_author_decision,
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

    def build_product_entry_manifest(
        self,
        *,
        input_path: str | Path,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        del funding_call
        resolved_input_path = Path(input_path).expanduser().resolve()
        progress_payload = self.read_grant_progress(input_path=resolved_input_path)
        progress_projection = _require_mapping(
            progress_payload,
            "progress_projection",
            context="grant-progress",
        )
        mainline_payload = read_mainline_status()
        mainline_snapshot = _build_mainline_snapshot(mainline_payload)
        current_runtime_owner = _require_mapping(
            mainline_payload,
            "current_runtime_owner",
            context="mainline_status",
        )
        current_phase = _require_mapping(
            mainline_payload,
            "current_phase",
            context="mainline_status",
        )
        command_catalog = _build_product_command_catalog(resolved_input_path)
        grant_user_loop_command = (
            "uv run python -m med_autogrant grant-user-loop "
            f"--input {resolved_input_path} --task-intent <describe-task-intent> --format json"
        )
        product_frontdesk_command = (
            "uv run python -m med_autogrant product-frontdesk "
            f"--input {resolved_input_path} --format json"
        )
        grant_cockpit_command = (
            f"uv run python -m med_autogrant grant-cockpit --input {resolved_input_path} --format json"
        )
        grant_direct_entry_command = (
            "uv run python -m med_autogrant grant-direct-entry "
            f"--input {resolved_input_path} --task-intent <describe-task-intent> --format json"
        )
        operator_loop_actions = {
            "open_loop": {
                "command": grant_user_loop_command,
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": "进入当前 direct grant user inbox shell。",
                "requires": [],
            },
            "inspect_progress": {
                "command": command_catalog["grant_progress"],
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                "summary": "读取当前 workspace 的阶段摘要、checkpoint 与下一步。",
                "requires": [],
            },
            "inspect_cockpit": {
                "command": grant_cockpit_command,
                "surface_kind": GRANT_COCKPIT_KIND,
                "summary": "查看主线 snapshot、对象面和当前 route action 汇总。",
                "requires": [],
            },
            "build_direct_entry": {
                "command": grant_direct_entry_command,
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                "summary": "把用户意图组合成当前 grant direct-entry contract。",
                "requires": ["task_intent"],
            },
        }
        current_route_id = _require_nonempty_string_from_mapping(
            progress_projection,
            "current_stage",
            context="grant-progress.progress_projection",
        )
        recommended_route_id = _require_nonempty_string_from_mapping(
            progress_projection,
            "recommended_next_stage",
            context="grant-progress.progress_projection",
        )
        family_orchestration = _build_family_orchestration_companion(
            current_route_id=current_route_id,
            recommended_route_id=recommended_route_id,
            recommended_route_status=_route_status_from_route_id(recommended_route_id),
            needs_author_decision=bool(progress_projection.get("needs_author_decision")),
            review_surface_ref="/product_entry_manifest/operator_loop_surface",
            event_envelope_surface_ref="/product_entry_manifest/recommended_command",
            checkpoint_lineage_surface_ref="/product_entry_manifest/repo_mainline/phase_status",
            resume_surface_kind=GRANT_USER_LOOP_KIND,
        )
        product_entry_quickstart = {
            "surface_kind": "product_entry_quickstart",
            "recommended_step_id": "open_frontdesk",
            "summary": (
                "先从 direct grant product frontdesk 进入当前 frontdoor，"
                "再回到 grant-user-loop，必要时读取 progress 或 cockpit projection。"
            ),
            "steps": [
                {
                    "step_id": "open_frontdesk",
                    "title": "Open grant frontdesk",
                    "command": product_frontdesk_command,
                    "surface_kind": PRODUCT_FRONTDESK_KIND,
                    "summary": "打开当前 direct grant frontdoor。",
                    "requires": [],
                },
                {
                    "step_id": "continue_grant_loop",
                    "title": "Continue current grant loop",
                    "command": grant_user_loop_command,
                    "surface_kind": GRANT_USER_LOOP_KIND,
                    "summary": operator_loop_actions["open_loop"]["summary"],
                    "requires": ["task_intent"],
                },
                {
                    "step_id": "inspect_progress",
                    "title": "Inspect current progress",
                    "command": command_catalog["grant_progress"],
                    "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                    "summary": operator_loop_actions["inspect_progress"]["summary"],
                    "requires": list(operator_loop_actions["inspect_progress"]["requires"]),
                },
                {
                    "step_id": "inspect_cockpit",
                    "title": "Inspect current cockpit",
                    "command": grant_cockpit_command,
                    "surface_kind": GRANT_COCKPIT_KIND,
                    "summary": operator_loop_actions["inspect_cockpit"]["summary"],
                    "requires": list(operator_loop_actions["inspect_cockpit"]["requires"]),
                },
            ],
            "resume_contract": dict(family_orchestration["resume_contract"]),
            "human_gate_ids": [
                gate["gate_id"]
                for gate in family_orchestration["human_gates"]
                if isinstance(gate, dict) and gate.get("gate_id")
            ],
        }

        return {
            "ok": True,
            "command": "product-entry-manifest",
            "grant_run_id": progress_payload["grant_run_id"],
            "workspace_id": progress_payload["workspace_id"],
            "draft_id": progress_payload["draft_id"],
            "lifecycle_stage": progress_payload["lifecycle_stage"],
            "input_path": progress_payload["input_path"],
            "product_entry_manifest": {
                "surface_kind": "product_entry_manifest",
                "manifest_version": PRODUCT_ENTRY_MANIFEST_VERSION,
                "manifest_kind": PRODUCT_ENTRY_MANIFEST_KIND,
                "target_domain_id": TARGET_DOMAIN_ID,
                "formal_entry": {
                    "default": "CLI",
                    "supported_protocols": ["MCP"],
                    "internal_surface": "MedAutoGrantDomainEntry",
                },
                "workspace_locator": {
                    "workspace_surface_kind": "nsfc_workspace",
                    "workspace_root": str(resolved_input_path),
                    "workspace_path": str(resolved_input_path),
                },
                "recommended_shell": "grant_user_loop",
                "recommended_command": grant_user_loop_command,
                "frontdesk_surface": {
                    "shell_key": "product_frontdesk",
                    "command": product_frontdesk_command,
                    "surface_kind": PRODUCT_FRONTDESK_KIND,
                    "summary": (
                        "当前 direct grant product frontdesk 先暴露前台入口、user loop、projection 与 shared handoff。"
                    ),
                },
                "operator_loop_surface": {
                    "shell_key": "grant_user_loop",
                    "command": grant_user_loop_command,
                    "surface_kind": GRANT_USER_LOOP_KIND,
                    "summary": (
                        "当前 operator loop 以 grant-user-loop 作为 direct grant user inbox shell，"
                        "在同一入口下汇总 progress、route action 与 mainline snapshot。"
                    ),
                },
                "operator_loop_actions": operator_loop_actions,
                "repo_mainline": {
                    "program_id": _require_nonempty_string_from_mapping(
                        mainline_payload,
                        "program_id",
                        context="mainline_status",
                    ),
                    "phase_id": _require_nonempty_string_from_mapping(
                        current_phase,
                        "phase_id",
                        context="mainline_status.current_phase",
                    ),
                    "phase_name": _require_nonempty_string_from_mapping(
                        current_phase,
                        "phase_name",
                        context="mainline_status.current_phase",
                    ),
                    "phase_status": _require_nonempty_string_from_mapping(
                        current_phase,
                        "status",
                        context="mainline_status.current_phase",
                    ),
                    "phase_summary": _require_nonempty_string_from_mapping(
                        current_phase,
                        "summary",
                        context="mainline_status.current_phase",
                    ),
                    "active_phase": _require_nonempty_string_from_mapping(
                        current_runtime_owner,
                        "active_phase",
                        context="mainline_status.current_runtime_owner",
                    ),
                    "active_tranche": _require_nonempty_string_from_mapping(
                        current_runtime_owner,
                        "active_tranche",
                        context="mainline_status.current_runtime_owner",
                    ),
                    "next_focus": list(mainline_snapshot["next_focus"]),
                },
                "runtime": {
                    "current_owner_line": _require_nonempty_string_from_mapping(
                        current_runtime_owner,
                        "current_owner_line",
                        context="mainline_status.current_runtime_owner",
                    ),
                    "runtime_owner": "upstream_hermes_agent",
                },
                "product_entry_shell": {
                    "product_frontdesk": {
                        "command": product_frontdesk_command,
                        "surface_kind": PRODUCT_FRONTDESK_KIND,
                    },
                    "grant_progress": {
                        "command": command_catalog["grant_progress"],
                        "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                    },
                    "grant_cockpit": {
                        "command": grant_cockpit_command,
                        "surface_kind": GRANT_COCKPIT_KIND,
                    },
                    "grant_direct_entry": {
                        "command": grant_direct_entry_command,
                        "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                    },
                    "grant_user_loop": {
                        "command": grant_user_loop_command,
                        "surface_kind": GRANT_USER_LOOP_KIND,
                    },
                },
                "shared_handoff": {
                    "direct_entry_builder": {
                        "command": command_catalog["build_direct_entry"],
                        "entry_mode": "direct",
                    },
                    "opl_handoff_builder": {
                        "command": command_catalog["build_opl_handoff"],
                        "entry_mode": "opl-handoff",
                    },
                },
                "product_entry_quickstart": product_entry_quickstart,
                "family_orchestration": family_orchestration,
                "product_entry_status": {
                    "summary": _require_nonempty_string_from_mapping(
                        current_phase,
                        "summary",
                        context="mainline_status.current_phase",
                    ),
                    "next_focus": list(mainline_snapshot["next_focus"]),
                    "remaining_gaps_count": len(mainline_snapshot["remaining_gaps"]),
                },
                "remaining_gaps": list(mainline_payload.get("remaining_gaps") or []),
                "notes": [
                    "This manifest freezes the current repo-tracked grant product shell only.",
                    "It does not claim that mature hosted runtime or Web UI is already landed.",
                    "funding_call stays part of direct-entry build time rather than manifest discovery time.",
                ],
            },
        }

    def build_product_frontdesk(
        self,
        *,
        input_path: str | Path,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        manifest_payload = self.build_product_entry_manifest(
            input_path=input_path,
            funding_call=funding_call,
        )
        manifest = _require_mapping(
            manifest_payload,
            "product_entry_manifest",
            context="product_frontdesk",
        )
        product_entry_shell = _require_mapping(
            manifest,
            "product_entry_shell",
            context="product_frontdesk.product_entry_manifest",
        )
        shared_handoff = _require_mapping(
            manifest,
            "shared_handoff",
            context="product_frontdesk.product_entry_manifest",
        )

        return {
            "ok": True,
            "command": "product-frontdesk",
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
            "product_frontdesk": {
                "surface_kind": PRODUCT_FRONTDESK_KIND,
                "recommended_action": "inspect_or_prepare_grant_loop",
                "target_domain_id": _require_nonempty_string_from_mapping(
                    manifest,
                    "target_domain_id",
                    context="product_frontdesk.product_entry_manifest",
                ),
                "workspace_locator": dict(_require_mapping(
                    manifest,
                    "workspace_locator",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "runtime": dict(_require_mapping(
                    manifest,
                    "runtime",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "product_entry_status": dict(_require_mapping(
                    manifest,
                    "product_entry_status",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "frontdesk_surface": dict(_require_mapping(
                    manifest,
                    "frontdesk_surface",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "operator_loop_surface": dict(_require_mapping(
                    manifest,
                    "operator_loop_surface",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "operator_loop_actions": dict(_require_mapping(
                    manifest,
                    "operator_loop_actions",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "product_entry_quickstart": dict(_require_mapping(
                    manifest,
                    "product_entry_quickstart",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "family_orchestration": dict(_require_mapping(
                    manifest,
                    "family_orchestration",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "product_entry_manifest": dict(manifest),
                "entry_surfaces": {
                    "frontdesk": dict(_require_mapping(
                        product_entry_shell,
                        "product_frontdesk",
                        context="product_frontdesk.product_entry_shell",
                    )),
                    "grant_progress": dict(_require_mapping(
                        product_entry_shell,
                        "grant_progress",
                        context="product_frontdesk.product_entry_shell",
                    )),
                    "grant_cockpit": dict(_require_mapping(
                        product_entry_shell,
                        "grant_cockpit",
                        context="product_frontdesk.product_entry_shell",
                    )),
                    "grant_direct_entry": dict(_require_mapping(
                        product_entry_shell,
                        "grant_direct_entry",
                        context="product_frontdesk.product_entry_shell",
                    )),
                    "grant_user_loop": dict(_require_mapping(
                        product_entry_shell,
                        "grant_user_loop",
                        context="product_frontdesk.product_entry_shell",
                    )),
                    "direct_entry_builder": dict(_require_mapping(
                        shared_handoff,
                        "direct_entry_builder",
                        context="product_frontdesk.shared_handoff",
                    )),
                    "opl_handoff_builder": dict(_require_mapping(
                        shared_handoff,
                        "opl_handoff_builder",
                        context="product_frontdesk.shared_handoff",
                    )),
                },
                "summary": {
                    "frontdesk_command": _require_nonempty_string_from_mapping(
                        _require_mapping(manifest, "frontdesk_surface", context="product_frontdesk.product_entry_manifest"),
                        "command",
                        context="product_frontdesk.frontdesk_surface",
                    ),
                    "recommended_command": _require_nonempty_string_from_mapping(
                        manifest,
                        "recommended_command",
                        context="product_frontdesk.product_entry_manifest",
                    ),
                    "operator_loop_command": _require_nonempty_string_from_mapping(
                        _require_mapping(manifest, "operator_loop_surface", context="product_frontdesk.product_entry_manifest"),
                        "command",
                        context="product_frontdesk.operator_loop_surface",
                    ),
                },
                "notes": [
                    "This frontdesk surface is a controller-owned direct grant front door over the landed product-entry shell.",
                    "It does not claim that mature Web UI or hosted runtime is already landed.",
                ],
            },
        }

    def _load_projection_context(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        route_report = self._domain_entry.dispatch(
            {
                "command": "stage-route-report",
                "input_path": str(resolved_input_path),
            }
        )
        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
        )
        lifecycle_stage = _require_nonempty_string_from_mapping(
            route_report,
            "lifecycle_stage",
            context="stage-route-report",
        )
        critique_summary = None
        if lifecycle_stage in REVIEW_CONTEXT_STAGES:
            critique_summary = self._domain_entry.dispatch(
                {
                    "command": "critique-summary",
                    "input_path": str(resolved_input_path),
                }
            )
        return {
            "resolved_input_path": resolved_input_path,
            "route_report": route_report,
            "workspace_summary": workspace_summary,
            "critique_summary": critique_summary,
        }


def _read_funding_call_from_summary(summary: Mapping[str, Any]) -> str:
    intake_snapshot = _require_mapping(summary, "intake_snapshot", context="summarize-workspace")
    return _require_nonempty_string_from_mapping(
        intake_snapshot,
        "funding_program",
        context="summarize-workspace.intake_snapshot",
    )


def _require_entry_mode(entry_mode: str) -> str:
    resolved_entry_mode = _require_nonempty_string(entry_mode, field_name="entry_mode")
    if resolved_entry_mode not in SUPPORTED_ENTRY_MODES:
        raise WorkspaceStateError(
            f"entry_mode 不支持: {resolved_entry_mode}。只允许 {', '.join(SUPPORTED_ENTRY_MODES)}。"
        )
    return resolved_entry_mode


def _require_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> Mapping[str, Any]:
    value = payload.get(field_name)
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field_name}")
    return value


def _require_nonempty_string_from_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> str:
    value = payload.get(field_name)
    return _require_nonempty_string(value, field_name=field_name, context=context)


def _require_nonempty_string(
    value: Any,
    *,
    field_name: str,
    context: str = "product entry",
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field_name}")
    return value.strip()


def _require_optional_string(value: Any, *, field_name: str) -> str | None:
    if value is None:
        return None
    return _require_nonempty_string(value, field_name=field_name)


def _optional_mapping(payload: Mapping[str, Any], field_name: str) -> Mapping[str, Any] | None:
    value = payload.get(field_name)
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"product entry 缺少合法字段: {field_name}")
    return value


def _optional_string_from_mapping(payload: Mapping[str, Any] | None, field_name: str) -> str | None:
    if not isinstance(payload, Mapping):
        return None
    value = payload.get(field_name)
    if value is None:
        return None
    return _require_nonempty_string(value, field_name=field_name)


def _read_nonempty_string_list(value: Any, *, context: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context} 缺少合法字段: workspace_alerts")
    return [item for item in value if isinstance(item, str) and item.strip()]


def _route_status_from_route_id(route_id: str) -> str:
    resolved_route_id = _require_nonempty_string(route_id, field_name="route_id")
    if resolved_route_id in LANDED_ROUTE_IDS:
        return "landed"
    return "pending"


def _build_family_orchestration_companion(
    *,
    current_route_id: str,
    recommended_route_id: str,
    recommended_route_status: str,
    needs_author_decision: bool,
    review_surface_ref: str,
    event_envelope_surface_ref: str,
    checkpoint_lineage_surface_ref: str,
    resume_surface_kind: str,
) -> dict[str, Any]:
    resolved_current_route_id = _require_nonempty_string(current_route_id, field_name="current_route_id")
    resolved_recommended_route_id = _require_nonempty_string(
        recommended_route_id,
        field_name="recommended_route_id",
    )
    resolved_review_surface_ref = _require_nonempty_string(
        review_surface_ref,
        field_name="review_surface_ref",
    )
    resolved_event_envelope_surface_ref = _require_nonempty_string(
        event_envelope_surface_ref,
        field_name="event_envelope_surface_ref",
    )
    resolved_checkpoint_lineage_surface_ref = _require_nonempty_string(
        checkpoint_lineage_surface_ref,
        field_name="checkpoint_lineage_surface_ref",
    )
    resolved_resume_surface_kind = _require_nonempty_string(
        resume_surface_kind,
        field_name="resume_surface_kind",
    )
    route_status = _require_nonempty_string(
        recommended_route_status,
        field_name="recommended_route_status",
    )
    if route_status not in {"landed", "pending"}:
        raise WorkspaceStateError("family_orchestration.recommended_route_status 只允许 landed 或 pending。")

    gate_status = "requested" if needs_author_decision or route_status == "pending" else "approved"
    gate_id = f"mag_route_gate_{resolved_recommended_route_id}"
    return {
        "action_graph_ref": {
            "ref_kind": "json_pointer",
            "ref": "/family_orchestration/action_graph",
            "label": "mag family action graph",
        },
        "action_graph": _build_family_action_graph(
            current_route_id=resolved_current_route_id,
            recommended_route_id=resolved_recommended_route_id,
            gate_id=gate_id,
            gate_status=gate_status,
        ),
        "human_gates": [
            {
                "gate_id": gate_id,
                "title": f"确认 {resolved_recommended_route_id} route 执行决策",
                "status": gate_status,
                "review_surface": {
                    "ref_kind": "json_pointer",
                    "ref": resolved_review_surface_ref,
                    "label": "route review surface",
                },
            }
        ],
        "resume_contract": {
            "surface_kind": resolved_resume_surface_kind,
            "session_locator_field": "grant_run_id",
            "checkpoint_locator_field": "lifecycle_stage",
        },
        "event_envelope_surface": {
            "ref_kind": "json_pointer",
            "ref": resolved_event_envelope_surface_ref,
            "label": "family event envelope surface",
        },
        "checkpoint_lineage_surface": {
            "ref_kind": "json_pointer",
            "ref": resolved_checkpoint_lineage_surface_ref,
            "label": "family checkpoint lineage surface",
        },
    }


def _build_family_action_graph(
    *,
    current_route_id: str,
    recommended_route_id: str,
    gate_id: str,
    gate_status: str,
) -> dict[str, Any]:
    current_node_id = f"route:{current_route_id}"
    recommended_node_id = f"route:{recommended_route_id}"
    edge_on = "decision" if gate_status == "requested" else "success"
    return {
        "version": "family-action-graph.v1",
        "graph_id": f"mag_{current_route_id}_to_{recommended_route_id}_graph",
        "target_domain_id": TARGET_DOMAIN_ID,
        "graph_kind": "grant_route_orchestration",
        "graph_version": "2026-04-13",
        "nodes": [
            {
                "node_id": current_node_id,
                "node_kind": _route_to_action_node_kind(current_route_id),
                "title": f"Current route: {current_route_id}",
                "produces_checkpoint": True,
            },
            {
                "node_id": recommended_node_id,
                "node_kind": _route_to_action_node_kind(recommended_route_id),
                "title": f"Recommended route: {recommended_route_id}",
                "produces_checkpoint": True,
            },
        ],
        "edges": [
            {
                "from": current_node_id,
                "to": recommended_node_id,
                "on": edge_on,
            },
        ],
        "entry_nodes": [current_node_id],
        "exit_nodes": [recommended_node_id],
        "human_gates": [
            {
                "gate_id": gate_id,
                "trigger_nodes": [recommended_node_id],
                "blocking": gate_status == "requested",
            }
        ],
        "checkpoint_policy": {
            "mode": "explicit_nodes",
            "checkpoint_nodes": [current_node_id, recommended_node_id],
        },
    }


def _route_to_action_node_kind(route_id: str) -> str:
    if route_id in {"critique", "revision", "frozen"}:
        return "review"
    if route_id in {"artifact_bundle", "final_package", "hosted_contract_bundle"}:
        return "publish"
    return "authoring"


def _write_product_entry_output(output_path: Path, product_entry: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(product_entry, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 product entry 输出失败: {output_path}") from exc


def _read_blocking_issues(critique_summary: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(critique_summary, Mapping):
        return []
    blocking_issues = critique_summary.get("blocking_issues")
    if not isinstance(blocking_issues, list):
        return []
    return [item for item in blocking_issues if isinstance(item, str) and item.strip()]


def _read_next_system_action(next_step: Mapping[str, Any]) -> str:
    actions = next_step.get("actions")
    if isinstance(actions, list):
        for item in actions:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return _require_nonempty_string_from_mapping(
        next_step,
        "reason",
        context="stage-route-report.route.next_step",
    )


def _build_current_stage_summary(
    *,
    lifecycle_stage: str,
    checkpoint_status: str,
    next_step: Mapping[str, Any],
) -> str:
    if lifecycle_stage == "frozen" and checkpoint_status == "submission_frozen":
        reason = "送审前冻结 gate 已闭合，可保持当前阶段继续推进。"
    else:
        reason = _require_nonempty_string_from_mapping(
            next_step,
            "reason",
            context="stage-route-report.route.next_step",
        )
    return f"当前 grant 已进入 {lifecycle_stage} 阶段；{reason}"


def _build_author_decision_summary(next_step: Mapping[str, Any]) -> str | None:
    if not bool(next_step.get("requires_human_confirmation")):
        return None
    return _require_nonempty_string_from_mapping(
        next_step,
        "reason",
        context="stage-route-report.route.next_step",
    )


def _build_focus_payload(
    *,
    workspace_summary: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> dict[str, Any]:
    intake_snapshot = _require_mapping(
        workspace_summary,
        "intake_snapshot",
        context="summarize-workspace",
    )
    selected_direction = _optional_mapping(workspace_summary, "selected_direction")
    selected_question = _optional_mapping(workspace_summary, "selected_question")
    active_draft = _optional_mapping(workspace_summary, "active_draft")
    active_critique = _optional_mapping(workspace_summary, "active_critique")
    critique_verdict = _optional_string_from_mapping(active_critique, "verdict")
    if isinstance(critique_summary, Mapping):
        critique_verdict = _optional_string_from_mapping(critique_summary, "verdict") or critique_verdict
    return {
        "applicant_name": _require_nonempty_string_from_mapping(
            intake_snapshot,
            "applicant_name",
            context="summarize-workspace.intake_snapshot",
        ),
        "funding_program": _require_nonempty_string_from_mapping(
            intake_snapshot,
            "funding_program",
            context="summarize-workspace.intake_snapshot",
        ),
        "selected_direction_title": _optional_string_from_mapping(selected_direction, "title"),
        "selected_question": _optional_string_from_mapping(selected_question, "core_question"),
        "active_draft_title": _optional_string_from_mapping(active_draft, "project_title"),
        "critique_verdict": critique_verdict,
    }


def _build_workspace_overview(
    *,
    workspace_summary: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> dict[str, Any]:
    focus = _build_focus_payload(
        workspace_summary=workspace_summary,
        critique_summary=critique_summary,
    )
    return {
        "applicant_name": focus["applicant_name"],
        "funding_program": focus["funding_program"],
        "lifecycle_stage": _require_nonempty_string_from_mapping(
            progress_projection,
            "current_stage",
            context="grant-progress.progress_projection",
        ),
        "checkpoint_status": _require_nonempty_string_from_mapping(
            progress_projection,
            "checkpoint_status",
            context="grant-progress.progress_projection",
        ),
        "selected_direction_title": focus["selected_direction_title"],
        "selected_question": focus["selected_question"],
        "active_draft_title": focus["active_draft_title"],
        "critique_verdict": focus["critique_verdict"],
    }


def _build_workspace_status(*, blockers: list[str], needs_author_decision: bool) -> str:
    if blockers or needs_author_decision:
        return "attention_required"
    return "on_track"


def _require_matching_top_level_identity(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    *,
    context: str,
) -> None:
    for field_name in ("grant_run_id", "workspace_id", "draft_id", "lifecycle_stage", "input_path"):
        if left.get(field_name) != right.get(field_name):
            raise WorkspaceStateError(f"{context} 与当前 direct entry identity 不一致: {field_name}")


def _assert_entry_mode(
    payload: Mapping[str, Any],
    *,
    expected_entry_mode: str,
    context: str,
) -> None:
    resolved_entry_mode = _require_nonempty_string_from_mapping(
        payload,
        "entry_mode",
        context=context,
    )
    if resolved_entry_mode != expected_entry_mode:
        raise WorkspaceStateError(f"{context}.entry_mode 必须为 {expected_entry_mode}。")


def _validate_grant_direct_entry_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_contract_schema(
        payload,
        schema_file=GRANT_DIRECT_ENTRY_SCHEMA_FILE,
        context="grant_direct_entry",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    grant_direct_entry = _require_mapping(
        payload,
        "grant_direct_entry",
        context="grant_direct_entry",
    )
    direct_entry = _require_mapping(
        grant_direct_entry,
        "direct_entry",
        context="grant_direct_entry.direct_entry",
    )
    opl_handoff_entry = _require_mapping(
        grant_direct_entry,
        "opl_handoff_entry",
        context="grant_direct_entry.opl_handoff_entry",
    )
    if (
        _require_nonempty_string_from_mapping(
            direct_entry,
            "entry_mode",
            context="grant_direct_entry.direct_entry",
        )
        != "direct"
    ):
        raise WorkspaceStateError(
            "grant_direct_entry.direct_entry.entry_mode 必须为 direct。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            opl_handoff_entry,
            "entry_mode",
            context="grant_direct_entry.opl_handoff_entry",
        )
        != "opl-handoff"
    ):
        raise WorkspaceStateError(
            "grant_direct_entry.opl_handoff_entry.entry_mode 必须为 opl-handoff。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    direct_task_intent = _require_nonempty_string_from_mapping(
        direct_entry,
        "task_intent",
        context="grant_direct_entry.direct_entry",
    )
    opl_handoff_task_intent = _require_nonempty_string_from_mapping(
        opl_handoff_entry,
        "task_intent",
        context="grant_direct_entry.opl_handoff_entry",
    )
    task_intent = _require_nonempty_string_from_mapping(
        grant_direct_entry,
        "task_intent",
        context="grant_direct_entry",
    )
    if direct_task_intent != task_intent:
        raise WorkspaceStateError(
            "grant_direct_entry.direct_entry.task_intent 与顶层 direct entry contract 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_handoff_task_intent != task_intent:
        raise WorkspaceStateError(
            "grant_direct_entry.opl_handoff_entry.task_intent 与顶层 direct entry contract 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    current_stage_route = _require_mapping(
        grant_direct_entry,
        "current_stage_route",
        context="grant_direct_entry",
    )
    recommended_executor_route = _require_mapping(
        grant_direct_entry,
        "recommended_executor_route",
        context="grant_direct_entry",
    )
    direct_executor_routing_contract = _require_mapping(
        direct_entry,
        "executor_routing_contract",
        context="grant_direct_entry.direct_entry",
    )
    opl_executor_routing_contract = _require_mapping(
        opl_handoff_entry,
        "executor_routing_contract",
        context="grant_direct_entry.opl_handoff_entry",
    )
    if direct_executor_routing_contract.get("current_stage_route") != current_stage_route:
        raise WorkspaceStateError(
            "grant_direct_entry.current_stage_route 与 direct entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if direct_executor_routing_contract.get("recommended_executor_route") != recommended_executor_route:
        raise WorkspaceStateError(
            "grant_direct_entry.recommended_executor_route 与 direct entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_executor_routing_contract.get("current_stage_route") != current_stage_route:
        raise WorkspaceStateError(
            "grant_direct_entry.current_stage_route 与 opl_handoff entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_executor_routing_contract.get("recommended_executor_route") != recommended_executor_route:
        raise WorkspaceStateError(
            "grant_direct_entry.recommended_executor_route 与 opl_handoff entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _build_mainline_snapshot(mainline_status: Mapping[str, Any]) -> dict[str, Any]:
    current_runtime_owner = _require_mapping(
        mainline_status,
        "current_runtime_owner",
        context="mainline_status",
    )
    phase_ladder = mainline_status.get("phase_ladder")
    if not isinstance(phase_ladder, list):
        raise WorkspaceStateError("mainline_status.phase_ladder 必须为 list。")
    return {
        "current_owner_line": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "current_owner_line",
            context="mainline_status.current_runtime_owner",
        ),
        "active_phase": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_phase",
            context="mainline_status.current_runtime_owner",
        ),
        "active_tranche": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_tranche",
            context="mainline_status.current_runtime_owner",
        ),
        "phase_map": [
            {
                "phase_id": _require_nonempty_string_from_mapping(item, "phase_id", context="mainline_status.phase_ladder"),
                "phase_name": _require_nonempty_string_from_mapping(item, "phase_name", context="mainline_status.phase_ladder"),
                "status": _require_nonempty_string_from_mapping(item, "status", context="mainline_status.phase_ladder"),
            }
            for item in phase_ladder
            if isinstance(item, Mapping)
        ],
        "next_focus": _read_nonempty_string_list(
            mainline_status.get("next_focus"),
            context="mainline_status.next_focus",
        ),
        "remaining_gaps": _read_nonempty_string_list(
            mainline_status.get("remaining_gaps"),
            context="mainline_status.remaining_gaps",
        ),
    }


def _build_next_action_payload(
    *,
    recommended_executor_route: Mapping[str, Any],
    input_path: Path,
) -> dict[str, Any]:
    route_id = _require_nonempty_string_from_mapping(
        recommended_executor_route,
        "route_id",
        context="grant_user_loop.recommended_executor_route",
    )
    route_status = _require_nonempty_string_from_mapping(
        recommended_executor_route,
        "route_status",
        context="grant_user_loop.recommended_executor_route",
    )
    if route_status == "landed":
        return {
            "action_kind": "execute_landed_route",
            "route_id": route_id,
            "route_status": route_status,
            "summary": f"当前推荐 route {route_id} 已 landed，可直接调用现有 author-side executor surface。",
            "command": _build_route_execution_command(route_id=route_id, input_path=input_path),
            "handoff_surfaces": None,
        }

    handoff_requirements = _optional_mapping(recommended_executor_route, "handoff_requirements")
    handoff_surfaces = _build_handoff_surface_commands(
        handoff_requirements=handoff_requirements,
        input_path=input_path,
    )
    return {
        "action_kind": "prepare_pending_handoff",
        "route_id": route_id,
        "route_status": route_status,
        "summary": f"当前推荐 route {route_id} 仍未 landed，应先按 handoff contract 准备所需 domain surfaces。",
        "command": None,
        "handoff_surfaces": handoff_surfaces,
    }


def _build_handoff_surface_commands(
    *,
    handoff_requirements: Mapping[str, Any] | None,
    input_path: Path,
) -> dict[str, str] | None:
    if not isinstance(handoff_requirements, Mapping):
        return None
    required_domain_surfaces = handoff_requirements.get("required_domain_surfaces")
    if not isinstance(required_domain_surfaces, list):
        return None
    commands: dict[str, str] = {}
    for item in required_domain_surfaces:
        if not isinstance(item, Mapping):
            continue
        command = _optional_string_from_mapping(item, "command")
        if command is None:
            continue
        commands[_command_name_to_catalog_key(command)] = _build_domain_surface_command(
            command=command,
            input_path=input_path,
        )
    return commands or None


def _command_name_to_catalog_key(command: str) -> str:
    return command.replace("-", "_")


def _build_domain_surface_command(*, command: str, input_path: Path) -> str:
    resolved_input_path = input_path.expanduser().resolve()
    return f"uv run python -m med_autogrant {command} --input {resolved_input_path} --format json"


def _build_route_execution_command(*, route_id: str, input_path: Path) -> str:
    resolved_input_path = input_path.expanduser().resolve()
    if route_id == "critique":
        return (
            "uv run python -m med_autogrant execute-critique-pass "
            f"--input {resolved_input_path} --output <critique-output-path> --format json"
        )
    if route_id == "revision":
        return (
            "uv run python -m med_autogrant execute-revision-pass "
            f"--input {resolved_input_path} --output <revision-output-path> --format json"
        )
    if route_id == "artifact_bundle":
        return (
            "uv run python -m med_autogrant build-artifact-bundle "
            f"--input {resolved_input_path} --output <artifact-bundle-output-path> --format json"
        )
    if route_id == "final_package":
        return (
            "uv run python -m med_autogrant build-final-package "
            f"--input {resolved_input_path} --artifact-bundle <artifact-bundle-output-path> "
            "--output <final-package-output-path> --format json"
        )
    if route_id == "hosted_contract_bundle":
        return (
            "uv run python -m med_autogrant build-hosted-contract-bundle "
            "--final-package <final-package-output-path> "
            "--output <hosted-contract-bundle-output-path> --format json"
        )
    raise WorkspaceStateError(f"grant_user_loop 不支持 landed route command: {route_id}")


def _build_grant_user_loop_commands(
    *,
    input_path: Path,
    task_intent: str,
    run_recommended_route: Any,
) -> dict[str, Any]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "mainline_status": "uv run python -m med_autogrant mainline-status --format json",
        "phase_status_current": "uv run python -m med_autogrant mainline-phase --phase current --format json",
        "phase_status_next": "uv run python -m med_autogrant mainline-phase --phase next --format json",
        "open_grant_cockpit": (
            f"uv run python -m med_autogrant grant-cockpit --input {resolved_input_path} --format json"
        ),
        "open_grant_direct_entry": (
            "uv run python -m med_autogrant grant-direct-entry "
            f"--input {resolved_input_path} --task-intent {task_intent} --format json"
        ),
        "run_recommended_route": (
            _require_nonempty_string(run_recommended_route, field_name="run_recommended_route")
            if run_recommended_route is not None
            else None
        ),
        "build_direct_entry": (
            "uv run python -m med_autogrant build-product-entry "
            f"--input {resolved_input_path} --entry-mode direct "
            f"--task-intent {task_intent} --format json"
        ),
        "build_opl_handoff": (
            "uv run python -m med_autogrant build-product-entry "
            f"--input {resolved_input_path} --entry-mode opl-handoff "
            f"--task-intent {task_intent} --format json"
        ),
    }


def _validate_grant_user_loop_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_contract_schema(
        payload,
        schema_file=GRANT_USER_LOOP_SCHEMA_FILE,
        context="grant_user_loop",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    grant_user_loop = _require_mapping(
        payload,
        "grant_user_loop",
        context="grant_user_loop",
    )
    grant_direct_entry = _require_mapping(
        grant_user_loop,
        "grant_direct_entry",
        context="grant_user_loop.grant_direct_entry",
    )
    if (
        _require_nonempty_string_from_mapping(
            grant_user_loop,
            "task_intent",
            context="grant_user_loop",
        )
        != _require_nonempty_string_from_mapping(
            grant_direct_entry,
            "task_intent",
            context="grant_user_loop.grant_direct_entry",
        )
    ):
        raise WorkspaceStateError(
            "grant_user_loop.task_intent 与 grant_direct_entry.task_intent 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    next_action = _require_mapping(
        grant_user_loop,
        "next_action",
        context="grant_user_loop.next_action",
    )
    recommended_executor_route = _require_mapping(
        grant_direct_entry,
        "recommended_executor_route",
        context="grant_user_loop.grant_direct_entry",
    )
    if next_action.get("route_id") != recommended_executor_route.get("route_id"):
        raise WorkspaceStateError(
            "grant_user_loop.next_action.route_id 与 grant_direct_entry.recommended_executor_route.route_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if next_action.get("route_status") != recommended_executor_route.get("route_status"):
        raise WorkspaceStateError(
            "grant_user_loop.next_action.route_status 与 grant_direct_entry.recommended_executor_route.route_status 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    action_kind = _require_nonempty_string_from_mapping(
        next_action,
        "action_kind",
        context="grant_user_loop.next_action",
    )
    command = next_action.get("command")
    handoff_surfaces = next_action.get("handoff_surfaces")
    if action_kind == "execute_landed_route":
        if not isinstance(command, str) or not command.strip():
            raise WorkspaceStateError(
                "grant_user_loop.next_action.command 必须在 landed route 时非空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
        if handoff_surfaces is not None:
            raise WorkspaceStateError(
                "grant_user_loop.next_action.handoff_surfaces 必须在 landed route 时为空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
    if action_kind == "prepare_pending_handoff":
        if command is not None:
            raise WorkspaceStateError(
                "grant_user_loop.next_action.command 必须在 pending handoff 时为空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
        if not isinstance(handoff_surfaces, Mapping) or not handoff_surfaces:
            raise WorkspaceStateError(
                "grant_user_loop.next_action.handoff_surfaces 必须在 pending handoff 时非空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )


def _build_product_command_catalog(input_path: Path) -> dict[str, str]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "grant_progress": (
            f"uv run python -m med_autogrant grant-progress --input {resolved_input_path} --format json"
        ),
        "summarize_workspace": (
            f"uv run python -m med_autogrant summarize-workspace --input {resolved_input_path} --format json"
        ),
        "stage_route_report": (
            f"uv run python -m med_autogrant stage-route-report --input {resolved_input_path} --format json"
        ),
        "critique_summary": (
            f"uv run python -m med_autogrant critique-summary --input {resolved_input_path} --format json"
        ),
        "build_direct_entry": (
            "uv run python -m med_autogrant build-product-entry "
            f"--input {resolved_input_path} --entry-mode direct "
            "--task-intent <describe-task-intent> --format json"
        ),
        "build_opl_handoff": (
            "uv run python -m med_autogrant build-product-entry "
            f"--input {resolved_input_path} --entry-mode opl-handoff "
            "--task-intent <describe-task-intent> --format json"
        ),
    }
