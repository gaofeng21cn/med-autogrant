from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.domain_entry_contract import build_domain_entry_contract  # noqa: E402
from med_autogrant.public_cli import public_cli_argv, public_command_label  # noqa: E402
from med_autogrant import hosted_contract_bundle as hosted_contract_bundle_module  # noqa: E402
from support.domain_contracts import (  # noqa: E402
    AUTHOR_SIDE_ROUTE_IDS,
    CANONICAL_EXPORT_SURFACES,
)


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"

PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND = public_command_label("build-product-entry")



class HostedContractBundleCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_build_hosted_contract_bundle_writes_expected_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "build-hosted-contract-bundle")
            self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["output_path"], str(hosted_contract_path.resolve()))

            contract_bundle = payload["hosted_contract_bundle"]
            self.assertEqual(contract_bundle["contract_version"], 1)
            self.assertEqual(contract_bundle["bundle_kind"], "hosted_contract_bundle")
            self.assertEqual(
                contract_bundle["formal_entry_matrix"],
                {
                    "default_formal_entry": "CLI",
                    "supported_protocol_layer": "MCP",
                    "internal_controller_surface": "controller",
                },
            )
            self.assertEqual(
                contract_bundle["execution_identity"],
                {
                    "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    "workspace_id": "nsfc-demo-001",
                    "draft_id": "draft-v1",
                    "program_id": "med-autogrant-mainline",
                },
            )
            self.assertEqual(
                contract_bundle["runtime_substrate_contract"],
                {
                    "runtime_owner": "Hermes",
                    "current_owner_line": self._current_runtime_owner()["current_owner_line"],
                    "active_phase": self._current_runtime_owner()["active_phase"],
                    "active_tranche": self._current_runtime_owner()["active_tranche"],
                    "compatibility_bridge": self._current_runtime_owner()["compatibility_bridge"],
                    "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                },
            )
            self.assertEqual(
                contract_bundle["runtime_state_contract"],
                {
                    "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                    "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
                    "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                    "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                    "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                    "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                    "non_repo_tracked": True,
                },
            )
            self.assertEqual(
                contract_bundle["session_contract"],
                {
                    "session_handle_kind": "grant_run_id",
                    "start_entry": "runtime-run",
                    "resume_entry": "runtime-resume",
                    "required_local_surfaces": [
                        "runtime-run",
                        "runtime-resume",
                        "build-artifact-bundle",
                        "build-final-package",
                        "run_journal",
                        "stage_action_envelope",
                    ],
                },
            )
            self.assertEqual(
                contract_bundle["operator_contract"],
                {
                    "canonical_audit_surfaces": [
                        "validate-workspace",
                        "summarize-workspace",
                        "grant-intake-audit",
                        "grant-evidence-grounding",
                        "grant-quality-scorecard",
                        "grant-quality-closure-dossier",
                        "grant-quality-diff",
                        "next-step",
                        "critique-summary",
                        "stage-route-report",
                    ],
                    "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
                    "checkpoint_aggregation_surface": "stage-route-report",
                },
            )
            self.assertEqual(
                contract_bundle["state_contract"],
                {
                    "workspace_surface_kind": "nsfc_workspace",
                    "run_journal_kind": "local_run_journal",
                    "stage_action_envelope_kind": "stage_action_envelope",
                    "artifact_bundle_kind": "artifact_bundle",
                    "final_package_kind": "final_package",
                },
            )
            self.assertEqual(
                contract_bundle["artifact_contract"],
                {
                    "artifact_bundle_manifest_kind": "artifact_bundle_manifest",
                    "final_package_manifest_kind": "freeze_manifest",
                    "lineage_fields": [
                        "frozen_question_id",
                        "selected_direction_id",
                        "selected_question_id",
                        "active_fit_mapping_id",
                        "draft_id",
                        "revision_plan_id",
                    ],
                },
            )
            self.assertEqual(
                contract_bundle["audit_contract"],
                {
                    "verification_checkpoint_kind": "verification_checkpoint",
                    "checkpoint_status_kind": "checkpoint_status",
                    "reviewed_revision_evidence_kind": "reviewed_revision_evidence",
                },
            )
            self.assertEqual(
                contract_bundle["domain_entry_contract"],
                build_domain_entry_contract(),
            )
            self.assertEqual(
                contract_bundle["schema_contract"],
                {
                    "schema_version": "v1",
                    "schema_index_path": "schemas/v1/schema-index.json",
                    "aggregate_root_schema": "nsfc-workspace.schema.json",
                    "contract_schema_files": [
                        "service-safe-domain-surface.schema.json",
                        "executor-routing-contract.schema.json",
                        "product-entry.schema.json",
                        "grant-intake-audit.schema.json",
                        "grant-evidence-grounding.schema.json",
                        "grant-quality-scorecard.schema.json",
                        "grant-quality-closure-dossier.schema.json",
                        "grant-quality-diff.schema.json",
                        "grant-autonomy-controller-input.schema.json",
                        "grant-autonomy-controller-report.schema.json",
                        "funding-landscape-discovery-input.schema.json",
                        "funding-landscape-discovery.schema.json",
                        "funding-landscape-cache.schema.json",
                        "funding-landscape-diff-report.schema.json",
                        "project-profile-selection-input.schema.json",
                        "project-profile-selection.schema.json",
                        "critique-loop-report.schema.json",
                        "authoring-mainline-loop-report.schema.json",
                        "hosted-contract-bundle.schema.json",
                        "submission-ready-package.schema.json",
                    ],
                },
            )
            self.assertEqual(contract_bundle["authoring_contract"]["route_contract_version"], 1)
            self.assertEqual(contract_bundle["authoring_contract"]["route_catalog_kind"], "author_side_route_catalog")
            self.assertEqual(
                [route["route_id"] for route in contract_bundle["authoring_contract"]["author_side_route_catalog"]],
                list(AUTHOR_SIDE_ROUTE_IDS),
            )
            route_catalog = {
                route["route_id"]: route
                for route in contract_bundle["authoring_contract"]["author_side_route_catalog"]
            }
            self.assertEqual(route_catalog["critique"]["route_status"], "landed")
            self.assertEqual(route_catalog["critique"]["handoff_contract_kind"], "service-safe-domain-entry-command")
            self.assertEqual(route_catalog["critique"]["execution_surface"]["command"], "execute-critique-pass")
            self.assertEqual(route_catalog["revision"]["route_status"], "landed")
            self.assertEqual(route_catalog["revision"]["execution_surface"]["command"], "execute-revision-pass")
            self.assertEqual(route_catalog["hosted_contract_bundle"]["route_status"], "landed")
            self.assertEqual(
                route_catalog["hosted_contract_bundle"]["execution_surface"]["command"],
                "build-hosted-contract-bundle",
            )
            self.assertEqual(json.loads(hosted_contract_path.read_text(encoding="utf-8")), contract_bundle)

    def test_build_hosted_contract_bundle_fails_closed_on_invalid_hosted_contract_shape(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate
        from med_autogrant.workspace import WorkspaceStateError

        runtime = HermesRuntimeSubstrate()
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)

            with patch(
                "med_autogrant.hermes_runtime.build_hosted_contract_bundle_document",
                return_value={
                    "contract_version": 1,
                    "bundle_kind": "hosted_contract_bundle",
                },
            ):
                with self.assertRaises(WorkspaceStateError):
                    runtime.build_hosted_contract_bundle(
                        final_package_path=str(final_package_path),
                        output_path=str(hosted_contract_path),
                    )

    def test_build_hosted_contract_bundle_fails_closed_for_non_final_package_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "not-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            final_package_path.write_text(
                json.dumps(
                    {
                        "package_kind": "artifact_bundle",
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        "workspace_id": "nsfc-demo-001",
                        "draft_id": "draft-v1",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("final package kind 非法", payload["error"])

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_freeze_manifest_is_not_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-freeze-manifest-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["freeze_manifest"] = []
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("freeze_manifest", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_checkpoint_summary_is_not_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-checkpoint-summary-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["checkpoint_summary"] = []
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("checkpoint_summary", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_lineage_is_not_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-lineage-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["lineage"] = []
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("lineage", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_package_version_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "missing-package-version-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package.pop("package_version")
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("package_version", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_lifecycle_stage_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "missing-lifecycle-stage-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package.pop("lifecycle_stage")
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("lifecycle_stage", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_identity_fields_are_not_nonempty_strings(self) -> None:
        cases = (
            ("grant_run_id", []),
            ("workspace_id", {}),
            ("draft_id", []),
        )
        for field, bad_value in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"bad-{field}-final-package.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package[field] = bad_value
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    exit_code, stdout, stderr = self.run_cli(
                        "build-hosted-contract-bundle",
                        "--final-package",
                        str(final_package_path),
                        "--output",
                        str(hosted_contract_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn("final package 缺少字段", payload["error"])
                    self.assertIn(field, payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_freeze_manifest_missing_required_fields(self) -> None:
        required_fields = (
            "draft_version_label",
            "draft_status",
            "active_revision_plan_id",
            "critique_id",
            "checkpoint_status",
            "presubmission_frozen",
        )
        for field in required_fields:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"missing-freeze-manifest-{field}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["freeze_manifest"].pop(field)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    exit_code, stdout, stderr = self.run_cli(
                        "build-hosted-contract-bundle",
                        "--final-package",
                        str(final_package_path),
                        "--output",
                        str(hosted_contract_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn("final package freeze_manifest 缺少字段", payload["error"])
                    self.assertIn(field, payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_lineage_values_are_not_nonempty_strings(self) -> None:
        cases = (
            ("frozen_question_id", ""),
            ("selected_direction_id", ""),
            ("selected_question_id", ""),
            ("active_fit_mapping_id", []),
            ("draft_id", ""),
            ("revision_plan_id", []),
        )
        for field, bad_value in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"bad-lineage-value-{field}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["lineage"][field] = bad_value
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    exit_code, stdout, stderr = self.run_cli(
                        "build-hosted-contract-bundle",
                        "--final-package",
                        str(final_package_path),
                        "--output",
                        str(hosted_contract_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"final package lineage.{field} 非法", payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_existing_output_identity_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            hosted_contract_path.write_text(
                json.dumps(
                    {
                        "grant_run_id": "other-run",
                        "workspace_id": "other-workspace",
                        "draft_id": "other-draft",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("hosted contract output identity 不匹配", payload["error"])

    def test_build_hosted_contract_bundle_fails_closed_when_existing_execution_identity_program_id_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            hosted_contract_path.write_text(
                json.dumps(
                    {
                        "bundle_kind": "hosted_contract_bundle",
                        "execution_identity": {
                            "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                            "workspace_id": "nsfc-demo-001",
                            "draft_id": "draft-v1",
                            "program_id": "other-program",
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("hosted contract output identity 不匹配", payload["error"])
            self.assertIn("other-program", payload["error"])
            self.assertIn("med-autogrant-mainline", payload["error"])

    def test_build_hosted_contract_bundle_allows_overwrite_for_same_identity_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)

            first_exit, first_stdout, first_stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )
            self.assertEqual(first_exit, 0)
            self.assertEqual(first_stderr, "")
            first_payload = json.loads(first_stdout)
            self.assertTrue(first_payload["ok"])

            second_exit, second_stdout, second_stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(second_exit, 0)
            self.assertEqual(second_stderr, "")
            second_payload = json.loads(second_stdout)
            self.assertTrue(second_payload["ok"])
            self.assertEqual(
                json.loads(hosted_contract_path.read_text(encoding="utf-8")),
                second_payload["hosted_contract_bundle"],
            )

    def _build_final_package(self, input_path: Path, final_package_path: Path) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "bundle.json"
            build_bundle_exit, _, build_bundle_stderr = self.run_cli(
                "build-artifact-bundle",
                "--input",
                str(input_path),
                "--output",
                str(bundle_path),
                "--format",
                "json",
            )
            self.assertEqual(build_bundle_exit, 0)
            self.assertEqual(build_bundle_stderr, "")

            build_package_exit, _, build_package_stderr = self.run_cli(
                "build-final-package",
                "--input",
                str(input_path),
                "--artifact-bundle",
                str(bundle_path),
                "--output",
                str(final_package_path),
                "--format",
                "json",
            )
            self.assertEqual(build_package_exit, 0)
            self.assertEqual(build_package_stderr, "")

    def _current_runtime_owner(self) -> dict[str, str]:
        contract = json.loads(CURRENT_PROGRAM_CONTRACT.read_text(encoding="utf-8"))
        return contract["runtime_owner"]


if __name__ == "__main__":
    unittest.main()
