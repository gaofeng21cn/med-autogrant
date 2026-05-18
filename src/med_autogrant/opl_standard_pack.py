from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.action_catalog import build_mag_family_action_catalog
from med_autogrant.product_entry_parts.consumer_thinning import build_mag_consumer_thinning_contract
from med_autogrant.product_entry_parts.consumer_thinning_pack import (
    build_mag_minimal_authority_surface_taxonomy,
)
from med_autogrant.product_entry_parts.primitives import (
    GRANT_COCKPIT_KIND,
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    PRODUCT_STATUS_KIND,
    TARGET_DOMAIN_ID,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.stage_control_plane import build_mag_family_stage_control_plane
from opl_harness_shared.product_entry_companions import build_operator_loop_action_catalog


REPO_ROOT = Path(__file__).resolve().parents[2]
DOMAIN_LABEL = "Med Auto Grant"
GENERATED_SURFACE_OWNER = "one-person-lab"
INPUT_PLACEHOLDER = "<input_path>"
TASK_INTENT_PLACEHOLDER = "<task_intent>"
OUTPUT_DIR_PLACEHOLDER = "<output_dir>"

FORBIDDEN_GENERIC_OWNER_ROLES = [
    "generic_scheduler_owner",
    "generic_daemon_owner",
    "generic_lifecycle_owner",
    "generic_queue_owner",
    "generic_attempt_ledger_owner",
    "generic_state_machine_runner_owner",
    "generic_cli_mcp_product_wrapper_owner",
    "generic_sidecar_owner",
    "generic_session_store_owner",
    "generic_status_workbench_owner",
    "generic_workspace_source_intake_owner",
    "generic_memory_transport_owner",
    "generic_artifact_gallery_owner",
    "generic_operator_workbench_owner",
    "generic_observability_slo_owner",
    "generic_persistence_engine_owner",
    "generic_sqlite_lifecycle_owner",
    "generic_native_helper_envelope_owner",
    "generic_review_repair_transport_owner",
    "generated_surface_owner_in_domain_repo",
]

GENERATED_SURFACES = [
    "cli",
    "mcp",
    "skill",
    "product_entry_manifest",
    "sidecar_export_dispatch",
    "status_read_model",
    "workbench_drilldown",
    "functional_harness_cases",
]

DECLARATIVE_DOMAIN_PACK = [
    "stage_descriptors",
    "action_catalog",
    "transition_oracle",
    "funding_call_source_policy",
    "domain_memory_locator",
    "artifact_locator_contract",
    "owner_receipt_schema",
]

MINIMAL_AUTHORITY_FUNCTIONS = [
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "package_authority",
    "memory_accept_reject",
    "owner_receipt_signer",
    "grant_helper",
]


def _json_ready(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def build_standard_pack() -> dict[str, Any]:
    action_catalog = build_mag_family_action_catalog(
        action_commands=_base_operator_loop_actions(),
    )
    stage_control_plane = build_mag_family_stage_control_plane(
        family_action_catalog=action_catalog,
    )
    consumer_thinning_contract = build_mag_consumer_thinning_contract()

    return {
        "domain_descriptor": _domain_descriptor(),
        "pack_compiler_input": _pack_compiler_input(
            consumer_thinning_contract["minimal_authority_functions"]
        ),
        "generated_surface_handoff": _generated_surface_handoff(),
        "action_catalog": _with_forbidden_roles(action_catalog),
        "stage_control_plane": stage_control_plane,
        "memory_descriptor": _memory_descriptor(),
        "artifact_locator_contract": _artifact_locator_contract(),
        "owner_receipt_contract": _owner_receipt_contract(),
        "functional_privatization_audit": _functional_privatization_audit(consumer_thinning_contract),
        "private_functional_surface_policy": _private_functional_surface_policy(),
    }


def sync_standard_pack(*, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    contracts = build_standard_pack()
    contract_dir = repo_root / "contracts"
    contract_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for name, payload in contracts.items():
        relative = Path("contracts") / f"{name}.json"
        path = repo_root / relative
        path.write_text(
            json.dumps(_json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(str(relative))
    return {
        "surface_kind": "mag_opl_standard_pack_sync",
        "target_domain_id": TARGET_DOMAIN_ID,
        "written": written,
    }


def _base_operator_loop_actions() -> dict[str, Mapping[str, Any]]:
    command_catalog = {
        "grant_progress": public_cli_command(
            "grant-progress",
            "--input",
            INPUT_PLACEHOLDER,
            "--format",
            "json",
        ),
        "build_submission_ready_package": public_cli_command(
            "build-submission-ready-package",
            "--input",
            INPUT_PLACEHOLDER,
            "--output-dir",
            OUTPUT_DIR_PLACEHOLDER,
            "--format",
            "json",
        ),
    }
    return build_operator_loop_action_catalog(
        {
            "open_loop": {
                "command": public_cli_command(
                    "grant-user-loop",
                    "--input",
                    INPUT_PLACEHOLDER,
                    "--task-intent",
                    TASK_INTENT_PLACEHOLDER,
                    "--format",
                    "json",
                ),
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": "Open the MAG grant user loop through the existing domain action target.",
                "requires": ["input_path", "task_intent"],
            },
            "inspect_progress": {
                "command": command_catalog["grant_progress"],
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                "summary": "Read MAG grant progress through the existing domain action target.",
                "requires": ["input_path"],
            },
            "inspect_cockpit": {
                "command": public_cli_command(
                    "grant-cockpit",
                    "--input",
                    INPUT_PLACEHOLDER,
                    "--format",
                    "json",
                ),
                "surface_kind": GRANT_COCKPIT_KIND,
                "summary": "Read the MAG cockpit projection through the existing domain action target.",
                "requires": ["input_path"],
            },
            "build_direct_entry": {
                "command": public_cli_command(
                    "grant-direct-entry",
                    "--input",
                    INPUT_PLACEHOLDER,
                    "--task-intent",
                    TASK_INTENT_PLACEHOLDER,
                    "--format",
                    "json",
                ),
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                "summary": "Build a MAG direct-entry contract through the existing domain action target.",
                "requires": ["input_path", "task_intent"],
            },
            "build_submission_ready_package": {
                "command": command_catalog["build_submission_ready_package"],
                "surface_kind": "submission_ready_package",
                "summary": "Run the MAG submission-ready package gate through the existing domain action target.",
                "requires": ["input_path", "output_dir"],
            },
            "product_status": {
                "command": public_cli_command(
                    "product-status",
                    "--input",
                    INPUT_PLACEHOLDER,
                    "--format",
                    "json",
                ),
                "surface_kind": PRODUCT_STATUS_KIND,
                "summary": "Read MAG product status through the existing domain action target.",
                "requires": ["input_path"],
            },
        }
    )


def _domain_descriptor() -> dict[str, Any]:
    return {
        "surface_kind": "domain_agent_descriptor",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "domain_label": DOMAIN_LABEL,
        "package_role": "opl_standard_domain_agent",
        "generated_surface_owner": GENERATED_SURFACE_OWNER,
        "domain_repo_can_own_generated_surface": False,
        "standard_contract_refs": {
            "action_catalog": "contracts/action_catalog.json",
            "stage_control_plane": "contracts/stage_control_plane.json",
            "pack_compiler_input": "contracts/pack_compiler_input.json",
            "generated_surface_handoff": "contracts/generated_surface_handoff.json",
            "functional_privatization_audit": "contracts/functional_privatization_audit.json",
        },
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_owns_truth_quality_artifact_memory_and_receipts": True,
            "domain_truth_owner": TARGET_DOMAIN_ID,
        },
    }


def _pack_compiler_input(minimal_authority_surfaces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "surface_kind": "opl_domain_pack_compiler_input",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "domain_pack_owner": TARGET_DOMAIN_ID,
        "generated_surface_owner": GENERATED_SURFACE_OWNER,
        "declarative_domain_pack": DECLARATIVE_DOMAIN_PACK,
        "minimal_authority_functions": MINIMAL_AUTHORITY_FUNCTIONS,
        "minimal_authority_surface_taxonomy": build_mag_minimal_authority_surface_taxonomy(),
        "minimal_authority_surface_contracts": _json_ready(minimal_authority_surfaces),
        "generated_surfaces_requested": GENERATED_SURFACES,
        "domain_repo_can_own_generated_surface": False,
        "source_refs": {
            "action_catalog": "src/med_autogrant/action_catalog.py::build_mag_family_action_catalog",
            "stage_control_plane": "src/med_autogrant/stage_control_plane.py::build_mag_family_stage_control_plane",
            "functional_audit": (
                "src/med_autogrant/product_entry_parts/consumer_thinning.py::"
                "build_mag_consumer_thinning_contract"
            ),
        },
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_can_claim_generated_surface_owner": False,
        },
    }


def _generated_surface_handoff() -> dict[str, Any]:
    return {
        "surface_kind": "opl_generated_surface_handoff",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "generated_surface_owner": GENERATED_SURFACE_OWNER,
        "domain_repo_can_own_generated_surface": False,
        "source_contract_ref": "contracts/pack_compiler_input.json",
        "generated_surfaces": [
            {
                "surface_id": surface_id,
                "owner": GENERATED_SURFACE_OWNER,
                "domain_repo_can_own_generated_surface": False,
                "status": "descriptor_source_available",
            }
            for surface_id in GENERATED_SURFACES
        ],
        "required_domain_handoff": [
            "owner_receipt_schema",
            "typed_blocker_schema",
            "minimal_authority_function_refs",
            "no_forbidden_write_evidence",
        ],
    }


def _with_forbidden_roles(action_catalog: Mapping[str, Any]) -> dict[str, Any]:
    payload = dict(action_catalog)
    payload["forbidden_generic_owner_roles"] = FORBIDDEN_GENERIC_OWNER_ROLES
    payload["generated_surface_owner"] = GENERATED_SURFACE_OWNER
    payload["domain_repo_can_own_generated_surface"] = False
    return payload


def _memory_descriptor() -> dict[str, Any]:
    return {
        "surface_kind": "domain_memory_descriptor_locator",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "memory_body_owner": TARGET_DOMAIN_ID,
        "opl_projection_policy": "locator_and_receipt_refs_only",
        "authority_boundary": {
            "opl_can_write_memory_body": False,
            "opl_can_accept_or_reject_writeback": False,
            "domain_memory_accept_reject_owner": TARGET_DOMAIN_ID,
        },
    }


def _artifact_locator_contract() -> dict[str, Any]:
    return {
        "surface_kind": "artifact_locator_contract",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "canonical_artifact_authority": TARGET_DOMAIN_ID,
        "opl_projection_policy": "locator_lifecycle_and_receipt_refs_only",
        "authority_boundary": {
            "opl_can_mutate_artifacts": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_artifact_authority_owner": TARGET_DOMAIN_ID,
        },
    }


def _owner_receipt_contract() -> dict[str, Any]:
    return {
        "surface_kind": "owner_receipt_contract",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "allowed_receipt_classes": [
            "owner_receipt",
            "typed_blocker",
            "no_regression_evidence",
            "memory_writeback_receipt",
            "artifact_lifecycle_receipt",
        ],
        "forbidden_claims": [
            "opl_authorized_domain_ready",
            "opl_authorized_quality_or_export_verdict",
            "opl_wrote_domain_truth",
            "opl_wrote_memory_body",
        ],
    }


def _functional_privatization_audit(consumer_thinning_contract: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "surface_kind": "functional_privatization_audit",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "mag_consumer_thinning_contract": dict(consumer_thinning_contract),
        "privatized_functional_module_audit": dict(consumer_thinning_contract["privatized_functional_module_audit"]),
        "functional_followthrough_gap_classification": dict(
            consumer_thinning_contract["functional_followthrough_gap_classification"]
        ),
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_can_claim_generic_runtime_owner": False,
            "domain_repo_can_own_generated_surface": False,
        },
    }


def _private_functional_surface_policy() -> dict[str, Any]:
    return {
        "surface_kind": "opl_domain_private_functional_surface_admission_policy",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "default_posture": "forbidden_until_classified_and_receipted",
        "forbidden_private_surface_classes": [
            "generic_scheduler",
            "generic_queue_or_attempt_ledger",
            "generic_cli_mcp_product_wrapper",
            "generic_workbench_shell",
            "generic_observability_runtime",
        ],
        "allowed_private_surface_classes": [
            "minimal_authority_function",
            "grant_native_helper_implementation",
            "ai_first_verdict_ref_materializer",
        ],
        "forbidden_generic_owner_roles": FORBIDDEN_GENERIC_OWNER_ROLES,
    }


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync MAG OPL standard domain-agent pack contracts.")
    parser.add_argument("--check", action="store_true", help="Print the generated pack without writing.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.check:
        print(json.dumps(build_standard_pack(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(json.dumps(sync_standard_pack(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
