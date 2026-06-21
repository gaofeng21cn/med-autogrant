#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.functional_closure_skeleton import (
    build_physical_skeleton_follow_through,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


REPO_ROOT = Path(__file__).resolve().parents[1]
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

    failures = _collect_failures(
        active_path_scan=active_path_scan,
        source_ref_gate=source_ref_gate,
        strict_guard=strict_guard,
        compact_summary=compact_summary,
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
        "compact_cleanup_readiness_summary": compact_summary,
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
    compact_summary: Mapping[str, Any],
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


def _load_private_surface_policy() -> dict[str, Any]:
    return json.loads(PRIVATE_POLICY_PATH.read_text(encoding="utf-8"))


def _require_mapping(payload: Mapping[str, Any], key: str, *, context: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"{context}.{key} must be an object")
    return value


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check MAG strict source-purity guard readback.")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    payload = build_source_purity_guard_readback()
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            f"{payload['surface_kind']}: {payload['state']} "
            f"({len(payload['failed_checks'])} failed checks)"
        )
    return 0 if payload["state"] == "passed_repo_source_guard_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
