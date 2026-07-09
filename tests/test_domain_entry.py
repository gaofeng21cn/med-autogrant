from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.domain_entry import MedAutoGrantDomainEntry  # noqa: E402
from med_autogrant.domain_entry_contract import build_domain_entry_contract  # noqa: E402
from med_autogrant.family_shared_release import inspect_current_repo_family_shared_alignment  # noqa: E402
from med_autogrant.product_entry import MedAutoGrantProductEntry  # noqa: E402
from med_autogrant.workspace import WorkspaceStateError  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
NSFC_SELECTION_INPUT = REPO_ROOT / "examples" / "profile_selection_input_nsfc_general.json"
DISCOVERY_INPUT = REPO_ROOT / "examples" / "funding_discovery_input_cardiovascular.json"


class DomainEntryDispatchTest(unittest.TestCase):
    def test_domain_entry_dispatches_runtime_commands(self) -> None:
        opl_stage_attempt = {
            "runtime_owner": "one-person-lab",
            "executor_kind": "codex_cli",
            "attempt_lease_ref": "lease:opl/stage-run/mag/domain-entry/owner-chain-default-caller",
        }
        cases = (
            (
                "grant-intake-audit",
                "grant_intake_audit",
                {"input_path": str(INPUT_EXAMPLE_PATH)},
            ),
            (
                "grant-evidence-grounding",
                "grant_evidence_grounding",
                {"input_path": str(INPUT_EXAMPLE_PATH)},
            ),
            (
                "grant-quality-scorecard",
                "grant_quality_scorecard",
                {"input_path": str(CRITIQUE_EXAMPLE_PATH)},
            ),
            (
                "grant-quality-diff",
                "grant_quality_diff",
                {
                    "input_path": str(FROZEN_EXAMPLE_PATH),
                    "previous_input_path": str(CRITIQUE_EXAMPLE_PATH),
                },
            ),
            (
                "grant-quality-closure-dossier",
                "grant_quality_closure_dossier",
                {"input_path": str(CRITIQUE_EXAMPLE_PATH)},
            ),
            (
                "execute-critique-pass",
                "execute_critique_pass",
                {
                    "input_path": str(CRITIQUE_EXAMPLE_PATH),
                    "output_path": "/tmp/critique-output.json",
                },
            ),
            (
                "execute-critique-pass",
                "execute_critique_pass",
                {
                    "input_path": str(CRITIQUE_EXAMPLE_PATH),
                    "output_path": "/tmp/critique-output.json",
                    "executor_kind": "hermes_agent",
                },
            ),
            (
                "execute-direction-screening-pass",
                "execute_direction_screening_pass",
                {
                    "input_path": str(INPUT_EXAMPLE_PATH),
                    "output_path": "/tmp/direction-screening-output.json",
                },
            ),
            (
                "select-project-profile",
                "select_project_profile",
                {"input_path": str(NSFC_SELECTION_INPUT)},
            ),
            (
                "initialize-intake-workspace",
                "initialize_intake_workspace",
                {
                    "input_path": str(NSFC_SELECTION_INPUT),
                    "output_path": "/tmp/initialized-workspace.json",
                },
            ),
            (
                "discover-funding-opportunities",
                "discover_funding_opportunities",
                {"input_path": str(DISCOVERY_INPUT)},
            ),
            (
                "refresh-funding-opportunities-cache",
                "refresh_funding_opportunities_cache",
                {
                    "input_path": str(DISCOVERY_INPUT),
                    "output_path": "/tmp/funding-cache.json",
                },
            ),
            (
                "execute-critique-revision-loop",
                "execute_critique_revision_loop",
                {
                    "input_path": str(CRITIQUE_EXAMPLE_PATH),
                    "output_dir": "/tmp/critique-loop",
                    "max_rounds": 4,
                    "opl_stage_attempt": opl_stage_attempt,
                },
            ),
            (
                "execute-authoring-mainline-loop",
                "execute_authoring_mainline_loop",
                {
                    "input_path": str(INPUT_EXAMPLE_PATH),
                    "output_dir": "/tmp/mainline-loop",
                    "max_cycles": 6,
                    "opl_stage_attempt": opl_stage_attempt,
                },
            ),
            (
                "execute-grant-autonomy-controller",
                "execute_grant_autonomy_controller",
                {
                    "input_path": "/tmp/autonomy-request.json",
                    "output_dir": "/tmp/autonomy-output",
                    "opl_stage_attempt": opl_stage_attempt,
                },
            ),
            (
                "build-submission-ready-package",
                "build_submission_ready_package",
                {
                    "input_path": str(FROZEN_EXAMPLE_PATH),
                    "output_dir": "/tmp/submission-ready-output",
                },
            ),
        )

        for command, runtime_method, request_args in cases:
            with self.subTest(command=command, runtime_method=runtime_method):
                runtime = Mock()
                getattr(runtime, runtime_method).return_value = {
                    "ok": True,
                    "command": command,
                }

                payload = _dispatch(
                    MedAutoGrantDomainEntry(runtime=runtime),
                    command,
                    **request_args,
                )

                self.assertEqual(payload, {"ok": True, "command": command})
                getattr(runtime, runtime_method).assert_called_once_with(**request_args)

    def test_domain_entry_rejects_missing_required_field(self) -> None:
        with self.assertRaisesRegex(WorkspaceStateError, "缺少必填字段: output_path"):
            _dispatch(
                MedAutoGrantDomainEntry(runtime=Mock()),
                "build-artifact-bundle",
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )


class DomainEntryContractSurfaceTest(unittest.TestCase):
    def test_domain_entry_contract_exports_mag_domain_agent_entry_spec_v1(self) -> None:
        contract = build_domain_entry_contract()
        self.assertIsInstance(contract.get("domain_agent_entry_spec"), dict)
        domain_agent_entry_spec = contract["domain_agent_entry_spec"]

        self.assertEqual(domain_agent_entry_spec["surface_kind"], "domain_agent_entry_spec")
        self.assertEqual(domain_agent_entry_spec["agent_id"], "mag")
        self.assertEqual(domain_agent_entry_spec["title"], "Med Auto Grant Domain Agent")
        self.assertEqual(
            domain_agent_entry_spec["description"],
            "Grant authoring domain truth owner surface for Med Auto Grant.",
        )
        self.assertEqual(domain_agent_entry_spec["default_engine"], "codex")
        self.assertEqual(domain_agent_entry_spec["workspace_requirement"], "required")
        self.assertEqual(
            domain_agent_entry_spec["locator_schema"],
            {
                "required_fields": ["input_path"],
                "optional_fields": ["workspace_id", "grant_run_id", "draft_id"],
                "workspace_field": "input_path",
                "workspace_kind": "nsfc_workspace",
                "workspace_id_field": "workspace_id",
                "run_id_field": "grant_run_id",
                "draft_id_field": "draft_id",
            },
        )
        self.assertEqual(domain_agent_entry_spec["codex_entry_strategy"], "domain_agent_entry")
        self.assertEqual(domain_agent_entry_spec["artifact_conventions"], "grant_proposal_package")
        self.assertEqual(domain_agent_entry_spec["progress_conventions"], "grant_workloop_narration")
        self.assertEqual(domain_agent_entry_spec["entry_command"], "product-status")
        self.assertEqual(domain_agent_entry_spec["manifest_command"], "product-entry-manifest")

    def test_loop_commands_require_opl_stage_attempt_in_machine_contract(self) -> None:
        contract = build_domain_entry_contract()
        command_specs = {
            item["command"]: item
            for item in contract["command_contracts"]
        }

        for command in (
            "execute-critique-revision-loop",
            "execute-authoring-mainline-loop",
            "execute-grant-autonomy-controller",
        ):
            with self.subTest(command=command):
                self.assertIn("opl_stage_attempt", command_specs[command]["required_fields"])


class DomainEntryFreshProofTest(unittest.TestCase):
    def test_family_shared_release_adapter_targets_medautogrant_repo(self) -> None:
        inspection = inspect_current_repo_family_shared_alignment()

        self.assertEqual(inspection["repo_id"], "medautogrant")
        self.assertEqual(Path(inspection["repo_root"]), REPO_ROOT.resolve())
        self.assertEqual(
            [item["file"] for item in inspection["findings"]],
            ["pyproject.toml", "uv.lock"],
        )

    @pytest.mark.proof
    def test_service_safe_domain_entry_runs_fresh_cutover_walkthrough(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            revised_workspace_path, final_package_path, hosted_contract_path = (
                tmp_root / file_name
                for file_name in ("revised.json", "final-package.json", "hosted-contract.json")
            )

            entry = MedAutoGrantDomainEntry()

            critique_report = _dispatch(
                entry,
                "stage-route-report",
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )
            self.assertTrue(critique_report["ok"])
            self.assertEqual(
                critique_report["verification_checkpoint"]["identity"]["grant_run_id"],
                "grant-run-nsfc-demo-001-baseline-001",
            )

            revision_payload = _dispatch(
                entry,
                "execute-revision-pass",
                input_path=str(RE_REVIEW_EXAMPLE_PATH),
                output_path=str(revised_workspace_path),
            )
            self.assertTrue(revision_payload["ok"])
            self.assertEqual(revision_payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")

            hosted_contract = _build_hosted_bundle_for_external_caller(
                tmp_root=tmp_root,
                final_package_path=final_package_path,
                hosted_contract_path=hosted_contract_path,
            )

        self.assertEqual(
            hosted_contract["execution_identity"],
            {
                "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                "workspace_id": "nsfc-demo-001",
                "draft_id": "draft-v1",
                "program_id": "med-autogrant-mainline",
            },
        )


class HostedCallerConsumptionProofTest(unittest.TestCase):
    def test_external_caller_can_consume_domain_entry_contract_without_repo_local_helper(self) -> None:
        with TemporaryDirectory() as tmp_dir:
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

            payloads = {}
            for route_id, context in (
                (
                    "artifact_bundle",
                    {
                        "input_path": str(FROZEN_EXAMPLE_PATH),
                        "output_path": str(artifact_bundle_path),
                    },
                ),
                (
                    "final_package",
                    {
                        "input_path": str(FROZEN_EXAMPLE_PATH),
                        "artifact_bundle_path": str(artifact_bundle_path),
                        "output_path": str(final_package_path),
                    },
                ),
                (
                    "hosted_contract_bundle",
                    {
                        "final_package_path": str(final_package_path),
                        "output_path": str(hosted_contract_path),
                    },
                ),
            ):
                payloads[route_id] = MedAutoGrantDomainEntry().dispatch(
                    _build_request_from_contract(
                        hosted_entry_contract,
                        route_catalog[route_id]["execution_surface"]["command"],
                        **context,
                    )
                )
                self.assertTrue(payloads[route_id]["ok"])
            self.assertEqual(
                payloads["hosted_contract_bundle"]["hosted_contract_bundle"]["domain_entry_contract"][
                    "command_contracts"
                ],
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


def _dispatch(
    entry: MedAutoGrantDomainEntry,
    command: str,
    **request_args: object,
) -> dict[str, object]:
    return entry.dispatch({"command": command, **request_args})


def _build_request_from_contract(
    domain_entry_contract: dict[str, object],
    command: str,
    **context: str,
) -> dict[str, str]:
    item = next(
        (item for item in domain_entry_contract["command_contracts"] if item["command"] == command),
        None,
    )
    if item is None:
        raise AssertionError(f"未找到 command contract: {command}")

    fields = item["required_fields"] + item["optional_fields"]
    request = {
        "command": command,
        **{field: context[field] for field in fields if field in context},
    }
    missing_fields = [field for field in item["required_fields"] if field not in request]
    if missing_fields:
        raise AssertionError(f"external caller context 缺少字段: {missing_fields}")
    return request


def _build_hosted_bundle_for_external_caller(
    *,
    tmp_root: Path,
    final_package_path: Path,
    hosted_contract_path: Path,
) -> dict[str, object]:
    artifact_bundle_path = tmp_root / "bundle-for-hosted-proof.json"
    entry = MedAutoGrantDomainEntry()
    bundle_payload = _dispatch(
        entry,
        "build-artifact-bundle",
        input_path=str(FROZEN_EXAMPLE_PATH),
        output_path=str(artifact_bundle_path),
    )
    if bundle_payload["ok"] is not True:
        raise AssertionError("artifact bundle proof 构建失败")

    final_payload = _dispatch(
        entry,
        "build-final-package",
        input_path=str(FROZEN_EXAMPLE_PATH),
        artifact_bundle_path=str(artifact_bundle_path),
        output_path=str(final_package_path),
    )
    if final_payload["ok"] is not True:
        raise AssertionError("final package proof 构建失败")

    hosted_payload = _dispatch(
        entry,
        "build-hosted-contract-bundle",
        final_package_path=str(final_package_path),
        output_path=str(hosted_contract_path),
    )
    if hosted_payload["ok"] is not True:
        raise AssertionError("hosted contract proof 构建失败")
    return hosted_payload["hosted_contract_bundle"]


if __name__ == "__main__":
    unittest.main()
