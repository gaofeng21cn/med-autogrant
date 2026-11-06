from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from opl_framework.json_io import write_json_object_atomic

from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _read_json_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.workspace_types import WorkspaceStateError


DOMAIN_MEMORY_WRITEBACK_PROPOSAL_KIND = "mag_domain_memory_writeback_proposal"
DOMAIN_MEMORY_WRITEBACK_DECISION_KIND = "mag_domain_memory_writeback_decision"
DOMAIN_MEMORY_OPERATOR_RECEIPT_PROJECTION_KIND = "mag_domain_memory_operator_receipt_projection"
DOMAIN_MEMORY_RUNTIME_RECEIPT_EVIDENCE_KIND = "mag_domain_memory_runtime_receipt_evidence"
DOMAIN_MEMORY_POLICY_REF = "docs/references/grant_strategy_memory_policy.md"

STAGE_IDS = (
    "call_and_candidate_intake",
    "fundability_strategy",
    "specific_aims_and_structure",
    "proposal_authoring",
    "review_and_rebuttal",
    "package_and_submit_ready",
)

def build_domain_memory_writeback_proposal(
    *,
    input_path: str | Path,
    workspace_root: str | Path,
    project_root: str | Path,
    stage_id: str,
    lesson_summary: str,
    source_ref: str,
    proposal_id: str | None = None,
) -> dict[str, Any]:
    resolved_stage_id = _require_stage_id(stage_id)
    resolved_lesson_summary = _require_nonempty_string(lesson_summary, field_name="lesson_summary")
    resolved_source_ref = _require_nonempty_string(source_ref, field_name="source_ref")
    resolved_input_path = Path(input_path).expanduser().resolve()
    resolved_proposal_id = _safe_id(proposal_id or f"{resolved_stage_id}-writeback-proposal")
    scope = _project_scope(workspace_root, project_root)
    proposal = {
        "surface_kind": DOMAIN_MEMORY_WRITEBACK_PROPOSAL_KIND,
        "proposal_id": _require_nonempty_string(resolved_proposal_id, field_name="proposal_id"),
        "target_domain_id": TARGET_DOMAIN_ID,
        "decision_owner": TARGET_DOMAIN_ID,
        "stage_id": resolved_stage_id,
        "memory_role": "strategy_context",
        "policy_ref": DOMAIN_MEMORY_POLICY_REF,
        "catalog_ref": "memory/opl_durable_knowledge_catalog.json",
        "target_layer": "workspace_project",
        "target_scope": scope,
        "stage_descriptor_ref": _stage_descriptor_ref(resolved_stage_id),
        "source_locator": {
            "locator_kind": "workspace_or_runtime_ref",
            "workspace_path": str(resolved_input_path),
            "source_ref": resolved_source_ref,
            "repo_tracked": False,
        },
        "lesson_summary": resolved_lesson_summary,
        "write_policy": "owner_decision_then_project_markdown_and_opl_catalog",
        "proposal_ref": f"memory/proposals/{resolved_proposal_id}.json",
        "decision_receipt_ref": f"receipts/domain-memory/{resolved_proposal_id}.json",
        "authority_boundary": _memory_authority_boundary(),
    }
    return {
        "ok": True,
        "command": "domain-memory-writeback-proposal",
        "input_path": str(resolved_input_path),
        "domain_memory_writeback_proposal": proposal,
    }


def build_domain_memory_writeback_decision(
    *,
    proposal_path: str | Path,
    decision: str,
    decision_reason: str,
    memory_id: str | None = None,
) -> dict[str, Any]:
    proposal = _read_json_mapping(Path(proposal_path).expanduser().resolve(), context="domain_memory_writeback_proposal")
    proposal_body = _require_proposal_body(proposal)
    resolved_decision = _require_decision(decision)
    proposal_id = _require_nonempty_string_from_mapping(
        proposal_body,
        "proposal_id",
        context="domain_memory_writeback_proposal",
    )
    stage_id = _require_stage_id(
        _require_nonempty_string_from_mapping(
            proposal_body,
            "stage_id",
            context="domain_memory_writeback_proposal",
        )
    )
    resolved_reason = _require_nonempty_string(decision_reason, field_name="decision_reason")
    proposal_id = _safe_id(proposal_id)
    resolved_memory_id = _safe_id(memory_id or proposal_id)
    target_scope = proposal_body.get("target_scope")
    if not isinstance(target_scope, Mapping) or proposal_body.get("target_layer") != "workspace_project":
        raise WorkspaceStateError("domain memory proposal requires an explicit project scope.")
    scope = _project_scope(target_scope.get("workspace_root"), target_scope.get("project_root"))
    accepted_memory_ref = f"memory/{resolved_memory_id}.md"
    decision_receipt_ref = f"receipts/domain-memory/{proposal_id}.json"
    rejected_memory_ref = decision_receipt_ref
    receipt_projection = {
        "surface_kind": DOMAIN_MEMORY_OPERATOR_RECEIPT_PROJECTION_KIND,
        "projection_id": "mag.domain_memory.operator_receipt_projection.v1",
        "proposal_id": proposal_id,
        "decision": resolved_decision,
        "stage_id": stage_id,
        "receipt_ref": decision_receipt_ref,
        "accepted_memory_ref": accepted_memory_ref if resolved_decision == "accepted" else None,
        "rejected_memory_ref": rejected_memory_ref if resolved_decision == "rejected" else None,
        "contains_memory_body": False,
        "contains_grant_artifact_content": False,
        "contains_quality_or_export_verdict": False,
        "opl_consumes_receipt_ref_only": True,
    }
    decision_payload = {
        "surface_kind": DOMAIN_MEMORY_WRITEBACK_DECISION_KIND,
        "proposal_id": proposal_id,
        "decision": resolved_decision,
        "decision_owner": TARGET_DOMAIN_ID,
        "decision_reason": resolved_reason,
        "target_layer": "workspace_project",
        "target_scope": scope,
        "catalog_ref": "memory/opl_durable_knowledge_catalog.json",
        "knowledge_persistence": "pending_owner_markdown_and_catalog_update" if resolved_decision == "accepted" else "not_applicable",
        "policy_ref": DOMAIN_MEMORY_POLICY_REF,
        "stage_id": stage_id,
        "accepted_memory_ref": accepted_memory_ref if resolved_decision == "accepted" else None,
        "rejected_memory_ref": rejected_memory_ref if resolved_decision == "rejected" else None,
        "decision_receipt_ref": decision_receipt_ref,
        "operator_receipt_projection": receipt_projection,
        "write_policy": "owner_decision_then_project_markdown_and_opl_catalog",
        "authority_boundary": _memory_authority_boundary(),
    }
    return {
        "ok": True,
        "command": "domain-memory-writeback-decision",
        "domain_memory_writeback_decision": decision_payload,
    }


def write_domain_memory_receipt_evidence(
    *,
    decision_payload: str | Path | Mapping[str, Any],
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    decision_body = _require_decision_body(_coerce_decision_payload(decision_payload))
    proposal_id = _require_nonempty_string_from_mapping(
        decision_body,
        "proposal_id",
        context="domain_memory_writeback_decision",
    )
    decision = _require_decision(
        _require_nonempty_string_from_mapping(
            decision_body,
            "decision",
            context="domain_memory_writeback_decision",
        )
    )
    stage_id = _require_stage_id(
        _require_nonempty_string_from_mapping(
            decision_body,
            "stage_id",
            context="domain_memory_writeback_decision",
        )
    )
    receipt_ref = _require_nonempty_string_from_mapping(
        decision_body,
        "decision_receipt_ref",
        context="domain_memory_writeback_decision",
    )
    resolved_runtime_root = (
        Path(runtime_root).expanduser().resolve()
        if runtime_root is not None
        else resolve_runtime_state_root()
    )
    proposal_id = _safe_id(proposal_id)
    receipt_path = resolved_runtime_root / "receipts" / "domain-memory" / f"{proposal_id}.json"
    receipt = {
        "surface_kind": DOMAIN_MEMORY_RUNTIME_RECEIPT_EVIDENCE_KIND,
        "version": "v1",
        "receipt_id": f"mag.domain_memory.receipt.{proposal_id}",
        "state": "runtime_receipt_instance_written",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "proposal_id": proposal_id,
        "decision": decision,
        "decision_owner": TARGET_DOMAIN_ID,
        "stage_id": stage_id,
        "policy_ref": _require_nonempty_string_from_mapping(
            decision_body,
            "policy_ref",
            context="domain_memory_writeback_decision",
        ),
        "receipt_ref": str(receipt_path),
        "declared_receipt_ref": receipt_ref,
        "receipt_instance_ref": str(receipt_path),
        "accepted_memory_ref": decision_body.get("accepted_memory_ref") if decision == "accepted" else None,
        "rejected_memory_ref": decision_body.get("rejected_memory_ref") if decision == "rejected" else None,
        "source_refs": [
            "src/med_autogrant/product_entry_parts/domain_memory_runtime.py#write_domain_memory_receipt_evidence",
            "contracts/durable_knowledge_catalog.json",
            "/product_entry_manifest/owner_receipt_contract",
        ],
        "artifact_mutation": "none",
        "memory_mutation": "decision_receipt_metadata_only",
        "lifecycle_mutation": "none",
        "repo_tracked": False,
        "contains_memory_body": False,
        "contains_grant_artifact_content": False,
        "contains_quality_or_export_verdict": False,
        "forbidden_write_proof": {
            "repo_receipt_instance_written": False,
            "memory_body_written": False,
            "grant_artifact_written": False,
            "fundability_verdict_written": False,
            "authoring_quality_verdict_written": False,
            "submission_ready_export_verdict_written": False,
        },
        "opl_consumption": {
            "role": "receipt_ref_consumer_only",
            "can_hold_memory_content": False,
            "can_issue_fundability_verdict": False,
            "can_issue_authoring_quality_verdict": False,
            "can_issue_export_verdict": False,
        },
    }
    write_json_object_atomic(receipt_path, receipt)
    return {
        "ok": True,
        "command": "domain-memory-receipt-evidence",
        "domain_memory_receipt_evidence": receipt,
    }


def build_domain_memory_operator_projection_contract() -> dict[str, Any]:
    return {
        "surface_kind": DOMAIN_MEMORY_OPERATOR_RECEIPT_PROJECTION_KIND,
        "projection_id": "mag.domain_memory.operator_receipt_projection.v1",
        "maps_to_opl_contract": "opl_family_product_operator_projection.v1",
        "source_refs": [
            "contracts/durable_knowledge_catalog.json",
            "src/med_autogrant/product_entry_parts/domain_memory_runtime.py#build_domain_memory_writeback_proposal",
            "src/med_autogrant/product_entry_parts/domain_memory_runtime.py#build_domain_memory_writeback_decision",
            "src/med_autogrant/product_entry_parts/domain_memory_runtime.py#write_domain_memory_receipt_evidence",
        ],
        "receipt_content_policy": "receipt_refs_and_decision_metadata_only_no_memory_body",
        "operator_fields": [
            "proposal_id",
            "decision",
            "stage_id",
            "receipt_ref",
            "accepted_memory_ref",
            "rejected_memory_ref",
        ],
        "opl_consumption": {
            "role": "operator_receipt_projection_consumer_only",
            "can_hold_memory_content": False,
            "can_issue_fundability_verdict": False,
            "can_issue_authoring_quality_verdict": False,
            "can_issue_export_verdict": False,
        },
    }


def _coerce_decision_payload(payload: str | Path | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(payload, Mapping):
        return payload
    return _read_json_mapping(Path(payload).expanduser().resolve(), context="domain_memory_writeback_decision")


def _require_decision_body(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") == DOMAIN_MEMORY_WRITEBACK_DECISION_KIND:
        return payload
    body = payload.get("domain_memory_writeback_decision")
    if isinstance(body, Mapping):
        return body
    raise WorkspaceStateError("domain_memory_writeback_decision 缺少 decision body。")


def _require_proposal_body(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") == DOMAIN_MEMORY_WRITEBACK_PROPOSAL_KIND:
        return payload
    body = payload.get("domain_memory_writeback_proposal")
    if isinstance(body, Mapping):
        return body
    raise WorkspaceStateError("domain_memory_writeback_proposal 缺少 proposal body。")


def _require_stage_id(stage_id: str) -> str:
    resolved = _require_nonempty_string(stage_id, field_name="stage_id")
    if resolved not in STAGE_IDS:
        raise WorkspaceStateError(f"domain memory stage_id 不允许: {resolved}")
    return resolved


def _require_decision(decision: str) -> str:
    resolved = _require_nonempty_string(decision, field_name="decision")
    if resolved not in {"accepted", "rejected"}:
        raise WorkspaceStateError(f"domain memory decision 不允许: {resolved}")
    return resolved


def _stage_descriptor_ref(stage_id: str) -> str:
    index = STAGE_IDS.index(stage_id)
    return f"/product_entry_manifest/family_stage_control_plane/stages/{index}"


def _memory_authority_boundary() -> dict[str, Any]:
    return {
        "domain_truth_owner": TARGET_DOMAIN_ID,
        "memory_content_owner": TARGET_DOMAIN_ID,
        "fundability_verdict_owner": TARGET_DOMAIN_ID,
        "authoring_quality_verdict_owner": TARGET_DOMAIN_ID,
        "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
        "opl_role": "receipt_ref_and_operator_projection_consumer_only",
    }


def _safe_id(value: str) -> str:
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", value):
        raise WorkspaceStateError("domain memory id must be a filename-safe identifier.")
    return value


def _project_scope(workspace_root: Any, project_root: Any) -> dict[str, str]:
    if not workspace_root or not project_root:
        raise WorkspaceStateError("domain memory requires workspace_root and project_root.")
    workspace = Path(workspace_root).expanduser().resolve(strict=True)
    project = Path(project_root).expanduser().resolve(strict=True)
    if not workspace.is_dir() or not project.is_dir() or workspace == project or workspace not in project.parents:
        raise WorkspaceStateError("domain memory project must be a distinct directory inside its workspace.")
    return {"workspace_root": str(workspace), "project_root": str(project)}
