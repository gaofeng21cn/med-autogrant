from __future__ import annotations

import unittest

from med_autogrant.product_entry_parts.manifest_owner_payload_response import (
    EXTERNAL_EVIDENCE_LEDGER_REF,
    MANIFEST_SUSTAINED_CONSUMPTION_EVIDENCE_REF,
    PRODUCTION_ACCEPTANCE_REF,
    WORKSPACE_RECEIPT_SCALEOUT_REF,
)
from product_entry_cases.test_manifest_and_status_cases.context import ManifestStatusContext


def assert_status_projection(
    test_case: unittest.TestCase,
    context: ManifestStatusContext,
) -> None:
    status = context.status
    manifest = context.manifest

    test_case.assertEqual(manifest["operator_loop_surface"]["shell_key"], "grant_user_loop")
    test_case.assertEqual(manifest["operator_loop_surface"]["command"], manifest["recommended_command"])
    test_case.assertEqual(manifest["operator_loop_surface"]["surface_kind"], "grant_user_loop")
    test_case.assertIn("direct grant user inbox shell", manifest["operator_loop_surface"]["summary"])
    test_case.assertEqual(manifest["operator_loop_actions"]["open_loop"]["command"], manifest["recommended_command"])
    test_case.assertEqual(manifest["operator_loop_actions"]["open_loop"]["surface_kind"], "grant_user_loop")
    test_case.assertEqual(manifest["operator_loop_actions"]["inspect_progress"]["requires"], [])
    test_case.assertEqual(manifest["operator_loop_actions"]["build_direct_entry"]["requires"], ["task_intent"])
    test_case.assertEqual(manifest["repo_mainline"]["active_phase"], "P4 mature direct grant product entry")
    test_case.assertEqual(
        manifest["repo_mainline"]["active_tranche"],
        "P4.G authoring-quality-first completion semantics alignment",
    )
    test_case.assertEqual(manifest["repo_mainline"]["phase_id"], "P4")
    test_case.assertEqual(
        manifest["repo_mainline"]["phase_summary"],
        "把 direct grant product 面逐步收成当前用户 inbox shell，并以 authoring quality 作为主任务完成语义。",
    )
    test_case.assertEqual(
        manifest["repo_mainline"]["next_focus"],
        [
            "继续把 `product-entry-manifest` / `product-status` 当作当前 direct grant product entry surface contract，并让 `grant-progress`、`grant-cockpit`、`grant-direct-entry` 与 `grant-user-loop` 继续对齐同一份 product entry surface truth。",
            "继续把 `family_orchestration` companion 从 action graph / human gate preview 深压到 family product-entry manifest v2、event envelope 与 checkpoint lineage contract，并保持 route status 直接读取共享 author-side route truth。",
            "把形式审查/客观补件统一收口到 TODO 与显式唤醒链路，并仅在直接破坏科学论证时升级为 blocker。",
            "对已锁定 funder/family 的任务线保持 continuity，不引入 opportunistic 跨 funder 切换叙事。",
        ],
    )
    test_case.assertEqual(
        manifest["product_entry_status"]["summary"],
        "把 direct grant product 面逐步收成当前用户 inbox shell，并以 authoring quality 作为主任务完成语义。",
    )
    test_case.assertEqual(
        manifest["product_entry_status"]["remaining_gaps_count"],
        len(manifest["remaining_gaps"]),
    )
    test_case.assertEqual(
        manifest["product_entry_status"]["next_focus"],
        manifest["repo_mainline"]["next_focus"],
    )
    product_status = status["product_status"]
    test_case.assertEqual(
        product_status["temporal_stage_run_consumption_policy"],
        manifest["temporal_stage_run_consumption_policy"],
    )
    test_case.assertFalse(
        product_status["temporal_stage_run_consumption_policy"][
            "provider_completion_is_domain_completion"
        ]
    )
    test_case.assertFalse(
        product_status["temporal_stage_run_consumption_policy"][
            "domain_repo_can_own_temporal_runtime"
        ]
    )
    test_case.assertFalse(
        product_status["temporal_stage_run_consumption_policy"][
            "generated_surface_ready_can_claim_domain_ready"
        ]
    )
    owner_payload = manifest["owner_payload_response"]
    test_case.assertEqual(owner_payload["surface_kind"], "mag_opl_owner_payload_response")
    test_case.assertEqual(owner_payload["status"], "blocked_by_submission_ready_human_gate")
    test_case.assertEqual(
        owner_payload["source_surface_refs"],
        {
            "production_acceptance_ref": PRODUCTION_ACCEPTANCE_REF,
            "external_evidence_ledger_ref": EXTERNAL_EVIDENCE_LEDGER_REF,
            "workspace_receipt_scaleout_evidence_ref": WORKSPACE_RECEIPT_SCALEOUT_REF,
            "manifest_sustained_consumption_evidence_ref": (
                MANIFEST_SUSTAINED_CONSUMPTION_EVIDENCE_REF
            ),
        },
    )
    test_case.assertEqual(
        owner_payload["manifest_projection_policy"],
        "default_manifest_refs_only_owner_payload_response_with_count_only_scaleout_provenance",
    )
    test_case.assertFalse(owner_payload["body_included"])
    test_case.assertFalse(owner_payload["operator_payload_submitted"])
    test_case.assertFalse(owner_payload["workspace_receipt_scaleout_count_snapshot_is_receipt_refs"])
    manifest_consumer = owner_payload["manifest_consumer_evidence"]
    test_case.assertEqual(
        manifest_consumer["surface_kind"],
        "mag_manifest_owner_payload_consumer_evidence",
    )
    test_case.assertEqual(
        manifest_consumer["state"],
        "manifest_owner_payload_response_consumed_refs_only",
    )
    test_case.assertEqual(manifest_consumer["consumer"], "one_person_lab_app_operator_manifest")
    test_case.assertEqual(
        manifest_consumer["consumed_surface_refs"]["owner_payload_response_ref"],
        "/product_entry_manifest/owner_payload_response",
    )
    test_case.assertEqual(
        manifest_consumer["consumed_surface_refs"][
            "stage_expected_receipt_payload_summary_ref"
        ],
        "/product_entry_manifest/owner_payload_response/stage_expected_receipt_payload_summary",
    )
    test_case.assertEqual(manifest_consumer["observed_counts"]["workspace_count"], 4)
    test_case.assertEqual(
        manifest_consumer["observed_counts"]["count_only_scaleout_total_receipt_ref_count"],
        36,
    )
    test_case.assertEqual(
        manifest_consumer["observed_counts"]["stage_expected_receipt_payload_stage_count"],
        6,
    )
    test_case.assertIn(
        "typed-blocker:mag/package_and_submit_ready/"
        "submission_ready_export_gate/human-approval-required/2026-05-22",
        manifest_consumer["human_gate_blocker_refs"],
    )
    test_case.assertFalse(manifest_consumer["operator_payload_submitted"])
    test_case.assertFalse(manifest_consumer["count_only_scaleout_snapshot_is_receipt_refs"])
    test_case.assertFalse(manifest_consumer["claims_sustained_app_consumption_complete"])
    test_case.assertFalse(manifest_consumer["claims_submission_ready"])
    test_case.assertFalse(manifest_consumer["claims_provider_long_soak_complete"])
    test_case.assertFalse(manifest_consumer["authority_boundary"]["can_create_owner_receipt"])
    test_case.assertFalse(manifest_consumer["authority_boundary"]["can_submit_operator_payload"])
    test_case.assertFalse(
        manifest_consumer["authority_boundary"]["can_declare_app_sustained_consumption_complete"]
    )
    test_case.assertFalse(owner_payload["grant_ready_claimed"])
    test_case.assertFalse(owner_payload["quality_ready_claimed"])
    test_case.assertFalse(owner_payload["export_ready_claimed"])
    test_case.assertFalse(owner_payload["submission_ready_claimed"])
    test_case.assertFalse(owner_payload["authority_boundary"]["opl_writes_grant_truth"])
    test_case.assertFalse(owner_payload["authority_boundary"]["opl_reads_memory_body"])
    test_case.assertFalse(owner_payload["authority_boundary"]["opl_reads_artifact_body"])
    test_case.assertFalse(owner_payload["authority_boundary"]["opl_authorizes_quality_or_export"])
    test_case.assertFalse(owner_payload["authority_boundary"]["can_declare_submission_ready"])
    test_case.assertFalse(owner_payload["authority_boundary"]["typed_blocker_is_submission_ready"])
    test_case.assertIn(
        "typed-blocker:mag/package_and_submit_ready/"
        "submission_ready_export_gate/human-approval-required/2026-05-22",
        owner_payload["typed_blocker_refs"],
    )
    test_case.assertNotIn("stage_expected_receipt_payload_summary", owner_payload["record_payload"])
    stage_payload = owner_payload["stage_expected_receipt_payload_summary"]
    test_case.assertEqual(stage_payload["surface_kind"], "mag_stage_expected_receipt_payload_summary")
    test_case.assertEqual(stage_payload["stage_count"], 6)
    test_case.assertFalse(stage_payload["payload_body_allowed"])
    test_case.assertFalse(stage_payload["success_refs_visible_is_completion"])
    test_case.assertFalse(stage_payload["grant_ready_claimed"])
    test_case.assertFalse(stage_payload["quality_ready_claimed"])
    test_case.assertFalse(stage_payload["export_ready_claimed"])
    test_case.assertFalse(stage_payload["submission_ready_claimed"])
    test_case.assertEqual(
        owner_payload["workspace_receipt_scaleout_summary"]["total_receipt_ref_count"],
        36,
    )
    test_case.assertEqual(
        manifest["workspace_receipt_scaleout_evidence"]["surface_kind"],
        "mag_workspace_receipt_scaleout_evidence.v1",
    )
    test_case.assertFalse(
        manifest["workspace_receipt_scaleout_evidence"]["claims"]["claims_grant_ready"]
    )
    test_case.assertFalse(
        manifest["workspace_receipt_scaleout_evidence"]["claims"]["claims_submission_ready_export"]
    )
