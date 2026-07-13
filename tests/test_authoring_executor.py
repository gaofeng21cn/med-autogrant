from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from cli_validate_cases import (  # noqa: E402
    CRITIQUE_EXAMPLE_PATH,
    INPUT_EXAMPLE_PATH,
    QUESTION_EXAMPLE_PATH,
    READY_FOR_SUBMISSION_EXAMPLE_PATH,
)
from med_autogrant.authoring_executor import (  # noqa: E402
    build_argument_building_execution_document,
    build_direction_screening_execution_document,
    build_drafting_execution_document,
    build_fit_alignment_execution_document,
    build_freeze_execution_document,
    build_outline_execution_document,
    build_question_refinement_execution_document,
    build_strategy_authoring_execution_document,
)
from med_autogrant.authoring_executor_parts import (  # noqa: E402
    _build_argument_building_prompt,
    _build_direction_screening_prompt,
    _build_drafting_prompt,
)
from med_autogrant.workspace import validate_workspace_document  # noqa: E402
from opl_framework.executor_client import run_agent_execution_request  # noqa: E402


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _executor_receipt(route_id: str, domain_output: dict[str, Any]) -> dict[str, Any]:
    return {
        "surface_kind": "opl_agent_execution_receipt",
        "executor_kind": "codex_cli",
        "mode": "structured_call",
        "cwd": "/tmp",
        "prompt_preview": "prompt",
        "session_id": f"codex-{route_id}",
        "event_summary": [],
        "stdout_preview": "{}",
        "stderr_preview": "",
        "exit_code": 0,
        "closeout_packet": {
            "surface_kind": "domain_stage_closeout_packet",
            "route_id": route_id,
            "domain_output_kind": "mag_authoring_output",
            "domain_output": copy.deepcopy(domain_output),
        },
        "executor_contract": None,
        "capabilities": ["structured_call"],
        "non_equivalence_notice": "codex_cli_first_class_default",
        "proof": {
            "model": None,
            "provider": None,
            "reasoning_effort": None,
            "default_executor": True,
        },
    }


def _rewind_critique(
    stage: str,
    selection_keys: tuple[str, ...],
) -> dict[str, Any]:
    document = _load(CRITIQUE_EXAMPLE_PATH)
    document["lifecycle_stage"] = stage
    document["current_selection"] = {
        key: document["current_selection"][key] for key in selection_keys
    }
    return document


class AuthoringExecutorTest(unittest.TestCase):
    def test_strategy_authoring_projects_six_checkpoints_from_one_observed_default_invocation(self) -> None:
        canonical = _load(CRITIQUE_EXAMPLE_PATH)
        direction = copy.deepcopy(canonical["direction_hypotheses"][0])
        direction["required_evidence_ids"] = []
        question = copy.deepcopy(canonical["scientific_question_cards"][0])
        question["linked_evidence_ids"] = []
        argument = copy.deepcopy(canonical["argument_chains"][0])
        argument["linked_evidence_ids"] = []
        fit = copy.deepcopy(canonical["applicant_fit_mappings"][0])
        fit["linked_evidence_ids"] = []
        draft = copy.deepcopy(canonical["application_drafts"][0])
        for item in [*draft["outline"], *draft["sections"]]:
            item["linked_object_ids"] = []
        response = {
            "selected_direction_index": 0,
            "direction_hypotheses": [direction],
            "scientific_question_card": question,
            "argument_chain": argument,
            "applicant_fit_mapping": fit,
            "application_draft": draft,
        }
        calls = []

        def executor_runner(request: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
            calls.append((request, timeout_seconds))
            return _executor_receipt("strategy_authoring", response)

        payload = build_strategy_authoring_execution_document(
            document=_load(INPUT_EXAMPLE_PATH),
            input_path=INPUT_EXAMPLE_PATH,
            executor_runner=executor_runner,
        )

        self.assertEqual(len(calls), 1)
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        execution = payload["strategy_authoring_execution"]
        self.assertEqual(execution["observed_codex_invocation_count"], 1)
        self.assertFalse(execution["invocation_count_is_success_condition"])
        self.assertEqual(execution["checkpoint_projection_mode"], "deterministic_contract_projection")
        self.assertTrue(execution["attempt_retry_and_route_back_allowed"])
        self.assertEqual(
            payload["strategy_authoring_execution"]["checkpoint_routes"],
            ["direction_screening", "question_refinement", "argument_building", "fit_alignment", "outline", "drafting"],
        )
        self.assertTrue(validate_workspace_document(payload["strategy_authoring_workspace"]).ok)

    def test_authoring_prompts_keep_dependencies_without_fixed_cognitive_recipe(self) -> None:
        canonical = _load(CRITIQUE_EXAMPLE_PATH)
        direction_prompt = _build_direction_screening_prompt(input_path=INPUT_EXAMPLE_PATH, known_ids=[])
        argument_prompt = _build_argument_building_prompt(
            input_path=QUESTION_EXAMPLE_PATH,
            selected_direction=canonical["direction_hypotheses"][0],
            selected_question=canonical["scientific_question_cards"][0],
            known_ids=[],
        )
        drafting_prompt = _build_drafting_prompt(
            input_path=CRITIQUE_EXAMPLE_PATH,
            active_draft=canonical["application_drafts"][0],
            selected_question=canonical["scientific_question_cards"][0],
            active_argument_chain=canonical["argument_chains"][0],
            active_fit_mapping=canonical["applicant_fit_mappings"][0],
            known_ids=[],
        )

        self.assertIn("use multiple candidates only when comparison improves the decision", direction_prompt)
        self.assertNotIn("2 to 5 objects", direction_prompt)
        self.assertIn("interdependent professional judgments", argument_prompt)
        self.assertNotIn("write significance first", argument_prompt)
        self.assertIn("unless human approval has frozen it", drafting_prompt)

    def test_authoring_stages_materialize_only_their_domain_delta(self) -> None:
        canonical = _load(CRITIQUE_EXAMPLE_PATH)
        direction = copy.deepcopy(canonical["direction_hypotheses"][0])
        direction["required_evidence_ids"] = []
        other_direction = copy.deepcopy(direction)
        other_direction["title"] = f'{direction["title"]}（备选）'

        question = copy.deepcopy(canonical["scientific_question_cards"][0])
        question["linked_evidence_ids"] = []
        argument = copy.deepcopy(canonical["argument_chains"][0])
        argument["linked_evidence_ids"] = []
        fit_mapping = copy.deepcopy(canonical["applicant_fit_mappings"][0])
        fit_mapping["linked_evidence_ids"] = []

        direction_input = _load(INPUT_EXAMPLE_PATH)
        for field in (
            "scientific_question_cards",
            "argument_chains",
            "applicant_fit_mappings",
            "application_drafts",
            "mentor_critiques",
            "revision_plans",
        ):
            direction_input[field] = copy.deepcopy(canonical[field])

        question_input = _load(QUESTION_EXAMPLE_PATH)
        question_input["lifecycle_stage"] = "direction_screening"
        question_input["current_selection"] = {
            "selected_direction_id": question_input["current_selection"]["selected_direction_id"]
        }

        fit_input = _rewind_critique(
            "argument_building",
            ("selected_direction_id", "selected_question_id"),
        )
        outline_input = _rewind_critique(
            "fit_alignment",
            ("selected_direction_id", "selected_question_id", "active_fit_mapping_id"),
        )
        drafting_input = _rewind_critique(
            "outline",
            (
                "selected_direction_id",
                "selected_question_id",
                "active_fit_mapping_id",
                "active_draft_id",
            ),
        )
        drafting_input["application_drafts"][0]["status"] = "outline"
        drafting_input["application_drafts"][0]["sections"] = []

        cases = (
            (
                "direction_screening",
                build_direction_screening_execution_document,
                direction_input,
                INPUT_EXAMPLE_PATH,
                {"selected_direction_index": 1, "direction_hypotheses": [direction, other_direction]},
                "direction_screening_workspace",
                {"direction_hypotheses": 2},
                (
                    "scientific_question_cards",
                    "argument_chains",
                    "applicant_fit_mappings",
                    "application_drafts",
                    "mentor_critiques",
                    "revision_plans",
                ),
            ),
            (
                "question_refinement",
                build_question_refinement_execution_document,
                question_input,
                QUESTION_EXAMPLE_PATH,
                {"scientific_question_card": question},
                "question_refinement_workspace",
                {"scientific_question_cards": 1},
                ("argument_chains", "applicant_fit_mappings", "application_drafts", "mentor_critiques", "revision_plans"),
            ),
            (
                "argument_building",
                build_argument_building_execution_document,
                _load(QUESTION_EXAMPLE_PATH),
                QUESTION_EXAMPLE_PATH,
                {"argument_chain": argument},
                "argument_building_workspace",
                {"argument_chains": 1},
                ("applicant_fit_mappings", "application_drafts", "mentor_critiques", "revision_plans"),
            ),
            (
                "fit_alignment",
                build_fit_alignment_execution_document,
                fit_input,
                CRITIQUE_EXAMPLE_PATH,
                {"applicant_fit_mapping": fit_mapping},
                "fit_alignment_workspace",
                {"applicant_fit_mappings": 1},
                ("application_drafts", "mentor_critiques", "revision_plans"),
            ),
            (
                "outline",
                build_outline_execution_document,
                outline_input,
                CRITIQUE_EXAMPLE_PATH,
                {"application_draft": canonical["application_drafts"][0]},
                "outline_workspace",
                {"application_drafts": 1},
                ("mentor_critiques", "revision_plans"),
            ),
            (
                "drafting",
                build_drafting_execution_document,
                drafting_input,
                CRITIQUE_EXAMPLE_PATH,
                {"application_draft": canonical["application_drafts"][0]},
                "drafting_workspace",
                {"application_drafts": 1},
                ("mentor_critiques", "revision_plans"),
            ),
        )

        for _stage, builder, *_rest in cases:
            self.assertIs(
                builder.__kwdefaults__["executor_runner"],
                run_agent_execution_request,
            )

        for stage, builder, document, input_path, response, workspace_key, counts, cleared in cases:
            with self.subTest(stage=stage):
                calls: list[tuple[dict[str, Any], float]] = []

                def executor_runner(
                    request: dict[str, Any],
                    *,
                    timeout_seconds: float,
                ) -> dict[str, Any]:
                    calls.append((request, timeout_seconds))
                    return _executor_receipt(stage, response)

                payload = builder(
                    document=document,
                    input_path=input_path,
                    executor_runner=executor_runner,
                )
                workspace = payload[workspace_key]
                selection = workspace["current_selection"]
                executor = payload[f"{stage}_execution"]["executor"]
                self.assertEqual(executor["kind"], "codex_cli")
                self.assertEqual(executor["adapter_owner"], "one-person-lab")
                self.assertEqual(executor["model"], "inherit_local_executor_default")
                self.assertEqual(executor["reasoning_effort"], "inherit_local_executor_default")
                self.assertEqual(executor["session_id"], f"codex-{stage}")
                if stage == "direction_screening":
                    execution_fields = {
                        "selected_direction_id": selection["selected_direction_id"],
                        "direction_count": len(workspace["direction_hypotheses"]),
                    }
                elif stage == "question_refinement":
                    execution_fields = {
                        "selected_direction_id": selection["selected_direction_id"],
                        "selected_question_id": selection["selected_question_id"],
                    }
                elif stage == "argument_building":
                    execution_fields = {
                        "selected_question_id": selection["selected_question_id"],
                        "argument_chain_id": workspace["argument_chains"][0]["argument_chain_id"],
                    }
                elif stage == "fit_alignment":
                    execution_fields = {
                        "selected_question_id": selection["selected_question_id"],
                        "active_fit_mapping_id": selection["active_fit_mapping_id"],
                    }
                elif stage == "outline":
                    execution_fields = {
                        "active_fit_mapping_id": selection["active_fit_mapping_id"],
                        "draft_id": selection["active_draft_id"],
                        "outline_count": len(workspace["application_drafts"][0]["outline"]),
                    }
                else:
                    execution_fields = {
                        "draft_id": selection["active_draft_id"],
                        "version_label": workspace["application_drafts"][0]["version_label"],
                        "section_count": len(workspace["application_drafts"][0]["sections"]),
                    }

                self.assertEqual(payload["lifecycle_stage"], stage)
                self.assertEqual(payload["grant_run_id"], workspace["grant_run_id"])
                self.assertEqual(payload["workspace_id"], workspace["workspace_id"])
                self.assertEqual(payload["draft_id"], selection.get("active_draft_id"))
                self.assertEqual(
                    {key: value for key, value in payload[f"{stage}_execution"].items() if key != "executor"},
                    execution_fields,
                )
                self.assertEqual(len(calls), 1)
                request, timeout_seconds = calls[0]
                self.assertIn(str(input_path.resolve()), request["prompt"])
                self.assertEqual(request["cwd"], str(input_path.resolve().parent))
                self.assertEqual(request["executor_kind"], "codex_cli")
                self.assertEqual(request["domain_payload"]["route_id"], stage)
                self.assertEqual(timeout_seconds, 300.0)
                for field, expected_count in counts.items():
                    self.assertEqual(len(workspace[field]), expected_count)
                for field in cleared:
                    self.assertEqual(workspace[field], [])
                if stage == "direction_screening":
                    self.assertEqual(workspace["direction_hypotheses"][1]["decision_status"], "selected")
                if stage in {"outline", "drafting"}:
                    expected_status = "outline" if stage == "outline" else "draft"
                    self.assertEqual(workspace["application_drafts"][0]["status"], expected_status)
                validation = validate_workspace_document(workspace)
                self.assertTrue(validation.ok, validation.to_dict(workspace))

    def test_freeze_pass_closes_presubmission_authority_gate(self) -> None:
        document = _load(READY_FOR_SUBMISSION_EXAMPLE_PATH)
        payload = build_freeze_execution_document(document=document)
        workspace = payload["frozen_workspace"]

        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertEqual(payload["grant_run_id"], workspace["grant_run_id"])
        self.assertEqual(payload["workspace_id"], workspace["workspace_id"])
        self.assertEqual(payload["draft_id"], workspace["current_selection"]["active_draft_id"])
        self.assertTrue(workspace["gates"]["presubmission_frozen"])
        self.assertEqual(workspace["application_drafts"][0]["status"], "frozen")
        self.assertEqual(
            payload["freeze_execution"],
            {
                "executor": {
                    "kind": "deterministic_domain_logic",
                    "model": None,
                    "reasoning_effort": None,
                },
                "draft_id": document["current_selection"]["active_draft_id"],
                "revision_plan_id": document["current_selection"]["active_revision_plan_id"],
                "critique_id": document["mentor_critiques"][0]["critique_id"],
            },
        )
        self.assertTrue(validate_workspace_document(workspace).ok)
