from __future__ import annotations

import copy
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
    def load_example(self, path: Path = EXAMPLE_PATH) -> dict[str, object]:
        return load_workspace_document(path)

    def summarize_example(self, path: Path) -> dict[str, object]:
        return summarize_workspace_document(self.load_example(path))

    def assert_paths(self, actual: dict[str, object], expected: dict[object, object]) -> None:
        for path, value in expected.items():
            current: object = actual
            for part in path if isinstance(path, tuple) else str(path).split("."):
                current = current[part]
            self.assertEqual(current, value, path)

    def assert_validation_ok(self, document: dict[str, object]) -> None:
        result = validate_workspace_document(document)
        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def assert_validation_error(self, document: dict[str, object], expected: tuple[str, str]) -> None:
        result = validate_workspace_document(document)
        self.assertFalse(result.ok)
        self.assertIn(expected, {(item.path, item.message) for item in result.errors})

    def test_summary_exposes_key_fields(self) -> None:
        cases = (
            (
                "minimal",
                EXAMPLE_PATH,
                {
                    "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    "workspace_id": "nsfc-demo-001",
                    "mode": "auto",
                    "lifecycle_stage": "critique",
                    "selected_direction.id": "dir-inflammatory-remodeling",
                    "selected_question.id": "question-immune-fibrosis",
                    "active_fit_mapping.id": "fit-001",
                    "active_draft.id": "draft-v1",
                    "active_revision_plan.id": "revision-v1",
                    "active_critique.id": "critique-v1",
                },
            ),
            (
                "input_intake",
                INPUT_EXAMPLE_PATH,
                {
                    "project_profile.profile_id": "profile-nsfc-general-medical",
                    "project_profile.preset_id": "nsfc_general_medical_v1",
                    "project_profile.template_id": "nsfc_general_grant_template_v1",
                    "project_profile.collaboration_mode": "applicant_led_agent_copilot",
                    "project_profile.critique_policy_id": "nsfc_mentor_critique_v1",
                    "grant_intake_audit.audit_kind": "grant_intake_audit",
                    "grant_intake_audit.surface_kind": "grant_intake_audit",
                    "grant_intake_audit.applicant_profile_id": "applicant-gaofeng",
                    "grant_intake_audit.project_profile_id": "profile-nsfc-general-medical",
                    "grant_intake_audit.overall_readiness": "ready_for_direction_screening",
                    "grant_intake_audit.blocking_gaps": [],
                    "grant_intake_audit.trust_summary.trusted": 2,
                    "grant_intake_audit.trust_summary.usable_with_verification": 1,
                    "grant_intake_audit.project_profile_summary.critique_policy_id": "nsfc_mentor_critique_v1",
                    "grant_intake_audit.readiness.ready_for_direction_screening": True,
                    "grant_intake_audit.readiness.project_profile_ready": True,
                    "grant_evidence_grounding.grounding_kind": "grant_evidence_grounding",
                    "grant_evidence_grounding.surface_kind": "grant_evidence_grounding",
                    "grant_evidence_grounding.grounding_status": "intake_grounded",
                    "grant_evidence_grounding.evidence_gaps": [],
                    "grant_evidence_grounding.ready_for_direction_screening": True,
                    "grant_evidence_grounding.project_profile_summary.template_id": "nsfc_general_grant_template_v1",
                    "grant_evidence_grounding.project_profile_summary.collaboration_mode": "applicant_led_agent_copilot",
                    "grant_evidence_grounding.evidence_inventory.primary_evidence_ids": ["evi-output-1", "evi-prelim-1", "evi-project-1"],
                    ("grant_evidence_grounding", "trust_ranked_evidence", 0, "supports"): ["applicant_fit", "scientific_question", "technical_route"],
                },
            ),
            (
                "non_nsfc_input_intake",
                NON_NSFC_INPUT_EXAMPLE_PATH,
                {
                    "project_profile.preset_id": "nih_r21_translational_v1",
                    "project_profile.funder": "NIH",
                    "project_profile.program_family": "NHLBI R21",
                    "project_profile.critique_policy_id": "nih_r21_significance_innovation_v1",
                    "project_profile.grant_family_grammar.family_id": "nih_r21_translational_family_v1",
                    "project_profile.grant_family_grammar.governance_entry_points": [
                        "grant-quality-scorecard",
                        "grant-quality-diff",
                        "execute-grant-autonomy-controller",
                    ],
                    "project_profile.grant_family_grammar.governance_policy.default_tranche": "aims_significance_innovation_loop",
                    "project_profile.grant_family_grammar.governance_policy.quality_bar.minimum_score": 78,
                    "project_profile.grant_family_grammar.governance_policy.controller_defaults.target_status": "near_submission_candidate",
                    "project_profile.family_grammar_trace.family_id": "nih_r21_translational_family_v1",
                    "project_profile.family_grammar_trace.review_grammar.review_focus": "significance_and_innovation_weighted_review",
                    "project_profile.family_grammar_trace.governance_policy.rollback_bias.default_rollback_stage": "fit_alignment",
                },
            ),
        )
        for label, path, expected in cases:
            with self.subTest(case=label):
                self.assert_paths(self.summarize_example(path), expected)

        input_summary = self.summarize_example(INPUT_EXAMPLE_PATH)
        self.assertEqual(
            [section["section_id"] for section in input_summary["grant_intake_audit"]["intake_sections"]],
            ["applicant_profile", "project_profile", "track_record", "active_project_set", "preliminary_evidence_pack", "funding_opportunity_brief"],
        )
        self.assertEqual(
            [item["trust_level"] for item in input_summary["grant_evidence_grounding"]["trust_ranked_evidence"]],
            ["trusted", "trusted", "usable_with_verification"],
        )

        non_nsfc_trace = self.summarize_example(NON_NSFC_INPUT_EXAMPLE_PATH)["project_profile"]["family_grammar_trace"]
        self.assertTrue(
            any(
                item["rule_id"] == "rule.project_types"
                and "exploratory_developmental" in item["allowed_values"]
                for item in non_nsfc_trace["family_compatibility_hooks"]
            )
        )

    def test_validation_accepts_stage_fixture_workspaces(self) -> None:
        paths = (
            INPUT_EXAMPLE_PATH, NON_NSFC_INPUT_EXAMPLE_PATH, DIRECTION_EXAMPLE_PATH, QUESTION_EXAMPLE_PATH,
            ARGUMENT_EXAMPLE_PATH, FIT_EXAMPLE_PATH, OUTLINE_EXAMPLE_PATH, DRAFTING_EXAMPLE_PATH,
            CRITIQUE_EXAMPLE_PATH, MAJOR_REFRAME_EXAMPLE_PATH, READY_FOR_SUBMISSION_EXAMPLE_PATH,
            REVISION_EXAMPLE_PATH, RE_REVIEW_EXAMPLE_PATH, FORCED_ROLLBACK_EXAMPLE_PATH,
            PRESUBMISSION_FROZEN_EXAMPLE_PATH,
        )
        for path in paths:
            with self.subTest(path=path.name):
                self.assert_validation_ok(self.load_example(path))

    def test_validation_rejects_stage_invariants(self) -> None:
        def remove_draft_question_links(document: dict[str, object]) -> None:
            for item in document["application_drafts"][0]["sections"]:
                if "linked_object_ids" in item:
                    item["linked_object_ids"] = [
                        ref for ref in item["linked_object_ids"] if ref != "question-immune-fibrosis"
                    ]

        def remove_outline_fit_links(document: dict[str, object]) -> None:
            for item in document["application_drafts"][0]["outline"]:
                if "linked_object_ids" in item:
                    item["linked_object_ids"] = [ref for ref in item["linked_object_ids"] if ref != "fit-001"]

        def mark_frozen_without_completed_revision(document: dict[str, object]) -> None:
            document["revision_plans"][0]["execution_status"] = "planned"
            for field in ("pre_revision_version_label", "post_revision_version_label", "comparison_summary"):
                document["revision_plans"][0].pop(field, None)

        def mark_completed_revision_without_revised_draft(document: dict[str, object]) -> None:
            document["lifecycle_stage"] = "revision"
            document["revision_plans"][0]["execution_status"] = "completed"
            document["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
            document["revision_plans"][0]["post_revision_version_label"] = "v0.4"
            document["revision_plans"][0]["comparison_summary"] = "已根据 major_revision 完成修订。"

        cases = (
            (
                "direction_screening_min_candidates",
                DIRECTION_EXAMPLE_PATH,
                lambda document: document.__setitem__("direction_hypotheses", [document["direction_hypotheses"][0]]),
                ("direction_hypotheses", "P2.A 方向阶段必须保留 2 到 5 个 DirectionHypothesis。"),
            ),
            (
                "fit_alignment_active_mapping",
                FIT_EXAMPLE_PATH,
                lambda document: document["current_selection"].pop("active_fit_mapping_id"),
                ("current_selection.active_fit_mapping_id", "fit_alignment 阶段必须显式绑定当前 ApplicantFitMapping。"),
            ),
            (
                "drafting_sections",
                DRAFTING_EXAMPLE_PATH,
                lambda document: document["application_drafts"][0].__setitem__("sections", []),
                ("application_drafts.sections", "drafting 阶段的激活草稿必须包含非空 sections。"),
            ),
            (
                "drafting_selected_question_links",
                DRAFTING_EXAMPLE_PATH,
                remove_draft_question_links,
                ("application_drafts.sections", "drafting 阶段的激活草稿 sections 必须显式链接当前 ScientificQuestionCard。"),
            ),
            (
                "outline_fit_links",
                OUTLINE_EXAMPLE_PATH,
                remove_outline_fit_links,
                ("application_drafts", "激活草稿必须显式链接当前问题对应的 ApplicantFitMapping。"),
            ),
            (
                "question_refinement_binding",
                QUESTION_EXAMPLE_PATH,
                lambda document: document["current_selection"].pop("selected_question_id"),
                ("current_selection.selected_question_id", "question_refinement 阶段必须显式绑定当前 ScientificQuestionCard。"),
            ),
            (
                "missing_selected_question_reference",
                EXAMPLE_PATH,
                lambda document: document["current_selection"].__setitem__("selected_question_id", "question-missing"),
                ("current_selection.selected_question_id", "未找到对应的 ScientificQuestionCard。"),
            ),
            (
                "critique_current_question",
                CRITIQUE_EXAMPLE_PATH,
                lambda document: document["mentor_critiques"][0].__setitem__("current_scientific_question", "错误的问题表述"),
                ("mentor_critiques.current_scientific_question", "激活批注必须锚定当前选中问题的 core_question。"),
            ),
            (
                "critique_revision_plan_items",
                EXAMPLE_PATH,
                lambda document: document["revision_plans"][0].__setitem__("items", []),
                ("revision_plans", "critique 阶段必须存在非空 RevisionPlan。"),
            ),
            (
                "frozen_ready_verdict",
                EXAMPLE_PATH,
                lambda document: (
                    document.__setitem__("lifecycle_stage", "frozen"),
                    document["gates"].__setitem__("presubmission_frozen", True),
                ),
                ("mentor_critiques.verdict", "frozen 阶段的激活批注 verdict 必须为 ready_for_submission。"),
            ),
            (
                "frozen_draft_status",
                EXAMPLE_PATH,
                lambda document: (
                    document.__setitem__("lifecycle_stage", "frozen"),
                    document["gates"].__setitem__("presubmission_frozen", True),
                    document["mentor_critiques"][0].__setitem__("verdict", "ready_for_submission"),
                ),
                ("application_drafts.status", "frozen 阶段的激活草稿 status 必须为 frozen。"),
            ),
            (
                "forced_rollback_reason",
                FORCED_ROLLBACK_EXAMPLE_PATH,
                lambda document: document["mentor_critiques"][1].pop("forced_rollback_reason"),
                ("mentor_critiques.forced_rollback_reason", "forced_rollback_stage 存在时必须提供非空 forced_rollback_reason。"),
            ),
            (
                "forced_rollback_target",
                FORCED_ROLLBACK_EXAMPLE_PATH,
                lambda document: document["mentor_critiques"][1].__setitem__("forced_rollback_stage", "question_refinement"),
                ("mentor_critiques.forced_rollback_stage", "verdict=major_revision 时 forced_rollback_stage 只能是 argument_building 或 fit_alignment。"),
            ),
            (
                "non_frozen_presubmission_gate",
                READY_FOR_SUBMISSION_EXAMPLE_PATH,
                lambda document: document["gates"].__setitem__("presubmission_frozen", True),
                ("gates.presubmission_frozen", "只有 frozen 阶段才允许将 presubmission_frozen 置为 true。"),
            ),
            (
                "frozen_completed_revision",
                PRESUBMISSION_FROZEN_EXAMPLE_PATH,
                mark_frozen_without_completed_revision,
                ("revision_plans.execution_status", "frozen 阶段的激活 RevisionPlan.execution_status 必须为 completed。"),
            ),
            (
                "frozen_blocking_issues",
                PRESUBMISSION_FROZEN_EXAMPLE_PATH,
                lambda document: document["mentor_critiques"][0]["feasibility"].__setitem__(
                    "blocking_issues", ["仍缺关键闭环实验。"]
                ),
                ("mentor_critiques.feasibility.blocking_issues", "frozen 阶段的 feasibility.blocking_issues 必须为空。"),
            ),
            (
                "completed_revision_requires_revised_draft",
                EXAMPLE_PATH,
                mark_completed_revision_without_revised_draft,
                ("application_drafts.status", "revision plan 已标记 completed 时，激活草稿 status 必须显式切换为 revised。"),
            ),
            (
                "revised_draft_requires_completed_revision",
                EXAMPLE_PATH,
                lambda document: (
                    document.__setitem__("lifecycle_stage", "revision"),
                    document["application_drafts"][0].__setitem__("status", "revised"),
                    document["application_drafts"][0].__setitem__("version_label", "v0.4"),
                ),
                ("revision_plans.execution_status", "激活草稿 status=revised 时，RevisionPlan.execution_status 必须为 completed。"),
            ),
            (
                "revision_major_reframe_verdict",
                EXAMPLE_PATH,
                lambda document: (
                    document.__setitem__("lifecycle_stage", "revision"),
                    document["mentor_critiques"][0].__setitem__("verdict", "major_reframe"),
                ),
                ("mentor_critiques.verdict", "revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。"),
            ),
            (
                "revision_ready_for_submission_verdict",
                EXAMPLE_PATH,
                lambda document: (
                    document.__setitem__("lifecycle_stage", "revision"),
                    document["mentor_critiques"][0].__setitem__("verdict", "ready_for_submission"),
                ),
                ("mentor_critiques.verdict", "revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。"),
            ),
            (
                "revision_outline_draft_status",
                EXAMPLE_PATH,
                lambda document: (
                    document.__setitem__("lifecycle_stage", "revision"),
                    document["application_drafts"][0].__setitem__("status", "outline"),
                ),
                ("application_drafts.status", "revision 阶段的激活草稿 status 必须为 draft 或 revised。"),
            ),
            (
                "critique_outline_draft_status",
                EXAMPLE_PATH,
                lambda document: (
                    document.__setitem__("lifecycle_stage", "critique"),
                    document["application_drafts"][0].__setitem__("status", "outline"),
                ),
                ("application_drafts.status", "critique 阶段的激活草稿 status 必须为 draft 或 revised。"),
            ),
            (
                "minor_revision_forced_rollback_stage",
                FORCED_ROLLBACK_EXAMPLE_PATH,
                lambda document: document["mentor_critiques"][1].__setitem__("verdict", "minor_revision"),
                ("mentor_critiques.forced_rollback_stage", "minor_revision 不得携带 forced_rollback_stage。"),
            ),
            (
                "ready_for_submission_forced_rollback_stage",
                FORCED_ROLLBACK_EXAMPLE_PATH,
                lambda document: document["mentor_critiques"][1].__setitem__("verdict", "ready_for_submission"),
                ("mentor_critiques.forced_rollback_stage", "ready_for_submission 不得携带 forced_rollback_stage。"),
            ),
        )
        for label, path, mutate, expected in cases:
            with self.subTest(case=label):
                document = copy.deepcopy(self.load_example(path))
                mutate(document)
                self.assert_validation_error(document, expected)

    def test_summary_exposes_stage_and_review_fields(self) -> None:
        cases = (
            (
                "question_refinement",
                QUESTION_EXAMPLE_PATH,
                {"grant_run_id": "grant-run-nsfc-demo-001-baseline-001", "lifecycle_stage": "question_refinement", "current_selection.selected_question_id": "question-immune-fibrosis", "selected_question.id": "question-immune-fibrosis", "active_draft": None},
            ),
            (
                "fit_alignment",
                FIT_EXAMPLE_PATH,
                {"lifecycle_stage": "fit_alignment", "current_selection.active_fit_mapping_id": "fit-001", "active_fit_mapping.id": "fit-001", "active_draft": None},
            ),
            (
                "drafting",
                DRAFTING_EXAMPLE_PATH,
                {"lifecycle_stage": "drafting", "active_draft.status": "draft", "active_draft.section_count": 3},
            ),
            (
                "completed_revision",
                REVISION_EXAMPLE_PATH,
                {"lifecycle_stage": "revision", "active_draft.status": "revised", "active_draft.version_label": "v0.4", "active_revision_plan.execution_status": "completed"},
            ),
            (
                "major_reframe",
                MAJOR_REFRAME_EXAMPLE_PATH,
                {"lifecycle_stage": "critique", "active_critique.verdict": "major_reframe"},
            ),
            (
                "ready_for_submission",
                READY_FOR_SUBMISSION_EXAMPLE_PATH,
                {"lifecycle_stage": "critique", "active_critique.verdict": "ready_for_submission", "active_revision_plan.execution_status": "completed"},
            ),
            (
                "forced_rollback",
                FORCED_ROLLBACK_EXAMPLE_PATH,
                {"lifecycle_stage": "critique", "gates.presubmission_frozen": False, "active_critique.forced_rollback_stage": "argument_building"},
            ),
            (
                "presubmission_frozen",
                PRESUBMISSION_FROZEN_EXAMPLE_PATH,
                {"lifecycle_stage": "frozen", "gates.presubmission_frozen": True, "active_draft.status": "frozen", "active_critique.verdict": "ready_for_submission"},
            ),
            (
                "re_review",
                RE_REVIEW_EXAMPLE_PATH,
                {"lifecycle_stage": "critique", "active_critique.verdict": "major_revision", "active_critique.reviewed_revision_plan_id": "revision-v1", "active_revision_plan.id": "revision-v2", "reviewed_revision_evidence.revision_plan_id": "revision-v1"},
            ),
        )
        for label, path, expected in cases:
            with self.subTest(case=label):
                self.assert_paths(self.summarize_example(path), expected)

if __name__ == "__main__":
    unittest.main()
