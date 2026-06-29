from __future__ import annotations

DOMAIN_READINESS_FALSE_READY_CLAIM_KEYS = [
    "claims_grant_ready",
    "claims_fundability_ready",
    "claims_authoring_quality_ready",
    "claims_quality_ready",
    "claims_export_ready",
    "claims_submission_ready",
    "claims_submission_ready_export",
    "claims_production_ready",
    "grant_ready_claimed",
    "fundability_ready_claimed",
    "authoring_quality_ready_claimed",
    "quality_ready_claimed",
    "export_ready_claimed",
    "submission_ready_claimed",
    "production_ready_claimed",
]


PRIVATE_WRAPPER_RETIREMENT_FALSE_READY_CLAIM_KEYS = [
    "private_wrapper_retirement_complete",
    "private_platform_residue_retired",
    "legacy_wrapper_retirement_complete",
    "generic_wrapper_retirement_complete",
    "no_active_private_wrapper_caller_complete",
    "no_active_legacy_wrapper_caller_complete",
    "tombstone_provenance_complete",
    "wrapper_retirement_gate_satisfied",
    "physical_morphology_cleanup_complete",
    "retirement_readback_cleanup_complete",
    "retirement_readback_guard_satisfied",
    "cleanup_readback_physical_delete_authorized",
    "claims_private_wrapper_retired",
    "claims_private_platform_residue_retired",
    "claims_no_active_caller_complete",
    "claims_cleanup_readback_authorizes_delete",
    "claims_retirement_cleanup_applied",
]


GENERATED_HOSTED_SURFACE_FALSE_READY_CLAIM_KEYS = [
    "claims_app_workbench_live_rendering_complete",
    "claims_app_operator_sustained_consumption_complete",
    "claims_registry_discovery_live_complete",
    "claims_generated_hosted_surface_live_ready",
    "claims_default_caller_cutover_complete",
    "claims_generated_surface_consumption_complete",
    "app_workbench_live_rendering_complete",
    "app_operator_sustained_consumption_complete",
    "registry_discovery_live_complete",
    "generated_hosted_surface_live_ready",
    "default_caller_cutover_complete",
    "generated_surface_consumption_complete",
]


STRICT_SOURCE_PURITY_FALSE_READY_CLAIM_KEYS = [
    "strict_source_purity_complete",
    "source_purity_guard_satisfied",
    "active_path_scan_complete",
    "active_path_current_role_guard_complete",
    "source_ref_integrity_complete",
    "source_ref_integrity_guard_satisfied",
    "source_ref_integrity_can_claim_ready",
    "source_ref_integrity_can_authorize_delete",
    "machine_source_guard_can_claim_domain_ready",
]


def _domain_readiness_false_ready_patterns() -> list[dict[str, object]]:
    patterns: list[dict[str, object]] = []
    for claim_key in DOMAIN_READINESS_FALSE_READY_CLAIM_KEYS:
        policy = (
            "Domain readiness requires MAG owner verdicts, owner receipts, human-gate "
            "receipts, or typed blockers; repo source true flags are false-ready claims"
        )
        patterns.extend(
            [
                {
                    "pattern_id": f"json_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_single_{claim_key}_true",
                    "literal_parts": ["'", claim_key, "': True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"toml_{claim_key}_true",
                    "literal_parts": [claim_key, " = true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"yaml_{claim_key}_true",
                    "literal_parts": [claim_key, ": true"],
                    "policy": policy,
                },
            ]
        )
    return patterns


DOMAIN_READINESS_FALSE_READY_PATTERN_IDS = [
    pattern["pattern_id"] for pattern in _domain_readiness_false_ready_patterns()
]


def _private_wrapper_retirement_false_ready_patterns() -> list[dict[str, object]]:
    patterns: list[dict[str, object]] = []
    for claim_key in PRIVATE_WRAPPER_RETIREMENT_FALSE_READY_CLAIM_KEYS:
        policy = (
            "Private wrapper retirement requires explicit MAG owner receipt plus active-caller "
            "migration, direct/hosted parity, no-forbidden-write and tombstone/provenance evidence; "
            "repo source true flags are false-ready resurrection claims"
        )
        patterns.extend(
            [
                {
                    "pattern_id": f"json_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_single_{claim_key}_true",
                    "literal_parts": ["'", claim_key, "': True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"toml_{claim_key}_true",
                    "literal_parts": [claim_key, " = true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"yaml_{claim_key}_true",
                    "literal_parts": [claim_key, ": true"],
                    "policy": policy,
                },
            ]
        )
    return patterns


PRIVATE_WRAPPER_RETIREMENT_FALSE_READY_PATTERN_IDS = [
    pattern["pattern_id"]
    for pattern in _private_wrapper_retirement_false_ready_patterns()
]


def _generated_hosted_surface_false_ready_patterns() -> list[dict[str, object]]:
    patterns: list[dict[str, object]] = []
    for claim_key in GENERATED_HOSTED_SURFACE_FALSE_READY_CLAIM_KEYS:
        policy = (
            "Generated/hosted surface live consumption, App/workbench rendering, registry discovery "
            "and default-caller cutover are OPL/App external evidence tails; MAG repo source true "
            "flags are false-ready claims"
        )
        patterns.extend(
            [
                {
                    "pattern_id": f"json_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_single_{claim_key}_true",
                    "literal_parts": ["'", claim_key, "': True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"toml_{claim_key}_true",
                    "literal_parts": [claim_key, " = true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"yaml_{claim_key}_true",
                    "literal_parts": [claim_key, ": true"],
                    "policy": policy,
                },
            ]
        )
    return patterns


GENERATED_HOSTED_SURFACE_FALSE_READY_PATTERN_IDS = [
    pattern["pattern_id"]
    for pattern in _generated_hosted_surface_false_ready_patterns()
]


def _strict_source_purity_false_ready_patterns() -> list[dict[str, object]]:
    patterns: list[dict[str, object]] = []
    for claim_key in STRICT_SOURCE_PURITY_FALSE_READY_CLAIM_KEYS:
        policy = (
            "Strict source-purity and source-ref integrity scans are no-second-truth guards; "
            "repo source true flags cannot claim readiness, default-caller cutover or delete authority"
        )
        patterns.extend(
            [
                {
                    "pattern_id": f"json_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_{claim_key}_true",
                    "literal_parts": ["\"", claim_key, "\": True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"python_single_{claim_key}_true",
                    "literal_parts": ["'", claim_key, "': True"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"toml_{claim_key}_true",
                    "literal_parts": [claim_key, " = true"],
                    "policy": policy,
                },
                {
                    "pattern_id": f"yaml_{claim_key}_true",
                    "literal_parts": [claim_key, ": true"],
                    "policy": policy,
                },
            ]
        )
    return patterns


STRICT_SOURCE_PURITY_FALSE_READY_PATTERN_IDS = [
    pattern["pattern_id"]
    for pattern in _strict_source_purity_false_ready_patterns()
]
