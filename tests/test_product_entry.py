from __future__ import annotations

import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.workspace import WorkspaceStateError  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"


class ProductEntryCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(list(args))
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


class ProductEntryEnvelopeTest(unittest.TestCase):
    def test_product_entry_builds_shared_envelope_for_direct_and_opl_handoff(self) -> None:
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
        self.assertEqual(direct_envelope["runtime_session_contract"]["start_entry"], "run-local")
        self.assertEqual(direct_envelope["runtime_session_contract"]["resume_entry"], "resume-local")
        self.assertEqual(
            direct_envelope["return_surface_contract"]["entry_adapter"],
            "MedAutoGrantDomainEntry",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["checkpoint_aggregation_surface"],
            "stage-route-report",
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
                "current_stage_route": {
                    "route_id": "critique",
                    "route_status": "pending",
                    "executor_owner": "med-autogrant",
                    "execution_surface": None,
                    "handoff_contract_kind": "handoff-required",
                },
                "recommended_executor_route": {
                    "route_id": "revision",
                    "route_status": "landed",
                    "executor_owner": "med-autogrant",
                    "execution_surface": {
                        "surface_kind": "service-safe-domain-entry-command",
                        "entry_adapter": "MedAutoGrantDomainEntry",
                        "command": "execute-revision-pass",
                    },
                    "handoff_contract_kind": "service-safe-domain-entry-command",
                },
                "author_side_route_catalog": [
                    {
                        "route_id": "critique",
                        "route_status": "pending",
                        "executor_owner": "med-autogrant",
                        "execution_surface": None,
                        "handoff_contract_kind": "handoff-required",
                    },
                    {
                        "route_id": "revision",
                        "route_status": "landed",
                        "executor_owner": "med-autogrant",
                        "execution_surface": {
                            "surface_kind": "service-safe-domain-entry-command",
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "command": "execute-revision-pass",
                        },
                        "handoff_contract_kind": "service-safe-domain-entry-command",
                    },
                    {
                        "route_id": "artifact_bundle",
                        "route_status": "landed",
                        "executor_owner": "med-autogrant",
                        "execution_surface": {
                            "surface_kind": "service-safe-domain-entry-command",
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "command": "build-artifact-bundle",
                        },
                        "handoff_contract_kind": "service-safe-domain-entry-command",
                    },
                    {
                        "route_id": "final_package",
                        "route_status": "landed",
                        "executor_owner": "med-autogrant",
                        "execution_surface": {
                            "surface_kind": "service-safe-domain-entry-command",
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "command": "build-final-package",
                        },
                        "handoff_contract_kind": "service-safe-domain-entry-command",
                    },
                    {
                        "route_id": "hosted_contract_bundle",
                        "route_status": "landed",
                        "executor_owner": "med-autogrant",
                        "execution_surface": {
                            "surface_kind": "service-safe-domain-entry-command",
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "command": "build-hosted-contract-bundle",
                        },
                        "handoff_contract_kind": "service-safe-domain-entry-command",
                    },
                ],
            },
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


if __name__ == "__main__":
    unittest.main()
