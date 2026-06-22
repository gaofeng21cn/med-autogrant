from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.functional_closure_skeleton import (
    build_physical_skeleton_follow_through,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


REPO_ROOT = Path(__file__).resolve().parents[3]
PRIVATE_POLICY_PATH = REPO_ROOT / "contracts" / "private_functional_surface_policy.json"


def build_source_purity_guard_readback() -> dict[str, Any]:
    policy = _load_private_surface_policy()
    morphology = _require_mapping(
        policy,
        "physical_source_morphology_policy",
        context="private_functional_surface_policy",
    )
    active_path_scan = build_physical_skeleton_follow_through()[
        "active_path_scan_no_legacy_default_caller"
    ]
    source_ref_gate = _require_mapping(
        morphology,
        "source_ref_integrity_gate",
        context="physical_source_morphology_policy",
    )
    strict_guard = _require_mapping(
        morphology,
        "strict_source_purity_no_second_truth_guard",
        context="physical_source_morphology_policy",
    )
    repo_shell_guard = _repo_shell_verification_wrapper_guard(morphology)
    retirement_guard = _require_mapping(
        morphology,
        "retirement_readback_cleanup_guard",
        context="physical_source_morphology_policy",
    )
    compact_summary = _require_mapping(
        retirement_guard,
        "compact_cleanup_readiness_summary",
        context="retirement_readback_cleanup_guard",
    )
    owner_delta_work_order_pack = _require_mapping(
        compact_summary,
        "owner_delta_work_order_pack",
        context="compact_cleanup_readiness_summary",
    )

    failures = _collect_failures(
        active_path_scan=active_path_scan,
        source_ref_gate=source_ref_gate,
        strict_guard=strict_guard,
        repo_shell_guard=repo_shell_guard,
        compact_summary=compact_summary,
        owner_delta_work_order_pack=owner_delta_work_order_pack,
    )
    return {
        "surface_kind": "mag_strict_source_purity_guard_readback",
        "schema_version": 1,
        "target_domain_id": TARGET_DOMAIN_ID,
        "state": "passed_repo_source_guard_only" if not failures else "failed",
        "failed_checks": failures,
        "active_path_scan": active_path_scan,
        "source_ref_integrity_gate": source_ref_gate,
        "strict_source_purity_no_second_truth_guard": strict_guard,
        "repo_shell_verification_wrapper_guard": repo_shell_guard,
        "compact_cleanup_readiness_summary": compact_summary,
        "owner_delta_work_order_pack": owner_delta_work_order_pack,
        "allowed_outputs": list(strict_guard["allowed_outputs"]),
        "forbidden_outputs": list(strict_guard["forbidden_outputs"]),
        "authority_boundary": {
            "readback_can_write_grant_truth": False,
            "readback_can_sign_owner_receipt": False,
            "readback_can_create_typed_blocker": False,
            "readback_can_authorize_physical_delete": False,
            "readback_can_claim_default_caller_cutover": False,
            "readback_can_claim_generated_hosted_live_consumption": False,
            "readback_can_claim_grant_readiness": False,
            "readback_can_claim_submission_ready": False,
            "readback_can_claim_production_ready": False,
        },
    }


def _collect_failures(
    *,
    active_path_scan: Mapping[str, Any],
    source_ref_gate: Mapping[str, Any],
    strict_guard: Mapping[str, Any],
    repo_shell_guard: Mapping[str, Any],
    compact_summary: Mapping[str, Any],
    owner_delta_work_order_pack: Mapping[str, Any],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    if active_path_scan.get("state") != "passed":
        failures.append(
            {
                "check_id": "active_path_scan",
                "state": active_path_scan.get("state"),
                "match_count": len(active_path_scan.get("forbidden_default_caller_matches") or []),
                "retired_path_match_count": len(
                    [
                        item
                        for item in active_path_scan.get("retired_surface_path_status") or []
                        if isinstance(item, Mapping) and item.get("state") != "absent"
                    ]
                ),
            }
        )
    source_ref_failures = _invalid_source_refs(source_ref_gate)
    if source_ref_failures:
        failures.append(
            {
                "check_id": "source_ref_integrity_gate",
                "state": "failed",
                "invalid_source_refs": source_ref_failures,
            }
        )
    if strict_guard.get("guard_id") != "mag.physical_morphology.strict_source_purity_no_second_truth_guard.v1":
        failures.append(
            {
                "check_id": "strict_guard_identity",
                "state": "failed",
                "guard_id": strict_guard.get("guard_id"),
            }
        )
    boundary = strict_guard.get("authority_boundary")
    if not isinstance(boundary, Mapping) or any(bool(value) for value in boundary.values()):
        failures.append(
            {
                "check_id": "strict_guard_authority_boundary",
                "state": "failed",
                "authority_boundary": boundary,
            }
        )
    if repo_shell_guard.get("state") != "passed_repo_native_verification_wrapper_classified":
        failures.append(
            {
                "check_id": "repo_shell_verification_wrapper_guard",
                "state": repo_shell_guard.get("state"),
                "unclassified_script_refs": repo_shell_guard.get("unclassified_script_refs"),
                "stale_classified_script_refs": repo_shell_guard.get(
                    "stale_classified_script_refs"
                ),
            }
        )
    for key in [
        "can_apply_cleanup",
        "can_authorize_physical_delete",
        "can_claim_default_caller_cutover_complete",
        "can_claim_app_operator_consumption",
        "can_claim_grant_ready",
        "can_claim_submission_ready",
        "can_claim_domain_ready",
        "can_claim_production_ready",
    ]:
        if compact_summary.get(key) is not False:
            failures.append(
                {
                    "check_id": "compact_cleanup_readiness_false_ready_guard",
                    "state": "failed",
                    "key": key,
                    "value": compact_summary.get(key),
                }
            )
    if compact_summary.get("owner_delta_required") is not True:
        failures.append(
            {
                "check_id": "compact_cleanup_readiness_owner_delta_required",
                "state": "failed",
                "owner_delta_required": compact_summary.get("owner_delta_required"),
            }
        )
    if compact_summary.get("cleanup_candidate_count") != 7:
        failures.append(
            {
                "check_id": "compact_cleanup_readiness_candidate_count",
                "state": "failed",
                "cleanup_candidate_count": compact_summary.get("cleanup_candidate_count"),
            }
        )
    route_count = owner_delta_work_order_pack.get("owner_delta_route_count")
    candidate_count = compact_summary.get("cleanup_candidate_count")
    if route_count != candidate_count:
        failures.append(
            {
                "check_id": "owner_delta_work_order_route_count",
                "state": "failed",
                "owner_delta_route_count": route_count,
                "cleanup_candidate_count": candidate_count,
            }
        )
    work_order_boundary = owner_delta_work_order_pack.get("authority_boundary")
    if not isinstance(work_order_boundary, Mapping) or any(
        bool(value) for value in work_order_boundary.values()
    ):
        failures.append(
            {
                "check_id": "owner_delta_work_order_authority_boundary",
                "state": "failed",
                "authority_boundary": work_order_boundary,
            }
        )
    for route in owner_delta_work_order_pack.get("owner_delta_routes") or []:
        if not isinstance(route, Mapping):
            failures.append(
                {
                    "check_id": "owner_delta_work_order_route_shape",
                    "state": "failed",
                    "route": route,
                }
            )
            continue
        if not route.get("owner_receipt_ref_shape") or not route.get("typed_blocker_ref_shape"):
            failures.append(
                {
                    "check_id": "owner_delta_work_order_route_ref_shape",
                    "state": "failed",
                    "surface_id": route.get("surface_id"),
                }
            )
    return failures


def _invalid_source_refs(source_ref_gate: Mapping[str, Any]) -> list[dict[str, str]]:
    invalid: list[dict[str, str]] = []
    checked_refs = source_ref_gate.get("checked_source_refs")
    if not isinstance(checked_refs, list) or not checked_refs:
        return [{"ref": "<checked_source_refs>", "reason": "missing_or_empty_list"}]
    for ref in checked_refs:
        if not isinstance(ref, str) or not ref.strip():
            invalid.append({"ref": repr(ref), "reason": "empty_ref"})
            continue
        path = Path(ref)
        if ref.startswith("human_doc:"):
            invalid.append({"ref": ref, "reason": "human_doc_ref_as_machine_source_ref"})
        elif path.is_absolute():
            invalid.append({"ref": ref, "reason": "absolute_path"})
        elif ".." in path.parts:
            invalid.append({"ref": ref, "reason": "parent_directory_traversal"})
        elif "://" in ref:
            invalid.append({"ref": ref, "reason": "uri_or_url"})
        elif not (REPO_ROOT / path).exists():
            invalid.append({"ref": ref, "reason": "missing_repo_local_source_ref"})
    return invalid


def _repo_shell_verification_wrapper_guard(
    morphology: Mapping[str, Any],
) -> dict[str, Any]:
    classifications = morphology.get("surface_classifications")
    surface: Mapping[str, Any] | None = None
    if isinstance(classifications, list):
        for item in classifications:
            if isinstance(item, Mapping) and item.get("surface_id") == "repo_shell_verification_wrappers":
                surface = item
                break
    if surface is None:
        return {
            "surface_kind": "mag_repo_shell_verification_wrapper_guard",
            "state": "missing_repo_shell_verification_wrapper_classification",
            "checked_script_refs": _active_repo_script_refs(),
            "classified_script_refs": [],
            "unclassified_script_refs": _active_repo_script_refs(),
            "stale_classified_script_refs": [],
            "authority_boundary": {},
        }

    checked_script_refs = _active_repo_script_refs()
    classified_script_refs = sorted(
        str(item)
        for item in surface.get("source_refs") or []
        if isinstance(item, str)
    )
    unclassified_script_refs = sorted(set(checked_script_refs) - set(classified_script_refs))
    stale_classified_script_refs = sorted(set(classified_script_refs) - set(checked_script_refs))
    authority_boundary = _require_mapping(
        surface,
        "authority_boundary",
        context="repo_shell_verification_wrappers",
    )
    retirement_gate = _require_mapping(
        surface,
        "retirement_gate",
        context="repo_shell_verification_wrappers",
    )
    boundary_false = all(value is False for value in authority_boundary.values())
    retirement_gate_ok = (
        retirement_gate.get("compatibility_alias_allowed") is False
        and retirement_gate.get("state")
        == "retained_repo_native_verification_entry_do_not_promote_to_runtime_owner"
    )
    classified_as_wrapper = (
        surface.get("classification") == "repo_native_verification_wrapper"
        and surface.get("active_caller_status") == "active_repo_verification_entry"
    )
    state = (
        "passed_repo_native_verification_wrapper_classified"
        if classified_as_wrapper
        and boundary_false
        and retirement_gate_ok
        and not unclassified_script_refs
        and not stale_classified_script_refs
        else "failed_repo_native_verification_wrapper_classification"
    )
    return {
        "surface_kind": "mag_repo_shell_verification_wrapper_guard",
        "state": state,
        "surface_id": "repo_shell_verification_wrappers",
        "classification": surface.get("classification"),
        "active_caller_status": surface.get("active_caller_status"),
        "allowed_role": surface.get("allowed_role"),
        "target_owner_after_migration": surface.get("target_owner_after_migration"),
        "checked_script_refs": checked_script_refs,
        "classified_script_refs": classified_script_refs,
        "unclassified_script_refs": unclassified_script_refs,
        "stale_classified_script_refs": stale_classified_script_refs,
        "authority_boundary": dict(authority_boundary),
        "retirement_gate": dict(retirement_gate),
        "false_ready_guard": {
            "repo_shell_guard_can_claim_runtime_owner": False,
            "repo_shell_guard_can_claim_generated_wrapper_owner": False,
            "repo_shell_guard_can_authorize_physical_delete": False,
            "repo_shell_guard_can_claim_grant_ready": False,
            "repo_shell_guard_can_claim_production_ready": False,
        },
    }


def _active_repo_script_refs() -> list[str]:
    scripts_dir = REPO_ROOT / "scripts"
    if not scripts_dir.is_dir():
        return []
    return sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in scripts_dir.iterdir()
        if path.is_file() and path.suffix in {".py", ".sh"}
    )


def _load_private_surface_policy() -> dict[str, Any]:
    return json.loads(PRIVATE_POLICY_PATH.read_text(encoding="utf-8"))


def _require_mapping(payload: Mapping[str, Any], key: str, *, context: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"{context}.{key} must be an object")
    return value
