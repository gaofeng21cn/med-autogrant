from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.sidecar_contract import (
    ALLOWED_ACTIONS,
    SIDECAR_ADAPTER_ID,
    SIDECAR_DISPATCH_KIND,
    SIDECAR_EXPORT_KIND,
    SIDECAR_VERSION,
)
from med_autogrant.product_entry_parts.sidecar_closeout import (
    _dispatch_codex_stage_receipts,
    _dispatch_executor_first_bundle,
    _dispatch_operator_readiness,
    _dispatch_physical_morphology_guard,
)
from med_autogrant.product_entry_parts.sidecar_projection import (
    build_attention_queue_projection,
    build_autonomy_controller_projection,
    build_todo_wakeup_projection,
    default_executor_owner,
    first_skill,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


def build_sidecar_export(
    product_entry: Any,
    *,
    input_path: str | Path,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    manifest_payload = product_entry.build_product_entry_manifest(input_path=resolved_input_path)
    manifest = _require_mapping(
        manifest_payload,
        "product_entry_manifest",
        context="sidecar_export",
    )
    skill_catalog = _require_mapping(manifest, "skill_catalog", context="sidecar_export.product_entry_manifest")
    skill = first_skill(skill_catalog)
    domain_projection = _require_mapping(skill, "domain_projection", context="sidecar_export.skill_catalog.skill")
    runtime_control = _require_mapping(manifest, "runtime_control", context="sidecar_export.product_entry_manifest")
    runtime_continuity = _require_mapping(
        domain_projection,
        "runtime_continuity",
        context="sidecar_export.skill_catalog.domain_projection",
    )
    runtime_registration = _require_mapping(
        domain_projection,
        "opl_stage_runtime_registration",
        context="sidecar_export.skill_catalog.domain_projection",
    )
    standard_domain_agent_skeleton = _require_mapping(
        domain_projection,
        "standard_domain_agent_skeleton",
        context="sidecar_export.skill_catalog.domain_projection",
    )
    controlled_stage_attempt = _require_mapping(
        manifest,
        "controlled_stage_attempt_projection",
        context="sidecar_export.product_entry_manifest",
    )
    controlled_domain_memory_apply_proof = _require_mapping(
        manifest,
        "controlled_domain_memory_apply_proof",
        context="sidecar_export.product_entry_manifest",
    )
    owner_receipt_contract = _require_mapping(
        manifest,
        "owner_receipt_contract",
        context="sidecar_export.product_entry_manifest",
    )
    lifecycle_guarded_apply_proof = _require_mapping(
        manifest,
        "lifecycle_guarded_apply_proof",
        context="sidecar_export.product_entry_manifest",
    )
    mag_consumer_thinning_contract = _require_mapping(
        manifest,
        "mag_consumer_thinning_contract",
        context="sidecar_export.product_entry_manifest",
    )
    physical_skeleton_follow_through = _require_mapping(
        manifest,
        "physical_skeleton_follow_through",
        context="sidecar_export.product_entry_manifest",
    )
    ideal_state_closure_status = _require_mapping(
        manifest,
        "ideal_state_closure_status",
        context="sidecar_export.product_entry_manifest",
    )
    opl_substrate_adapter_export = _require_mapping(
        manifest,
        "opl_substrate_adapter_export",
        context="sidecar_export.product_entry_manifest",
    )
    source_provenance = _require_mapping(
        manifest,
        "source_provenance",
        context="sidecar_export.product_entry_manifest",
    )
    automation = _require_mapping(manifest, "automation", context="sidecar_export.product_entry_manifest")
    autonomy_observability = _require_mapping(
        manifest,
        "autonomy_observability",
        context="sidecar_export.product_entry_manifest",
    )
    user_loop_command = _require_nonempty_string_from_mapping(
        _require_mapping(manifest, "operator_loop_surface", context="sidecar_export.product_entry_manifest"),
        "command",
        context="sidecar_export.operator_loop_surface",
    )
    export_payload = {
        "surface_kind": SIDECAR_EXPORT_KIND,
        "schema_version": SIDECAR_VERSION,
        "adapter_id": SIDECAR_ADAPTER_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "caller_owner_contract": {
            "active_caller_owner": TARGET_DOMAIN_ID,
            "active_caller_surface": "mag_product_sidecar_handler_until_opl_caller_evidence",
            "target_caller_owner": "one-person-lab",
            "target_caller_surface": "opl_generated_or_hosted_sidecar",
            "domain_handler_target": TARGET_DOMAIN_ID,
            "domain_handler_owner": TARGET_DOMAIN_ID,
            "mag_role": "guarded_domain_handler_target_and_authority_refs_only",
            "claims_fully_cleaned": False,
            "mag_handler_boundary_ready": True,
            "external_opl_generated_or_hosted_caller_evidence_required": True,
        },
        "substrate_boundary": {
            "online_substrate_owner": "explicit_opl_provider",
            "control_plane_owner": "one-person-lab",
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "quality_gate_owner": TARGET_DOMAIN_ID,
            "artifact_owner": TARGET_DOMAIN_ID,
            "default_executor_owner": default_executor_owner(manifest),
            "default_executor_note": (
                "Default executor remains Codex/domain-selected; OPL may explicitly choose "
                "a stage-led runtime provider for wakeup/control-plane carrier duties."
            ),
            "hermes_proof_executor_default": False,
        },
        "workspace_locator": dict(
            _require_mapping(manifest, "workspace_locator", context="sidecar_export.product_entry_manifest")
        ),
        "identity": {
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
        },
        "runtime_control": dict(runtime_control),
        "runtime_continuity": dict(runtime_continuity),
        "standard_domain_agent_skeleton": dict(standard_domain_agent_skeleton),
        "artifact_locator_contract": dict(
            _require_mapping(manifest, "artifact_locator_contract", context="sidecar_export.product_entry_manifest")
        ),
        "source_provenance": dict(source_provenance),
        "opl_substrate_adapter_export": dict(opl_substrate_adapter_export),
        "controlled_stage_attempt_projection": dict(controlled_stage_attempt),
        "controlled_domain_memory_apply_proof": dict(controlled_domain_memory_apply_proof),
        "owner_receipt_contract": dict(owner_receipt_contract),
        "lifecycle_guarded_apply_proof": dict(lifecycle_guarded_apply_proof),
        "mag_consumer_thinning_contract": dict(mag_consumer_thinning_contract),
        "functional_harness_consumer_coverage": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "functional_harness_consumer_coverage",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "privatized_functional_module_audit": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "privatized_functional_module_audit",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "declarative_grant_pack_compiler_input": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "declarative_grant_pack_compiler_input",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "generated_surface_handoff": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "generated_surface_handoff",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "generated_hosted_default_caller_proof": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "generated_hosted_default_caller_proof",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "minimal_authority_functions": list(
            mag_consumer_thinning_contract.get("minimal_authority_functions") or []
        ),
        "functional_followthrough_gap_classification": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "functional_followthrough_gap_classification",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "external_evidence_request_pack": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "external_evidence_request_pack",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "consumed_opl_standard_surfaces": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "consumed_opl_standard_surfaces",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "opl_family_conflict_blocker_projection": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "opl_family_conflict_blocker_projection",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "opl_runtime_observability_consumption": dict(
            _require_mapping(
                mag_consumer_thinning_contract,
                "opl_runtime_observability_consumption",
                context="sidecar_export.mag_consumer_thinning_contract",
            )
        ),
        "physical_skeleton_follow_through": dict(physical_skeleton_follow_through),
        "ideal_state_closure_status": dict(ideal_state_closure_status),
        "receipt_refs": dict(
            _require_mapping(
                controlled_stage_attempt,
                "receipt_refs",
                context="sidecar_export.controlled_stage_attempt_projection",
            )
        ),
        "memory_receipt_refs": dict(
            _require_mapping(
                controlled_domain_memory_apply_proof,
                "writeback_receipt_refs",
                context="sidecar_export.controlled_domain_memory_apply_proof",
            )
        ),
        "repo_source_layout_audit": dict(
            _require_mapping(
                controlled_domain_memory_apply_proof,
                "repo_source_layout_audit",
                context="sidecar_export.controlled_domain_memory_apply_proof",
            )
        ),
        "todo_wakeup": build_todo_wakeup_projection(
            automation=automation,
            manifest=manifest,
            user_loop_command=user_loop_command,
        ),
        "autonomy_controller": build_autonomy_controller_projection(
            manifest=manifest,
            autonomy_observability=autonomy_observability,
        ),
        "user_loop_attention_queue": build_attention_queue_projection(
            manifest=manifest,
            autonomy_observability=autonomy_observability,
            user_loop_command=user_loop_command,
        ),
        "opl_control_plane": {
            "registration": dict(runtime_registration),
            "family_lifecycle_adapter": dict(
                _require_mapping(
                    runtime_registration,
                    "family_lifecycle_adapter",
                    context="sidecar_export.runtime_registration",
                )
            ),
            "write_policy": "opl_index_only_no_grant_truth_writes",
            "substrate_adapter_export_ref": "/sidecar_export/opl_substrate_adapter_export",
            "allowed_dispatch_actions": sorted(ALLOWED_ACTIONS),
            "replacement_expectations_ref": (
                "/sidecar_export/mag_consumer_thinning_contract/opl_replacement_expectations"
            ),
        },
        "guardrails": {
            "dispatch_boundary": "OPL-hosted caller may invoke only MAG domain handler guarded actions.",
            "forbidden_defaults": [
                "hermes_proof_executor",
                "grant_truth_mutation_by_opl",
                "quality_gate_override_by_opl",
                "submission_ready_gate_bypass",
            ],
        },
    }
    return {
        "ok": True,
        "command": "product-sidecar-export",
        "grant_run_id": manifest_payload["grant_run_id"],
        "workspace_id": manifest_payload["workspace_id"],
        "draft_id": manifest_payload["draft_id"],
        "lifecycle_stage": manifest_payload["lifecycle_stage"],
        "input_path": manifest_payload["input_path"],
        "sidecar_export": export_payload,
    }


def dispatch_sidecar_task(
    product_entry: Any,
    *,
    task_path: str | Path,
) -> dict[str, Any]:
    resolved_task_path = Path(task_path).expanduser().resolve()
    task = _read_json_mapping(resolved_task_path, context="sidecar_task")
    action = _require_nonempty_string_from_mapping(task, "action", context="sidecar_task")
    if action not in ALLOWED_ACTIONS:
        raise WorkspaceStateError(f"sidecar task action 不允许: {action}")
    input_path = _require_nonempty_string_from_mapping(task, "input_path", context="sidecar_task")
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
    raise WorkspaceStateError(f"sidecar task action 不允许: {action}")


def _dispatch_domain_memory_proposal(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    proposal = product_entry.build_domain_memory_writeback_proposal(
        input_path=input_path,
        stage_id=_require_nonempty_string_from_mapping(task, "stage_id", context="sidecar_task"),
        source_ref=_require_nonempty_string_from_mapping(task, "source_ref", context="sidecar_task"),
        lesson_summary=_require_nonempty_string_from_mapping(task, "lesson_summary", context="sidecar_task"),
        proposal_id=_optional_nonempty_string(task.get("proposal_id")),
    )
    return _dispatch_payload(
        action="domain-memory/propose",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "sidecar_domain_memory_writeback_proposal_result",
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
        proposal_path=_require_nonempty_string_from_mapping(task, "proposal_path", context="sidecar_task"),
        decision=_require_nonempty_string_from_mapping(task, "decision", context="sidecar_task"),
        decision_reason=_require_nonempty_string_from_mapping(task, "decision_reason", context="sidecar_task"),
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
            "surface_kind": "sidecar_domain_memory_writeback_decision_result",
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
        receipt_shape=_require_nonempty_string_from_mapping(task, "receipt_shape", context="sidecar_task"),
        stage_id=_require_nonempty_string_from_mapping(task, "stage_id", context="sidecar_task"),
        source_ref=_require_nonempty_string_from_mapping(task, "source_ref", context="sidecar_task"),
        closeout_summary=_require_nonempty_string_from_mapping(task, "closeout_summary", context="sidecar_task"),
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
            "surface_kind": "sidecar_stage_attempt_closeout_result",
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
        operation=_require_nonempty_string_from_mapping(task, "operation", context="sidecar_task"),
        receipt_shape=_require_nonempty_string_from_mapping(task, "receipt_shape", context="sidecar_task"),
        source_ref=_require_nonempty_string_from_mapping(task, "source_ref", context="sidecar_task"),
        closeout_summary=_require_nonempty_string_from_mapping(task, "closeout_summary", context="sidecar_task"),
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
            "surface_kind": "sidecar_lifecycle_receipt_result",
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
        "command": "product-sidecar-dispatch",
        "sidecar_dispatch": {
            "surface_kind": SIDECAR_DISPATCH_KIND,
            "schema_version": SIDECAR_VERSION,
            "adapter_id": SIDECAR_ADAPTER_ID,
            "task_id": _optional_nonempty_string(task.get("task_id")) or f"{action}:{task_path.name}",
            "action": action,
            "status": status,
            "target_domain_id": TARGET_DOMAIN_ID,
            "caller_owner_contract": {
                "active_caller_owner": TARGET_DOMAIN_ID,
                "active_caller_surface": "mag_product_sidecar_dispatch_handler_until_opl_caller_evidence",
                "target_caller_owner": "one-person-lab",
                "target_caller_surface": "opl_generated_or_hosted_sidecar_dispatch",
                "domain_handler_target": TARGET_DOMAIN_ID,
                "domain_handler_owner": TARGET_DOMAIN_ID,
                "mag_role": "guarded_domain_handler_target_only",
                "claims_fully_cleaned": False,
                "mag_handler_boundary_ready": True,
                "external_opl_generated_or_hosted_caller_evidence_required": True,
            },
            "input_path": str(Path(input_path).expanduser().resolve()),
            "task_path": str(task_path),
            "executed_by_sidecar": action
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
    if receipt.get("receipt_shape") != "typed_blocker":
        return None
    return {
        "blocker_kind": blocker_kind,
        "owner": TARGET_DOMAIN_ID,
        "receipt_ref": receipt.get("receipt_instance_ref"),
        "source_ref": receipt.get("source_ref"),
        "next_action": "Route the blocker back to MAG owner surface before mutating grant truth, memory body, or artifact content.",
    }


def _stage_attempt_closeout_refs(task: Mapping[str, Any]) -> dict[str, Any]:
    refs: dict[str, Any] = {
        "grant_transition_oracle_ref": _optional_nonempty_string(task.get("grant_transition_oracle_ref"))
        or "/product_entry_manifest/grant_transition_oracle",
        "controlled_soak_no_regression_attempt_ref": (
            "/product_entry_manifest/controlled_soak_no_regression_attempt"
        ),
        "sidecar_stage_attempt_closeout_action": "stage-attempt/closeout",
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
    return _require_nonempty_string(value, field_name="task_id", context="sidecar_task")


def _optional_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError("sidecar_task refs 必须是 string list。")
    refs: list[str] = []
    for item in value:
        refs.append(_require_nonempty_string(item, field_name="ref", context="sidecar_task"))
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
        "sidecar_dispatch_receipt_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
            f"sidecar-dispatch/{task_id}.json"
        ),
        "input_path": str(Path(input_path).expanduser().resolve()),
        "write_policy": "receipt_ref_only_no_domain_truth_mutation",
        "opl_consumes_receipt_ref_only": True,
    }
