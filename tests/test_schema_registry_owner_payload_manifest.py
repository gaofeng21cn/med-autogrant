from __future__ import annotations

import json
import unittest
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


class OwnerPayloadManifestSchemaTest(unittest.TestCase):
    def test_product_entry_manifest_schema_pins_owner_payload_response_boundary(self) -> None:
        manifest_schema = json.loads(
            (SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8")
        )
        manifest = manifest_schema["$defs"]["productEntryManifest"]
        owner_payload = manifest_schema["$defs"]["magOplOwnerPayloadResponse"]
        authority = owner_payload["properties"]["authority_boundary"]["properties"]

        self.assertIn("owner_payload_response", manifest["required"])
        self.assertEqual(
            manifest["properties"]["owner_payload_response"]["$ref"],
            "#/$defs/magOplOwnerPayloadResponse",
        )
        self.assertEqual(
            owner_payload["properties"]["surface_kind"]["const"],
            "mag_opl_owner_payload_response",
        )
        self.assertFalse(owner_payload["properties"]["body_included"]["const"])
        self.assertFalse(owner_payload["properties"]["grant_ready_claimed"]["const"])
        self.assertFalse(owner_payload["properties"]["quality_ready_claimed"]["const"])
        self.assertFalse(owner_payload["properties"]["export_ready_claimed"]["const"])
        self.assertFalse(owner_payload["properties"]["submission_ready_claimed"]["const"])
        self.assertFalse(authority["opl_writes_grant_truth"]["const"])
        self.assertFalse(authority["opl_authorizes_quality_or_export"]["const"])
        self.assertFalse(authority["can_declare_submission_ready"]["const"])
