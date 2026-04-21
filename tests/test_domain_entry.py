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
from med_autogrant.family_shared_release import inspect_current_repo_family_shared_alignment  # noqa: E402
from med_autogrant.product_entry import MedAutoGrantProductEntry  # noqa: E402
from med_autogrant.workspace import WorkspaceStateError  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
NSFC_SELECTION_INPUT = REPO_ROOT / "examples" / "profile_selection_input_nsfc_general.json"
DISCOVERY_INPUT = REPO_ROOT / "examples" / "funding_discovery_input_cardiovascular.json"


class DomainEntryDispatchTest(unittest.TestCase):
    def test_domain_entry_rejects_legacy_runtime_alias(self) -> None:
        with self.assertRaisesRegex(WorkspaceStateError, "不支持的 domain entry command: run-local"):
            MedAutoGrantDomainEntry(runtime=Mock()).dispatch(
                {
                    "command": "run-local",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH),
                }
            )

    def test_domain_entry_dispatches_runtime_command(self) -> None:
        runtime = Mock()
        runtime.run_local.return_value = {"ok": True, "command": "runtime-run"}

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "runtime-run",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
                "journal_path": "/tmp/test-journal.json",
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "runtime-run"})
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

    def test_domain_entry_dispatches_grant_intake_audit(self) -> None:
        runtime = Mock()
        runtime.grant_intake_audit.return_value = {
            "ok": True,
            "command": "grant-intake-audit",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "grant-intake-audit",
                "input_path": str(INPUT_EXAMPLE_PATH),
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "grant-intake-audit"})
        runtime.grant_intake_audit.assert_called_once_with(
            input_path=str(INPUT_EXAMPLE_PATH),
        )

    def test_domain_entry_dispatches_grant_evidence_grounding(self) -> None:
        runtime = Mock()
        runtime.grant_evidence_grounding.return_value = {
            "ok": True,
            "command": "grant-evidence-grounding",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "grant-evidence-grounding",
                "input_path": str(INPUT_EXAMPLE_PATH),
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "grant-evidence-grounding"})
        runtime.grant_evidence_grounding.assert_called_once_with(
            input_path=str(INPUT_EXAMPLE_PATH),
        )

    def test_domain_entry_dispatches_execute_critique_pass(self) -> None:
        runtime = Mock()
        runtime.execute_critique_pass.return_value = {
            "ok": True,
            "command": "execute-critique-pass",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "execute-critique-pass",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
                "output_path": "/tmp/critique-output.json",
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "execute-critique-pass"})
        runtime.execute_critique_pass.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            output_path="/tmp/critique-output.json",
        )

    def test_domain_entry_dispatches_execute_critique_pass_with_explicit_executor(self) -> None:
        runtime = Mock()
        runtime.execute_critique_pass.return_value = {
            "ok": True,
            "command": "execute-critique-pass",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "execute-critique-pass",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
                "output_path": "/tmp/critique-output.json",
                "executor_kind": "hermes_native_proof",
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "execute-critique-pass"})
        runtime.execute_critique_pass.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            output_path="/tmp/critique-output.json",
            executor_kind="hermes_native_proof",
        )

    def test_domain_entry_dispatches_execute_direction_screening_pass(self) -> None:
        runtime = Mock()
        runtime.execute_direction_screening_pass.return_value = {
            "ok": True,
            "command": "execute-direction-screening-pass",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "execute-direction-screening-pass",
                "input_path": str(INPUT_EXAMPLE_PATH),
                "output_path": "/tmp/direction-screening-output.json",
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "execute-direction-screening-pass"})
        runtime.execute_direction_screening_pass.assert_called_once_with(
            input_path=str(INPUT_EXAMPLE_PATH),
            output_path="/tmp/direction-screening-output.json",
        )

    def test_domain_entry_dispatches_select_project_profile(self) -> None:
        runtime = Mock()
        runtime.select_project_profile.return_value = {
            "ok": True,
            "command": "select-project-profile",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "select-project-profile",
                "input_path": str(NSFC_SELECTION_INPUT),
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "select-project-profile"})
        runtime.select_project_profile.assert_called_once_with(
            input_path=str(NSFC_SELECTION_INPUT),
        )

    def test_domain_entry_dispatches_initialize_intake_workspace(self) -> None:
        runtime = Mock()
        runtime.initialize_intake_workspace.return_value = {
            "ok": True,
            "command": "initialize-intake-workspace",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "initialize-intake-workspace",
                "input_path": str(NSFC_SELECTION_INPUT),
                "output_path": "/tmp/initialized-workspace.json",
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "initialize-intake-workspace"})
        runtime.initialize_intake_workspace.assert_called_once_with(
            input_path=str(NSFC_SELECTION_INPUT),
            output_path="/tmp/initialized-workspace.json",
        )

    def test_domain_entry_dispatches_discover_funding_opportunities(self) -> None:
        runtime = Mock()
        runtime.discover_funding_opportunities.return_value = {
            "ok": True,
            "command": "discover-funding-opportunities",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "discover-funding-opportunities",
                "input_path": str(DISCOVERY_INPUT),
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "discover-funding-opportunities"})
        runtime.discover_funding_opportunities.assert_called_once_with(
            input_path=str(DISCOVERY_INPUT),
        )

    def test_domain_entry_dispatches_execute_critique_revision_loop(self) -> None:
        runtime = Mock()
        runtime.execute_critique_revision_loop.return_value = {
            "ok": True,
            "command": "execute-critique-revision-loop",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "execute-critique-revision-loop",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
                "output_dir": "/tmp/critique-loop",
                "max_rounds": 4,
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "execute-critique-revision-loop"})
        runtime.execute_critique_revision_loop.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            output_dir="/tmp/critique-loop",
            max_rounds=4,
        )

    def test_domain_entry_dispatches_execute_authoring_mainline_loop(self) -> None:
        runtime = Mock()
        runtime.execute_authoring_mainline_loop.return_value = {
            "ok": True,
            "command": "execute-authoring-mainline-loop",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "execute-authoring-mainline-loop",
                "input_path": str(INPUT_EXAMPLE_PATH),
                "output_dir": "/tmp/mainline-loop",
                "max_cycles": 6,
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "execute-authoring-mainline-loop"})
        runtime.execute_authoring_mainline_loop.assert_called_once_with(
            input_path=str(INPUT_EXAMPLE_PATH),
            output_dir="/tmp/mainline-loop",
            max_cycles=6,
        )

    def test_domain_entry_dispatches_build_submission_ready_package(self) -> None:
        runtime = Mock()
        runtime.build_submission_ready_package.return_value = {
            "ok": True,
            "command": "build-submission-ready-package",
        }

        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {
                "command": "build-submission-ready-package",
                "input_path": str(FROZEN_EXAMPLE_PATH),
                "output_dir": "/tmp/submission-ready-output",
            }
        )

        self.assertEqual(payload, {"ok": True, "command": "build-submission-ready-package"})
        runtime.build_submission_ready_package.assert_called_once_with(
            input_path=str(FROZEN_EXAMPLE_PATH),
            output_dir="/tmp/submission-ready-output",
        )

    def test_domain_entry_rejects_missing_required_field(self) -> None:
        with self.assertRaisesRegex(WorkspaceStateError, "缺少必填字段: output_path"):
            MedAutoGrantDomainEntry(runtime=Mock()).dispatch(
                {
                    "command": "build-artifact-bundle",
                    "input_path": str(CRITIQUE_EXAMPLE_PATH),
                }
            )


class DomainEntryFreshProofTest(unittest.TestCase):
    def test_family_shared_release_adapter_targets_medautogrant_repo(self) -> None:
        inspection = inspect_current_repo_family_shared_alignment()

        self.assertEqual(inspection["repo_id"], "medautogrant")
        self.assertEqual(Path(inspection["repo_root"]), REPO_ROOT.resolve())
        self.assertEqual(
            [item["file"] for item in inspection["findings"]],
            ["pyproject.toml", "uv.lock"],
        )

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
                        "command": "runtime-run",
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
                        "route_status": "landed",
                        "executor_owner": "med-autogrant",
                        "execution_surface": {
                            "surface_kind": "service-safe-domain-entry-command",
                            "entry_adapter": "MedAutoGrantDomainEntry",
                            "command": "execute-critique-pass",
                        },
                        "handoff_contract_kind": "service-safe-domain-entry-command",
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
                        "command": "runtime-run",
                        "input_path": str(revised_workspace_path),
                        "journal_path": str(revised_journal_path),
                    }
                )
                self.assertTrue(run_payload["ok"])
                self.assertEqual(run_payload["attempt_index"], 1)
                self.assertEqual(run_payload["stop_reason"]["recommended_next_stage"], "revision")

                resume_payload = entry.dispatch(
                    {
                        "command": "runtime-resume",
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


class HostedCallerConsumptionProofTest(unittest.TestCase):
    def test_external_caller_can_consume_domain_entry_contract_without_repo_local_helper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            critique_product_entry = MedAutoGrantProductEntry().build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="opl-handoff",
                task_intent="tighten-grant-mainline",
            )["product_entry"]
            critique_contract = critique_product_entry["return_surface_contract"]["domain_entry_contract"]

            critique_request = _build_request_from_contract(
                critique_contract,
                "stage-route-report",
                input_path=critique_product_entry["workspace_locator"]["workspace_path"],
            )
            critique_payload = MedAutoGrantDomainEntry().dispatch(critique_request)
            self.assertTrue(critique_payload["ok"])
            self.assertEqual(critique_payload["command"], "stage-route-report")

            artifact_bundle_path = tmp_root / "artifact-bundle.json"
            final_package_path = tmp_root / "final-package.json"
            hosted_contract_path = tmp_root / "hosted-contract.json"

            hosted_contract = _build_hosted_bundle_for_external_caller(
                tmp_root=tmp_root,
                final_package_path=final_package_path,
                hosted_contract_path=hosted_contract_path,
            )
            hosted_entry_contract = hosted_contract["domain_entry_contract"]
            route_catalog = {
                route["route_id"]: route
                for route in hosted_contract["authoring_contract"]["author_side_route_catalog"]
            }

            artifact_request = _build_request_from_contract(
                hosted_entry_contract,
                route_catalog["artifact_bundle"]["execution_surface"]["command"],
                input_path=str(FROZEN_EXAMPLE_PATH),
                output_path=str(artifact_bundle_path),
            )
            artifact_payload = MedAutoGrantDomainEntry().dispatch(artifact_request)
            self.assertTrue(artifact_payload["ok"])

            final_request = _build_request_from_contract(
                hosted_entry_contract,
                route_catalog["final_package"]["execution_surface"]["command"],
                input_path=str(FROZEN_EXAMPLE_PATH),
                artifact_bundle_path=str(artifact_bundle_path),
                output_path=str(final_package_path),
            )
            final_payload = MedAutoGrantDomainEntry().dispatch(final_request)
            self.assertTrue(final_payload["ok"])

            hosted_request = _build_request_from_contract(
                hosted_entry_contract,
                route_catalog["hosted_contract_bundle"]["execution_surface"]["command"],
                final_package_path=str(final_package_path),
                output_path=str(hosted_contract_path),
            )
            hosted_payload = MedAutoGrantDomainEntry().dispatch(hosted_request)
            self.assertTrue(hosted_payload["ok"])
            self.assertEqual(
                hosted_payload["hosted_contract_bundle"]["domain_entry_contract"]["command_contracts"],
                hosted_entry_contract["command_contracts"],
            )
            submission_ready_request = _build_request_from_contract(
                hosted_entry_contract,
                "build-submission-ready-package",
                input_path=str(FROZEN_EXAMPLE_PATH),
                output_dir=str(tmp_root / "submission-ready-output"),
            )
            self.assertEqual(
                submission_ready_request,
                {
                    "command": "build-submission-ready-package",
                    "input_path": str(FROZEN_EXAMPLE_PATH),
                    "output_dir": str(tmp_root / "submission-ready-output"),
                },
            )


def _build_request_from_contract(
    domain_entry_contract: dict[str, object],
    command: str,
    **context: str,
) -> dict[str, str]:
    for item in domain_entry_contract["command_contracts"]:
        if item["command"] == command:
            request = {"command": command}
            for field in item["required_fields"] + item["optional_fields"]:
                value = context.get(field)
                if value is not None:
                    request[field] = value
            missing_fields = [field for field in item["required_fields"] if field not in request]
            if missing_fields:
                raise AssertionError(f"external caller context 缺少字段: {missing_fields}")
            return request
    raise AssertionError(f"未找到 command contract: {command}")


def _build_hosted_bundle_for_external_caller(
    *,
    tmp_root: Path,
    final_package_path: Path,
    hosted_contract_path: Path,
) -> dict[str, object]:
    artifact_bundle_path = tmp_root / "bundle-for-hosted-proof.json"
    bundle_payload = MedAutoGrantDomainEntry().dispatch(
        {
            "command": "build-artifact-bundle",
            "input_path": str(FROZEN_EXAMPLE_PATH),
            "output_path": str(artifact_bundle_path),
        }
    )
    if bundle_payload["ok"] is not True:
        raise AssertionError("artifact bundle proof 构建失败")

    final_payload = MedAutoGrantDomainEntry().dispatch(
        {
            "command": "build-final-package",
            "input_path": str(FROZEN_EXAMPLE_PATH),
            "artifact_bundle_path": str(artifact_bundle_path),
            "output_path": str(final_package_path),
        }
    )
    if final_payload["ok"] is not True:
        raise AssertionError("final package proof 构建失败")

    hosted_payload = MedAutoGrantDomainEntry().dispatch(
        {
            "command": "build-hosted-contract-bundle",
            "final_package_path": str(final_package_path),
            "output_path": str(hosted_contract_path),
        }
    )
    if hosted_payload["ok"] is not True:
        raise AssertionError("hosted contract proof 构建失败")
    return hosted_payload["hosted_contract_bundle"]


if __name__ == "__main__":
    unittest.main()
