from __future__ import annotations

__test__ = False

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryCoreSurfaceTest(unittest.TestCase):
    def test_product_entry_builds_shared_envelope_for_direct_and_opl_handoff(self) -> None:
        from med_autogrant.domain_entry_contract import build_domain_entry_contract
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()

        direct_payload = entry.build(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        handoff_payload = entry.build(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="opl-handoff",
            task_intent="tighten-grant-mainline",
        )

        direct_envelope = direct_payload["product_entry"]
        handoff_envelope = handoff_payload["product_entry"]

        self.assertEqual(direct_payload["command"], "build-product-entry")
        self.assertEqual(direct_payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(direct_payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(direct_payload["draft_id"], "draft-v1")
        self.assertEqual(direct_payload["lifecycle_stage"], "critique")

        self.assertEqual(direct_envelope["entry_kind"], "med_auto_grant_product_entry")
        self.assertEqual(direct_envelope["entry_version"], 1)
        self.assertEqual(direct_envelope["target_domain_id"], "med-autogrant")
        self.assertEqual(direct_envelope["task_intent"], "tighten-grant-mainline")
        self.assertEqual(direct_envelope["entry_mode"], "direct")
        self.assertEqual(handoff_envelope["entry_mode"], "opl-handoff")

        self.assertEqual(direct_envelope["workspace_locator"], handoff_envelope["workspace_locator"])
        self.assertEqual(direct_envelope["runtime_session_contract"], handoff_envelope["runtime_session_contract"])
        self.assertEqual(direct_envelope["return_surface_contract"], handoff_envelope["return_surface_contract"])
        self.assertEqual(direct_envelope["domain_payload"], handoff_envelope["domain_payload"])
        self.assertEqual(direct_envelope["stage_snapshot"], handoff_envelope["stage_snapshot"])

        self.assertEqual(
            direct_envelope["workspace_locator"],
            {
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
            },
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["session_handle_kind"],
            "grant_run_id",
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["grant_run_id"],
            "grant-run-nsfc-demo-001-baseline-001",
        )
        self.assertEqual(direct_envelope["runtime_session_contract"]["start_entry"], "runtime-run")
        self.assertEqual(direct_envelope["runtime_session_contract"]["resume_entry"], "runtime-resume")
        self.assertEqual(
            direct_envelope["return_surface_contract"]["entry_adapter"],
            "MedAutoGrantDomainEntry",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["domain_entry_contract"],
            build_domain_entry_contract(),
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["checkpoint_aggregation_surface"],
            "stage-route-report",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["session_continuity"]["surface_kind"],
            "session_continuity",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["progress_projection"]["surface_kind"],
            "progress_projection",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["artifact_inventory"]["surface_kind"],
            "artifact_inventory",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["runtime_control"]["surface_kind"],
            "runtime_control",
        )
        self.assertEqual(
            direct_envelope["domain_payload"],
            {
                "workspace_id": "nsfc-demo-001",
                "draft_id": "draft-v1",
                "funding_call": "nsfc-2026-general",
            },
        )
        self.assertEqual(
            direct_envelope["stage_snapshot"],
            {
                "lifecycle_stage": "critique",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "revision",
            },
        )
        self.assertEqual(
            direct_envelope["executor_routing_contract"],
            {
                "contract_version": 1,
                "current_stage_route": _expected_route("critique", source_stage="critique"),
                "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                "author_side_route_catalog": [
                    _expected_route(route_id, source_stage=route_id)
                    for route_id in AUTHOR_SIDE_ROUTE_IDS
                ],
            },
        )

    def test_product_entry_surfaces_revision_completed_reroute_to_critique_handoff(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build(
            input_path=str(REVISION_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )

        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(
            payload["product_entry"]["stage_snapshot"],
            {
                "lifecycle_stage": "revision",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "critique",
            },
        )
        self.assertEqual(
            payload["product_entry"]["executor_routing_contract"],
            {
                "contract_version": 1,
                "current_stage_route": _expected_route("revision", source_stage="revision"),
                "recommended_executor_route": _expected_route("critique", source_stage="revision"),
                "author_side_route_catalog": [
                    _expected_route(route_id, source_stage=route_id)
                    for route_id in AUTHOR_SIDE_ROUTE_IDS
                ],
            },
        )

    def test_product_entry_contextualizes_drafting_and_frozen_pending_handoff_matrix(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        drafting_payload = MedAutoGrantProductEntry().build(
            input_path=str(DRAFTING_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        drafting_contract = drafting_payload["product_entry"]["executor_routing_contract"]
        self.assertEqual(
            drafting_contract["current_stage_route"],
            _expected_route("drafting", source_stage="drafting"),
        )
        self.assertEqual(
            drafting_contract["recommended_executor_route"],
            _expected_route("critique", source_stage="drafting"),
        )
        self.assertNotIn("handoff_requirements", drafting_contract["recommended_executor_route"])
        self.assertEqual(
            [
                route["route_id"]
                for route in drafting_contract["author_side_route_catalog"]
            ],
            list(AUTHOR_SIDE_ROUTE_IDS),
        )

        frozen_payload = MedAutoGrantProductEntry().build(
            input_path=str(FROZEN_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        self.assertEqual(
            frozen_payload["product_entry"]["executor_routing_contract"]["current_stage_route"],
            _expected_route("frozen", source_stage="frozen"),
        )

    def test_product_entry_fails_closed_on_blank_task_intent(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with self.assertRaisesRegex(WorkspaceStateError, "task_intent"):
            MedAutoGrantProductEntry().build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="   ",
            )

    def test_product_entry_rejects_missing_workspace_identity_from_stage_snapshot(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        domain_entry = Mock()
        domain_entry.dispatch.side_effect = [
            {
                "ok": True,
                "grant_run_id": "grant-run-test",
                "workspace_id": None,
                "lifecycle_stage": "critique",
                "verification_checkpoint": {
                    "checkpoint_status": "forward_progress",
                    "identity": {
                        "draft_id": "draft-test",
                    },
                },
                "route": {
                    "next_step": {
                        "recommended_stage": "revision",
                    }
                },
            },
            {
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "intake_snapshot": {
                    "funding_program": "nsfc-2026-general",
                },
            },
        ]

        with self.assertRaisesRegex(WorkspaceStateError, "workspace_id"):
            MedAutoGrantProductEntry(domain_entry=domain_entry).build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="tighten-grant-mainline",
            )

    def test_product_entry_fails_closed_on_invalid_executor_routing_contract_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.entry._build_executor_routing_contract",
            return_value={
                "contract_version": 1,
                "current_stage_route": {
                    "route_id": "critique",
                    "route_status": "pending",
                },
            },
            ):
                with self.assertRaises(WorkspaceStateError):
                    MedAutoGrantProductEntry().build(
                        input_path=str(CRITIQUE_EXAMPLE_PATH),
                        entry_mode="direct",
                        task_intent="tighten-grant-mainline",
                    )

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
        self.assertEqual(
            payload["progress_projection"],
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
        self.assertEqual(
            payload["progress_projection"],
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
            },
        )

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
        self.assertEqual(runtime_control["runtime_owner"], "upstream_hermes_agent")
        self.assertEqual(runtime_control["domain_owner"], "med-autogrant")
        self.assertEqual(runtime_control["executor_owner"], "med-autogrant")
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
                        "start_entry": "runtime-run",
                        "resume_entry": "runtime-resume",
                        "runtime_substrate_contract": {
                            "runtime_owner": "Hermes",
                            "current_owner_line": "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers",
                            "active_phase": "P4 mature direct grant product entry",
                            "active_tranche": "P4.G authoring-quality-first completion semantics alignment",
                            "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                            "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                        },
                        "runtime_state_contract": {
                            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                            "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
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
                        "start_entry": "runtime-run",
                        "resume_entry": "runtime-resume",
                        "runtime_substrate_contract": {
                            "runtime_owner": "Hermes",
                            "current_owner_line": "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers",
                            "active_phase": "P4 mature direct grant product entry",
                            "active_tranche": "P4.G authoring-quality-first completion semantics alignment",
                            "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                            "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                        },
                        "runtime_state_contract": {
                            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                            "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
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

    def test_grant_direct_entry_fails_closed_on_mismatched_entry_mode(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry.MedAutoGrantProductEntry.build",
            side_effect=[
                {
                    "ok": True,
                    "command": "build-product-entry",
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "lifecycle_stage": "critique",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "output_path": None,
                    "product_entry": {
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
                            "grant_run_id": "grant-run-test",
                            "session_handle_kind": "grant_run_id",
                            "start_entry": "runtime-run",
                            "resume_entry": "runtime-resume",
                            "runtime_substrate_contract": {
                                "runtime_owner": "Hermes",
                                "current_owner_line": "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers",
                                "active_phase": "P4 mature direct grant product entry",
                                "active_tranche": "P4.G authoring-quality-first completion semantics alignment",
                                "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                                "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                            },
                            "runtime_state_contract": {
                                "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                                "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
                                "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                                "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                                "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                                "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                                "non_repo_tracked": True,
                            },
                        },
                        "return_surface_contract": {
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "default_formal_entry": "CLI",
                            "supported_entry_modes": ["direct", "opl-handoff"],
                            "domain_entry_contract": {
                                "entry_adapter": "MedAutoGrantDomainEntry",
                                "service_safe_surface_kind": "service-safe-domain-entry-command",
                                "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                                "product_entry_kind": "med_auto_grant_product_entry",
                                "supported_entry_modes": ["direct", "opl-handoff"],
                                "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
                                "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
                            },
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
                    },
                        "domain_payload": {
                            "workspace_id": "workspace-test",
                            "draft_id": "draft-test",
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
                {
                    "ok": True,
                    "command": "build-product-entry",
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "lifecycle_stage": "critique",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "output_path": None,
                    "product_entry": {
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
                            "grant_run_id": "grant-run-test",
                            "session_handle_kind": "grant_run_id",
                            "start_entry": "runtime-run",
                            "resume_entry": "runtime-resume",
                            "runtime_substrate_contract": {
                                "runtime_owner": "Hermes",
                                "current_owner_line": "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers",
                                "active_phase": "P4 mature direct grant product entry",
                                "active_tranche": "P4.G authoring-quality-first completion semantics alignment",
                                "compatibility_bridge": "post-R5A local runtime closeout / host-agent regression oracle",
                                "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
                            },
                            "runtime_state_contract": {
                                "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
                                "session_journal_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
                                "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
                                "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
                                "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
                                "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
                                "non_repo_tracked": True,
                            },
                        },
                        "return_surface_contract": {
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "default_formal_entry": "CLI",
                            "supported_entry_modes": ["direct", "opl-handoff"],
                            "domain_entry_contract": {
                                "entry_adapter": "MedAutoGrantDomainEntry",
                                "service_safe_surface_kind": "service-safe-domain-entry-command",
                                "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
                                "product_entry_kind": "med_auto_grant_product_entry",
                                "supported_entry_modes": ["direct", "opl-handoff"],
                                "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
                                "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
                            },
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
                        },
                        "domain_payload": {
                            "workspace_id": "workspace-test",
                            "draft_id": "draft-test",
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
            ],
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_direct_entry.direct_entry"):
                MedAutoGrantProductEntry().build_grant_direct_entry(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                    task_intent="tighten-grant-mainline",
                )
