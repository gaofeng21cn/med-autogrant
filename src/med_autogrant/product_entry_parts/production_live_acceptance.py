from __future__ import annotations

from typing import Any, Mapping, Sequence

from med_autogrant.product_entry_parts.owner_receipt_common import (
    PATCH_LOOP_REF_KEYS,
    PATCH_LOOP_REF_LIST_KEYS,
    PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_PROJECTION_KIND,
    PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_SHAPES,
    require_choice,
    require_mapping_payload,
    require_nonempty_string_from_receipt,
    require_owner_receipt_evidence,
)
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)
from med_autogrant.workspace_types import WorkspaceStateError


def build_production_live_acceptance_receipt_projection(
    *,
    owner_receipt_evidence: Mapping[str, Any],
    agent_lab_suite_result: Mapping[str, Any],
    meta_agent_coordination_result: Mapping[str, Any],
) -> dict[str, Any]:
    receipt = require_owner_receipt_evidence(owner_receipt_evidence)
    receipt_shape = require_choice(
        require_nonempty_string_from_receipt(receipt, "receipt_shape"),
        choices=PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    if receipt_shape not in PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_SHAPES:
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
    receipt_ref = require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
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
            "receipt_id": require_nonempty_string_from_receipt(receipt, "receipt_id"),
            "receipt_shape": receipt_shape,
            "stage_id": require_nonempty_string_from_receipt(receipt, "stage_id"),
            "source_ref": require_nonempty_string_from_receipt(receipt, "source_ref"),
            "owner_receipt_contract_ref": require_nonempty_string_from_receipt(
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


def _extract_agent_lab_suite_result(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    record = require_mapping_payload(payload, context="agent_lab_suite_result")
    if record.get("surface_kind") == "opl_agent_lab_suite_result":
        suite_result = record
    elif isinstance(record.get("suite_result"), Mapping):
        suite_result = record["suite_result"]
    elif isinstance(record.get("agent_lab_run"), Mapping):
        suite_result = require_mapping_payload(record["agent_lab_run"], context="agent_lab_run").get("suite_result")
    else:
        raise WorkspaceStateError("agent_lab_suite_result 缺少 OPL Agent Lab suite_result。")
    suite_result = require_mapping_payload(suite_result, context="agent_lab_suite_result.suite_result")
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
    require_mapping_payload(suite_result.get("summary"), context="agent_lab_suite_result.summary")
    forbidden_flag_count = _suite_summary_int(suite_result, "forbidden_authority_flag_count")
    if forbidden_flag_count != 0:
        raise WorkspaceStateError("Agent Lab suite result 存在 forbidden authority flag。")
    refs = require_mapping_payload(suite_result.get("refs"), context="agent_lab_suite_result.refs")
    receipt_refs = refs.get("receipt_refs")
    if not isinstance(receipt_refs, Sequence) or isinstance(receipt_refs, (str, bytes)):
        raise WorkspaceStateError("Agent Lab suite result 必须提供 receipt_refs。")
    if "receipt:mag/production-live-acceptance/2026-05-20" not in receipt_refs:
        raise WorkspaceStateError("Agent Lab suite result 缺少 MAG production live acceptance receipt ref。")
    authority = require_mapping_payload(
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
    summary = require_mapping_payload(suite_result.get("summary"), context="agent_lab_suite_result.summary")
    value = summary.get(key)
    if not isinstance(value, int):
        raise WorkspaceStateError(f"agent_lab_suite_result.summary.{key} 必须是整数。")
    return value


def _extract_meta_agent_coordination_result(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    record = require_mapping_payload(payload, context="meta_agent_coordination_result")
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
    for key in PATCH_LOOP_REF_KEYS:
        if key in PATCH_LOOP_REF_LIST_KEYS:
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
