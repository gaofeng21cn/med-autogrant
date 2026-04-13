from __future__ import annotations

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
SUPPORTED_DOMAIN_ENTRY_COMMANDS = [
    "probe-upstream-hermes",
    "validate-workspace",
    "summarize-workspace",
    "next-step",
    "critique-summary",
    "stage-route-report",
    "run-local",
    "resume-local",
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
]
DOMAIN_ENTRY_COMMAND_CONTRACTS = [
    {"command": "probe-upstream-hermes", "required_fields": [], "optional_fields": []},
    {"command": "validate-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "summarize-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "next-step", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "critique-summary", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "stage-route-report", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "run-local", "required_fields": ["input_path"], "optional_fields": ["journal_path"]},
    {"command": "resume-local", "required_fields": ["journal_path"], "optional_fields": []},
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


class ProductEntryCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(list(args))
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
        self.assertEqual(direct_envelope["runtime_session_contract"]["start_entry"], "run-local")
        self.assertEqual(direct_envelope["runtime_session_contract"]["resume_entry"], "resume-local")
        self.assertEqual(
            direct_envelope["return_surface_contract"]["entry_adapter"],
            "MedAutoGrantDomainEntry",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["domain_entry_contract"],
            {
                "entry_adapter": "MedAutoGrantDomainEntry",
                "service_safe_surface_kind": "service-safe-domain-entry-command",
                "product_entry_builder_command": "build-product-entry",
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
                "focus": {
                    "applicant_name": "示例申请人",
                    "funding_program": "nsfc-2026-general",
                    "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                    "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                    "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                    "critique_verdict": "major_revision",
                },
                "product_entry_surface": {
                    "builder_command": "build-product-entry",
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
                "focus": {
                    "applicant_name": "示例申请人",
                    "funding_program": "nsfc-2026-general",
                    "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                    "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                    "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                    "critique_verdict": "ready_for_submission",
                },
                "product_entry_surface": {
                    "builder_command": "build-product-entry",
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
        self.assertEqual(
            payload["grant_cockpit"]["workspace_overview"],
            {
                "applicant_name": "示例申请人",
                "funding_program": "nsfc-2026-general",
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
                "grant_progress": f"uv run python -m med_autogrant grant-progress --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
                "summarize_workspace": f"uv run python -m med_autogrant summarize-workspace --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
                "stage_route_report": f"uv run python -m med_autogrant stage-route-report --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
                "critique_summary": f"uv run python -m med_autogrant critique-summary --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
                "build_direct_entry": f"uv run python -m med_autogrant build-product-entry --input {CRITIQUE_EXAMPLE_PATH.resolve()} --entry-mode direct --task-intent <describe-task-intent> --format json",
                "build_opl_handoff": f"uv run python -m med_autogrant build-product-entry --input {CRITIQUE_EXAMPLE_PATH.resolve()} --entry-mode opl-handoff --task-intent <describe-task-intent> --format json",
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
                    "focus": {
                        "applicant_name": "示例申请人",
                        "funding_program": "nsfc-2026-general",
                        "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                        "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                        "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                        "critique_verdict": "major_revision",
                    },
                    "product_entry_surface": {
                        "builder_command": "build-product-entry",
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
                        "start_entry": "run-local",
                        "resume_entry": "resume-local",
                        "runtime_substrate_contract": {
                            "runtime_owner": "Hermes",
                            "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                            "active_phase": "P4 mature direct grant product entry",
                            "active_tranche": "P4.D full grant authoring executor landing",
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
                            "product_entry_builder_command": "build-product-entry",
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
                        "start_entry": "run-local",
                        "resume_entry": "resume-local",
                        "runtime_substrate_contract": {
                            "runtime_owner": "Hermes",
                            "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                            "active_phase": "P4 mature direct grant product entry",
                            "active_tranche": "P4.D full grant authoring executor landing",
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
                            "product_entry_builder_command": "build-product-entry",
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
                            "start_entry": "run-local",
                            "resume_entry": "resume-local",
                            "runtime_substrate_contract": {
                                "runtime_owner": "Hermes",
                                "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                                "active_phase": "P4 mature direct grant product entry",
                                "active_tranche": "P4.D full grant authoring executor landing",
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
                                "product_entry_builder_command": "build-product-entry",
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
                            "start_entry": "run-local",
                            "resume_entry": "resume-local",
                            "runtime_substrate_contract": {
                                "runtime_owner": "Hermes",
                                "current_owner_line": "CLI-first with real upstream Hermes-Agent runtime substrate",
                                "active_phase": "P4 mature direct grant product entry",
                                "active_tranche": "P4.D full grant authoring executor landing",
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
                                "product_entry_builder_command": "build-product-entry",
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
            "P4.D full grant authoring executor landing",
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
            (
                "uv run python -m med_autogrant execute-revision-pass "
                f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} "
                "--output <revision-output-path> --format json"
            ),
        )
        self.assertIsNone(payload["grant_user_loop"]["next_action"]["handoff_surfaces"])
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["mainline_status"],
            "uv run python -m med_autogrant mainline-status --format json",
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["phase_status_current"],
            "uv run python -m med_autogrant mainline-phase --phase current --format json",
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_cockpit"],
            f"uv run python -m med_autogrant grant-cockpit --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
            (
                "uv run python -m med_autogrant grant-direct-entry "
                f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} "
                "--task-intent tighten-grant-mainline --format json"
            ),
        )

    def test_product_entry_manifest_projects_current_grant_shell_and_shared_handoff(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertEqual(payload["command"], "product-entry-manifest")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        manifest = payload["product_entry_manifest"]
        self.assertEqual(manifest["surface_kind"], "product_entry_manifest")
        self.assertEqual(manifest["manifest_kind"], "med_auto_grant_product_entry_manifest")
        self.assertEqual(manifest["target_domain_id"], "med-autogrant")
        self.assertEqual(manifest["formal_entry"]["default"], "CLI")
        self.assertEqual(manifest["formal_entry"]["supported_protocols"], ["MCP"])
        self.assertEqual(manifest["workspace_locator"]["workspace_root"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(manifest["workspace_locator"]["workspace_path"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(manifest["recommended_shell"], "grant_user_loop")
        self.assertEqual(
            manifest["recommended_command"],
            "uv run python -m med_autogrant grant-user-loop "
            f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} --task-intent <describe-task-intent> --format json",
        )
        self.assertEqual(manifest["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(
            manifest["frontdesk_surface"]["command"],
            f"uv run python -m med_autogrant product-frontdesk --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
        )
        self.assertEqual(manifest["frontdesk_surface"]["surface_kind"], "product_frontdesk")
        self.assertIn("direct grant product frontdesk", manifest["frontdesk_surface"]["summary"])
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
            "P4.D full grant authoring executor landing",
        )
        self.assertEqual(manifest["repo_mainline"]["phase_id"], "P4")
        self.assertEqual(
            manifest["repo_mainline"]["phase_summary"],
            "把 direct grant product 面逐步收成当前用户 inbox shell，而不越界写成 mature Web UI 或 hosted runtime。",
        )
        self.assertEqual(
            manifest["repo_mainline"]["next_focus"],
            [
                "继续把 `grant-user-loop` 当作当前 direct grant user inbox shell，并保持全链 landed route catalog 与 mainline snapshot / product entry truth 对齐。",
                "继续用 fresh proof 验证 direction_screening -> frozen 的 landed authoring executor 链条在 Hermes substrate 上不漂移。",
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
            f"uv run python -m med_autogrant grant-progress --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
        )
        self.assertEqual(
            manifest["product_entry_shell"]["grant_user_loop"]["command"],
            "uv run python -m med_autogrant grant-user-loop "
            f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} --task-intent <describe-task-intent> --format json",
        )
        self.assertEqual(
            manifest["product_entry_shell"]["product_frontdesk"]["command"],
            f"uv run python -m med_autogrant product-frontdesk --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
        )
        self.assertEqual(
            manifest["shared_handoff"]["direct_entry_builder"]["command"],
            "uv run python -m med_autogrant build-product-entry "
            f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} --entry-mode direct --task-intent <describe-task-intent> --format json",
        )
        self.assertEqual(
            manifest["shared_handoff"]["opl_handoff_builder"]["command"],
            "uv run python -m med_autogrant build-product-entry "
            f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} --entry-mode opl-handoff --task-intent <describe-task-intent> --format json",
        )

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
            (
                "uv run python -m med_autogrant execute-critique-pass "
                f"--input {DRAFTING_EXAMPLE_PATH.resolve()} "
                "--output <critique-output-path> --format json"
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["handoff_surfaces"],
            None,
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            (
                "uv run python -m med_autogrant execute-critique-pass "
                f"--input {DRAFTING_EXAMPLE_PATH.resolve()} "
                "--output <critique-output-path> --format json"
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
            (
                "uv run python -m med_autogrant grant-direct-entry "
                f"--input {DRAFTING_EXAMPLE_PATH.resolve()} "
                "--task-intent prepare-critique-handoff --format json"
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
            (
                "uv run python -m med_autogrant execute-question-refinement-pass "
                f"--input {DIRECTION_EXAMPLE_PATH.resolve()} "
                "--output <question-refinement-output-path> --format json"
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            (
                "uv run python -m med_autogrant execute-question-refinement-pass "
                f"--input {DIRECTION_EXAMPLE_PATH.resolve()} "
                "--output <question-refinement-output-path> --format json"
            ),
        )

    def test_product_frontdesk_projects_frontdoor_over_current_grant_loop(self) -> None:
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
            f"uv run python -m med_autogrant product-frontdesk --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
        )
        self.assertEqual(frontdesk["operator_loop_surface"]["shell_key"], "grant_user_loop")
        self.assertEqual(
            frontdesk["entry_surfaces"]["frontdesk"]["command"],
            f"uv run python -m med_autogrant product-frontdesk --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
        )
        self.assertEqual(
            frontdesk["entry_surfaces"]["grant_user_loop"]["command"],
            "uv run python -m med_autogrant grant-user-loop "
            f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} --task-intent <describe-task-intent> --format json",
        )
        self.assertEqual(
            frontdesk["entry_surfaces"]["direct_entry_builder"]["command"],
            "uv run python -m med_autogrant build-product-entry "
            f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} --entry-mode direct --task-intent <describe-task-intent> --format json",
        )
        self.assertEqual(
            frontdesk["summary"]["frontdesk_command"],
            f"uv run python -m med_autogrant product-frontdesk --input {CRITIQUE_EXAMPLE_PATH.resolve()} --format json",
        )
        self.assertEqual(
            frontdesk["summary"]["operator_loop_command"],
            "uv run python -m med_autogrant grant-user-loop "
            f"--input {CRITIQUE_EXAMPLE_PATH.resolve()} --task-intent <describe-task-intent> --format json",
        )
        self.assertEqual(frontdesk["product_entry_manifest"]["frontdesk_surface"]["shell_key"], "product_frontdesk")

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
                "grant_progress": "uv run python -m med_autogrant grant-progress --format json",
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_cockpit"):
                MedAutoGrantProductEntry().read_grant_cockpit(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )


if __name__ == "__main__":
    unittest.main()
