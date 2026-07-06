from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.codex_stage_receipts import (
    build_codex_stage_execution_receipt_bundle,
)
from med_autogrant.product_entry_parts.conflict_envelopes import (
    build_opl_conflict_or_blocker_envelope,
)
from med_autogrant.product_entry_parts.continuous_reconciliation import (
    build_continuous_receipt_reconciliation_snapshot,
)
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
    build_executor_first_closeout_bundle,
)
from med_autogrant.product_entry_parts.external_evidence_ledger import (
    build_external_evidence_consumption_ledger,
)
from med_autogrant.product_entry_parts.hosted_receipt_verification import (
    build_focused_hosted_receipt_verification,
)
from med_autogrant.product_entry_parts.manifest_sustained_consumption_payload import (
    build_manifest_sustained_consumption_payload_response,
)
from med_autogrant.product_entry_parts.operator_closeout import (
    build_operator_closeout_readiness_projection,
)
from med_autogrant.product_entry_parts.opl_owner_payload_response import (
    build_opl_owner_payload_response,
)
from med_autogrant.product_entry_parts.owner_receipt_reconciliation import (
    build_controlled_soak_receipt_reconciliation_inventory,
    build_controlled_soak_receipt_reconciliation_proof,
)
from med_autogrant.product_entry_parts.owner_receipt_writers import (
    write_lifecycle_receipt_evidence,
    write_owner_receipt_evidence,
)
from med_autogrant.product_entry_parts.physical_morphology_guard import (
    build_physical_morphology_guard_projection,
)
from med_autogrant.product_entry_parts.production_live_acceptance import (
    build_production_live_acceptance_receipt_projection,
)
from med_autogrant.product_entry_parts.receipt_observability import (
    build_controlled_soak_receipt_observability_summary,
)
from med_autogrant.product_entry_parts.stage_attempt_observability import (
    build_stage_attempt_observability_projection,
)


class ProductEntryEvidenceMixin:
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
