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
        runtime_substrate_contract = payload["grant_direct_entry"]["direct_entry"]["runtime_session_contract"][
            "runtime_substrate_contract"
        ]
        self.assertEqual(runtime_substrate_contract["runtime_owner"], "configured_family_runtime_provider")
        self.assertEqual(runtime_substrate_contract["task_runtime_owner"], "one-person-lab")
        self.assertEqual(runtime_substrate_contract["runtime_substrate"], "temporal")
        self.assertEqual(runtime_substrate_contract["stage_executor_owner"], "codex_cli")
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
        self.assertEqual(
            payload["grant_direct_entry"],
            {
                "entry_version": 1,
                "entry_kind": "grant_direct_entry",
                "target_domain_id": "med-autogrant",
                "workspace_surface_kind": "nsfc_workspace",
                "task_intent": "tighten-grant-mainline",
                "workspace_overview": {
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
                "workspace_status": "attention_required",
                "workspace_alerts": [
                    "必要性表述仍略偏现象描述。",
                ],
                "progress_projection": {
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
                "current_stage_route": _expected_route("critique", source_stage="critique"),
                "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                "direct_entry": {
                    "entry_version": 1,
                    "entry_kind": "med_auto_grant_product_entry",
                    "target_domain_id": "med-autogrant",
                    "task_intent": "tighten-grant-mainline",
                    "entry_mode": "direct",
                    "workspace_locator": {
                        "workspace_surface_kind": "nsfc_workspace",
                        "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    },
                    "runtime_session_contract": {
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        "session_handle_kind": "grant_run_id",
                        "session_owner": "one-person-lab",
                        "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
                        "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
                        "domain_authority_surface_ref": "/product_entry_manifest/owner_receipt_contract",
                        "runtime_substrate_contract": runtime_substrate_contract,
                        "runtime_state_contract": {
                            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                            "session_state_owner": "one-person-lab",
                            "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
                            "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
                            "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                            "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                            "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                            "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                            "non_repo_tracked": True,
                        },
                    },
                    "return_surface_contract": {
                        **expected_return_surface_contract,
                    },
                    "domain_payload": {
                        "workspace_id": "nsfc-demo-001",
                        "draft_id": "draft-v1",
                        "funding_call": "nsfc-2026-general",
                    },
                    "stage_snapshot": {
                        "lifecycle_stage": "critique",
                        "checkpoint_status": "forward_progress",
                        "recommended_next_stage": "revision",
                    },
                    "executor_routing_contract": {
                        "contract_version": 1,
                        "current_stage_route": _expected_route("critique", source_stage="critique"),
                        "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                        "author_side_route_catalog": [
                            _expected_route(route_id, source_stage=route_id)
                            for route_id in AUTHOR_SIDE_ROUTE_IDS
                        ],
                    },
                },
                "opl_handoff_entry": {
                    "entry_version": 1,
                    "entry_kind": "med_auto_grant_product_entry",
                    "target_domain_id": "med-autogrant",
                    "task_intent": "tighten-grant-mainline",
                    "entry_mode": "opl-handoff",
                    "workspace_locator": {
                        "workspace_surface_kind": "nsfc_workspace",
                        "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    },
                    "runtime_session_contract": {
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        "session_handle_kind": "grant_run_id",
                        "session_owner": "one-person-lab",
                        "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
                        "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
                        "domain_authority_surface_ref": "/product_entry_manifest/owner_receipt_contract",
                        "runtime_substrate_contract": runtime_substrate_contract,
                        "runtime_state_contract": {
                            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                            "session_state_owner": "one-person-lab",
                            "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
                            "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
                            "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                            "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                            "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                            "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                            "non_repo_tracked": True,
                        },
                    },
                    "return_surface_contract": {
                        **expected_return_surface_contract,
                    },
                    "domain_payload": {
                        "workspace_id": "nsfc-demo-001",
                        "draft_id": "draft-v1",
                        "funding_call": "nsfc-2026-general",
                    },
                    "stage_snapshot": {
                        "lifecycle_stage": "critique",
                        "checkpoint_status": "forward_progress",
                        "recommended_next_stage": "revision",
                    },
                    "executor_routing_contract": {
                        "contract_version": 1,
                        "current_stage_route": _expected_route("critique", source_stage="critique"),
                        "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                        "author_side_route_catalog": [
                            _expected_route(route_id, source_stage=route_id)
                            for route_id in AUTHOR_SIDE_ROUTE_IDS
                        ],
                    },
                },
            },
        )
