from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


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

    def test_build_product_entry_dispatches_shell(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "build-product-entry",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "output_path": None,
            "product_entry": {
                "entry_kind": "med_auto_grant_product_entry",
                "entry_mode": "direct",
                "task_intent": "tighten-grant-mainline",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--entry-mode",
                "direct",
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
            output_path=None,
            funding_call=None,
        )

    def test_grant_progress_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-progress",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "progress_projection": {
                "projection_kind": "grant_progress",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.read_grant_progress.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "grant-progress",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.read_grant_progress.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

    def test_grant_cockpit_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-cockpit",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "grant_cockpit": {
                "cockpit_kind": "grant_cockpit",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.read_grant_cockpit.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "grant-cockpit",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.read_grant_cockpit.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

    def test_grant_direct_entry_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-direct-entry",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "grant_direct_entry": {
                "entry_kind": "grant_direct_entry",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_grant_direct_entry.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "grant-direct-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_grant_direct_entry.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
            funding_call=None,
        )

    def test_product_entry_manifest_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "product-entry-manifest",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "product_entry_manifest": {
                "manifest_kind": "med_auto_grant_product_entry_manifest",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_product_entry_manifest.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product-entry-manifest",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_product_entry_manifest.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            funding_call=None,
        )

    def test_product_preflight_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "product-preflight",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "product_entry_preflight": {
                "surface_kind": "product_entry_preflight",
                "ready_to_try_now": True,
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_product_entry_preflight.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product-preflight",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_product_entry_preflight.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
