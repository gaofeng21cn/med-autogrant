from __future__ import annotations

from copy import deepcopy
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any, Mapping
from unittest.mock import Mock, patch


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
