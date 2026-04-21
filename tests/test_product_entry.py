from __future__ import annotations

from copy import deepcopy
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.public_cli import public_cli_argv, public_cli_command, public_command_label  # noqa: E402
from med_autogrant.control_plane import read_program_id, resolve_runtime_state_root  # noqa: E402
from med_autogrant.workspace import WorkspaceStateError  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"

AUTHOR_SIDE_ROUTE_IDS = (
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
    "artifact_bundle",
    "final_package",
    "hosted_contract_bundle",
)
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

PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND = public_command_label("build-product-entry")
SUPPORTED_DOMAIN_ENTRY_COMMANDS = [
    "probe-upstream-hermes",
    "validate-workspace",
    "summarize-workspace",
    "grant-intake-audit",
    "grant-evidence-grounding",
    "next-step",
    "critique-summary",
    "stage-route-report",
    "runtime-run",
    "runtime-resume",
    "execute-direction-screening-pass",
    "execute-question-refinement-pass",
    "execute-argument-building-pass",
    "execute-fit-alignment-pass",
    "execute-outline-pass",
    "execute-drafting-pass",
    "build-artifact-bundle",
    "execute-critique-pass",
    "execute-revision-pass",
    "execute-freeze-pass",
    "build-final-package",
    "build-hosted-contract-bundle",
    "build-submission-ready-package",
]
DOMAIN_ENTRY_COMMAND_CONTRACTS = [
    {"command": "probe-upstream-hermes", "required_fields": [], "optional_fields": []},
    {"command": "validate-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "summarize-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-intake-audit", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-evidence-grounding", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "next-step", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "critique-summary", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "stage-route-report", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "runtime-run", "required_fields": ["input_path"], "optional_fields": ["journal_path"]},
    {"command": "runtime-resume", "required_fields": ["journal_path"], "optional_fields": []},
    {"command": "execute-direction-screening-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-question-refinement-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-argument-building-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-fit-alignment-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-outline-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-drafting-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "build-artifact-bundle", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-critique-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-revision-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-freeze-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {
        "command": "build-final-package",
        "required_fields": ["input_path", "artifact_bundle_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-hosted-contract-bundle",
        "required_fields": ["final_package_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-submission-ready-package",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": [],
    },
]
CANONICAL_EXPORT_SURFACES = [
    "execute-direction-screening-pass",
    "execute-question-refinement-pass",
    "execute-argument-building-pass",
    "execute-fit-alignment-pass",
    "execute-outline-pass",
    "execute-drafting-pass",
    "execute-critique-pass",
    "execute-revision-pass",
    "execute-freeze-pass",
    "build-artifact-bundle",
    "build-final-package",
    "build-hosted-contract-bundle",
    "build-submission-ready-package",
]
CANONICAL_EXPORT_SURFACES = [
    "execute-direction-screening-pass",
    "execute-question-refinement-pass",
    "execute-argument-building-pass",
    "execute-fit-alignment-pass",
    "execute-outline-pass",
    "execute-drafting-pass",
    "execute-critique-pass",
    "execute-revision-pass",
    "execute-freeze-pass",
    "build-artifact-bundle",
    "build-final-package",
    "build-hosted-contract-bundle",
    "build-submission-ready-package",
]


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


def _expected_pending_route(route_id: str, *, source_stage: str) -> dict[str, object]:
    requirements = PENDING_ROUTE_REQUIREMENTS[route_id]
    required_domain_surfaces = [_service_safe_surface("summarize-workspace")]
    if source_stage in REVIEW_CONTEXT_STAGES:
        required_domain_surfaces.append(_service_safe_surface("critique-summary"))
    required_domain_surfaces.append(_service_safe_surface("stage-route-report"))

    required_identity_fields = ["grant_run_id", "workspace_id"]
    if source_stage in DRAFT_ID_CONTEXT_STAGES:
        required_identity_fields.append("draft_id")

    return {
        "route_id": route_id,
        "route_status": "pending",
        "executor_owner": "med-autogrant",
        "execution_surface": None,
        "handoff_contract_kind": "handoff-required",
        "handoff_requirements": {
            "contract_kind": f"{route_id}-pending-handoff",
            "workspace_surface_kind": "nsfc_workspace",
            "required_domain_surfaces": required_domain_surfaces,
            "required_identity_fields": required_identity_fields,
            "required_summary_fields": requirements["summary_fields"],
            "required_gate_fields": requirements["gate_fields"],
        },
    }


def _expected_route(route_id: str, *, source_stage: str) -> dict[str, object]:
    del source_stage
    return _expected_landed_route(route_id)


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


class ProductEntryCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_build_product_entry_dispatches_shell(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "build-product-entry",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "output_path": None,
            "product_entry": {
                "entry_kind": "med_auto_grant_product_entry",
                "entry_mode": "direct",
                "task_intent": "tighten-grant-mainline",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--entry-mode",
                "direct",
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
            output_path=None,
            funding_call=None,
        )

    def test_grant_progress_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-progress",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "progress_projection": {
                "projection_kind": "grant_progress",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.read_grant_progress.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "grant-progress",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.read_grant_progress.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

    def test_grant_cockpit_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-cockpit",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "grant_cockpit": {
                "cockpit_kind": "grant_cockpit",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.read_grant_cockpit.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "grant-cockpit",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.read_grant_cockpit.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

    def test_grant_direct_entry_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-direct-entry",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "grant_direct_entry": {
                "entry_kind": "grant_direct_entry",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_grant_direct_entry.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "grant-direct-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_grant_direct_entry.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
            funding_call=None,
        )

    def test_product_entry_manifest_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "product-entry-manifest",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "product_entry_manifest": {
                "manifest_kind": "med_auto_grant_product_entry_manifest",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_product_entry_manifest.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product-entry-manifest",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_product_entry_manifest.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            funding_call=None,
        )

    def test_product_preflight_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "product-preflight",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "product_entry_preflight": {
                "surface_kind": "product_entry_preflight",
                "ready_to_try_now": True,
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_product_entry_preflight.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product-preflight",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_product_entry_preflight.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )


class ProductEntryEnvelopeTest(unittest.TestCase):
    def test_product_entry_builds_shared_envelope_for_direct_and_opl_handoff(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()

        direct_payload = entry.build(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        handoff_payload = entry.build(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="opl-handoff",
            task_intent="tighten-grant-mainline",
        )

        direct_envelope = direct_payload["product_entry"]
        handoff_envelope = handoff_payload["product_entry"]

        self.assertEqual(direct_payload["command"], "build-product-entry")
        self.assertEqual(direct_payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(direct_payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(direct_payload["draft_id"], "draft-v1")
        self.assertEqual(direct_payload["lifecycle_stage"], "critique")

        self.assertEqual(direct_envelope["entry_kind"], "med_auto_grant_product_entry")
        self.assertEqual(direct_envelope["entry_version"], 1)
        self.assertEqual(direct_envelope["target_domain_id"], "med-autogrant")
        self.assertEqual(direct_envelope["task_intent"], "tighten-grant-mainline")
        self.assertEqual(direct_envelope["entry_mode"], "direct")
        self.assertEqual(handoff_envelope["entry_mode"], "opl-handoff")

        self.assertEqual(direct_envelope["workspace_locator"], handoff_envelope["workspace_locator"])
        self.assertEqual(direct_envelope["runtime_session_contract"], handoff_envelope["runtime_session_contract"])
        self.assertEqual(direct_envelope["return_surface_contract"], handoff_envelope["return_surface_contract"])
        self.assertEqual(direct_envelope["domain_payload"], handoff_envelope["domain_payload"])
        self.assertEqual(direct_envelope["stage_snapshot"], handoff_envelope["stage_snapshot"])

        self.assertEqual(
            direct_envelope["workspace_locator"],
            {
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
            },
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["session_handle_kind"],
            "grant_run_id",
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["grant_run_id"],
            "grant-run-nsfc-demo-001-baseline-001",
        )
        self.assertEqual(direct_envelope["runtime_session_contract"]["start_entry"], "runtime-run")
        self.assertEqual(direct_envelope["runtime_session_contract"]["resume_entry"], "runtime-resume")
        self.assertEqual(
            direct_envelope["return_surface_contract"]["entry_adapter"],
            "MedAutoGrantDomainEntry",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["domain_entry_contract"],
            {
                "entry_adapter": "MedAutoGrantDomainEntry",
                "service_safe_surface_kind": "service-safe-domain-entry-command",
                "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                "product_entry_kind": "med_auto_grant_product_entry",
                "supported_entry_modes": [
                    "direct",
                    "opl-handoff",
                ],
                "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
                "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
            },
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["checkpoint_aggregation_surface"],
            "stage-route-report",
        )
        self.assertEqual(
            direct_envelope["domain_payload"],
            {
                "workspace_id": "nsfc-demo-001",
                "draft_id": "draft-v1",
                "funding_call": "nsfc-2026-general",
            },
        )
        self.assertEqual(
            direct_envelope["stage_snapshot"],
            {
                "lifecycle_stage": "critique",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "revision",
            },
        )
        self.assertEqual(
            direct_envelope["executor_routing_contract"],
            {
                "contract_version": 1,
                "current_stage_route": _expected_route("critique", source_stage="critique"),
                "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                "author_side_route_catalog": [
                    _expected_route(route_id, source_stage=route_id)
                    for route_id in AUTHOR_SIDE_ROUTE_IDS
                ],
            },
        )

    def test_product_entry_surfaces_revision_completed_reroute_to_critique_handoff(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build(
            input_path=str(REVISION_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )

        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(
            payload["product_entry"]["stage_snapshot"],
            {
                "lifecycle_stage": "revision",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "critique",
            },
        )
        self.assertEqual(
            payload["product_entry"]["executor_routing_contract"],
            {
                "contract_version": 1,
                "current_stage_route": _expected_route("revision", source_stage="revision"),
                "recommended_executor_route": _expected_route("critique", source_stage="revision"),
                "author_side_route_catalog": [
                    _expected_route(route_id, source_stage=route_id)
                    for route_id in AUTHOR_SIDE_ROUTE_IDS
                ],
            },
        )

    def test_product_entry_contextualizes_drafting_and_frozen_pending_handoff_matrix(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        drafting_payload = MedAutoGrantProductEntry().build(
            input_path=str(DRAFTING_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        drafting_contract = drafting_payload["product_entry"]["executor_routing_contract"]
        self.assertEqual(
            drafting_contract["current_stage_route"],
            _expected_route("drafting", source_stage="drafting"),
        )
        self.assertEqual(
            drafting_contract["recommended_executor_route"],
            _expected_route("critique", source_stage="drafting"),
        )
        self.assertNotIn("handoff_requirements", drafting_contract["recommended_executor_route"])
        self.assertEqual(
            [
                route["route_id"]
                for route in drafting_contract["author_side_route_catalog"]
            ],
            list(AUTHOR_SIDE_ROUTE_IDS),
        )

        frozen_payload = MedAutoGrantProductEntry().build(
            input_path=str(FROZEN_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        self.assertEqual(
            frozen_payload["product_entry"]["executor_routing_contract"]["current_stage_route"],
            _expected_route("frozen", source_stage="frozen"),
        )

    def test_product_entry_fails_closed_on_blank_task_intent(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with self.assertRaisesRegex(WorkspaceStateError, "task_intent"):
            MedAutoGrantProductEntry().build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="   ",
            )

    def test_product_entry_rejects_missing_workspace_identity_from_stage_snapshot(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        domain_entry = Mock()
        domain_entry.dispatch.side_effect = [
            {
                "ok": True,
                "grant_run_id": "grant-run-test",
                "workspace_id": None,
                "lifecycle_stage": "critique",
                "verification_checkpoint": {
                    "checkpoint_status": "forward_progress",
                    "identity": {
                        "draft_id": "draft-test",
                    },
                },
                "route": {
                    "next_step": {
                        "recommended_stage": "revision",
                    }
                },
            },
            {
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "intake_snapshot": {
                    "funding_program": "nsfc-2026-general",
                },
            },
        ]

        with self.assertRaisesRegex(WorkspaceStateError, "workspace_id"):
            MedAutoGrantProductEntry(domain_entry=domain_entry).build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="tighten-grant-mainline",
            )

    def test_product_entry_fails_closed_on_invalid_executor_routing_contract_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry._build_executor_routing_contract",
            return_value={
                "contract_version": 1,
                "current_stage_route": {
                    "route_id": "critique",
                    "route_status": "pending",
                },
            },
            ):
                with self.assertRaises(WorkspaceStateError):
                    MedAutoGrantProductEntry().build(
                        input_path=str(CRITIQUE_EXAMPLE_PATH),
                        entry_mode="direct",
                        task_intent="tighten-grant-mainline",
                    )

    def test_grant_progress_projects_critique_stage_for_direct_entry(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_progress(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertEqual(payload["command"], "grant-progress")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["input_path"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
        self.assertEqual(
            payload["progress_projection"],
            {
                "projection_version": 1,
                "projection_kind": "grant_progress",
                "workspace_surface_kind": "nsfc_workspace",
                "current_stage": "critique",
                "current_stage_summary": "当前 grant 已进入 critique 阶段；导师批注 verdict=major_revision，应先执行结构化修订。",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "revision",
                "current_blockers": [
                    "必要性表述仍略偏现象描述。",
                ],
                "next_system_action": "执行 revision plan 中的 P0/P1 项。",
                "needs_author_decision": False,
                "author_decision_summary": None,
                "status_narration_contract": {
                    "schema_version": 1,
                    "contract_kind": "ai_status_narration",
                    "contract_id": "grant-progress::nsfc-demo-001",
                    "surface_kind": "grant_progress",
                    "audience": "human_user",
                    "milestone": {},
                    "stage": {
                        "current_stage": "critique",
                        "recommended_next_stage": "revision",
                        "checkpoint_status": "forward_progress",
                    },
                    "readiness": {
                        "needs_author_decision": False,
                    },
                    "remaining_scope": {},
                    "current_blockers": [
                        "必要性表述仍略偏现象描述。",
                    ],
                    "latest_update": "当前 grant 已进入 critique 阶段；导师批注 verdict=major_revision，应先执行结构化修订。",
                    "next_step": "执行 revision plan 中的 P0/P1 项。",
                    "human_gate": {},
                    "facts": {
                        "workspace_id": "nsfc-demo-001",
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    },
                    "narration_policy": {
                        "mode": "ai_first",
                        "legacy_summary_role": "fallback_only",
                        "style": "plain_language",
                        "answer_checklist": ["current_stage", "current_blockers", "next_step"],
                    },
                },
                "focus": {
                    "applicant_name": "示例申请人",
                    "funding_program": "nsfc-2026-general",
                    "project_profile_label": "NSFC general medical grant profile",
                    "template_label": "NSFC general medical grant template",
                    "critique_policy_id": "nsfc_mentor_critique_v1",
                    "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                    "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                    "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                    "critique_verdict": "major_revision",
                },
                "product_entry_surface": {
                    "builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                    "target_domain_id": "med-autogrant",
                    "supported_entry_modes": ["direct", "opl-handoff"],
                    "task_intent_required": True,
                    "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                },
            },
        )

    def test_grant_progress_projects_frozen_stage_without_blockers(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_progress(
            input_path=str(FROZEN_EXAMPLE_PATH),
        )

        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertEqual(
            payload["progress_projection"],
            {
                "projection_version": 1,
                "projection_kind": "grant_progress",
                "workspace_surface_kind": "nsfc_workspace",
                "current_stage": "frozen",
                "current_stage_summary": "当前 grant 已进入 frozen 阶段；送审前冻结 gate 已闭合，可保持当前阶段继续推进。",
                "checkpoint_status": "submission_frozen",
                "recommended_next_stage": "frozen",
                "current_blockers": [],
                "next_system_action": "沿当前阶段继续执行主线任务。",
                "needs_author_decision": False,
                "author_decision_summary": None,
                "status_narration_contract": {
                    "schema_version": 1,
                    "contract_kind": "ai_status_narration",
                    "contract_id": "grant-progress::nsfc-demo-001",
                    "surface_kind": "grant_progress",
                    "audience": "human_user",
                    "milestone": {},
                    "stage": {
                        "current_stage": "frozen",
                        "recommended_next_stage": "frozen",
                        "checkpoint_status": "submission_frozen",
                    },
                    "readiness": {
                        "needs_author_decision": False,
                    },
                    "remaining_scope": {},
                    "current_blockers": [],
                    "latest_update": "当前 grant 已进入 frozen 阶段；送审前冻结 gate 已闭合，可保持当前阶段继续推进。",
                    "next_step": "沿当前阶段继续执行主线任务。",
                    "human_gate": {},
                    "facts": {
                        "workspace_id": "nsfc-demo-001",
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    },
                    "narration_policy": {
                        "mode": "ai_first",
                        "legacy_summary_role": "fallback_only",
                        "style": "plain_language",
                        "answer_checklist": ["current_stage", "current_blockers", "next_step"],
                    },
                },
                "focus": {
                    "applicant_name": "示例申请人",
                    "funding_program": "nsfc-2026-general",
                    "project_profile_label": "NSFC general medical grant profile",
                    "template_label": "NSFC general medical grant template",
                    "critique_policy_id": "nsfc_mentor_critique_v1",
                    "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                    "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                    "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                    "critique_verdict": "ready_for_submission",
                },
                "product_entry_surface": {
                    "builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                    "target_domain_id": "med-autogrant",
                    "supported_entry_modes": ["direct", "opl-handoff"],
                    "task_intent_required": True,
                    "workspace_path": str(FROZEN_EXAMPLE_PATH.resolve()),
                },
            },
        )

    def test_grant_cockpit_packages_progress_alerts_and_entry_commands(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_cockpit(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertEqual(payload["command"], "grant-cockpit")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
        self.assertEqual(
            payload["grant_cockpit"]["workspace_overview"],
            {
                "applicant_name": "示例申请人",
                "funding_program": "nsfc-2026-general",
                "project_profile_label": "NSFC general medical grant profile",
                "template_label": "NSFC general medical grant template",
                "critique_policy_id": "nsfc_mentor_critique_v1",
                "lifecycle_stage": "critique",
                "checkpoint_status": "forward_progress",
                "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                "critique_verdict": "major_revision",
            },
        )
        self.assertEqual(payload["grant_cockpit"]["workspace_status"], "attention_required")
        self.assertEqual(
            payload["grant_cockpit"]["workspace_alerts"],
            [
                "必要性表述仍略偏现象描述。",
            ],
        )
        self.assertEqual(
            payload["grant_cockpit"]["progress_projection"]["projection_kind"],
            "grant_progress",
        )
        self.assertEqual(
            payload["grant_cockpit"]["commands"],
            {
                "grant_progress": public_cli_command(
                    "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "grant_intake_audit": public_cli_command(
                    "grant-intake-audit", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "grant_evidence_grounding": public_cli_command(
                    "grant-evidence-grounding", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "summarize_workspace": public_cli_command(
                    "summarize-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "stage_route_report": public_cli_command(
                    "stage-route-report", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "critique_summary": public_cli_command(
                    "critique-summary", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "build_direct_entry": public_cli_command(
                    "build-product-entry",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--entry-mode",
                    "direct",
                    "--task-intent",
                    "<describe-task-intent>",
                    "--format",
                    "json",
                ),
                "build_opl_handoff": public_cli_command(
                    "build-product-entry",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--entry-mode",
                    "opl-handoff",
                    "--task-intent",
                    "<describe-task-intent>",
                    "--format",
                    "json",
                ),
                "build_submission_ready_package": public_cli_command(
                    "build-submission-ready-package",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--output-dir",
                    "<submission-ready-output-dir>",
                    "--format",
                    "json",
                ),
            },
        )

    def test_grant_direct_entry_composes_projection_and_entry_envelopes(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_direct_entry(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )

        self.assertEqual(payload["command"], "grant-direct-entry")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
        self.assertEqual(
            payload["grant_direct_entry"],
            {
                "entry_version": 1,
                "entry_kind": "grant_direct_entry",
                "target_domain_id": "med-autogrant",
                "workspace_surface_kind": "nsfc_workspace",
                "task_intent": "tighten-grant-mainline",
                "workspace_overview": {
                    "applicant_name": "示例申请人",
                    "funding_program": "nsfc-2026-general",
                    "project_profile_label": "NSFC general medical grant profile",
                    "template_label": "NSFC general medical grant template",
                    "critique_policy_id": "nsfc_mentor_critique_v1",
                    "lifecycle_stage": "critique",
                    "checkpoint_status": "forward_progress",
                    "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                    "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                    "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                    "critique_verdict": "major_revision",
                },
                "workspace_status": "attention_required",
                "workspace_alerts": [
                    "必要性表述仍略偏现象描述。",
                ],
                "progress_projection": {
                    "projection_version": 1,
                    "projection_kind": "grant_progress",
                    "workspace_surface_kind": "nsfc_workspace",
                    "current_stage": "critique",
                    "current_stage_summary": "当前 grant 已进入 critique 阶段；导师批注 verdict=major_revision，应先执行结构化修订。",
                    "checkpoint_status": "forward_progress",
                    "recommended_next_stage": "revision",
                    "current_blockers": [
                        "必要性表述仍略偏现象描述。",
                    ],
                    "next_system_action": "执行 revision plan 中的 P0/P1 项。",
                    "needs_author_decision": False,
                    "author_decision_summary": None,
                    "status_narration_contract": {
                        "schema_version": 1,
                        "contract_kind": "ai_status_narration",
                        "contract_id": "grant-progress::nsfc-demo-001",
                        "surface_kind": "grant_progress",
                        "audience": "human_user",
                        "milestone": {},
                        "stage": {
                            "current_stage": "critique",
                            "recommended_next_stage": "revision",
                            "checkpoint_status": "forward_progress",
                        },
                        "readiness": {
                            "needs_author_decision": False,
                        },
                        "remaining_scope": {},
                        "current_blockers": [
                            "必要性表述仍略偏现象描述。",
                        ],
                        "latest_update": "当前 grant 已进入 critique 阶段；导师批注 verdict=major_revision，应先执行结构化修订。",
                        "next_step": "执行 revision plan 中的 P0/P1 项。",
                        "human_gate": {},
                        "facts": {
                            "workspace_id": "nsfc-demo-001",
                            "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        },
                        "narration_policy": {
                            "mode": "ai_first",
                            "legacy_summary_role": "fallback_only",
                            "style": "plain_language",
                            "answer_checklist": ["current_stage", "current_blockers", "next_step"],
                        },
                    },
                    "focus": {
                        "applicant_name": "示例申请人",
                        "funding_program": "nsfc-2026-general",
                        "project_profile_label": "NSFC general medical grant profile",
                        "template_label": "NSFC general medical grant template",
                        "critique_policy_id": "nsfc_mentor_critique_v1",
                        "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                        "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                        "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                        "critique_verdict": "major_revision",
                    },
                    "product_entry_surface": {
                        "builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                        "target_domain_id": "med-autogrant",
                        "supported_entry_modes": ["direct", "opl-handoff"],
                        "task_intent_required": True,
                        "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    },
                },
                "current_stage_route": _expected_route("critique", source_stage="critique"),
                "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                "direct_entry": {
                    "entry_version": 1,
                    "entry_kind": "med_auto_grant_product_entry",
                    "target_domain_id": "med-autogrant",
                    "task_intent": "tighten-grant-mainline",
                    "entry_mode": "direct",
                    "workspace_locator": {
                        "workspace_surface_kind": "nsfc_workspace",
                        "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    },
                    "runtime_session_contract": {
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        "session_handle_kind": "grant_run_id",
                        "start_entry": "runtime-run",
                        "resume_entry": "runtime-resume",
                        "runtime_substrate_contract": {
                            "runtime_owner": "Hermes",
                            "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                            "active_phase": "P4 mature direct grant product entry",
                            "active_tranche": "P4.F local submission-ready package landing",
                            "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                            "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                        },
                        "runtime_state_contract": {
                            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                            "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
                            "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                            "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                            "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                            "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                            "non_repo_tracked": True,
                        },
                    },
                    "return_surface_contract": {
                        "entry_adapter": "MedAutoGrantDomainEntry",
                        "default_formal_entry": "CLI",
                        "supported_entry_modes": ["direct", "opl-handoff"],
                        "domain_entry_contract": {
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "service_safe_surface_kind": "service-safe-domain-entry-command",
                            "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                            "product_entry_kind": "med_auto_grant_product_entry",
                            "supported_entry_modes": ["direct", "opl-handoff"],
                            "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
                            "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
                        },
                        "checkpoint_aggregation_surface": "stage-route-report",
                        "operator_contract": {
                            "canonical_audit_surfaces": [
                                "validate-workspace",
                                "summarize-workspace",
                                "grant-intake-audit",
                                "grant-evidence-grounding",
                                "next-step",
                                "critique-summary",
                                "stage-route-report",
                            ],
                            "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
                            "checkpoint_aggregation_surface": "stage-route-report",
                        },
                    },
                    "domain_payload": {
                        "workspace_id": "nsfc-demo-001",
                        "draft_id": "draft-v1",
                        "funding_call": "nsfc-2026-general",
                    },
                    "stage_snapshot": {
                        "lifecycle_stage": "critique",
                        "checkpoint_status": "forward_progress",
                        "recommended_next_stage": "revision",
                    },
                    "executor_routing_contract": {
                        "contract_version": 1,
                        "current_stage_route": _expected_route("critique", source_stage="critique"),
                        "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                        "author_side_route_catalog": [
                            _expected_route(route_id, source_stage=route_id)
                            for route_id in AUTHOR_SIDE_ROUTE_IDS
                        ],
                    },
                },
                "opl_handoff_entry": {
                    "entry_version": 1,
                    "entry_kind": "med_auto_grant_product_entry",
                    "target_domain_id": "med-autogrant",
                    "task_intent": "tighten-grant-mainline",
                    "entry_mode": "opl-handoff",
                    "workspace_locator": {
                        "workspace_surface_kind": "nsfc_workspace",
                        "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    },
                    "runtime_session_contract": {
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        "session_handle_kind": "grant_run_id",
                        "start_entry": "runtime-run",
                        "resume_entry": "runtime-resume",
                        "runtime_substrate_contract": {
                            "runtime_owner": "Hermes",
                            "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                            "active_phase": "P4 mature direct grant product entry",
                            "active_tranche": "P4.F local submission-ready package landing",
                            "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                            "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                        },
                        "runtime_state_contract": {
                            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                            "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
                            "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                            "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                            "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                            "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                            "non_repo_tracked": True,
                        },
                    },
                    "return_surface_contract": {
                        "entry_adapter": "MedAutoGrantDomainEntry",
                        "default_formal_entry": "CLI",
                        "supported_entry_modes": ["direct", "opl-handoff"],
                        "domain_entry_contract": {
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "service_safe_surface_kind": "service-safe-domain-entry-command",
                            "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                            "product_entry_kind": "med_auto_grant_product_entry",
                            "supported_entry_modes": ["direct", "opl-handoff"],
                            "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
                            "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
                        },
                        "checkpoint_aggregation_surface": "stage-route-report",
                        "operator_contract": {
                            "canonical_audit_surfaces": [
                                "validate-workspace",
                                "summarize-workspace",
                                "grant-intake-audit",
                                "grant-evidence-grounding",
                                "next-step",
                                "critique-summary",
                                "stage-route-report",
                            ],
                            "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
                            "checkpoint_aggregation_surface": "stage-route-report",
                        },
                    },
                    "domain_payload": {
                        "workspace_id": "nsfc-demo-001",
                        "draft_id": "draft-v1",
                        "funding_call": "nsfc-2026-general",
                    },
                    "stage_snapshot": {
                        "lifecycle_stage": "critique",
                        "checkpoint_status": "forward_progress",
                        "recommended_next_stage": "revision",
                    },
                    "executor_routing_contract": {
                        "contract_version": 1,
                        "current_stage_route": _expected_route("critique", source_stage="critique"),
                        "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                        "author_side_route_catalog": [
                            _expected_route(route_id, source_stage=route_id)
                            for route_id in AUTHOR_SIDE_ROUTE_IDS
                        ],
                    },
                },
            },
        )

    def test_grant_direct_entry_fails_closed_on_mismatched_entry_mode(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry.MedAutoGrantProductEntry.build",
            side_effect=[
                {
                    "ok": True,
                    "command": "build-product-entry",
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "lifecycle_stage": "critique",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "output_path": None,
                    "product_entry": {
                        "entry_version": 1,
                        "entry_kind": "med_auto_grant_product_entry",
                        "target_domain_id": "med-autogrant",
                        "task_intent": "tighten-grant-mainline",
                        "entry_mode": "opl-handoff",
                        "workspace_locator": {
                            "workspace_surface_kind": "nsfc_workspace",
                            "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                        },
                        "runtime_session_contract": {
                            "grant_run_id": "grant-run-test",
                            "session_handle_kind": "grant_run_id",
                            "start_entry": "runtime-run",
                            "resume_entry": "runtime-resume",
                            "runtime_substrate_contract": {
                                "runtime_owner": "Hermes",
                                "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                                "active_phase": "P4 mature direct grant product entry",
                                "active_tranche": "P4.F local submission-ready package landing",
                                "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                                "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                            },
                            "runtime_state_contract": {
                                "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                                "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
                                "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                                "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                                "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                                "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                                "non_repo_tracked": True,
                            },
                        },
                        "return_surface_contract": {
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "default_formal_entry": "CLI",
                            "supported_entry_modes": ["direct", "opl-handoff"],
                            "domain_entry_contract": {
                                "entry_adapter": "MedAutoGrantDomainEntry",
                                "service_safe_surface_kind": "service-safe-domain-entry-command",
                                "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                                "product_entry_kind": "med_auto_grant_product_entry",
                                "supported_entry_modes": ["direct", "opl-handoff"],
                                "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
                                "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
                            },
                            "checkpoint_aggregation_surface": "stage-route-report",
                            "operator_contract": {
                                "canonical_audit_surfaces": [
                                    "validate-workspace",
                                    "summarize-workspace",
                                    "grant-intake-audit",
                                    "grant-evidence-grounding",
                                    "next-step",
                                    "critique-summary",
                                    "stage-route-report",
                                ],
                            "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
                            "checkpoint_aggregation_surface": "stage-route-report",
                        },
                    },
                        "domain_payload": {
                            "workspace_id": "workspace-test",
                            "draft_id": "draft-test",
                            "funding_call": "nsfc-2026-general",
                        },
                        "stage_snapshot": {
                            "lifecycle_stage": "critique",
                            "checkpoint_status": "forward_progress",
                            "recommended_next_stage": "revision",
                        },
                        "executor_routing_contract": {
                            "contract_version": 1,
                            "current_stage_route": _expected_route("critique", source_stage="critique"),
                            "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                            "author_side_route_catalog": [
                                _expected_route(route_id, source_stage=route_id)
                                for route_id in AUTHOR_SIDE_ROUTE_IDS
                            ],
                        },
                    },
                },
                {
                    "ok": True,
                    "command": "build-product-entry",
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "lifecycle_stage": "critique",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "output_path": None,
                    "product_entry": {
                        "entry_version": 1,
                        "entry_kind": "med_auto_grant_product_entry",
                        "target_domain_id": "med-autogrant",
                        "task_intent": "tighten-grant-mainline",
                        "entry_mode": "opl-handoff",
                        "workspace_locator": {
                            "workspace_surface_kind": "nsfc_workspace",
                            "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                        },
                        "runtime_session_contract": {
                            "grant_run_id": "grant-run-test",
                            "session_handle_kind": "grant_run_id",
                            "start_entry": "runtime-run",
                            "resume_entry": "runtime-resume",
                            "runtime_substrate_contract": {
                                "runtime_owner": "Hermes",
                                "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                                "active_phase": "P4 mature direct grant product entry",
                                "active_tranche": "P4.F local submission-ready package landing",
                                "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                                "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                            },
                            "runtime_state_contract": {
                                "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                                "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
                                "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                                "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                                "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                                "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                                "non_repo_tracked": True,
                            },
                        },
                        "return_surface_contract": {
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "default_formal_entry": "CLI",
                            "supported_entry_modes": ["direct", "opl-handoff"],
                            "domain_entry_contract": {
                                "entry_adapter": "MedAutoGrantDomainEntry",
                                "service_safe_surface_kind": "service-safe-domain-entry-command",
                                "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                                "product_entry_kind": "med_auto_grant_product_entry",
                                "supported_entry_modes": ["direct", "opl-handoff"],
                                "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
                                "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
                            },
                            "checkpoint_aggregation_surface": "stage-route-report",
                            "operator_contract": {
                                "canonical_audit_surfaces": [
                                    "validate-workspace",
                                    "summarize-workspace",
                                    "grant-intake-audit",
                                    "grant-evidence-grounding",
                                    "next-step",
                                    "critique-summary",
                                    "stage-route-report",
                                ],
                                "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
                                "checkpoint_aggregation_surface": "stage-route-report",
                            },
                        },
                        "domain_payload": {
                            "workspace_id": "workspace-test",
                            "draft_id": "draft-test",
                            "funding_call": "nsfc-2026-general",
                        },
                        "stage_snapshot": {
                            "lifecycle_stage": "critique",
                            "checkpoint_status": "forward_progress",
                            "recommended_next_stage": "revision",
                        },
                        "executor_routing_contract": {
                            "contract_version": 1,
                            "current_stage_route": _expected_route("critique", source_stage="critique"),
                            "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                            "author_side_route_catalog": [
                                _expected_route(route_id, source_stage=route_id)
                                for route_id in AUTHOR_SIDE_ROUTE_IDS
                            ],
                        },
                    },
                },
            ],
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_direct_entry.direct_entry"):
                MedAutoGrantProductEntry().build_grant_direct_entry(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                    task_intent="tighten-grant-mainline",
                )

    def test_grant_user_loop_packages_mainline_snapshot_and_landed_next_action(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["grant_user_loop"]["entry_kind"], "grant_user_loop")
        self.assertEqual(
            payload["grant_user_loop"]["mainline_snapshot"]["active_tranche"],
            "P4.F local submission-ready package landing",
        )
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "revision",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["route_id"],
            "revision",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["command"],
            public_cli_command(
                "execute-revision-pass",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id="draft-v1",
                        file_name="revision-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertIsNone(payload["grant_user_loop"]["next_action"]["handoff_surfaces"])
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["mainline_status"],
            public_cli_command("mainline-status", "--format", "json"),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["phase_status_current"],
            public_cli_command("mainline-phase", "--phase", "current", "--format", "json"),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_cockpit"],
            public_cli_command(
                "grant-cockpit", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
            public_cli_command(
                "grant-direct-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            ),
        )

    def test_product_preflight_uses_shared_program_companion_builder(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        captured: dict[str, object] = {}

        def _fake_build_product_entry_preflight(**kwargs: object) -> dict[str, object]:
            captured.update(kwargs)
            return {
                "surface_kind": "product_entry_preflight",
                "summary": "[shared-builder] preflight",
                "ready_to_try_now": True,
                "recommended_check_command": str(kwargs["recommended_check_command"]),
                "recommended_start_command": str(kwargs["recommended_start_command"]),
                "blocking_check_ids": [],
                "checks": list(kwargs["checks"]),  # type: ignore[arg-type]
            }

        with patch(
            "med_autogrant.product_entry._build_shared_product_entry_preflight",
            side_effect=_fake_build_product_entry_preflight,
        ) as preflight_builder:
            payload = MedAutoGrantProductEntry().build_product_entry_preflight(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )

        preflight_builder.assert_called_once()
        self.assertEqual(payload["product_entry_preflight"]["summary"], "[shared-builder] preflight")
        self.assertEqual(
            [check["check_id"] for check in captured["checks"]],  # type: ignore[index]
            [
                "workspace_document_valid",
                "upstream_hermes_owner_line",
                "direct_frontdoor_contract_landed",
                "submission_ready_export_gate",
            ],
        )
        self.assertEqual(
            captured["recommended_check_command"],
            public_cli_command(
                "validate-workspace",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--format",
                "json",
            ),
        )

    def test_grant_authoring_readiness_uses_shared_detailed_builders(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        workflow_calls: list[dict[str, object]] = []

        def _fake_build_workflow_coverage_item(**kwargs: object) -> dict[str, str]:
            payload = {key: str(value) for key, value in kwargs.items()}
            payload["remaining_gap"] = f"[shared-item] {payload['remaining_gap']}"
            workflow_calls.append(dict(kwargs))
            return payload

        def _fake_build_detailed_readiness(**kwargs: object) -> dict[str, object]:
            payload = dict(kwargs)
            payload["summary"] = f"{payload['summary']} [shared-detailed-readiness]"
            return payload

        with patch(
            "med_autogrant.product_entry._build_shared_workflow_coverage_item",
            side_effect=_fake_build_workflow_coverage_item,
        ) as workflow_builder, patch(
            "med_autogrant.product_entry._build_shared_detailed_readiness",
            side_effect=_fake_build_detailed_readiness,
        ) as readiness_builder:
            manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )["product_entry_manifest"]

        workflow_builder.assert_called()
        readiness_builder.assert_called_once()
        self.assertEqual(len(workflow_calls), 9)
        self.assertEqual(workflow_calls[0]["step_id"], "accumulation_direction_screening")
        readiness = manifest["grant_authoring_readiness"]
        self.assertTrue(readiness["summary"].endswith("[shared-detailed-readiness]"))
        self.assertTrue(
            readiness["workflow_coverage"][0]["remaining_gap"].startswith("[shared-item] ")
        )

    def test_product_entry_manifest_projects_current_grant_shell_and_shared_handoff(self) -> None:
        from med_autogrant.domain_entry_contract import (
            build_domain_entry_contract,
            build_gateway_interaction_contract,
        )
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertEqual(payload["command"], "product-entry-manifest")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        manifest = payload["product_entry_manifest"]
        self.assertEqual(manifest["surface_kind"], "product_entry_manifest")
        self.assertEqual(manifest["manifest_version"], 2)
        self.assertEqual(manifest["manifest_kind"], "med_auto_grant_product_entry_manifest")
        self.assertEqual(manifest["target_domain_id"], "med-autogrant")
        self.assertEqual(manifest["formal_entry"]["default"], "CLI")
        self.assertEqual(manifest["formal_entry"]["supported_protocols"], ["MCP"])
        self.assertEqual(manifest["workspace_locator"]["workspace_root"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(manifest["workspace_locator"]["workspace_path"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(manifest["recommended_shell"], "grant_user_loop")
        self.assertEqual(
            manifest["recommended_command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(manifest["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(
            manifest["frontdesk_surface"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(manifest["frontdesk_surface"]["surface_kind"], "product_frontdesk")
        self.assertIn("direct grant product frontdesk", manifest["frontdesk_surface"]["summary"])
        self.assertEqual(
            manifest["managed_runtime_contract"],
            {
                "shared_contract_ref": "contracts/opl-gateway/managed-runtime-three-layer-contract.json",
                "runtime_owner": "upstream_hermes_agent",
                "domain_owner": "med-autogrant",
                "executor_owner": "med-autogrant",
                "supervision_status_surface": {
                    "surface_kind": "grant_progress",
                    "owner": "med-autogrant",
                },
                "attention_queue_surface": {
                    "surface_kind": "grant_user_loop",
                    "owner": "med-autogrant",
                },
                "recovery_contract_surface": {
                    "surface_kind": "grant_user_loop",
                    "owner": "med-autogrant",
                },
                "fail_closed_rules": [
                    "domain_supervision_cannot_bypass_runtime",
                    "executor_cannot_declare_global_gate_clear",
                    "runtime_cannot_invent_domain_publishability_truth",
                ],
            },
        )
        self.assertEqual(manifest["runtime_inventory"]["surface_kind"], "runtime_inventory")
        self.assertEqual(manifest["runtime_inventory"]["runtime_owner"], "upstream_hermes_agent")
        self.assertEqual(
            manifest["runtime_inventory"]["domain_owner"],
            manifest["managed_runtime_contract"]["domain_owner"],
        )
        self.assertEqual(manifest["task_lifecycle"]["surface_kind"], "task_lifecycle")
        self.assertEqual(
            manifest["task_lifecycle"]["status"],
            "forward_progress",
        )
        self.assertEqual(
            manifest["task_lifecycle"]["progress_surface"]["surface_kind"],
            "grant_progress",
        )
        self.assertEqual(manifest["skill_catalog"]["surface_kind"], "skill_catalog")
        self.assertIn("validate-workspace", manifest["skill_catalog"]["supported_commands"])
        self.assertTrue(manifest["skill_catalog"]["command_contracts"])
        self.assertEqual(manifest["domain_entry_contract"], build_domain_entry_contract())
        self.assertEqual(
            manifest["gateway_interaction_contract"],
            build_gateway_interaction_contract(),
        )
        self.assertEqual(manifest["automation"]["surface_kind"], "automation")
        self.assertEqual(
            [item["automation_id"] for item in manifest["automation"]["automations"]],
            ["mag.submission_ready_export", "mag.authoring_loop_continuation"],
        )
        self.assertEqual(manifest["operator_loop_surface"]["shell_key"], "grant_user_loop")
        self.assertEqual(manifest["operator_loop_surface"]["command"], manifest["recommended_command"])
        self.assertEqual(manifest["operator_loop_surface"]["surface_kind"], "grant_user_loop")
        self.assertIn("direct grant user inbox shell", manifest["operator_loop_surface"]["summary"])
        self.assertEqual(manifest["operator_loop_actions"]["open_loop"]["command"], manifest["recommended_command"])
        self.assertEqual(manifest["operator_loop_actions"]["open_loop"]["surface_kind"], "grant_user_loop")
        self.assertEqual(manifest["operator_loop_actions"]["inspect_progress"]["requires"], [])
        self.assertEqual(manifest["operator_loop_actions"]["build_direct_entry"]["requires"], ["task_intent"])
        self.assertEqual(manifest["repo_mainline"]["active_phase"], "P4 mature direct grant product entry")
        self.assertEqual(
            manifest["repo_mainline"]["active_tranche"],
            "P4.F local submission-ready package landing",
        )
        self.assertEqual(manifest["repo_mainline"]["phase_id"], "P4")
        self.assertEqual(
            manifest["repo_mainline"]["phase_summary"],
            "把 direct grant product 面逐步收成当前用户 inbox shell，而不越界写成 mature Web UI 或 hosted runtime。",
        )
        self.assertEqual(
            manifest["repo_mainline"]["next_focus"],
            [
                "继续把 `product-entry-manifest` / `product-frontdesk` 当作当前 direct grant frontdoor contract，并让 `grant-progress`、`grant-cockpit`、`grant-direct-entry` 与 `grant-user-loop` 继续对齐同一份 frontdoor truth。",
                "继续把 `family_orchestration` companion 从 action graph / human gate preview 深压到 family product-entry manifest v2、event envelope 与 checkpoint lineage contract，并保持 route status 直接读取共享 author-side route truth。",
            ],
        )
        self.assertEqual(
            manifest["product_entry_status"]["summary"],
            "把 direct grant product 面逐步收成当前用户 inbox shell，而不越界写成 mature Web UI 或 hosted runtime。",
        )
        self.assertEqual(
            manifest["product_entry_status"]["remaining_gaps_count"],
            len(manifest["remaining_gaps"]),
        )
        self.assertEqual(
            manifest["product_entry_status"]["next_focus"],
            manifest["repo_mainline"]["next_focus"],
        )
        self.assertEqual(
            manifest["product_entry_shell"]["grant_progress"]["command"],
            public_cli_command(
                "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["product_entry_shell"]["grant_user_loop"]["command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            manifest["product_entry_shell"]["product_frontdesk"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["shared_handoff"]["direct_entry_builder"]["command"],
            public_cli_command(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--entry-mode",
                "direct",
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            manifest["shared_handoff"]["opl_handoff_builder"]["command"],
            public_cli_command(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--entry-mode",
                "opl-handoff",
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        _assert_family_orchestration_companion(
            self,
            manifest.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        self.assertEqual(
            manifest["family_orchestration"]["human_gates"][0]["gate_id"],
            "mag_route_gate_revision",
        )
        self.assertEqual(
            manifest["family_orchestration"]["event_envelope_surface"]["ref"],
            "/product_entry_manifest/recommended_command",
        )
        self.assertEqual(
            manifest["family_orchestration"]["checkpoint_lineage_surface"]["ref"],
            "/product_entry_manifest/repo_mainline/active_phase",
        )
        self.assertEqual(manifest["product_entry_quickstart"]["surface_kind"], "product_entry_quickstart")
        self.assertEqual(manifest["product_entry_quickstart"]["recommended_step_id"], "open_frontdesk")
        self.assertEqual(
            [step["step_id"] for step in manifest["product_entry_quickstart"]["steps"]],
            [
                "open_frontdesk",
                "continue_grant_loop",
                "inspect_progress",
                "inspect_cockpit",
                "build_submission_ready_package",
            ],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["steps"][0]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["steps"][1]["requires"],
            ["task_intent"],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["steps"][4]["requires"],
            ["output_dir"],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["resume_contract"],
            manifest["family_orchestration"]["resume_contract"],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["human_gate_ids"],
            ["mag_route_gate_revision"],
        )
        product_start = manifest["product_entry_start"]
        self.assertEqual(product_start["surface_kind"], "product_entry_start")
        self.assertEqual(product_start["recommended_mode_id"], "open_frontdesk")
        self.assertEqual(
            [mode["mode_id"] for mode in product_start["modes"]],
            ["open_frontdesk", "continue_grant_loop", "build_direct_entry"],
        )
        self.assertEqual(
            product_start["modes"][0]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(product_start["modes"][1]["requires"], ["task_intent"])
        self.assertEqual(product_start["modes"][2]["surface_kind"], "grant_direct_entry")
        self.assertEqual(
            product_start["resume_surface"],
            manifest["family_orchestration"]["resume_contract"],
        )
        self.assertEqual(product_start["human_gate_ids"], ["mag_route_gate_revision"])
        self.assertEqual(manifest["product_entry_overview"]["surface_kind"], "product_entry_overview")
        self.assertEqual(
            manifest["product_entry_overview"]["summary"],
            manifest["product_entry_status"]["summary"],
        )
        self.assertEqual(
            manifest["product_entry_overview"]["frontdesk_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["product_entry_overview"]["recommended_command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            manifest["product_entry_overview"]["progress_surface"],
            {
                "surface_kind": "grant_progress",
                "command": public_cli_command(
                    "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "step_id": "inspect_progress",
            },
        )
        self.assertEqual(
            manifest["product_entry_overview"]["resume_surface"],
            {
                "surface_kind": "grant_user_loop",
                "command": public_cli_command(
                    "grant-user-loop",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--task-intent",
                    "<describe-task-intent>",
                    "--format",
                    "json",
                ),
                "session_locator_field": "grant_run_id",
                "checkpoint_locator_field": "lifecycle_stage",
            },
        )
        self.assertEqual(manifest["product_entry_overview"]["recommended_step_id"], "open_frontdesk")
        self.assertEqual(
            manifest["product_entry_overview"]["next_focus"],
            manifest["product_entry_status"]["next_focus"],
        )
        self.assertEqual(
            manifest["product_entry_overview"]["remaining_gaps_count"],
            manifest["product_entry_status"]["remaining_gaps_count"],
        )
        self.assertEqual(
            manifest["product_entry_overview"]["human_gate_ids"],
            ["mag_route_gate_revision"],
        )
        preflight = manifest["product_entry_preflight"]
        self.assertEqual(preflight["surface_kind"], "product_entry_preflight")
        self.assertEqual(
            preflight["summary"],
            "当前 direct grant frontdoor 的前置检查已通过，可以先复核 workspace 与主线，再进入 product frontdesk。",
        )
        self.assertTrue(preflight["ready_to_try_now"])
        self.assertEqual(
            preflight["recommended_check_command"],
            public_cli_command(
                "validate-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            preflight["recommended_start_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(preflight["blocking_check_ids"], [])
        self.assertEqual(
            [check["check_id"] for check in preflight["checks"]],
            [
                "workspace_document_valid",
                "upstream_hermes_owner_line",
                "direct_frontdoor_contract_landed",
                "submission_ready_export_gate",
            ],
        )
        self.assertEqual(preflight["checks"][0]["status"], "pass")
        self.assertEqual(preflight["checks"][0]["blocking"], True)
        self.assertEqual(preflight["checks"][1]["status"], "pass")
        self.assertEqual(preflight["checks"][2]["status"], "pass")
        self.assertEqual(preflight["checks"][3]["status"], "warn")
        product_readiness = manifest["product_entry_readiness"]
        self.assertEqual(product_readiness["surface_kind"], "product_entry_readiness")
        self.assertEqual(product_readiness["verdict"], "agent_assisted_ready_not_product_grade")
        self.assertTrue(product_readiness["usable_now"])
        self.assertFalse(product_readiness["good_to_use_now"])
        self.assertFalse(product_readiness["fully_automatic"])
        self.assertEqual(product_readiness["recommended_start_surface"], "product_frontdesk")
        self.assertEqual(
            product_readiness["recommended_start_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(product_readiness["recommended_loop_surface"], "grant_user_loop")
        self.assertEqual(
            product_readiness["recommended_loop_command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertIn("还不是 mature direct grant Web UI / hosted runtime。", product_readiness["blocking_gaps"])
        readiness = manifest["grant_authoring_readiness"]
        self.assertEqual(readiness["surface_kind"], "grant_authoring_readiness")
        self.assertEqual(readiness["verdict"], "agent_assisted_cli_ready_not_full_autopilot")
        self.assertFalse(readiness["fully_automatic"])
        self.assertTrue(readiness["usable_now"])
        self.assertFalse(readiness["good_to_use_now"])
        self.assertEqual(readiness["recommended_start_surface"], "product_frontdesk")
        self.assertEqual(
            readiness["recommended_start_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(readiness["recommended_loop_surface"], "grant_user_loop")
        self.assertEqual(
            [item["step_id"] for item in readiness["workflow_coverage"]],
            [
                "accumulation_direction_screening",
                "hotspot_literature_fit",
                "clinical_question_refinement",
                "innovation_framework",
                "mainline_closure",
                "significance_background_drafting",
                "preliminary_evidence_and_basis",
                "expected_results_timeline",
                "final_review_figures_package",
            ],
        )
        self.assertEqual(readiness["workflow_coverage"][0]["coverage_status"], "landed_route")
        self.assertEqual(readiness["workflow_coverage"][1]["coverage_status"], "partially_supported")
        self.assertIn("还不是 mature direct grant Web UI / hosted runtime。", readiness["blocking_gaps"])

    def test_family_orchestration_companion_is_projected_across_product_surfaces(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        progress_payload = entry.read_grant_progress(input_path=str(CRITIQUE_EXAMPLE_PATH))
        cockpit_payload = entry.read_grant_cockpit(input_path=str(CRITIQUE_EXAMPLE_PATH))
        direct_entry_payload = entry.build_grant_direct_entry(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )
        user_loop_payload = entry.build_grant_user_loop(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )
        manifest_payload = entry.build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        _assert_family_orchestration_companion(
            self,
            progress_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            cockpit_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            direct_entry_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            user_loop_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            manifest_payload["product_entry_manifest"].get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )

    def test_family_orchestration_action_graph_uses_shared_product_entry_orchestration(self) -> None:
        from med_autogrant import product_entry as module

        captured: dict[str, object] = {}

        def _fake_build_family_product_entry_orchestration(**kwargs: object) -> dict[str, object]:
            captured.update(kwargs)
            return {
                "action_graph_ref": {
                    "ref_kind": "json_pointer",
                    "ref": "/family_orchestration/action_graph",
                    "label": "mag family action graph",
                },
                "action_graph": {
                    "graph_id": str(kwargs["graph_id"]),
                    "target_domain_id": str(kwargs["target_domain_id"]),
                    "graph_kind": str(kwargs["graph_kind"]),
                    "graph_version": str(kwargs["graph_version"]),
                    "nodes": list(kwargs["nodes"]),
                    "edges": list(kwargs["edges"]),
                    "entry_nodes": list(kwargs["entry_nodes"]),
                    "exit_nodes": list(kwargs["exit_nodes"]),
                    "human_gates": list(kwargs["human_gates"]),
                    "checkpoint_policy": {
                        "mode": "explicit_nodes",
                        "checkpoint_nodes": list(kwargs["checkpoint_nodes"]),
                    },
                },
                "human_gates": list(kwargs["human_gate_previews"]),
                "resume_contract": {
                    "surface_kind": str(kwargs["resume_surface_kind"]),
                    "session_locator_field": str(kwargs["session_locator_field"]),
                    "checkpoint_locator_field": str(kwargs["checkpoint_locator_field"]),
                },
            }

        with patch.object(
            module,
            "_build_shared_family_product_entry_orchestration",
            side_effect=_fake_build_family_product_entry_orchestration,
        ):
            payload = module._build_family_orchestration_companion(
                current_route_id="drafting",
                recommended_route_id="critique",
                recommended_route_status="pending",
                needs_author_decision=True,
                review_surface_ref="/review",
                event_envelope_surface_ref="/events",
                checkpoint_lineage_surface_ref="/lineage",
                resume_surface_kind="grant_user_loop",
            )

        self.assertEqual(payload["action_graph"]["graph_id"], "mag_drafting_to_critique_graph")
        self.assertEqual(captured["graph_kind"], "grant_route_orchestration")
        self.assertEqual([node["node_id"] for node in captured["nodes"]], ["route:drafting", "route:critique"])
        self.assertEqual([edge["on"] for edge in captured["edges"]], ["decision"])
        self.assertEqual(captured["entry_nodes"], ["route:drafting"])
        self.assertEqual(captured["exit_nodes"], ["route:critique"])
        self.assertEqual(captured["checkpoint_nodes"], ["route:drafting", "route:critique"])
        self.assertEqual(captured["human_gate_previews"][0]["gate_id"], "mag_route_gate_critique")

    def test_grant_user_loop_projects_landed_critique_route_when_drafting_can_execute_directly(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(DRAFTING_EXAMPLE_PATH),
            task_intent="prepare-critique-handoff",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "critique",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_id"], "critique")
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_status"], "landed")
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["command"],
            public_cli_command(
                "execute-critique-pass",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id="draft-v1",
                        file_name="critique-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["handoff_surfaces"],
            None,
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            public_cli_command(
                "execute-critique-pass",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id="draft-v1",
                        file_name="critique-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
            public_cli_command(
                "grant-direct-entry",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "prepare-critique-handoff",
                "--format",
                "json",
            ),
        )

    def test_grant_user_loop_projects_landed_question_refinement_route_when_direction_screening_can_execute_directly(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(DIRECTION_EXAMPLE_PATH),
            task_intent="advance-grant-mainline",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["lifecycle_stage"], "direction_screening")
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "question_refinement",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_id"], "question_refinement")
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_status"], "landed")
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["command"],
            public_cli_command(
                "execute-question-refinement-pass",
                "--input",
                str(DIRECTION_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id=None,
                        file_name="question-refinement-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            public_cli_command(
                "execute-question-refinement-pass",
                "--input",
                str(DIRECTION_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id=None,
                        file_name="question-refinement-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )

    def test_product_frontdesk_projects_frontdoor_over_current_grant_loop(self) -> None:
        from med_autogrant.domain_entry_contract import (
            build_domain_entry_contract,
            build_gateway_interaction_contract,
        )
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_frontdesk(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-frontdesk")
        frontdesk = payload["product_frontdesk"]
        self.assertEqual(frontdesk["surface_kind"], "product_frontdesk")
        self.assertEqual(frontdesk["recommended_action"], "inspect_or_prepare_grant_loop")
        self.assertEqual(frontdesk["target_domain_id"], "med-autogrant")
        self.assertEqual(frontdesk["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(
            frontdesk["frontdesk_surface"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(frontdesk["operator_loop_surface"]["shell_key"], "grant_user_loop")
        self.assertEqual(
            frontdesk["entry_surfaces"]["frontdesk"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            frontdesk["entry_surfaces"]["grant_user_loop"]["command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            frontdesk["entry_surfaces"]["direct_entry_builder"]["command"],
            public_cli_command(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--entry-mode",
                "direct",
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            frontdesk["summary"]["frontdesk_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            frontdesk["summary"]["operator_loop_command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        _assert_family_orchestration_companion(
            self,
            frontdesk.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        self.assertEqual(frontdesk["family_orchestration"]["human_gates"][0]["gate_id"], "mag_route_gate_revision")
        self.assertEqual(
            frontdesk["family_orchestration"]["event_envelope_surface"]["ref"],
            "/product_entry_manifest/recommended_command",
        )
        self.assertEqual(frontdesk["product_entry_overview"]["surface_kind"], "product_entry_overview")
        self.assertEqual(
            frontdesk["product_entry_overview"]["progress_surface"]["surface_kind"],
            "grant_progress",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["project_profile_label"],
            "NSFC general medical grant profile",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["critique_policy_id"],
            "nsfc_mentor_critique_v1",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["resume_surface"]["surface_kind"],
            "grant_user_loop",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["resume_surface"]["command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(frontdesk["product_entry_preflight"]["surface_kind"], "product_entry_preflight")
        self.assertTrue(frontdesk["product_entry_preflight"]["ready_to_try_now"])
        self.assertEqual(
            frontdesk["product_entry_preflight"]["recommended_check_command"],
            public_cli_command(
                "validate-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            frontdesk["product_entry_preflight"],
            frontdesk["product_entry_manifest"]["product_entry_preflight"],
        )
        self.assertEqual(frontdesk["product_entry_start"]["surface_kind"], "product_entry_start")
        self.assertEqual(frontdesk["product_entry_start"]["recommended_mode_id"], "open_frontdesk")
        self.assertEqual(frontdesk["product_entry_start"]["modes"][1]["mode_id"], "continue_grant_loop")
        self.assertEqual(frontdesk["product_entry_start"]["modes"][2]["mode_id"], "build_direct_entry")
        self.assertEqual(frontdesk["product_entry_start"]["resume_surface"]["surface_kind"], "grant_user_loop")
        self.assertEqual(
            frontdesk["product_entry_start"],
            frontdesk["product_entry_manifest"]["product_entry_start"],
        )
        self.assertEqual(frontdesk["product_entry_readiness"]["surface_kind"], "product_entry_readiness")
        self.assertTrue(frontdesk["product_entry_readiness"]["usable_now"])
        self.assertFalse(frontdesk["product_entry_readiness"]["good_to_use_now"])
        self.assertEqual(
            frontdesk["product_entry_readiness"],
            frontdesk["product_entry_manifest"]["product_entry_readiness"],
        )
        self.assertEqual(frontdesk["grant_authoring_readiness"]["surface_kind"], "grant_authoring_readiness")
        self.assertFalse(frontdesk["grant_authoring_readiness"]["fully_automatic"])
        self.assertTrue(frontdesk["grant_authoring_readiness"]["usable_now"])
        self.assertFalse(frontdesk["grant_authoring_readiness"]["good_to_use_now"])
        self.assertEqual(
            frontdesk["grant_authoring_readiness"],
            frontdesk["product_entry_manifest"]["grant_authoring_readiness"],
        )
        self.assertEqual(frontdesk["product_entry_quickstart"]["recommended_step_id"], "open_frontdesk")
        self.assertEqual(frontdesk["product_entry_quickstart"]["steps"][2]["step_id"], "inspect_progress")
        self.assertEqual(frontdesk["product_entry_quickstart"]["steps"][2]["surface_kind"], "grant_progress")
        self.assertEqual(frontdesk["product_entry_quickstart"]["steps"][4]["step_id"], "build_submission_ready_package")
        self.assertEqual(
            frontdesk["product_entry_quickstart"]["steps"][4]["surface_kind"],
            "submission_ready_package",
        )
        self.assertEqual(frontdesk["product_entry_manifest"]["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(frontdesk["product_entry_manifest"]["manifest_version"], 2)
        self.assertEqual(frontdesk["domain_entry_contract"], build_domain_entry_contract())
        self.assertEqual(
            frontdesk["gateway_interaction_contract"],
            build_gateway_interaction_contract(),
        )
        self.assertEqual(
            frontdesk["domain_entry_contract"],
            frontdesk["product_entry_manifest"]["domain_entry_contract"],
        )
        self.assertEqual(
            frontdesk["gateway_interaction_contract"],
            frontdesk["product_entry_manifest"]["gateway_interaction_contract"],
        )

    def test_product_entry_manifest_fails_closed_on_invalid_mainline_snapshot_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry._build_mainline_snapshot",
            return_value={
                "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                "active_phase": "P4 mature direct grant product entry",
                "active_tranche": "P4.F local submission-ready package landing",
                "phase_map": [{"phase_id": "P4", "phase_name": "mature direct grant product entry", "status": "next"}],
                "next_focus": [1],
                "remaining_gaps": ["mature direct grant Web UI / hosted runtime 仍未 landed。"],
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "product_entry_manifest"):
                MedAutoGrantProductEntry().build_product_entry_manifest(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_product_frontdesk_fails_closed_on_invalid_operator_loop_action_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        manifest_payload = deepcopy(
            entry.build_product_entry_manifest(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )
        )
        manifest_payload["product_entry_manifest"]["operator_loop_actions"]["open_loop"] = {
            "command": public_cli_command("grant-user-loop", "--format", "json"),
        }

        with patch.object(
            MedAutoGrantProductEntry,
            "build_product_entry_manifest",
            return_value=manifest_payload,
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "product_frontdesk"):
                MedAutoGrantProductEntry().build_product_frontdesk(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_grant_progress_family_orchestration_marks_landed_authoring_route_as_approved(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_progress(
            input_path=str(DIRECTION_EXAMPLE_PATH),
        )

        family_orchestration = payload["family_orchestration"]
        self.assertEqual(family_orchestration["human_gates"][0]["gate_id"], "mag_route_gate_question_refinement")
        self.assertEqual(family_orchestration["human_gates"][0]["status"], "approved")
        self.assertEqual(family_orchestration["action_graph"]["edges"][0]["on"], "success")

    def test_grant_progress_fails_closed_on_invalid_projection_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry._build_focus_payload",
            return_value={
                "applicant_name": "示例申请人",
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_progress"):
                MedAutoGrantProductEntry().read_grant_progress(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_grant_cockpit_fails_closed_on_invalid_command_catalog_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry._build_product_command_catalog",
            return_value={
                "grant_progress": public_cli_command("grant-progress", "--format", "json"),
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_cockpit"):
                MedAutoGrantProductEntry().read_grant_cockpit(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )


if __name__ == "__main__":
    unittest.main()
