from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.domain_handler_contract import (
    ALLOWED_ACTIONS,
    DOMAIN_HANDLER_ADAPTER_ID,
    DOMAIN_HANDLER_EXPORT_KIND,
    DOMAIN_HANDLER_VERSION,
)
from med_autogrant.product_entry_parts.domain_handler_dispatch import dispatch_domain_handler_task
from med_autogrant.public_cli import public_cli_command
from med_autogrant.workspace_types import WorkspaceStateError


def build_domain_handler_export(
    product_entry: Any,
    *,
    input_path: str | Path,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    manifest_payload = product_entry.build_product_entry_manifest(input_path=resolved_input_path)
    surfaces = _collect_domain_handler_export_surfaces(manifest_payload)
    export_payload = _build_domain_handler_export_payload(manifest_payload, surfaces)
    return _build_domain_handler_export_response(manifest_payload, export_payload)


@dataclass(frozen=True)
class _DomainHandlerExportSurfaces:
    manifest: dict[str, Any]
    runtime_control: dict[str, Any]
    runtime_continuity: dict[str, Any]
    runtime_registration: dict[str, Any]
    standard_domain_agent_skeleton: dict[str, Any]
    controlled_stage_attempt: dict[str, Any]
    controlled_domain_memory_apply_proof: dict[str, Any]
    owner_receipt_contract: dict[str, Any]
    lifecycle_guarded_apply_proof: dict[str, Any]
    mag_consumer_thinning_contract: dict[str, Any]
    physical_skeleton_follow_through: dict[str, Any]
    ideal_state_closure_status: dict[str, Any]
    opl_substrate_adapter_export: dict[str, Any]
    source_provenance: dict[str, Any]
    automation: dict[str, Any]
    autonomy_observability: dict[str, Any]
    workspace_locator: dict[str, Any]
    artifact_locator_contract: dict[str, Any]
    user_loop_command: str


def _collect_domain_handler_export_surfaces(
    manifest_payload: dict[str, Any],
) -> _DomainHandlerExportSurfaces:
    manifest = _require_mapping(
        manifest_payload,
        "product_entry_manifest",
        context="domain_handler_export",
    )
    skill_catalog = _require_mapping(manifest, "skill_catalog", context="domain_handler_export.product_entry_manifest")
    skill = first_skill(skill_catalog)
    domain_projection = _require_mapping(skill, "domain_projection", context="domain_handler_export.skill_catalog.skill")
    runtime_control = _require_mapping(manifest, "runtime_control", context="domain_handler_export.product_entry_manifest")
    runtime_continuity = _require_mapping(
        domain_projection,
        "runtime_continuity",
        context="domain_handler_export.skill_catalog.domain_projection",
    )
    runtime_registration = _require_mapping(
        domain_projection,
        "opl_stage_runtime_registration",
        context="domain_handler_export.skill_catalog.domain_projection",
    )
    standard_domain_agent_skeleton = _require_mapping(
        domain_projection,
        "standard_domain_agent_skeleton",
        context="domain_handler_export.skill_catalog.domain_projection",
    )
    controlled_stage_attempt = _require_mapping(
        manifest,
        "controlled_stage_attempt_projection",
        context="domain_handler_export.product_entry_manifest",
    )
    controlled_domain_memory_apply_proof = _require_mapping(
        manifest,
        "controlled_domain_memory_apply_proof",
        context="domain_handler_export.product_entry_manifest",
    )
    owner_receipt_contract = _require_mapping(
        manifest,
        "owner_receipt_contract",
        context="domain_handler_export.product_entry_manifest",
    )
    lifecycle_guarded_apply_proof = _require_mapping(
        manifest,
        "lifecycle_guarded_apply_proof",
        context="domain_handler_export.product_entry_manifest",
    )
    mag_consumer_thinning_contract = _require_mapping(
        manifest,
        "mag_consumer_thinning_contract",
        context="domain_handler_export.product_entry_manifest",
    )
    physical_skeleton_follow_through = _require_mapping(
        manifest,
        "physical_skeleton_follow_through",
        context="domain_handler_export.product_entry_manifest",
    )
    ideal_state_closure_status = _require_mapping(
        manifest,
        "ideal_state_closure_status",
        context="domain_handler_export.product_entry_manifest",
    )
    opl_substrate_adapter_export = _require_mapping(
        manifest,
        "opl_substrate_adapter_export",
        context="domain_handler_export.product_entry_manifest",
    )
    source_provenance = _require_mapping(
        manifest,
        "source_provenance",
        context="domain_handler_export.product_entry_manifest",
    )
    automation = _require_mapping(manifest, "automation", context="domain_handler_export.product_entry_manifest")
    autonomy_observability = _require_mapping(
        manifest,
        "autonomy_observability",
        context="domain_handler_export.product_entry_manifest",
    )
    user_loop_command = _require_nonempty_string_from_mapping(
        _require_mapping(manifest, "operator_loop_surface", context="domain_handler_export.product_entry_manifest"),
        "command",
        context="domain_handler_export.operator_loop_surface",
    )
    workspace_locator = _require_mapping(
        manifest,
        "workspace_locator",
        context="domain_handler_export.product_entry_manifest",
    )
    artifact_locator_contract = _require_mapping(
        manifest,
        "artifact_locator_contract",
        context="domain_handler_export.product_entry_manifest",
    )
    return _DomainHandlerExportSurfaces(
        manifest=dict(manifest),
        runtime_control=dict(runtime_control),
        runtime_continuity=dict(runtime_continuity),
        runtime_registration=dict(runtime_registration),
        standard_domain_agent_skeleton=dict(standard_domain_agent_skeleton),
        controlled_stage_attempt=dict(controlled_stage_attempt),
        controlled_domain_memory_apply_proof=dict(controlled_domain_memory_apply_proof),
        owner_receipt_contract=dict(owner_receipt_contract),
        lifecycle_guarded_apply_proof=dict(lifecycle_guarded_apply_proof),
        mag_consumer_thinning_contract=dict(mag_consumer_thinning_contract),
        physical_skeleton_follow_through=dict(physical_skeleton_follow_through),
        ideal_state_closure_status=dict(ideal_state_closure_status),
        opl_substrate_adapter_export=dict(opl_substrate_adapter_export),
        source_provenance=dict(source_provenance),
        automation=dict(automation),
        autonomy_observability=dict(autonomy_observability),
        workspace_locator=dict(workspace_locator),
        artifact_locator_contract=dict(artifact_locator_contract),
        user_loop_command=user_loop_command,
    )


def _build_domain_handler_export_payload(
    manifest_payload: dict[str, Any],
    surfaces: _DomainHandlerExportSurfaces,
) -> dict[str, Any]:
    export_payload = {
        "surface_kind": DOMAIN_HANDLER_EXPORT_KIND,
        "schema_version": DOMAIN_HANDLER_VERSION,
        "adapter_id": DOMAIN_HANDLER_ADAPTER_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        **_build_domain_handler_shell_payload(
            manifest=surfaces.manifest,
            runtime_registration=surfaces.runtime_registration,
            automation=surfaces.automation,
            autonomy_observability=surfaces.autonomy_observability,
            user_loop_command=surfaces.user_loop_command,
        ),
        "workspace_locator": dict(surfaces.workspace_locator),
        "identity": {
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
        },
        "runtime_control": dict(surfaces.runtime_control),
        "runtime_continuity": dict(surfaces.runtime_continuity),
        "standard_domain_agent_skeleton": dict(surfaces.standard_domain_agent_skeleton),
        "artifact_locator_contract": dict(surfaces.artifact_locator_contract),
        "source_provenance": dict(surfaces.source_provenance),
        "opl_substrate_adapter_export": dict(surfaces.opl_substrate_adapter_export),
        "controlled_stage_attempt_projection": dict(surfaces.controlled_stage_attempt),
        "controlled_domain_memory_apply_proof": dict(surfaces.controlled_domain_memory_apply_proof),
        "owner_receipt_contract": dict(surfaces.owner_receipt_contract),
        "lifecycle_guarded_apply_proof": dict(surfaces.lifecycle_guarded_apply_proof),
        "mag_consumer_thinning_contract": dict(surfaces.mag_consumer_thinning_contract),
        **_build_consumer_thinning_export_surfaces(surfaces.mag_consumer_thinning_contract),
        "physical_skeleton_follow_through": dict(surfaces.physical_skeleton_follow_through),
        "ideal_state_closure_status": dict(surfaces.ideal_state_closure_status),
        "receipt_refs": _required_child_dict(
            surfaces.controlled_stage_attempt,
            "receipt_refs",
            context="domain_handler_export.controlled_stage_attempt_projection",
        ),
        "memory_receipt_refs": _required_child_dict(
            surfaces.controlled_domain_memory_apply_proof,
            "writeback_receipt_refs",
            context="domain_handler_export.controlled_domain_memory_apply_proof",
        ),
        "repo_source_layout_audit": _required_child_dict(
            surfaces.controlled_domain_memory_apply_proof,
            "repo_source_layout_audit",
            context="domain_handler_export.controlled_domain_memory_apply_proof",
        ),
    }
    return export_payload


def _build_consumer_thinning_export_surfaces(
    mag_consumer_thinning_contract: dict[str, Any],
) -> dict[str, Any]:
    return {
        "functional_harness_consumer_coverage": _required_child_dict(
            mag_consumer_thinning_contract,
            "functional_harness_consumer_coverage",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "privatized_functional_module_audit": _required_child_dict(
            mag_consumer_thinning_contract,
            "privatized_functional_module_audit",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "declarative_grant_pack_compiler_input": _required_child_dict(
            mag_consumer_thinning_contract,
            "declarative_grant_pack_compiler_input",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "generated_surface_handoff": _required_child_dict(
            mag_consumer_thinning_contract,
            "generated_surface_handoff",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "generated_hosted_default_caller_proof": _required_child_dict(
            mag_consumer_thinning_contract,
            "generated_hosted_default_caller_proof",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "minimal_authority_functions": list(
            mag_consumer_thinning_contract.get("minimal_authority_functions") or []
        ),
        "functional_followthrough_gap_classification": _required_child_dict(
            mag_consumer_thinning_contract,
            "functional_followthrough_gap_classification",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "external_evidence_request_pack": _required_child_dict(
            mag_consumer_thinning_contract,
            "external_evidence_request_pack",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "consumed_opl_standard_surfaces": _required_child_dict(
            mag_consumer_thinning_contract,
            "consumed_opl_standard_surfaces",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "opl_family_conflict_blocker_projection": _required_child_dict(
            mag_consumer_thinning_contract,
            "opl_family_conflict_blocker_projection",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
        "opl_runtime_observability_consumption": _required_child_dict(
            mag_consumer_thinning_contract,
            "opl_runtime_observability_consumption",
            context="domain_handler_export.mag_consumer_thinning_contract",
        ),
    }


def _build_domain_handler_shell_payload(
    *,
    manifest: dict[str, Any],
    runtime_registration: dict[str, Any],
    automation: dict[str, Any],
    autonomy_observability: dict[str, Any],
    user_loop_command: str,
) -> dict[str, Any]:
    return {
        "caller_owner_contract": _build_domain_handler_caller_owner_contract(),
        "substrate_boundary": _build_domain_handler_substrate_boundary(manifest),
        "todo_wakeup": _build_todo_wakeup_projection(
            automation=automation,
            manifest=manifest,
            user_loop_command=user_loop_command,
        ),
        "autonomy_controller": _build_autonomy_controller_projection(
            manifest=manifest,
            autonomy_observability=autonomy_observability,
        ),
        "user_loop_attention_queue": _build_attention_queue_projection(
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
                    context="domain_handler_export.runtime_registration",
                )
            ),
            "write_policy": "opl_index_only_no_grant_truth_writes",
            "substrate_adapter_export_ref": "/domain_handler_export/opl_substrate_adapter_export",
            "allowed_dispatch_actions": sorted(ALLOWED_ACTIONS),
            "replacement_expectations_ref": (
                "/domain_handler_export/mag_consumer_thinning_contract/opl_replacement_expectations"
            ),
        },
        "guardrails": {
            "dispatch_boundary": "OPL-hosted caller may invoke only MAG domain handler guarded actions.",
            "readback_boundary": {
                "active_caller_remains": "mag_direct_domain_handler_until_opl_caller_evidence",
                "grant_truth_write_authorized": False,
                "external_evidence_authorized_by_mag_repo": False,
                "physical_delete_authorized": False,
                "provider_completion_is_grant_ready": False,
                "provider_completion_is_submission_ready": False,
            },
            "forbidden_defaults": [
                "hermes_proof_executor",
                "grant_truth_mutation_by_opl",
                "quality_gate_override_by_opl",
                "submission_ready_gate_bypass",
            ],
        },
    }


def _build_domain_handler_caller_owner_contract() -> dict[str, Any]:
    return {
        "active_caller_owner": TARGET_DOMAIN_ID,
        "active_caller_surface": "mag_domain_handler_handler_until_opl_caller_evidence",
        "active_caller_readback_state": "mag_direct_domain_handler_active_until_opl_caller_evidence",
        "target_caller_owner": "one-person-lab",
        "target_caller_surface": "opl_generated_or_hosted_domain_handler",
        "domain_handler_target": TARGET_DOMAIN_ID,
        "domain_handler_owner": TARGET_DOMAIN_ID,
        "mag_role": "guarded_domain_handler_target_and_authority_refs_only",
        "claims_fully_cleaned": False,
        "mag_handler_boundary_ready": True,
        "external_opl_generated_or_hosted_caller_evidence_required": True,
        "opl_generated_or_hosted_caller_evidence_observed": False,
        "readback_guard": {
            "active_caller_owner_until_evidence": TARGET_DOMAIN_ID,
            "active_caller_surface_until_evidence": "mag_direct_domain_handler",
            "evidence_owner": "one-person-lab",
            "grant_truth_write_authorized": False,
            "external_evidence_authorized_by_mag_repo": False,
            "physical_delete_authorized": False,
            "provider_completion_is_grant_ready": False,
            "provider_completion_is_submission_ready": False,
        },
    }


def _build_domain_handler_substrate_boundary(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "online_substrate_owner": "explicit_opl_provider",
        "control_plane_owner": "one-person-lab",
        "domain_truth_owner": TARGET_DOMAIN_ID,
        "quality_gate_owner": TARGET_DOMAIN_ID,
        "artifact_owner": TARGET_DOMAIN_ID,
        "default_executor_owner": _default_executor_owner(manifest),
        "default_executor_note": (
            "Default executor remains Codex/domain-selected; OPL may explicitly choose "
            "a stage-led runtime provider for wakeup/control-plane carrier duties."
        ),
        "hermes_proof_executor_default": False,
    }


def _build_todo_wakeup_projection(
    *,
    automation: dict[str, Any],
    manifest: dict[str, Any],
    user_loop_command: str,
) -> dict[str, Any]:
    automations = automation.get("automations")
    if not isinstance(automations, list):
        raise WorkspaceStateError("domain_handler_export.automation 缺少 automations。")
    authoring_wakeup = next(
        (
            dict(item)
            for item in automations
            if isinstance(item, dict) and item.get("automation_id") == "mag.authoring_loop_continuation"
        ),
        None,
    )
    if authoring_wakeup is None:
        raise WorkspaceStateError("domain_handler_export 缺少 authoring loop continuation automation。")
    return {
        "surface_kind": "mag_todo_wakeup_projection",
        "explicit_wakeup_policy": "manual_or_opl_queue_triggered_authoring_loop_continuation",
        "todo_source_refs": [
            "/product_entry_manifest/remaining_gaps",
            "/product_entry_manifest/automation/automations/1",
            "/product_entry_manifest/autonomy_observability/attention_candidates",
        ],
        "remaining_gaps": list(manifest.get("remaining_gaps") or []),
        "authoring_loop_continuation": authoring_wakeup,
        "recommended_wakeup_command": user_loop_command,
        "opl_wakeup_contract": {
            "owner": "one-person-lab",
            "provider_role": "typed_family_queue_and_provider_wakeup_shell",
            "mag_role": "refs_only_authoring_continuation_action_target",
            "target_action_ref": "open_grant_user_loop",
            "target_surface": "opl_generated_grant_user_loop",
            "target_command": user_loop_command,
            "domain_handler_dispatch_action": None,
            "queue_write_policy": "enqueue_wakeup_only_no_grant_truth_writes",
            "required_return_shapes": [
                "domain_owner_receipt",
                "typed_blocker",
                "no_regression_evidence",
            ],
        },
        "forbidden_private_runtime_roles": {
            "hermes_24h_substrate_owner": False,
            "mag_scheduler_daemon_owner": False,
            "mag_attempt_ledger_owner": False,
            "mag_app_workbench_owner": False,
        },
        "opl_queue_role": "typed_family_queue_control_plane_only",
    }


def _build_autonomy_controller_projection(
    *,
    manifest: dict[str, Any],
    autonomy_observability: dict[str, Any],
) -> dict[str, Any]:
    workspace_path = _require_nonempty_string_from_mapping(
        _require_mapping(manifest, "workspace_locator", context="domain_handler_export.product_entry_manifest"),
        "workspace_path",
        context="domain_handler_export.workspace_locator",
    )
    return {
        "surface_kind": "mag_autonomy_controller_projection",
        "owner": "med-autogrant",
        "observability": dict(autonomy_observability),
        "execution_scope": "bounded_single_opl_provider_attempt",
        "mag_role": "refs_only_domain_authority_action_target",
        "post_start_residency_owner": "one-person-lab",
        "attempt_ledger_owner": "one-person-lab",
        "max_domain_cycles_per_invocation": 1,
        "mag_long_running_driver": False,
        "mag_scheduler_daemon_owner": False,
        "mag_attempt_ledger_owner": False,
        "allowed_return_shapes": [
            "domain_owner_receipt",
            "typed_blocker",
            "no_regression_evidence",
        ],
        "allowed_modes": ["dry_run", "guarded_run"],
        "default_mode": "dry_run",
        "command_template": public_cli_command(
            "execute-grant-autonomy-controller",
            "--input",
            workspace_path,
            "--output-dir",
            "<output-dir>",
            "--format",
            "json",
        ),
        "executor_override_allowed": False,
        "hermes_proof_executor_default": False,
    }


def _build_attention_queue_projection(
    *,
    manifest: dict[str, Any],
    autonomy_observability: dict[str, Any],
    user_loop_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_user_loop_attention_queue",
        "owner": "med-autogrant",
        "queue_owner": "one-person-lab",
        "queue_write_policy": "enqueue_wakeup_only_no_grant_truth_writes",
        "attention_candidates": list(autonomy_observability.get("attention_candidates") or []),
        "operator_loop_surface": dict(
            _require_mapping(manifest, "operator_loop_surface", context="domain_handler_export.product_entry_manifest")
        ),
        "recommended_wakeup_command": user_loop_command,
    }


def _default_executor_owner(manifest: dict[str, Any]) -> str:
    runtime_control = _require_mapping(manifest, "runtime_control", context="domain_handler_export.product_entry_manifest")
    return _require_nonempty_string_from_mapping(
        runtime_control,
        "executor_owner",
        context="domain_handler_export.runtime_control",
    )


def first_skill(skill_catalog: dict[str, Any]) -> dict[str, Any]:
    skills = skill_catalog.get("skills")
    if not isinstance(skills, list) or not skills or not isinstance(skills[0], dict):
        raise WorkspaceStateError("domain_handler_export.skill_catalog 缺少首个 skill。")
    return skills[0]


def _required_child_dict(
    payload: dict[str, Any],
    key: str,
    *,
    context: str,
) -> dict[str, Any]:
    return dict(_require_mapping(payload, key, context=context))


def _build_domain_handler_export_response(
    manifest_payload: dict[str, Any],
    export_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ok": True,
        "command": "domain-handler-export",
        "grant_run_id": manifest_payload["grant_run_id"],
        "workspace_id": manifest_payload["workspace_id"],
        "draft_id": manifest_payload["draft_id"],
        "lifecycle_stage": manifest_payload["lifecycle_stage"],
        "input_path": manifest_payload["input_path"],
        "domain_handler_export": export_payload,
    }
