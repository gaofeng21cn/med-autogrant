from __future__ import annotations

import json
import unittest
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
from io import StringIO
from unittest.mock import patch
from argparse import _SubParsersAction
from med_autogrant.cli import build_parser, main
from med_autogrant.public_cli import public_cli_command
from support.cli import public_cli_argv
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_public_groups_are_registered_directly_without_flat_grouped_wrapper(self) -> None:
        parser = build_parser()
        root_subparsers = next(
            action for action in parser._actions if isinstance(action, _SubParsersAction)
        )

        self.assertIn("workspace", root_subparsers.choices)
        self.assertIn("authority", root_subparsers.choices)
        self.assertIn("domain-handler", root_subparsers.choices)
        self.assertNotIn("validate-workspace", root_subparsers.choices)
        workspace_parser = root_subparsers.choices["workspace"]
        workspace_subparsers = next(
            action
            for action in workspace_parser._actions
            if isinstance(action, _SubParsersAction)
        )
        self.assertIn("validate", workspace_subparsers.choices)
        self.assertNotIn("validate-workspace", workspace_subparsers.choices)

    def test_product_group_is_retired_from_public_cli(self) -> None:
        for command in (
            ("product", "build-entry"),
            ("product", "status"),
            ("product", "user-loop"),
            ("product", "direct-entry"),
            ("product", "manifest"),
            ("product", "preflight"),
            ("product", "start"),
            ("product", "domain_handler", "export"),
            ("product", "domain_handler", "dispatch"),
            ("workspace", "progress"),
            ("workspace", "cockpit"),
        ):
            with self.subTest(command=command):
                exit_code, stdout, stderr = self.run_cli(
                    *command,
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH),
                    "--format",
                    "json",
                )
                self.assertEqual(exit_code, 2)
                self.assertEqual(stdout, "")
                if command[0] == "workspace":
                    self.assertIn(
                        f"argument public_command: invalid choice: '{command[1]}'",
                        stderr,
                    )
                else:
                    self.assertIn(f"invalid choice: '{command[0]}'", stderr)

    def test_flat_product_status_alias_has_no_special_compatibility_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-status",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("invalid choice: 'product-status'", stderr)

    def test_generated_surface_commands_are_refs_not_repo_local_shells(self) -> None:
        for command in (
            "grant-progress",
            "grant-cockpit",
            "grant-direct-entry",
            "grant-user-loop",
            "skill-catalog",
            "product-entry-manifest",
            "product-status",
            "build-product-entry",
        ):
            with self.subTest(command=command):
                rendered = public_cli_command(command, "--input", "<input_path>", "--format", "json")
                self.assertTrue(rendered.startswith("opl://generated-surfaces/mag/"))
                self.assertNotIn("python -m med_autogrant", rendered)

    def test_domain_handler_group_is_repo_local_standard_target(self) -> None:
        export_command = public_cli_command("domain-handler-export", "--input", "<input_path>", "--format", "json")
        dispatch_command = public_cli_command(
            "domain-handler-dispatch",
            "--task",
            "<task_path>",
            "--format",
            "json",
        )

        self.assertEqual(
            export_command,
            "uv run python -m med_autogrant domain-handler export --input <input_path> --format json",
        )
        self.assertEqual(
            dispatch_command,
            "uv run python -m med_autogrant domain-handler dispatch --task <task_path> --format json",
        )

    def test_domain_memory_writeback_proposal_dispatches_authority_target(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "domain-memory-writeback-proposal",
            "domain_memory_writeback_proposal": {
                "surface_kind": "mag_domain_memory_writeback_proposal",
            },
        }

        with patch(
            "med_autogrant.cli_parts.handlers.build_domain_memory_writeback_proposal",
            return_value=expected_payload,
        ) as build_proposal:

            exit_code, stdout, stderr = self.run_cli(
                "authority",
                "memory-proposal",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--stage-id",
                "review_and_rebuttal",
                "--source-ref",
                "runtime-closeout://grant-run/example",
                "--lesson-summary",
                "Keep reusable reviewer risk framing as strategy memory.",
                "--proposal-id",
                "review-risk-framing",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        build_proposal.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            stage_id="review_and_rebuttal",
            source_ref="runtime-closeout://grant-run/example",
            lesson_summary="Keep reusable reviewer risk framing as strategy memory.",
            proposal_id="review-risk-framing",
        )

    def test_domain_memory_writeback_decision_dispatches_authority_target(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "domain-memory-writeback-decision",
            "domain_memory_writeback_decision": {
                "surface_kind": "mag_domain_memory_writeback_decision",
            },
        }

        with patch(
            "med_autogrant.cli_parts.handlers.build_domain_memory_writeback_decision",
            return_value=expected_payload,
        ) as build_decision:

            exit_code, stdout, stderr = self.run_cli(
                "authority",
                "memory-decision",
                "--proposal",
                "/tmp/proposal.json",
                "--decision",
                "accepted",
                "--decision-reason",
                "Reusable strategy memory.",
                "--memory-id",
                "review-risk-framing",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        build_decision.assert_called_once_with(
            proposal_path="/tmp/proposal.json",
            decision="accepted",
            decision_reason="Reusable strategy memory.",
            memory_id="review-risk-framing",
        )

    def test_domain_memory_receipt_evidence_dispatches_authority_target(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "domain-memory-receipt-evidence",
            "domain_memory_receipt_evidence": {
                "surface_kind": "mag_domain_memory_runtime_receipt_evidence",
            },
        }

        with patch(
            "med_autogrant.cli_parts.handlers.write_domain_memory_receipt_evidence",
            return_value=expected_payload,
        ) as write_receipt:

            exit_code, stdout, stderr = self.run_cli(
                "authority",
                "memory-receipt-evidence",
                "--decision",
                "/tmp/decision.json",
                "--runtime-root",
                "/tmp/runtime-state",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        write_receipt.assert_called_once_with(
            decision_payload="/tmp/decision.json",
            runtime_root="/tmp/runtime-state",
        )

    def test_owner_receipt_evidence_dispatches_authority_target(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "owner-receipt-evidence",
            "owner_receipt_evidence": {
                "surface_kind": "mag_owner_receipt_evidence",
            },
        }

        with patch(
            "med_autogrant.cli_parts.handlers.write_owner_receipt_evidence",
            return_value=expected_payload,
        ) as write_receipt:

            exit_code, stdout, stderr = self.run_cli(
                "authority",
                "owner-receipt-evidence",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--receipt-shape",
                "no_regression_evidence",
                "--stage-id",
                "review_and_rebuttal",
                "--source-ref",
                "opl-stage-attempt://attempt-1",
                "--closeout-summary",
                "No regression evidence.",
                "--runtime-root",
                "/tmp/runtime-state",
                "--receipt-id",
                "attempt-1",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        write_receipt.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            receipt_shape="no_regression_evidence",
            stage_id="review_and_rebuttal",
            source_ref="opl-stage-attempt://attempt-1",
            closeout_summary="No regression evidence.",
            runtime_root="/tmp/runtime-state",
            receipt_id="attempt-1",
        )
