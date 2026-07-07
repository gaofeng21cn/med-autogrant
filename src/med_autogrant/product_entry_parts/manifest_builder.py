from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.action_catalog import (
    annotate_operator_loop_actions_with_catalog_refs,
    build_mag_family_action_catalog,
    project_mag_family_action_catalog,
)
from med_autogrant.domain_entry_contract import (
    build_domain_entry_contract,
    build_user_interaction_contract,
    build_shared_handoff,
)
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.product_entry_parts.autonomy_observability import build_grant_autonomy_observability
from med_autogrant.product_entry_parts.primitives import (
    GRANT_COCKPIT_KIND,
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    PRODUCT_STATUS_KIND,
    PRODUCT_ENTRY_MANIFEST_KIND,
    TARGET_DOMAIN_ID,
    _optional_mapping,
    _optional_string_from_mapping,
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
from med_autogrant.product_entry_parts.orchestration_companions import (
    _build_family_orchestration_companion,
    _build_managed_runtime_contract,
    _build_product_entry_start,
    _route_status_from_route_id,
)
from med_autogrant.product_entry_parts.manifest_readiness import build_manifest_readiness_surfaces
from med_autogrant.product_entry_parts.manifest_owner_receipt_surfaces import (
    build_production_live_acceptance_receipt_surface,
)
from med_autogrant.product_entry_parts.manifest_owner_payload_response import (
    build_manifest_owner_payload_surfaces,
)
from med_autogrant.product_entry_parts.manifest_runtime_companions import build_manifest_runtime_companions
from med_autogrant.product_entry_parts.manifest_runtime_task_surfaces import (
    _build_automation_catalog,
    _build_runtime_inventory,
    _build_task_lifecycle,
)
from med_autogrant.product_entry_parts.manifest_skill_catalog import build_product_entry_skill_catalog
from med_autogrant.product_entry_parts.domain_agent_projection_surfaces import (
    build_artifact_locator_contract,
    build_controlled_soak_no_regression_attempt,
    build_controlled_stage_attempt_projection,
)
from med_autogrant.product_entry_parts.domain_memory import build_manifest_domain_memory_surfaces
from med_autogrant.product_entry_parts.functional_closure import build_manifest_functional_closure_surfaces
from med_autogrant.product_entry_parts.opl_substrate_adapter import build_manifest_opl_substrate_adapter_export
from med_autogrant.product_entry_parts.source_provenance import build_source_provenance_surface
from med_autogrant.product_entry_parts.executor_defaults import build_executor_defaults_surface
from med_autogrant.product_entry_parts.runtime_surfaces import (
    _build_default_runtime_continuity_surfaces,
    _build_product_command_catalog,
    _build_skill_runtime_continuity_envelope,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.runtime_defaults import build_default_runtime_summary
from med_autogrant.stage_control_plane import (
    build_mag_family_stage_control_plane,
    build_mag_grant_transition_oracle,
)
from med_autogrant.temporal_stage_run_consumption import (
    build_temporal_stage_run_consumption_policy,
)
from opl_harness_shared.product_entry_companions import (
    build_operator_loop_action_catalog as _build_shared_operator_loop_action_catalog,
    build_family_product_entry_manifest as _build_shared_family_product_entry_manifest,
    build_product_entry_overview as _build_shared_product_entry_overview,
    build_product_entry_quickstart as _build_shared_product_entry_quickstart,
    build_product_entry_resume_surface as _build_shared_product_entry_resume_surface,
    build_product_entry_shell_catalog as _build_shared_product_entry_shell_catalog,
    build_product_entry_shell_linked_surface as _build_shared_product_entry_shell_linked_surface,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
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
        command_catalog = _build_product_command_catalog(resolved_input_path)
        task_intent_placeholder = "<describe-task-intent>"
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
        base_operator_loop_actions = _build_base_operator_loop_actions(
            command_catalog=command_catalog,
            grant_user_loop_command=grant_user_loop_command,
            grant_cockpit_command=grant_cockpit_command,
            grant_direct_entry_command=grant_direct_entry_command,
        )
        family_action_catalog = build_mag_family_action_catalog(
            action_commands=base_operator_loop_actions,
        )
        family_stage_control_plane = build_mag_family_stage_control_plane(
            family_action_catalog=family_action_catalog,
        )
        grant_transition_oracle = build_mag_grant_transition_oracle(
            family_stage_control_plane=family_stage_control_plane,
            family_action_catalog=family_action_catalog,
        )
        action_catalog_projections = project_mag_family_action_catalog(family_action_catalog)
        operator_loop_actions = annotate_operator_loop_actions_with_catalog_refs(
            operator_loop_actions=base_operator_loop_actions,
            action_catalog=family_action_catalog,
        )
        family_orchestration = _build_manifest_family_orchestration(
            progress_payload=progress_payload,
            progress_projection=progress_projection,
        )
        product_entry_start = _build_product_entry_start(
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
            grant_direct_entry_command=grant_direct_entry_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
        )
        product_entry_quickstart = _build_product_entry_quickstart(
            command_catalog=command_catalog,
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
            grant_cockpit_command=grant_cockpit_command,
            grant_direct_entry_command=grant_direct_entry_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
        )
        product_entry_shell = _build_product_entry_shell(
            command_catalog=command_catalog,
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
            grant_cockpit_command=grant_cockpit_command,
            grant_direct_entry_command=grant_direct_entry_command,
        )
        product_entry_overview = _build_product_entry_overview(
            command_catalog=command_catalog,
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
            product_entry_quickstart=product_entry_quickstart,
            current_focus=current_focus,
            mainline_snapshot=mainline_snapshot,
            workspace_summary=workspace_summary,
        )
        product_entry_surface = _build_shared_product_entry_shell_linked_surface(
            shell_key="product_status",
            shell_surface=product_entry_shell["product_status"],
            summary=(
                "OPL generated/hosted status caller 只读消费 MAG handler refs、user loop、projection 与 handoff。"
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
        human_gate_ids = _collect_family_human_gate_ids(family_orchestration)
        shell_commands = _build_shell_commands(
            product_entry_shell=product_entry_shell,
            command_catalog=command_catalog,
        )
        grant_run_id = _require_nonempty_string_from_mapping(
            progress_payload,
            "grant_run_id",
            context="grant-progress",
        )
        workspace_id = _require_nonempty_string_from_mapping(
            progress_payload,
            "workspace_id",
            context="grant-progress",
        )
        lifecycle_stage = _require_nonempty_string_from_mapping(
            progress_payload,
            "lifecycle_stage",
            context="grant-progress",
        )
        runtime_summary = build_default_runtime_summary(
            current_owner_line=_require_nonempty_string_from_mapping(
                current_line,
                "current_owner_line",
                context="mainline_status.current_line",
            )
        )
        opl_provider_runtime_contract = _build_managed_runtime_contract()
        continuity_surfaces = _build_default_runtime_continuity_surfaces(
            resolved_input_path=resolved_input_path,
            progress_projection=progress_projection,
            workspace_summary=workspace_summary,
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
            grant_user_loop_command=grant_user_loop_command,
            grant_direct_entry_command=grant_direct_entry_command,
        )
        session_continuity = continuity_surfaces["session_continuity"]
        manifest_progress_projection = continuity_surfaces["progress_projection"]
        artifact_inventory = continuity_surfaces["artifact_inventory"]
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
        domain_entry_contract = build_domain_entry_contract()
        user_interaction_contract = build_user_interaction_contract()
        readiness_surfaces = build_manifest_readiness_surfaces(
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
        )
        grant_authoring_readiness = readiness_surfaces["grant_authoring_readiness"]
        product_entry_readiness = readiness_surfaces["product_entry_readiness"]
        runtime_control = continuity_surfaces["runtime_control"]
        runtime_inventory = _build_runtime_inventory(
            resolved_input_path=resolved_input_path,
            progress_payload=progress_payload,
            product_entry_preflight=product_entry_preflight,
            runtime_summary=runtime_summary,
            opl_provider_runtime_contract=opl_provider_runtime_contract,
            checkpoint_status=checkpoint_status,
            repo_mainline=repo_mainline,
        )
        task_lifecycle = _build_task_lifecycle(
            progress_payload=progress_payload,
            checkpoint_status=checkpoint_status,
            grant_user_loop_command=grant_user_loop_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
            human_gate_ids=human_gate_ids,
            continuation_route_id=continuation_route_id,
            continuation_route_status=continuation_route_status,
            continuation_next_action=continuation_next_action,
            continuation_action_kind=continuation_action_kind,
            verification_checkpoint=verification_checkpoint,
            verification_identity=verification_identity,
            repo_mainline=repo_mainline,
        )
        automation = _build_automation_catalog(
            grant_authoring_readiness=grant_authoring_readiness,
            command_catalog=command_catalog,
            grant_user_loop_command=grant_user_loop_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
            human_gate_ids=human_gate_ids,
            continuation_route_id=continuation_route_id,
            continuation_route_status=continuation_route_status,
            continuation_next_action=continuation_next_action,
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
        source_provenance = build_source_provenance_surface()
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
        owner_payload_surfaces = build_manifest_owner_payload_surfaces()
        functional_closure_surfaces = build_manifest_functional_closure_surfaces(
            input_path=resolved_input_path,
            progress_payload=progress_payload,
            verification_identity=verification_identity,
            family_stage_control_plane=family_stage_control_plane,
            runtime_control=runtime_control,
            progress_projection=manifest_progress_projection,
            artifact_locator_contract=artifact_locator_contract,
            controlled_stage_attempt_projection=controlled_stage_attempt_projection,
            domain_memory_surfaces=domain_memory_surfaces,
        )
        standard_domain_agent_skeleton = functional_closure_surfaces["standard_domain_agent_skeleton"]
        skill_catalog = build_product_entry_skill_catalog(
            resolved_input_path=resolved_input_path,
            runtime_summary=runtime_summary,
            runtime_continuity=runtime_continuity,
            shell_commands=shell_commands,
            domain_entry_contract=domain_entry_contract,
            action_catalog_projections=action_catalog_projections,
            standard_domain_agent_skeleton=standard_domain_agent_skeleton,
        )
        opl_substrate_adapter_export = build_manifest_opl_substrate_adapter_export(
            resolved_input_path=resolved_input_path,
            progress_payload=progress_payload,
            verification_identity=verification_identity,
            domain_memory_surfaces=domain_memory_surfaces,
            functional_closure_surfaces=functional_closure_surfaces,
            skill_catalog=skill_catalog,
            runtime_control=runtime_control,
            session_continuity=session_continuity,
            task_lifecycle=task_lifecycle,
            manifest_progress_projection=manifest_progress_projection,
            artifact_inventory=artifact_inventory,
            artifact_locator_contract=artifact_locator_contract,
            controlled_stage_attempt_projection=controlled_stage_attempt_projection,
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
            managed_runtime_contract=None,
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
                "opl_provider_runtime_contract": opl_provider_runtime_contract,
                "family_action_catalog": family_action_catalog,
                "family_stage_control_plane": family_stage_control_plane,
                "grant_transition_oracle": grant_transition_oracle,
                "action_catalog_projections": action_catalog_projections,
                "source_provenance": source_provenance,
                "executor_defaults": build_executor_defaults_surface(),
                "temporal_stage_run_consumption_policy": (
                    build_temporal_stage_run_consumption_policy()
                ),
                "runtime_control": runtime_control,
                "grant_authoring_readiness": grant_authoring_readiness,
                "autonomy_observability": autonomy_observability,
                "artifact_locator_contract": artifact_locator_contract,
                "opl_substrate_adapter_export": opl_substrate_adapter_export,
                "controlled_stage_attempt_projection": controlled_stage_attempt_projection,
                "controlled_soak_no_regression_attempt": build_controlled_soak_no_regression_attempt(),
                "production_live_acceptance_receipt": (
                    build_production_live_acceptance_receipt_surface()
                ),
                **owner_payload_surfaces,
                **domain_memory_surfaces,
                **functional_closure_surfaces,
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


def _build_base_operator_loop_actions(
    *,
    command_catalog: Mapping[str, str],
    grant_user_loop_command: str,
    grant_cockpit_command: str,
    grant_direct_entry_command: str,
) -> dict[str, Any]:
    return _build_shared_operator_loop_action_catalog(
        {
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
        }
    )


def _build_manifest_family_orchestration(
    *,
    progress_payload: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
) -> dict[str, Any]:
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
    orchestration_projection = _require_mapping(
        progress_payload,
        "family_orchestration",
        context="grant-progress",
    )
    return _build_family_orchestration_companion(
        current_route_id=current_route_id,
        recommended_route_id=recommended_route_id,
        recommended_route_status=_route_status_from_route_id(recommended_route_id),
        needs_author_decision=bool(progress_projection.get("needs_author_decision")),
        intake_evidence_companion=_optional_mapping(
            orchestration_projection,
            "intake_evidence_companion",
        ),
        project_profile_companion=_optional_mapping(
            orchestration_projection,
            "project_profile_companion",
        ),
        review_surface_ref="/product_entry_manifest/operator_loop_surface",
        event_envelope_surface_ref="/product_entry_manifest/recommended_command",
        checkpoint_lineage_surface_ref="/product_entry_manifest/repo_mainline/active_phase",
        resume_surface_kind=GRANT_USER_LOOP_KIND,
    )


def _build_product_entry_quickstart(
    *,
    command_catalog: Mapping[str, str],
    product_status_command: str,
    grant_user_loop_command: str,
    grant_cockpit_command: str,
    grant_direct_entry_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
) -> dict[str, Any]:
    return _build_shared_product_entry_quickstart(
        summary=(
            "先从 OPL-hosted grant status caller 进入 MAG domain handler target，"
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


def _build_product_entry_overview(
    *,
    command_catalog: Mapping[str, str],
    product_status_command: str,
    grant_user_loop_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
    product_entry_quickstart: Mapping[str, Any],
    current_focus: Mapping[str, Any],
    mainline_snapshot: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
) -> dict[str, Any]:
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
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
        context="summarize-workspace",
    )
    product_entry_overview.update(
        {
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
        }
    )
    return product_entry_overview


def _build_product_entry_shell(
    *,
    command_catalog: Mapping[str, str],
    product_status_command: str,
    grant_user_loop_command: str,
    grant_cockpit_command: str,
    grant_direct_entry_command: str,
) -> dict[str, Any]:
    return _build_shared_product_entry_shell_catalog(
        {
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
        }
    )


def _build_shell_commands(
    *,
    product_entry_shell: Mapping[str, Mapping[str, Any]],
    command_catalog: Mapping[str, str],
) -> dict[str, str]:
    return {
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
        "domain_memory_receipt_evidence": command_catalog["domain_memory_receipt_evidence"],
    }
