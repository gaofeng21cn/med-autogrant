from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from cli_validate_cases import DRAFTING_EXAMPLE_PATH, REVISION_EXAMPLE_PATH  # noqa: E402
from med_autogrant.workspace import load_workspace_document, validate_workspace_document  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
CRITIQUE_PACKET_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REREVIEW_PACKET_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"


def _closeout_packet(path: Path) -> dict[str, object]:
    workspace = json.loads(path.read_text(encoding="utf-8"))
    return {
        "mentor_critique": deepcopy(workspace["mentor_critiques"][-1]),
        "revision_plan": deepcopy(workspace["revision_plans"][-1]),
    }


def _codex_receipt(packet: dict[str, object]) -> dict[str, object]:
    return {
        "surface_kind": "opl_agent_execution_receipt",
        "executor_kind": "codex_cli",
        "mode": "structured_call",
        "cwd": str(DRAFTING_EXAMPLE_PATH.resolve().parent),
        "prompt_preview": "prompt",
        "session_id": "codex-session-proof-001",
        "event_summary": [],
        "stdout_preview": "{}",
        "stderr_preview": "",
        "exit_code": 0,
        "non_equivalence_notice": "codex_cli_first_class_default",
        "proof": {
            "model": None,
            "provider": None,
            "reasoning_effort": None,
            "default_executor": True,
        },
        "closeout_packet": {
            "surface_kind": "domain_stage_closeout_packet",
            "route_id": "critique",
            "domain_output_kind": "mag_critique_output",
            "domain_output": deepcopy(packet),
        },
    }


def _hermes_receipt(packet: dict[str, object]) -> dict[str, object]:
    event_stream = [{"type": "tool_complete", "tool": "read_file"}]
    proof = {
        "full_agent_loop_proved": True,
        "session_id": "hermes-session-proof-001",
        "api_calls": 2,
        "tool_call_count": 1,
        "event_count": 1,
        "provider_reasoning_status": "unproven_custom_chat_completions",
        "event_stream": event_stream,
    }
    return {
        "surface_kind": "opl_agent_execution_receipt",
        "executor_kind": "hermes_agent",
        "mode": "agent_loop",
        "event_summary": event_stream,
        "exit_code": 0,
        "non_equivalence_notice": "connectivity_lifecycle_receipt_audit_only",
        "proof": proof,
        "executor_contract": {
            "entrypoint": "OPL AgentExecutionRequest -> AgentExecutionReceipt",
            "model": "gpt-5.4",
            "provider": "custom",
            "api_mode": "chat_completions",
            "reasoning_effort": "xhigh",
        },
        "closeout_packet": {
            "surface_kind": "domain_stage_closeout_packet",
            "route_id": "critique",
            "domain_output_kind": "mag_critique_output",
            "domain_output": deepcopy(packet),
        },
    }


class CritiqueExecutionDocumentTest(unittest.TestCase):
    def test_prompt_keeps_grant_review_policy_and_profile_resolution(self) -> None:
        from med_autogrant.critique_executor import _build_critique_context, _build_critique_prompt
        from med_autogrant.workspace_projection_parts import _build_workspace_state

        cases = (
            (
                load_workspace_document(DRAFTING_EXAMPLE_PATH),
                (
                    "must each be an object with exactly weight, score, judgment",
                    "necessity_scientific_value=60, applicant_fit=30, feasibility=10",
                    "diagnose necessity and scientific question first",
                ),
            ),
            (
                self._nih_workspace(),
                (
                    "policy_id: nih_r21_significance_innovation_v1",
                    "persona role: NIH R21 scientific reviewer",
                    "significance=45, innovation=35, investigator_environment_fit=20",
                ),
            ),
        )
        for document, fragments in cases:
            with self.subTest(profile=document["project_profile"]["preset_id"]):
                prompt = _build_critique_prompt(
                    context=_build_critique_context(document=document, state=_build_workspace_state(document)),
                    input_path=DRAFTING_EXAMPLE_PATH,
                )
                for fragment in fragments:
                    self.assertIn(fragment, prompt)

    def test_critique_materializes_initial_and_rereview_domain_evidence(self) -> None:
        from med_autogrant.critique_executor import build_critique_execution_document

        cases = (
            (DRAFTING_EXAMPLE_PATH, CRITIQUE_PACKET_PATH, "revision-v1", None, "v0.1"),
            (REVISION_EXAMPLE_PATH, REREVIEW_PACKET_PATH, "revision-v2", "revision-v1", "v0.4"),
        )
        for input_path, packet_path, revision_id, reviewed_revision_id, pre_version in cases:
            with self.subTest(input=input_path.name):
                payload = build_critique_execution_document(
                    document=load_workspace_document(input_path),
                    input_path=input_path,
                    executor_runner=lambda _request, *, timeout_seconds: _codex_receipt(
                        _closeout_packet(packet_path)
                    ),
                )
                workspace = payload["critique_workspace"]
                critique = workspace["mentor_critiques"][-1]
                revision = workspace["revision_plans"][-1]
                evidence = critique["metadata"]["independent_review_evidence"]

                self.assertEqual(payload["active_revision_plan_id"], revision_id)
                self.assertEqual(critique.get("reviewed_revision_plan_id"), reviewed_revision_id)
                self.assertEqual(revision["revision_plan_id"], revision_id)
                self.assertEqual(revision["pre_revision_version_label"], pre_version)
                self.assertEqual(
                    [critique[field]["weight"] for field in ("necessity_scientific_value", "applicant_fit", "feasibility")],
                    [60, 30, 10],
                )
                self.assertTrue(evidence["no_shared_context_verified"])
                self.assertEqual(revision["execution_status"], "planned")
                self.assertTrue(validate_workspace_document(workspace).ok)

    def test_hermes_receipt_preserves_non_equivalence_and_review_receipt(self) -> None:
        from med_autogrant.critique_executor import build_critique_execution_document
        from med_autogrant.domain_executor_client import OPL_EXECUTOR_TIMEOUT_SECONDS
        from opl_framework.executor_client import run_agent_execution_request

        self.assertIs(
            build_critique_execution_document.__kwdefaults__["executor_runner"],
            run_agent_execution_request,
        )

        observed: dict[str, object] = {}

        def run_via_opl(request: dict[str, object], *, timeout_seconds: float) -> dict[str, object]:
            observed["request"] = request
            observed["timeout_seconds"] = timeout_seconds
            return _hermes_receipt(_closeout_packet(CRITIQUE_PACKET_PATH))

        payload = build_critique_execution_document(
            document=load_workspace_document(DRAFTING_EXAMPLE_PATH),
            input_path=DRAFTING_EXAMPLE_PATH,
            executor_kind="hermes_agent",
            executor_runner=run_via_opl,
        )
        executor = payload["critique_execution"]["executor"]
        evidence = payload["critique_workspace"]["mentor_critiques"][-1]["metadata"][
            "independent_review_evidence"
        ]

        self.assertEqual(executor["kind"], "hermes_agent")
        self.assertEqual(executor["adapter_owner"], "one-person-lab")
        self.assertFalse(executor["fallback_allowed"])
        self.assertEqual(executor["non_equivalence_notice"], "connectivity_lifecycle_receipt_audit_only")
        self.assertTrue(executor["full_agent_loop_proved"])
        self.assertEqual(evidence["review_receipt_ref"], "opl_agent_execution_receipt::hermes-session-proof-001")
        self.assertEqual(observed["timeout_seconds"], OPL_EXECUTOR_TIMEOUT_SECONDS)
        request = observed["request"]
        self.assertIsInstance(request, dict)
        self.assertEqual(request["executor_kind"], "hermes_agent")
        self.assertEqual(request["mode"], "agent_loop")
        self.assertEqual(request["cwd"], str(DRAFTING_EXAMPLE_PATH.resolve().parent))
        self.assertEqual(request["domain_payload"]["route_id"], "critique")

    def test_default_codex_critique_uses_the_same_opl_client_contract(self) -> None:
        from med_autogrant.critique_executor import build_critique_execution_document

        observed: dict[str, object] = {}

        def run_via_opl(request: dict[str, object], *, timeout_seconds: float) -> dict[str, object]:
            observed["request"] = request
            observed["timeout_seconds"] = timeout_seconds
            return _codex_receipt(_closeout_packet(CRITIQUE_PACKET_PATH))

        payload = build_critique_execution_document(
            document=load_workspace_document(DRAFTING_EXAMPLE_PATH),
            input_path=DRAFTING_EXAMPLE_PATH,
            executor_runner=run_via_opl,
        )

        executor = payload["critique_execution"]["executor"]
        request = observed["request"]
        self.assertEqual(executor["kind"], "codex_cli")
        self.assertEqual(executor["adapter_owner"], "one-person-lab")
        self.assertEqual(request["executor_kind"], "codex_cli")
        self.assertEqual(request["mode"], "structured_call")
        self.assertEqual(request["domain_payload"]["domain_output_kind"], "mag_critique_output")
        self.assertEqual(observed["timeout_seconds"], 300.0)

    def test_executor_selection_and_receipt_shape_fail_closed(self) -> None:
        from med_autogrant.critique_executor import (
            _resolve_critique_executor_kind,
            build_critique_execution_document,
        )
        from med_autogrant.workspace import WorkspaceStateError

        self.assertEqual(_resolve_critique_executor_kind(None), "codex_cli")
        self.assertEqual(_resolve_critique_executor_kind("hermes_agent"), "hermes_agent")
        for retired_alias in ("codex_cli_autonomous", "hermes_native_proof"):
            with self.subTest(retired_alias=retired_alias):
                with self.assertRaisesRegex(WorkspaceStateError, "不支持该 executor_kind"):
                    _resolve_critique_executor_kind(retired_alias)

        invalid_receipt = _hermes_receipt(_closeout_packet(CRITIQUE_PACKET_PATH))
        invalid_receipt.pop("surface_kind")
        with self.assertRaisesRegex(WorkspaceStateError, "surface_kind"):
            build_critique_execution_document(
                document=load_workspace_document(DRAFTING_EXAMPLE_PATH),
                input_path=DRAFTING_EXAMPLE_PATH,
                executor_kind="hermes_agent",
                executor_runner=lambda _request, *, timeout_seconds: invalid_receipt,
            )

        def timed_out(_request: dict[str, object], *, timeout_seconds: float) -> dict[str, object]:
            raise TimeoutError(f"timed out after {timeout_seconds}")

        with self.assertRaisesRegex(WorkspaceStateError, "OPL executor client 执行失败"):
            build_critique_execution_document(
                document=load_workspace_document(DRAFTING_EXAMPLE_PATH),
                input_path=DRAFTING_EXAMPLE_PATH,
                executor_kind="hermes_agent",
                executor_runner=timed_out,
            )

    @staticmethod
    def _nih_workspace() -> dict[str, object]:
        document = deepcopy(load_workspace_document(DRAFTING_EXAMPLE_PATH))
        document["project_profile"]["preset_id"] = "nih_r21_translational_v1"
        document["project_profile"]["profile_label"] = "NIH R21 translational profile"
        document["project_profile"]["critique_policy"] = {
            "preset_id": "nih_r21_significance_innovation_v1",
            "policy_id": "nih_r21_significance_innovation_v1",
        }
        return document
