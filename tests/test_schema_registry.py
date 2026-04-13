from __future__ import annotations

import json
import unittest
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPO_ROOT / "schemas" / "v1"

EXPECTED_SCHEMAS = {
    "common.schema.json",
    "applicant-profile.schema.json",
    "track-record.schema.json",
    "active-project-set.schema.json",
    "preliminary-evidence-pack.schema.json",
    "funding-opportunity-brief.schema.json",
    "direction-hypothesis.schema.json",
    "scientific-question-card.schema.json",
    "argument-chain.schema.json",
    "applicant-fit-mapping.schema.json",
    "application-draft.schema.json",
    "mentor-critique.schema.json",
    "revision-plan.schema.json",
    "nsfc-workspace.schema.json",
    "service-safe-domain-surface.schema.json",
    "pending-handoff-requirements.schema.json",
    "executor-routing-contract.schema.json",
    "product-entry.schema.json",
    "grant-progress.schema.json",
    "grant-cockpit.schema.json",
    "grant-direct-entry.schema.json",
    "grant-user-loop.schema.json",
    "hosted-contract-bundle.schema.json",
    "schema-index.json",
}


def walk_refs(node: object) -> list[str]:
    refs: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                refs.append(value)
            else:
                refs.extend(walk_refs(value))
    elif isinstance(node, list):
        for item in node:
            refs.extend(walk_refs(item))
    return refs


class SchemaRegistryTest(unittest.TestCase):
    def test_expected_schema_files_exist(self) -> None:
        self.assertTrue(SCHEMA_ROOT.is_dir(), "schemas/v1 目录必须存在。")
        actual = {path.name for path in SCHEMA_ROOT.glob("*.json")}
        self.assertEqual(EXPECTED_SCHEMAS, actual)

    def test_schema_files_are_valid_json(self) -> None:
        for name in EXPECTED_SCHEMAS:
            with self.subTest(schema=name):
                payload = json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))
                self.assertIsInstance(payload, dict)

    def test_non_index_schemas_expose_core_metadata(self) -> None:
        for name in EXPECTED_SCHEMAS - {"schema-index.json"}:
            with self.subTest(schema=name):
                payload = json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))
                self.assertIn("$schema", payload)
                self.assertIn("$id", payload)
                self.assertIn("title", payload)
                self.assertIn("type", payload)

    def test_local_refs_are_resolvable(self) -> None:
        for name in EXPECTED_SCHEMAS - {"schema-index.json"}:
            with self.subTest(schema=name):
                payload = json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))
                refs = walk_refs(payload)
                for ref in refs:
                    parsed = urlparse(ref)
                    if parsed.scheme in {"http", "https"}:
                        continue
                    path_part = parsed.path
                    if not path_part:
                        continue
                    target = (SCHEMA_ROOT / path_part).resolve()
                    self.assertTrue(target.exists(), f"{name} 引用了不存在的 schema: {ref}")

    def test_workspace_schema_references_all_core_objects(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "nsfc-workspace.schema.json").read_text(encoding="utf-8"))
        refs = set(walk_refs(payload))
        expected_refs = {
            "applicant-profile.schema.json",
            "track-record.schema.json",
            "active-project-set.schema.json",
            "preliminary-evidence-pack.schema.json",
            "funding-opportunity-brief.schema.json",
            "direction-hypothesis.schema.json",
            "scientific-question-card.schema.json",
            "argument-chain.schema.json",
            "applicant-fit-mapping.schema.json",
            "application-draft.schema.json",
            "mentor-critique.schema.json",
            "revision-plan.schema.json",
        }
        for ref in expected_refs:
            self.assertIn(ref, refs)

    def test_schema_index_tracks_domain_handoff_contract_schemas(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "schema-index.json").read_text(encoding="utf-8"))
        names = {item["name"]: item["file"] for item in payload["schemas"]}

        self.assertEqual(names["service_safe_domain_surface"], "service-safe-domain-surface.schema.json")
        self.assertEqual(names["pending_handoff_requirements"], "pending-handoff-requirements.schema.json")
        self.assertEqual(names["executor_routing_contract"], "executor-routing-contract.schema.json")
        self.assertEqual(names["product_entry"], "product-entry.schema.json")
        self.assertEqual(names["grant_progress_projection"], "grant-progress.schema.json")
        self.assertEqual(names["grant_cockpit_projection"], "grant-cockpit.schema.json")
        self.assertEqual(names["grant_direct_entry_surface"], "grant-direct-entry.schema.json")
        self.assertEqual(names["grant_user_loop_surface"], "grant-user-loop.schema.json")
        self.assertEqual(names["hosted_contract_bundle"], "hosted-contract-bundle.schema.json")

    def test_product_surface_schemas_require_family_orchestration_companion(self) -> None:
        schema_files = [
            "grant-progress.schema.json",
            "grant-cockpit.schema.json",
            "grant-direct-entry.schema.json",
            "grant-user-loop.schema.json",
        ]
        for schema_file in schema_files:
            with self.subTest(schema=schema_file):
                payload = json.loads((SCHEMA_ROOT / schema_file).read_text(encoding="utf-8"))
                required = payload.get("required")
                self.assertIsInstance(required, list)
                self.assertIn("family_orchestration", required)


if __name__ == "__main__":
    unittest.main()
