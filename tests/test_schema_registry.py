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
    "project-profile.schema.json",
    "funding-landscape-discovery-input.schema.json",
    "funding-landscape-discovery.schema.json",
    "funding-landscape-cache.schema.json",
    "funding-landscape-diff-report.schema.json",
    "project-profile-selection-input.schema.json",
    "project-profile-selection.schema.json",
    "critique-loop-report.schema.json",
    "authoring-mainline-loop-report.schema.json",
    "funding-opportunity-brief.schema.json",
    "direction-hypothesis.schema.json",
    "scientific-question-card.schema.json",
    "argument-chain.schema.json",
    "applicant-fit-mapping.schema.json",
    "application-draft.schema.json",
    "mentor-critique.schema.json",
    "revision-plan.schema.json",
    "nsfc-workspace.schema.json",
    "grant-intake-audit.schema.json",
    "grant-evidence-grounding.schema.json",
    "grant-quality-scorecard.schema.json",
    "grant-quality-diff.schema.json",
    "grant-quality-closure-dossier.schema.json",
    "grant-autonomy-controller-input.schema.json",
    "grant-autonomy-controller-report.schema.json",
    "service-safe-domain-surface.schema.json",
    "executor-routing-contract.schema.json",
    "product-entry.schema.json",
    "grant-progress.schema.json",
    "grant-cockpit.schema.json",
    "grant-direct-entry.schema.json",
    "grant-user-loop.schema.json",
    "product-entry-manifest.schema.json",
    "product-status.schema.json",
    "hosted-contract-bundle.schema.json",
    "submission-ready-package.schema.json",
    "codex-stage-execution-receipt-bundle.schema.json",
    "operator-closeout-readiness-projection.schema.json",
    "physical-morphology-guard-projection.schema.json",
    "executor-first-closeout-bundle.schema.json",
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
    def assert_required_fields(self, required: list[str], fields: str) -> None:
        self.assertEqual(sorted(set(fields.split()) - set(required)), [])

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

    def test_schema_index_names_and_files_are_unique(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "schema-index.json").read_text(encoding="utf-8"))
        schemas = payload["schemas"]
        names = [item["name"] for item in schemas]
        files = [item["file"] for item in schemas]

        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(files), len(set(files)))

    def test_workspace_schema_references_all_core_objects(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "nsfc-workspace.schema.json").read_text(encoding="utf-8"))
        refs = set(walk_refs(payload))
        expected_refs = {
            "applicant-profile.schema.json",
            "track-record.schema.json",
            "active-project-set.schema.json",
            "preliminary-evidence-pack.schema.json",
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
        for ref in expected_refs:
            self.assertIn(ref, refs)

    def test_loop_report_schemas_require_quality_surfaces(self) -> None:
        for schema_name in ("critique-loop-report.schema.json", "authoring-mainline-loop-report.schema.json"):
            with self.subTest(schema=schema_name):
                schema = json.loads((SCHEMA_ROOT / schema_name).read_text(encoding="utf-8"))
                self.assert_required_fields(
                    schema["required"],
                    "grant_quality_scorecard grant_quality_closure_dossier",
                )
                self.assertEqual(
                    schema["properties"]["grant_quality_scorecard"]["$ref"],
                    "grant-quality-scorecard.schema.json#/$defs/grantQualityScorecard",
                )
                self.assertEqual(
                    schema["properties"]["grant_quality_closure_dossier"]["$ref"],
                    "grant-quality-closure-dossier.schema.json#/$defs/grantQualityClosureDossier",
                )

    def test_autonomy_controller_schemas_require_tranche_planning_surface(self) -> None:
        input_schema = json.loads((SCHEMA_ROOT / "grant-autonomy-controller-input.schema.json").read_text(encoding="utf-8"))
        self.assertIn("controller_plan", input_schema["properties"])
        self.assertEqual(
            input_schema["$defs"]["controllerPlan"]["required"],
            ["current_tranche", "tranche_objective", "tranche_success_gate"],
        )

        report_schema = json.loads((SCHEMA_ROOT / "grant-autonomy-controller-report.schema.json").read_text(encoding="utf-8"))
        self.assert_required_fields(
            report_schema["required"],
            "controller_checkpoint controller_plan tranche_history latest_quality_closure_dossier "
            "closure_package_queue active_closure_package",
        )
        self.assertEqual(
            report_schema["$defs"]["controllerPlan"]["required"],
            [
                "current_tranche",
                "tranche_objective",
                "tranche_success_gate",
                "quality_summary",
                "closure_package_queue_ids",
                "active_closure_package_id",
                "active_closure_package_action",
                "active_closure_package_target_stage",
                "next_controller_action",
                "decision_basis",
            ],
        )
        planning_fields = (
            "quality_summary closure_package_queue_ids active_closure_package_id "
            "active_closure_package_action active_closure_package_target_stage"
        )
        self.assert_required_fields(report_schema["$defs"]["controllerDecisionBasis"]["required"], planning_fields)
        self.assert_required_fields(report_schema["$defs"]["trancheHistoryEntry"]["required"], planning_fields)
        self.assertEqual(
            report_schema["$defs"]["trancheHistoryEntry"]["properties"]["next_controller_action"]["$ref"],
            "#/$defs/controllerAction",
        )
        dossier_any_of = report_schema["properties"]["latest_quality_closure_dossier"]["anyOf"]
        self.assertEqual(
            dossier_any_of[0]["$ref"],
            "grant-quality-closure-dossier.schema.json#/$defs/grantQualityClosureDossier",
        )

    def test_project_profile_schema_supports_family_grammar_contract(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "project-profile.schema.json").read_text(encoding="utf-8"))
        properties = payload["properties"]
        self.assertIn("grant_family_grammar", properties)
        self.assertIn("family_grammar_trace", properties)
        self.assertEqual(
            properties["grant_family_grammar"]["$ref"],
            "common.schema.json#/$defs/projectProfileGrantFamilyGrammar",
        )
        self.assertEqual(
            properties["family_grammar_trace"]["$ref"],
            "common.schema.json#/$defs/projectProfileFamilyGrammarTrace",
        )

    def test_common_schema_supports_structured_family_governance_policy(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "common.schema.json").read_text(encoding="utf-8"))
        defs = payload["$defs"]

        self.assertIn("projectProfileFamilyGovernancePolicy", defs)
        governance_policy = defs["projectProfileFamilyGovernancePolicy"]
        self.assertEqual(
            governance_policy["required"],
            [
                "default_tranche",
                "preferred_stop_target",
                "quality_bar",
                "rollback_bias",
                "evidence_escalation_policy",
                "controller_defaults",
            ],
        )

        family_trace = defs["projectProfileFamilyGrammarTrace"]
        self.assertIn("governance_policy", family_trace["required"])
        self.assertEqual(
            family_trace["properties"]["governance_policy"]["$ref"],
            "#/$defs/projectProfileFamilyGovernancePolicy",
        )

        family_grammar = defs["projectProfileGrantFamilyGrammar"]
        self.assertIn("governance_policy", family_grammar["required"])
        self.assertEqual(
            family_grammar["properties"]["governance_policy"]["$ref"],
            "#/$defs/projectProfileFamilyGovernancePolicy",
        )

    def test_grant_quality_schemas_require_issue_closure_contract(self) -> None:
        scorecard_schema = json.loads((SCHEMA_ROOT / "grant-quality-scorecard.schema.json").read_text(encoding="utf-8"))
        scorecard_required_fields = (
            ("trackedIssue", "lineage_id lineage_basis closure_status blocking_reason evidence_obligations recommended_closure_action"),
            ("grantQualityScorecard", "assessment_owner ai_reviewer_required review_artifact_ref evidence_supply_queue"),
            ("evidenceSupplyQueueItem", "gap_id gap_kind controller_action_hint required_input_ids linked_issue_ids"),
        )
        for def_name, fields in scorecard_required_fields:
            with self.subTest(schema="scorecard", def_name=def_name):
                self.assert_required_fields(scorecard_schema["$defs"][def_name]["required"], fields)

        diff_schema = json.loads((SCHEMA_ROOT / "grant-quality-diff.schema.json").read_text(encoding="utf-8"))
        diff_required_fields = (
            ("issueProgress", "issue_closure_progress"),
            (
                "issueClosureProgress",
                "lineage_id lineage_basis previous_issue_id current_issue_id previous_summary current_summary "
                "previous_closure_status current_closure_status closure_delta",
            ),
            ("grantQualityDiff", "evidence_supply_progress"),
            ("evidenceSupplyProgress", "closed_gaps remaining_open_gaps newly_opened_gaps gap_progress"),
            ("evidenceSupplyGapProgress", "gap_id transition supply_delta"),
            ("controllerActionHint", "action"),
        )
        for def_name, fields in diff_required_fields:
            with self.subTest(schema="diff", def_name=def_name):
                self.assert_required_fields(diff_schema["$defs"][def_name]["required"], fields)

        dossier_schema = json.loads(
            (SCHEMA_ROOT / "grant-quality-closure-dossier.schema.json").read_text(encoding="utf-8")
        )
        dossier_required_fields = (
            (
                "grantQualityClosureDossier",
                "quality_summary unclosed_hard_issues evidence_supply_queue_summary closure_packages",
            ),
            ("qualitySummary", "assessment_owner ai_reviewer_required review_artifact_ref"),
            (
                "closurePackage",
                "closure_id severity target_stage action required_input_ids linked_issue_ids "
                "blocking_reasons evidence_obligations acceptance_signals",
            ),
        )
        for def_name, fields in dossier_required_fields:
            with self.subTest(schema="dossier", def_name=def_name):
                self.assert_required_fields(dossier_schema["$defs"][def_name]["required"], fields)

if __name__ == "__main__":
    unittest.main()
