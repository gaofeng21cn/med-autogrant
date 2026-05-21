from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.sidecar_contract import (
    ALLOWED_ACTIONS,
    SIDECAR_ADAPTER_ID,
    SIDECAR_EXPORT_KIND,
    SIDECAR_VERSION,
)
from med_autogrant.product_entry_parts.sidecar_dispatch import dispatch_sidecar_task
from med_autogrant.product_entry_parts.sidecar_projection import (
    build_attention_queue_projection,
    build_autonomy_controller_projection,
    build_todo_wakeup_projection,
    default_executor_owner,
    first_skill,
)


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
