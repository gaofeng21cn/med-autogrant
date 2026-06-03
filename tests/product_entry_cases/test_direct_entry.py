from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryDirectEntryTest(unittest.TestCase):
    def test_grant_direct_entry_composes_projection_and_entry_envelopes(self) -> None:
        from med_autogrant.domain_entry_contract import build_domain_entry_contract
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_direct_entry(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )

        self.assertEqual(payload["command"], "grant-direct-entry")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
        self.assertEqual(payload["session_continuity"]["surface_kind"], "session_continuity")
        self.assertEqual(payload["session_continuity"]["session_id"], payload["grant_run_id"])
        self.assertEqual(payload["progress_projection"]["surface_kind"], "progress_projection")
        self.assertEqual(
            payload["progress_projection"]["projection"]["projection_kind"],
            "grant_progress",
        )
        self.assertEqual(payload["artifact_inventory"]["surface_kind"], "artifact_inventory")

        runtime_control = payload["runtime_control"]
        self.assertEqual(runtime_control["surface_kind"], "runtime_control")
        self.assertEqual(runtime_control["runtime_owner"], "one-person-lab")
        self.assertEqual(runtime_control["domain_owner"], "med-autogrant")
        self.assertEqual(runtime_control["executor_owner"], "codex_cli")
        self.assertEqual(runtime_control["session_locator"]["locator_value"], payload["grant_run_id"])
        self.assertEqual(runtime_control["restore_point"]["lifecycle_stage"], payload["lifecycle_stage"])
        self.assertIn(
            "--task-intent tighten-grant-mainline",
            runtime_control["approval_control_surface"]["command"],
        )
        self.assertIn(
            "--task-intent tighten-grant-mainline",
            runtime_control["direct_entry"]["command"],
        )

        grant_direct_entry = payload["grant_direct_entry"]
        self.assertEqual(grant_direct_entry["entry_version"], 1)
        self.assertEqual(grant_direct_entry["entry_kind"], "grant_direct_entry")
        self.assertEqual(grant_direct_entry["target_domain_id"], "med-autogrant")
        self.assertEqual(grant_direct_entry["workspace_surface_kind"], "nsfc_workspace")
        self.assertEqual(grant_direct_entry["task_intent"], "tighten-grant-mainline")
        self.assertEqual(grant_direct_entry["workspace_status"], "attention_required")
        self.assertEqual(grant_direct_entry["workspace_alerts"], ["必要性表述仍略偏现象描述。"])
        self.assertEqual(
            grant_direct_entry["workspace_overview"]["selected_question"],
            "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
        )

        progress_projection = grant_direct_entry["progress_projection"]
        self.assertEqual(progress_projection["projection_version"], 1)
        self.assertEqual(progress_projection["projection_kind"], "grant_progress")
        self.assertEqual(progress_projection["current_stage"], "critique")
        self.assertEqual(progress_projection["recommended_next_stage"], "revision")
        self.assertEqual(progress_projection["current_blockers"], ["必要性表述仍略偏现象描述。"])
        self.assertFalse(progress_projection["needs_author_decision"])
        self.assertEqual(
            progress_projection["currentness_resolver"]["authority_boundary"]["grant_truth_owner"],
            "med-autogrant",
        )
        self.assertFalse(
            progress_projection["currentness_resolver"]["authority_boundary"]["can_write_grant_truth"]
        )
        self.assertEqual(
            progress_projection["opl_progress_delta"]["progress_delta_classification"],
            "mixed",
        )
        self.assertEqual(
            progress_projection["status_narration_contract"]["facts"]["grant_run_id"],
            payload["grant_run_id"],
        )
        self.assertEqual(
            progress_projection["product_entry_surface"]["builder_command"],
            PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
        )

        self.assertEqual(
            grant_direct_entry["current_stage_route"],
            _expected_route("critique", source_stage="critique"),
        )
        self.assertEqual(
            grant_direct_entry["recommended_executor_route"],
            _expected_route("revision", source_stage="critique"),
        )

        expected_return_surface_contract = {
            "entry_adapter": "MedAutoGrantDomainEntry",
            "default_formal_entry": "CLI",
            "supported_entry_modes": ["direct", "opl-handoff"],
            "domain_entry_contract": build_domain_entry_contract(),
            "checkpoint_aggregation_surface": "stage-route-report",
            "operator_contract": {
                "canonical_audit_surfaces": [
                    "validate-workspace",
                    "summarize-workspace",
                    "grant-intake-audit",
                    "grant-evidence-grounding",
                    "grant-quality-scorecard",
                    "grant-quality-closure-dossier",
                    "grant-quality-diff",
                    "next-step",
                    "critique-summary",
                    "stage-route-report",
                ],
                "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
                "checkpoint_aggregation_surface": "stage-route-report",
            },
            "session_continuity": payload["session_continuity"],
            "progress_projection": payload["progress_projection"],
            "artifact_inventory": payload["artifact_inventory"],
            "runtime_control": payload["runtime_control"],
        }

        runtime_substrate_contract = grant_direct_entry["direct_entry"]["runtime_session_contract"][
            "runtime_substrate_contract"
        ]
        self.assertEqual(runtime_substrate_contract["runtime_owner"], "configured_family_runtime_provider")
        self.assertEqual(runtime_substrate_contract["task_runtime_owner"], "one-person-lab")
        self.assertEqual(runtime_substrate_contract["runtime_substrate"], "temporal")
        self.assertEqual(runtime_substrate_contract["stage_executor_owner"], "codex_cli")

        for entry_key, entry_mode in (
            ("direct_entry", "direct"),
            ("opl_handoff_entry", "opl-handoff"),
        ):
            with self.subTest(entry_key=entry_key):
                entry = grant_direct_entry[entry_key]
                self.assertEqual(entry["entry_version"], 1)
                self.assertEqual(entry["entry_kind"], "med_auto_grant_product_entry")
                self.assertEqual(entry["target_domain_id"], "med-autogrant")
                self.assertEqual(entry["task_intent"], "tighten-grant-mainline")
                self.assertEqual(entry["entry_mode"], entry_mode)
                self.assertEqual(
                    entry["workspace_locator"],
                    {
                        "workspace_surface_kind": "nsfc_workspace",
                        "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    },
                )
                self.assertEqual(entry["return_surface_contract"], expected_return_surface_contract)
                self.assertEqual(
                    entry["domain_payload"],
                    {
                        "workspace_id": "nsfc-demo-001",
                        "draft_id": "draft-v1",
                        "funding_call": "nsfc-2026-general",
                    },
                )
                self.assertEqual(
                    entry["stage_snapshot"],
                    {
                        "lifecycle_stage": "critique",
                        "checkpoint_status": "forward_progress",
                        "recommended_next_stage": "revision",
                    },
                )

                runtime_session_contract = entry["runtime_session_contract"]
                self.assertEqual(runtime_session_contract["grant_run_id"], payload["grant_run_id"])
                self.assertEqual(runtime_session_contract["session_handle_kind"], "grant_run_id")
                self.assertEqual(runtime_session_contract["session_owner"], "one-person-lab")
                self.assertEqual(
                    runtime_session_contract["generated_session_surface_ref"],
                    "opl://generated-surfaces/mag/product-entry-session",
                )
                self.assertEqual(
                    runtime_session_contract["generated_resume_surface_ref"],
                    "opl://generated-surfaces/mag/product-entry-session#resume",
                )
                self.assertEqual(
                    runtime_session_contract["domain_authority_surface_ref"],
                    "/product_entry_manifest/owner_receipt_contract",
                )
                self.assertEqual(
                    runtime_session_contract["runtime_substrate_contract"],
                    runtime_substrate_contract,
                )
                self.assertEqual(
                    runtime_session_contract["runtime_state_contract"]["root"],
                    "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                )
                self.assertTrue(runtime_session_contract["runtime_state_contract"]["non_repo_tracked"])

                executor_routing_contract = entry["executor_routing_contract"]
                self.assertEqual(executor_routing_contract["contract_version"], 1)
                self.assertEqual(
                    executor_routing_contract["current_stage_route"],
                    _expected_route("critique", source_stage="critique"),
                )
                self.assertEqual(
                    executor_routing_contract["recommended_executor_route"],
                    _expected_route("revision", source_stage="critique"),
                )
                self.assertEqual(
                    executor_routing_contract["author_side_route_catalog"],
                    [_expected_route(route_id, source_stage=route_id) for route_id in AUTHOR_SIDE_ROUTE_IDS],
                )
