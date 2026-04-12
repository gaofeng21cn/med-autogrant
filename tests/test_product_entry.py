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
    "build-artifact-bundle",
    "execute-revision-pass",
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
    {"command": "build-artifact-bundle", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-revision-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
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
                "revision": "execute-revision-pass",
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
    if route_id in {"revision", "artifact_bundle", "final_package", "hosted_contract_bundle"}:
        return _expected_landed_route(route_id)
    return _expected_pending_route(route_id, source_stage=source_stage)


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
        self.assertEqual(
            drafting_contract["recommended_executor_route"]["handoff_requirements"]["required_domain_surfaces"],
            [
                _service_safe_surface("summarize-workspace"),
                _service_safe_surface("stage-route-report"),
            ],
        )
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


if __name__ == "__main__":
    unittest.main()
