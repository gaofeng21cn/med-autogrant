from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from med_autogrant.revision_executor import (  # noqa: E402
    build_revision_execution_document,
    build_revision_execution_payload,
)
from med_autogrant.route_report import build_stage_route_report  # noqa: E402
from med_autogrant.workspace import WorkspaceStateError, validate_workspace_document  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
P2C_CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
P3B_RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class RevisionExecutorTest(unittest.TestCase):
    def test_revision_applies_domain_mutations_and_persists_valid_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "revised-workspace.json"
            payload = build_revision_execution_payload(
                _load(P2C_CRITIQUE_EXAMPLE_PATH),
                output_path=output_path,
            )

            workspace = payload["revised_workspace"]
            draft = self._active(workspace, "application_drafts", "active_draft_id", "draft_id")
            revision = self._active(workspace, "revision_plans", "active_revision_plan_id", "revision_plan_id")
            self.assertEqual(draft["status"], "revised")
            self.assertEqual(draft["version_label"], "v0.4")
            self.assertEqual(self._section(draft, "basis")["linked_object_ids"], ["arg-001", "question-immune-fibrosis"])
            self.assertEqual(self._section(draft, "foundation")["linked_object_ids"], ["output-1", "project-1"])
            self.assertEqual(revision["execution_status"], "completed")
            self.assertEqual(revision["pre_revision_version_label"], "v0.3")
            self.assertEqual(revision["post_revision_version_label"], "v0.4")
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), workspace)
            self.assertTrue(validate_workspace_document(workspace).ok)
            self.assertEqual(
                build_stage_route_report(workspace)["route"]["next_step"]["recommended_stage"],
                "revision",
            )

    def test_rereview_preserves_completed_revision_evidence(self) -> None:
        payload = build_revision_execution_document(document=_load(P3B_RE_REVIEW_EXAMPLE_PATH))
        workspace = payload["revised_workspace"]
        revision = self._active(workspace, "revision_plans", "active_revision_plan_id", "revision_plan_id")
        critique = next(item for item in workspace["mentor_critiques"] if item["critique_id"] == revision["critique_id"])

        self.assertEqual(payload["revision_execution"]["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["revision_execution"]["pre_revision_version_label"], "v0.4")
        self.assertEqual(payload["revision_execution"]["post_revision_version_label"], "v0.5")
        self.assertEqual(critique["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(revision["execution_status"], "completed")
        self.assertEqual(
            build_stage_route_report(workspace)["verification_checkpoint"]["identity"]["reviewed_revision_plan_id"],
            "revision-v1",
        )

    def test_revision_can_apply_ai_selected_whole_draft_restructure(self) -> None:
        document = copy.deepcopy(_load(P2C_CRITIQUE_EXAMPLE_PATH))
        draft = self._active(document, "application_drafts", "active_draft_id", "draft_id")
        replacement_sections = copy.deepcopy(draft["sections"])
        replacement_sections.reverse()
        replacement_sections[0]["text"] = f"{replacement_sections[0]['text']} 全文结构已按独立审阅重新组织。"
        plan = self._active(document, "revision_plans", "active_revision_plan_id", "revision_plan_id")
        plan["items"] = [{
            "item_id": "repair-whole-draft",
            "priority": "p0",
            "action_type": "rebuild_cross_section_argument",
            "target_ref": f"draft:{draft['draft_id']}",
            "action": "重组全文论证顺序",
            "done_criteria": "跨章节论证连续",
            "required_input_ids": [],
            "mutation_payload": {
                "operation": "replace_draft_sections",
                "linked_object_ids": [],
                "replacement_sections": replacement_sections,
            },
        }]

        payload = build_revision_execution_document(document=document)
        revised = self._active(payload["revised_workspace"], "application_drafts", "active_draft_id", "draft_id")
        self.assertEqual(revised["sections"][0]["section_key"], replacement_sections[0]["section_key"])
        self.assertIn("全文结构已按独立审阅重新组织", revised["sections"][0]["text"])
        self.assertTrue(validate_workspace_document(payload["revised_workspace"]).ok)

    def test_revision_gate_and_ai_review_authority_fail_closed(self) -> None:
        no_owner = _load(P2C_CRITIQUE_EXAMPLE_PATH)
        for critique in no_owner["mentor_critiques"]:
            critique.get("metadata", {}).pop("owner", None)

        cases = (
            (no_owner, "AI reviewer-backed critique"),
            (_load(FORCED_ROLLBACK_EXAMPLE_PATH), "forced_rollback_stage"),
            (_load(PRESUBMISSION_FROZEN_EXAMPLE_PATH), "presubmission_frozen"),
            (_load(READY_FOR_SUBMISSION_EXAMPLE_PATH), "major_revision / minor_revision"),
        )
        for document, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(WorkspaceStateError, message):
                    build_revision_execution_document(document=document)

    def test_revision_mutation_contract_fails_closed(self) -> None:
        cases = (
            ("mutation_payload", lambda doc: doc["revision_plans"][0]["items"][0].pop("mutation_payload")),
            (
                "target_ref",
                lambda doc: doc["revision_plans"][0]["items"][0]["mutation_payload"].__setitem__(
                    "target_section_key", "foundation"
                ),
            ),
            ("duplicate", self._duplicate_target),
            (
                "required_input_ids",
                lambda doc: doc["revision_plans"][0]["items"][0]["mutation_payload"].__setitem__(
                    "linked_object_ids", ["arg-001"]
                ),
            ),
        )
        for message, mutate in cases:
            with self.subTest(message=message):
                document = copy.deepcopy(_load(P2C_CRITIQUE_EXAMPLE_PATH))
                mutate(document)
                with self.assertRaisesRegex(WorkspaceStateError, message):
                    build_revision_execution_document(document=document)

    def test_existing_output_identity_mismatch_is_irreversible_write_guard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "revised-workspace.json"
            existing = {
                "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                "workspace_id": "nsfc-demo-001",
                "current_selection": {"active_revision_plan_id": "revision-other"},
                "application_drafts": [{"draft_id": "draft-v1"}],
            }
            output_path.write_text(json.dumps(existing), encoding="utf-8")

            with self.assertRaisesRegex(WorkspaceStateError, "output identity 不匹配"):
                build_revision_execution_payload(
                    _load(P2C_CRITIQUE_EXAMPLE_PATH),
                    output_path=output_path,
                )
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), existing)

    @staticmethod
    def _duplicate_target(document: dict[str, object]) -> None:
        item = document["revision_plans"][0]["items"][1]
        item["target_ref"] = "section:basis"
        item["mutation_payload"]["target_section_key"] = "basis"

    @staticmethod
    def _active(
        document: dict[str, object],
        collection: str,
        selection_key: str,
        id_key: str,
    ) -> dict[str, object]:
        active_id = document["current_selection"][selection_key]
        return next(item for item in document[collection] if item[id_key] == active_id)

    @staticmethod
    def _section(draft: dict[str, object], section_key: str) -> dict[str, object]:
        return next(item for item in draft["sections"] if item["section_key"] == section_key)
