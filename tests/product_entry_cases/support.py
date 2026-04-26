from __future__ import annotations

from copy import deepcopy
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch


REPO_ROOT = Path(__file__).resolve().parents[2]
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
    "grant-quality-scorecard",
    "grant-quality-diff",
    "grant-quality-closure-dossier",
    "discover-funding-opportunities",
    "refresh-funding-opportunities-cache",
    "select-project-profile",
    "initialize-intake-workspace",
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
    "execute-critique-revision-loop",
    "execute-authoring-mainline-loop",
    "execute-grant-autonomy-controller",
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
    {"command": "grant-quality-scorecard", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-quality-closure-dossier", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "grant-quality-diff",
        "required_fields": ["input_path", "previous_input_path"],
        "optional_fields": [],
    },
    {"command": "discover-funding-opportunities", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "refresh-funding-opportunities-cache",
        "required_fields": ["input_path"],
        "optional_fields": ["output_path"],
    },
    {"command": "select-project-profile", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "initialize-intake-workspace",
        "required_fields": ["input_path"],
        "optional_fields": ["output_path", "workspace_root", "initialize_git"],
    },
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
    {
        "command": "execute-critique-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": ["executor_kind"],
    },
    {
        "command": "execute-critique-revision-loop",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["max_rounds", "executor_kind"],
    },
    {
        "command": "execute-authoring-mainline-loop",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["max_cycles", "executor_kind"],
    },
    {
        "command": "execute-grant-autonomy-controller",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["executor_kind"],
    },
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

__all__ = [name for name in globals() if not name.startswith("__")]
