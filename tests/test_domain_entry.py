from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.domain_entry import MedAutoGrantDomainEntry  # noqa: E402
from med_autogrant.workspace import WorkspaceStateError  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class DomainEntryDispatchTest(unittest.TestCase):
    def test_domain_entry_dispatches_runtime_command(self) -> None:
        runtime = Mock()
        runtime.run_local.return_value = {"ok": True, "command": "run-local"}

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "run-local",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
                "journal_path": "/tmp/test-journal.json",
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "run-local"})
        runtime.run_local.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            journal_path="/tmp/test-journal.json",
        )

    def test_domain_entry_dispatches_probe_command(self) -> None:
        expected_payload = {"ok": True, "command": "probe-upstream-hermes"}
        payload = MedAutoGrantDomainEntry(
            runtime=Mock(),
            probe=lambda: expected_payload,
        ).dispatch({"command": "probe-upstream-hermes"})

        self.assertEqual(payload, expected_payload)

    def test_domain_entry_rejects_missing_required_field(self) -> None:
        with self.assertRaisesRegex(WorkspaceStateError, "缺少必填字段: output_path"):
            MedAutoGrantDomainEntry(runtime=Mock()).dispatch(
                {
                    "command": "build-artifact-bundle",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH),
                }
            )


class DomainEntryFreshProofTest(unittest.TestCase):
    def test_service_safe_domain_entry_runs_fresh_cutover_walkthrough(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            hermes_home = tmp_root / "hermes-home"
            reroute_journal_path = tmp_root / "reroute-journal.json"
            revised_workspace_path = tmp_root / "revised.json"
            revised_journal_path = tmp_root / "revised-journal.json"
            frozen_bundle_path = tmp_root / "frozen-bundle.json"
            final_package_path = tmp_root / "final-package.json"
            hosted_contract_path = tmp_root / "hosted-contract.json"

            with unittest.mock.patch.dict(
                os.environ,
                {"MED_AUTOGRANT_HERMES_HOME": str(hermes_home)},
                clear=False,
            ):
                entry = MedAutoGrantDomainEntry()

                probe_payload = entry.dispatch({"command": "probe-upstream-hermes"})
                self.assertTrue(probe_payload["ok"])
                self.assertEqual(Path(probe_payload["runtime_root"]), hermes_home.resolve())
                self.assertEqual(Path(probe_payload["state_db_path"]), (hermes_home / "state.db").resolve())

                critique_report = entry.dispatch(
                    {
                        "command": "stage-route-report",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                    }
                )
                self.assertTrue(critique_report["ok"])
                self.assertEqual(
                    critique_report["verification_checkpoint"]["identity"]["grant_run_id"],
                    "grant-run-nsfc-demo-001-baseline-001",
                )

                reroute_payload = entry.dispatch(
                    {
                        "command": "run-local",
                        "input_path": str(REVISION_EXAMPLE_PATH),
                        "journal_path": str(reroute_journal_path),
                    }
                )
                self.assertTrue(reroute_payload["ok"])
                self.assertEqual(reroute_payload["stop_reason"]["recommended_next_stage"], "critique")
                self.assertEqual(
                    reroute_payload["stage_action_envelope"]["executor_routing_contract"]["recommended_executor_route"],
                    {
                        "route_id": "critique",
                        "route_status": "pending",
                        "executor_owner": "med-autogrant",
                        "execution_surface": None,
                        "handoff_contract_kind": "handoff-required",
                        "handoff_requirements": {
                            "contract_kind": "critique-pending-handoff",
                            "workspace_surface_kind": "nsfc_workspace",
                            "required_domain_surfaces": [
                                {
                                    "surface_kind": "service-safe-domain-entry-command",
                                    "entry_adapter": "MedAutoGrantDomainEntry",
                                    "command": "summarize-workspace",
                                },
                                {
                                    "surface_kind": "service-safe-domain-entry-command",
                                    "entry_adapter": "MedAutoGrantDomainEntry",
                                    "command": "critique-summary",
                                },
                                {
                                    "surface_kind": "service-safe-domain-entry-command",
                                    "entry_adapter": "MedAutoGrantDomainEntry",
                                    "command": "stage-route-report",
                                },
                            ],
                            "required_identity_fields": [
                                "grant_run_id",
                                "workspace_id",
                                "draft_id",
                            ],
                        },
                    },
                )

                revision_payload = entry.dispatch(
                    {
                        "command": "execute-revision-pass",
                        "input_path": str(RE_REVIEW_EXAMPLE_PATH),
                        "output_path": str(revised_workspace_path),
                    }
                )
                self.assertTrue(revision_payload["ok"])
                self.assertEqual(revision_payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")

                run_payload = entry.dispatch(
                    {
                        "command": "run-local",
                        "input_path": str(revised_workspace_path),
                        "journal_path": str(revised_journal_path),
                    }
                )
                self.assertTrue(run_payload["ok"])
                self.assertEqual(run_payload["attempt_index"], 1)
                self.assertEqual(run_payload["stop_reason"]["recommended_next_stage"], "revision")

                resume_payload = entry.dispatch(
                    {
                        "command": "resume-local",
                        "journal_path": str(revised_journal_path),
                    }
                )
                self.assertTrue(resume_payload["ok"])
                self.assertEqual(resume_payload["attempt_index"], 2)
                self.assertEqual(resume_payload["stop_reason"]["recommended_next_stage"], "revision")

                bundle_payload = entry.dispatch(
                    {
                        "command": "build-artifact-bundle",
                        "input_path": str(FROZEN_EXAMPLE_PATH),
                        "output_path": str(frozen_bundle_path),
                    }
                )
                self.assertTrue(bundle_payload["ok"])

                final_package_payload = entry.dispatch(
                    {
                        "command": "build-final-package",
                        "input_path": str(FROZEN_EXAMPLE_PATH),
                        "artifact_bundle_path": str(frozen_bundle_path),
                        "output_path": str(final_package_path),
                    }
                )
                self.assertTrue(final_package_payload["ok"])

                hosted_contract_payload = entry.dispatch(
                    {
                        "command": "build-hosted-contract-bundle",
                        "final_package_path": str(final_package_path),
                        "output_path": str(hosted_contract_path),
                    }
                )

        self.assertTrue(hosted_contract_payload["ok"])
        self.assertEqual(
            hosted_contract_payload["hosted_contract_bundle"]["execution_identity"],
            {
                "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                "workspace_id": "nsfc-demo-001",
                "draft_id": "draft-v1",
                "program_id": "med-autogrant-mainline",
            },
        )


if __name__ == "__main__":
    unittest.main()
