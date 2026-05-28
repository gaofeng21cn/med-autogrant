from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.product_entry_parts.orchestration_companions import _build_managed_runtime_contract
from med_autogrant.product_entry_parts.primitives import (
    PRODUCT_ENTRY_KIND,
    PRODUCT_ENTRY_VERSION,
    SUPPORTED_ENTRY_MODES,
    TARGET_DOMAIN_ID,
    _read_funding_call_from_summary,
    _require_entry_mode,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
    _require_optional_string,
    _write_product_entry_output,
)
from med_autogrant.product_entry_parts.runtime_contracts import (
    PRODUCT_ENTRY_SCHEMA_FILE,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.product_entry_parts.runtime_surfaces import (
    DOMAIN_AUTHORITY_SURFACE_REF,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
    _build_product_command_catalog,
    _build_runtime_continuity_surfaces,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.runtime_defaults import build_default_runtime_summary
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.product_entry_parts.domain_entry_loader import build_default_domain_entry
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from med_autogrant.product_entry_parts.owner_receipt_reconciliation import (
    build_controlled_soak_receipt_reconciliation_inventory,
    build_controlled_soak_receipt_reconciliation_proof,
)
from med_autogrant.product_entry_parts.owner_receipt_writers import (
    write_lifecycle_receipt_evidence,
    write_owner_receipt_evidence,
)
from med_autogrant.product_entry_parts.production_live_acceptance import (
    build_production_live_acceptance_receipt_projection,
)
from med_autogrant.product_entry_parts.conflict_envelopes import build_opl_conflict_or_blocker_envelope
from med_autogrant.product_entry_parts.receipt_observability import (
    build_controlled_soak_receipt_observability_summary,
)
from med_autogrant.product_entry_parts.stage_attempt_observability import (
    build_stage_attempt_observability_projection,
)
from med_autogrant.product_entry_parts.hosted_receipt_verification import (
    build_focused_hosted_receipt_verification,
)
from med_autogrant.product_entry_parts.continuous_reconciliation import (
    build_continuous_receipt_reconciliation_snapshot,
)
from med_autogrant.product_entry_parts.lifecycle_receipt_bundle import (
    build_lifecycle_receipt_bundle,
)
from med_autogrant.product_entry_parts.memory_receipt_projection import (
    build_memory_receipt_read_projection,
)
from med_autogrant.product_entry_parts.external_evidence_ledger import (
    build_external_evidence_consumption_ledger,
)
from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
    build_package_lifecycle_handoff_projection,
)
from med_autogrant.product_entry_parts.receipt_readiness import (
    build_receipt_readiness_projection,
)
from med_autogrant.product_entry_parts.codex_stage_receipts import (
    build_codex_stage_execution_receipt_bundle,
)
from med_autogrant.product_entry_parts.operator_closeout import (
    build_operator_closeout_readiness_projection,
)
from med_autogrant.product_entry_parts.opl_owner_payload_response import (
    build_opl_owner_payload_response,
)
from med_autogrant.product_entry_parts.manifest_sustained_consumption_payload import (
    build_manifest_sustained_consumption_payload_response,
)
from med_autogrant.product_entry_parts.physical_morphology_guard import (
    build_physical_morphology_guard_projection,
)
from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
    build_executor_first_closeout_bundle,
)
from med_autogrant.product_entry_parts.progress import ProductEntryProgressMixin
from med_autogrant.product_entry_parts.manifest import ProductEntryManifestMixin
from med_autogrant.product_entry_parts.preflight import ProductEntryPreflightMixin
from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export, dispatch_domain_handler_task


class MedAutoGrantProductEntry(ProductEntryProgressMixin, ProductEntryManifestMixin, ProductEntryPreflightMixin):
    """轻量 grant product entry 壳，复用已 landed 的 domain entry 与默认 runtime contract。"""

    def __init__(self, *, domain_entry: Any | None = None) -> None:
        self._domain_entry = domain_entry or build_default_domain_entry()

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
        command_catalog = _build_product_command_catalog(resolved_input_path)
        progress_payload = self.read_grant_progress(input_path=resolved_input_path)
        progress_projection = _require_mapping(
            progress_payload,
            "progress_projection",
            context="build-product-entry.grant_progress",
        )
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
        continuity_surfaces = _build_runtime_continuity_surfaces(
            progress_projection=progress_projection,
            workspace_summary=workspace_summary,
            runtime_summary=runtime_summary,
            managed_runtime_contract=_build_managed_runtime_contract(),
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
            input_path=str(resolved_input_path),
            funding_call=resolved_funding_call,
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
                "session_owner": "one-person-lab",
                "generated_session_surface_ref": GENERATED_SESSION_SURFACE_REF,
                "generated_resume_surface_ref": GENERATED_SESSION_RESUME_SURFACE_REF,
                "domain_authority_surface_ref": DOMAIN_AUTHORITY_SURFACE_REF,
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
                "session_continuity": dict(continuity_surfaces["session_continuity"]),
                "progress_projection": dict(continuity_surfaces["progress_projection"]),
                "artifact_inventory": dict(continuity_surfaces["artifact_inventory"]),
                "runtime_control": dict(continuity_surfaces["runtime_control"]),
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

    def build_domain_handler_export(self, *, input_path: str | Path) -> dict[str, Any]:
        return build_domain_handler_export(self, input_path=input_path)

    def dispatch_domain_handler_task(self, *, task_path: str | Path) -> dict[str, Any]:
        return dispatch_domain_handler_task(self, task_path=task_path)

    def build_domain_memory_writeback_proposal(
        self,
        *,
        input_path: str | Path,
        stage_id: str,
        source_ref: str,
        lesson_summary: str,
        proposal_id: str | None = None,
    ) -> dict[str, Any]:
        return build_domain_memory_writeback_proposal(
            input_path=input_path,
            stage_id=stage_id,
            source_ref=source_ref,
            lesson_summary=lesson_summary,
            proposal_id=proposal_id,
        )

    def build_domain_memory_writeback_decision(
        self,
        *,
        proposal_path: str | Path,
        decision: str,
        decision_reason: str,
        memory_id: str | None = None,
    ) -> dict[str, Any]:
        return build_domain_memory_writeback_decision(
            proposal_path=proposal_path,
            decision=decision,
            decision_reason=decision_reason,
            memory_id=memory_id,
        )

    def write_domain_memory_receipt_evidence(
        self,
        *,
        decision_payload: str | Path | dict[str, Any],
        runtime_root: str | Path | None = None,
    ) -> dict[str, Any]:
        return write_domain_memory_receipt_evidence(
            decision_payload=decision_payload,
            runtime_root=runtime_root,
        )

    def write_owner_receipt_evidence(
        self,
        *,
        input_path: str | Path,
        receipt_shape: str,
        stage_id: str,
        source_ref: str,
        closeout_summary: str,
        runtime_root: str | Path | None = None,
        receipt_id: str | None = None,
        closeout_refs: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return write_owner_receipt_evidence(
            input_path=input_path,
            receipt_shape=receipt_shape,
            stage_id=stage_id,
            source_ref=source_ref,
            closeout_summary=closeout_summary,
            runtime_root=runtime_root,
            receipt_id=receipt_id,
            closeout_refs=closeout_refs,
        )

    def write_lifecycle_receipt_evidence(
        self,
        *,
        input_path: str | Path,
        operation: str,
        receipt_shape: str,
        source_ref: str,
        closeout_summary: str,
        runtime_root: str | Path | None = None,
        receipt_id: str | None = None,
    ) -> dict[str, Any]:
        return write_lifecycle_receipt_evidence(
            input_path=input_path,
            operation=operation,
            receipt_shape=receipt_shape,
            source_ref=source_ref,
            closeout_summary=closeout_summary,
            runtime_root=runtime_root,
            receipt_id=receipt_id,
        )

    def build_controlled_soak_receipt_reconciliation_proof(
        self,
        *,
        owner_receipt_evidence: Mapping[str, Any],
        opl_ledger_ref: str,
        domain_handler_closeout_result: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_controlled_soak_receipt_reconciliation_proof(
            owner_receipt_evidence=owner_receipt_evidence,
            opl_ledger_ref=opl_ledger_ref,
            domain_handler_closeout_result=domain_handler_closeout_result,
        )

    def build_controlled_soak_receipt_reconciliation_inventory(
        self,
        *,
        owner_receipt_evidence_items: list[Mapping[str, Any]],
        opl_ledger_ref: str,
        domain_handler_closeout_results: list[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return build_controlled_soak_receipt_reconciliation_inventory(
            owner_receipt_evidence_items=owner_receipt_evidence_items,
            opl_ledger_ref=opl_ledger_ref,
            domain_handler_closeout_results=domain_handler_closeout_results,
        )

    def build_production_live_acceptance_receipt_projection(
        self,
        *,
        owner_receipt_evidence: Mapping[str, Any],
        agent_lab_suite_result: Mapping[str, Any],
        meta_agent_coordination_result: Mapping[str, Any],
    ) -> dict[str, Any]:
        return build_production_live_acceptance_receipt_projection(
            owner_receipt_evidence=owner_receipt_evidence,
            agent_lab_suite_result=agent_lab_suite_result,
            meta_agent_coordination_result=meta_agent_coordination_result,
        )

    def build_controlled_soak_receipt_observability_summary(
        self,
        *,
        receipt_reconciliation_inventory: Mapping[str, Any],
    ) -> dict[str, Any]:
        return build_controlled_soak_receipt_observability_summary(
            receipt_reconciliation_inventory=receipt_reconciliation_inventory,
        )

    def build_stage_attempt_observability_projection(
        self,
        *,
        controlled_stage_attempt_projection: Mapping[str, Any],
        receipt_reconciliation_inventory: Mapping[str, Any],
        opl_usage_projection_ref: str,
        opl_control_loop_projection_ref: str,
    ) -> dict[str, Any]:
        return build_stage_attempt_observability_projection(
            controlled_stage_attempt_projection=controlled_stage_attempt_projection,
            receipt_reconciliation_inventory=receipt_reconciliation_inventory,
            opl_usage_projection_ref=opl_usage_projection_ref,
            opl_control_loop_projection_ref=opl_control_loop_projection_ref,
        )

    def build_opl_conflict_or_blocker_envelope(
        self,
        payload: Mapping[str, Any] | None = None,
        *,
        classification: str | None = None,
        severity: str | None = None,
        owner_receipt: Mapping[str, Any] | None = None,
        typed_blocker: Mapping[str, Any] | None = None,
        no_regression_evidence: Mapping[str, Any] | None = None,
        source_refs: list[str] | tuple[str, ...] | None = None,
        receipt_refs: Mapping[str, Any] | None = None,
        verdict_refs: Mapping[str, Any] | None = None,
        safe_action_refs: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_opl_conflict_or_blocker_envelope(
            payload,
            classification=classification,
            severity=severity,
            owner_receipt=owner_receipt,
            typed_blocker=typed_blocker,
            no_regression_evidence=no_regression_evidence,
            source_refs=source_refs,
            receipt_refs=receipt_refs,
            verdict_refs=verdict_refs,
            safe_action_refs=safe_action_refs,
        )

    def build_focused_hosted_receipt_verification(
        self,
        *,
        owner_receipt_evidence: Mapping[str, Any],
        opl_attempt_evidence: Mapping[str, Any],
        domain_handler_closeout_result: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_focused_hosted_receipt_verification(
            owner_receipt_evidence=owner_receipt_evidence,
            opl_attempt_evidence=opl_attempt_evidence,
            domain_handler_closeout_result=domain_handler_closeout_result,
        )

    def build_lifecycle_receipt_bundle(
        self,
        *,
        lifecycle_receipt_evidence_items: list[Mapping[str, Any]],
    ) -> dict[str, Any]:
        return build_lifecycle_receipt_bundle(
            lifecycle_receipt_evidence_items=lifecycle_receipt_evidence_items,
        )

    def build_memory_receipt_read_projection(
        self,
        *,
        receipt_items: list[Mapping[str, Any]],
    ) -> dict[str, Any]:
        return build_memory_receipt_read_projection(receipt_items)

    def build_external_evidence_consumption_ledger(
        self,
        *,
        external_evidence_request_pack: Mapping[str, Any],
        evidence_receipts: list[Mapping[str, Any]],
    ) -> dict[str, Any]:
        return build_external_evidence_consumption_ledger(
            external_evidence_request_pack=external_evidence_request_pack,
            evidence_receipts=evidence_receipts,
        )

    def build_package_lifecycle_handoff_projection(
        self,
        *,
        package_refs: Mapping[str, Any],
        gap_report: Mapping[str, Any],
        export_verdict: Mapping[str, Any],
        manual_portal_boundary: Mapping[str, Any],
        lifecycle_receipt_refs: Mapping[str, Any],
    ) -> dict[str, Any]:
        return build_package_lifecycle_handoff_projection(
            package_refs=package_refs,
            gap_report=gap_report,
            export_verdict=export_verdict,
            manual_portal_boundary=manual_portal_boundary,
            lifecycle_receipt_refs=lifecycle_receipt_refs,
        )

    def build_receipt_readiness_projection(
        self,
        *,
        owner_receipt_evidence_items: list[Mapping[str, Any]],
        memory_receipt_items: list[Mapping[str, Any]],
        package_lifecycle_items: list[Mapping[str, Any]],
        lifecycle_receipt_items: list[Mapping[str, Any]],
    ) -> dict[str, Any]:
        return build_receipt_readiness_projection(
            owner_receipt_evidence_items=owner_receipt_evidence_items,
            memory_receipt_items=memory_receipt_items,
            package_lifecycle_items=package_lifecycle_items,
            lifecycle_receipt_items=lifecycle_receipt_items,
        )

    def build_codex_stage_execution_receipt_bundle(
        self,
        *,
        stage_id: str,
        execution_attempts: list[Mapping[str, Any]],
        review_attempts: list[Mapping[str, Any]],
    ) -> dict[str, Any]:
        return build_codex_stage_execution_receipt_bundle(
            stage_id=stage_id,
            execution_attempts=execution_attempts,
            review_attempts=review_attempts,
        )

    def build_operator_closeout_readiness_projection(
        self,
        *,
        production_acceptance: Mapping[str, Any],
        external_evidence_receipt_ledger: Mapping[str, Any],
        receipt_readiness_projection: Mapping[str, Any],
    ) -> dict[str, Any]:
        return build_operator_closeout_readiness_projection(
            production_acceptance=production_acceptance,
            external_evidence_receipt_ledger=external_evidence_receipt_ledger,
            receipt_readiness_projection=receipt_readiness_projection,
        )

    def build_opl_owner_payload_response(
        self,
        *,
        production_acceptance: Mapping[str, Any],
        external_evidence_receipt_ledger: Mapping[str, Any],
        receipt_readiness_projection: Mapping[str, Any],
    ) -> dict[str, Any]:
        return build_opl_owner_payload_response(
            production_acceptance=production_acceptance,
            external_evidence_receipt_ledger=external_evidence_receipt_ledger,
            receipt_readiness_projection=receipt_readiness_projection,
        )

    def build_manifest_sustained_consumption_payload_response(
        self,
        *,
        owner_payload_response: Mapping[str, Any],
        workspace_receipt_scaleout_evidence: Mapping[str, Any],
        operator_payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        return build_manifest_sustained_consumption_payload_response(
            owner_payload_response=owner_payload_response,
            workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
            operator_payload=operator_payload,
        )

    def build_physical_morphology_guard_projection(
        self,
        *,
        source_items: list[Mapping[str, Any]],
        external_evidence_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        return build_physical_morphology_guard_projection(
            source_items=source_items,
            external_evidence_refs=external_evidence_refs,
        )

    def build_executor_first_closeout_bundle(
        self,
        *,
        codex_stage_execution_receipt_bundle: Mapping[str, Any],
        operator_closeout_readiness_projection: Mapping[str, Any],
        physical_morphology_guard_projection: Mapping[str, Any],
        external_evidence_consumption_ledger: Mapping[str, Any] | None = None,
        receipt_readiness_projection: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_executor_first_closeout_bundle(
            codex_stage_execution_receipt_bundle=codex_stage_execution_receipt_bundle,
            operator_closeout_readiness_projection=operator_closeout_readiness_projection,
            physical_morphology_guard_projection=physical_morphology_guard_projection,
            external_evidence_consumption_ledger=external_evidence_consumption_ledger,
            receipt_readiness_projection=receipt_readiness_projection,
        )

    def build_continuous_receipt_reconciliation_snapshot(
        self,
        *,
        focused_hosted_receipt_verification_items: list[Mapping[str, Any]],
        receipt_reconciliation_inventory: Mapping[str, Any],
        receipt_observability_summary: Mapping[str, Any] | None = None,
        stage_attempt_observability_projection: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_continuous_receipt_reconciliation_snapshot(
            focused_hosted_receipt_verification_items=focused_hosted_receipt_verification_items,
            receipt_reconciliation_inventory=receipt_reconciliation_inventory,
            receipt_observability_summary=receipt_observability_summary,
            stage_attempt_observability_projection=stage_attempt_observability_projection,
        )
