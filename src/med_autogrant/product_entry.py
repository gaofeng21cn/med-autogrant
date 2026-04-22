from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from med_autogrant.control_plane import read_program_id, resolve_runtime_state_root
from med_autogrant.domain_entry_contract import (
    build_domain_entry_contract,
    build_gateway_interaction_contract,
    build_shared_handoff,
)
from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.hermes_runtime import (
    _build_author_side_route_contract,
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_DIRECT_ENTRY_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    GRANT_USER_LOOP_SCHEMA_FILE,
    PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    PRODUCT_FRONTDESK_SCHEMA_FILE,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.public_cli import public_cli_command, public_command_label
from med_autogrant.workspace import (
    WorkspaceFileError,
    WorkspaceStateError,
    load_workspace_document,
    validate_workspace_document,
)

from opl_harness_shared.managed_runtime import build_managed_runtime_contract as _build_shared_managed_runtime_contract
from opl_harness_shared.family_orchestration import (
    buildFamilyIntakeEvidenceCompanion as _build_shared_family_intake_evidence_companion,
    build_family_product_entry_orchestration as _build_shared_family_product_entry_orchestration,
)
from opl_harness_shared.automation_companions import (
    build_automation_catalog as _build_shared_automation_catalog,
    build_automation_descriptor as _build_shared_automation_descriptor,
)
from opl_harness_shared.product_entry_companions import (
    build_family_product_frontdesk_from_manifest as _build_shared_family_product_frontdesk_from_manifest,
    build_family_product_entry_manifest as _build_shared_family_product_entry_manifest,
    build_operator_loop_action_catalog as _build_shared_operator_loop_action_catalog,
    build_product_entry_start as _build_shared_product_entry_start,
    build_product_entry_overview as _build_shared_product_entry_overview,
    build_product_entry_quickstart as _build_shared_product_entry_quickstart,
    build_product_entry_readiness as _build_shared_product_entry_readiness,
    build_product_entry_resume_surface as _build_shared_product_entry_resume_surface,
    build_product_entry_shell_catalog as _build_shared_product_entry_shell_catalog,
    build_product_entry_shell_linked_surface as _build_shared_product_entry_shell_linked_surface,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
    validate_family_product_frontdesk as _validate_shared_family_product_frontdesk,
    validate_family_product_entry_manifest as _validate_shared_family_product_entry_manifest,
)
from opl_harness_shared.product_entry_program_companions import (
    build_detailed_readiness as _build_shared_detailed_readiness,
    build_product_entry_preflight as _build_shared_product_entry_preflight,
    build_workflow_coverage_item as _build_shared_workflow_coverage_item,
)
from opl_harness_shared.runtime_task_companions import (
    build_runtime_inventory as _build_shared_runtime_inventory,
    build_task_lifecycle as _build_shared_task_lifecycle,
)
from opl_harness_shared.status_narration import (
    PROGRESS_ANSWER_CHECKLIST,
    build_status_narration_contract,
)
from opl_harness_shared.skill_catalog import (
    build_skill_catalog as _build_shared_skill_catalog,
    build_skill_descriptor as _build_shared_skill_descriptor,
)


PRODUCT_ENTRY_VERSION = 1
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
PRODUCT_ENTRY_MANIFEST_KIND = "med_auto_grant_product_entry_manifest"
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


def _build_managed_runtime_contract() -> dict[str, Any]:
    return _build_shared_managed_runtime_contract(
        domain_owner=TARGET_DOMAIN_ID,
        executor_owner="med-autogrant",
        supervision_status_surface=GRANT_PROGRESS_PROJECTION_KIND,
        attention_queue_surface=GRANT_USER_LOOP_KIND,
        recovery_contract_surface=GRANT_USER_LOOP_KIND,
    )


def _build_product_entry_start(
    *,
    product_frontdesk_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
) -> dict[str, Any]:
    return _build_shared_product_entry_start(
        summary=(
            "先进入 direct grant frontdesk；需要继续当前写作主线时恢复 grant user loop，"
            "需要把用户意图显式装配成入口合同时再构建 direct entry。"
        ),
        recommended_mode_id="open_frontdesk",
        modes=[
            {
                "mode_id": "open_frontdesk",
                "title": "Open grant frontdesk",
                "command": product_frontdesk_command,
                "surface_kind": PRODUCT_FRONTDESK_KIND,
                "summary": "打开当前 direct grant frontdoor。",
                "requires": [],
            },
            {
                "mode_id": "continue_grant_loop",
                "title": "Continue current grant loop",
                "command": grant_user_loop_command,
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": _require_nonempty_string_from_mapping(
                    operator_loop_actions["open_loop"],
                    "summary",
                    context="operator_loop_actions.open_loop",
                ),
                "requires": ["task_intent"],
            },
            {
                "mode_id": "build_direct_entry",
                "title": "Build direct entry",
                "command": grant_direct_entry_command,
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                "summary": _require_nonempty_string_from_mapping(
                    operator_loop_actions["build_direct_entry"],
                    "summary",
                    context="operator_loop_actions.build_direct_entry",
                ),
                "requires": list(
                    _require_mapping(
                        operator_loop_actions,
                        "build_direct_entry",
                        context="operator_loop_actions",
                    ).get("requires")
                    or []
                ),
            },
        ],
        resume_surface=dict(
            _require_mapping(
                family_orchestration,
                "resume_contract",
                context="family_orchestration",
            )
        ),
        human_gate_ids=_collect_family_human_gate_ids(family_orchestration),
    )


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
                "start_entry": "runtime-run",
                "resume_entry": "runtime-resume",
                "runtime_substrate_contract": _build_runtime_substrate_contract(
                    current_program_contract=current_program_contract,
                ),
                "runtime_state_contract": _build_runtime_state_contract(),
            },
            "return_surface_contract": {
                "entry_adapter": "MedAutoGrantDomainEntry",
                "default_formal_entry": "CLI",
                "supported_entry_modes": list(SUPPORTED_ENTRY_MODES),
                "domain_entry_contract": build_domain_entry_contract(),
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

    def build_product_entry_manifest(
        self,
        *,
        input_path: str | Path,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        del funding_call
        resolved_input_path = Path(input_path).expanduser().resolve()
        preflight_payload = self.build_product_entry_preflight(input_path=resolved_input_path)
        product_entry_preflight = dict(preflight_payload["product_entry_preflight"])
        progress_payload = self.read_grant_progress(input_path=resolved_input_path)
        progress_projection = _require_mapping(
            progress_payload,
            "progress_projection",
            context="grant-progress",
        )
        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
        )
        mainline_payload = read_mainline_status()
        mainline_snapshot = _build_mainline_snapshot(mainline_payload)
        current_line = _require_mapping(
            mainline_payload,
            "current_line",
            context="mainline_status",
        )
        current_focus = _require_mapping(
            mainline_payload,
            "current_focus",
            context="mainline_status",
        )
        maintainer_references = _require_mapping(
            mainline_payload,
            "maintainer_references",
            context="mainline_status",
        )
        current_runtime_owner = _require_mapping(
            maintainer_references,
            "runtime_owner",
            context="mainline_status.maintainer_references",
        )
        current_phase = _require_mapping(
            maintainer_references,
            "current_record_detail",
            context="mainline_status",
        )
        task_intent_placeholder = "<describe-task-intent>"
        command_catalog = _build_product_command_catalog(resolved_input_path)
        grant_user_loop_command = public_cli_command(
            "grant-user-loop",
            "--input",
            str(resolved_input_path),
            "--task-intent",
            task_intent_placeholder,
            "--format",
            "json",
        )
        product_frontdesk_command = public_cli_command(
            "product-frontdesk", "--input", str(resolved_input_path), "--format", "json"
        )
        grant_cockpit_command = public_cli_command(
            "grant-cockpit", "--input", str(resolved_input_path), "--format", "json"
        )
        grant_direct_entry_command = public_cli_command(
            "grant-direct-entry",
            "--input",
            str(resolved_input_path),
            "--task-intent",
            task_intent_placeholder,
            "--format",
            "json",
        )
        operator_loop_actions = _build_shared_operator_loop_action_catalog({
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
            "build_submission_ready_package": {
                "command": command_catalog["build_submission_ready_package"],
                "surface_kind": "submission_ready_package",
                "summary": "检查 submission-ready gate，并在通过时一次性导出本地交付目录。",
                "requires": ["output_dir"],
            },
        })
        session_continuity = _build_session_continuity_surface(
            grant_run_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "grant_run_id",
                context="grant-progress",
            ),
            workspace_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "workspace_id",
                context="grant-progress",
            ),
            lifecycle_stage=_require_nonempty_string_from_mapping(
                progress_payload,
                "lifecycle_stage",
                context="grant-progress",
            ),
            input_path=str(resolved_input_path),
        )
        manifest_progress_projection = _build_progress_projection_surface(
            projection=dict(progress_projection),
            grant_run_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "grant_run_id",
                context="grant-progress",
            ),
            workspace_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "workspace_id",
                context="grant-progress",
            ),
            lifecycle_stage=_require_nonempty_string_from_mapping(
                progress_payload,
                "lifecycle_stage",
                context="grant-progress",
            ),
            input_path=str(resolved_input_path),
            inspect_progress_command=command_catalog["grant_progress"],
            summarize_workspace_command=public_cli_command(
                "summarize-workspace", "--input", str(resolved_input_path), "--format", "json"
            ),
            stage_route_report_command=public_cli_command(
                "stage-route-report", "--input", str(resolved_input_path), "--format", "json"
            ),
        )
        artifact_inventory = _build_artifact_inventory_surface(
            workspace_summary=workspace_summary,
            grant_run_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "grant_run_id",
                context="grant-progress",
            ),
            workspace_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "workspace_id",
                context="grant-progress",
            ),
            lifecycle_stage=_require_nonempty_string_from_mapping(
                progress_payload,
                "lifecycle_stage",
                context="grant-progress",
            ),
            input_path=str(resolved_input_path),
        )
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
            intake_evidence_companion=_optional_mapping(
                _require_mapping(progress_payload, "family_orchestration", context="grant-progress"),
                "intake_evidence_companion",
            ),
            project_profile_companion=_optional_mapping(
                _require_mapping(progress_payload, "family_orchestration", context="grant-progress"),
                "project_profile_companion",
            ),
            review_surface_ref="/product_entry_manifest/operator_loop_surface",
            event_envelope_surface_ref="/product_entry_manifest/recommended_command",
            checkpoint_lineage_surface_ref="/product_entry_manifest/repo_mainline/active_phase",
            resume_surface_kind=GRANT_USER_LOOP_KIND,
        )
        route_report = self._domain_entry.dispatch(
            {
                "command": "stage-route-report",
                "input_path": str(resolved_input_path),
            }
        )
        verification_checkpoint = _require_mapping(
            route_report,
            "verification_checkpoint",
            context="stage-route-report",
        )
        verification_identity = _require_mapping(
            verification_checkpoint,
            "identity",
            context="stage-route-report.verification_checkpoint",
        )
        checkpoint_status = _require_nonempty_string_from_mapping(
            verification_checkpoint,
            "checkpoint_status",
            context="stage-route-report.verification_checkpoint",
        )
        route_snapshot = _require_mapping(
            route_report,
            "route",
            context="stage-route-report",
        )
        route_next_step = _require_mapping(
            route_snapshot,
            "next_step",
            context="stage-route-report.route",
        )
        continuation_route_id = _require_nonempty_string_from_mapping(
            route_next_step,
            "recommended_stage",
            context="stage-route-report.route.next_step",
        )
        continuation_route_contract = _build_author_side_route_contract(
            continuation_route_id,
            source_stage=_require_nonempty_string_from_mapping(
                route_report,
                "lifecycle_stage",
                context="stage-route-report",
            ),
        )
        continuation_next_action = _build_next_action_payload(
            recommended_executor_route=continuation_route_contract,
            input_path=resolved_input_path,
            grant_run_id=_require_nonempty_string_from_mapping(
                route_report,
                "grant_run_id",
                context="stage-route-report",
            ),
            workspace_id=_require_nonempty_string_from_mapping(
                route_report,
                "workspace_id",
                context="stage-route-report",
            ),
            draft_id=_optional_string_from_mapping(verification_identity, "draft_id"),
        )
        continuation_route_status = _require_nonempty_string_from_mapping(
            continuation_next_action,
            "route_status",
            context="product_entry_manifest.continuation_next_action",
        )
        continuation_action_kind = _require_nonempty_string_from_mapping(
            continuation_next_action,
            "action_kind",
            context="product_entry_manifest.continuation_next_action",
        )
        product_entry_start = _build_product_entry_start(
            product_frontdesk_command=product_frontdesk_command,
            grant_user_loop_command=grant_user_loop_command,
            grant_direct_entry_command=grant_direct_entry_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
        )
        product_entry_quickstart = _build_shared_product_entry_quickstart(
            summary=(
                "先从 direct grant product frontdesk 进入当前 frontdoor，"
                "再回到 grant-user-loop，必要时读取 progress 或 cockpit projection。"
            ),
            recommended_step_id="open_frontdesk",
            steps=[
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
                {
                    "step_id": "build_submission_ready_package",
                    "title": "Build submission-ready package",
                    "command": command_catalog["build_submission_ready_package"],
                    "surface_kind": "submission_ready_package",
                    "summary": operator_loop_actions["build_submission_ready_package"]["summary"],
                    "requires": list(operator_loop_actions["build_submission_ready_package"]["requires"]),
                },
            ],
            resume_contract=dict(family_orchestration["resume_contract"]),
            human_gate_ids=_collect_family_human_gate_ids(family_orchestration),
        )
        product_entry_overview = _build_shared_product_entry_overview(
            summary=_require_nonempty_string_from_mapping(
                current_focus,
                "summary",
                context="mainline_status.current_focus",
            ),
            frontdesk_command=product_frontdesk_command,
            recommended_command=grant_user_loop_command,
            operator_loop_command=grant_user_loop_command,
            progress_surface={
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                "command": command_catalog["grant_progress"],
                "step_id": "inspect_progress",
            },
            resume_surface=_build_shared_product_entry_resume_surface(
                command=grant_user_loop_command,
                resume_contract=family_orchestration["resume_contract"],
            ),
            recommended_step_id=product_entry_quickstart["recommended_step_id"],
            next_focus=list(mainline_snapshot["next_focus"]),
            remaining_gaps_count=len(mainline_snapshot["remaining_gaps"]),
            human_gate_ids=list(product_entry_quickstart["human_gate_ids"]),
        )
        product_entry_overview.update(
            {
                "project_profile_label": _require_nonempty_string_from_mapping(
                    _require_mapping(workspace_summary, "project_profile", context="summarize-workspace"),
                    "profile_label",
                    context="summarize-workspace.project_profile",
                ),
                "template_label": _require_nonempty_string_from_mapping(
                    _require_mapping(workspace_summary, "project_profile", context="summarize-workspace"),
                    "template_label",
                    context="summarize-workspace.project_profile",
                ),
                "critique_policy_id": _require_nonempty_string_from_mapping(
                    _require_mapping(workspace_summary, "project_profile", context="summarize-workspace"),
                    "critique_policy_id",
                    context="summarize-workspace.project_profile",
                ),
            }
        )
        repo_mainline = {
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
                current_focus,
                "summary",
                context="mainline_status.current_focus",
            ),
            "active_phase": _require_nonempty_string_from_mapping(
                current_runtime_owner,
                "active_phase",
                context="mainline_status.maintainer_references.runtime_owner",
            ),
            "active_tranche": _require_nonempty_string_from_mapping(
                current_runtime_owner,
                "active_tranche",
                context="mainline_status.maintainer_references.runtime_owner",
            ),
            "next_focus": list(mainline_snapshot["next_focus"]),
        }
        runtime_summary = {
            "current_owner_line": _require_nonempty_string_from_mapping(
                current_line,
                "current_owner_line",
                context="mainline_status.current_line",
            ),
            "runtime_owner": "upstream_hermes_agent",
        }
        managed_runtime_contract = _build_managed_runtime_contract()
        product_entry_shell = _build_shared_product_entry_shell_catalog({
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
        })
        frontdesk_surface = _build_shared_product_entry_shell_linked_surface(
            shell_key="product_frontdesk",
            shell_surface=product_entry_shell["product_frontdesk"],
            summary=(
                "当前 direct grant product frontdesk 先暴露前台入口、user loop、projection 与 shared handoff。"
            ),
        )
        operator_loop_surface = _build_shared_product_entry_shell_linked_surface(
            shell_key="grant_user_loop",
            shell_surface=product_entry_shell["grant_user_loop"],
            summary=(
                "当前 operator loop 以 grant-user-loop 作为 direct grant user inbox shell，"
                "在同一入口下汇总 progress、route action 与 mainline snapshot。"
            ),
        )
        domain_entry_contract = build_domain_entry_contract()
        gateway_interaction_contract = build_gateway_interaction_contract()
        grant_authoring_readiness = _build_shared_detailed_readiness(
            surface_kind="grant_authoring_readiness",
            verdict="agent_assisted_cli_ready_not_full_autopilot",
            fully_automatic=False,
            usable_now=True,
            good_to_use_now=False,
            user_experience_level="usable_for_agent_assisted_cli_authoring_not_yet_polished_product",
            summary=(
                "当前可以作为 Agent 协同的 CLI/controller 标书写作主线使用；"
                "对满足冻结与材料齐备条件的 workspace，已经能一键导出本地 submission-ready 交付包，"
                "但还不是无需人工材料、无需判断、可直接官网提交的全自动国自然标书产品。"
            ),
            recommended_start_surface=PRODUCT_FRONTDESK_KIND,
            recommended_start_command=product_frontdesk_command,
            recommended_loop_surface=GRANT_USER_LOOP_KIND,
            recommended_loop_command=grant_user_loop_command,
            workflow_coverage=[
                _build_shared_workflow_coverage_item(
                    step_id="accumulation_direction_screening",
                    manual_flow_label="从已有积累中筛选方向",
                    coverage_status="landed_route",
                    current_surface="execute-direction-screening-pass",
                    remaining_gap="需要用户先提供真实课题、论文、前期结果和在研工作材料。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="hotspot_literature_fit",
                    manual_flow_label="筛选可嵌入的热点",
                    coverage_status="partially_supported",
                    current_surface="question_refinement / argument_building",
                    remaining_gap="自动文献检索、热点筛选和引用证据绑定尚未作为 repo-tracked runtime contract 落地。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="clinical_question_refinement",
                    manual_flow_label="锚定具体临床问题",
                    coverage_status="landed_route",
                    current_surface="execute-question-refinement-pass",
                    remaining_gap="仍需要用户或导师确认问题是否真实、有价值且不跑偏。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="innovation_framework",
                    manual_flow_label="设计创新点和跨尺度框架",
                    coverage_status="landed_route",
                    current_surface="execute-argument-building-pass / execute-fit-alignment-pass",
                    remaining_gap="跨尺度组学、指南更新和多学科交叉证据仍依赖用户输入材料与后续证据补强。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="mainline_closure",
                    manual_flow_label="搭建整体课题并反复校验主线",
                    coverage_status="landed_route",
                    current_surface="grant-user-loop / stage-route-report",
                    remaining_gap="当前能投影 route 与 gate，但还不是成熟 Web UI 里的连续审稿体验。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="significance_background_drafting",
                    manual_flow_label="先写研究意义，再写研究背景",
                    coverage_status="landed_route",
                    current_surface="execute-outline-pass / execute-drafting-pass",
                    remaining_gap="背景文献的新鲜性、引用准确性和段落风格仍需要人工或 Agent 复核。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="preliminary_evidence_and_basis",
                    manual_flow_label="补足预实验、研究基础和前期结果",
                    coverage_status="partially_supported",
                    current_surface="workspace evidence surfaces / build-artifact-bundle",
                    remaining_gap="不会凭空生成真实预实验；缺失证据、图片和原始结果仍必须由用户补充。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="expected_results_timeline",
                    manual_flow_label="完善预期结果与研究进度",
                    coverage_status="partially_supported",
                    current_surface="execute-drafting-pass / build-artifact-bundle",
                    remaining_gap="研究进度、经费/时间排布与申请书表格化输出尚未形成成熟产品面。",
                ),
                _build_shared_workflow_coverage_item(
                    step_id="final_review_figures_package",
                    manual_flow_label="全文反复检查并补图补结果",
                    coverage_status="partially_supported",
                    current_surface="execute-critique-pass / execute-revision-pass / build-submission-ready-package",
                    remaining_gap="本地 submission-ready 交付包已可一键导出，但图件生成、Word/PDF 版式化、官网代投与最终格式审查仍未全自动产品化。",
                ),
            ],
            blocking_gaps=[
                "还不是 mature direct grant Web UI / hosted runtime。",
                "还不能在缺少用户真实材料、前期结果和图片素材时全自动生成可信标书。",
                "文献热点检索、引用证据绑定、图件生产、Word/PDF 定稿与外部官网提交仍未完整产品化。",
            ],
        )
        product_entry_readiness = _build_shared_product_entry_readiness(
            verdict="agent_assisted_ready_not_product_grade",
            usable_now=True,
            good_to_use_now=False,
            fully_automatic=False,
            summary=grant_authoring_readiness["summary"],
            recommended_start_surface=grant_authoring_readiness["recommended_start_surface"],
            recommended_start_command=grant_authoring_readiness["recommended_start_command"],
            recommended_loop_surface=grant_authoring_readiness["recommended_loop_surface"],
            recommended_loop_command=grant_authoring_readiness["recommended_loop_command"],
            blocking_gaps=list(grant_authoring_readiness["blocking_gaps"]),
        )
        runtime_control = _build_runtime_control_surface(
            runtime_summary=runtime_summary,
            managed_runtime_contract=managed_runtime_contract,
            grant_run_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "grant_run_id",
                context="grant-progress",
            ),
            workspace_id=_require_nonempty_string_from_mapping(
                progress_payload,
                "workspace_id",
                context="grant-progress",
            ),
            lifecycle_stage=_require_nonempty_string_from_mapping(
                progress_payload,
                "lifecycle_stage",
                context="grant-progress",
            ),
            journal_path=_require_nonempty_string_from_mapping(
                session_continuity,
                "journal_path",
                context="session_continuity",
            ),
            runtime_resume_command=_require_nonempty_string_from_mapping(
                _require_mapping(
                    _require_mapping(
                        session_continuity,
                        "runtime_entries",
                        context="session_continuity",
                    ),
                    "runtime_resume",
                    context="session_continuity.runtime_entries",
                ),
                "command",
                context="session_continuity.runtime_entries.runtime_resume",
            ),
            grant_progress_command=command_catalog["grant_progress"],
            summarize_workspace_command=command_catalog["summarize_workspace"],
            grant_user_loop_command=grant_user_loop_command,
            grant_direct_entry_command=grant_direct_entry_command,
        )
        human_gate_ids = _collect_family_human_gate_ids(family_orchestration)
        runtime_inventory = _build_shared_runtime_inventory(
            summary=(
                "当前 runtime inventory 由 mainline runtime owner、managed runtime contract 与 grant projection "
                "surface 共同构成。"
            ),
            runtime_owner=_require_nonempty_string_from_mapping(
                runtime_summary,
                "runtime_owner",
                context="product_entry_manifest.runtime",
            ),
            domain_owner=_require_nonempty_string_from_mapping(
                managed_runtime_contract,
                "domain_owner",
                context="product_entry_manifest.managed_runtime_contract",
            ),
            executor_owner=_require_nonempty_string_from_mapping(
                managed_runtime_contract,
                "executor_owner",
                context="product_entry_manifest.managed_runtime_contract",
            ),
            substrate="hermes_agent_managed_runtime",
            availability="ready_to_try_now" if bool(product_entry_preflight.get("ready_to_try_now")) else "preflight_blocked",
            health_status="attention_required" if checkpoint_status == "blocked" else "healthy",
            status_surface={
                "ref_kind": "json_pointer",
                "ref": "/product_entry_manifest/product_entry_shell/grant_progress",
                "role": "runtime_status",
                "label": "grant progress projection surface",
            },
            attention_surface={
                "ref_kind": "json_pointer",
                "ref": "/product_entry_manifest/operator_loop_surface",
                "role": "attention_queue",
                "label": "grant user loop attention surface",
            },
            recovery_surface={
                "ref_kind": "json_pointer",
                "ref": "/product_entry_manifest/family_orchestration/resume_contract",
                "role": "recovery_contract",
                "label": "family resume contract surface",
            },
            workspace_binding={
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(resolved_input_path),
                "grant_run_id": progress_payload["grant_run_id"],
                "workspace_id": progress_payload["workspace_id"],
                "draft_id": progress_payload["draft_id"],
                "lifecycle_stage": progress_payload["lifecycle_stage"],
            },
            domain_projection={
                "runtime": dict(runtime_summary),
                "managed_runtime_contract": dict(managed_runtime_contract),
                "checkpoint_status": checkpoint_status,
                "repo_mainline": dict(repo_mainline),
            },
        )
        task_lifecycle = _build_shared_task_lifecycle(
            task_kind="grant_authoring_mainline",
            task_id=(
                f"{progress_payload['workspace_id']}:"
                f"{_optional_string_from_mapping(verification_identity, 'draft_id') or 'no-draft'}"
            ),
            status=checkpoint_status,
            summary=(
                f"当前 checkpoint_status={checkpoint_status}，"
                f"continuation 指向 {continuation_route_id}({continuation_route_status})。"
            ),
            session_id=progress_payload["grant_run_id"],
            run_id=progress_payload["grant_run_id"],
            progress_surface={
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                "summary": operator_loop_actions["inspect_progress"]["summary"],
                "command": command_catalog["grant_progress"],
                "step_id": "inspect_progress",
                "locator_fields": ["grant_run_id", "workspace_id", "lifecycle_stage"],
            },
            resume_surface={
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": operator_loop_actions["open_loop"]["summary"],
                "command": grant_user_loop_command,
                "step_id": "continue_grant_loop",
                "locator_fields": ["grant_run_id", "lifecycle_stage"],
            },
            checkpoint_summary={
                "status": checkpoint_status,
                "summary": (
                    f"verification checkpoint 对齐 {continuation_route_id} route，"
                    f"route_status={continuation_route_status}。"
                ),
                "checkpoint_id": (
                    f"{progress_payload['workspace_id']}:"
                    f"{_optional_string_from_mapping(verification_identity, 'draft_id') or 'no-draft'}:"
                    f"{progress_payload['lifecycle_stage']}"
                ),
                "lineage_ref": dict(
                    _require_mapping(
                        family_orchestration,
                        "checkpoint_lineage_surface",
                        context="family_orchestration",
                    )
                ),
                "verification_ref": {
                    "ref_kind": "json_pointer",
                    "ref": "/product_entry_manifest/task_lifecycle/domain_projection/verification_checkpoint",
                    "label": "stage route verification checkpoint",
                },
            },
            human_gate_ids=human_gate_ids,
            domain_projection={
                "verification_checkpoint": dict(verification_checkpoint),
                "verification_identity": dict(verification_identity),
                "repo_mainline": dict(repo_mainline),
                "family_orchestration": dict(family_orchestration),
                "continuation_next_action": dict(continuation_next_action),
                "continuation_action_kind": continuation_action_kind,
            },
        )
        skill_catalog = _build_shared_skill_catalog(
            summary="skill catalog 聚合 domain entry command catalog 与当前 product-entry shells。",
            skills=[
                _build_shared_skill_descriptor(
                    skill_id=f"mag.{shell_key}",
                    title=shell_key.replace("_", " ").title(),
                    owner=TARGET_DOMAIN_ID,
                    distribution_mode="repo_tracked_cli_surface",
                    surface_kind=_require_nonempty_string_from_mapping(
                        shell_surface,
                        "surface_kind",
                        context=f"product_entry_shell.{shell_key}",
                    ),
                    description=f"{shell_key} shell 的当前 product-entry command surface。",
                    command=_require_nonempty_string_from_mapping(
                        shell_surface,
                        "command",
                        context=f"product_entry_shell.{shell_key}",
                    ),
                    readiness="landed",
                    tags=[TARGET_DOMAIN_ID, "product-entry-shell", shell_key],
                    domain_projection={"shell_key": shell_key},
                )
                for shell_key, shell_surface in product_entry_shell.items()
            ],
            supported_commands=list(domain_entry_contract.get("supported_commands") or []),
            command_contracts=list(domain_entry_contract.get("command_contracts") or []),
        )
        automation = _build_shared_automation_catalog(
            summary="automation companion 聚合 submission-ready 导出 gate 与 authoring loop continuation 提示。",
            readiness_summary=(
                f"submission_ready={grant_authoring_readiness['fully_automatic']}; "
                f"good_to_use_now={grant_authoring_readiness['good_to_use_now']}"
            ),
            automations=[
                _build_shared_automation_descriptor(
                    automation_id="mag.submission_ready_export",
                    title="Submission-ready export",
                    owner=TARGET_DOMAIN_ID,
                    trigger_kind="manual_submission_gate",
                    target_surface_kind="submission_ready_package",
                    summary=operator_loop_actions["build_submission_ready_package"]["summary"],
                    readiness_status=(
                        "agent_assisted"
                        if grant_authoring_readiness["fully_automatic"] is False
                        else "fully_automatic"
                    ),
                    gate_policy="fail_closed_submission_ready_gate",
                    output_expectation=[
                        "输出 submission-ready-package.json",
                        "输出 fail-closed audit summary",
                        "保持 external_submission_performed=false",
                    ],
                    target_command=command_catalog["build_submission_ready_package"],
                    domain_projection={
                        "automation_scope": "local_submission_package",
                        "readiness_verdict": (
                            "submission_ready"
                            if grant_authoring_readiness["fully_automatic"]
                            else "agent_assisted_ready_not_product_grade"
                        ),
                        "requires": ["output_dir", "submission_ready_export_gate"],
                    },
                ),
                _build_shared_automation_descriptor(
                    automation_id="mag.authoring_loop_continuation",
                    title="Authoring loop continuation",
                    owner=TARGET_DOMAIN_ID,
                    trigger_kind="manual_authoring_resume",
                    target_surface_kind=GRANT_USER_LOOP_KIND,
                    summary=(
                        f"继续 grant user loop 并推进 {continuation_route_id} route "
                        f"({continuation_route_status})。"
                    ),
                    readiness_status="landed",
                    gate_policy="family_human_gate_resume_contract",
                    output_expectation=[
                        "返回 next_action command 或 handoff_surfaces",
                        "保持 route_status 与 checkpoint_status 对齐",
                        "在 human gate 请求时保留人工决策位",
                    ],
                    target_command=grant_user_loop_command,
                    domain_projection={
                        "next_action": dict(continuation_next_action),
                        "human_gate_ids": human_gate_ids,
                        "resume_contract": dict(
                            _require_mapping(
                                family_orchestration,
                                "resume_contract",
                                context="family_orchestration",
                            )
                        ),
                    },
                ),
            ],
        )

        payload = {
            "ok": True,
            "command": "product-entry-manifest",
            "grant_run_id": progress_payload["grant_run_id"],
            "workspace_id": progress_payload["workspace_id"],
            "draft_id": progress_payload["draft_id"],
            "lifecycle_stage": progress_payload["lifecycle_stage"],
            "input_path": progress_payload["input_path"],
            "product_entry_manifest": _build_shared_family_product_entry_manifest(
                manifest_kind=PRODUCT_ENTRY_MANIFEST_KIND,
                target_domain_id=TARGET_DOMAIN_ID,
                formal_entry={
                    "default": "CLI",
                    "supported_protocols": ["MCP"],
                    "internal_surface": "MedAutoGrantDomainEntry",
                },
                workspace_locator={
                    "workspace_surface_kind": "nsfc_workspace",
                    "workspace_root": str(resolved_input_path),
                    "workspace_path": str(resolved_input_path),
                },
                recommended_shell="grant_user_loop",
                recommended_command=grant_user_loop_command,
                frontdesk_surface=frontdesk_surface,
                operator_loop_surface=operator_loop_surface,
                operator_loop_actions=operator_loop_actions,
                repo_mainline=repo_mainline,
                runtime=runtime_summary,
                managed_runtime_contract=managed_runtime_contract,
                runtime_inventory=runtime_inventory,
                task_lifecycle=task_lifecycle,
                session_continuity=session_continuity,
                progress_projection=manifest_progress_projection,
                artifact_inventory=artifact_inventory,
                skill_catalog=skill_catalog,
                automation=automation,
                schema_ref=f"contracts/schemas/v1/{PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE}",
                product_entry_shell=product_entry_shell,
                shared_handoff=build_shared_handoff(
                    direct_entry_builder_command=command_catalog["build_direct_entry"],
                    opl_handoff_builder_command=command_catalog["build_opl_handoff"],
                ),
                product_entry_start=product_entry_start,
                product_entry_overview=product_entry_overview,
                product_entry_preflight=product_entry_preflight,
                product_entry_readiness=product_entry_readiness,
                product_entry_status={
                    "summary": _require_nonempty_string_from_mapping(
                        current_focus,
                        "summary",
                        context="mainline_status.current_focus",
                    ),
                    "next_focus": list(mainline_snapshot["next_focus"]),
                    "remaining_gaps_count": len(mainline_snapshot["remaining_gaps"]),
                },
                product_entry_quickstart=product_entry_quickstart,
                family_orchestration=family_orchestration,
                remaining_gaps=list(mainline_payload.get("remaining_gaps") or []),
                notes=[
                    "This manifest freezes the current repo-tracked grant product shell only.",
                    "It does not claim that mature hosted runtime or Web UI is already landed.",
                    "funding_call stays part of direct-entry build time rather than manifest discovery time.",
                ],
                domain_entry_contract=domain_entry_contract,
                gateway_interaction_contract=gateway_interaction_contract,
                extra_payload={
                    "runtime_control": runtime_control,
                    "grant_authoring_readiness": grant_authoring_readiness,
                },
            ),
        }
        _validate_product_entry_manifest_contract(
            payload,
            grant_run_id=progress_payload["grant_run_id"],
            workspace_id=progress_payload["workspace_id"],
            lifecycle_stage=progress_payload["lifecycle_stage"],
        )
        return payload

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
        product_frontdesk = _build_shared_family_product_frontdesk_from_manifest(
            recommended_action="inspect_or_prepare_grant_loop",
            product_entry_manifest=dict(manifest),
            shell_aliases={
                "frontdesk": "product_frontdesk",
                "grant_progress": "grant_progress",
                "grant_cockpit": "grant_cockpit",
                "grant_direct_entry": "grant_direct_entry",
                "grant_user_loop": "grant_user_loop",
            },
            schema_ref=f"contracts/schemas/v1/{PRODUCT_FRONTDESK_SCHEMA_FILE}",
            notes=[
                "This frontdesk surface is a controller-owned direct grant front door over the landed product-entry shell.",
                "It does not claim that mature Web UI or hosted runtime is already landed.",
            ],
            extra_payload={
                "grant_authoring_readiness": dict(_require_mapping(
                    manifest,
                    "grant_authoring_readiness",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "session_continuity": dict(_require_mapping(
                    manifest,
                    "session_continuity",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "progress_projection": dict(_require_mapping(
                    manifest,
                    "progress_projection",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "artifact_inventory": dict(_require_mapping(
                    manifest,
                    "artifact_inventory",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "runtime_control": dict(_require_mapping(
                    manifest,
                    "runtime_control",
                    context="product_frontdesk.product_entry_manifest",
                )),
            },
        )

        payload = {
            "ok": True,
            "command": "product-frontdesk",
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
            "product_frontdesk": product_frontdesk,
        }
        _validate_product_frontdesk_contract(
            payload,
            grant_run_id=manifest_payload["grant_run_id"],
            workspace_id=manifest_payload["workspace_id"],
            lifecycle_stage=manifest_payload["lifecycle_stage"],
        )
        return payload

    def build_product_entry_start(
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
            context="product_start",
        )
        return {
            "ok": True,
            "command": "product-start",
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
            "product_entry_start": dict(
                _require_mapping(
                    manifest,
                    "product_entry_start",
                    context="product_start.product_entry_manifest",
                )
            ),
        }

    def build_product_entry_preflight(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        document = load_workspace_document(resolved_input_path)
        validation = validate_workspace_document(document)
        current_selection = document.get("current_selection") if isinstance(document.get("current_selection"), Mapping) else {}
        draft_id = _require_optional_string(current_selection.get("active_draft_id"), field_name="draft_id")
        mainline_payload = read_mainline_status()
        current_line = _require_mapping(
            mainline_payload,
            "current_line",
            context="mainline_status",
        )
        current_owner_line = _require_nonempty_string_from_mapping(
            current_line,
            "current_owner_line",
            context="mainline_status.current_line",
        )
        validate_command = public_cli_command(
            "validate-workspace", "--input", str(resolved_input_path), "--format", "json"
        )
        start_command = public_cli_command(
            "product-frontdesk", "--input", str(resolved_input_path), "--format", "json"
        )
        mainline_command = public_cli_command("mainline-status", "--format", "json")
        checks = [
            {
                "check_id": "workspace_document_valid",
                "title": "Workspace Document Valid",
                "status": "pass" if validation.ok else "fail",
                "blocking": True,
                "summary": (
                    "workspace document schema 与 runtime constraints 均通过。"
                    if validation.ok
                    else "workspace document 仍有 schema 或 runtime constraint 问题。"
                ),
                "command": validate_command,
            },
            {
                "check_id": "upstream_hermes_owner_line",
                "title": "Upstream Hermes Owner Line",
                "status": "pass" if "Hermes" in current_owner_line else "fail",
                "blocking": True,
                "summary": (
                    "当前 runtime owner line 已对齐 upstream Hermes substrate。"
                    if "Hermes" in current_owner_line
                    else "当前 runtime owner line 尚未对齐 upstream Hermes substrate。"
                ),
                "command": mainline_command,
            },
            {
                "check_id": "direct_frontdoor_contract_landed",
                "title": "Direct Frontdoor Contract Landed",
                "status": "pass",
                "blocking": True,
                "summary": "direct frontdoor contract 已 landed，可由 product-frontdesk / manifest 直接消费。",
                "command": start_command,
            },
            {
                "check_id": "submission_ready_export_gate",
                "title": "Submission Ready Export Gate",
                "status": "pass" if document.get("lifecycle_stage") == "frozen" else "warn",
                "blocking": False,
                "summary": (
                    "当前 stage 已接近或进入 submission-ready export gate。"
                    if document.get("lifecycle_stage") == "frozen"
                    else "当前 stage 还未到 submission-ready export gate；这不阻止进入 frontdoor，但后续仍需继续主线推进。"
                ),
                "command": public_cli_command(
                    "build-submission-ready-package",
                    "--input",
                    str(resolved_input_path),
                    "--output-dir",
                    "<output-dir>",
                    "--format",
                    "json",
                ),
            },
        ]
        blocking_check_ids = [
            check["check_id"]
            for check in checks
            if check["blocking"] and check["status"] != "pass"
        ]
        ready_to_try_now = not blocking_check_ids
        summary = (
            "当前 direct grant frontdoor 的前置检查已通过，可以先复核 workspace 与主线，再进入 product frontdesk。"
            if ready_to_try_now
            else "当前 direct grant frontdoor 仍有 blocking preflight check；请先修复 workspace 或 runtime owner line 再进入 product frontdesk。"
        )
        product_entry_preflight = _build_shared_product_entry_preflight(
            summary=summary,
            recommended_check_command=validate_command,
            recommended_start_command=start_command,
            checks=checks,
        )
        return {
            "ok": True,
            "command": "product-preflight",
            "grant_run_id": _require_nonempty_string(document.get("grant_run_id"), field_name="grant_run_id"),
            "workspace_id": _require_nonempty_string(document.get("workspace_id"), field_name="workspace_id"),
            "draft_id": draft_id,
            "lifecycle_stage": _require_nonempty_string(document.get("lifecycle_stage"), field_name="lifecycle_stage"),
            "input_path": str(resolved_input_path),
            "product_entry_preflight": product_entry_preflight,
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
    route_contract = _build_author_side_route_contract(
        resolved_route_id,
        source_stage=resolved_route_id,
    )
    return _require_nonempty_string_from_mapping(
        route_contract,
        "route_status",
        context="author_side_route_contract",
    )


def _build_family_orchestration_companion(
    *,
    current_route_id: str,
    recommended_route_id: str,
    recommended_route_status: str,
    needs_author_decision: bool,
    workspace_summary: Mapping[str, Any] | None = None,
    intake_evidence_companion: Mapping[str, Any] | None = None,
    project_profile_companion: Mapping[str, Any] | None = None,
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
    current_node_id = f"route:{resolved_current_route_id}"
    recommended_node_id = f"route:{resolved_recommended_route_id}"
    edge_on = "decision" if gate_status == "requested" else "success"
    resolved_intake_evidence_companion = (
        dict(intake_evidence_companion)
        if isinstance(intake_evidence_companion, Mapping)
        else _build_intake_evidence_companion(workspace_summary)
    )
    resolved_project_profile_companion = (
        dict(project_profile_companion)
        if isinstance(project_profile_companion, Mapping)
        else _build_project_profile_companion(workspace_summary)
    )
    payload = _build_shared_family_product_entry_orchestration(
        graph_id=f"mag_{resolved_current_route_id}_to_{resolved_recommended_route_id}_graph",
        target_domain_id=TARGET_DOMAIN_ID,
        graph_kind="grant_route_orchestration",
        graph_version="2026-04-13",
        nodes=[
            {
                "node_id": current_node_id,
                "node_kind": _route_to_action_node_kind(resolved_current_route_id),
                "title": f"Current route: {resolved_current_route_id}",
                "produces_checkpoint": True,
            },
            {
                "node_id": recommended_node_id,
                "node_kind": _route_to_action_node_kind(resolved_recommended_route_id),
                "title": f"Recommended route: {resolved_recommended_route_id}",
                "produces_checkpoint": True,
            },
        ],
        edges=[
            {
                "from": current_node_id,
                "to": recommended_node_id,
                "on": edge_on,
            }
        ],
        entry_nodes=[current_node_id],
        exit_nodes=[recommended_node_id],
        human_gates=[
            {
                "gate_id": gate_id,
                "trigger_nodes": [recommended_node_id],
                "blocking": gate_status == "requested",
            }
        ],
        checkpoint_nodes=[current_node_id, recommended_node_id],
        human_gate_previews=[
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
        action_graph_ref={
            "ref_kind": "json_pointer",
            "ref": "/family_orchestration/action_graph",
            "label": "mag family action graph",
        },
        resume_surface_kind=resolved_resume_surface_kind,
        session_locator_field="grant_run_id",
        checkpoint_locator_field="lifecycle_stage",
        event_envelope_surface={
            "ref_kind": "json_pointer",
            "ref": resolved_event_envelope_surface_ref,
            "label": "family event envelope surface",
        },
        checkpoint_lineage_surface={
            "ref_kind": "json_pointer",
            "ref": resolved_checkpoint_lineage_surface_ref,
            "label": "family checkpoint lineage surface",
        },
        intake_evidence_companion=resolved_intake_evidence_companion,
    )
    if resolved_project_profile_companion is not None:
        payload["project_profile_companion"] = resolved_project_profile_companion
    return payload


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


def _read_projection_blockers(
    *,
    workspace_summary: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> list[str]:
    critique_blockers = _read_blocking_issues(critique_summary)
    if critique_blockers:
        return critique_blockers

    blockers: list[str] = []
    intake_audit = _optional_mapping(workspace_summary, "grant_intake_audit")
    evidence_grounding = _optional_mapping(workspace_summary, "grant_evidence_grounding")
    if isinstance(intake_audit, Mapping):
        blockers.extend(_read_nonempty_string_list(intake_audit.get("blocking_gaps"), context="grant_intake_audit"))
    if isinstance(evidence_grounding, Mapping):
        blockers.extend(
            _read_nonempty_string_list(
                evidence_grounding.get("evidence_gaps"),
                context="grant_evidence_grounding",
            )
        )
    seen: set[str] = set()
    ordered: list[str] = []
    for blocker in blockers:
        if blocker not in seen:
            seen.add(blocker)
            ordered.append(blocker)
    return ordered


def _build_intake_evidence_companion(workspace_summary: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(workspace_summary, Mapping):
        return None
    intake_audit = _optional_mapping(workspace_summary, "grant_intake_audit")
    evidence_grounding = _optional_mapping(workspace_summary, "grant_evidence_grounding")
    intake_snapshot = _optional_mapping(workspace_summary, "intake_snapshot")
    if not isinstance(intake_audit, Mapping) or not isinstance(evidence_grounding, Mapping):
        return None
    trust_ranked_evidence = [
        entry
        for entry in evidence_grounding.get("trust_ranked_evidence", [])
        if isinstance(entry, Mapping)
    ]
    if not trust_ranked_evidence:
        return None

    workspace_id = _require_nonempty_string_from_mapping(
        workspace_summary,
        "workspace_id",
        context="summarize-workspace",
    )
    funding_program = (
        _require_nonempty_string_from_mapping(
            intake_snapshot,
            "funding_program",
            context="summarize-workspace.intake_snapshot",
        )
        if isinstance(intake_snapshot, Mapping)
        else _require_nonempty_string_from_mapping(
            evidence_grounding,
            "funding_program",
            context="grant_evidence_grounding",
        )
    )
    return _build_shared_family_intake_evidence_companion(
        target_domain_id=TARGET_DOMAIN_ID,
        intake_audit={
            "summary": _require_nonempty_string_from_mapping(
                intake_audit,
                "summary",
                context="grant_intake_audit",
            ),
            "verdict": _require_nonempty_string_from_mapping(
                intake_audit,
                "overall_readiness",
                context="grant_intake_audit",
            ),
            "summary_ref": {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::grant_intake_audit",
                "label": "grant intake audit",
            },
        },
        trust_ranked_evidence_refs=[
            {
                "ref_kind": _require_nonempty_string_from_mapping(
                    entry,
                    "ref_kind",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "ref": _require_nonempty_string_from_mapping(
                    entry,
                    "ref",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "label": _require_nonempty_string_from_mapping(
                    entry,
                    "label",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "trust_rank": int(entry["trust_rank"]),
                "trust_note": _optional_string_from_mapping(entry, "trust_note"),
                "supports": list(entry.get("supports") or []),
            }
            for entry in trust_ranked_evidence
        ],
        grounding_scope={
            "scope_kind": _require_nonempty_string_from_mapping(
                evidence_grounding,
                "scope_kind",
                context="grant_evidence_grounding",
            ),
            "summary": _require_nonempty_string_from_mapping(
                evidence_grounding,
                "summary",
                context="grant_evidence_grounding",
            ),
            "scope_refs": [
                {
                    "ref_kind": "workspace_locator",
                    "ref": f"grant_workspace::{workspace_id}::grant_evidence_grounding",
                    "label": "grant evidence grounding",
                },
                {
                    "ref_kind": "workspace_locator",
                    "ref": f"grant_workspace::{workspace_id}::funding_opportunity_brief::{funding_program}",
                    "label": "funding opportunity brief",
                },
            ],
        },
        human_gate_refs=[
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::family_human_gate",
                "label": "grant route gate",
            }
        ],
        checkpoint_lineage_refs=[
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::checkpoint_lineage",
                "label": "grant checkpoint lineage",
            }
        ],
    )


def _build_project_profile_companion(workspace_summary: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(workspace_summary, Mapping):
        return None
    workspace_id = _require_nonempty_string_from_mapping(
        workspace_summary,
        "workspace_id",
        context="summarize-workspace",
    )
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
        context="summarize-workspace",
    )
    profile_id = _require_nonempty_string_from_mapping(
        project_profile,
        "profile_id",
        context="summarize-workspace.project_profile",
    )
    funding_program = _require_nonempty_string_from_mapping(
        project_profile,
        "funding_program",
        context="summarize-workspace.project_profile",
    )
    return {
        "surface_kind": "project_profile_companion",
        "version": 1,
        "profile_id": profile_id,
        "preset_id": _require_nonempty_string_from_mapping(
            project_profile,
            "preset_id",
            context="summarize-workspace.project_profile",
        ),
        "profile_label": _require_nonempty_string_from_mapping(
            project_profile,
            "profile_label",
            context="summarize-workspace.project_profile",
        ),
        "funding_program": funding_program,
        "funder": _require_nonempty_string_from_mapping(
            project_profile,
            "funder",
            context="summarize-workspace.project_profile",
        ),
        "program_family": _require_nonempty_string_from_mapping(
            project_profile,
            "program_family",
            context="summarize-workspace.project_profile",
        ),
        "template_profile": {
            "template_id": _require_nonempty_string_from_mapping(
                project_profile,
                "template_id",
                context="summarize-workspace.project_profile",
            ),
            "template_label": _require_nonempty_string_from_mapping(
                project_profile,
                "template_label",
                context="summarize-workspace.project_profile",
            ),
        },
        "collaboration_preferences": {
            "collaboration_mode": _require_nonempty_string_from_mapping(
                project_profile,
                "collaboration_mode",
                context="summarize-workspace.project_profile",
            ),
            "author_touchpoints": list(project_profile.get("author_touchpoints") or []),
            "evidence_policy": _require_nonempty_string_from_mapping(
                project_profile,
                "evidence_policy",
                context="summarize-workspace.project_profile",
            ),
            "drafting_voice": _require_nonempty_string_from_mapping(
                project_profile,
                "drafting_voice",
                context="summarize-workspace.project_profile",
            ),
        },
        "critique_policy": {
            "preset_id": _require_nonempty_string_from_mapping(
                project_profile,
                "critique_policy_preset_id",
                context="summarize-workspace.project_profile",
            ),
            "policy_id": _require_nonempty_string_from_mapping(
                project_profile,
                "critique_policy_id",
                context="summarize-workspace.project_profile",
            ),
        },
        "profile_ref": {
            "ref_kind": "workspace_locator",
            "ref": f"grant_workspace::{workspace_id}::project_profile::{profile_id}",
            "label": "project profile",
        },
        "funding_opportunity_ref": {
            "ref_kind": "workspace_locator",
            "ref": f"grant_workspace::{workspace_id}::funding_opportunity_brief::{funding_program}",
            "label": "funding opportunity brief",
        },
    }


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
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
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
        "project_profile_label": _require_nonempty_string_from_mapping(
            project_profile,
            "profile_label",
            context="summarize-workspace.project_profile",
        ),
        "template_label": _require_nonempty_string_from_mapping(
            project_profile,
            "template_label",
            context="summarize-workspace.project_profile",
        ),
        "critique_policy_id": _require_nonempty_string_from_mapping(
            project_profile,
            "critique_policy_id",
            context="summarize-workspace.project_profile",
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
        "project_profile_label": focus["project_profile_label"],
        "template_label": focus["template_label"],
        "critique_policy_id": focus["critique_policy_id"],
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
    _validate_runtime_continuity_alignment(
        session_continuity=_require_mapping(
            payload,
            "session_continuity",
            context="grant_direct_entry",
        ),
        progress_surface=_require_mapping(
            payload,
            "progress_projection",
            context="grant_direct_entry",
        ),
        artifact_inventory=_require_mapping(
            payload,
            "artifact_inventory",
            context="grant_direct_entry",
        ),
        runtime_control=_require_mapping(
            payload,
            "runtime_control",
            context="grant_direct_entry",
        ),
        projection_truth=_require_mapping(
            grant_direct_entry,
            "progress_projection",
            context="grant_direct_entry",
        ),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        context_prefix="grant_direct_entry",
    )


def _build_mainline_snapshot(mainline_status: Mapping[str, Any]) -> dict[str, Any]:
    current_line = _require_mapping(
        mainline_status,
        "current_line",
        context="mainline_status",
    )
    current_focus = _require_mapping(
        mainline_status,
        "current_focus",
        context="mainline_status",
    )
    maintainer_references = _require_mapping(
        mainline_status,
        "maintainer_references",
        context="mainline_status",
    )
    current_runtime_owner = _require_mapping(
        maintainer_references,
        "runtime_owner",
        context="mainline_status.maintainer_references",
    )
    phase_ladder = maintainer_references.get("phase_ladder")
    if not isinstance(phase_ladder, list):
        raise WorkspaceStateError("mainline_status.maintainer_references.phase_ladder 必须为 list。")
    return {
        "current_owner_line": _require_nonempty_string_from_mapping(
            current_line,
            "current_owner_line",
            context="mainline_status.current_line",
        ),
        "active_phase": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_phase",
            context="mainline_status.maintainer_references.runtime_owner",
        ),
        "active_tranche": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_tranche",
            context="mainline_status.maintainer_references.runtime_owner",
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
            current_focus.get("focus_items"),
            context="mainline_status.current_focus.focus_items",
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
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
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
            "command": _build_route_execution_command(
                route_id=route_id,
                input_path=input_path,
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
            ),
            "handoff_surfaces": None,
        }

    raise WorkspaceStateError(
        f"grant_user_loop 只接受已 landed 的 route contract，收到 {route_id}({route_status})。",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=route_id,
    )


def _build_route_execution_command(
    *,
    route_id: str,
    input_path: Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> str:
    resolved_input_path = input_path.expanduser().resolve()
    output_path = _build_runtime_route_output_path(
        route_id=route_id,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
    )
    if route_id == "direction_screening":
        return public_cli_command(
            "execute-direction-screening-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "question_refinement":
        return public_cli_command(
            "execute-question-refinement-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "argument_building":
        return public_cli_command(
            "execute-argument-building-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "fit_alignment":
        return public_cli_command(
            "execute-fit-alignment-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "outline":
        return public_cli_command(
            "execute-outline-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "drafting":
        return public_cli_command(
            "execute-drafting-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "critique":
        return public_cli_command(
            "execute-critique-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "revision":
        return public_cli_command(
            "execute-revision-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "frozen":
        return public_cli_command(
            "execute-freeze-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "artifact_bundle":
        return public_cli_command(
            "build-artifact-bundle",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "final_package":
        artifact_bundle_path = _build_runtime_route_output_path(
            route_id="artifact_bundle",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            "build-final-package",
            "--input",
            str(resolved_input_path),
            "--artifact-bundle",
            str(artifact_bundle_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "hosted_contract_bundle":
        final_package_path = _build_runtime_route_output_path(
            route_id="final_package",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            "build-hosted-contract-bundle",
            "--final-package",
            str(final_package_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    raise WorkspaceStateError(f"grant_user_loop 不支持 landed route command: {route_id}")


def _build_runtime_route_output_path(
    *,
    route_id: str,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> Path:
    output_file = {
        "direction_screening": "direction-screening-workspace.json",
        "question_refinement": "question-refinement-workspace.json",
        "argument_building": "argument-building-workspace.json",
        "fit_alignment": "fit-alignment-workspace.json",
        "outline": "outline-workspace.json",
        "drafting": "drafting-workspace.json",
        "critique": "critique-workspace.json",
        "revision": "revision-workspace.json",
        "frozen": "frozen-workspace.json",
        "artifact_bundle": "artifact-bundle.json",
        "final_package": "final-package.json",
        "hosted_contract_bundle": "hosted-contract-bundle.json",
    }.get(route_id)
    if output_file is None:
        raise WorkspaceStateError(f"grant_user_loop 不支持 runtime output path route: {route_id}")

    program_id = _require_runtime_path_segment(read_program_id(), field_name="program_id")
    return (
        resolve_runtime_state_root()
        / "reports"
        / program_id
        / _require_runtime_path_segment(grant_run_id, field_name="grant_run_id")
        / _require_runtime_path_segment(workspace_id, field_name="workspace_id")
        / _require_runtime_path_segment(draft_id or "no-draft", field_name="draft_id")
        / output_file
    ).resolve()


def _require_runtime_path_segment(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"grant_user_loop runtime output path 缺少合法字段: {field_name}")
    resolved_value = value.strip()
    if resolved_value in {".", ".."} or "/" in resolved_value or "\\" in resolved_value:
        raise WorkspaceStateError(f"grant_user_loop runtime output path 字段不能包含路径分隔符: {field_name}")
    return resolved_value


def _build_grant_user_loop_commands(
    *,
    input_path: Path,
    task_intent: str,
    run_recommended_route: Any,
) -> dict[str, Any]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "mainline_status": public_cli_command("mainline-status", "--format", "json"),
        "phase_status_current": public_cli_command("mainline-phase", "--phase", "current", "--format", "json"),
        "phase_status_next": public_cli_command("mainline-phase", "--phase", "next", "--format", "json"),
        "open_grant_cockpit": public_cli_command(
            "grant-cockpit", "--input", str(resolved_input_path), "--format", "json"
        ),
        "open_grant_direct_entry": public_cli_command(
            "grant-direct-entry",
            "--input",
            str(resolved_input_path),
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        "run_recommended_route": (
            _require_nonempty_string(run_recommended_route, field_name="run_recommended_route")
            if run_recommended_route is not None
            else None
        ),
        "build_direct_entry": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "direct",
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        "build_opl_handoff": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "opl-handoff",
            "--task-intent",
            task_intent,
            "--format",
            "json",
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
    _validate_runtime_continuity_alignment(
        session_continuity=_require_mapping(
            grant_user_loop,
            "session_continuity",
            context="grant_user_loop.session_continuity",
        ),
        progress_surface=_require_mapping(
            grant_user_loop,
            "progress_projection",
            context="grant_user_loop.progress_projection",
        ),
        artifact_inventory=_require_mapping(
            grant_user_loop,
            "artifact_inventory",
            context="grant_user_loop.artifact_inventory",
        ),
        runtime_control=_require_mapping(
            grant_user_loop,
            "runtime_control",
            context="grant_user_loop.runtime_control",
        ),
        projection_truth=_require_mapping(
            grant_direct_entry,
            "progress_projection",
            context="grant_user_loop.grant_direct_entry",
        ),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        context_prefix="grant_user_loop",
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
    elif action_kind != "execute_landed_route":
        raise WorkspaceStateError(
            f"grant_user_loop.next_action.action_kind 非法: {action_kind}",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _validate_product_entry_manifest_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_shared_family_product_entry_manifest(
        payload["product_entry_manifest"],
        require_contract_bundle=True,
        require_runtime_companions=True,
    )
    _validate_contract_schema(
        _schema_payload_without_contract_bundle(payload, surface_key="product_entry_manifest"),
        schema_file=PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
        context="product_entry_manifest",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _validate_product_frontdesk_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_shared_family_product_frontdesk(
        payload["product_frontdesk"],
        require_contract_bundle=True,
        require_runtime_companions=True,
    )
    _validate_contract_schema(
        _schema_payload_without_contract_bundle(payload, surface_key="product_frontdesk"),
        schema_file=PRODUCT_FRONTDESK_SCHEMA_FILE,
        context="product_frontdesk",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    product_frontdesk = _require_mapping(
        payload,
        "product_frontdesk",
        context="product_frontdesk",
    )
    manifest = _require_mapping(
        product_frontdesk,
        "product_entry_manifest",
        context="product_frontdesk.product_entry_manifest",
    )
    for surface_key in ("session_continuity", "progress_projection", "artifact_inventory", "runtime_control"):
        if product_frontdesk.get(surface_key) != manifest.get(surface_key):
            raise WorkspaceStateError(
                f"product_frontdesk.{surface_key} 与 product_entry_manifest.{surface_key} 不一致。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )


def _validate_runtime_continuity_alignment(
    *,
    session_continuity: Mapping[str, Any],
    progress_surface: Mapping[str, Any],
    artifact_inventory: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    projection_truth: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    context_prefix: str,
) -> None:
    if progress_surface.get("projection") != projection_truth:
        raise WorkspaceStateError(
            f"{context_prefix}.progress_projection 与 continuity progress surface 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            session_continuity,
            "session_id",
            context=f"{context_prefix}.session_continuity",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.session_continuity.session_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            progress_surface,
            "grant_run_id",
            context=f"{context_prefix}.progress_projection",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.progress_projection.grant_run_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            artifact_inventory,
            "grant_run_id",
            context=f"{context_prefix}.artifact_inventory",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.artifact_inventory.grant_run_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    runtime_control_session_locator = _require_mapping(
        runtime_control,
        "session_locator",
        context=f"{context_prefix}.runtime_control",
    )
    if (
        _require_nonempty_string_from_mapping(
            runtime_control_session_locator,
            "locator_value",
            context=f"{context_prefix}.runtime_control.session_locator",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.runtime_control.session_locator.locator_value 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    runtime_control_restore_point = _require_mapping(
        runtime_control,
        "restore_point",
        context=f"{context_prefix}.runtime_control",
    )
    if (
        _require_nonempty_string_from_mapping(
            runtime_control_restore_point,
            "session_id",
            context=f"{context_prefix}.runtime_control.restore_point",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.runtime_control.restore_point.session_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _schema_payload_without_contract_bundle(
    payload: Mapping[str, Any],
    *,
    surface_key: str,
) -> dict[str, Any]:
    normalized_payload = dict(payload)
    surface = dict(
        _require_mapping(
            payload,
            surface_key,
            context=f"{surface_key}_schema_validation",
        )
    )
    _strip_contract_bundle_fields(surface)
    nested_manifest = surface.get("product_entry_manifest")
    if isinstance(nested_manifest, Mapping):
        normalized_manifest = dict(nested_manifest)
        _strip_contract_bundle_fields(normalized_manifest)
        surface["product_entry_manifest"] = normalized_manifest
    normalized_payload[surface_key] = surface
    return normalized_payload


def _build_runtime_continuity_surfaces(
    *,
    progress_projection: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
    runtime_summary: Mapping[str, Any],
    managed_runtime_contract: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
    grant_progress_command: str,
    summarize_workspace_command: str,
    stage_route_report_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
) -> dict[str, dict[str, Any]]:
    session_continuity = _build_session_continuity_surface(
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
    )
    progress_surface = _build_progress_projection_surface(
        projection=dict(progress_projection),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
        inspect_progress_command=grant_progress_command,
        summarize_workspace_command=summarize_workspace_command,
        stage_route_report_command=stage_route_report_command,
    )
    artifact_inventory = _build_artifact_inventory_surface(
        workspace_summary=workspace_summary,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
    )
    runtime_control = _build_runtime_control_surface(
        runtime_summary=runtime_summary,
        managed_runtime_contract=managed_runtime_contract,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        journal_path=_require_nonempty_string_from_mapping(
            session_continuity,
            "journal_path",
            context="session_continuity",
        ),
        runtime_resume_command=_require_nonempty_string_from_mapping(
            _require_mapping(
                _require_mapping(
                    session_continuity,
                    "runtime_entries",
                    context="session_continuity",
                ),
                "runtime_resume",
                context="session_continuity.runtime_entries",
            ),
            "command",
            context="session_continuity.runtime_entries.runtime_resume",
        ),
        grant_progress_command=grant_progress_command,
        summarize_workspace_command=summarize_workspace_command,
        grant_user_loop_command=grant_user_loop_command,
        grant_direct_entry_command=grant_direct_entry_command,
    )
    return {
        "session_continuity": session_continuity,
        "progress_projection": progress_surface,
        "artifact_inventory": artifact_inventory,
        "runtime_control": runtime_control,
    }


def _build_session_continuity_surface(
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
) -> dict[str, Any]:
    runtime_state_contract = _build_runtime_state_contract()
    session_journal_root = _require_nonempty_string_from_mapping(
        runtime_state_contract,
        "session_journal_root",
        context="runtime_state_contract",
    )
    journal_path = f"{session_journal_root}{grant_run_id}.json"
    runtime_run_command = public_cli_command(
        "runtime-run",
        "--input",
        input_path,
        "--journal",
        journal_path,
        "--format",
        "json",
    )
    runtime_resume_command = public_cli_command(
        "runtime-resume",
        "--journal",
        journal_path,
        "--format",
        "json",
    )
    return {
        "surface_kind": "session_continuity",
        "version": 1,
        "summary": "显式锚定 session locator 与 journal durable anchor，避免依赖默认 journal 推断。",
        "session_locator_field": "grant_run_id",
        "session_handle_kind": "grant_run_id",
        "session_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "runtime_state_contract": dict(runtime_state_contract),
        "journal_path": journal_path,
        "runtime_entries": {
            "runtime_run": {
                "command": runtime_run_command,
                "surface_kind": "runtime_run",
                "summary": "用显式 --journal 启动或继续当前 workspace 的 runtime run。",
            },
            "runtime_resume": {
                "command": runtime_resume_command,
                "surface_kind": "runtime_resume",
                "summary": "用显式 --journal 恢复当前 session。",
            },
        },
        "repo_owned_truth": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": input_path,
            "truth_owner": TARGET_DOMAIN_ID,
        },
    }


def _build_runtime_control_surface(
    *,
    runtime_summary: Mapping[str, Any],
    managed_runtime_contract: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    journal_path: str,
    runtime_resume_command: str,
    grant_progress_command: str,
    summarize_workspace_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "runtime_control",
        "version": 2,
        "summary": (
            "repo-owned runtime control reference：显式导出 owner 语义、restore point、"
            "progress/artifact/approval surface 与 direct-entry locator。"
        ),
        "runtime_owner": _require_nonempty_string_from_mapping(
            runtime_summary,
            "runtime_owner",
            context="runtime_summary",
        ),
        "domain_owner": _require_nonempty_string_from_mapping(
            managed_runtime_contract,
            "domain_owner",
            context="managed_runtime_contract",
        ),
        "executor_owner": _require_nonempty_string_from_mapping(
            managed_runtime_contract,
            "executor_owner",
            context="managed_runtime_contract",
        ),
        "session_locator": {
            "locator_field": "grant_run_id",
            "locator_value": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "restore_point": {
            "session_id": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "journal_path": journal_path,
            "resume_command": runtime_resume_command,
            "resume_surface_kind": "runtime_resume",
        },
        "progress_surface": {
            "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "command": grant_progress_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/progress_projection",
            "summary": "当前 grant progress projection surface。",
        },
        "artifact_pickup_surface": {
            "surface_kind": "artifact_inventory",
            "command": summarize_workspace_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/artifact_inventory",
            "summary": "当前 workspace artifact pickup index surface。",
        },
        "approval_control_surface": {
            "surface_kind": GRANT_USER_LOOP_KIND,
            "command": grant_user_loop_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/operator_loop_surface",
            "summary": "当前人工 gate / control action 入口。",
        },
        "direct_entry": {
            "surface_kind": GRANT_DIRECT_ENTRY_KIND,
            "command": grant_direct_entry_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/product_entry_shell/grant_direct_entry",
            "summary": "直接导出当前 grant direct-entry command 与 locator。",
        },
    }


def _build_progress_projection_surface(
    *,
    projection: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
    inspect_progress_command: str,
    summarize_workspace_command: str,
    stage_route_report_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "progress_projection",
        "version": 1,
        "summary": "repo-owned workspace truth 上的 grant progress projection。",
        "workspace_surface_kind": "nsfc_workspace",
        "workspace_path": input_path,
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "projection_kind": _require_nonempty_string_from_mapping(
            projection,
            "projection_kind",
            context="grant-progress.progress_projection",
        ),
        "projection": dict(projection),
        "truth_anchors": {
            "workspace_document": {
                "ref_kind": "path",
                "ref": input_path,
                "label": "workspace JSON (repo-owned truth)",
            },
            "stage_route_report": {
                "ref_kind": "command",
                "ref": stage_route_report_command,
                "label": "stage-route-report (derives from workspace truth)",
            },
            "summarize_workspace": {
                "ref_kind": "command",
                "ref": summarize_workspace_command,
                "label": "summarize-workspace (derives from workspace truth)",
            },
            "inspect_progress": {
                "ref_kind": "command",
                "ref": inspect_progress_command,
                "label": "grant-progress (projection surface)",
            },
        },
    }


def _build_artifact_inventory_surface(
    *,
    workspace_summary: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = [
        {
            "artifact_kind": "workspace_document",
            "label": "workspace JSON (repo-owned truth)",
            "ref": {
                "ref_kind": "path",
                "ref": input_path,
            },
        }
    ]

    def _append_workspace_ref(*, artifact_kind: str, label: str, ref: str) -> None:
        artifacts.append(
            {
                "artifact_kind": artifact_kind,
                "label": label,
                "ref": {
                    "ref_kind": "workspace_locator",
                    "ref": ref,
                },
            }
        )

    active_draft = _optional_mapping(workspace_summary, "active_draft")
    if isinstance(active_draft, Mapping):
        draft_id = _optional_string_from_mapping(active_draft, "id")
        if draft_id is not None:
            _append_workspace_ref(
                artifact_kind="active_draft",
                label=f"active draft: {draft_id}",
                ref=f"grant_workspace::{workspace_id}::application_drafts::{draft_id}",
            )

    active_revision_plan = _optional_mapping(workspace_summary, "active_revision_plan")
    if isinstance(active_revision_plan, Mapping):
        revision_plan_id = _optional_string_from_mapping(active_revision_plan, "id")
        if revision_plan_id is not None:
            _append_workspace_ref(
                artifact_kind="active_revision_plan",
                label=f"active revision plan: {revision_plan_id}",
                ref=f"grant_workspace::{workspace_id}::revision_plans::{revision_plan_id}",
            )

    active_critique = _optional_mapping(workspace_summary, "active_critique")
    if isinstance(active_critique, Mapping):
        critique_id = _optional_string_from_mapping(active_critique, "id")
        if critique_id is not None:
            _append_workspace_ref(
                artifact_kind="active_critique",
                label=f"active critique: {critique_id}",
                ref=f"grant_workspace::{workspace_id}::mentor_critiques::{critique_id}",
            )

    selected_direction = _optional_mapping(workspace_summary, "selected_direction")
    if isinstance(selected_direction, Mapping):
        direction_id = _optional_string_from_mapping(selected_direction, "id")
        if direction_id is not None:
            _append_workspace_ref(
                artifact_kind="selected_direction",
                label=f"selected direction: {direction_id}",
                ref=f"grant_workspace::{workspace_id}::direction_hypotheses::{direction_id}",
            )

    selected_question = _optional_mapping(workspace_summary, "selected_question")
    if isinstance(selected_question, Mapping):
        question_id = _optional_string_from_mapping(selected_question, "id")
        if question_id is not None:
            _append_workspace_ref(
                artifact_kind="selected_question",
                label=f"selected question: {question_id}",
                ref=f"grant_workspace::{workspace_id}::scientific_question_cards::{question_id}",
            )

    return {
        "surface_kind": "artifact_inventory",
        "version": 1,
        "summary": "汇总 workspace 内当前被选中的主要对象与 draft 工件，作为 repo-owned continuity truth 的索引。",
        "workspace_surface_kind": "nsfc_workspace",
        "workspace_path": input_path,
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "artifacts": artifacts,
    }


def _strip_contract_bundle_fields(surface: dict[str, Any]) -> None:
    surface.pop("schema_ref", None)
    surface.pop("domain_entry_contract", None)
    surface.pop("gateway_interaction_contract", None)


def _build_product_command_catalog(input_path: Path) -> dict[str, str]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "grant_progress": public_cli_command(
            "grant-progress", "--input", str(resolved_input_path), "--format", "json"
        ),
        "grant_intake_audit": public_cli_command(
            "grant-intake-audit", "--input", str(resolved_input_path), "--format", "json"
        ),
        "grant_evidence_grounding": public_cli_command(
            "grant-evidence-grounding", "--input", str(resolved_input_path), "--format", "json"
        ),
        "summarize_workspace": public_cli_command(
            "summarize-workspace", "--input", str(resolved_input_path), "--format", "json"
        ),
        "stage_route_report": public_cli_command(
            "stage-route-report", "--input", str(resolved_input_path), "--format", "json"
        ),
        "critique_summary": public_cli_command(
            "critique-summary", "--input", str(resolved_input_path), "--format", "json"
        ),
        "build_direct_entry": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "direct",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
        "build_opl_handoff": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "opl-handoff",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
        "build_submission_ready_package": public_cli_command(
            "build-submission-ready-package",
            "--input",
            str(resolved_input_path),
            "--output-dir",
            "<submission-ready-output-dir>",
            "--format",
            "json",
        ),
    }
