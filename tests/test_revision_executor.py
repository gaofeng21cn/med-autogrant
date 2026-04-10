from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.route_report import build_stage_route_report  # noqa: E402
from med_autogrant.workspace import validate_workspace_document  # noqa: E402


P2C_CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
P3B_RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class RevisionExecutorCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(list(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_execute_revision_pass_writes_revised_workspace_from_initial_critique(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "revised-workspace.json"

            exit_code, stdout, stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(P2C_CRITIQUE_EXAMPLE_PATH),
                "--output",
                str(output_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")

            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "execute-revision-pass")
            self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["lifecycle_stage"], "critique")
            self.assertEqual(payload["output_path"], str(output_path.resolve()))
            self.assertEqual(
                payload["revision_execution"],
                {
                    "active_revision_plan_id": "revision-v1",
                    "reviewed_revision_plan_id": None,
                    "source_critique_id": "critique-v1",
                    "reviewed_revision_evidence": None,
                    "pre_revision_version_label": "v0.3",
                    "post_revision_version_label": "v0.4",
                    "comparison_summary": (
                        "Applied revision plan revision-v1: updated sections [basis, foundation]; "
                        "draft version v0.3 -> v0.4."
                    ),
                },
            )

            revised_workspace = payload["revised_workspace"]
            self.assertEqual(revised_workspace["grant_run_id"], payload["grant_run_id"])
            self.assertEqual(revised_workspace["workspace_id"], payload["workspace_id"])
            self.assertEqual(revised_workspace["lifecycle_stage"], "critique")
            self.assertEqual(revised_workspace["current_selection"]["active_revision_plan_id"], "revision-v1")

            draft = self._active_draft(revised_workspace)
            self.assertEqual(draft["draft_id"], "draft-v1")
            self.assertEqual(draft["status"], "revised")
            self.assertEqual(draft["version_label"], "v0.4")
            self.assertEqual(
                self._section(draft, "basis")["text"],
                "当前关键知识缺口不在于心梗后炎症与纤维化是否相关，而在于炎症巨噬细胞如何通过时间窗依赖的旁分泌通讯触发成纤维细胞致纤维化重编程；若不回答这一机制问题，领域将持续停留在现象描述层。",
            )
            self.assertEqual(
                self._section(draft, "basis")["linked_object_ids"],
                ["arg-001", "question-immune-fibrosis"],
            )
            self.assertEqual(
                self._section(draft, "foundation")["text"],
                "申请人已积累心梗后免疫重塑单细胞图谱、时序样本库与动物模型流程，可直接支撑关键通讯轴定位与功能验证，从而把当前科学问题与申请人既有能力闭合为同一条执行路径。",
            )
            self.assertEqual(
                self._section(draft, "foundation")["linked_object_ids"],
                ["output-1", "project-1"],
            )
            self.assertEqual(
                self._section(draft, "content")["text"],
                "围绕关键通讯轴识别、时间窗验证与功能阻断三段展开，并让每一段都回指既有 argument chain 与 fit mapping。",
            )
            self.assertEqual(
                self._outline_item(draft, "basis")["core_claim"],
                "本研究的必要性在于解释炎症巨噬细胞驱动纤维化重编程的时间窗机制缺口。",
            )
            self.assertEqual(
                self._outline_item(draft, "basis")["linked_object_ids"],
                ["arg-001", "question-immune-fibrosis"],
            )
            self.assertEqual(
                self._outline_item(draft, "foundation")["core_claim"],
                "申请人的单细胞时序资源与模型平台可直接支撑当前问题的关键验证路径。",
            )
            self.assertEqual(
                self._outline_item(draft, "foundation")["linked_object_ids"],
                ["output-1", "project-1"],
            )

            revision_plan = self._active_revision_plan(revised_workspace)
            self.assertEqual(revision_plan["execution_status"], "completed")
            self.assertEqual(revision_plan["pre_revision_version_label"], "v0.3")
            self.assertEqual(revision_plan["post_revision_version_label"], "v0.4")
            self.assertEqual(
                revision_plan["comparison_summary"],
                "Applied revision plan revision-v1: updated sections [basis, foundation]; draft version v0.3 -> v0.4.",
            )
            self.assertTrue(output_path.exists())
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), revised_workspace)

    def test_execute_revision_pass_preserves_reviewed_revision_evidence_for_re_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "re_review-revised-workspace.json"

            exit_code, stdout, stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(P3B_RE_REVIEW_EXAMPLE_PATH),
                "--output",
                str(output_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")

            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["lifecycle_stage"], "critique")
            self.assertEqual(
                payload["revision_execution"],
                {
                    "active_revision_plan_id": "revision-v2",
                    "reviewed_revision_plan_id": "revision-v1",
                    "source_critique_id": "critique-v2",
                    "reviewed_revision_evidence": {
                        "revision_plan_id": "revision-v1",
                        "source_critique_id": "critique-v1",
                        "execution_status": "completed",
                        "pre_revision_version_label": "v0.3",
                        "post_revision_version_label": "v0.4",
                        "comparison_summary": "已比较修订前后版本：必要性链条更锋利，研究基础与当前问题的映射更直接。",
                    },
                    "pre_revision_version_label": "v0.4",
                    "post_revision_version_label": "v0.5",
                    "comparison_summary": (
                        "Applied revision plan revision-v2: updated sections [foundation]; "
                        "draft version v0.4 -> v0.5."
                    ),
                },
            )

            revised_workspace = payload["revised_workspace"]
            draft = self._active_draft(revised_workspace)
            self.assertEqual(draft["status"], "revised")
            self.assertEqual(draft["version_label"], "v0.5")
            self.assertEqual(
                self._section(draft, "foundation")["text"],
                "修订后的研究基础需要直接支撑关键验证实验：申请人现有单细胞时序数据可定位候选通讯轴，在研模型和样本流程可完成阻断验证，因此研究基础与修订后的执行路径形成一一对应的证据闭环。",
            )
            self.assertEqual(
                self._section(draft, "foundation")["linked_object_ids"],
                ["project-1", "output-1"],
            )
            self.assertEqual(
                self._outline_item(draft, "foundation")["core_claim"],
                "申请人的既有数据、模型与样本流程可直接支撑修订后方案的关键验证闭环。",
            )

            revision_plan = self._active_revision_plan(revised_workspace)
            self.assertEqual(revision_plan["execution_status"], "completed")
            self.assertEqual(revision_plan["comparison_summary"], payload["revision_execution"]["comparison_summary"])

            active_critique = self._active_critique(revised_workspace)
            self.assertEqual(active_critique["reviewed_revision_plan_id"], "revision-v1")

    def test_execute_revision_pass_re_review_output_remains_valid_and_routeable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "re_review-validated-workspace.json"

            exit_code, stdout, stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(P3B_RE_REVIEW_EXAMPLE_PATH),
                "--output",
                str(output_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")

            payload = json.loads(stdout)
            revised_workspace = payload["revised_workspace"]

            validation = validate_workspace_document(revised_workspace)
            self.assertTrue(validation.ok, validation.to_dict(revised_workspace))

            route_report = build_stage_route_report(revised_workspace)
            self.assertTrue(route_report["ok"])
            self.assertEqual(route_report["lifecycle_stage"], "critique")
            self.assertEqual(route_report["route"]["next_step"]["recommended_stage"], "revision")
            self.assertEqual(
                route_report["verification_checkpoint"]["identity"]["reviewed_revision_plan_id"],
                "revision-v1",
            )
            self.assertEqual(
                route_report["route"]["critique_summary"]["reviewed_revision_plan_id"],
                "revision-v1",
            )
            self.assertEqual(
                route_report["route"]["critique_summary"]["reviewed_revision_evidence"]["post_revision_version_label"],
                "v0.4",
            )
            self.assertEqual(
                route_report["route"]["summarize_workspace"]["active_revision_plan"]["post_revision_version_label"],
                "v0.5",
            )
            self.assertEqual(
                route_report["route"]["summarize_workspace"]["active_draft"]["version_label"],
                "v0.5",
            )

    def test_execute_revision_pass_initial_revision_output_remains_valid_and_routeable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "initial-validated-workspace.json"

            exit_code, stdout, stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(P2C_CRITIQUE_EXAMPLE_PATH),
                "--output",
                str(output_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")

            payload = json.loads(stdout)
            revised_workspace = payload["revised_workspace"]

            validation = validate_workspace_document(revised_workspace)
            self.assertTrue(validation.ok, validation.to_dict(revised_workspace))

            route_report = build_stage_route_report(revised_workspace)
            self.assertTrue(route_report["ok"])
            self.assertEqual(route_report["lifecycle_stage"], "critique")
            self.assertEqual(route_report["route"]["next_step"]["recommended_stage"], "revision")
            self.assertEqual(route_report["checkpoint_status"], "forward_progress")
            self.assertEqual(route_report["verification_checkpoint"]["checkpoint_status"], "forward_progress")
            self.assertTrue(route_report["verification_checkpoint"]["validation_ok"])
            self.assertEqual(
                route_report["verification_checkpoint"]["identity"],
                {
                    "grant_run_id": payload["grant_run_id"],
                    "workspace_id": payload["workspace_id"],
                    "draft_id": payload["draft_id"],
                    "active_revision_plan_id": "revision-v1",
                    "reviewed_revision_plan_id": None,
                },
            )
            self.assertEqual(
                route_report["route"]["summarize_workspace"]["active_revision_plan"]["post_revision_version_label"],
                "v0.4",
            )
            self.assertEqual(
                route_report["route"]["summarize_workspace"]["active_draft"]["version_label"],
                "v0.4",
            )

    def test_execute_revision_pass_fails_closed_for_non_executable_gate_states(self) -> None:
        cases = (
            (
                FORCED_ROLLBACK_EXAMPLE_PATH,
                "forced_rollback_stage",
            ),
            (
                PRESUBMISSION_FROZEN_EXAMPLE_PATH,
                "presubmission_frozen",
            ),
            (
                READY_FOR_SUBMISSION_EXAMPLE_PATH,
                "当前 active MentorCritique.verdict 必须属于 major_revision / minor_revision",
            ),
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            for input_path, expected_message in cases:
                with self.subTest(example=input_path.name):
                    output_path = Path(tmp_dir) / f"{input_path.stem}-revised.json"
                    exit_code, stdout, stderr = self.run_cli(
                        "execute-revision-pass",
                        "--input",
                        str(input_path),
                        "--output",
                        str(output_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertEqual(payload["command"], "execute-revision-pass")
                    self.assertIn(expected_message, payload["error"])
                    self.assertFalse(output_path.exists())

    def test_execute_revision_pass_rejects_missing_mutation_payload(self) -> None:
        document = self._load_example(P2C_CRITIQUE_EXAMPLE_PATH)
        document["revision_plans"][0]["items"][0].pop("mutation_payload", None)

        payload = self._run_with_workspace(document)

        self.assertFalse(payload["ok"])
        self.assertIn("mutation_payload", payload["error"])

    def test_execute_revision_pass_rejects_target_section_mismatch(self) -> None:
        document = self._load_example(P2C_CRITIQUE_EXAMPLE_PATH)
        document["revision_plans"][0]["items"][0]["mutation_payload"]["target_section_key"] = "foundation"

        payload = self._run_with_workspace(document)

        self.assertFalse(payload["ok"])
        self.assertIn("target_ref", payload["error"])

    def test_execute_revision_pass_rejects_duplicate_target_section(self) -> None:
        document = self._load_example(P2C_CRITIQUE_EXAMPLE_PATH)
        document["revision_plans"][0]["items"][1]["target_ref"] = "section:basis"
        document["revision_plans"][0]["items"][1]["mutation_payload"]["target_section_key"] = "basis"

        payload = self._run_with_workspace(document)

        self.assertFalse(payload["ok"])
        self.assertIn("duplicate", payload["error"])

    def test_execute_revision_pass_rejects_missing_required_linked_object_ids(self) -> None:
        document = self._load_example(P2C_CRITIQUE_EXAMPLE_PATH)
        document["revision_plans"][0]["items"][0]["mutation_payload"]["linked_object_ids"] = ["arg-001"]

        payload = self._run_with_workspace(document)

        self.assertFalse(payload["ok"])
        self.assertIn("required_input_ids", payload["error"])

    def test_execute_revision_pass_fails_closed_when_existing_output_identity_mismatches_active_revision_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "revised-workspace.json"
            output_path.write_text(
                json.dumps(
                    {
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        "workspace_id": "nsfc-demo-001",
                        "current_selection": {
                            "active_revision_plan_id": "revision-other",
                        },
                        "application_drafts": [
                            {
                                "draft_id": "draft-v1",
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            exit_code, stdout, stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(P2C_CRITIQUE_EXAMPLE_PATH),
                "--output",
                str(output_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("output identity 不匹配", payload["error"])
            existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(existing_payload["current_selection"]["active_revision_plan_id"], "revision-other")

    def _run_with_workspace(self, document: dict[str, object]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "workspace.json"
            output_path = Path(tmp_dir) / "revised-workspace.json"
            input_path.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            return json.loads(stdout)

    @staticmethod
    def _load_example(path: Path) -> dict[str, object]:
        return copy.deepcopy(json.loads(path.read_text(encoding="utf-8")))

    @staticmethod
    def _active_draft(document: dict[str, object]) -> dict[str, object]:
        draft_id = document["current_selection"]["active_draft_id"]
        return next(item for item in document["application_drafts"] if item["draft_id"] == draft_id)

    @staticmethod
    def _active_revision_plan(document: dict[str, object]) -> dict[str, object]:
        revision_plan_id = document["current_selection"]["active_revision_plan_id"]
        return next(item for item in document["revision_plans"] if item["revision_plan_id"] == revision_plan_id)

    @classmethod
    def _active_critique(cls, document: dict[str, object]) -> dict[str, object]:
        critique_id = cls._active_revision_plan(document)["critique_id"]
        return next(item for item in document["mentor_critiques"] if item["critique_id"] == critique_id)

    @staticmethod
    def _section(draft: dict[str, object], section_key: str) -> dict[str, object]:
        return next(item for item in draft["sections"] if item["section_key"] == section_key)

    @staticmethod
    def _outline_item(draft: dict[str, object], section_key: str) -> dict[str, object]:
        return next(item for item in draft["outline"] if item["section_key"] == section_key)


if __name__ == "__main__":
    unittest.main()
