from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


OWNER_RECEIPT_EVIDENCE_KIND = "mag_owner_receipt_evidence"
LIFECYCLE_RECEIPT_EVIDENCE_KIND = "mag_lifecycle_receipt_evidence"
RECEIPT_RECONCILIATION_PROOF_KIND = "mag_controlled_soak_receipt_reconciliation_proof"
RECEIPT_RECONCILIATION_INVENTORY_KIND = "mag_controlled_soak_receipt_reconciliation_inventory"
PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_PROJECTION_KIND = (
    "mag_production_live_acceptance_receipt_projection"
)

_RECEIPT_SHAPES = ("domain_owner_receipt", "typed_blocker", "no_regression_evidence")
_STAGE_IDS = (
    "call_and_candidate_intake",
    "fundability_strategy",
    "specific_aims_and_structure",
    "proposal_authoring",
    "review_and_rebuttal",
    "package_and_submit_ready",
)
_LIFECYCLE_OPERATIONS = ("cleanup", "restore", "retention")
_PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_SHAPES = ("domain_owner_receipt", "typed_blocker")
_PATCH_LOOP_REF_KEYS = (
    "blocked_suite_result_ref",
    "developer_patch_work_order_ref",
    "patch_traceability_matrix_ref",
    "target_repo_verification_refs",
    "target_runtime_read_model_consumption_ref",
    "workspace_environment_proof_ref",
    "no_forbidden_write_proof_ref",
    "target_owner_receipt_or_typed_blocker_ref",
    "patch_absorption_ref",
    "worktree_cleanup_ref",
    "agent_lab_re_evaluation_ref",
)
_PATCH_LOOP_REF_LIST_KEYS = ("target_repo_verification_refs",)


def write_owner_receipt_evidence(
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
    resolved_input_path = Path(input_path).expanduser().resolve()
    resolved_stage_id = _require_choice(stage_id, choices=_STAGE_IDS, field_name="stage_id")
    resolved_shape = _require_choice(
        receipt_shape,
        choices=_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    resolved_source_ref = _require_nonempty_string(source_ref, field_name="source_ref")
    resolved_summary = _require_nonempty_string(closeout_summary, field_name="closeout_summary")
    resolved_receipt_id = receipt_id or f"{resolved_stage_id}-{resolved_shape}"
    runtime_state_root = _resolve_runtime_root(runtime_root)
    receipt_path = runtime_state_root / "receipts" / "owner-receipts" / f"{resolved_receipt_id}.json"
    receipt = {
        "surface_kind": OWNER_RECEIPT_EVIDENCE_KIND,
        "version": "v1",
        "receipt_id": f"mag.owner_receipt.{resolved_receipt_id}",
        "state": "runtime_receipt_instance_written",
        "receipt_shape": resolved_shape,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "stage_id": resolved_stage_id,
        "source_ref": resolved_source_ref,
        "closeout_summary": resolved_summary,
        "workspace_locator": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(resolved_input_path),
            "repo_tracked": False,
        },
        "receipt_instance_ref": str(receipt_path),
        "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
        "source_refs": [
            "/product_entry_manifest/controlled_stage_attempt_projection",
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/controlled_domain_memory_apply_proof",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/grant_authoring_readiness",
        ],
        "artifact_mutation": "none",
        "memory_mutation": "none",
        "lifecycle_mutation": "none",
        "repo_tracked": False,
        "forbidden_write_proof": _forbidden_write_proof(),
        "opl_consumption": _opl_receipt_ref_consumption(),
        "closeout_refs": dict(closeout_refs or {}),
    }
    _write_receipt(receipt_path, receipt)
    return {
        "ok": True,
        "command": "owner-receipt-evidence",
        "owner_receipt_evidence": receipt,
    }


def write_lifecycle_receipt_evidence(
    *,
    input_path: str | Path,
    operation: str,
    receipt_shape: str,
    source_ref: str,
    closeout_summary: str,
    runtime_root: str | Path | None = None,
    receipt_id: str | None = None,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    resolved_operation = _require_choice(
        operation,
        choices=_LIFECYCLE_OPERATIONS,
        field_name="operation",
    )
    resolved_shape = _require_choice(
        receipt_shape,
        choices=_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    resolved_source_ref = _require_nonempty_string(source_ref, field_name="source_ref")
    resolved_summary = _require_nonempty_string(closeout_summary, field_name="closeout_summary")
    resolved_receipt_id = receipt_id or f"{resolved_operation}-{resolved_shape}"
    runtime_state_root = _resolve_runtime_root(runtime_root)
    receipt_path = runtime_state_root / "receipts" / "lifecycle" / f"{resolved_receipt_id}.json"
    receipt = {
        "surface_kind": LIFECYCLE_RECEIPT_EVIDENCE_KIND,
        "version": "v1",
        "receipt_id": f"mag.lifecycle.receipt.{resolved_receipt_id}",
        "state": "runtime_receipt_instance_written",
        "operation": resolved_operation,
        "receipt_shape": resolved_shape,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "source_ref": resolved_source_ref,
        "closeout_summary": resolved_summary,
        "workspace_locator": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(resolved_input_path),
            "repo_tracked": False,
        },
        "receipt_instance_ref": str(receipt_path),
        "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
        "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
        "source_refs": [
            "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/runtime_control/restore_point",
        ],
        "artifact_mutation": "none",
        "memory_mutation": "none",
        "lifecycle_mutation": "receipt_metadata_only",
        "repo_tracked": False,
        "forbidden_write_proof": _forbidden_write_proof(),
        "opl_consumption": _opl_receipt_ref_consumption(),
    }
    _write_receipt(receipt_path, receipt)
    return {
        "ok": True,
        "command": "lifecycle-receipt-evidence",
        "lifecycle_receipt_evidence": receipt,
    }


def build_controlled_soak_receipt_reconciliation_proof(
    *,
    owner_receipt_evidence: Mapping[str, Any],
    opl_ledger_ref: str,
    sidecar_closeout_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    receipt = _require_owner_receipt_evidence(owner_receipt_evidence)
    resolved_ledger_ref = _require_nonempty_string(opl_ledger_ref, field_name="opl_ledger_ref")
    closeout_result = dict(sidecar_closeout_result or {})
    receipt_ref = _require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
    receipt_shape = _require_choice(
        _require_nonempty_string_from_receipt(receipt, "receipt_shape"),
        choices=_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    typed_blocker = _reconciled_typed_blocker(receipt, closeout_result)
    evidence_refs = _reconciled_no_regression_evidence_refs(receipt, closeout_result)
    payload = {
        "surface_kind": RECEIPT_RECONCILIATION_PROOF_KIND,
        "version": "v1",
        "state": "probe_reconciled_not_live_soak_complete",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "probe_scope": "controlled_soak_deferred_blocker_receipt_reconciliation",
        "claims_production_long_run_soak_complete": False,
        "rebuilds_opl_runtime": False,
        "source_refs": [
            "/product_entry_manifest/controlled_soak_no_regression_attempt",
            "/product_entry_manifest/controlled_stage_attempt_projection",
            "/product_entry_manifest/owner_receipt_contract",
            "product sidecar-dispatch stage-attempt/closeout",
            "product owner-receipt-evidence",
        ],
        "opl_ledger": {
            "ledger_ref": resolved_ledger_ref,
            "role": "external_ref_for_reconciliation_only",
            "mag_writes_opl_ledger": False,
            "opl_holds_grant_truth": False,
        },
        "mag_owner_receipt": {
            "receipt_ref": receipt_ref,
            "receipt_id": _require_nonempty_string_from_receipt(receipt, "receipt_id"),
            "receipt_shape": receipt_shape,
            "stage_id": _require_nonempty_string_from_receipt(receipt, "stage_id"),
            "source_ref": _require_nonempty_string_from_receipt(receipt, "source_ref"),
            "owner_receipt_contract_ref": _require_nonempty_string_from_receipt(
                receipt,
                "owner_receipt_contract_ref",
            ),
        },
        "typed_blocker": typed_blocker,
        "no_regression_evidence": {
            "evidence_refs": evidence_refs,
            "present": bool(evidence_refs),
            "repo_tracked_projection_only": True,
        },
        "reconciliation": {
            "status": _reconciliation_status(receipt_shape, typed_blocker, evidence_refs),
            "receipt_ref_matches_sidecar": _receipt_ref_matches_sidecar(receipt_ref, closeout_result),
            "opl_ledger_ref_matches_receipt_source": (
                resolved_ledger_ref == _require_nonempty_string_from_receipt(receipt, "source_ref")
            ),
            "closeout_payload_consumed": bool(closeout_result),
        },
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_ref_consumer_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_authoring_quality_ready": False,
            "can_declare_submission_ready_export": False,
        },
        "forbidden_write_proof": dict(receipt["forbidden_write_proof"]),
    }
    return {
        "ok": True,
        "command": "controlled-soak-receipt-reconciliation-proof",
        "receipt_reconciliation_proof": payload,
    }


def build_controlled_soak_receipt_reconciliation_inventory(
    *,
    owner_receipt_evidence_items: Sequence[Mapping[str, Any]],
    opl_ledger_ref: str,
    sidecar_closeout_results: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    resolved_ledger_ref = _require_nonempty_string(opl_ledger_ref, field_name="opl_ledger_ref")
    if not owner_receipt_evidence_items:
        raise WorkspaceStateError("owner_receipt_evidence_items 至少需要一条 receipt evidence。")
    closeout_by_receipt_ref = _index_closeout_results_by_receipt_ref(sidecar_closeout_results or [])
    items: list[dict[str, Any]] = []
    for receipt_payload in owner_receipt_evidence_items:
        receipt = _require_owner_receipt_evidence(receipt_payload)
        receipt_ref = _require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
        proof = build_controlled_soak_receipt_reconciliation_proof(
            owner_receipt_evidence=receipt,
            opl_ledger_ref=resolved_ledger_ref,
            sidecar_closeout_result=closeout_by_receipt_ref.get(receipt_ref),
        )["receipt_reconciliation_proof"]
        items.append(
            {
                "receipt_ref": receipt_ref,
                "receipt_shape": proof["mag_owner_receipt"]["receipt_shape"],
                "stage_id": proof["mag_owner_receipt"]["stage_id"],
                "source_ref": proof["mag_owner_receipt"]["source_ref"],
                "reconciliation_status": proof["reconciliation"]["status"],
                "receipt_ref_matches_sidecar": proof["reconciliation"]["receipt_ref_matches_sidecar"],
                "opl_ledger_ref_matches_receipt_source": proof["reconciliation"][
                    "opl_ledger_ref_matches_receipt_source"
                ],
                "typed_blocker_present": proof["typed_blocker"] is not None,
                "no_regression_evidence_refs": list(proof["no_regression_evidence"]["evidence_refs"]),
                "authority_boundary": dict(proof["authority_boundary"]),
            }
        )
    payload = {
        "surface_kind": RECEIPT_RECONCILIATION_INVENTORY_KIND,
        "version": "v1",
        "state": "read_projection_only_not_live_soak_complete",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "opl_ledger": {
            "ledger_ref": resolved_ledger_ref,
            "role": "external_ref_for_inventory_reconciliation_only",
            "mag_writes_opl_ledger": False,
            "opl_holds_grant_truth": False,
        },
        "summary": {
            "item_count": len(items),
            "sidecar_closeout_result_count": len(closeout_by_receipt_ref),
            "by_receipt_shape": _count_by(items, "receipt_shape"),
            "by_reconciliation_status": _count_by(items, "reconciliation_status"),
            "typed_blocker_count": sum(1 for item in items if item["typed_blocker_present"]),
            "no_regression_evidence_ref_count": sum(
                len(item["no_regression_evidence_refs"]) for item in items
            ),
        },
        "items": items,
        "claims_production_long_run_soak_complete": False,
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_ref_consumer_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_authoring_quality_ready": False,
            "can_declare_submission_ready_export": False,
        },
        "forbidden_write_proof": _forbidden_write_proof(),
    }
    return {
        "ok": True,
        "command": "controlled-soak-receipt-reconciliation-inventory",
        "receipt_reconciliation_inventory": payload,
    }


def build_production_live_acceptance_receipt_projection(
    *,
    owner_receipt_evidence: Mapping[str, Any],
    agent_lab_suite_result: Mapping[str, Any],
    meta_agent_coordination_result: Mapping[str, Any],
) -> dict[str, Any]:
    receipt = _require_owner_receipt_evidence(owner_receipt_evidence)
    receipt_shape = _require_choice(
        _require_nonempty_string_from_receipt(receipt, "receipt_shape"),
        choices=_PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    if receipt_shape not in _PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_SHAPES:
        raise WorkspaceStateError(
            "production live acceptance 只能使用 domain_owner_receipt 或 typed_blocker closeout。"
        )
    suite_result = _extract_agent_lab_suite_result(agent_lab_suite_result)
    meta_result = _extract_meta_agent_coordination_result(meta_agent_coordination_result)
    suite_result_id = _require_nonempty_string(suite_result.get("result_id"), field_name="suite_result.result_id")
    meta_agent_lab_result_ref = _meta_agent_lab_result_ref(meta_result)
    if meta_agent_lab_result_ref != suite_result_id:
        raise WorkspaceStateError("opl-meta-agent coordination result 必须绑定同一个 Agent Lab result_id。")
    patch_loop_refs = _meta_patch_loop_refs(meta_result)
    if receipt_shape == "typed_blocker" and patch_loop_refs is None:
        raise WorkspaceStateError("typed_blocker closeout 必须提供完整 OMA developer patch-loop refs。")
    receipt_ref = _require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
    accepted_return_shape = (
        "domain_owner_receipt_ref"
        if receipt_shape == "domain_owner_receipt"
        else "typed_blocker_ref"
    )
    evidence_ref = (
        patch_loop_refs["target_owner_receipt_or_typed_blocker_ref"]
        if patch_loop_refs is not None
        else "receipt:mag/production-live-acceptance/2026-05-20"
    )
    payload = {
        "surface_kind": PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_PROJECTION_KIND,
        "version": "v1",
        "state": (
            "closed_by_mag_domain_owner_live_acceptance_receipt"
            if receipt_shape == "domain_owner_receipt"
            else "typed_blocker_closeout_refs_ready"
        ),
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "receipt": {
            "receipt_ref": receipt_ref,
            "receipt_id": _require_nonempty_string_from_receipt(receipt, "receipt_id"),
            "receipt_shape": receipt_shape,
            "stage_id": _require_nonempty_string_from_receipt(receipt, "stage_id"),
            "source_ref": _require_nonempty_string_from_receipt(receipt, "source_ref"),
            "owner_receipt_contract_ref": _require_nonempty_string_from_receipt(
                receipt,
                "owner_receipt_contract_ref",
            ),
            "repo_tracked_receipt_instance_body": False,
        },
        "agent_lab_coordination": {
            "surface_kind": suite_result["surface_kind"],
            "suite_id": _require_nonempty_string(suite_result.get("suite_id"), field_name="suite_id"),
            "suite_kind": _require_nonempty_string(suite_result.get("suite_kind"), field_name="suite_kind"),
            "result_id": _require_nonempty_string(suite_result.get("result_id"), field_name="result_id"),
            "status": suite_result["status"],
            "owner_or_human_gate_required_count": _suite_summary_int(
                suite_result,
                "owner_or_human_gate_required_count",
            ),
            "promotable_candidate_count": _suite_summary_int(suite_result, "promotable_candidate_count"),
            "agent_lab_can_issue_mag_owner_receipt": False,
        },
        "meta_agent_coordination": {
            "surface_kind": meta_result["surface_kind"],
            "status": meta_result["status"],
            "target_agent_id": _meta_target_domain_id(meta_result),
            "source_agent_lab_result_ref": meta_agent_lab_result_ref,
            "developer_work_order_status": _meta_developer_work_order_status(meta_result),
            "meta_agent_can_write_mag_truth": False,
            "meta_agent_can_authorize_fundability_ready": False,
        },
        "production_acceptance": {
            "accepted_return_shape": accepted_return_shape,
            "closed_typed_blocker_kind": "domain_owner_live_acceptance_receipt_scaleout_required",
            "evidence_ref": evidence_ref,
            "contract_ref": "contracts/production_acceptance/mag-production-acceptance.json",
            "doc_ref": "docs/status.md#production-acceptance",
            "next_verification_command": (
                "rtk ./scripts/run-pytest-clean.sh tests/test_production_acceptance.py "
                "tests/product_entry_cases/test_production_live_acceptance.py -q"
            ),
        },
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_agent_lab_ref_consumer_only": True,
            "meta_agent_work_order_consumer_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_authoring_quality_ready": False,
            "can_declare_submission_ready_export": False,
            "provider_completion_equals_fundability_ready": False,
            "agent_lab_pass_equals_fundability_ready": False,
            "meta_agent_pass_equals_fundability_ready": False,
        },
        "forbidden_write_proof": dict(receipt["forbidden_write_proof"]),
    }
    if patch_loop_refs is not None:
        payload["patch_loop_refs"] = patch_loop_refs
    return {
        "ok": True,
        "command": "production-live-acceptance-receipt",
        "production_live_acceptance_receipt": payload,
    }


def _resolve_runtime_root(runtime_root: str | Path | None) -> Path:
    if runtime_root is not None:
        return Path(runtime_root).expanduser().resolve()
    return resolve_runtime_state_root()


def _require_choice(value: str, *, choices: tuple[str, ...], field_name: str) -> str:
    resolved = _require_nonempty_string(value, field_name=field_name)
    if resolved not in choices:
        raise WorkspaceStateError(f"{field_name} 不支持: {resolved}。只允许 {', '.join(choices)}。")
    return resolved


def _forbidden_write_proof() -> dict[str, bool]:
    return {
        "repo_receipt_instance_written": False,
        "grant_truth_written": False,
        "grant_artifact_written": False,
        "memory_body_written": False,
        "fundability_verdict_written": False,
        "authoring_quality_verdict_written": False,
        "submission_ready_export_verdict_written": False,
    }


def _opl_receipt_ref_consumption() -> dict[str, bool | str]:
    return {
        "role": "receipt_ref_consumer_only",
        "consumes_receipt_ref_only": True,
        "can_write_grant_truth": False,
        "can_write_memory_body": False,
        "can_declare_export_ready": False,
    }


def _write_receipt(path: Path, receipt: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 receipt evidence 失败: {path}") from exc


def _index_closeout_results_by_receipt_ref(
    closeout_results: Sequence[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for closeout in closeout_results:
        receipt_ref = closeout.get("receipt_ref")
        if not isinstance(receipt_ref, str) or not receipt_ref.strip():
            raise WorkspaceStateError("sidecar_closeout_result.receipt_ref 必须是非空字符串。")
        if receipt_ref in indexed:
            raise WorkspaceStateError(f"sidecar_closeout_result.receipt_ref 重复: {receipt_ref}")
        indexed[receipt_ref] = closeout
    return indexed


def _count_by(items: Sequence[Mapping[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = _require_nonempty_string(item.get(key), field_name=key)
        counts[value] = counts.get(value, 0) + 1
    return counts


def _require_owner_receipt_evidence(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") != OWNER_RECEIPT_EVIDENCE_KIND:
        raise WorkspaceStateError("owner_receipt_evidence.surface_kind 必须是 mag_owner_receipt_evidence。")
    if payload.get("owner") != TARGET_DOMAIN_ID or payload.get("target_domain_id") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("owner_receipt_evidence.owner 和 target_domain_id 必须都是 med-autogrant。")
    forbidden = payload.get("forbidden_write_proof")
    if not isinstance(forbidden, Mapping):
        raise WorkspaceStateError("owner_receipt_evidence 缺少 forbidden_write_proof。")
    if any(bool(forbidden.get(key)) for key in (
        "repo_receipt_instance_written",
        "grant_truth_written",
        "grant_artifact_written",
        "memory_body_written",
        "fundability_verdict_written",
        "authoring_quality_verdict_written",
        "submission_ready_export_verdict_written",
    )):
        raise WorkspaceStateError("owner_receipt_evidence 不能包含 MAG/OPL forbidden write。")
    return payload


def _require_mapping_payload(payload: Mapping[str, Any], *, context: str) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object。")
    return payload


def _extract_agent_lab_suite_result(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    record = _require_mapping_payload(payload, context="agent_lab_suite_result")
    if record.get("surface_kind") == "opl_agent_lab_suite_result":
        suite_result = record
    elif isinstance(record.get("suite_result"), Mapping):
        suite_result = record["suite_result"]
    elif isinstance(record.get("agent_lab_run"), Mapping):
        suite_result = _require_mapping_payload(record["agent_lab_run"], context="agent_lab_run").get("suite_result")
    else:
        raise WorkspaceStateError("agent_lab_suite_result 缺少 OPL Agent Lab suite_result。")
    suite_result = _require_mapping_payload(suite_result, context="agent_lab_suite_result.suite_result")
    if suite_result.get("surface_kind") != "opl_agent_lab_suite_result":
        raise WorkspaceStateError("agent_lab_suite_result.surface_kind 必须是 opl_agent_lab_suite_result。")
    _require_nonempty_string(suite_result.get("suite_id"), field_name="suite_id")
    if suite_result.get("suite_kind") not in (
        "agent_lab_external_suite",
        "agent_production_evidence_suite",
    ):
        raise WorkspaceStateError("Agent Lab suite result.suite_kind 必须是标准 external/evidence suite kind。")
    if suite_result.get("status") != "passed":
        raise WorkspaceStateError("MAG production live acceptance 需要 passed Agent Lab suite result。")
    if "med-autogrant" not in _suite_domain_ids(suite_result):
        raise WorkspaceStateError("Agent Lab suite result 必须指向 med-autogrant。")
    summary = _require_mapping_payload(suite_result.get("summary"), context="agent_lab_suite_result.summary")
    forbidden_flag_count = _suite_summary_int(suite_result, "forbidden_authority_flag_count")
    if forbidden_flag_count != 0:
        raise WorkspaceStateError("Agent Lab suite result 存在 forbidden authority flag。")
    refs = _require_mapping_payload(suite_result.get("refs"), context="agent_lab_suite_result.refs")
    receipt_refs = refs.get("receipt_refs")
    if not isinstance(receipt_refs, Sequence) or isinstance(receipt_refs, (str, bytes)):
        raise WorkspaceStateError("Agent Lab suite result 必须提供 receipt_refs。")
    if "receipt:mag/production-live-acceptance/2026-05-20" not in receipt_refs:
        raise WorkspaceStateError("Agent Lab suite result 缺少 MAG production live acceptance receipt ref。")
    authority = _require_mapping_payload(
        suite_result.get("authority_boundary"),
        context="agent_lab_suite_result.authority_boundary",
    )
    if any(bool(authority.get(key)) for key in (
        "can_write_domain_truth",
        "can_write_memory_body",
        "can_authorize_quality_verdict",
        "can_write_owner_receipt",
    )):
        raise WorkspaceStateError("Agent Lab suite result 不能持有 MAG truth 或 quality authority。")
    return suite_result


def _suite_domain_ids(suite_result: Mapping[str, Any]) -> list[str]:
    domain_summary = suite_result.get("domain_summary")
    if not isinstance(domain_summary, Sequence) or isinstance(domain_summary, (str, bytes)):
        return []
    ids: list[str] = []
    for item in domain_summary:
        if isinstance(item, Mapping) and isinstance(item.get("domain_id"), str):
            ids.append(item["domain_id"])
    return ids


def _suite_summary_int(suite_result: Mapping[str, Any], key: str) -> int:
    summary = _require_mapping_payload(suite_result.get("summary"), context="agent_lab_suite_result.summary")
    value = summary.get(key)
    if not isinstance(value, int):
        raise WorkspaceStateError(f"agent_lab_suite_result.summary.{key} 必须是整数。")
    return value


def _extract_meta_agent_coordination_result(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    record = _require_mapping_payload(payload, context="meta_agent_coordination_result")
    if record.get("surface_kind") != "opl_meta_agent_external_suite_self_evolution_result":
        raise WorkspaceStateError(
            "meta_agent_coordination_result.surface_kind 必须是 opl_meta_agent_external_suite_self_evolution_result。"
        )
    if record.get("status") != "passed":
        raise WorkspaceStateError("MAG production live acceptance 需要 passed opl-meta-agent coordination result。")
    if _meta_target_domain_id(record) != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("opl-meta-agent coordination result 必须指向 med-autogrant。")
    authority = record.get("authority_boundary")
    if isinstance(authority, Mapping) and any(bool(authority.get(key)) for key in (
        "can_write_target_domain_truth",
        "can_write_target_domain_memory_body",
        "can_mutate_target_domain_artifact_body",
        "can_authorize_target_domain_quality_or_export",
    )):
        raise WorkspaceStateError("opl-meta-agent coordination result 不能持有 MAG truth、artifact 或 verdict authority。")
    if _meta_developer_work_order_status(record) not in ("no_patch_required", "patch_smoke_closed"):
        raise WorkspaceStateError(
            "MAG production live acceptance 需要 opl-meta-agent no_patch_required 或 patch_smoke_closed work order。"
        )
    return record


def _meta_target_domain_id(meta_result: Mapping[str, Any]) -> str:
    target = meta_result.get("target_agent")
    if not isinstance(target, Mapping):
        raise WorkspaceStateError("meta_agent_coordination_result 缺少 target_agent。")
    return _require_nonempty_string(target.get("domain_id"), field_name="target_agent.domain_id")


def _meta_developer_work_order_status(meta_result: Mapping[str, Any]) -> str:
    learning_loop = meta_result.get("learning_loop")
    if not isinstance(learning_loop, Mapping):
        raise WorkspaceStateError("meta_agent_coordination_result 缺少 learning_loop。")
    work_order = learning_loop.get("developer_patch_work_order")
    if not isinstance(work_order, Mapping):
        raise WorkspaceStateError("meta_agent_coordination_result 缺少 developer_patch_work_order。")
    return _require_nonempty_string(work_order.get("status"), field_name="developer_patch_work_order.status")


def _meta_agent_lab_result_ref(meta_result: Mapping[str, Any]) -> str:
    learning_loop = meta_result.get("learning_loop")
    if not isinstance(learning_loop, Mapping):
        raise WorkspaceStateError("meta_agent_coordination_result 缺少 learning_loop。")
    work_order = learning_loop.get("developer_patch_work_order")
    if not isinstance(work_order, Mapping):
        raise WorkspaceStateError("meta_agent_coordination_result 缺少 developer_patch_work_order。")
    return _require_nonempty_string(
        work_order.get("source_agent_lab_result_ref"),
        field_name="developer_patch_work_order.source_agent_lab_result_ref",
    )


def _meta_patch_loop_refs(meta_result: Mapping[str, Any]) -> dict[str, Any] | None:
    learning_loop = meta_result.get("learning_loop")
    if not isinstance(learning_loop, Mapping):
        raise WorkspaceStateError("meta_agent_coordination_result 缺少 learning_loop。")
    work_order = learning_loop.get("developer_patch_work_order")
    if not isinstance(work_order, Mapping):
        raise WorkspaceStateError("meta_agent_coordination_result 缺少 developer_patch_work_order。")
    if _meta_developer_work_order_status(meta_result) == "no_patch_required":
        return None
    refs: dict[str, Any] = {}
    for key in _PATCH_LOOP_REF_KEYS:
        if key in _PATCH_LOOP_REF_LIST_KEYS:
            value = work_order.get(key)
            if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
                raise WorkspaceStateError(f"developer_patch_work_order.{key} 必须是 ref 字符串列表。")
            refs[key] = [
                _require_nonempty_string(item, field_name=f"developer_patch_work_order.{key}[]")
                for item in value
            ]
            if not refs[key]:
                raise WorkspaceStateError(f"developer_patch_work_order.{key} 至少需要一个 ref。")
        else:
            refs[key] = _require_nonempty_string(
                work_order.get(key),
                field_name=f"developer_patch_work_order.{key}",
            )
    return refs


def _require_nonempty_string_from_receipt(receipt: Mapping[str, Any], key: str) -> str:
    return _require_nonempty_string(receipt.get(key), field_name=key)


def _receipt_ref_matches_sidecar(receipt_ref: str, closeout_result: Mapping[str, Any]) -> bool | None:
    if not closeout_result:
        return None
    return closeout_result.get("receipt_ref") == receipt_ref


def _reconciled_typed_blocker(
    receipt: Mapping[str, Any],
    closeout_result: Mapping[str, Any],
) -> dict[str, Any] | None:
    sidecar_blocker = closeout_result.get("typed_blocker")
    if isinstance(sidecar_blocker, Mapping):
        return dict(sidecar_blocker)
    if receipt.get("receipt_shape") != "typed_blocker":
        return None
    return {
        "blocker_kind": "mag_stage_attempt_owner_receipt_required",
        "owner": TARGET_DOMAIN_ID,
        "receipt_ref": receipt["receipt_instance_ref"],
        "source_ref": receipt["source_ref"],
        "next_action": "Route the blocker back to MAG owner surface before mutating grant truth, memory body, or artifact content.",
    }


def _reconciled_no_regression_evidence_refs(
    receipt: Mapping[str, Any],
    closeout_result: Mapping[str, Any],
) -> list[str]:
    refs: list[str] = []
    receipt_refs = closeout_result.get("receipt_refs")
    if isinstance(receipt_refs, Mapping):
        no_regression_ref = receipt_refs.get("no_regression_evidence_ref")
        if isinstance(no_regression_ref, str) and no_regression_ref:
            refs.append(no_regression_ref)
    if receipt.get("receipt_shape") == "no_regression_evidence":
        receipt_ref = _require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
        if receipt_ref not in refs:
            refs.append(receipt_ref)
    return refs


def _reconciliation_status(
    receipt_shape: str,
    typed_blocker: Mapping[str, Any] | None,
    evidence_refs: list[str],
) -> str:
    if receipt_shape == "typed_blocker" and typed_blocker is not None:
        return "typed_blocker_reconciled"
    if receipt_shape == "no_regression_evidence" and evidence_refs:
        return "no_regression_evidence_reconciled"
    return "domain_owner_receipt_reconciled"
