from __future__ import annotations

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

from med_autogrant.opl_standard_pack_source_policy_parts.false_ready_patterns import (
    _domain_readiness_false_ready_patterns,
    _generated_hosted_surface_false_ready_patterns,
    _private_wrapper_retirement_false_ready_patterns,
    _strict_source_purity_false_ready_patterns,
)

ACTIVE_PATH_SCAN_POLICY = {
    "surface_kind": "mag_active_path_scan_policy",
    "policy_id": "mag.active_path.current_role_guard.policy.v1",
    "target_domain_id": TARGET_DOMAIN_ID,
    "state": "contract_owned_current_role_guard_policy",
    "roots": ["src", "tests", "schemas", "contracts", "scripts", "plugins"],
    "files": ["Makefile", "pyproject.toml", ".agents/plugins/marketplace.json"],
    "suffixes": [".json", ".py", ".sh", ".toml", ".yaml", ".yml"],
    "excludes_human_docs": True,
    "human_doc_policy": (
        "docs/history/provenance may name retired surfaces without making them default callers"
    ),
    "scans_repo_source_only": True,
    "forbidden_active_paths": [
        "tests/test_product_entry.py",
        "src/med_autogrant/domain_runtime_parts/patch_targets.py",
        "src/med_autogrant/gateway.py",
        "src/med_autogrant/local_manager.py",
        "src/med_autogrant/" + "host" + "_agent.py",
    ],
    "forbidden_role_patterns": [
        {
            "pattern_id": "domain_runtime_patch_bridge_import",
            "literal_parts": ["med_autogrant.domain_runtime_parts", ".patch_targets"],
            "policy": "patch runtime owner modules directly; do not use retired facade patch bridge",
        },
        {
            "pattern_id": "hermes_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "hermes_agent", "\""],
            "policy": "Hermes-Agent remains explicit proof/provider provenance only",
        },
        {
            "pattern_id": "hermes_default_executor_owner",
            "literal_parts": ["DEFAULT_EXECUTOR_OWNER = \"", "hermes_agent", "\""],
            "policy": "default executor stays Codex CLI",
        },
        {
            "pattern_id": "claude_default_executor_owner",
            "literal_parts": ["DEFAULT_EXECUTOR_OWNER = \"", "claude_code", "\""],
            "policy": "non-default executors require explicit OPL adapter selection",
        },
        {
            "pattern_id": "gateway_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "gateway", "\""],
            "policy": "Gateway/local-manager wording is retired from active runtime ownership",
        },
        {
            "pattern_id": "local_manager_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "local_manager", "\""],
            "policy": "local-manager is not a default product/runtime owner",
        },
        {
            "pattern_id": "host" + "_agent_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "host" + "_agent", "\""],
            "policy": "repo-local host-agent runtime is not a product owner",
        },
        {
            "pattern_id": "json_hermes_default_executor",
            "literal_parts": ["\"default_executor_name\": \"", "hermes_agent", "\""],
            "policy": "manifest/contracts must keep Codex CLI as default executor",
        },
        {
            "pattern_id": "json_generated_surface_owner_points_to_mag",
            "literal_parts": ["\"generated_surface_owner\": \"", "med-autogrant", "\""],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "json_generated_surface_owner_points_to_mag_domain_id",
            "literal_parts": ["\"generated_surface_owner\": \"", "medautogrant", "\""],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "python_generated_surface_owner_points_to_mag",
            "literal_parts": ["'generated_surface_owner': '", "med-autogrant", "'"],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "python_generated_surface_owner_points_to_mag_domain_id",
            "literal_parts": ["'generated_surface_owner': '", "medautogrant", "'"],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "toml_generated_surface_owner_points_to_mag",
            "literal_parts": ["generated_surface_owner", " = \"", "med-autogrant", "\""],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "toml_generated_surface_owner_points_to_mag_domain_id",
            "literal_parts": ["generated_surface_owner", " = \"", "medautogrant", "\""],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "yaml_generated_surface_owner_points_to_mag",
            "literal_parts": ["generated_surface_owner: ", "med-autogrant"],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "yaml_generated_surface_owner_points_to_mag_domain_id",
            "literal_parts": ["generated_surface_owner: ", "medautogrant"],
            "policy": "generated/hosted surfaces stay owned by OPL Framework, not MAG",
        },
        {
            "pattern_id": "json_generated_surface_owner_in_mag_allowed_true",
            "literal_parts": ["\"generated_surface_owner_in_mag_allowed\": true"],
            "policy": "MAG must not re-open generated surface ownership after retirement",
        },
        {
            "pattern_id": "python_generated_surface_owner_in_mag_allowed_true",
            "literal_parts": ["\"generated_surface_owner_in_mag_allowed\": True"],
            "policy": "MAG must not re-open generated surface ownership after retirement",
        },
        {
            "pattern_id": "toml_generated_surface_owner_in_mag_allowed_true",
            "literal_parts": ["generated_surface_owner_in_mag_allowed", " = true"],
            "policy": "MAG must not re-open generated surface ownership after retirement",
        },
        {
            "pattern_id": "json_domain_can_claim_generated_surface_owner_true",
            "literal_parts": ["\"domain_can_claim_generated_surface_owner\": true"],
            "policy": "domain pack compiler input must keep generated surface ownership in OPL",
        },
        {
            "pattern_id": "python_domain_can_claim_generated_surface_owner_true",
            "literal_parts": ["\"domain_can_claim_generated_surface_owner\": True"],
            "policy": "domain pack compiler input must keep generated surface ownership in OPL",
        },
        {
            "pattern_id": "toml_domain_can_claim_generated_surface_owner_true",
            "literal_parts": ["domain_can_claim_generated_surface_owner", " = true"],
            "policy": "domain pack compiler input must keep generated surface ownership in OPL",
        },
        {
            "pattern_id": "json_mag_can_own_generated_wrapper_true",
            "literal_parts": ["\"mag_can_own_generated_wrapper\": true"],
            "policy": "MAG authority boundary must not claim generated wrapper ownership",
        },
        {
            "pattern_id": "python_mag_can_own_generated_wrapper_true",
            "literal_parts": ["\"mag_can_own_generated_wrapper\": True"],
            "policy": "MAG authority boundary must not claim generated wrapper ownership",
        },
        {
            "pattern_id": "json_mag_claims_default_caller_cutover_complete_true",
            "literal_parts": ["\"mag_claims_default_caller_cutover_complete\": true"],
            "policy": (
                "MAG repo-local refs-only evidence cannot claim generated/default caller cutover complete"
            ),
        },
        {
            "pattern_id": "python_mag_claims_default_caller_cutover_complete_true",
            "literal_parts": ["\"mag_claims_default_caller_cutover_complete\": True"],
            "policy": (
                "MAG repo-local refs-only evidence cannot claim generated/default caller cutover complete"
            ),
        },
        {
            "pattern_id": "python_single_mag_claims_default_caller_cutover_complete_true",
            "literal_parts": ["'mag_claims_default_caller_", "cutover_complete': True"],
            "policy": (
                "MAG repo-local refs-only evidence cannot claim generated/default caller cutover complete"
            ),
        },
        {
            "pattern_id": "toml_mag_claims_default_caller_cutover_complete_true",
            "literal_parts": ["mag_claims_default_caller_cutover_complete", " = true"],
            "policy": (
                "MAG repo-local refs-only evidence cannot claim generated/default caller cutover complete"
            ),
        },
        {
            "pattern_id": "yaml_mag_claims_default_caller_cutover_complete_true",
            "literal_parts": ["mag_claims_default_caller_", "cutover_complete: true"],
            "policy": (
                "MAG repo-local refs-only evidence cannot claim generated/default caller cutover complete"
            ),
        },
        {
            "pattern_id": "json_claims_external_default_caller_consumption_complete_true",
            "literal_parts": [
                "\"claims_external_default_caller_consumption_complete\": true"
            ],
            "policy": (
                "External default-caller consumption completion requires external evidence, not MAG source claims"
            ),
        },
        {
            "pattern_id": "python_claims_external_default_caller_consumption_complete_true",
            "literal_parts": [
                "\"claims_external_default_caller_consumption_complete\": True"
            ],
            "policy": (
                "External default-caller consumption completion requires external evidence, not MAG source claims"
            ),
        },
        {
            "pattern_id": "python_single_claims_external_default_caller_consumption_complete_true",
            "literal_parts": [
                "'claims_external_default_caller_",
                "consumption_complete': True",
            ],
            "policy": (
                "External default-caller consumption completion requires external evidence, not MAG source claims"
            ),
        },
        {
            "pattern_id": "toml_claims_external_default_caller_consumption_complete_true",
            "literal_parts": [
                "claims_external_default_caller_consumption_complete",
                " = true",
            ],
            "policy": (
                "External default-caller consumption completion requires external evidence, not MAG source claims"
            ),
        },
        {
            "pattern_id": "yaml_claims_external_default_caller_consumption_complete_true",
            "literal_parts": [
                "claims_external_default_caller_",
                "consumption_complete: true",
            ],
            "policy": (
                "External default-caller consumption completion requires external evidence, not MAG source claims"
            ),
        },
        {
            "pattern_id": "json_claims_opl_generated_hosted_production_caller_complete_true",
            "literal_parts": [
                "\"claims_opl_generated_hosted_production_caller_complete\": true"
            ],
            "policy": (
                "OPL generated/hosted production caller completion is an external evidence tail"
            ),
        },
        {
            "pattern_id": "python_claims_opl_generated_hosted_production_caller_complete_true",
            "literal_parts": [
                "\"claims_opl_generated_hosted_production_caller_complete\": True"
            ],
            "policy": (
                "OPL generated/hosted production caller completion is an external evidence tail"
            ),
        },
        {
            "pattern_id": "python_single_claims_opl_generated_hosted_production_caller_complete_true",
            "literal_parts": [
                "'claims_opl_generated_hosted_",
                "production_caller_complete': True",
            ],
            "policy": (
                "OPL generated/hosted production caller completion is an external evidence tail"
            ),
        },
        {
            "pattern_id": "toml_claims_opl_generated_hosted_production_caller_complete_true",
            "literal_parts": [
                "claims_opl_generated_hosted_production_caller_complete",
                " = true",
            ],
            "policy": (
                "OPL generated/hosted production caller completion is an external evidence tail"
            ),
        },
        {
            "pattern_id": "yaml_claims_opl_generated_hosted_production_caller_complete_true",
            "literal_parts": [
                "claims_opl_generated_hosted_",
                "production_caller_complete: true",
            ],
            "policy": (
                "OPL generated/hosted production caller completion is an external evidence tail"
            ),
        },
        {
            "pattern_id": "json_domain_repo_physical_delete_authorized_true",
            "literal_parts": ["\"domain_repo_physical_delete_authorized\": true"],
            "policy": "Physical delete requires explicit MAG owner receipt, not refs-only source claims",
        },
        {
            "pattern_id": "python_domain_repo_physical_delete_authorized_true",
            "literal_parts": ["\"domain_repo_physical_delete_authorized\": True"],
            "policy": "Physical delete requires explicit MAG owner receipt, not refs-only source claims",
        },
        {
            "pattern_id": "python_single_domain_repo_physical_delete_authorized_true",
            "literal_parts": ["'domain_repo_physical_", "delete_authorized': True"],
            "policy": "Physical delete requires explicit MAG owner receipt, not refs-only source claims",
        },
        {
            "pattern_id": "toml_domain_repo_physical_delete_authorized_true",
            "literal_parts": ["domain_repo_physical_delete_authorized", " = true"],
            "policy": "Physical delete requires explicit MAG owner receipt, not refs-only source claims",
        },
        {
            "pattern_id": "yaml_domain_repo_physical_delete_authorized_true",
            "literal_parts": ["domain_repo_physical_", "delete_authorized: true"],
            "policy": "Physical delete requires explicit MAG owner receipt, not refs-only source claims",
        },
        {
            "pattern_id": "json_physical_delete_authorized_by_refs_true",
            "literal_parts": ["\"physical_delete_authorized_by_refs\": true"],
            "policy": "Refs-only evidence cannot authorize physical delete",
        },
        {
            "pattern_id": "python_physical_delete_authorized_by_refs_true",
            "literal_parts": ["\"physical_delete_authorized_by_refs\": True"],
            "policy": "Refs-only evidence cannot authorize physical delete",
        },
        {
            "pattern_id": "python_single_physical_delete_authorized_by_refs_true",
            "literal_parts": ["'physical_delete_authorized_", "by_refs': True"],
            "policy": "Refs-only evidence cannot authorize physical delete",
        },
        {
            "pattern_id": "toml_physical_delete_authorized_by_refs_true",
            "literal_parts": ["physical_delete_authorized_by_refs", " = true"],
            "policy": "Refs-only evidence cannot authorize physical delete",
        },
        {
            "pattern_id": "yaml_physical_delete_authorized_by_refs_true",
            "literal_parts": ["physical_delete_authorized_", "by_refs: true"],
            "policy": "Refs-only evidence cannot authorize physical delete",
        },
        *_private_wrapper_retirement_false_ready_patterns(),
        *_generated_hosted_surface_false_ready_patterns(),
        *_domain_readiness_false_ready_patterns(),
        *_strict_source_purity_false_ready_patterns(),
    ],
    "authority_boundary": {
        "policy_can_authorize_physical_delete": False,
        "policy_can_claim_production_long_run_soak": False,
        "policy_can_claim_grant_readiness": False,
    },
}
