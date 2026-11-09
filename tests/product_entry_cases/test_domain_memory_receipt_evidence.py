from __future__ import annotations

import tempfile
from contextlib import redirect_stdout
from io import StringIO

import json
import unittest
from pathlib import Path

from med_autogrant.product_entry_parts.domain_memory_runtime import (
    DOMAIN_MEMORY_RUNTIME_RECEIPT_EVIDENCE_KIND,
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    export_framework_knowledge_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError
from med_autogrant.cli import main


CRITIQUE_EXAMPLE_PATH = (
    Path(__file__).resolve().parents[2] / "examples" / "nsfc_workspace_p2c_critique.json"
)


class ProductEntryDomainMemoryReceiptEvidenceTest(unittest.TestCase):
    def _write_proposal(self, proposal_payload: dict[str, object]) -> Path:
        proposal_path = Path(tempfile.mkdtemp()) / "proposal.json"
        proposal_path.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return proposal_path

    def test_preserves_proposal_json_loader_errors(self) -> None:
        cases = (
            ("{", WorkspaceStateError, "domain_memory_writeback_proposal 不是合法 JSON"),
            ("[]", WorkspaceStateError, "domain_memory_writeback_proposal 必须是 JSON object"),
            (None, WorkspaceFileError, "读取 domain_memory_writeback_proposal 失败"),
        )

        for contents, error_type, message in cases:
            with self.subTest(contents=contents):
                proposal_path = Path(tempfile.mkdtemp()) / "proposal.json"
                if contents is not None:
                    proposal_path.write_text(contents, encoding="utf-8")

                with self.assertRaises(error_type) as raised:
                    build_domain_memory_writeback_decision(
                        proposal_path=proposal_path,
                        decision="accepted",
                        decision_reason="Characterization only.",
                    )

                self.assertIs(type(raised.exception), error_type)
                self.assertEqual(str(raised.exception), f"{message}: {proposal_path.resolve()}")

    def test_preserves_decision_json_loader_errors(self) -> None:
        cases = (
            ("{", WorkspaceStateError, "domain_memory_writeback_decision 不是合法 JSON"),
            ("[]", WorkspaceStateError, "domain_memory_writeback_decision 必须是 JSON object"),
            (None, WorkspaceFileError, "读取 domain_memory_writeback_decision 失败"),
        )

        for contents, error_type, message in cases:
            with self.subTest(contents=contents):
                decision_path = Path(tempfile.mkdtemp()) / "decision.json"
                if contents is not None:
                    decision_path.write_text(contents, encoding="utf-8")

                with self.assertRaises(error_type) as raised:
                    write_domain_memory_receipt_evidence(decision_payload=decision_path)

                self.assertIs(type(raised.exception), error_type)
                self.assertEqual(str(raised.exception), f"{message}: {decision_path.resolve()}")

    def test_writes_accepted_runtime_receipt_instance_without_memory_body(self) -> None:
        proposal_payload = build_domain_memory_writeback_proposal(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            workspace_root=CRITIQUE_EXAMPLE_PATH.parent.parent,
            project_root=CRITIQUE_EXAMPLE_PATH.parent,
            stage_id="review_and_rebuttal",
            source_ref="runtime-closeout://grant-run/example",
            lesson_summary="Keep reusable reviewer risk framing as strategy memory.",
            knowledge_id="grant.reviewer-risk-framing",
            scope_kind="topic",
            scope_id="team.grant-strategy",
            content_kind="mechanism",
            evidence_class="reviewed_project_experience",
            review_requirement="Grant strategy owner accepts cross-project applicability.",
            proposal_id="review-risk-framing",
        )
        decision_payload = build_domain_memory_writeback_decision(
            proposal_path=self._write_proposal(proposal_payload),
            decision="accepted",
            decision_reason="Reusable reviewer risk framing.",
        )

        with tempfile.TemporaryDirectory() as runtime_root:
            evidence = write_domain_memory_receipt_evidence(
                decision_payload=decision_payload,
                runtime_root=runtime_root,
            )

            receipt = evidence["domain_memory_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            self.assertTrue(receipt_path.exists())
            self.assertEqual(receipt["surface_kind"], DOMAIN_MEMORY_RUNTIME_RECEIPT_EVIDENCE_KIND)
            self.assertEqual(receipt["state"], "runtime_receipt_instance_written")
            self.assertEqual(receipt["decision"], "accepted")
            self.assertEqual(receipt["owner"], "med-autogrant")
            self.assertFalse(receipt["repo_tracked"])
            self.assertFalse(receipt["contains_memory_body"])
            self.assertFalse(receipt["contains_grant_artifact_content"])
            self.assertFalse(receipt["contains_quality_or_export_verdict"])
            self.assertEqual(receipt["accepted_knowledge_id"], "grant.reviewer-risk-framing")
            self.assertEqual(receipt["target_scope"], {"kind": "topic", "id": "team.grant-strategy"})
            self.assertEqual(receipt["knowledge_persistence"], "pending_authorized_source_writeback")
            self.assertIsNone(receipt["rejected_memory_ref"])

            receipt_instance = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt_instance, receipt)
            self.assertNotIn("lesson_summary", receipt_instance)

    def test_writes_rejected_runtime_receipt_instance_without_memory_body(self) -> None:
        proposal_payload = build_domain_memory_writeback_proposal(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            workspace_root=CRITIQUE_EXAMPLE_PATH.parent.parent,
            project_root=CRITIQUE_EXAMPLE_PATH.parent,
            stage_id="review_and_rebuttal",
            source_ref="runtime-closeout://grant-run/example",
            lesson_summary="Do not store this text in the receipt evidence.",
            knowledge_id="grant.reviewer-risk-framing",
            scope_kind="project",
            scope_id="grant.example",
            content_kind="decision",
            evidence_class="project_observation",
            review_requirement="Project owner reviews the observation.",
            proposal_id="reject-review-risk-framing",
        )
        decision_payload = build_domain_memory_writeback_decision(
            proposal_path=self._write_proposal(proposal_payload),
            decision="rejected",
            decision_reason="Not broadly reusable enough.",
        )

        with tempfile.TemporaryDirectory() as runtime_root:
            evidence = write_domain_memory_receipt_evidence(
                decision_payload=decision_payload,
                runtime_root=runtime_root,
            )

            receipt = evidence["domain_memory_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            self.assertTrue(receipt_path.exists())
            self.assertEqual(receipt["decision"], "rejected")
            self.assertIsNone(receipt["accepted_knowledge_id"])
            self.assertIsNotNone(receipt["rejected_memory_ref"])
            self.assertFalse(receipt["contains_memory_body"])
            self.assertNotIn("lesson_summary", json.loads(receipt_path.read_text(encoding="utf-8")))

    def test_topic_proposal_preserves_identity_without_prescribing_storage(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            project = workspace / "projects" / "grant-a"
            project.mkdir(parents=True)
            source = workspace / "team-library" / "strategy.md"
            source.parent.mkdir()
            source.write_text("Existing canonical team knowledge.", encoding="utf-8")
            payload = build_domain_memory_writeback_proposal(
                input_path=CRITIQUE_EXAMPLE_PATH,
                workspace_root=workspace,
                project_root=project,
                stage_id="review_and_rebuttal",
                source_ref=str(source),
                lesson_summary="Refine the grant-topic reviewer strategy.",
                knowledge_id="team.grant-reviewer-strategy",
                scope_kind="topic",
                scope_id="team.grant-strategy",
                content_kind="policy",
                evidence_class="reviewed_project_experience",
                review_requirement="Team owner accepts the topic update.",
            )
            proposal = payload["domain_memory_writeback_proposal"]
            self.assertEqual(proposal["target_scope"], {"kind": "topic", "id": "team.grant-strategy"})
            self.assertEqual(proposal["execution_scope"]["project_root"], str(project.resolve()))
            self.assertNotIn("target_layer", proposal)
            self.assertNotIn("catalog_ref", proposal)
            self.assertEqual(source.read_text(encoding="utf-8"), "Existing canonical team knowledge.")
            self.assertFalse((project / "memory").exists())

            proposal_path = self._write_proposal(payload)
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["authority", "memory-export", "--proposal", str(proposal_path), "--json"])
            self.assertEqual(exit_code, 0)
            exported = json.loads(stdout.getvalue())
            self.assertEqual(set(exported), {
                "source_refs", "target_scope", "content_kind", "proposed_rule_or_mechanism",
                "evidence_class", "review_requirement",
            })
            self.assertEqual(exported["target_scope"], {"kind": "topic", "id": "team.grant-strategy"})
            self.assertEqual(exported["proposed_rule_or_mechanism"], "Refine the grant-topic reviewer strategy.")
            self.assertEqual(source.read_text(encoding="utf-8"), "Existing canonical team knowledge.")

            proposal["target_scope"] = {"kind": "product", "id": "med-autogrant"}
            with self.assertRaisesRegex(WorkspaceStateError, "Framework knowledge writeback proposal is invalid"):
                export_framework_knowledge_writeback_proposal(proposal_path=self._write_proposal(payload))

            proposal["target_scope"] = {"kind": "topic", "id": "team.grant-strategy", "root": str(workspace)}
            with self.assertRaisesRegex(WorkspaceStateError, "Framework knowledge writeback proposal is invalid"):
                export_framework_knowledge_writeback_proposal(proposal_path=self._write_proposal(payload))
            with self.assertRaisesRegex(WorkspaceStateError, "target_scope requires kind and id"):
                build_domain_memory_writeback_decision(
                    proposal_path=self._write_proposal(payload),
                    decision="accepted",
                    decision_reason="Must not smuggle a source locator into semantic scope.",
                )
