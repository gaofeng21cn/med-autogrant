from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryOplSubstrateAdapterTest(unittest.TestCase):
    def test_manifest_exports_opl_substrate_adapter_as_opaque_index_only_refs(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )["product_entry_manifest"]

        adapter = manifest["opl_substrate_adapter_export"]
        self.assertEqual(adapter["surface_kind"], "mag_opl_substrate_adapter_export")
        self.assertEqual(adapter["adapter_id"], "mag.opl_substrate_adapter.export.v1")
        self.assertEqual(adapter["export_policy"], "opaque_index_only_refs_no_domain_truth_payloads")
        self.assertEqual(adapter["workspace_ref_index"]["locator_ref"], "/product_entry_manifest/workspace_locator")
        self.assertEqual(adapter["workspace_ref_index"]["body_policy"], "locator_only_no_workspace_body")
        self.assertEqual(adapter["source_ref_index"]["index_policy"], "source_refs_only_no_source_body")
        self.assertEqual(
            [ref["role"] for ref in adapter["source_ref_index"]["source_refs"]],
            [
                "domain_entry_contract",
                "family_action_catalog",
                "stage_control_plane",
                "task_lifecycle",
                "runtime_control",
                "progress_projection",
            ],
        )
        self.assertEqual(
            adapter["artifact_ref_index"]["artifact_locator_contract_ref"],
            "/product_entry_manifest/artifact_locator_contract",
        )
        self.assertFalse(adapter["artifact_ref_index"]["runtime_artifact_root_repo_tracked"])
        self.assertEqual(adapter["artifact_ref_index"]["body_policy"], "locator_and_inventory_refs_only_no_package_body")
        self.assertEqual(
            adapter["memory_ref_index"]["domain_memory_descriptor_locator_ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator",
        )
        self.assertFalse(adapter["memory_ref_index"]["memory_locator_repo_tracked"])
        self.assertFalse(adapter["memory_ref_index"]["receipt_locator_repo_tracked"])
        self.assertEqual(adapter["memory_ref_index"]["body_policy"], "locator_and_receipt_refs_only_no_memory_body")
        self.assertEqual(
            adapter["lifecycle_ref_index"]["owner_receipt_contract_ref"],
            "/product_entry_manifest/owner_receipt_contract",
        )
        self.assertEqual(adapter["projection_ref_index"]["runtime_control_ref"], "/product_entry_manifest/runtime_control")
        self.assertEqual(
            adapter["body_exposure_policy"],
            {
                "workspace": "opaque_ref_and_locator_ref_only",
                "source": "json_pointer_refs_only",
                "artifact": "locator_index_only_no_package_body",
                "memory": "locator_receipt_refs_only_no_memory_body",
                "owner_receipt": "receipt_ref_only_no_authority_transfer",
            },
        )
        self.assertFalse(adapter["authority_boundary"]["opl_can_write_grant_truth"])
        self.assertFalse(adapter["authority_boundary"]["opl_can_hold_fundability_verdict"])
        self.assertFalse(adapter["authority_boundary"]["opl_can_read_package_body"])
        self.assertFalse(adapter["authority_boundary"]["opl_can_read_memory_body"])
        self.assertFalse(adapter["authority_boundary"]["opl_can_issue_owner_receipt"])
        self.assertIn("package_body", adapter["forbidden_payload_classes"])
        self.assertIn("memory_body", adapter["forbidden_payload_classes"])
