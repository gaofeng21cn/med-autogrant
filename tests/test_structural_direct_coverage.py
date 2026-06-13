from __future__ import annotations

import med_autogrant.artifact_bundle as artifact_bundle
import med_autogrant.artifact_bundle_validation as artifact_bundle_validation
import med_autogrant.authoring_executor_parts as authoring_executor_parts
import med_autogrant.final_package as final_package
import med_autogrant.final_package_validation as final_package_validation
import med_autogrant.grant_autonomy_controller_plan as grant_autonomy_controller_plan
import med_autogrant.grant_autonomy_report_resume as grant_autonomy_report_resume
import med_autogrant.grant_autonomy_start as grant_autonomy_start
import med_autogrant.grant_quality_assessment as grant_quality_assessment
import med_autogrant.grant_quality_closure as grant_quality_closure
import med_autogrant.grant_quality_parts as grant_quality_parts
import med_autogrant.domain_runtime_parts.contracts as contracts
import med_autogrant.domain_runtime_parts.io as io
import med_autogrant.domain_runtime_parts.package_surface as package_surface
import med_autogrant.domain_runtime_parts.shared as shared
import med_autogrant.domain_runtime_parts.substrate as substrate
import med_autogrant.mainline_status as mainline_status
import med_autogrant.product_entry_parts.autonomy_observability as autonomy_observability
import med_autogrant.product_entry_parts.entry as entry
import med_autogrant.product_entry_parts.evidence as evidence
import med_autogrant.product_entry_parts.loop_contracts as loop_contracts
import med_autogrant.product_entry_parts.manifest as manifest
import med_autogrant.product_entry_parts.manifest_builder as manifest_builder
import med_autogrant.product_entry_parts.manifest_readiness as manifest_readiness
import med_autogrant.product_entry_parts.manifest_skill_catalog as manifest_skill_catalog
import med_autogrant.product_entry_parts.owner_receipt_writers as owner_receipt_writers
import med_autogrant.product_entry_parts.preflight as preflight
import med_autogrant.product_entry_parts.primitives as primitives
import med_autogrant.product_entry_parts.progress as progress
import med_autogrant.product_entry_parts.runtime_registration as runtime_registration
import med_autogrant.product_entry_parts.runtime_contracts as runtime_contracts
import med_autogrant.product_entry_parts.runtime_surfaces as runtime_surfaces
import med_autogrant.revision_executor as revision_executor
import med_autogrant.runtime_defaults as runtime_defaults
import med_autogrant.schema_loader as schema_loader
import med_autogrant.schema_subset_validator as schema_subset_validator
import med_autogrant.stage_control_plane as stage_control_plane
import med_autogrant.submission_ready as submission_ready
import med_autogrant.workspace_parts as workspace_parts
import med_autogrant.workspace_projection_parts as workspace_projection_parts
import med_autogrant.workspace_reference_validation as workspace_reference_validation
import med_autogrant.workspace_runtime_constraints as workspace_runtime_constraints
import med_autogrant.workspace_scaffold as workspace_scaffold
import med_autogrant.workspace_types as workspace_types
import med_autogrant.workspace_validation as workspace_validation


def test_structural_leaf_modules_expose_expected_contract_surfaces() -> None:
    assert artifact_bundle.build_artifact_bundle_document
    assert artifact_bundle_validation.REQUIRED_ARTIFACT_BUNDLE_OBJECT_FIELDS
    assert authoring_executor_parts._fresh_metadata
    assert final_package.build_final_package_document
    assert final_package_validation.SUPPORTED_FINAL_PACKAGE_VERSION == 1
    assert grant_autonomy_report_resume._build_report
    assert grant_autonomy_controller_plan._normalize_controller_plan
    assert grant_autonomy_start._resolve_grant_autonomy_start
    assert grant_quality_assessment._resolve_dimension_status
    assert grant_quality_closure._build_quality_closure_packages
    assert grant_quality_parts._build_issue
    assert grant_quality_parts._read_active_draft_id
    assert mainline_status.read_mainline_status
    assert revision_executor.build_revision_execution_document
    assert schema_loader.SchemaStore
    assert schema_subset_validator.SchemaSubsetValidator
    assert submission_ready.build_submission_ready_package_document
    assert workspace_parts._validate_runtime_constraints
    assert workspace_projection_parts._build_workspace_state
    assert workspace_reference_validation._draft_sections_link_object
    assert workspace_runtime_constraints._validate_runtime_constraints
    assert workspace_scaffold.resolve_mag_workspace_document_path
    assert workspace_types.ValidationIssue("x", "y").path == "x"
    assert workspace_validation._validate_schema


def test_runtime_and_product_entry_leaf_modules_keep_split_contracts() -> None:
    assert contracts.build_runtime_substrate_contract
    assert io._read_active_draft_id({"current_selection": {"active_draft_id": "draft-1"}}) == "draft-1"
    assert package_surface.DomainRuntimePackageSurfaceMixin.build_final_package
    assert shared.PRODUCT_ENTRY_SCHEMA_FILE == "product-entry.schema.json"
    assert substrate.MagDomainRuntime.__name__ == "MagDomainRuntime"
    assert autonomy_observability.build_grant_autonomy_observability
    assert entry.MedAutoGrantProductEntry
    assert evidence.ProductEntryEvidenceMixin
    assert loop_contracts._build_mainline_snapshot
    assert manifest.ProductEntryManifestMixin
    assert manifest_builder.ProductEntryManifestBuilderMixin
    assert manifest_readiness.build_manifest_readiness_surfaces
    assert manifest_skill_catalog.build_product_entry_skill_catalog
    assert owner_receipt_writers.write_owner_receipt_evidence
    assert owner_receipt_writers.write_lifecycle_receipt_evidence
    assert preflight.ProductEntryPreflightMixin
    assert primitives.TARGET_DOMAIN_ID == "med-autogrant"
    assert primitives._require_entry_mode("direct") == "direct"
    assert progress.ProductEntryProgressMixin
    assert runtime_contracts.PRODUCT_ENTRY_SCHEMA_FILE == "product-entry.schema.json"
    runtime_summary = runtime_defaults.build_default_runtime_summary(
        current_owner_line="OPL hosted runtime owns task execution"
    )
    assert runtime_summary["runtime_owner"] == runtime_defaults.DEFAULT_RUNTIME_OWNER
    assert runtime_summary["default_task_runtime_owner"] == "one-person-lab"
    assert runtime_summary["default_stage_executor"] == "codex_cli"
    assert runtime_summary["optional_carriers"] == ["hermes_agent", "claude_code"]
    assert runtime_defaults.parse_opl_command({}) == ("opl",)
    assert runtime_defaults.parse_opl_command({"MED_AUTOGRANT_OPL_COMMAND": "opl run --json"}) == (
        "opl",
        "run",
        "--json",
    )
    assert runtime_registration._build_opl_stage_runtime_registration
    assert runtime_surfaces._build_runtime_continuity_surfaces
    assert stage_control_plane.DEFAULT_GOLDEN_PATH_STAGE_ID == "call_and_candidate_intake"
    assert stage_control_plane.build_mag_family_stage_control_plane
