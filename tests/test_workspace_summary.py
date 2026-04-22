from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.workspace import (  # noqa: E402
    load_workspace_document,
    summarize_workspace_document,
    validate_workspace_document,
)


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"
QUESTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_question_refinement.json"
ARGUMENT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_argument_building.json"
FIT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_fit_alignment.json"
OUTLINE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_outline.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
MAJOR_REFRAME_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_major_reframe.json"
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
NON_NSFC_INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nih_r21_workspace_p2a_input_intake.json"


class WorkspaceSummaryTest(unittest.TestCase):
    def load_example(self) -> dict[str, object]:
        return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def build_re_review_workspace(self) -> dict[str, object]:
        return load_workspace_document(RE_REVIEW_EXAMPLE_PATH)

    def build_forced_rollback_workspace(self) -> dict[str, object]:
        return load_workspace_document(FORCED_ROLLBACK_EXAMPLE_PATH)

    def build_presubmission_frozen_workspace(self) -> dict[str, object]:
        return load_workspace_document(PRESUBMISSION_FROZEN_EXAMPLE_PATH)

    def test_summary_exposes_selected_objects(self) -> None:
        document = load_workspace_document(EXAMPLE_PATH)
        summary = summarize_workspace_document(document)

        self.assertEqual(summary["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(summary["workspace_id"], "nsfc-demo-001")
        self.assertEqual(summary["mode"], "auto")
        self.assertEqual(summary["lifecycle_stage"], "critique")
        self.assertEqual(summary["selected_direction"]["id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["selected_question"]["id"], "question-immune-fibrosis")
        self.assertEqual(summary["active_fit_mapping"]["id"], "fit-001")
        self.assertEqual(summary["active_draft"]["id"], "draft-v1")
        self.assertEqual(summary["active_revision_plan"]["id"], "revision-v1")
        self.assertEqual(summary["active_critique"]["id"], "critique-v1")

    def test_validation_accepts_input_intake_without_downstream_objects(self) -> None:
        document = load_workspace_document(INPUT_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_summary_exposes_intake_audit_and_evidence_grounding_for_input_intake(self) -> None:
        document = load_workspace_document(INPUT_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["project_profile"]["profile_id"], "profile-nsfc-general-medical")
        self.assertEqual(summary["project_profile"]["preset_id"], "nsfc_general_medical_v1")
        self.assertEqual(summary["project_profile"]["template_id"], "nsfc_general_grant_template_v1")
        self.assertEqual(summary["project_profile"]["collaboration_mode"], "applicant_led_agent_copilot")
        self.assertEqual(summary["project_profile"]["critique_policy_id"], "nsfc_mentor_critique_v1")
        self.assertEqual(summary["grant_intake_audit"]["audit_kind"], "grant_intake_audit")
        self.assertEqual(summary["grant_intake_audit"]["applicant_profile_id"], "applicant-gaofeng")
        self.assertEqual(summary["grant_intake_audit"]["project_profile_id"], "profile-nsfc-general-medical")
        self.assertEqual(
            summary["grant_intake_audit"]["project_profile_summary"]["critique_policy_id"],
            "nsfc_mentor_critique_v1",
        )
        self.assertTrue(summary["grant_intake_audit"]["readiness"]["ready_for_direction_screening"])
        self.assertEqual(summary["grant_evidence_grounding"]["grounding_kind"], "grant_evidence_grounding")
        self.assertEqual(summary["grant_evidence_grounding"]["grounding_status"], "intake_grounded")
        self.assertEqual(
            summary["grant_evidence_grounding"]["project_profile_summary"]["template_id"],
            "nsfc_general_grant_template_v1",
        )
        self.assertEqual(
            summary["grant_evidence_grounding"]["evidence_inventory"]["primary_evidence_ids"],
            ["evi-output-1", "evi-prelim-1", "evi-project-1"],
        )

    def test_summary_exposes_grant_intake_audit_and_evidence_grounding_for_input_intake(self) -> None:
        document = load_workspace_document(INPUT_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        intake_audit = summary["grant_intake_audit"]
        self.assertEqual(intake_audit["surface_kind"], "grant_intake_audit")
        self.assertEqual(intake_audit["overall_readiness"], "ready_for_direction_screening")
        self.assertEqual(intake_audit["trust_summary"]["trusted"], 2)
        self.assertEqual(intake_audit["trust_summary"]["usable_with_verification"], 1)
        self.assertEqual(
            [section["section_id"] for section in intake_audit["intake_sections"]],
            [
                "applicant_profile",
                "project_profile",
                "track_record",
                "active_project_set",
                "preliminary_evidence_pack",
                "funding_opportunity_brief",
            ],
        )
        self.assertEqual(intake_audit["blocking_gaps"], [])
        self.assertTrue(intake_audit["readiness"]["project_profile_ready"])

        evidence_grounding = summary["grant_evidence_grounding"]
        self.assertEqual(evidence_grounding["surface_kind"], "grant_evidence_grounding")
        self.assertEqual(evidence_grounding["grounding_status"], "intake_grounded")
        self.assertTrue(evidence_grounding["ready_for_direction_screening"])
        self.assertEqual(
            evidence_grounding["project_profile_summary"]["collaboration_mode"],
            "applicant_led_agent_copilot",
        )
        self.assertEqual(
            [item["trust_level"] for item in evidence_grounding["trust_ranked_evidence"]],
            ["trusted", "trusted", "usable_with_verification"],
        )
        self.assertEqual(
            evidence_grounding["trust_ranked_evidence"][0]["supports"],
            ["applicant_fit", "scientific_question", "technical_route"],
        )
        self.assertEqual(evidence_grounding["evidence_gaps"], [])

    def test_validation_accepts_non_nsfc_profiled_workspace(self) -> None:
        document = load_workspace_document(NON_NSFC_INPUT_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_summary_exposes_non_nsfc_project_profile(self) -> None:
        document = load_workspace_document(NON_NSFC_INPUT_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["project_profile"]["preset_id"], "nih_r21_translational_v1")
        self.assertEqual(summary["project_profile"]["funder"], "NIH")
        self.assertEqual(summary["project_profile"]["program_family"], "NHLBI R21")
        self.assertEqual(summary["project_profile"]["critique_policy_id"], "nih_r21_significance_innovation_v1")
        self.assertEqual(
            summary["project_profile"]["grant_family_grammar"]["family_id"],
            "nih_r21_translational_family_v1",
        )
        self.assertEqual(
            summary["project_profile"]["grant_family_grammar"]["governance_entry_points"],
            [
                "grant-quality-scorecard",
                "grant-quality-diff",
                "execute-grant-autonomy-controller",
            ],
        )
        self.assertEqual(
            summary["project_profile"]["grant_family_grammar"]["governance_policy"]["default_tranche"],
            "aims_significance_innovation_loop",
        )
        self.assertEqual(
            summary["project_profile"]["grant_family_grammar"]["governance_policy"]["quality_bar"]["minimum_score"],
            78,
        )
        self.assertEqual(
            summary["project_profile"]["family_grammar_trace"]["family_id"],
            "nih_r21_translational_family_v1",
        )
        self.assertEqual(
            summary["project_profile"]["family_grammar_trace"]["review_grammar"]["review_focus"],
            "significance_and_innovation_weighted_review",
        )
        self.assertEqual(
            summary["project_profile"]["family_grammar_trace"]["governance_policy"]["rollback_bias"]["default_rollback_stage"],
            "fit_alignment",
        )
        self.assertTrue(
            any(
                item["rule_id"] == "rule.project_types"
                and "exploratory_developmental" in item["allowed_values"]
                for item in summary["project_profile"]["family_grammar_trace"]["family_compatibility_hooks"]
            )
        )

    def test_validation_accepts_direction_screening_with_selected_direction_only(self) -> None:
        document = load_workspace_document(DIRECTION_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_rejects_direction_screening_with_only_one_direction_candidate(self) -> None:
        document = load_workspace_document(DIRECTION_EXAMPLE_PATH)
        document["direction_hypotheses"] = [document["direction_hypotheses"][0]]

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("direction_hypotheses", "P2.A 方向阶段必须保留 2 到 5 个 DirectionHypothesis。"),
            messages,
        )

    def test_validation_accepts_question_refinement_with_direction_question_binding_only(self) -> None:
        document = load_workspace_document(QUESTION_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_summary_exposes_direction_question_binding_for_question_refinement(self) -> None:
        document = load_workspace_document(QUESTION_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(summary["lifecycle_stage"], "question_refinement")
        self.assertEqual(summary["current_selection"]["selected_direction_id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["current_selection"]["selected_question_id"], "question-immune-fibrosis")
        self.assertEqual(summary["selected_direction"]["id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["selected_question"]["id"], "question-immune-fibrosis")
        self.assertIsNone(summary["active_argument_chain"])
        self.assertIsNone(summary["active_draft"])
        self.assertIsNone(summary["active_revision_plan"])
        self.assertIsNone(summary["active_critique"])
        self.assertIsNone(summary["active_fit_mapping"])

    def test_validation_accepts_argument_building_with_argument_chain_only(self) -> None:
        document = load_workspace_document(ARGUMENT_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_fit_alignment_with_explicit_fit_mapping_binding(self) -> None:
        document = load_workspace_document(FIT_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_summary_exposes_active_fit_mapping_for_fit_alignment(self) -> None:
        document = load_workspace_document(FIT_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "fit_alignment")
        self.assertEqual(summary["current_selection"]["selected_direction_id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["current_selection"]["selected_question_id"], "question-immune-fibrosis")
        self.assertEqual(summary["current_selection"]["active_fit_mapping_id"], "fit-001")
        self.assertEqual(summary["active_fit_mapping"]["id"], "fit-001")
        self.assertEqual(summary["active_fit_mapping"]["argument_chain_id"], "arg-001")
        self.assertIsNone(summary["active_draft"])

    def test_validation_rejects_fit_alignment_without_active_fit_mapping_binding(self) -> None:
        document = load_workspace_document(FIT_EXAMPLE_PATH)
        document["current_selection"].pop("active_fit_mapping_id")

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("current_selection.active_fit_mapping_id", "fit_alignment 阶段必须显式绑定当前 ApplicantFitMapping。"),
            messages,
        )

    def test_validation_accepts_outline_with_fit_mapping_and_outline_freeze(self) -> None:
        document = load_workspace_document(OUTLINE_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_drafting_with_sections_bound_to_upstream_objects(self) -> None:
        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_summary_exposes_draft_audit_for_drafting(self) -> None:
        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "drafting")
        self.assertEqual(summary["active_draft"]["id"], "draft-v1")
        self.assertEqual(summary["active_draft"]["status"], "draft")
        self.assertEqual(summary["active_draft"]["section_count"], 3)
        self.assertIsNone(summary["active_revision_plan"])
        self.assertIsNone(summary["active_critique"])

    def test_validation_rejects_drafting_without_sections(self) -> None:
        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)
        document["application_drafts"][0]["sections"] = []

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.sections", "drafting 阶段的激活草稿必须包含非空 sections。"),
            messages,
        )

    def test_validation_rejects_drafting_without_selected_question_link_in_sections(self) -> None:
        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)
        for item in document["application_drafts"][0]["sections"]:
            if "linked_object_ids" in item:
                item["linked_object_ids"] = [
                    ref for ref in item["linked_object_ids"] if ref != "question-immune-fibrosis"
                ]

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.sections", "drafting 阶段的激活草稿 sections 必须显式链接当前 ScientificQuestionCard。"),
            messages,
        )

    def test_validation_rejects_outline_without_fit_mapping_link_on_active_draft(self) -> None:
        document = load_workspace_document(OUTLINE_EXAMPLE_PATH)
        for item in document["application_drafts"][0]["outline"]:
            if "linked_object_ids" in item:
                item["linked_object_ids"] = [ref for ref in item["linked_object_ids"] if ref != "fit-001"]

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts", "激活草稿必须显式链接当前问题对应的 ApplicantFitMapping。"),
            messages,
        )

    def test_validation_rejects_question_refinement_without_selected_question_binding(self) -> None:
        document = load_workspace_document(QUESTION_EXAMPLE_PATH)
        document["current_selection"].pop("selected_question_id")

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("current_selection.selected_question_id", "question_refinement 阶段必须显式绑定当前 ScientificQuestionCard。"),
            messages,
        )

    def test_validation_rejects_missing_selected_question_reference(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["current_selection"]["selected_question_id"] = "question-missing"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("current_selection.selected_question_id", "未找到对应的 ScientificQuestionCard。"),
            messages,
        )

    def test_validation_accepts_critique_with_structured_revision_inputs(self) -> None:
        document = load_workspace_document(CRITIQUE_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_major_reframe_critique_workspace(self) -> None:
        document = load_workspace_document(MAJOR_REFRAME_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_ready_for_submission_critique_workspace(self) -> None:
        document = load_workspace_document(READY_FOR_SUBMISSION_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_re_review_critique_with_linked_completed_revision_evidence(self) -> None:
        document = self.build_re_review_workspace()

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_forced_rollback_workspace(self) -> None:
        document = self.build_forced_rollback_workspace()

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_presubmission_frozen_workspace(self) -> None:
        document = self.build_presubmission_frozen_workspace()

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_rejects_critique_with_mismatched_current_scientific_question(self) -> None:
        document = load_workspace_document(CRITIQUE_EXAMPLE_PATH)
        document["mentor_critiques"][0]["current_scientific_question"] = "错误的问题表述"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.current_scientific_question", "激活批注必须锚定当前选中问题的 core_question。"),
            messages,
        )

    def test_validation_rejects_empty_revision_plan_during_critique(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["revision_plans"][0]["items"] = []

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("revision_plans", "critique 阶段必须存在非空 RevisionPlan。"),
            messages,
        )

    def test_validation_rejects_frozen_stage_without_ready_for_submission_verdict(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "frozen"
        document["gates"]["presubmission_frozen"] = True

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.verdict", "frozen 阶段的激活批注 verdict 必须为 ready_for_submission。"),
            messages,
        )

    def test_validation_rejects_revision_stage_with_major_reframe_verdict(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["mentor_critiques"][0]["verdict"] = "major_reframe"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.verdict", "revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。"),
            messages,
        )

    def test_validation_rejects_revision_stage_with_ready_for_submission_verdict(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["mentor_critiques"][0]["verdict"] = "ready_for_submission"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.verdict", "revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。"),
            messages,
        )

    def test_validation_rejects_revision_stage_with_outline_draft_status(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["application_drafts"][0]["status"] = "outline"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "revision 阶段的激活草稿 status 必须为 draft 或 revised。"),
            messages,
        )

    def test_validation_rejects_critique_stage_with_outline_draft_status(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["application_drafts"][0]["status"] = "outline"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "critique 阶段的激活草稿 status 必须为 draft 或 revised。"),
            messages,
        )

    def test_validation_rejects_frozen_stage_without_frozen_draft_status(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "frozen"
        document["gates"]["presubmission_frozen"] = True
        document["mentor_critiques"][0]["verdict"] = "ready_for_submission"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "frozen 阶段的激活草稿 status 必须为 frozen。"),
            messages,
        )

    def test_validation_rejects_minor_revision_with_forced_rollback_stage(self) -> None:
        document = copy.deepcopy(self.build_forced_rollback_workspace())
        document["mentor_critiques"][1]["verdict"] = "minor_revision"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.forced_rollback_stage", "minor_revision 不得携带 forced_rollback_stage。"),
            messages,
        )

    def test_validation_rejects_ready_for_submission_with_forced_rollback_stage(self) -> None:
        document = copy.deepcopy(self.build_forced_rollback_workspace())
        document["mentor_critiques"][1]["verdict"] = "ready_for_submission"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.forced_rollback_stage", "ready_for_submission 不得携带 forced_rollback_stage。"),
            messages,
        )

    def test_validation_rejects_forced_rollback_stage_without_reason(self) -> None:
        document = copy.deepcopy(self.build_forced_rollback_workspace())
        document["mentor_critiques"][1].pop("forced_rollback_reason")

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.forced_rollback_reason", "forced_rollback_stage 存在时必须提供非空 forced_rollback_reason。"),
            messages,
        )

    def test_validation_rejects_major_revision_with_invalid_forced_rollback_target(self) -> None:
        document = copy.deepcopy(self.build_forced_rollback_workspace())
        document["mentor_critiques"][1]["forced_rollback_stage"] = "question_refinement"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.forced_rollback_stage", "verdict=major_revision 时 forced_rollback_stage 只能是 argument_building 或 fit_alignment。"),
            messages,
        )

    def test_validation_rejects_non_frozen_stage_with_presubmission_gate_marked_true(self) -> None:
        document = load_workspace_document(READY_FOR_SUBMISSION_EXAMPLE_PATH)
        document["gates"]["presubmission_frozen"] = True

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("gates.presubmission_frozen", "只有 frozen 阶段才允许将 presubmission_frozen 置为 true。"),
            messages,
        )

    def test_validation_rejects_frozen_stage_without_completed_revision_plan(self) -> None:
        document = self.build_presubmission_frozen_workspace()
        document["revision_plans"][0]["execution_status"] = "planned"
        for field in ("pre_revision_version_label", "post_revision_version_label", "comparison_summary"):
            document["revision_plans"][0].pop(field, None)

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("revision_plans.execution_status", "frozen 阶段的激活 RevisionPlan.execution_status 必须为 completed。"),
            messages,
        )

    def test_validation_rejects_frozen_stage_with_criterion_blocking_issues(self) -> None:
        document = self.build_presubmission_frozen_workspace()
        document["mentor_critiques"][0]["feasibility"]["blocking_issues"] = ["仍缺关键闭环实验。"]

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.feasibility.blocking_issues", "frozen 阶段的 feasibility.blocking_issues 必须为空。"),
            messages,
        )

    def test_validation_accepts_completed_revision_with_explicit_revised_switch(self) -> None:
        document = load_workspace_document(REVISION_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_summary_exposes_revision_audit_for_completed_revision(self) -> None:
        document = load_workspace_document(REVISION_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "revision")
        self.assertEqual(summary["active_draft"]["status"], "revised")
        self.assertEqual(summary["active_draft"]["version_label"], "v0.4")
        self.assertEqual(summary["active_revision_plan"]["execution_status"], "completed")
        self.assertEqual(summary["active_revision_plan"]["pre_revision_version_label"], "v0.3")
        self.assertEqual(summary["active_revision_plan"]["post_revision_version_label"], "v0.4")
        self.assertEqual(summary["active_critique"]["blocking_issue_count"], 1)

    def test_summary_exposes_major_reframe_verdict(self) -> None:
        document = load_workspace_document(MAJOR_REFRAME_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "critique")
        self.assertEqual(summary["active_critique"]["verdict"], "major_reframe")
        self.assertEqual(summary["active_revision_plan"]["item_count"], 1)

    def test_summary_exposes_ready_for_submission_verdict(self) -> None:
        document = load_workspace_document(READY_FOR_SUBMISSION_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "critique")
        self.assertEqual(summary["active_draft"]["status"], "revised")
        self.assertEqual(summary["active_critique"]["verdict"], "ready_for_submission")
        self.assertEqual(summary["active_revision_plan"]["execution_status"], "completed")

    def test_summary_exposes_forced_rollback_fields(self) -> None:
        document = self.build_forced_rollback_workspace()

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "critique")
        self.assertFalse(summary["gates"]["presubmission_frozen"])
        self.assertEqual(summary["active_critique"]["id"], "critique-v2")
        self.assertEqual(summary["active_critique"]["forced_rollback_stage"], "argument_building")
        self.assertEqual(summary["active_critique"]["forced_rollback_reason"], "当前必要性链条已经失真，必须回到 argument chain 重建。")

    def test_summary_exposes_presubmission_frozen_gate(self) -> None:
        document = self.build_presubmission_frozen_workspace()

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "frozen")
        self.assertTrue(summary["gates"]["presubmission_frozen"])
        self.assertEqual(summary["active_draft"]["status"], "frozen")
        self.assertEqual(summary["active_revision_plan"]["execution_status"], "completed")
        self.assertEqual(summary["active_critique"]["verdict"], "ready_for_submission")

    def test_summary_exposes_re_review_linkage_and_previous_revision_evidence(self) -> None:
        document = self.build_re_review_workspace()

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["lifecycle_stage"], "critique")
        self.assertEqual(summary["active_draft"]["status"], "revised")
        self.assertEqual(summary["active_critique"]["id"], "critique-v2")
        self.assertEqual(summary["active_critique"]["verdict"], "major_revision")
        self.assertEqual(summary["active_critique"]["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(summary["active_revision_plan"]["id"], "revision-v2")
        self.assertEqual(summary["active_revision_plan"]["execution_status"], "planned")
        self.assertEqual(summary["reviewed_revision_evidence"]["revision_plan_id"], "revision-v1")
        self.assertEqual(summary["reviewed_revision_evidence"]["post_revision_version_label"], "v0.4")

    def test_validation_rejects_completed_revision_without_revised_status_switch(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["revision_plans"][0]["execution_status"] = "completed"
        document["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        document["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        document["revision_plans"][0]["comparison_summary"] = "已根据 major_revision 完成修订。"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "revision plan 已标记 completed 时，激活草稿 status 必须显式切换为 revised。"),
            messages,
        )

    def test_validation_rejects_revised_status_without_completed_revision_evidence(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["application_drafts"][0]["status"] = "revised"
        document["application_drafts"][0]["version_label"] = "v0.4"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("revision_plans.execution_status", "激活草稿 status=revised 时，RevisionPlan.execution_status 必须为 completed。"),
            messages,
        )

if __name__ == "__main__":
    unittest.main()
