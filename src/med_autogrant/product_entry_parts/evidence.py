from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.codex_stage_receipts import (
    build_codex_stage_execution_receipt_bundle,
)
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
    build_executor_first_closeout_bundle,
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
