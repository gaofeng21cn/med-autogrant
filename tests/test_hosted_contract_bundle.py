from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
from support.hosted_contract_bundle import (  # noqa: E402
    assert_hosted_contract_bundle_cli_failure,
    assert_hosted_contract_bundle_contract,
    build_final_package,
    current_runtime_owner,
    run_hosted_contract_bundle_cli,
)


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"


class HostedContractBundleCliTest(unittest.TestCase):
    def test_build_and_same_identity_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_path = Path(tmp_dir) / "final.json"
            output_path = Path(tmp_dir) / "hosted.json"
            build_final_package(self, FROZEN_EXAMPLE_PATH, final_path)

            first = run_hosted_contract_bundle_cli(final_path, output_path)
            second = run_hosted_contract_bundle_cli(final_path, output_path)

            for exit_code, stdout, stderr in (first, second):
                self.assertEqual((exit_code, stderr), (0, ""))
                payload = json.loads(stdout)
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["command"], "build-hosted-contract-bundle")
                self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
                self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
                self.assertEqual(payload["draft_id"], "draft-v1")
                self.assertEqual(payload["output_path"], str(output_path.resolve()))
                assert_hosted_contract_bundle_contract(
                    self,
                    payload["hosted_contract_bundle"],
                    current_runtime_owner=current_runtime_owner(CURRENT_PROGRAM_CONTRACT),
                )
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), json.loads(second[1])["hosted_contract_bundle"])

    def test_non_final_package_and_existing_identity_mismatch_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            output_path = root / "hosted.json"
            not_final = root / "not-final.json"
            not_final.write_text(json.dumps({"package_kind": "artifact_bundle"}), encoding="utf-8")
            assert_hosted_contract_bundle_cli_failure(
                self,
                run_hosted_contract_bundle_cli(not_final, output_path),
                output_path,
            )

            final_path = root / "final.json"
            build_final_package(self, FROZEN_EXAMPLE_PATH, final_path)
            output_path.write_text(
                json.dumps({"grant_run_id": "other", "workspace_id": "other", "draft_id": "other"}),
                encoding="utf-8",
            )
            exit_code, stdout, stderr = run_hosted_contract_bundle_cli(final_path, output_path)
            self.assertEqual((exit_code, stderr), (1, ""))
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("identity", payload["error"])

    def test_invalid_built_contract_shape_is_rejected(self) -> None:
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime
        from med_autogrant.workspace import WorkspaceStateError

        with tempfile.TemporaryDirectory() as tmp_dir:
            final_path = Path(tmp_dir) / "final.json"
            output_path = Path(tmp_dir) / "hosted.json"
            build_final_package(self, FROZEN_EXAMPLE_PATH, final_path)
            with patch(
                "med_autogrant.domain_runtime_parts.package_surface.build_hosted_contract_bundle_document",
                return_value={"contract_version": 1, "bundle_kind": "hosted_contract_bundle"},
            ), self.assertRaises(WorkspaceStateError):
                MagDomainRuntime().build_hosted_contract_bundle(
                    final_package_path=str(final_path),
                    output_path=str(output_path),
                )


if __name__ == "__main__":
    unittest.main()
