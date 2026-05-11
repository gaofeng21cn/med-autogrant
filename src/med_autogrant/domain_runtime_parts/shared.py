from __future__ import annotations

from pathlib import Path

from med_autogrant.workspace_types import WorkspaceError


JOURNAL_VERSION = 1
CURRENT_PROGRAM_RELATIVE_PATH = Path("contracts/runtime-program/current-program.json")
EXECUTOR_ROUTING_CONTRACT_VERSION = 1
EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE = "executor-routing-contract.schema.json"
PRODUCT_ENTRY_SCHEMA_FILE = "product-entry.schema.json"
GRANT_PROGRESS_SCHEMA_FILE = "grant-progress.schema.json"
GRANT_COCKPIT_SCHEMA_FILE = "grant-cockpit.schema.json"
GRANT_DIRECT_ENTRY_SCHEMA_FILE = "grant-direct-entry.schema.json"
GRANT_USER_LOOP_SCHEMA_FILE = "grant-user-loop.schema.json"
PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE = "product-entry-manifest.schema.json"
PRODUCT_STATUS_SCHEMA_FILE = "product-status.schema.json"
GRANT_INTAKE_AUDIT_SCHEMA_FILE = "grant-intake-audit.schema.json"
GRANT_EVIDENCE_GROUNDING_SCHEMA_FILE = "grant-evidence-grounding.schema.json"
GRANT_QUALITY_SCORECARD_SCHEMA_FILE = "grant-quality-scorecard.schema.json"
GRANT_QUALITY_DIFF_SCHEMA_FILE = "grant-quality-diff.schema.json"
GRANT_QUALITY_CLOSURE_DOSSIER_SCHEMA_FILE = "grant-quality-closure-dossier.schema.json"
GRANT_AUTONOMY_CONTROLLER_INPUT_SCHEMA_FILE = "grant-autonomy-controller-input.schema.json"
GRANT_AUTONOMY_CONTROLLER_REPORT_SCHEMA_FILE = "grant-autonomy-controller-report.schema.json"
HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE = "hosted-contract-bundle.schema.json"
SUBMISSION_READY_PACKAGE_SCHEMA_FILE = "submission-ready-package.schema.json"
PROJECT_PROFILE_SELECTION_INPUT_SCHEMA_FILE = "project-profile-selection-input.schema.json"
PROJECT_PROFILE_SELECTION_SCHEMA_FILE = "project-profile-selection.schema.json"
CRITIQUE_LOOP_REPORT_SCHEMA_FILE = "critique-loop-report.schema.json"
FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE = "funding-landscape-discovery-input.schema.json"
FUNDING_LANDSCAPE_DISCOVERY_SCHEMA_FILE = "funding-landscape-discovery.schema.json"
FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE = "funding-landscape-cache.schema.json"
FUNDING_LANDSCAPE_DIFF_REPORT_SCHEMA_FILE = "funding-landscape-diff-report.schema.json"
AUTHORING_MAINLINE_LOOP_REPORT_SCHEMA_FILE = "authoring-mainline-loop-report.schema.json"
SCHEMA_INDEX_RELATIVE_PATH = "schemas/v1/schema-index.json"
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
HOSTED_CONTRACT_SCHEMA_FILES = (
    "service-safe-domain-surface.schema.json",
    "executor-routing-contract.schema.json",
    "product-entry.schema.json",
    "grant-intake-audit.schema.json",
    "grant-evidence-grounding.schema.json",
    "grant-quality-scorecard.schema.json",
    "grant-quality-closure-dossier.schema.json",
    "grant-quality-diff.schema.json",
    "grant-autonomy-controller-input.schema.json",
    "grant-autonomy-controller-report.schema.json",
    "funding-landscape-discovery-input.schema.json",
    "funding-landscape-discovery.schema.json",
    "funding-landscape-cache.schema.json",
    "funding-landscape-diff-report.schema.json",
    "project-profile-selection-input.schema.json",
    "project-profile-selection.schema.json",
    "critique-loop-report.schema.json",
    "authoring-mainline-loop-report.schema.json",
    "hosted-contract-bundle.schema.json",
    "submission-ready-package.schema.json",
)
AUTHOR_SIDE_ROUTE_IDS = (
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
    "artifact_bundle",
    "final_package",
    "hosted_contract_bundle",
)
EXECUTOR_ROUTE_OWNER = "med-autogrant"


class LocalRuntimeStateError(WorkspaceError):
    """Local runtime journal/state mismatch。"""
