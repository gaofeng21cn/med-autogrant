from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.domain_handler_closeout import (
    _dispatch_codex_stage_receipts,
    _dispatch_executor_first_bundle,
    _dispatch_operator_readiness,
    _dispatch_physical_morphology_guard,
)
from med_autogrant.product_entry_parts.domain_handler_contract import (
    ALLOWED_ACTIONS,
    DOMAIN_HANDLER_ADAPTER_ID,
    DOMAIN_HANDLER_DISPATCH_KIND,
    DOMAIN_HANDLER_VERSION,
)
from med_autogrant.product_entry_parts.typed_blocker_projection import (
    build_typed_blocker_projection,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


def dispatch_domain_handler_task(
    product_entry: Any,
    *,
    task_path: str | Path,
) -> dict[str, Any]:
    resolved_task_path = Path(task_path).expanduser().resolve()
    task = _read_json_mapping(resolved_task_path, context="domain_handler_task")
    action = _require_nonempty_string_from_mapping(task, "action", context="domain_handler_task")
    if action not in ALLOWED_ACTIONS:
        raise WorkspaceStateError(f"domain_handler task action 不允许: {action}")
    input_path = _require_nonempty_string_from_mapping(task, "input_path", context="domain_handler_task")
    if action == "domain-memory/propose":
        return _dispatch_domain_memory_proposal(product_entry, task=task, input_path=input_path, task_path=resolved_task_path)
    if action == "domain-memory/decide":
        return _dispatch_domain_memory_decision(product_entry, task=task, input_path=input_path, task_path=resolved_task_path)
    if action == "stage-attempt/closeout":
        return _dispatch_stage_attempt_closeout(product_entry, task=task, input_path=input_path, task_path=resolved_task_path)
    if action == "lifecycle/receipt":
        return _dispatch_lifecycle_receipt(product_entry, task=task, input_path=input_path, task_path=resolved_task_path)
    if action == "closeout/codex-stage-receipts":
        return _dispatch_codex_stage_receipts(
            product_entry,
            task=task,
            input_path=input_path,
            task_path=resolved_task_path,
            dispatch_payload=_dispatch_payload,
        )
    if action == "closeout/operator-readiness":
        return _dispatch_operator_readiness(
            product_entry,
            task=task,
            input_path=input_path,
            task_path=resolved_task_path,
            dispatch_payload=_dispatch_payload,
        )
    if action == "closeout/physical-morphology-guard":
        return _dispatch_physical_morphology_guard(
            product_entry,
            task=task,
            input_path=input_path,
            task_path=resolved_task_path,
            dispatch_payload=_dispatch_payload,
        )
    if action == "closeout/executor-first-bundle":
        return _dispatch_executor_first_bundle(
            product_entry,
            task=task,
            input_path=input_path,
            task_path=resolved_task_path,
            dispatch_payload=_dispatch_payload,
        )
    raise WorkspaceStateError(f"domain_handler task action 不允许: {action}")


def _dispatch_domain_memory_proposal(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    proposal = product_entry.build_domain_memory_writeback_proposal(
        input_path=input_path,
        stage_id=_require_nonempty_string_from_mapping(task, "stage_id", context="domain_handler_task"),
        source_ref=_require_nonempty_string_from_mapping(task, "source_ref", context="domain_handler_task"),
        lesson_summary=_require_nonempty_string_from_mapping(task, "lesson_summary", context="domain_handler_task"),
        proposal_id=_optional_nonempty_string(task.get("proposal_id")),
    )
    return _dispatch_payload(
        action="domain-memory/propose",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "domain_handler_domain_memory_writeback_proposal_result",
            "proposal": proposal["domain_memory_writeback_proposal"],
            "write_policy": "runtime_store_only_no_repo_write",
        },
        executed_command=None,
    )


def _dispatch_domain_memory_decision(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    decision = product_entry.build_domain_memory_writeback_decision(
        proposal_path=_require_nonempty_string_from_mapping(task, "proposal_path", context="domain_handler_task"),
        decision=_require_nonempty_string_from_mapping(task, "decision", context="domain_handler_task"),
        decision_reason=_require_nonempty_string_from_mapping(task, "decision_reason", context="domain_handler_task"),
        memory_id=_optional_nonempty_string(task.get("memory_id")),
    )
    receipt_evidence = product_entry.write_domain_memory_receipt_evidence(
        decision_payload=decision,
        runtime_root=_optional_nonempty_string(task.get("runtime_root")),
    )
    return _dispatch_payload(
        action="domain-memory/decide",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "domain_handler_domain_memory_writeback_decision_result",
            "decision": decision["domain_memory_writeback_decision"],
            "receipt_evidence": receipt_evidence["domain_memory_receipt_evidence"],
            "write_policy": "runtime_store_only_no_repo_write",
        },
        executed_command=None,
    )


def _dispatch_stage_attempt_closeout(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    closeout_refs = _stage_attempt_closeout_refs(task)
    receipt_evidence = product_entry.write_owner_receipt_evidence(
        input_path=input_path,
        receipt_shape=_require_nonempty_string_from_mapping(task, "receipt_shape", context="domain_handler_task"),
        stage_id=_require_nonempty_string_from_mapping(task, "stage_id", context="domain_handler_task"),
        source_ref=_require_nonempty_string_from_mapping(task, "source_ref", context="domain_handler_task"),
        closeout_summary=_require_nonempty_string_from_mapping(task, "closeout_summary", context="domain_handler_task"),
        runtime_root=_optional_nonempty_string(task.get("runtime_root")),
        receipt_id=_optional_nonempty_string(task.get("receipt_id") or task.get("task_id")),
        closeout_refs=closeout_refs,
    )
    receipt = receipt_evidence["owner_receipt_evidence"]
    receipt_refs = _stage_attempt_receipt_refs(receipt)
    return _dispatch_payload(
        action="stage-attempt/closeout",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "domain_handler_stage_attempt_closeout_result",
            "return_shape": receipt["receipt_shape"],
            "receipt_ref": receipt["receipt_instance_ref"],
            "receipt_refs": receipt_refs,
            "closeout_refs": closeout_refs,
            "source_refs": list(receipt["source_refs"]),
            "consumed_memory_refs": _optional_string_list(task.get("consumed_memory_refs")),
            "writeback_receipt_refs": _optional_string_list(task.get("writeback_receipt_refs")),
            "owner_receipt_evidence": receipt,
            "write_policy": "runtime_receipt_instance_only_no_repo_write",
            "typed_blocker": _typed_blocker_for_receipt(
                receipt,
                blocker_kind="mag_stage_attempt_owner_receipt_required",
            ),
        },
        executed_command=None,
    )


def _dispatch_lifecycle_receipt(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    receipt_evidence = product_entry.write_lifecycle_receipt_evidence(
        input_path=input_path,
        operation=_require_nonempty_string_from_mapping(task, "operation", context="domain_handler_task"),
        receipt_shape=_require_nonempty_string_from_mapping(task, "receipt_shape", context="domain_handler_task"),
        source_ref=_require_nonempty_string_from_mapping(task, "source_ref", context="domain_handler_task"),
        closeout_summary=_require_nonempty_string_from_mapping(task, "closeout_summary", context="domain_handler_task"),
        runtime_root=_optional_nonempty_string(task.get("runtime_root")),
        receipt_id=_optional_nonempty_string(task.get("receipt_id") or task.get("task_id")),
    )
    receipt = receipt_evidence["lifecycle_receipt_evidence"]
    return _dispatch_payload(
        action="lifecycle/receipt",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "domain_handler_lifecycle_receipt_result",
            "return_shape": receipt["receipt_shape"],
            "receipt_ref": receipt["receipt_instance_ref"],
            "receipt_refs": {
                "lifecycle_receipt_ref": receipt["receipt_instance_ref"],
                "owner_receipt_contract_ref": receipt["owner_receipt_contract_ref"],
                "lifecycle_guarded_apply_proof_ref": receipt["lifecycle_guarded_apply_proof_ref"],
                "source_ref": receipt["source_ref"],
                "opl_consumes_receipt_ref_only": True,
            },
            "source_refs": list(receipt["source_refs"]),
            "lifecycle_receipt_evidence": receipt,
            "write_policy": "runtime_receipt_instance_only_no_repo_write",
            "typed_blocker": _typed_blocker_for_receipt(
                receipt,
                blocker_kind="mag_lifecycle_owner_receipt_required",
            ),
        },
        executed_command=None,
    )


def _dispatch_payload(
    *,
    action: str,
    task: Mapping[str, Any],
    task_path: Path,
    input_path: str,
    status: str,
    result: Mapping[str, Any],
    executed_command: str | None,
) -> dict[str, Any]:
    return {
        "ok": True,
        "command": "domain-handler-dispatch",
        "domain_handler_dispatch": {
            "surface_kind": DOMAIN_HANDLER_DISPATCH_KIND,
            "schema_version": DOMAIN_HANDLER_VERSION,
            "adapter_id": DOMAIN_HANDLER_ADAPTER_ID,
            "task_id": _optional_nonempty_string(task.get("task_id")) or f"{action}:{task_path.name}",
            "action": action,
            "status": status,
            "target_domain_id": TARGET_DOMAIN_ID,
            "caller_owner_contract": {
                "active_caller_owner": TARGET_DOMAIN_ID,
                "active_caller_surface": "mag_domain_handler_dispatch_handler_until_opl_caller_evidence",
                "target_caller_owner": "one-person-lab",
                "target_caller_surface": "opl_generated_or_hosted_domain_handler_dispatch",
                "domain_handler_target": TARGET_DOMAIN_ID,
                "domain_handler_owner": TARGET_DOMAIN_ID,
                "mag_role": "guarded_domain_handler_target_only",
                "claims_fully_cleaned": False,
                "mag_handler_boundary_ready": True,
                "external_opl_generated_or_hosted_caller_evidence_required": True,
            },
            "input_path": str(Path(input_path).expanduser().resolve()),
            "task_path": str(task_path),
            "executed_by_domain_handler": action
            in {
                "domain-memory/propose",
                "domain-memory/decide",
                "stage-attempt/closeout",
                "lifecycle/receipt",
                "closeout/codex-stage-receipts",
                "closeout/operator-readiness",
                "closeout/physical-morphology-guard",
                "closeout/executor-first-bundle",
            },
            "executed_command": executed_command,
            "result": dict(result),
            "receipt_refs": _receipt_refs_for_task(
                task=task,
                action=action,
                input_path=input_path,
            ),
            "guardrails": {
                "allowed_actions": sorted(ALLOWED_ACTIONS),
                "domain_truth_owner": TARGET_DOMAIN_ID,
                "opl_role": "generated_hosted_caller_and_typed_family_queue_control_plane",
                "hermes_role": "explicit_diagnostic_or_executor_proof_carrier_only",
                "hermes_proof_executor_default": False,
            },
        },
    }


def _typed_blocker_for_receipt(receipt: Mapping[str, Any], *, blocker_kind: str) -> dict[str, Any] | None:
    return build_typed_blocker_projection(receipt, blocker_kind=blocker_kind)


def _stage_attempt_closeout_refs(task: Mapping[str, Any]) -> dict[str, Any]:
    refs: dict[str, Any] = {
        "grant_transition_oracle_ref": _optional_nonempty_string(task.get("grant_transition_oracle_ref"))
        or "/product_entry_manifest/grant_transition_oracle",
        "controlled_soak_no_regression_attempt_ref": (
            "/product_entry_manifest/controlled_soak_no_regression_attempt"
        ),
        "domain_handler_stage_attempt_closeout_action": "stage-attempt/closeout",
    }
    transition_id = _optional_nonempty_string(task.get("transition_id"))
    if transition_id is not None:
        refs["transition_id"] = transition_id
    oracle_fixture_id = _optional_nonempty_string(task.get("oracle_fixture_id"))
    if oracle_fixture_id is not None:
        refs["oracle_fixture_id"] = oracle_fixture_id
    return refs


def _stage_attempt_receipt_refs(receipt: Mapping[str, Any]) -> dict[str, Any]:
    refs = {
        "owner_receipt_ref": receipt["receipt_instance_ref"],
        "owner_receipt_contract_ref": receipt["owner_receipt_contract_ref"],
        "source_ref": receipt["source_ref"],
        "opl_consumes_receipt_ref_only": True,
    }
    if receipt.get("receipt_shape") == "no_regression_evidence":
        refs["no_regression_evidence_ref"] = receipt["receipt_instance_ref"]
    return refs


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


def _optional_nonempty_string(value: Any) -> str | None:
    if value is None:
        return None
    return _require_nonempty_string(value, field_name="task_id", context="domain_handler_task")


def _optional_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError("domain_handler_task refs 必须是 string list。")
    refs: list[str] = []
    for item in value:
        refs.append(_require_nonempty_string(item, field_name="ref", context="domain_handler_task"))
    return refs


def _receipt_refs_for_task(
    *,
    task: Mapping[str, Any],
    action: str,
    input_path: str,
) -> dict[str, Any]:
    task_id = _optional_nonempty_string(task.get("task_id")) or f"{action}:ad-hoc"
    return {
        "receipt_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
        "domain_handler_dispatch_receipt_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
            f"domain_handler-dispatch/{task_id}.json"
        ),
        "input_path": str(Path(input_path).expanduser().resolve()),
        "write_policy": "receipt_ref_only_no_domain_truth_mutation",
        "opl_consumes_receipt_ref_only": True,
    }
