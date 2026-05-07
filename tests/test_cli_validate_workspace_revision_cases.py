from __future__ import annotations

from cli_validate_cases import *  # noqa: F401,F403



class CliValidateWorkspaceRevisionCasesTest(CliValidateWorkspaceTest):
    def test_stage_route_report_aggregates_p2a_question_refinement_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(QUESTION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "question_refinement")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "argument_building")
        self.assertEqual(payload["checkpoint_status"], "forward_progress")
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "forward_progress")
        self.assertEqual(
            payload["verification_checkpoint"]["route_alignment"]["recommended_next_stage"],
            "argument_building",
        )
        self.assertEqual(
            payload["route"]["summarize_workspace"]["current_selection"]["selected_question_id"],
            "question-immune-fibrosis",
        )
        self.assertNotIn("critique_summary", payload["route"])

    def test_stage_route_report_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("下一阶段: 修订落实", stdout)
        self.assertIn("当前 checkpoint: 继续向前推进", stdout)
        self.assertIn("当前判断: 批注结论 major_revision", stdout)
        self.assertNotIn("recommended_stage:", stdout)
        self.assertNotIn("checkpoint_status:", stdout)

    def test_next_step_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("下一阶段: 修订落实", stdout)
        self.assertIn("当前判断: 导师批注 verdict=major_revision，应先执行结构化修订。", stdout)
        self.assertIn("- 建议动作: 执行 revision plan 中的 P0/P1 项。", stdout)
        self.assertNotIn("current_stage:", stdout)
        self.assertNotIn("recommended_stage:", stdout)
        self.assertNotIn("reason:", stdout)

    def test_stage_route_report_aggregates_p2b_outline_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(OUTLINE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "outline")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "drafting")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_fit_mapping"]["id"], "fit-001")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_draft"]["id"], "draft-outline-v1")
        self.assertNotIn("critique_summary", payload["route"])

    def test_stage_route_report_aggregates_p2c_drafting_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(DRAFTING_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "critique")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_draft"]["section_count"], 3)
        self.assertNotIn("critique_summary", payload["route"])

    def test_critique_summary_exposes_revision_audit_for_p2c_critique(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["critique_id"], "critique-v1")
        self.assertEqual(payload["revision_plan_id"], "revision-v1")
        self.assertEqual(payload["execution_status"], "planned")
        self.assertEqual(payload["recommended_next_stage"], "revision")

    def test_grant_cockpit_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-cockpit",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前状态: 需要处理", stdout)
        self.assertIn("当前判断: 必要性表述仍略偏现象描述。", stdout)
        self.assertIn("- 可用命令 build_direct_entry:", stdout)
        self.assertNotIn("workspace_status:", stdout)
        self.assertNotIn("- alert:", stdout)

    def test_grant_direct_entry_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-direct-entry",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--task-intent",
            "tighten-grant-mainline",
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("当前状态: 需要处理", stdout)
        self.assertIn("推荐执行路径: 修订落实", stdout)
        self.assertIn("当前判断: 必要性表述仍略偏现象描述。", stdout)
        self.assertNotIn("workspace_status:", stdout)
        self.assertNotIn("recommended_route:", stdout)
        self.assertNotIn("- alert:", stdout)

    def test_critique_summary_exposes_completed_revision_evidence_for_p2c_revision(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["execution_status"], "completed")
        self.assertEqual(payload["pre_revision_version_label"], "v0.3")
        self.assertEqual(payload["post_revision_version_label"], "v0.4")
        self.assertIn("比较", payload["comparison_summary"])
        self.assertEqual(payload["recommended_next_stage"], "critique")

    def test_critique_summary_exposes_major_reframe_verdict(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(MAJOR_REFRAME_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["verdict"], "major_reframe")
        self.assertEqual(payload["recommended_next_stage"], "question_refinement")

    def test_critique_summary_exposes_ready_for_submission_verdict(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["verdict"], "ready_for_submission")
        self.assertEqual(payload["recommended_next_stage"], "frozen")

    def test_stage_route_report_aggregates_p2c_critique_with_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
        self.assertEqual(payload["route"]["critique_summary"]["execution_status"], "planned")

    def test_stage_route_report_aggregates_p2c_revision_with_re_review_boundary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "critique")
        self.assertEqual(payload["route"]["critique_summary"]["execution_status"], "completed")

    def test_stage_route_report_aggregates_p3a_major_reframe_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(MAJOR_REFRAME_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "question_refinement")
        self.assertEqual(payload["route"]["critique_summary"]["verdict"], "major_reframe")

    def test_stage_route_report_aggregates_p3a_ready_for_submission_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "frozen")
        self.assertEqual(payload["route"]["critique_summary"]["verdict"], "ready_for_submission")
        self.assertFalse(payload["route"]["critique_summary"]["presubmission_frozen"])
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "freeze_ready")
        self.assertFalse(payload["verification_checkpoint"]["route_alignment"]["presubmission_frozen"])

    def test_validate_workspace_accepts_re_review_critique_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_validate_workspace_accepts_forced_rollback_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_validate_workspace_accepts_presubmission_frozen_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "frozen")

    def test_generated_revised_workspace_reenters_validator_and_checkpoint_surfaces(self) -> None:
        cases = (
            (CRITIQUE_EXAMPLE_PATH, "v0.4", None),
            (RE_REVIEW_EXAMPLE_PATH, "v0.5", "revision-v1"),
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            for input_path, expected_version_label, expected_reviewed_revision_plan_id in cases:
                with self.subTest(example=input_path.name):
                    revised_path = tmp_path / f"{input_path.stem}-revised.json"
                    revised_payload = self.run_json_cli(
                        "execute-revision-pass",
                        "--input",
                        str(input_path),
                        "--output",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertTrue(revised_payload["ok"])

                    validate_payload = self.run_json_cli(
                        "validate-workspace",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertTrue(validate_payload["ok"])
                    self.assertEqual(validate_payload["lifecycle_stage"], "critique")

                    summary_payload = self.run_json_cli(
                        "summarize-workspace",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertEqual(summary_payload["active_draft"]["status"], "revised")
                    self.assertEqual(summary_payload["active_draft"]["version_label"], expected_version_label)
                    self.assertEqual(summary_payload["active_revision_plan"]["execution_status"], "completed")

                    next_step_payload = self.run_json_cli(
                        "next-step",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertEqual(next_step_payload["current_stage"], "critique")
                    self.assertEqual(next_step_payload["recommended_stage"], "revision")

                    critique_payload = self.run_json_cli(
                        "critique-summary",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertEqual(critique_payload["draft_status"], "revised")
                    self.assertEqual(critique_payload["draft_version_label"], expected_version_label)
                    self.assertEqual(critique_payload["execution_status"], "completed")
                    self.assertEqual(
                        critique_payload["reviewed_revision_plan_id"],
                        expected_reviewed_revision_plan_id,
                    )

                    route_payload = self.run_json_cli(
                        "stage-route-report",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertTrue(route_payload["ok"])
                    self.assertEqual(route_payload["lifecycle_stage"], "critique")
                    self.assertEqual(route_payload["route"]["next_step"]["recommended_stage"], "revision")
                    self.assertEqual(route_payload["route"]["summarize_workspace"]["active_draft"]["status"], "revised")
                    self.assertEqual(
                        route_payload["route"]["summarize_workspace"]["active_draft"]["version_label"],
                        expected_version_label,
                    )
                    self.assertEqual(route_payload["route"]["critique_summary"]["execution_status"], "completed")
                    self.assertEqual(route_payload["verification_checkpoint"]["checkpoint_status"], "forward_progress")
                    self.assertEqual(
                        route_payload["verification_checkpoint"]["route_alignment"]["recommended_next_stage"],
                        "revision",
                    )
                    self.assertEqual(
                        route_payload["verification_checkpoint"]["review_checkpoint"]["reviewed_revision_evidence"],
                        route_payload["route"]["summarize_workspace"]["reviewed_revision_evidence"],
                    )
                    self.assertEqual(
                        route_payload["route"]["critique_summary"]["reviewed_revision_plan_id"],
                        expected_reviewed_revision_plan_id,
                    )

    def test_critique_summary_exposes_re_review_linkage(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["critique_id"], "critique-v2")
        self.assertEqual(payload["revision_plan_id"], "revision-v2")
        self.assertEqual(payload["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["reviewed_revision_evidence"]["post_revision_version_label"], "v0.4")

    def test_critique_summary_exposes_forced_rollback_fields(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["critique_id"], "critique-v2")
        self.assertEqual(payload["forced_rollback_stage"], "argument_building")
        self.assertEqual(payload["forced_rollback_reason"], "当前必要性链条已经失真，必须回到 argument chain 重建。")
        self.assertFalse(payload["presubmission_frozen"])
        self.assertEqual(payload["recommended_next_stage"], "argument_building")

    def test_critique_summary_exposes_presubmission_frozen_fields(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertEqual(payload["verdict"], "ready_for_submission")
        self.assertTrue(payload["presubmission_frozen"])
        self.assertEqual(payload["recommended_next_stage"], "frozen")

    def test_summarize_workspace_exposes_re_review_evidence(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["active_critique"]["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["reviewed_revision_evidence"]["source_critique_id"], "critique-v1")

    def test_summarize_workspace_exposes_forced_rollback_evidence(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["active_critique"]["forced_rollback_stage"], "argument_building")
        self.assertEqual(payload["active_critique"]["forced_rollback_reason"], "当前必要性链条已经失真，必须回到 argument chain 重建。")
        self.assertFalse(payload["gates"]["presubmission_frozen"])

    def test_summarize_workspace_exposes_presubmission_frozen_gate(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertTrue(payload["gates"]["presubmission_frozen"])
        self.assertEqual(payload["active_draft"]["status"], "frozen")

    def test_stage_route_report_aggregates_p3b_re_review_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
        self.assertEqual(payload["checkpoint_status"], "forward_progress")
        self.assertEqual(payload["route"]["summarize_workspace"]["reviewed_revision_evidence"]["revision_plan_id"], "revision-v1")
        self.assertEqual(payload["route"]["critique_summary"]["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "forward_progress")
        self.assertEqual(
            payload["verification_checkpoint"]["review_checkpoint"]["reviewed_revision_evidence"]["revision_plan_id"],
            "revision-v1",
        )

    def test_stage_route_report_aggregates_p3c_forced_rollback_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "argument_building")
        self.assertEqual(payload["route"]["next_step"]["forced_rollback_stage"], "argument_building")
        self.assertEqual(payload["route"]["critique_summary"]["forced_rollback_stage"], "argument_building")
        self.assertFalse(payload["route"]["critique_summary"]["presubmission_frozen"])
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "rollback_required")
        self.assertEqual(
            payload["verification_checkpoint"]["route_alignment"]["forced_rollback_stage"],
            "argument_building",
        )

    def test_stage_route_report_aggregates_p3c_presubmission_frozen_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "frozen")
        self.assertTrue(payload["route"]["summarize_workspace"]["gates"]["presubmission_frozen"])
        self.assertTrue(payload["route"]["critique_summary"]["presubmission_frozen"])
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "submission_frozen")
        self.assertTrue(payload["verification_checkpoint"]["route_alignment"]["presubmission_frozen"])

    def test_validate_workspace_accepts_re_review_revised_output_after_execute_revision_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / "p3b-revised.json"

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(RE_REVIEW_EXAMPLE_PATH),
                "--output",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, "")
            self.assertTrue(json.loads(execute_stdout)["ok"])

            exit_code, stdout, stderr = self.run_cli(
                "validate-workspace",
                "--input",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["error_count"], 0)
            self.assertEqual(payload["errors"], [])

    def test_next_step_keeps_revised_output_on_existing_revision_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / "p2c-revised.json"

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--output",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, "")
            self.assertTrue(json.loads(execute_stdout)["ok"])

            exit_code, stdout, stderr = self.run_cli(
                "next-step",
                "--input",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertEqual(payload["current_stage"], "critique")
            self.assertEqual(payload["recommended_stage"], "revision")
            self.assertIn("major_revision", payload["reason"])

    def test_stage_route_report_accepts_re_review_revised_output_and_keeps_reviewed_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / "p3b-revised.json"

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(RE_REVIEW_EXAMPLE_PATH),
                "--output",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, "")
            self.assertTrue(json.loads(execute_stdout)["ok"])

            exit_code, stdout, stderr = self.run_cli(
                "stage-route-report",
                "--input",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["lifecycle_stage"], "critique")
            self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
            self.assertEqual(
                payload["route"]["summarize_workspace"]["reviewed_revision_evidence"]["revision_plan_id"],
                "revision-v1",
            )
            self.assertEqual(
                payload["route"]["summarize_workspace"]["active_revision_plan"]["execution_status"],
                "completed",
            )
            self.assertEqual(
                payload["verification_checkpoint"]["review_checkpoint"]["reviewed_revision_evidence"]["revision_plan_id"],
                "revision-v1",
            )
