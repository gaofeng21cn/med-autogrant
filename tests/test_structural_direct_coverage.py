from __future__ import annotations

from pathlib import Path

import med_autogrant.artifact_bundle as artifact_bundle
import med_autogrant.artifact_bundle_validation as artifact_bundle_validation
import med_autogrant.authoring_executor_parts as authoring_executor_parts
import med_autogrant.facade_exports as facade_exports
import med_autogrant.final_package as final_package
import med_autogrant.final_package_validation as final_package_validation
import med_autogrant.grant_autonomy_parts as grant_autonomy_parts
import med_autogrant.grant_autonomy_start as grant_autonomy_start
import med_autogrant.grant_quality_assessment as grant_quality_assessment
import med_autogrant.grant_quality_closure as grant_quality_closure
import med_autogrant.grant_quality_parts as grant_quality_parts
import med_autogrant.hermes_runtime_parts.contracts as contracts
import med_autogrant.hermes_runtime_parts.io as io
import med_autogrant.hermes_runtime_parts.shared as shared
import med_autogrant.hermes_runtime_parts.substrate as substrate
import med_autogrant.mainline_status as mainline_status
import med_autogrant.product_entry_parts.autonomy_observability as autonomy_observability
import med_autogrant.product_entry_parts.entry as entry
import med_autogrant.product_entry_parts.loop_contracts as loop_contracts
import med_autogrant.product_entry_parts.manifest as manifest
import med_autogrant.product_entry_parts.manifest_builder as manifest_builder
import med_autogrant.product_entry_parts.manifest_skill_catalog as manifest_skill_catalog
import med_autogrant.product_entry_parts.preflight as preflight
import med_autogrant.product_entry_parts.progress as progress
import med_autogrant.product_entry_parts.runtime_contracts as runtime_contracts
import med_autogrant.product_entry_parts.runtime_surfaces as runtime_surfaces
import med_autogrant.revision_executor as revision_executor
import med_autogrant.schema_loader as schema_loader
import med_autogrant.schema_subset_validator as schema_subset_validator
import med_autogrant.submission_ready as submission_ready
import med_autogrant.workspace_index as workspace_index
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
    assert grant_autonomy_parts._build_report
    assert grant_autonomy_start._resolve_grant_autonomy_start
    assert grant_quality_assessment._resolve_dimension_status
    assert grant_quality_closure._build_quality_closure_packages
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
    assert shared.PRODUCT_ENTRY_SCHEMA_FILE == "product-entry.schema.json"
    assert substrate.HermesRuntimeSubstrate.__name__ == "HermesRuntimeSubstrate"
    assert autonomy_observability.build_grant_autonomy_observability
    assert entry.MedAutoGrantProductEntry
    assert loop_contracts._build_mainline_snapshot
    assert manifest.ProductEntryManifestMixin
    assert manifest_builder.ProductEntryManifestBuilderMixin
    assert manifest_skill_catalog.build_product_entry_skill_catalog
    assert preflight.ProductEntryPreflightMixin
    assert progress.ProductEntryProgressMixin
    assert runtime_contracts.PRODUCT_ENTRY_SCHEMA_FILE == "product-entry.schema.json"
    assert runtime_surfaces._build_runtime_continuity_surfaces


def test_workspace_index_and_facade_export_helpers_have_direct_behavior() -> None:
    issues: list[workspace_types.ValidationIssue] = []
    indexed = workspace_index._index_objects(
        [{"item_id": "a"}, {"item_id": "a"}],
        "item_id",
        "items",
        issues,
    )

    assert indexed == {"a": {"item_id": "a"}}
    assert [(issue.path, issue.message) for issue in issues] == [("items[1].item_id", "item_id 不能重复。")]

    namespace: dict[str, object] = {}
    facade_exports.re_export_public_names(Path, namespace)
    assert "cwd" in namespace
    assert "_flavour" not in namespace
