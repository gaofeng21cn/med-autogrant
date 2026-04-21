from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

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


INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"
QUESTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_question_refinement.json"
ARGUMENT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_argument_building.json"
FIT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_fit_alignment.json"
OUTLINE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_outline.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"


class AuthoringExecutorTest(unittest.TestCase):
    def test_direction_screening_builds_workspace_and_clears_downstream_state(self) -> None:
        document = self._load_workspace(INPUT_EXAMPLE_PATH)
        stale_downstream = self._load_workspace(CRITIQUE_EXAMPLE_PATH)
        document["scientific_question_cards"] = copy.deepcopy(stale_downstream["scientific_question_cards"])
        document["argument_chains"] = copy.deepcopy(stale_downstream["argument_chains"])
        document["applicant_fit_mappings"] = copy.deepcopy(stale_downstream["applicant_fit_mappings"])
        document["application_drafts"] = copy.deepcopy(stale_downstream["application_drafts"])
        document["mentor_critiques"] = copy.deepcopy(stale_downstream["mentor_critiques"])
        document["revision_plans"] = copy.deepcopy(stale_downstream["revision_plans"])

        payload = build_direction_screening_execution_document(
            document=document,
            input_path=INPUT_EXAMPLE_PATH,
            codex_runner=self._runner(
                {
                    "selected_direction_index": 1,
                    "direction_hypotheses": [
                        {
                            "title": "心梗后炎症分辨失败驱动致纤维化记忆",
                            "rationale": "先从炎症分辨失败这一主轴重看心梗后纤维化时序。",
                            "knowledge_gap_summary": "尚不清楚炎症分辨失败如何锁定成纤维细胞致纤维化程序。",
                            "applicant_fit_summary": "申请人已有心梗后免疫时序与纤维化基础。",
                            "novelty_angle": "把炎症分辨时窗与跨细胞通讯主线并到一个机制问题里。",
                            "risk_summary": "时窗界定需要稳定动物模型支持。",
                            "required_evidence_ids": [],
                        },
                        {
                            "title": "巨噬细胞-成纤维细胞跨细胞通讯调控心肌纤维化重塑",
                            "rationale": "聚焦巨噬细胞对成纤维细胞重编程的关键通讯轴。",
                            "knowledge_gap_summary": "缺少特定时间窗内关键通讯节点到致纤维化表型的机制闭环。",
                            "applicant_fit_summary": "申请人已有免疫互作和心肌纤维化前期证据。",
                            "novelty_angle": "把单细胞热点自然吸收到机制验证主线中。",
                            "risk_summary": "通讯轴候选需先缩窄。",
                            "required_evidence_ids": [],
                        },
                    ],
                },
                expected_input_path=INPUT_EXAMPLE_PATH,
            ),
        )

        workspace = payload["direction_screening_workspace"]
        self.assertEqual(payload["lifecycle_stage"], "direction_screening")
        self.assertEqual(workspace["current_selection"]["selected_direction_id"], "direction-v2")
        self.assertEqual(len(workspace["direction_hypotheses"]), 2)
        self.assertEqual(workspace["direction_hypotheses"][1]["decision_status"], "selected")
        self.assertEqual(workspace["scientific_question_cards"], [])
        self.assertEqual(workspace["argument_chains"], [])
        self.assertEqual(workspace["applicant_fit_mappings"], [])
        self.assertEqual(workspace["application_drafts"], [])
        self.assertEqual(workspace["mentor_critiques"], [])
        self.assertEqual(workspace["revision_plans"], [])
        self.assertEqual(workspace["grant_intake_audit"]["audit_kind"], "grant_intake_audit")
        self.assertEqual(
            workspace["grant_evidence_grounding"]["selection_context"]["selected_direction_id"],
            "direction-v2",
        )
        self.assert_workspace_valid(workspace, "direction_screening")

    def test_question_refinement_builds_question_and_clears_downstream_state(self) -> None:
        document = self._load_workspace(QUESTION_EXAMPLE_PATH)
        stale_downstream = self._load_workspace(CRITIQUE_EXAMPLE_PATH)
        document["lifecycle_stage"] = "direction_screening"
        document["gates"] = {
            "direction_frozen": True,
            "scientific_question_frozen": False,
            "argument_chain_frozen": False,
            "fit_alignment_frozen": False,
            "outline_frozen": False,
            "presubmission_frozen": False,
        }
        document["current_selection"] = {
            "selected_direction_id": document["current_selection"]["selected_direction_id"],
        }
        document["argument_chains"] = copy.deepcopy(stale_downstream["argument_chains"])
        document["applicant_fit_mappings"] = copy.deepcopy(stale_downstream["applicant_fit_mappings"])
        document["application_drafts"] = copy.deepcopy(stale_downstream["application_drafts"])
        document["mentor_critiques"] = copy.deepcopy(stale_downstream["mentor_critiques"])
        document["revision_plans"] = copy.deepcopy(stale_downstream["revision_plans"])

        payload = build_question_refinement_execution_document(
            document=document,
            input_path=QUESTION_EXAMPLE_PATH,
            codex_runner=self._runner(
                {
                    "scientific_question_card": {
                        "phenomenon": "心梗后特定时窗成纤维细胞出现持续致纤维化重编程。",
                        "knowledge_boundary": "限定在心梗后炎症巨噬细胞对成纤维细胞的跨细胞通讯机制。",
                        "unknown_mechanism": "尚不清楚哪条关键信号轴在特定时窗锁定成纤维化程序。",
                        "core_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                        "subquestions": ["关键配体-受体轴是什么", "时窗依赖性如何形成"],
                        "falsifiable_statement": "若阻断关键通讯轴，则该时窗内成纤维细胞致纤维化重编程会被显著削弱。",
                        "proposed_breakthrough_angle": "把炎症时窗与跨细胞通讯锁定到单一可验证机制轴。",
                        "why_not_engineering": "问题核心在于机制识别与因果闭环，而非单纯优化检测或干预流程。",
                        "why_now": "申请人已有前期证据足以缩窄候选通讯轴。",
                        "linked_evidence_ids": [],
                    },
                },
                expected_input_path=QUESTION_EXAMPLE_PATH,
            ),
        )

        workspace = payload["question_refinement_workspace"]
        self.assertEqual(payload["lifecycle_stage"], "question_refinement")
        self.assertEqual(workspace["current_selection"]["selected_direction_id"], document["current_selection"]["selected_direction_id"])
        self.assertEqual(workspace["current_selection"]["selected_question_id"], "question-v1")
        self.assertEqual(workspace["argument_chains"], [])
        self.assertEqual(workspace["applicant_fit_mappings"], [])
        self.assertEqual(workspace["application_drafts"], [])
        self.assertEqual(workspace["mentor_critiques"], [])
        self.assertEqual(workspace["revision_plans"], [])
        self.assert_workspace_valid(workspace, "question_refinement")

    def test_argument_building_builds_argument_chain_and_clears_lower_outputs(self) -> None:
        document = self._load_workspace(QUESTION_EXAMPLE_PATH)
        stale_downstream = self._load_workspace(CRITIQUE_EXAMPLE_PATH)
        document["argument_chains"] = copy.deepcopy(stale_downstream["argument_chains"])
        document["applicant_fit_mappings"] = copy.deepcopy(stale_downstream["applicant_fit_mappings"])
        document["application_drafts"] = copy.deepcopy(stale_downstream["application_drafts"])
        document["mentor_critiques"] = copy.deepcopy(stale_downstream["mentor_critiques"])
        document["revision_plans"] = copy.deepcopy(stale_downstream["revision_plans"])

        payload = build_argument_building_execution_document(
            document=document,
            input_path=QUESTION_EXAMPLE_PATH,
            codex_runner=self._runner(
                {
                    "argument_chain": {
                        "background_claim": "心梗后炎症期的细胞互作决定后续纤维化重塑走向。",
                        "field_gap": "现有研究缺少对特定时间窗关键通讯轴的机制级闭环。",
                        "necessity_claim": "若不锁定该通讯轴，难以解释为什么部分患者进入不可逆纤维化。",
                        "uniqueness_claim": "申请人的前期模型和证据能把该问题从现象推进到因果机制。",
                        "route_justification": "先界定时窗，再锁定通讯轴，最后做因果阻断验证，形成非任意主线。",
                        "non_arbitrary_route_reason": "该顺序直接对应问题中的时间窗、通讯轴与致纤维化结果。",
                        "if_not_done_loss": "将继续停留在表型相关层面，难以支撑机制级基金申请。",
                        "linked_evidence_ids": [],
                    },
                },
                expected_input_path=QUESTION_EXAMPLE_PATH,
            ),
        )

        workspace = payload["argument_building_workspace"]
        self.assertEqual(payload["lifecycle_stage"], "argument_building")
        self.assertEqual(workspace["current_selection"]["selected_question_id"], document["current_selection"]["selected_question_id"])
        self.assertEqual(len(workspace["argument_chains"]), 1)
        self.assertEqual(workspace["applicant_fit_mappings"], [])
        self.assertEqual(workspace["application_drafts"], [])
        self.assertEqual(workspace["mentor_critiques"], [])
        self.assertEqual(workspace["revision_plans"], [])
        self.assert_workspace_valid(workspace, "argument_building")

    def test_fit_alignment_builds_fit_mapping_and_clears_draft_review_outputs(self) -> None:
        document = self._load_workspace(CRITIQUE_EXAMPLE_PATH)
        document["lifecycle_stage"] = "argument_building"
        document["gates"] = {
            "direction_frozen": True,
            "scientific_question_frozen": True,
            "argument_chain_frozen": True,
            "fit_alignment_frozen": False,
            "outline_frozen": False,
            "presubmission_frozen": False,
        }
        document["current_selection"] = {
            "selected_direction_id": document["current_selection"]["selected_direction_id"],
            "selected_question_id": document["current_selection"]["selected_question_id"],
        }

        payload = build_fit_alignment_execution_document(
            document=document,
            input_path=CRITIQUE_EXAMPLE_PATH,
            codex_runner=self._runner(
                {
                    "applicant_fit_mapping": {
                        "applicant_fit_summary": "申请人已有心梗后免疫时序、单细胞解析和纤维化模型基础。",
                        "unique_advantage": "能把已有单细胞线索直接压缩到候选通讯轴并做因果验证。",
                        "methods_readiness": "具备免疫细胞操控、时窗采样和成纤维细胞表型验证手段。",
                        "resource_readiness": "已有临床样本协作与稳定动物模型平台。",
                        "risk_mitigation": "若首选通讯轴不稳，可按前期证据的优先级切换备选轴。",
                        "linked_evidence_ids": [],
                    },
                },
                expected_input_path=CRITIQUE_EXAMPLE_PATH,
            ),
        )

        workspace = payload["fit_alignment_workspace"]
        self.assertEqual(payload["lifecycle_stage"], "fit_alignment")
        self.assertEqual(len(workspace["applicant_fit_mappings"]), 1)
        self.assertEqual(workspace["application_drafts"], [])
        self.assertEqual(workspace["mentor_critiques"], [])
        self.assertEqual(workspace["revision_plans"], [])
        self.assert_workspace_valid(workspace, "fit_alignment")

    def test_outline_builds_outline_and_clears_review_outputs(self) -> None:
        document = self._load_workspace(CRITIQUE_EXAMPLE_PATH)
        document["lifecycle_stage"] = "fit_alignment"
        document["gates"] = {
            "direction_frozen": True,
            "scientific_question_frozen": True,
            "argument_chain_frozen": True,
            "fit_alignment_frozen": True,
            "outline_frozen": False,
            "presubmission_frozen": False,
        }
        document["current_selection"] = {
            "selected_direction_id": document["current_selection"]["selected_direction_id"],
            "selected_question_id": document["current_selection"]["selected_question_id"],
            "active_fit_mapping_id": document["current_selection"]["active_fit_mapping_id"],
        }

        payload = build_outline_execution_document(
            document=document,
            input_path=CRITIQUE_EXAMPLE_PATH,
            codex_runner=self._runner(
                {
                    "application_draft": {
                        "project_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                        "outline": [
                            {
                                "section_key": "significance",
                                "section_title": "立项依据与科学意义",
                                "core_claim": "该问题决定我们能否解释心梗后致纤维化重塑的关键转折。",
                                "linked_object_ids": ["question-immune-fibrosis", "arg-001", "fit-001"],
                            },
                            {
                                "section_key": "plan",
                                "section_title": "研究内容与技术路线",
                                "core_claim": "围绕时间窗、通讯轴和因果阻断构建研究主线。",
                                "linked_object_ids": ["question-immune-fibrosis", "arg-001", "fit-001"],
                            },
                        ],
                    },
                },
                expected_input_path=CRITIQUE_EXAMPLE_PATH,
            ),
        )

        workspace = payload["outline_workspace"]
        active_draft = workspace["application_drafts"][0]
        self.assertEqual(payload["lifecycle_stage"], "outline")
        self.assertEqual(active_draft["status"], "outline")
        self.assertEqual(active_draft["sections"], [])
        self.assertEqual(workspace["mentor_critiques"], [])
        self.assertEqual(workspace["revision_plans"], [])
        self.assert_workspace_valid(workspace, "outline")

    def test_drafting_builds_sections_and_clears_review_outputs(self) -> None:
        document = self._load_workspace(CRITIQUE_EXAMPLE_PATH)
        document["lifecycle_stage"] = "outline"
        document["gates"] = {
            "direction_frozen": True,
            "scientific_question_frozen": True,
            "argument_chain_frozen": True,
            "fit_alignment_frozen": True,
            "outline_frozen": True,
            "presubmission_frozen": False,
        }
        document["current_selection"] = {
            "selected_direction_id": document["current_selection"]["selected_direction_id"],
            "selected_question_id": document["current_selection"]["selected_question_id"],
            "active_fit_mapping_id": document["current_selection"]["active_fit_mapping_id"],
            "active_draft_id": document["current_selection"]["active_draft_id"],
        }
        document["application_drafts"][0]["status"] = "outline"
        document["application_drafts"][0]["sections"] = []

        payload = build_drafting_execution_document(
            document=document,
            input_path=CRITIQUE_EXAMPLE_PATH,
            codex_runner=self._runner(
                {
                    "application_draft": {
                        "project_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                        "sections": [
                            {
                                "section_key": "basis",
                                "section_title": "立项依据",
                                "text": "我们前期观察到心梗后炎症巨噬细胞与成纤维细胞之间存在时间窗受限的通讯增强现象。",
                                "linked_object_ids": ["question-immune-fibrosis", "arg-001", "fit-001"],
                            },
                            {
                                "section_key": "content",
                                "section_title": "研究内容",
                                "text": "将围绕时间窗界定、候选通讯轴锁定与因果阻断验证三个层次展开。",
                                "linked_object_ids": ["question-immune-fibrosis", "arg-001", "fit-001"],
                            },
                        ],
                    },
                },
                expected_input_path=CRITIQUE_EXAMPLE_PATH,
            ),
        )

        workspace = payload["drafting_workspace"]
        active_draft = workspace["application_drafts"][0]
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(active_draft["status"], "draft")
        self.assertEqual(len(active_draft["sections"]), 2)
        self.assertEqual(workspace["mentor_critiques"], [])
        self.assertEqual(workspace["revision_plans"], [])
        self.assert_workspace_valid(workspace, "drafting")

    def test_freeze_pass_closes_presubmission_gate_and_marks_active_draft_frozen(self) -> None:
        document = self._load_workspace(READY_FOR_SUBMISSION_EXAMPLE_PATH)

        payload = build_freeze_execution_document(document=document)

        workspace = payload["frozen_workspace"]
        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertTrue(workspace["gates"]["presubmission_frozen"])
        self.assertEqual(workspace["application_drafts"][0]["status"], "frozen")
        self.assertEqual(payload["freeze_execution"]["executor"]["kind"], "deterministic_domain_logic")
        self.assert_workspace_valid(workspace, "frozen")

    def _load_workspace(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _runner(self, payload: dict[str, Any], *, expected_input_path: Path):
        def run(prompt: str, *, cwd: Path) -> dict[str, Any]:
            self.assertIn(str(expected_input_path.resolve()), prompt)
            self.assertEqual(cwd, expected_input_path.resolve().parent)
            return copy.deepcopy(payload)

        return run

    def assert_workspace_valid(self, document: dict[str, Any], expected_stage: str) -> None:
        self.assertEqual(document["lifecycle_stage"], expected_stage)
        validation = validate_workspace_document(document)
        self.assertTrue(validation.ok, validation.to_dict(document))


if __name__ == "__main__":
    unittest.main()
