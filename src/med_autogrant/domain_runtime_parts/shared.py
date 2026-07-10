from __future__ import annotations

from pathlib import Path


CURRENT_PROGRAM_RELATIVE_PATH = Path("contracts/runtime-program/current-program.json")
EXECUTOR_ROUTING_CONTRACT_VERSION = 1
EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE = "executor-routing-contract.schema.json"
GRANT_INTAKE_AUDIT_SCHEMA_FILE = "grant-intake-audit.schema.json"
GRANT_EVIDENCE_GROUNDING_SCHEMA_FILE = "grant-evidence-grounding.schema.json"
GRANT_QUALITY_SCORECARD_SCHEMA_FILE = "grant-quality-scorecard.schema.json"
GRANT_QUALITY_DIFF_SCHEMA_FILE = "grant-quality-diff.schema.json"
GRANT_QUALITY_CLOSURE_DOSSIER_SCHEMA_FILE = "grant-quality-closure-dossier.schema.json"
HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE = "hosted-contract-bundle.schema.json"
SUBMISSION_READY_PACKAGE_SCHEMA_FILE = "submission-ready-package.schema.json"
PROJECT_PROFILE_SELECTION_INPUT_SCHEMA_FILE = "project-profile-selection-input.schema.json"
PROJECT_PROFILE_SELECTION_SCHEMA_FILE = "project-profile-selection.schema.json"
FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE = "funding-landscape-discovery-input.schema.json"
FUNDING_LANDSCAPE_DISCOVERY_SCHEMA_FILE = "funding-landscape-discovery.schema.json"
FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE = "funding-landscape-cache.schema.json"
FUNDING_LANDSCAPE_DIFF_REPORT_SCHEMA_FILE = "funding-landscape-diff-report.schema.json"
SCHEMA_INDEX_RELATIVE_PATH = "schemas/v1/schema-index.json"
GENERATED_SESSION_SURFACE_REF = "opl://generated-surfaces/mag/product-entry-session"
GENERATED_SESSION_RESUME_SURFACE_REF = "opl://generated-surfaces/mag/product-entry-session#resume"
DOMAIN_AUTHORITY_SURFACE_REF = "/product_entry_manifest/owner_receipt_contract"
HOSTED_CONTRACT_SCHEMA_FILES = (
    "service-safe-domain-surface.schema.json",
    "executor-routing-contract.schema.json",
    "product-entry.schema.json",
    "grant-intake-audit.schema.json",
    "grant-evidence-grounding.schema.json",
    "grant-quality-scorecard.schema.json",
    "grant-quality-closure-dossier.schema.json",
    "grant-quality-diff.schema.json",
    "funding-landscape-discovery-input.schema.json",
    "funding-landscape-discovery.schema.json",
    "funding-landscape-cache.schema.json",
    "funding-landscape-diff-report.schema.json",
    "project-profile-selection-input.schema.json",
    "project-profile-selection.schema.json",
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
