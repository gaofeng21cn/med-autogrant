from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

_RETIRED_PUBLIC_COMMANDS = (
    "run-local",
    "runtime-run",
    "runtime-resume",
    "probe-upstream-hermes",
)
_RETIRED_PUBLIC_COMMAND_TEST_REFS = {
    "run-local": [
        "tests/test_domain_entry.py::DomainEntryDispatchTest::test_domain_entry_rejects_legacy_runtime_alias",
    ],
    "runtime-run": [
        "tests/test_domain_entry.py::DomainEntryDispatchTest::test_domain_entry_rejects_retired_runtime_commands",
    ],
    "runtime-resume": [
        "tests/test_domain_entry.py::DomainEntryDispatchTest::test_domain_entry_rejects_retired_runtime_commands",
    ],
    "probe-upstream-hermes": [
        "tests/test_domain_entry.py::DomainEntryDispatchTest::test_domain_entry_rejects_retired_runtime_commands",
    ],
}
def build_retired_legacy_default_path_receipts() -> list[dict[str, Any]]:
    return [
        {
            "path_family": "default Hermes active path",
            "state": "tombstone_only",
            "active_source_residue": False,
            "evidence_ref": "docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md",
            "domain_owner_handoff_receipt_refs": [],
        },
        {
            "path_family": "default Gateway active path",
            "state": "physically_removed_from_active_source",
            "active_source_residue": False,
            "evidence_ref": (
                "docs/decisions.md#2026-05-12-temporal-backed-opl-production-runtime-"
                "supersedes-gateway-manager-wording"
            ),
            "domain_owner_handoff_receipt_refs": [
                "mag://owner-handoff/default-gateway-active-path-retired",
            ],
        },
        {
            "path_family": "default local-manager active path",
            "state": "physically_removed_from_active_source",
            "active_source_residue": False,
            "evidence_ref": "docs/status.md#旧面退役校准",
            "domain_owner_handoff_receipt_refs": [
                "mag://owner-handoff/default-local-manager-active-path-retired",
            ],
        },
    ]


def build_physical_skeleton_follow_through(
    *, active_path_scan_policy: dict[str, Any] | None = None
) -> dict[str, Any]:
    roots = {
        "agent": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "agent/prompts/call_and_candidate_intake.md",
            "state": "declarative_grant_pack_present",
            "role": "canonical declarative grant pack for prompts, stages, skills, quality gates, and knowledge",
            "canonical_semantic_pack_root": "agent/",
            "canonical_semantic_pack_role": "repo_source_declarative_grant_pack",
            "required_pack_refs": [
                "agent/prompts/call_and_candidate_intake.md",
                "agent/prompts/fundability_strategy.md",
                "agent/prompts/specific_aims_and_structure.md",
                "agent/prompts/proposal_authoring.md",
                "agent/prompts/review_and_rebuttal.md",
                "agent/prompts/package_and_submit_ready.md",
                "agent/stages/call_and_candidate_intake.md",
                "agent/stages/fundability_strategy.md",
                "agent/stages/specific_aims_and_structure.md",
                "agent/stages/proposal_authoring.md",
                "agent/stages/review_and_rebuttal.md",
                "agent/stages/package_and_submit_ready.md",
                "agent/skills/grant_authoring.md",
                "agent/quality_gates/fundability.md",
                "agent/quality_gates/quality.md",
                "agent/quality_gates/export_and_package.md",
                "agent/quality_gates/memory_and_receipts.md",
                "agent/quality_gates/authority_boundaries.md",
                "agent/knowledge/grant_strategy_memory.md",
                "agent/knowledge/package_authority.md",
                "agent/knowledge/owner_receipt_boundary.md",
            ],
            "human_readable_provenance_refs": [
                "agent/README.md",
            ],
        },
        "contracts": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "contracts/runtime-program/current-program.json",
            "state": "physical_root_present",
            "role": "machine-readable contract and schema boundary anchor",
            "human_readable_provenance_refs": [
                "contracts/README.md",
            ],
        },
        "runtime": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "src/med_autogrant/product_entry_parts/domain_handler.py",
            "state": "physical_root_present",
            "role": "runtime descriptor and domain_handler boundary anchor",
            "human_readable_provenance_refs": [
                "runtime/README.md",
            ],
        },
        "docs": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "docs/status.md",
            "state": "physical_root_present",
            "role": "human status and governance boundary anchor",
        },
    }
    repo_root = Path(__file__).resolve().parents[3]
    active_path_scan = _build_active_path_scan_no_legacy_default_caller(
        repo_root,
        scan_policy=active_path_scan_policy,
    )
    retired_public_command_scan = _build_retired_public_command_scan()
    return {
        "surface_kind": "mag_physical_skeleton_follow_through",
        "version": "v1",
        "follow_through_id": "mag.physical_skeleton.follow_through.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "state": "declarative_grant_pack_landed",
        "roots": roots,
        "root_status": [
            {
                "root": root_key,
                "anchor_ref": root["anchor_ref"],
                "exists": (repo_root / root["anchor_ref"]).exists(),
                "owner": root["owner"],
                "required_pack_refs_exist": all(
                    (repo_root / required_ref).exists()
                    for required_ref in root.get("required_pack_refs", [])
                ),
            }
            for root_key, root in roots.items()
        ],
        "moves_workspace_artifacts": False,
        "moves_runtime_receipt_instances": False,
        "moves_memory_body": False,
        "human_readable_provenance_refs": [
            "agent/README.md",
            "contracts/README.md",
            "runtime/README.md",
        ],
        "human_readable_provenance_policy": (
            "README refs are retained for human orientation/provenance only and are not required "
            "semantic pack compiler inputs or current machine anchors."
        ),
        "active_path_scan_no_legacy_default_caller_ref": (
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_scan_no_legacy_default_caller"
        ),
        "active_path_scan_no_legacy_default_caller": active_path_scan,
        "retired_public_command_scan_ref": (
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "retired_public_command_scan"
        ),
        "retired_public_command_scan": retired_public_command_scan,
        "replacement_parity_refs": [
            "/product_entry_manifest/mag_consumer_thinning_contract",
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/grant_transition_oracle",
            "/product_entry_manifest/controlled_soak_no_regression_attempt",
            "/product_entry_manifest/physical_skeleton_follow_through/active_path_scan_no_legacy_default_caller",
            "/product_entry_manifest/physical_skeleton_follow_through/retired_public_command_scan",
        ],
        "no_regression_evidence_refs": [
            "tests/product_entry_cases/test_hosted_receipt_verification.py::ProductEntryHostedReceiptVerificationTest::test_hosted_receipt_verification_matches_opl_attempt_to_mag_receipt_refs",
            "tests/product_entry_cases/test_grant_transition_oracle.py::ProductEntryGrantTransitionOracleTest::test_oracle_domain_handler_closeout_writes_no_regression_owner_receipt_refs",
        ],
        "tombstone_refs": [
            "docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md",
        ],
        "history_refs": [
            "docs/decisions.md#2026-05-12-temporal-backed-opl-production-runtime-supersedes-gateway-manager-wording",
            "docs/status.md#旧面退役校准",
        ],
        "first_follow_through_scope": [
            "manifest exposes root anchors and declarative agent pack refs",
            "repo-source layout audit requires root anchors to exist",
            "workspace artifacts and runtime receipts stay outside repo source",
            "active-path scan proves retired default callers are not used by machine surfaces",
            "domain-memory receipt evidence writer persists accepted/rejected receipt instances under runtime roots only",
        ],
        "legacy_active_path_policy": "physically_removed_or_history_tombstone_only",
        "legacy_active_path_residue": [],
        "retired_legacy_default_path_receipts": build_retired_legacy_default_path_receipts(),
        "next_physical_moves": [
            {
                "path_family": "domain entry and stage descriptors",
                "source_owner": TARGET_DOMAIN_ID,
                "condition": "direct/hosted parity, restore/provenance proof, and no-active-caller proof",
            },
            {
                "path_family": "runtime descriptors and domain_handler declarations",
                "source_owner": TARGET_DOMAIN_ID,
                "condition": "direct skill and OPL-hosted parity proof",
            },
        ],
    }


def _build_retired_public_command_scan() -> dict[str, Any]:
    from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
    from med_autogrant.public_cli import (
        PUBLIC_THREE_TOKEN_COMMANDS,
        PUBLIC_TO_INTERNAL_COMMAND,
    )

    active_domain_entry_commands = set(SERVICE_SAFE_DOMAIN_COMMANDS)
    active_public_cli_command_labels = {
        " ".join(tokens) for tokens in PUBLIC_TO_INTERNAL_COMMAND
    } | {" ".join(tokens) for tokens in PUBLIC_THREE_TOKEN_COMMANDS}
    command_status = [
        _retired_public_command_status(
            command,
            active_domain_entry_commands=active_domain_entry_commands,
            active_public_cli_command_labels=active_public_cli_command_labels,
        )
        for command in _RETIRED_PUBLIC_COMMANDS
    ]
    matches = [
        status
        for status in command_status
        if status["active_domain_entry_command"] or status["active_public_cli_command"]
    ]
    return {
        "surface_kind": "mag_retired_public_command_no_resurrection_scan",
        "version": "v1",
        "scan_id": "mag.retired_public_command.no_resurrection.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "state": "passed" if not matches else "failed",
        "no_retired_public_commands": not matches,
        "retired_exact_commands": list(_RETIRED_PUBLIC_COMMANDS),
        "command_status": command_status,
        "retired_command_matches": matches,
        "active_catalogs": {
            "domain_entry_command_count": len(active_domain_entry_commands),
            "public_grouped_cli_command_count": len(active_public_cli_command_labels),
            "flat_internal_command_aliases_rejected_by_cli_normalizer": True,
            "flat_internal_command_alias_count": len(PUBLIC_TO_INTERNAL_COMMAND),
            "negative_test_refs": [
                "tests/product_entry_cases/test_cli_dispatch.py::ProductEntryCliDispatchTest::test_flat_product_status_alias_has_no_special_compatibility_branch",
            ],
        },
        "claims_production_long_run_soak_complete": False,
        "authority_boundary": {
            "proves_repo_local_command_catalog_only": True,
            "proves_opl_hosted_production_soak": False,
            "proves_app_workbench_consumption": False,
            "proves_grant_quality_or_export_readiness": False,
            "opl_can_write_domain_truth": False,
            "opl_can_declare_export_ready": False,
        },
    }


def _retired_public_command_status(
    command: str,
    *,
    active_domain_entry_commands: set[str],
    active_public_cli_command_labels: set[str],
) -> dict[str, Any]:
    active_domain_entry_command = command in active_domain_entry_commands
    active_public_cli_command = (
        command in active_public_cli_command_labels
        or command.replace("-", " ") in active_public_cli_command_labels
    )
    return {
        "command": command,
        "state": (
            "present_forbidden"
            if active_domain_entry_command or active_public_cli_command
            else "absent_from_active_catalogs"
        ),
        "active_domain_entry_command": active_domain_entry_command,
        "active_public_cli_command": active_public_cli_command,
        "negative_test_refs": list(_RETIRED_PUBLIC_COMMAND_TEST_REFS[command]),
    }


def _build_active_path_scan_no_legacy_default_caller(
    repo_root: Path,
    *,
    scan_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if scan_policy is None:
        scan_policy = _load_active_path_scan_policy(repo_root)
    else:
        scan_policy = _validated_active_path_scan_policy(scan_policy)
    scanned_paths = _active_path_scan_paths(repo_root, scan_policy=scan_policy)
    forbidden_patterns = [
        {
            "pattern_id": str(pattern["pattern_id"]),
            "literal": "".join(pattern["literal_parts"]),
            "policy": str(pattern["policy"]),
        }
        for pattern in scan_policy["forbidden_default_caller_patterns"]
    ]
    matches: list[dict[str, Any]] = []
    for path in scanned_paths:
        text = _read_scan_text(path)
        if text is None:
            continue
        relative_path = path.relative_to(repo_root).as_posix()
        for pattern in forbidden_patterns:
            literal = pattern["literal"]
            if literal in text:
                matches.append(
                    {
                        "path": relative_path,
                        "pattern_id": pattern["pattern_id"],
                        "literal": literal,
                    }
                )
    retired_surface_path_status = [
        {
            "path": path,
            "exists": (repo_root / path).exists(),
            "state": "absent" if not (repo_root / path).exists() else "present_forbidden",
        }
        for path in scan_policy["retired_active_paths"]
    ]
    retired_surface_path_matches = [
        status for status in retired_surface_path_status if status["state"] != "absent"
    ]
    return {
        "surface_kind": "mag_active_path_scan_no_legacy_default_caller",
        "version": "v1",
        "scan_id": "mag.active_path_scan.no_legacy_default_caller.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "state": "passed" if not matches and not retired_surface_path_matches else "failed",
        "evidence_ref_id": "active_path_scan_no_legacy_default_caller_ref",
        "no_legacy_default_caller": not matches and not retired_surface_path_matches,
        "policy_ref": (
            "contracts/private_functional_surface_policy.json#/"
            "physical_source_morphology_policy/active_path_scan_policy"
        ),
        "policy_id": scan_policy["policy_id"],
        "scanned_scope": {
            "roots": list(scan_policy["roots"]),
            "files": list(scan_policy["files"]),
            "suffixes": list(scan_policy["suffixes"]),
            "excludes_human_docs": scan_policy["excludes_human_docs"],
            "human_doc_policy": scan_policy["human_doc_policy"],
            "scans_repo_source_only": scan_policy["scans_repo_source_only"],
        },
        "scanned_file_count": len(scanned_paths),
        "scanned_sample_refs": [
            path.relative_to(repo_root).as_posix()
            for path in scanned_paths[:12]
        ],
        "forbidden_default_caller_patterns": forbidden_patterns,
        "forbidden_default_caller_matches": matches,
        "retired_surface_path_status": retired_surface_path_status,
        "claims_production_long_run_soak_complete": False,
        "authority_boundary": {
            "proves_repo_local_active_machine_surface_only": True,
            "proves_opl_hosted_production_soak": False,
            "proves_grant_quality_or_export_readiness": False,
            "opl_can_write_domain_truth": False,
            "opl_can_declare_export_ready": False,
        },
    }


def _load_active_path_scan_policy(repo_root: Path) -> dict[str, Any]:
    policy_path = repo_root / "contracts" / "private_functional_surface_policy.json"
    payload = json.loads(policy_path.read_text(encoding="utf-8"))
    morphology_policy = _require_mapping(
        payload,
        "physical_source_morphology_policy",
        context="private_functional_surface_policy",
    )
    scan_policy = _require_mapping(
        morphology_policy,
        "active_path_scan_policy",
        context="private_functional_surface_policy.physical_source_morphology_policy",
    )
    return _validated_active_path_scan_policy(scan_policy)


def _validated_active_path_scan_policy(policy: dict[str, Any]) -> dict[str, Any]:
    if policy.get("target_domain_id") != TARGET_DOMAIN_ID:
        raise ValueError("active path scan policy target_domain_id must be med-autogrant.")
    if policy.get("policy_id") != "mag.active_path_scan.no_legacy_default_caller.policy.v1":
        raise ValueError("Unsupported active path scan policy_id.")
    result = {
        "policy_id": _require_nonempty_string(policy, "policy_id", context="active_path_scan_policy"),
        "roots": _require_string_list(policy, "roots", context="active_path_scan_policy"),
        "files": _require_string_list(policy, "files", context="active_path_scan_policy"),
        "suffixes": sorted(
            _require_string_list(policy, "suffixes", context="active_path_scan_policy")
        ),
        "retired_active_paths": _require_string_list(
            policy,
            "retired_active_paths",
            context="active_path_scan_policy",
        ),
        "forbidden_default_caller_patterns": _validated_forbidden_patterns(policy),
        "excludes_human_docs": _require_bool(
            policy,
            "excludes_human_docs",
            context="active_path_scan_policy",
        ),
        "human_doc_policy": _require_nonempty_string(
            policy,
            "human_doc_policy",
            context="active_path_scan_policy",
        ),
        "scans_repo_source_only": _require_bool(
            policy,
            "scans_repo_source_only",
            context="active_path_scan_policy",
        ),
    }
    return result


def _validated_forbidden_patterns(policy: dict[str, Any]) -> list[dict[str, Any]]:
    patterns = _require_list(
        policy,
        "forbidden_default_caller_patterns",
        context="active_path_scan_policy",
    )
    result: list[dict[str, Any]] = []
    for index, pattern in enumerate(patterns):
        pattern_mapping = _require_mapping(
            pattern,
            context=f"active_path_scan_policy.forbidden_default_caller_patterns[{index}]",
        )
        result.append(
            {
                "pattern_id": _require_nonempty_string(
                    pattern_mapping,
                    "pattern_id",
                    context=f"forbidden_default_caller_patterns[{index}]",
                ),
                "literal_parts": _require_string_list(
                    pattern_mapping,
                    "literal_parts",
                    context=f"forbidden_default_caller_patterns[{index}]",
                ),
                "policy": _require_nonempty_string(
                    pattern_mapping,
                    "policy",
                    context=f"forbidden_default_caller_patterns[{index}]",
                ),
            }
        )
    return result


def _active_path_scan_paths(repo_root: Path, *, scan_policy: dict[str, Any]) -> list[Path]:
    paths: set[Path] = set()
    for root_name in scan_policy["roots"]:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in scan_policy["suffixes"]:
                paths.add(path)
    for file_name in scan_policy["files"]:
        path = repo_root / file_name
        if path.is_file():
            paths.add(path)
    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def _read_scan_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def _require_mapping(value: Any, key: str | None = None, *, context: str) -> dict[str, Any]:
    candidate = value if key is None else value.get(key) if isinstance(value, dict) else None
    if not isinstance(candidate, dict):
        field = context if key is None else f"{context}.{key}"
        raise ValueError(f"{field} must be an object.")
    return candidate


def _require_list(value: dict[str, Any], key: str, *, context: str) -> list[Any]:
    candidate = value.get(key)
    if not isinstance(candidate, list) or not candidate:
        raise ValueError(f"{context}.{key} must be a non-empty list.")
    return candidate


def _require_string_list(value: dict[str, Any], key: str, *, context: str) -> list[str]:
    candidate = _require_list(value, key, context=context)
    if not all(isinstance(item, str) and item for item in candidate):
        raise ValueError(f"{context}.{key} must contain only non-empty strings.")
    return list(candidate)


def _require_nonempty_string(value: dict[str, Any], key: str, *, context: str) -> str:
    candidate = value.get(key)
    if not isinstance(candidate, str) or not candidate:
        raise ValueError(f"{context}.{key} must be a non-empty string.")
    return candidate


def _require_bool(value: dict[str, Any], key: str, *, context: str) -> bool:
    candidate = value.get(key)
    if not isinstance(candidate, bool):
        raise ValueError(f"{context}.{key} must be a boolean.")
    return candidate
