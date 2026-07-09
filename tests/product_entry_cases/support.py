from __future__ import annotations

import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any, Mapping


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.control_plane import read_program_id, resolve_runtime_state_root  # noqa: E402
from med_autogrant.cli import main  # noqa: E402
from med_autogrant.domain_entry_contract import build_domain_entry_contract  # noqa: E402
from med_autogrant.domain_runtime_parts.contracts import (  # noqa: E402
    build_author_side_route_contract,
    build_operator_contract,
)
from med_autogrant.domain_runtime_parts.shared import AUTHOR_SIDE_ROUTE_IDS  # noqa: E402
from med_autogrant.public_cli import public_cli_command, public_command_label  # noqa: E402
from support.cli import public_cli_argv  # noqa: E402
from med_autogrant.workspace import WorkspaceStateError  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"

_DOMAIN_ENTRY_CONTRACT = build_domain_entry_contract()
SUPPORTED_DOMAIN_ENTRY_COMMANDS = _DOMAIN_ENTRY_CONTRACT["supported_commands"]
DOMAIN_ENTRY_COMMAND_CONTRACTS = _DOMAIN_ENTRY_CONTRACT["command_contracts"]
CANONICAL_EXPORT_SURFACES = build_operator_contract()["canonical_export_surfaces"]

PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND = public_command_label("build-product-entry")


def run_public_cli(*args: str) -> tuple[int, str, str]:
    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            exit_code = main(public_cli_argv(args))
        except SystemExit as exc:
            exit_code = int(exc.code)
    return exit_code, stdout.getvalue(), stderr.getvalue()


def assert_contains_all(test_case: unittest.TestCase, container: Any, expected_items: tuple[str, ...]) -> None:
    for item in expected_items:
        test_case.assertIn(item, container)


def assert_false_keys(test_case: unittest.TestCase, mapping: Mapping[str, Any], keys: tuple[str, ...]) -> None:
    for key in keys:
        test_case.assertFalse(mapping[key])


def assert_true_keys(test_case: unittest.TestCase, mapping: Mapping[str, Any], keys: tuple[str, ...]) -> None:
    for key in keys:
        test_case.assertTrue(mapping[key])


def assert_path_values(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
    expected_by_path: Mapping[str | tuple[Any, ...], Any],
) -> None:
    for path, expected in expected_by_path.items():
        current: Any = payload
        for part in path if isinstance(path, tuple) else path.split("."):
            current = current[part]
        test_case.assertEqual(current, expected, path)


def codex_execution_attempt(*, include_stage_pack_ref: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {
        "attempt_id": "attempt-critique-001",
        "executor": "codex_cli",
        "invocation_ref": "codex://invocations/critique-001",
        "task_record_ref": "runtime://opl/stage-attempts/critique-001.json",
        "receipt_ref": "runtime://mag/receipts/stage/critique-001.json",
        "output_artifact_ref": "runtime://mag/artifacts/critique-001.json",
    }
    if include_stage_pack_ref:
        payload["stage_pack_ref"] = "agent/prompts/review_and_rebuttal.md"
    return payload


def codex_review_attempt() -> dict[str, object]:
    return {
        "review_attempt_id": "review-critique-001",
        "reviewer_executor": "codex_cli",
        "review_invocation_ref": "codex://invocations/review-critique-001",
        "review_task_record_ref": "runtime://opl/stage-attempts/review-critique-001.json",
        "review_receipt_ref": "runtime://mag/receipts/review/review-critique-001.json",
        "review_artifact_ref": "runtime://mag/artifacts/review-critique-001.json",
        "review_target_attempt_id": "attempt-critique-001",
        "independent_context": True,
        "shared_context_with_execution": False,
    }


def production_acceptance_evidence(
    *,
    include_owner_refs: bool = False,
    include_patch_loop_refs: bool = False,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "surface_kind": "mag_production_acceptance_evidence.v1",
        "evidence_tail_status": "closed_by_domain_owned_acceptance_receipt",
        "closure_evidence": {
            "accepted_return_shape": "domain_owner_receipt_ref",
            "owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
        },
    }
    if include_owner_refs:
        payload["refs"] = {
            "grant_owner_receipt_refs": [
                "contracts/owner_receipt_contract.json",
                "receipt:mag/grant-stage-controlled-attempt/body-free-closeout/2026-05-20",
            ],
            "owner_receipt_refs": [
                "receipt:mag/production-live-acceptance/2026-05-20",
                "/product_entry_manifest/production_live_acceptance_receipt",
            ],
        }
    if include_patch_loop_refs:
        payload["patch_loop_refs"] = {
            "blocked_suite_result_ref": "agent-lab-suite-result:oma/mag/blocked-suite",
            "developer_patch_work_order_ref": "developer-work-order:oma/mag/ai-first-mag-patch-smoke",
            "patch_traceability_matrix_ref": "patch-traceability:oma/mag/ai-first-mag-patch-smoke",
            "target_repo_verification_refs": [
                "rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_executor_first_closeout_bundle.py -q",
                "rtk ./scripts/verify.sh",
                "rtk git diff --check",
            ],
            "target_runtime_read_model_consumption_ref": "/product_entry_manifest/production_live_acceptance_receipt",
            "workspace_environment_proof_ref": "workspace-proof:med-autogrant/.worktrees/ai-first-mag-patch-smoke",
            "no_forbidden_write_proof_ref": "contracts/agent_lab_handoff.json#/authority_boundary/oma_consumes_mag_refs_only",
            "target_owner_receipt_or_typed_blocker_ref": "receipt:mag/production-live-acceptance/2026-05-20",
            "patch_absorption_ref": "git-commit:pending/codex/ai-first-mag-patch-smoke",
            "worktree_cleanup_ref": "worktree-cleanup:pending/ai-first-mag-patch-smoke",
            "agent_lab_re_evaluation_ref": "agent-lab-run:oma/mag/ai-first-mag-patch-smoke/re-evaluation",
        }
    return payload


def receipt_readiness_projection(
    *,
    missing: list[str] | None = None,
    total_ref_count: int = 3,
    include_receipt_refs: bool = False,
) -> dict[str, object]:
    missing_categories = list(missing or [])
    payload: dict[str, object] = {
        "surface_kind": "mag_receipt_readiness_projection",
        "state": "receipt_refs_ready_not_quality_ready" if not missing_categories else "partial_receipt_coverage",
        "missing_categories": missing_categories,
        "summary": {
            "covered_category_count": 4 - len(missing_categories),
            "missing_category_count": len(missing_categories),
            "total_receipt_ref_count": total_ref_count,
        },
    }
    if include_receipt_refs:
        payload["receipt_refs"] = {
            "owner_receipt": ["runtime://mag/receipts/owner/package-closeout.json"],
            "memory_accept_reject": ["runtime://mag/receipts/memory/accepted-risk.json"],
            "package_export_lifecycle": ["runtime://mag/receipts/package/lifecycle.json"],
            "cleanup_restore_retention_lifecycle": ["runtime://mag/receipts/lifecycle/cleanup.json"],
        }
    return payload


def _expected_route(route_id: str, *, source_stage: str) -> dict[str, object]:
    return build_author_side_route_contract(route_id, source_stage=source_stage)


def _expected_runtime_output_path(
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    file_name: str,
) -> Path:
    draft_path_segment = draft_id or "no-draft"
    return (
        resolve_runtime_state_root()
        / "reports"
        / read_program_id(repo_root=REPO_ROOT)
        / grant_run_id
        / workspace_id
        / draft_path_segment
        / file_name
    )


def _assert_family_orchestration_companion(
    test_case: unittest.TestCase,
    family_orchestration: object,
    *,
    expected_resume_surface: str,
) -> None:
    test_case.assertIsInstance(family_orchestration, dict)
    companion = family_orchestration
    test_case.assertIn("action_graph_ref", companion)
    test_case.assertIn("human_gates", companion)
    test_case.assertIn("resume_contract", companion)
    test_case.assertIn("action_graph", companion)

    action_graph_ref = companion["action_graph_ref"]
    test_case.assertIsInstance(action_graph_ref, dict)
    test_case.assertEqual(action_graph_ref["ref_kind"], "json_pointer")
    test_case.assertEqual(action_graph_ref["ref"], "/family_orchestration/action_graph")

    human_gates = companion["human_gates"]
    test_case.assertIsInstance(human_gates, list)
    test_case.assertGreaterEqual(len(human_gates), 1)
    for gate in human_gates:
        test_case.assertIsInstance(gate, dict)
        test_case.assertIn("gate_id", gate)
        test_case.assertIn("status", gate)
        test_case.assertIn(gate["status"], {"requested", "approved", "rejected", "changes_requested"})

    resume_contract = companion["resume_contract"]
    test_case.assertIsInstance(resume_contract, dict)
    test_case.assertEqual(resume_contract["surface_kind"], expected_resume_surface)
    test_case.assertEqual(resume_contract["session_locator_field"], "grant_run_id")
    test_case.assertEqual(resume_contract["checkpoint_locator_field"], "lifecycle_stage")

    action_graph = companion["action_graph"]
    test_case.assertIsInstance(action_graph, dict)
    test_case.assertEqual(action_graph["version"], "family-action-graph.v1")
    test_case.assertEqual(action_graph["target_domain_id"], "med-autogrant")
    test_case.assertGreaterEqual(len(action_graph["nodes"]), 2)
    test_case.assertGreaterEqual(len(action_graph["entry_nodes"]), 1)
    test_case.assertIn("intake_evidence_companion", companion)
    test_case.assertIn("project_profile_companion", companion)
    intake_evidence_companion = companion["intake_evidence_companion"]
    test_case.assertIsInstance(intake_evidence_companion, dict)
    test_case.assertEqual(
        intake_evidence_companion["version"],
        "family-intake-evidence-companion.v1",
    )
    test_case.assertEqual(
        intake_evidence_companion["target_domain_id"],
        "med-autogrant",
    )
    test_case.assertEqual(
        intake_evidence_companion["intake_audit"]["verdict"],
        "ready_for_direction_screening",
    )
    test_case.assertGreaterEqual(len(intake_evidence_companion["trust_ranked_evidence_refs"]), 1)
    project_profile_companion = companion["project_profile_companion"]
    test_case.assertIsInstance(project_profile_companion, dict)
    test_case.assertEqual(project_profile_companion["surface_kind"], "project_profile_companion")
    test_case.assertEqual(project_profile_companion["profile_id"], "profile-nsfc-general-medical")
    test_case.assertEqual(project_profile_companion["preset_id"], "nsfc_general_medical_v1")
    test_case.assertEqual(
        project_profile_companion["critique_policy"]["policy_id"],
        "nsfc_mentor_critique_v1",
    )
