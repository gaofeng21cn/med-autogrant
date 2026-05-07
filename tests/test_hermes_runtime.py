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
from med_autogrant.public_cli import public_cli_argv  # noqa: E402
from support.domain_contracts import AUTHOR_SIDE_ROUTE_IDS  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"

REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}
DRAFT_ID_CONTEXT_STAGES = {"outline", "drafting", "critique", "revision", "frozen"}
PENDING_ROUTE_REQUIREMENTS = {
    "direction_screening": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "selected_direction.id",
            "selected_direction.title",
            "selected_direction.decision_status",
        ],
        "gate_fields": ["gates.direction_frozen"],
    },
    "question_refinement": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "selected_direction.id",
            "selected_direction.title",
            "selected_question.id",
            "selected_question.core_question",
            "selected_question.knowledge_boundary",
        ],
        "gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
        ],
    },
    "argument_building": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "selected_direction.id",
            "selected_question.id",
            "selected_question.core_question",
            "active_argument_chain.id",
            "active_argument_chain.necessity_claim",
        ],
        "gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
        ],
    },
    "fit_alignment": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_fit_mapping.applicant_fit_summary",
            "active_fit_mapping.unique_advantage",
        ],
        "gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
        ],
    },
    "outline": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_draft.outline_count",
        ],
        "gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
        ],
    },
    "drafting": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_draft.outline_count",
            "active_draft.section_count",
        ],
        "gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
        ],
    },
    "critique": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "current_selection.active_revision_plan_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_revision_plan.id",
            "active_revision_plan.execution_status",
            "active_critique.id",
            "active_critique.verdict",
            "active_critique.blocking_issue_count",
        ],
        "gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
            "gates.presubmission_frozen",
        ],
    },
    "frozen": {
        "summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "current_selection.active_revision_plan_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_draft.section_count",
            "active_revision_plan.id",
            "active_revision_plan.execution_status",
            "active_critique.id",
            "active_critique.verdict",
        ],
        "gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
            "gates.presubmission_frozen",
        ],
    },
}


def _service_safe_surface(command: str) -> dict[str, str]:
    return {
        "surface_kind": "service-safe-domain-entry-command",
        "entry_adapter": "MedAutoGrantDomainEntry",
        "command": command,
    }


def _expected_landed_route(route_id: str) -> dict[str, object]:
    return {
        "route_id": route_id,
        "route_status": "landed",
        "executor_owner": "med-autogrant",
        "execution_surface": _service_safe_surface(
            {
                "direction_screening": "execute-direction-screening-pass",
                "question_refinement": "execute-question-refinement-pass",
                "argument_building": "execute-argument-building-pass",
                "fit_alignment": "execute-fit-alignment-pass",
                "outline": "execute-outline-pass",
                "drafting": "execute-drafting-pass",
                "critique": "execute-critique-pass",
                "revision": "execute-revision-pass",
                "frozen": "execute-freeze-pass",
                "artifact_bundle": "build-artifact-bundle",
                "final_package": "build-final-package",
                "hosted_contract_bundle": "build-hosted-contract-bundle",
            }[route_id]
        ),
        "handoff_contract_kind": "service-safe-domain-entry-command",
    }


def _expected_route(route_id: str, *, source_stage: str) -> dict[str, object]:
    del source_stage
    return _expected_landed_route(route_id)


class HermesRuntimeCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_validate_workspace_dispatches_through_hermes_runtime_substrate(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "validate-workspace",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "lifecycle_stage": "critique",
            "error_count": 0,
            "errors": [],
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "validate-workspace",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "validate-workspace",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
            }
        )

    def test_run_local_dispatches_through_hermes_runtime_substrate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "journal.json"
            expected_payload = {
                "ok": True,
                "command": "runtime-run",
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "draft_id": "draft-test",
                "lifecycle_stage": "critique",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
                "journal_path": str(journal_path),
                "attempt_index": 1,
                "stop_reason": {
                    "code": "stage_action_required",
                    "reason": "runtime owned by Hermes",
                    "current_stage": "critique",
                    "recommended_next_stage": "revision",
                    "checkpoint_status": "forward_progress",
                    "requires_human_confirmation": False,
                    "forced_rollback_stage": None,
                    "forced_rollback_reason": None,
                },
                "stage_action_envelope": None,
                "route_report": {"ok": True},
                "resume": {
                    "command": "runtime-resume",
                    "journal_path": str(journal_path),
                },
            }

            with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
                entry = entry_class.return_value
                entry.dispatch.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "runtime-run",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH),
                    "--journal",
                    str(journal_path),
                    "--format",
                    "json",
                )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertEqual(json.loads(stdout), expected_payload)
            entry.dispatch.assert_called_once_with(
                {
                    "command": "runtime-run",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH),
                    "journal_path": str(journal_path),
                }
            )


class HermesRuntimeSubstrateFlowTest(unittest.TestCase):
    def test_hermes_runtime_substrate_keeps_revision_and_export_paths_identity_stable(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        self.assertEqual(runtime.runtime_owner, "Hermes")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            critique_journal_path = tmp_root / "critique-journal.json"
            revised_workspace_path = tmp_root / "revised.json"
            revised_bundle_path = tmp_root / "revised-bundle.json"
            revised_journal_path = tmp_root / "revised-journal.json"
            frozen_bundle_path = tmp_root / "frozen-bundle.json"
            final_package_path = tmp_root / "final-package.json"
            hosted_contract_path = tmp_root / "hosted-contract.json"

            critique_report = runtime.stage_route_report(input_path=str(CRITIQUE_EXAMPLE_PATH))
            self.assertTrue(critique_report["ok"])
            self.assertEqual(critique_report["verification_checkpoint"]["identity"]["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")

            critique_run = runtime.run_local(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                journal_path=str(critique_journal_path),
            )
            self.assertTrue(critique_run["ok"])
            self.assertEqual(critique_run["stop_reason"]["recommended_next_stage"], "revision")
            self.assertEqual(
                critique_run["stage_action_envelope"]["executor_routing_contract"],
                {
                    "contract_version": 1,
                    "current_stage_route": _expected_route("critique", source_stage="critique"),
                    "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                },
            )

            revision_return_run = runtime.run_local(
                input_path=str(REVISION_EXAMPLE_PATH),
                journal_path=str(tmp_root / "revision-return-journal.json"),
            )
            self.assertTrue(revision_return_run["ok"])
            self.assertEqual(revision_return_run["stop_reason"]["recommended_next_stage"], "critique")
            self.assertEqual(
                revision_return_run["stage_action_envelope"]["executor_routing_contract"],
                {
                    "contract_version": 1,
                    "current_stage_route": _expected_route("revision", source_stage="revision"),
                    "recommended_executor_route": _expected_route("critique", source_stage="revision"),
                },
            )

            revised_payload = runtime.execute_revision_pass(
                input_path=str(RE_REVIEW_EXAMPLE_PATH),
                output_path=str(revised_workspace_path),
            )
            self.assertTrue(revised_payload["ok"])
            self.assertEqual(revised_payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(revised_payload["draft_id"], "draft-v1")

            revised_report = runtime.stage_route_report(input_path=str(revised_workspace_path))
            self.assertTrue(revised_report["ok"])
            self.assertEqual(
                revised_report["verification_checkpoint"]["identity"]["reviewed_revision_plan_id"],
                "revision-v1",
            )

            revised_bundle = runtime.build_artifact_bundle(
                input_path=str(revised_workspace_path),
                output_path=str(revised_bundle_path),
            )
            self.assertTrue(revised_bundle["ok"])
            self.assertEqual(revised_bundle["bundle"]["draft_id"], "draft-v1")

            revised_run = runtime.run_local(
                input_path=str(revised_workspace_path),
                journal_path=str(revised_journal_path),
            )
            self.assertTrue(revised_run["ok"])
            self.assertEqual(revised_run["stop_reason"]["recommended_next_stage"], "revision")

            frozen_bundle = runtime.build_artifact_bundle(
                input_path=str(FROZEN_EXAMPLE_PATH),
                output_path=str(frozen_bundle_path),
            )
            self.assertTrue(frozen_bundle["ok"])

            final_package = runtime.build_final_package(
                input_path=str(FROZEN_EXAMPLE_PATH),
                artifact_bundle_path=str(frozen_bundle_path),
                output_path=str(final_package_path),
            )
            self.assertTrue(final_package["ok"])
            self.assertEqual(final_package["final_package"]["checkpoint_summary"]["checkpoint_status"], "submission_frozen")

            hosted_contract = runtime.build_hosted_contract_bundle(
                final_package_path=str(final_package_path),
                output_path=str(hosted_contract_path),
            )
            self.assertTrue(hosted_contract["ok"])
            self.assertEqual(
                hosted_contract["hosted_contract_bundle"]["execution_identity"],
                {
                    "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    "workspace_id": "nsfc-demo-001",
                    "draft_id": "draft-v1",
                    "program_id": "med-autogrant-mainline",
                },
            )

    def test_executor_routing_contract_publishes_landed_route_catalog_only(self) -> None:
        from med_autogrant.hermes_runtime import _build_executor_routing_contract

        drafting_contract = _build_executor_routing_contract(
            current_stage="drafting",
            recommended_next_stage="critique",
            include_route_catalog=True,
        )
        self.assertEqual(
            drafting_contract["current_stage_route"],
            _expected_route("drafting", source_stage="drafting"),
        )
        self.assertEqual(
            drafting_contract["recommended_executor_route"],
            _expected_route("critique", source_stage="drafting"),
        )
        self.assertNotIn("handoff_requirements", drafting_contract["recommended_executor_route"])

        critique_reroute_contract = _build_executor_routing_contract(
            current_stage="critique",
            recommended_next_stage="question_refinement",
        )
        self.assertEqual(
            critique_reroute_contract["recommended_executor_route"],
            _expected_route("question_refinement", source_stage="critique"),
        )
        self.assertNotIn("handoff_requirements", critique_reroute_contract["recommended_executor_route"])

        self.assertEqual(
            [
                route["route_id"]
                for route in drafting_contract["author_side_route_catalog"]
            ],
            list(AUTHOR_SIDE_ROUTE_IDS),
        )

    def test_run_local_fails_closed_on_invalid_executor_routing_contract_shape(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate
        from med_autogrant.workspace import WorkspaceStateError

        runtime = HermesRuntimeSubstrate()
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "critique-journal.json"
            with patch(
                "med_autogrant.hermes_runtime._build_executor_routing_contract",
                return_value={
                    "contract_version": 1,
                    "current_stage_route": {
                        "route_id": "critique",
                        "route_status": "pending",
                    },
                },
            ):
                with self.assertRaises(WorkspaceStateError):
                    runtime.run_local(
                        input_path=str(CRITIQUE_EXAMPLE_PATH),
                        journal_path=str(journal_path),
                    )


class HostedContractBundleBridgeTest(unittest.TestCase):
    def test_hosted_contract_bundle_payload_uses_split_runtime_helpers(self) -> None:
        from med_autogrant.hosted_contract_bundle import build_hosted_contract_bundle_payload

        final_package = {
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "frozen",
        }
        hosted_contract_bundle = {
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "program_id": "program-test",
            "lifecycle_stage": "frozen",
        }
        with patch(
            "med_autogrant.hosted_contract_bundle._read_final_package",
            return_value=final_package,
        ) as read_final_package, patch(
            "med_autogrant.hosted_contract_bundle._validate_required_final_package_fields",
        ) as validate_final_package, patch(
            "med_autogrant.hosted_contract_bundle._read_current_program_contract",
            return_value={"program_id": "program-test"},
        ), patch(
            "med_autogrant.hosted_contract_bundle._read_program_id",
            return_value="program-test",
        ), patch(
            "med_autogrant.hosted_contract_bundle._build_runtime_substrate_contract",
            return_value={},
        ), patch(
            "med_autogrant.hosted_contract_bundle._build_runtime_state_contract",
            return_value={},
        ), patch(
            "med_autogrant.hosted_contract_bundle._build_operator_contract",
            return_value={},
        ), patch(
            "med_autogrant.hosted_contract_bundle.build_domain_entry_contract",
            return_value={},
        ), patch(
            "med_autogrant.hosted_contract_bundle._build_schema_contract",
            return_value={},
        ), patch(
            "med_autogrant.hosted_contract_bundle._build_hosted_authoring_contract",
            return_value={},
        ), patch(
            "med_autogrant.hosted_contract_bundle.build_hosted_contract_bundle_document",
            return_value=hosted_contract_bundle,
        ) as build_document, patch(
            "med_autogrant.hosted_contract_bundle._validate_hosted_contract_bundle",
        ) as validate_bundle, patch(
            "med_autogrant.hosted_contract_bundle._guard_output_identity",
        ) as guard_output, patch(
            "med_autogrant.hosted_contract_bundle._write_hosted_contract_bundle",
        ) as write_bundle:
            payload = build_hosted_contract_bundle_payload(
                final_package_path="/tmp/final-package.json",
                output_path="/tmp/hosted-contract.json",
            )

        self.assertEqual(payload["hosted_contract_bundle"], hosted_contract_bundle)
        read_final_package.assert_called_once_with("/tmp/final-package.json")
        validate_final_package.assert_called_once_with(final_package)
        build_document.assert_called_once()
        validate_bundle.assert_called_once_with(
            hosted_contract_bundle,
            grant_run_id="grant-run-test",
            workspace_id="workspace-test",
            lifecycle_stage="frozen",
        )
        guard_output.assert_called_once()
        write_bundle.assert_called_once_with(
            Path("/tmp/hosted-contract.json").resolve(),
            hosted_contract_bundle,
        )


class ArtifactBundleHandoffTest(unittest.TestCase):
    def test_build_artifact_bundle_uses_hermes_handoff_owner(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        expected_bundle = {
            "bundle_version": 1,
            "bundle_kind": "artifact_bundle",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "bundle.json"
            with patch(
                "med_autogrant.hermes_runtime.build_artifact_bundle_document",
                create=True,
                return_value=expected_bundle,
            ) as build_document, patch(
                "med_autogrant.hermes_runtime._guard_artifact_bundle_output_identity",
                create=True,
            ) as guard_output, patch(
                "med_autogrant.hermes_runtime._write_artifact_bundle_output",
                create=True,
            ) as write_output:
                payload = runtime.build_artifact_bundle(
                    input_path=str(FROZEN_EXAMPLE_PATH),
                    output_path=str(bundle_path),
                )

        self.assertEqual(payload["bundle"], expected_bundle)
        build_document.assert_called_once()
        guard_output.assert_called_once()
        write_output.assert_called_once_with(bundle_path.resolve(), expected_bundle)


class RevisionExecutionHandoffTest(unittest.TestCase):
    def test_execute_critique_pass_uses_codex_cli_handoff_owner(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        expected_critique_workspace = {
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "lifecycle_stage": "critique",
            "current_selection": {
                "active_draft_id": "draft-test",
                "active_revision_plan_id": "revision-plan-test",
            },
        }
        expected_critique_execution = {
            "critique_id": "critique-test",
            "active_revision_plan_id": "revision-plan-test",
            "verdict": "major_revision",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_path = Path(tmp_dir) / "critique.json"
            with patch(
                "med_autogrant.hermes_runtime.build_critique_execution_document",
                create=True,
                return_value={
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "active_revision_plan_id": "revision-plan-test",
                    "lifecycle_stage": "critique",
                    "critique_execution": expected_critique_execution,
                    "critique_workspace": expected_critique_workspace,
                },
            ) as build_document, patch(
                "med_autogrant.hermes_runtime._guard_critique_output_identity",
                create=True,
            ) as guard_output, patch(
                "med_autogrant.hermes_runtime._write_revised_workspace_output",
                create=True,
            ) as write_output:
                payload = runtime.execute_critique_pass(
                    input_path=str(REVISION_EXAMPLE_PATH),
                    output_path=str(workspace_path),
                )

        self.assertEqual(payload["critique_workspace"], expected_critique_workspace)
        self.assertEqual(payload["critique_execution"], expected_critique_execution)
        build_document.assert_called_once()
        guard_output.assert_called_once()
        write_output.assert_called_once_with(workspace_path.resolve(), expected_critique_workspace)

    def test_execute_critique_pass_forwards_explicit_executor_kind(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()

        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_path = Path(tmp_dir) / "critique.json"
            with patch(
                "med_autogrant.hermes_runtime.build_critique_execution_document",
                create=True,
                return_value={
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "active_revision_plan_id": "revision-plan-test",
                    "lifecycle_stage": "critique",
                    "critique_execution": {
                        "critique_id": "critique-test",
                        "active_revision_plan_id": "revision-plan-test",
                        "verdict": "major_revision",
                    },
                    "critique_workspace": {
                        "grant_run_id": "grant-run-test",
                        "workspace_id": "workspace-test",
                        "lifecycle_stage": "critique",
                    },
                },
            ) as build_document, patch(
                "med_autogrant.hermes_runtime._guard_critique_output_identity",
                create=True,
            ), patch(
                "med_autogrant.hermes_runtime._write_revised_workspace_output",
                create=True,
            ):
                runtime.execute_critique_pass(
                    input_path=str(REVISION_EXAMPLE_PATH),
                    output_path=str(workspace_path),
                    executor_kind="hermes_native_proof",
                )

        _, kwargs = build_document.call_args
        self.assertEqual(kwargs["executor_kind"], "hermes_native_proof")

    def test_execute_revision_pass_uses_hermes_handoff_owner(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        expected_revised_workspace = {
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
        }
        expected_revision_execution = {
            "active_revision_plan_id": "revision-plan-test",
            "comparison_summary": {"changed_section_count": 1},
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_path = Path(tmp_dir) / "revised.json"
            with patch(
                "med_autogrant.hermes_runtime.build_revision_execution_document",
                create=True,
                return_value={
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "active_revision_plan_id": "revision-plan-test",
                    "lifecycle_stage": "critique",
                    "revision_execution": expected_revision_execution,
                    "revised_workspace": expected_revised_workspace,
                },
            ) as build_document, patch(
                "med_autogrant.hermes_runtime._guard_revision_output_identity",
                create=True,
            ) as guard_output, patch(
                "med_autogrant.hermes_runtime._write_revised_workspace_output",
                create=True,
            ) as write_output:
                payload = runtime.execute_revision_pass(
                    input_path=str(RE_REVIEW_EXAMPLE_PATH),
                    output_path=str(workspace_path),
                )

        self.assertEqual(payload["revised_workspace"], expected_revised_workspace)
        self.assertEqual(payload["revision_execution"], expected_revision_execution)
        build_document.assert_called_once()
        guard_output.assert_called_once()
        write_output.assert_called_once_with(workspace_path.resolve(), expected_revised_workspace)


class FinalPackageHandoffTest(unittest.TestCase):
    def test_build_final_package_uses_hermes_handoff_owner(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            bundle_path = tmp_root / "bundle.json"
            package_path = tmp_root / "package.json"
            runtime.build_artifact_bundle(
                input_path=str(FROZEN_EXAMPLE_PATH),
                output_path=str(bundle_path),
            )
            expected_final_package = {
                "package_version": 1,
                "package_kind": "final_package",
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "draft_id": "draft-test",
                "lifecycle_stage": "frozen",
            }

            with patch(
                "med_autogrant.hermes_runtime._read_artifact_bundle",
                create=True,
                return_value={"manifest": {}, "artifacts": [1, 2]},
            ) as read_bundle, patch(
                "med_autogrant.hermes_runtime.build_final_package_document",
                create=True,
                return_value=expected_final_package,
            ) as build_document, patch(
                "med_autogrant.hermes_runtime._guard_final_package_output_identity",
                create=True,
            ) as guard_output, patch(
                "med_autogrant.hermes_runtime._write_final_package_output",
                create=True,
            ) as write_output:
                payload = runtime.build_final_package(
                    input_path=str(FROZEN_EXAMPLE_PATH),
                    artifact_bundle_path=str(bundle_path),
                    output_path=str(package_path),
                )

        self.assertEqual(payload["final_package"], expected_final_package)
        read_bundle.assert_called_once()
        build_document.assert_called_once()
        guard_output.assert_called_once()
        write_output.assert_called_once_with(package_path.resolve(), expected_final_package)


if __name__ == "__main__":
    unittest.main()
