from __future__ import annotations

import json
import tempfile
import unittest
from collections.abc import Mapping
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from med_autogrant.cli import main
from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.domain_runtime_parts.contracts import build_operator_contract
from med_autogrant.domain_runtime_parts.shared import AUTHOR_SIDE_ROUTE_IDS
from support.cli import public_cli_argv


CANONICAL_EXPORT_SURFACES = build_operator_contract()["canonical_export_surfaces"]
HOSTED_CONTRACT_BUNDLE_COMMAND = ("package", "hosted-contract-bundle")


def run_public_cli(*args: str) -> tuple[int, str, str]:
    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            exit_code = main(public_cli_argv(args))
        except SystemExit as exc:
            exit_code = int(exc.code)
    return exit_code, stdout.getvalue(), stderr.getvalue()


def build_final_package(
    test_case: unittest.TestCase,
    input_path: Path,
    final_package_path: Path,
) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        bundle_path = Path(tmp_dir) / "bundle.json"
        build_bundle_exit, _, build_bundle_stderr = run_public_cli(
            "package",
            "artifact-bundle",
            "--input",
            str(input_path),
            "--output",
            str(bundle_path),
            "--format",
            "json",
        )
        test_case.assertEqual(build_bundle_exit, 0)
        test_case.assertEqual(build_bundle_stderr, "")

        build_package_exit, _, build_package_stderr = run_public_cli(
            "package",
            "final-package",
            "--input",
            str(input_path),
            "--artifact-bundle",
            str(bundle_path),
            "--output",
            str(final_package_path),
            "--format",
            "json",
        )
        test_case.assertEqual(build_package_exit, 0)
        test_case.assertEqual(build_package_stderr, "")


def run_hosted_contract_bundle_cli(
    final_package_path: Path,
    hosted_contract_path: Path,
) -> tuple[int, str, str]:
    return run_public_cli(
        *HOSTED_CONTRACT_BUNDLE_COMMAND,
        "--final-package",
        str(final_package_path),
        "--output",
        str(hosted_contract_path),
        "--format",
        "json",
    )


def assert_hosted_contract_bundle_cli_failure(
    test_case: unittest.TestCase,
    result: tuple[int, str, str],
    hosted_contract_path: Path,
    *expected_error_parts: str,
) -> None:
    exit_code, stdout, stderr = result
    test_case.assertEqual(exit_code, 1)
    test_case.assertEqual(stderr, "")
    payload = json.loads(stdout)
    test_case.assertFalse(payload["ok"])
    for expected_error_part in expected_error_parts:
        test_case.assertIn(expected_error_part, payload["error"])
    test_case.assertFalse(hosted_contract_path.exists())


def current_runtime_owner(current_program_contract: Path) -> dict[str, str]:
    contract = json.loads(current_program_contract.read_text(encoding="utf-8"))
    return contract["runtime_owner"]


def assert_hosted_contract_bundle_contract(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
    *,
    current_runtime_owner: Mapping[str, str],
) -> None:
    _assert_hosted_contract_bundle_header(test_case, contract_bundle)
    _assert_hosted_runtime_contracts(
        test_case,
        contract_bundle,
        current_runtime_owner=current_runtime_owner,
    )
    _assert_hosted_domain_and_schema_contracts(test_case, contract_bundle)
    _assert_hosted_authoring_contract(test_case, contract_bundle)


def _assert_hosted_contract_bundle_header(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
) -> None:
    test_case.assertEqual(contract_bundle["contract_version"], 1)
    test_case.assertEqual(contract_bundle["bundle_kind"], "hosted_contract_bundle")
    formal_entry_matrix = contract_bundle["formal_entry_matrix"]
    test_case.assertEqual(formal_entry_matrix["default_formal_entry"], "CLI")
    test_case.assertEqual(formal_entry_matrix["supported_protocol_layer"], "MCP")
    execution_identity = contract_bundle["execution_identity"]
    test_case.assertEqual(execution_identity["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
    test_case.assertEqual(execution_identity["workspace_id"], "nsfc-demo-001")
    test_case.assertEqual(execution_identity["draft_id"], "draft-v1")
    test_case.assertEqual(execution_identity["program_id"], "med-autogrant-mainline")


def _assert_hosted_runtime_contracts(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
    *,
    current_runtime_owner: Mapping[str, str],
) -> None:
    runtime_substrate = contract_bundle["runtime_substrate_contract"]
    test_case.assertEqual(runtime_substrate["runtime_owner"], "configured_family_runtime_provider")
    test_case.assertEqual(runtime_substrate["task_runtime_owner"], "one-person-lab")
    test_case.assertEqual(runtime_substrate["runtime_substrate"], "temporal")
    test_case.assertEqual(runtime_substrate["stage_executor_owner"], "codex_cli")
    for owner_field in ("current_owner_line", "active_phase", "active_tranche", "provenance_oracle"):
        test_case.assertEqual(runtime_substrate[owner_field], current_runtime_owner[owner_field])
    test_case.assertEqual(
        runtime_substrate["repo_tracked_current_program_contract"],
        "contracts/runtime-program/current-program.json",
    )

    runtime_state = contract_bundle["runtime_state_contract"]
    test_case.assertEqual(runtime_state["root"], "$CODEX_HOME/projects/med-autogrant/runtime-state/")
    test_case.assertEqual(runtime_state["session_state_owner"], "one-person-lab")
    test_case.assertTrue(runtime_state["non_repo_tracked"])

    session_contract = contract_bundle["session_contract"]
    test_case.assertEqual(session_contract["session_handle_kind"], "grant_run_id")
    test_case.assertEqual(session_contract["session_owner"], "one-person-lab")
    test_case.assertIn("owner_receipt_contract", session_contract["required_mag_authority_surfaces"])

    operator_contract = contract_bundle["operator_contract"]
    test_case.assertEqual(operator_contract["canonical_export_surfaces"], CANONICAL_EXPORT_SURFACES)
    test_case.assertEqual(operator_contract["checkpoint_aggregation_surface"], "stage-route-report")


def _assert_hosted_domain_and_schema_contracts(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
) -> None:
    state_contract = contract_bundle["state_contract"]
    test_case.assertEqual(state_contract["workspace_surface_kind"], "nsfc_workspace")
    test_case.assertEqual(state_contract["domain_authority_surface_kind"], "owner_receipt_contract")
    test_case.assertEqual(state_contract["artifact_bundle_kind"], "artifact_bundle")
    test_case.assertEqual(state_contract["final_package_kind"], "final_package")
    test_case.assertEqual(
        contract_bundle["artifact_contract"]["lineage_fields"],
        [
            "frozen_question_id",
            "selected_direction_id",
            "selected_question_id",
            "active_fit_mapping_id",
            "draft_id",
            "revision_plan_id",
        ],
    )
    audit_contract = contract_bundle["audit_contract"]
    test_case.assertEqual(audit_contract["verification_checkpoint_kind"], "verification_checkpoint")
    test_case.assertEqual(audit_contract["checkpoint_status_kind"], "checkpoint_status")
    test_case.assertEqual(
        contract_bundle["domain_entry_contract"],
        build_domain_entry_contract(),
    )
    schema_contract = contract_bundle["schema_contract"]
    test_case.assertEqual(schema_contract["schema_version"], "v1")
    test_case.assertEqual(schema_contract["schema_index_path"], "schemas/v1/schema-index.json")
    test_case.assertIn("hosted-contract-bundle.schema.json", schema_contract["contract_schema_files"])
    test_case.assertIn("submission-ready-package.schema.json", schema_contract["contract_schema_files"])


def _assert_hosted_authoring_contract(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
) -> None:
    authoring_contract = contract_bundle["authoring_contract"]
    test_case.assertEqual(authoring_contract["route_contract_version"], 1)
    test_case.assertEqual(
        authoring_contract["route_catalog_kind"],
        "author_side_route_catalog",
    )
    test_case.assertEqual(
        [route["route_id"] for route in authoring_contract["author_side_route_catalog"]],
        list(AUTHOR_SIDE_ROUTE_IDS),
    )
    route_catalog = {route["route_id"]: route for route in authoring_contract["author_side_route_catalog"]}
    test_case.assertEqual(route_catalog["critique"]["route_status"], "landed")
    test_case.assertEqual(route_catalog["critique"]["handoff_contract_kind"], "service-safe-domain-entry-command")
    test_case.assertEqual(route_catalog["critique"]["execution_surface"]["command"], "execute-critique-pass")
    test_case.assertEqual(route_catalog["revision"]["route_status"], "landed")
    test_case.assertEqual(route_catalog["revision"]["execution_surface"]["command"], "execute-revision-pass")
    test_case.assertEqual(route_catalog["hosted_contract_bundle"]["route_status"], "landed")
    test_case.assertEqual(
        route_catalog["hosted_contract_bundle"]["execution_surface"]["command"],
        "build-hosted-contract-bundle",
    )
