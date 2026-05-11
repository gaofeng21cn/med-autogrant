from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.domain_entry_contract import (
    build_domain_entry_contract,
    build_user_interaction_contract,
    build_shared_handoff,
)
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.action_catalog import (
    annotate_operator_loop_actions_with_catalog_refs,
    build_mag_family_action_catalog,
    project_mag_family_action_catalog,
)
from med_autogrant.stage_control_plane import build_mag_family_stage_control_plane
from med_autogrant.product_entry_parts.autonomy_observability import build_grant_autonomy_observability
from med_autogrant.product_entry_parts.orchestration_companions import (
    _build_family_orchestration_companion,
    _build_managed_runtime_contract,
    _build_product_entry_start,
    _route_status_from_route_id,
)
from med_autogrant.product_entry_parts.primitives import (
    GRANT_COCKPIT_KIND,
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    PRODUCT_ENTRY_MANIFEST_KIND,
    PRODUCT_STATUS_KIND,
    TARGET_DOMAIN_ID,
    _optional_mapping,
    _optional_string_from_mapping,
    _read_funding_call_from_summary,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.runtime_contracts import (
    PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
    _build_author_side_route_contract,
)
from med_autogrant.product_entry_parts.loop_contracts import (
    _build_mainline_snapshot,
    _build_next_action_payload,
    _validate_product_entry_manifest_contract,
)
from med_autogrant.product_entry_parts.manifest_readiness import build_manifest_readiness_surfaces
from med_autogrant.product_entry_parts.manifest_runtime_companions import build_manifest_runtime_companions
from med_autogrant.product_entry_parts.manifest_skill_catalog import build_product_entry_skill_catalog
from med_autogrant.product_entry_parts.domain_agent_skeleton import build_artifact_locator_contract, build_controlled_stage_attempt_projection, build_domain_agent_skeleton_mapping
from med_autogrant.product_entry_parts.domain_memory import build_manifest_domain_memory_surfaces
from med_autogrant.product_entry_parts.runtime_surfaces import (
    _build_artifact_inventory_surface,
    _build_product_command_catalog,
    _build_progress_projection_surface,
    _build_runtime_control_surface,
    _build_session_continuity_surface,
    _build_skill_runtime_continuity_envelope,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.runtime_defaults import DEFAULT_RUNTIME_SUBSTRATE, build_default_runtime_summary

from opl_harness_shared.automation_companions import (
    build_automation_catalog as _build_shared_automation_catalog,
    build_automation_descriptor as _build_shared_automation_descriptor,
)
from opl_harness_shared.product_entry_companions import (
    build_family_product_entry_manifest as _build_shared_family_product_entry_manifest,
    build_operator_loop_action_catalog as _build_shared_operator_loop_action_catalog,
    build_product_entry_overview as _build_shared_product_entry_overview,
    build_product_entry_quickstart as _build_shared_product_entry_quickstart,
    build_product_entry_readiness as _build_shared_product_entry_readiness,
    build_product_entry_resume_surface as _build_shared_product_entry_resume_surface,
    build_product_entry_shell_catalog as _build_shared_product_entry_shell_catalog,
    build_product_entry_shell_linked_surface as _build_shared_product_entry_shell_linked_surface,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
)
from opl_harness_shared.runtime_task_companions import (
    build_runtime_inventory as _build_shared_runtime_inventory,
    build_task_lifecycle as _build_shared_task_lifecycle,
)


class ProductEntryManifestBuilderMixin:
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
        product_status_command = public_cli_command(
            "product-status", "--input", str(resolved_input_path), "--format", "json"
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
        base_operator_loop_actions = _build_shared_operator_loop_action_catalog({
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
        family_action_catalog = build_mag_family_action_catalog(
            action_commands=base_operator_loop_actions,
        )
        family_stage_control_plane = build_mag_family_stage_control_plane(
            family_action_catalog=family_action_catalog,
        )
        action_catalog_projections = project_mag_family_action_catalog(family_action_catalog)
        operator_loop_actions = annotate_operator_loop_actions_with_catalog_refs(
            operator_loop_actions=base_operator_loop_actions,
            action_catalog=family_action_catalog,
        )
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
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
            grant_direct_entry_command=grant_direct_entry_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
        )
        product_entry_quickstart = _build_shared_product_entry_quickstart(
            summary=(
                "先从 direct grant product status 进入当前 product entry surface，"
                "再回到 grant-user-loop，必要时读取 progress 或 cockpit projection。"
            ),
            recommended_step_id="open_product_entry",
            steps=[
                {
                    "step_id": "open_product_entry",
                    "title": "Open grant status",
                    "command": product_status_command,
                    "surface_kind": PRODUCT_STATUS_KIND,
                    "summary": "打开当前 direct grant product entry surface。",
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
            product_entry_command=product_status_command,
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
        runtime_summary = build_default_runtime_summary(
            current_owner_line=_require_nonempty_string_from_mapping(
                current_line,
                "current_owner_line",
                context="mainline_status.current_line",
            )
        )
        managed_runtime_contract = _build_managed_runtime_contract()
        product_entry_shell = _build_shared_product_entry_shell_catalog({
            "product_status": {
                "command": product_status_command,
                "surface_kind": PRODUCT_STATUS_KIND,
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
        product_entry_surface = _build_shared_product_entry_shell_linked_surface(
            shell_key="product_status",
            shell_surface=product_entry_shell["product_status"],
            summary=(
                "当前 direct grant product status 先暴露前台入口、user loop、projection 与 shared handoff。"
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
        user_interaction_contract = build_user_interaction_contract()
        readiness_surfaces = build_manifest_readiness_surfaces(
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
        )
        grant_authoring_readiness = readiness_surfaces["grant_authoring_readiness"]
        product_entry_readiness = readiness_surfaces["product_entry_readiness"]
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
            funding_call=_read_funding_call_from_summary(workspace_summary),
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
            substrate=DEFAULT_RUNTIME_SUBSTRATE,
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
        runtime_companions = build_manifest_runtime_companions(
            progress_payload=progress_payload,
            checkpoint_status=checkpoint_status,
            continuation_route_id=continuation_route_id,
            continuation_route_status=continuation_route_status,
            grant_user_loop_command=grant_user_loop_command,
        )
        runtime_continuity = _build_skill_runtime_continuity_envelope(
            session_continuity=session_continuity,
            progress_surface=manifest_progress_projection,
            artifact_inventory=artifact_inventory,
            runtime_control=runtime_control,
        )
        shell_commands = {
            "product_status": _require_nonempty_string_from_mapping(
                product_entry_shell["product_status"],
                "command",
                context="product_entry_shell.product_status",
            ),
            "grant_progress": _require_nonempty_string_from_mapping(
                product_entry_shell["grant_progress"],
                "command",
                context="product_entry_shell.grant_progress",
            ),
            "grant_cockpit": _require_nonempty_string_from_mapping(
                product_entry_shell["grant_cockpit"],
                "command",
                context="product_entry_shell.grant_cockpit",
            ),
            "grant_direct_entry": _require_nonempty_string_from_mapping(
                product_entry_shell["grant_direct_entry"],
                "command",
                context="product_entry_shell.grant_direct_entry",
            ),
            "grant_user_loop": _require_nonempty_string_from_mapping(
                product_entry_shell["grant_user_loop"],
                "command",
                context="product_entry_shell.grant_user_loop",
            ),
            "domain_memory_writeback_proposal": command_catalog["domain_memory_writeback_proposal"],
            "domain_memory_writeback_decision": command_catalog["domain_memory_writeback_decision"],
        }
        artifact_locator_contract = build_artifact_locator_contract(
            input_path=resolved_input_path,
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
            draft_id=_optional_string_from_mapping(verification_identity, "draft_id"),
            lifecycle_stage=_require_nonempty_string_from_mapping(
                progress_payload,
                "lifecycle_stage",
                context="grant-progress",
            ),
            artifact_inventory=artifact_inventory,
        )
        controlled_stage_attempt_projection = build_controlled_stage_attempt_projection(
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
            draft_id=_optional_string_from_mapping(verification_identity, "draft_id"),
            lifecycle_stage=_require_nonempty_string_from_mapping(
                progress_payload,
                "lifecycle_stage",
                context="grant-progress",
            ),
            progress_projection=manifest_progress_projection,
            task_lifecycle=task_lifecycle,
        )
        domain_memory_surfaces = build_manifest_domain_memory_surfaces(
            progress_payload=progress_payload, verification_identity=verification_identity
        )
        domain_memory_descriptor_locator = domain_memory_surfaces["domain_memory_descriptor_locator"]
        domain_agent_skeleton_mapping = build_domain_agent_skeleton_mapping(
            input_path=resolved_input_path,
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
            draft_id=_optional_string_from_mapping(verification_identity, "draft_id"),
            lifecycle_stage=_require_nonempty_string_from_mapping(
                progress_payload,
                "lifecycle_stage",
                context="grant-progress",
            ),
            family_stage_control_plane=family_stage_control_plane,
            runtime_control=runtime_control,
            progress_projection=manifest_progress_projection,
            artifact_locator_contract=artifact_locator_contract,
            controlled_stage_attempt_projection=controlled_stage_attempt_projection,
            domain_memory_descriptor_locator=domain_memory_descriptor_locator,
        )
        skill_catalog = build_product_entry_skill_catalog(
            resolved_input_path=resolved_input_path,
            runtime_summary=runtime_summary,
            runtime_continuity=runtime_continuity,
            shell_commands=shell_commands,
            domain_entry_contract=domain_entry_contract,
            action_catalog_projections=action_catalog_projections,
            domain_agent_skeleton_mapping=domain_agent_skeleton_mapping,
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
        autonomy_observability = build_grant_autonomy_observability(
            task_lifecycle=task_lifecycle,
            runtime_inventory=runtime_inventory,
            grant_authoring_readiness=grant_authoring_readiness,
            runtime_control=runtime_control,
            remaining_gaps=list(mainline_payload.get("remaining_gaps") or []),
        )

        product_entry_manifest = _build_shared_family_product_entry_manifest(
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
            product_entry_surface=product_entry_surface,
            operator_loop_surface=operator_loop_surface,
            operator_loop_actions=operator_loop_actions,
            repo_mainline=repo_mainline,
            runtime=runtime_summary,
            managed_runtime_contract=managed_runtime_contract,
            runtime_inventory=runtime_inventory,
            task_lifecycle=task_lifecycle,
            persistence_policy=runtime_companions["persistence_policy"],
            lifecycle_ledger=runtime_companions["lifecycle_ledger"],
            owner_route=runtime_companions["owner_route"],
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
            user_interaction_contract=user_interaction_contract,
            extra_payload={
                "family_action_catalog": family_action_catalog,
                "family_stage_control_plane": family_stage_control_plane,
                "action_catalog_projections": action_catalog_projections,
                "runtime_control": runtime_control,
                "grant_authoring_readiness": grant_authoring_readiness,
                "autonomy_observability": autonomy_observability,
                "artifact_locator_contract": artifact_locator_contract,
                "controlled_stage_attempt_projection": controlled_stage_attempt_projection,
                **domain_memory_surfaces,
                "domain_agent_skeleton_mapping": domain_agent_skeleton_mapping,
            },
        )
        payload = {
            "ok": True,
            "command": "product-entry-manifest",
            "grant_run_id": progress_payload["grant_run_id"],
            "workspace_id": progress_payload["workspace_id"],
            "draft_id": progress_payload["draft_id"],
            "lifecycle_stage": progress_payload["lifecycle_stage"],
            "input_path": progress_payload["input_path"],
            "product_entry_manifest": product_entry_manifest,
        }
        _validate_product_entry_manifest_contract(
            payload,
            grant_run_id=progress_payload["grant_run_id"],
            workspace_id=progress_payload["workspace_id"],
            lifecycle_stage=progress_payload["lifecycle_stage"],
        )
        return payload
