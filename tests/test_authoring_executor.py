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
)
from med_autogrant.workspace import validate_workspace_document  # noqa: E402


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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

        for stage, builder, document, input_path, response, workspace_key, counts, cleared in cases:
            with self.subTest(stage=stage):
                payload = builder(
                    document=document,
                    input_path=input_path,
                    codex_runner=lambda _prompt, *, cwd, response=response: copy.deepcopy(response),
                )
                workspace = payload[workspace_key]

                self.assertEqual(payload["lifecycle_stage"], stage)
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
        payload = build_freeze_execution_document(document=_load(READY_FOR_SUBMISSION_EXAMPLE_PATH))
        workspace = payload["frozen_workspace"]

        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertTrue(workspace["gates"]["presubmission_frozen"])
        self.assertEqual(workspace["application_drafts"][0]["status"], "frozen")
        self.assertEqual(payload["freeze_execution"]["executor"]["kind"], "deterministic_domain_logic")
        self.assertTrue(validate_workspace_document(workspace).ok)
