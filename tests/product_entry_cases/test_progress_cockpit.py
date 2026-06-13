from __future__ import annotations

import unittest
from pathlib import Path

from med_autogrant.product_entry_parts.progress_projection_helpers import (
    _build_opl_progress_delta_mapping,
)
from med_autogrant.public_cli import public_cli_command
from product_entry_cases.support import (
    CRITIQUE_EXAMPLE_PATH,
    FROZEN_EXAMPLE_PATH,
    PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
)


PROGRESS_PROJECTION_KEYS = {
    "projection_version",
    "projection_kind",
    "workspace_surface_kind",
    "current_stage",
    "current_stage_summary",
    "checkpoint_status",
    "recommended_next_stage",
    "current_blockers",
    "next_system_action",
    "needs_author_decision",
    "author_decision_summary",
    "currentness_resolver",
    "opl_progress_delta",
    "status_narration_contract",
    "focus",
    "product_entry_surface",
}


def _assert_progress_first_projection_contract(
    test_case: unittest.TestCase,
    projection: dict[str, object],
    *,
    current_stage: str,
    recommended_next_stage: str,
    checkpoint_status: str,
    workspace_path: Path,
) -> None:
    test_case.assertEqual(set(projection), PROGRESS_PROJECTION_KEYS)

    currentness = projection["currentness_resolver"]
    test_case.assertIsInstance(currentness, dict)
    test_case.assertEqual(currentness["surface_kind"], "mag_progress_first_currentness_resolver")
    test_case.assertEqual(currentness["current_program"]["program_id"], "med-autogrant-mainline")
    test_case.assertEqual(currentness["workspace_truth"]["workspace_id"], "nsfc-demo-001")
    test_case.assertEqual(
        currentness["workspace_truth"]["grant_run_id"],
        "grant-run-nsfc-demo-001-baseline-001",
    )
    test_case.assertEqual(currentness["workspace_truth"]["lifecycle_stage"], current_stage)
    test_case.assertEqual(currentness["workspace_truth"]["checkpoint_status"], checkpoint_status)
    test_case.assertEqual(currentness["workspace_truth"]["workspace_path"], str(workspace_path.resolve()))
    test_case.assertEqual(
        currentness["last_receipt_or_blocker"]["ref"],
        f"receipt:mag/grant-stage-controlled-attempt/{current_stage}/owner-receipt-or-typed-blocker",
    )
    test_case.assertEqual(currentness["stage_refs"]["current_stage"], current_stage)
    test_case.assertEqual(currentness["stage_refs"]["recommended_next_stage"], recommended_next_stage)
    test_case.assertEqual(
        currentness["manifest_refs"]["progress_projection_ref"],
        "/product_entry_manifest/progress_projection",
    )

    opl_delta = projection["opl_progress_delta"]
    test_case.assertIsInstance(opl_delta, dict)
    test_case.assertEqual(
        opl_delta,
        _build_opl_progress_delta_mapping(progress_projection=projection),
    )
    test_case.assertEqual(opl_delta["surface_kind"], "opl_progress_first_delta_mapping")
    test_case.assertEqual(opl_delta["progress_delta_classification"], "mixed")
    test_case.assertEqual(opl_delta["grant_work_progress"]["owner"], "med-autogrant")
    test_case.assertEqual(opl_delta["grant_work_progress"]["current_stage"], current_stage)
    test_case.assertEqual(opl_delta["grant_work_progress"]["recommended_next_stage"], recommended_next_stage)
    test_case.assertEqual(opl_delta["platform_evidence_progress"]["owner"], "one-person-lab")
    test_case.assertFalse(opl_delta["grant_work_progress"]["can_claim_submission_ready"])
    test_case.assertFalse(opl_delta["platform_evidence_progress"]["can_claim_export_ready"])
    test_case.assertEqual(
        opl_delta["next_forced_delta"]["required_delta_kind"],
        "grant_deliverable_progress_delta_or_domain_owned_typed_blocker",
    )
    test_case.assertEqual(opl_delta["next_forced_delta"]["current_stage"], current_stage)
    test_case.assertEqual(opl_delta["next_forced_delta"]["recommended_next_stage"], recommended_next_stage)
    test_case.assertEqual(opl_delta["next_forced_delta"]["next_owner"], "med-autogrant")
    test_case.assertIn("typed_blocker_ref", opl_delta["next_forced_delta"]["accepted_return_shapes"])
    test_case.assertFalse(opl_delta["next_forced_delta"]["can_claim_grant_ready"])
    test_case.assertFalse(opl_delta["next_forced_delta"]["can_claim_export_ready"])


class ProductEntryProgressCockpitTest(unittest.TestCase):
    def test_grant_progress_projects_critique_stage_for_direct_entry(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_progress(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertEqual(payload["command"], "grant-progress")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["input_path"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
        progress_projection = payload["progress_projection"]
        _assert_progress_first_projection_contract(
            self,
            progress_projection,
            current_stage="critique",
            recommended_next_stage="revision",
            checkpoint_status="forward_progress",
            workspace_path=CRITIQUE_EXAMPLE_PATH,
        )
        self.assertEqual(
            {
                key: progress_projection[key]
                for key in (
                    "projection_version",
                    "projection_kind",
                    "workspace_surface_kind",
                    "current_stage",
                    "current_stage_summary",
                    "checkpoint_status",
                    "recommended_next_stage",
                    "current_blockers",
                    "next_system_action",
                    "needs_author_decision",
                    "author_decision_summary",
                    "status_narration_contract",
                    "focus",
                    "product_entry_surface",
                )
            },
            {
                "projection_version": 1,
                "projection_kind": "grant_progress",
                "workspace_surface_kind": "nsfc_workspace",
                "current_stage": "critique",
                "current_stage_summary": "当前 grant 已进入 critique 阶段；导师批注 verdict=major_revision，应先执行结构化修订。",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "revision",
                "current_blockers": [
                    "必要性表述仍略偏现象描述。",
                ],
                "next_system_action": "执行 revision plan 中的 P0/P1 项。",
                "needs_author_decision": False,
                "author_decision_summary": None,
                "status_narration_contract": {
                    "schema_version": 1,
                    "contract_kind": "ai_status_narration",
                    "contract_id": "grant-progress::nsfc-demo-001",
                    "surface_kind": "grant_progress",
                    "audience": "human_user",
                    "milestone": {},
                    "stage": {
                        "current_stage": "critique",
                        "recommended_next_stage": "revision",
                        "checkpoint_status": "forward_progress",
                    },
                    "readiness": {
                        "needs_author_decision": False,
                    },
                    "remaining_scope": {},
                    "current_blockers": [
                        "必要性表述仍略偏现象描述。",
                    ],
                    "latest_update": "当前 grant 已进入 critique 阶段；导师批注 verdict=major_revision，应先执行结构化修订。",
                    "next_step": "执行 revision plan 中的 P0/P1 项。",
                    "human_gate": {},
                    "facts": {
                        "workspace_id": "nsfc-demo-001",
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    },
                    "narration_policy": {
                        "mode": "ai_first",
                        "legacy_summary_role": "fallback_only",
                        "style": "plain_language",
                        "answer_checklist": ["current_stage", "current_blockers", "next_step"],
                    },
                },
                "focus": {
                    "applicant_name": "示例申请人",
                    "funding_program": "nsfc-2026-general",
                    "project_profile_label": "NSFC general medical grant profile",
                    "template_label": "NSFC general medical grant template",
                    "critique_policy_id": "nsfc_mentor_critique_v1",
                    "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                    "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                    "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                    "critique_verdict": "major_revision",
                },
                "product_entry_surface": {
                    "builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                    "target_domain_id": "med-autogrant",
                    "supported_entry_modes": ["direct", "opl-handoff"],
                    "task_intent_required": True,
                    "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                },
            },
        )

    def test_grant_progress_projects_frozen_stage_without_blockers(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_progress(
            input_path=str(FROZEN_EXAMPLE_PATH),
        )

        self.assertEqual(payload["lifecycle_stage"], "frozen")
        progress_projection = payload["progress_projection"]
        _assert_progress_first_projection_contract(
            self,
            progress_projection,
            current_stage="frozen",
            recommended_next_stage="frozen",
            checkpoint_status="submission_frozen",
            workspace_path=FROZEN_EXAMPLE_PATH,
        )
        self.assertEqual(
            {
                key: progress_projection[key]
                for key in (
                    "projection_version",
                    "projection_kind",
                    "workspace_surface_kind",
                    "current_stage",
                    "current_stage_summary",
                    "checkpoint_status",
                    "recommended_next_stage",
                    "current_blockers",
                    "next_system_action",
                    "needs_author_decision",
                    "author_decision_summary",
                    "status_narration_contract",
                    "focus",
                    "product_entry_surface",
                )
            },
            {
                "projection_version": 1,
                "projection_kind": "grant_progress",
                "workspace_surface_kind": "nsfc_workspace",
                "current_stage": "frozen",
                "current_stage_summary": "当前 grant 已进入 frozen 阶段；送审前冻结 gate 已闭合，可保持当前阶段继续推进。",
                "checkpoint_status": "submission_frozen",
                "recommended_next_stage": "frozen",
                "current_blockers": [],
                "next_system_action": "沿当前阶段继续执行主线任务。",
                "needs_author_decision": False,
                "author_decision_summary": None,
                "status_narration_contract": {
                    "schema_version": 1,
                    "contract_kind": "ai_status_narration",
                    "contract_id": "grant-progress::nsfc-demo-001",
                    "surface_kind": "grant_progress",
                    "audience": "human_user",
                    "milestone": {},
                    "stage": {
                        "current_stage": "frozen",
                        "recommended_next_stage": "frozen",
                        "checkpoint_status": "submission_frozen",
                    },
                    "readiness": {
                        "needs_author_decision": False,
                    },
                    "remaining_scope": {},
                    "current_blockers": [],
                    "latest_update": "当前 grant 已进入 frozen 阶段；送审前冻结 gate 已闭合，可保持当前阶段继续推进。",
                    "next_step": "沿当前阶段继续执行主线任务。",
                    "human_gate": {},
                    "facts": {
                        "workspace_id": "nsfc-demo-001",
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    },
                    "narration_policy": {
                        "mode": "ai_first",
                        "legacy_summary_role": "fallback_only",
                        "style": "plain_language",
                        "answer_checklist": ["current_stage", "current_blockers", "next_step"],
                    },
                },
                "focus": {
                    "applicant_name": "示例申请人",
                    "funding_program": "nsfc-2026-general",
                    "project_profile_label": "NSFC general medical grant profile",
                    "template_label": "NSFC general medical grant template",
                    "critique_policy_id": "nsfc_mentor_critique_v1",
                    "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                    "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                    "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                    "critique_verdict": "ready_for_submission",
                },
                "product_entry_surface": {
                    "builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                    "target_domain_id": "med-autogrant",
                    "supported_entry_modes": ["direct", "opl-handoff"],
                    "task_intent_required": True,
                    "workspace_path": str(FROZEN_EXAMPLE_PATH.resolve()),
                },
            },
        )

    def test_grant_cockpit_packages_progress_alerts_and_entry_commands(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_cockpit(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertEqual(payload["command"], "grant-cockpit")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
        self.assertEqual(
            payload["grant_cockpit"]["workspace_overview"],
            {
                "applicant_name": "示例申请人",
                "funding_program": "nsfc-2026-general",
                "project_profile_label": "NSFC general medical grant profile",
                "template_label": "NSFC general medical grant template",
                "critique_policy_id": "nsfc_mentor_critique_v1",
                "lifecycle_stage": "critique",
                "checkpoint_status": "forward_progress",
                "selected_direction_title": "心梗后免疫-成纤维细胞互作驱动心肌纤维化重塑",
                "selected_question": "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
                "active_draft_title": "心梗后炎症巨噬细胞介导的跨细胞通讯机制与心肌纤维化重塑",
                "critique_verdict": "major_revision",
            },
        )
        self.assertEqual(payload["grant_cockpit"]["workspace_status"], "attention_required")
        self.assertEqual(
            payload["grant_cockpit"]["workspace_alerts"],
            [
                "必要性表述仍略偏现象描述。",
            ],
        )
        self.assertEqual(
            payload["grant_cockpit"]["progress_projection"]["projection_kind"],
            "grant_progress",
        )
        self.assertEqual(
            payload["grant_cockpit"]["commands"],
            {
                "grant_progress": public_cli_command(
                    "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "grant_intake_audit": public_cli_command(
                    "grant-intake-audit", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "grant_evidence_grounding": public_cli_command(
                    "grant-evidence-grounding", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "summarize_workspace": public_cli_command(
                    "summarize-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "stage_route_report": public_cli_command(
                    "stage-route-report", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "critique_summary": public_cli_command(
                    "critique-summary", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "build_direct_entry": public_cli_command(
                    "build-product-entry",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--entry-mode",
                    "direct",
                    "--task-intent",
                    "<describe-task-intent>",
                    "--format",
                    "json",
                ),
                "build_opl_handoff": public_cli_command(
                    "build-product-entry",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--entry-mode",
                    "opl-handoff",
                    "--task-intent",
                    "<describe-task-intent>",
                    "--format",
                    "json",
                ),
                "build_submission_ready_package": public_cli_command(
                    "build-submission-ready-package",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--output-dir",
                    "<submission-ready-output-dir>",
                    "--format",
                    "json",
                ),
                "domain_memory_writeback_proposal": public_cli_command(
                    "product-domain-memory-proposal",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--stage-id",
                    "<stage-id>",
                    "--source-ref",
                    "<workspace-or-runtime-ref>",
                    "--lesson-summary",
                    "<strategy-lesson-summary>",
                    "--format",
                    "json",
                ),
                "domain_memory_writeback_decision": public_cli_command(
                    "product-domain-memory-decision",
                    "--proposal",
                    "<proposal-json>",
                    "--decision",
                    "<accepted|rejected>",
                    "--decision-reason",
                    "<decision-reason>",
                    "--format",
                    "json",
                ),
                "domain_memory_receipt_evidence": public_cli_command(
                    "product-domain-memory-receipt-evidence",
                    "--decision",
                    "<decision-json>",
                    "--runtime-root",
                    "<runtime-state-root>",
                    "--format",
                    "json",
                ),
            },
        )
