from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"
EXPECTED_SCHEMA_ALIASES = {
    "grant_intake_audit_surface": "grant-intake-audit.schema.json",
    "grant_evidence_grounding_surface": "grant-evidence-grounding.schema.json",
    "grant_quality_scorecard_surface": "grant-quality-scorecard.schema.json",
    "grant_quality_diff_surface": "grant-quality-diff.schema.json",
    "grant_quality_closure_dossier_surface": "grant-quality-closure-dossier.schema.json",
    "grant_progress_projection": "grant-progress.schema.json",
    "grant_cockpit_projection": "grant-cockpit.schema.json",
    "grant_direct_entry_surface": "grant-direct-entry.schema.json",
    "grant_user_loop_surface": "grant-user-loop.schema.json",
}


def _load(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _refs(node: object) -> list[str]:
    if isinstance(node, dict):
        return [
            ref
            for key, value in node.items()
            for ref in ([value] if key == "$ref" and isinstance(value, str) else _refs(value))
        ]
    if isinstance(node, list):
        return [ref for item in node for ref in _refs(item)]
    return []


class SchemaRegistryTest(unittest.TestCase):
    def test_schema_index_is_the_single_registry_owner(self) -> None:
        index = _load("schema-index.json")
        entries = index["schemas"]
        names = [item["name"] for item in entries]
        files = [item["file"] for item in entries]

        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(files), len(set(files)))
        semantic_aliases = {
            item["name"]: item["file"]
            for item in entries
            if item["name"] != item["file"].removesuffix(".schema.json").replace("-", "_")
        }
        self.assertEqual(semantic_aliases, EXPECTED_SCHEMA_ALIASES)
        self.assertEqual(
            set(files),
            {path.name for path in SCHEMA_ROOT.glob("*.json")} - {"schema-index.json"},
        )

        for name in files:
            with self.subTest(schema=name):
                schema = _load(name)
                self.assertTrue({"$schema", "$id", "title", "type"} <= schema.keys())
                for ref in _refs(schema):
                    parsed = urlparse(ref)
                    if parsed.scheme in {"http", "https"} or not parsed.path:
                        continue
                    self.assertTrue((SCHEMA_ROOT / parsed.path).exists(), f"{name}: {ref}")

    def test_workspace_schema_composes_core_grant_objects(self) -> None:
        refs = set(_refs(_load("nsfc-workspace.schema.json")))
        self.assertTrue(
            {
                "applicant-profile.schema.json",
                "project-profile.schema.json",
                "funding-opportunity-brief.schema.json",
                "direction-hypothesis.schema.json",
                "scientific-question-card.schema.json",
                "argument-chain.schema.json",
                "applicant-fit-mapping.schema.json",
                "application-draft.schema.json",
                "mentor-critique.schema.json",
                "revision-plan.schema.json",
                "grant-intake-audit.schema.json#/$defs/grantIntakeAudit",
                "grant-evidence-grounding.schema.json#/$defs/grantEvidenceGrounding",
            }
            <= refs
        )

    def test_domain_quality_schemas_keep_high_value_required_surfaces(self) -> None:
        cases = (
            (
                "grant-quality-scorecard.schema.json",
                "trackedIssue",
                {"lineage_id", "closure_status", "evidence_obligations", "recommended_closure_action"},
            ),
            (
                "grant-quality-diff.schema.json",
                "issueClosureProgress",
                {"lineage_id", "previous_closure_status", "current_closure_status", "closure_delta"},
            ),
            (
                "grant-quality-closure-dossier.schema.json",
                "closurePackage",
                {"closure_id", "target_stage", "blocking_reasons", "evidence_obligations", "acceptance_signals"},
            ),
            (
                "common.schema.json",
                "projectProfileFamilyGovernancePolicy",
                {"default_tranche", "quality_bar", "route_back_advisory", "ready_claim_policy"},
            ),
        )
        for schema_name, definition, required_fields in cases:
            with self.subTest(schema=schema_name, definition=definition):
                schema = _load(schema_name)
                surface = schema if definition is None else schema["$defs"][definition]
                self.assertTrue(required_fields <= set(surface["required"]))

    def test_project_profile_route_advisory_uses_standard_route_owner_split(self) -> None:
        advisory = _load("common.schema.json")["$defs"][
            "projectProfileFamilyGovernanceRouteBackAdvisory"
        ]

        self.assertEqual(
            set(advisory["required"]),
            {
                "suggested_route_back_stage",
                "advisory_trigger",
                "semantic_route_decision_owner",
                "stage_transition_materialization_owner",
                "binding",
            },
        )
        self.assertEqual(
            advisory["properties"]["semantic_route_decision_owner"]["const"],
            "decisive_codex_attempt",
        )
        self.assertEqual(
            advisory["properties"]["stage_transition_materialization_owner"]["const"],
            "opl_stage_run_controller",
        )
        self.assertNotIn("route_selection_owner", advisory["properties"])

    def test_funding_discovery_route_back_owner_is_the_decisive_attempt(self) -> None:
        summary = _load("funding-landscape-discovery.schema.json")["$defs"][
            "discoverySummary"
        ]

        self.assertEqual(
            summary["properties"]["route_back_selection_owner"]["const"],
            "decisive_codex_attempt",
        )
