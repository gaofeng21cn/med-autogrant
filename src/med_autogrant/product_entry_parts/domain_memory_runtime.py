from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


DOMAIN_MEMORY_WRITEBACK_PROPOSAL_KIND = "mag_domain_memory_writeback_proposal"
DOMAIN_MEMORY_WRITEBACK_DECISION_KIND = "mag_domain_memory_writeback_decision"
DOMAIN_MEMORY_OPERATOR_RECEIPT_PROJECTION_KIND = "mag_domain_memory_operator_receipt_projection"
DOMAIN_MEMORY_POLICY_REF = "docs/references/grant_strategy_memory_policy.md"

STAGE_IDS = (
    "call_and_candidate_intake",
    "fundability_strategy",
    "specific_aims_and_structure",
    "proposal_authoring",
    "review_and_rebuttal",
    "package_and_submit_ready",
)

_FORBIDDEN_SCAN = {
    "contains_workspace_private_evidence": False,
    "contains_canonical_grant_artifact_content": False,
    "contains_fundability_verdict": False,
    "contains_authoring_quality_verdict": False,
    "contains_submission_ready_export_verdict": False,
}


def build_domain_memory_writeback_proposal(
    *,
    input_path: str | Path,
    stage_id: str,
    lesson_summary: str,
    source_ref: str,
    proposal_id: str | None = None,
    grant_run_id: str | None = None,
) -> dict[str, Any]:
    resolved_stage_id = _require_stage_id(stage_id)
    resolved_lesson_summary = _require_nonempty_string(lesson_summary, field_name="lesson_summary")
    resolved_source_ref = _require_nonempty_string(source_ref, field_name="source_ref")
    resolved_input_path = Path(input_path).expanduser().resolve()
    resolved_proposal_id = proposal_id or f"{resolved_stage_id}-writeback-proposal"
    grant_run_segment = grant_run_id or "<grant_run_id>"
    proposal = {
        "surface_kind": DOMAIN_MEMORY_WRITEBACK_PROPOSAL_KIND,
        "proposal_id": _require_nonempty_string(resolved_proposal_id, field_name="proposal_id"),
        "target_domain_id": TARGET_DOMAIN_ID,
        "decision_owner": TARGET_DOMAIN_ID,
        "stage_id": resolved_stage_id,
        "memory_role": "strategy_context",
        "policy_ref": DOMAIN_MEMORY_POLICY_REF,
        "descriptor_ref": "/product_entry_manifest/domain_memory_descriptor_locator",
        "stage_descriptor_ref": _stage_descriptor_ref(resolved_stage_id),
        "source_locator": {
            "locator_kind": "workspace_or_runtime_ref",
            "workspace_path": str(resolved_input_path),
            "source_ref": resolved_source_ref,
            "repo_tracked": False,
        },
        "lesson_summary": resolved_lesson_summary,
        "forbidden_content_scan": dict(_FORBIDDEN_SCAN),
        "write_policy": "runtime_store_only_no_repo_write",
        "proposal_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
            f"writeback-proposals/{grant_run_segment}/{resolved_proposal_id}.json"
        ),
        "decision_receipt_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
            f"{grant_run_segment}/memory-writeback-decisions/{resolved_proposal_id}.json"
        ),
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
    _validate_forbidden_scan(proposal_body)
    resolved_reason = _require_nonempty_string(decision_reason, field_name="decision_reason")
    resolved_memory_id = memory_id or proposal_id
    accepted_memory_ref = (
        "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
        f"accepted/{resolved_memory_id}.json"
    )
    rejected_memory_ref = (
        "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
        f"rejected/{proposal_id}.json"
    )
    decision_receipt_ref = (
        "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
        f"<grant_run_id>/memory-writeback-decisions/{proposal_id}.json"
    )
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
        "policy_ref": DOMAIN_MEMORY_POLICY_REF,
        "stage_id": stage_id,
        "accepted_memory_ref": accepted_memory_ref if resolved_decision == "accepted" else None,
        "rejected_memory_ref": rejected_memory_ref if resolved_decision == "rejected" else None,
        "decision_receipt_ref": decision_receipt_ref,
        "operator_receipt_projection": receipt_projection,
        "write_policy": "runtime_store_only_no_repo_write",
        "authority_boundary": _memory_authority_boundary(),
    }
    return {
        "ok": True,
        "command": "domain-memory-writeback-decision",
        "domain_memory_writeback_decision": decision_payload,
    }


def build_domain_memory_operator_projection_contract() -> dict[str, Any]:
    return {
        "surface_kind": DOMAIN_MEMORY_OPERATOR_RECEIPT_PROJECTION_KIND,
        "projection_id": "mag.domain_memory.operator_receipt_projection.v1",
        "maps_to_opl_contract": "opl_family_product_operator_projection.v1",
        "source_refs": [
            "/product_entry_manifest/domain_memory_descriptor_locator",
            "/product_entry_manifest/domain_memory_descriptor_locator/writeback_proposal_generator",
            "/product_entry_manifest/domain_memory_descriptor_locator/accept_reject_command",
            "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator",
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


def _require_proposal_body(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") == DOMAIN_MEMORY_WRITEBACK_PROPOSAL_KIND:
        return payload
    body = payload.get("domain_memory_writeback_proposal")
    if isinstance(body, Mapping):
        return body
    raise WorkspaceStateError("domain_memory_writeback_proposal 缺少 proposal body。")


def _read_json_mapping(path: Path, *, context: str) -> Mapping[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise WorkspaceFileError(f"读取 {context} 失败: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(f"{context} 不是合法 JSON: {path}") from exc
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object: {path}")
    return payload


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


def _validate_forbidden_scan(proposal: Mapping[str, Any]) -> None:
    scan = proposal.get("forbidden_content_scan")
    if not isinstance(scan, Mapping):
        raise WorkspaceStateError("domain memory proposal 缺少 forbidden_content_scan。")
    for key, expected in _FORBIDDEN_SCAN.items():
        if scan.get(key) is not expected:
            raise WorkspaceStateError(f"domain memory proposal 违反内容边界: {key}")


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
