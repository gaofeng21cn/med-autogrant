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
    DOMAIN_HANDLER_ADAPTER_ID,
    DOMAIN_HANDLER_EXPORT_KIND,
    DOMAIN_HANDLER_VERSION,
)
from med_autogrant.product_entry_parts.domain_handler_dispatch import dispatch_domain_handler_task
from med_autogrant.product_entry_parts.domain_handler_projection import (
    first_skill,
)
from med_autogrant.product_entry_parts.domain_handler_shell_projection import build_domain_handler_shell_payload


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
        **build_domain_handler_shell_payload(
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
