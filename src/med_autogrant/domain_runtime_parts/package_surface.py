from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.artifact_bundle import build_artifact_bundle_document
from med_autogrant.final_package import build_final_package_document
from med_autogrant.hosted_contract_bundle import (
    _validate_required_final_package_fields,
    build_hosted_contract_bundle_document,
)
from med_autogrant.submission_ready import build_submission_ready_package_document
from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.workspace_projection_parts import _require_workspace_context
from med_autogrant.workspace_types import WorkspaceStateError

from med_autogrant.domain_runtime_parts.contracts import (
    build_hosted_authoring_contract as _build_hosted_authoring_contract,
    build_operator_contract as _build_operator_contract,
    build_runtime_state_contract as _build_runtime_state_contract,
    build_runtime_substrate_contract as _build_runtime_substrate_contract,
    build_schema_contract as _build_schema_contract,
    read_current_program_contract as _read_current_program_contract,
    read_program_id as _read_program_id,
    validate_contract_schema as _validate_contract_schema,
    validate_hosted_contract_bundle as _validate_hosted_contract_bundle,
)
from med_autogrant.domain_runtime_parts.io import (
    _guard_artifact_bundle_output_identity,
    _guard_final_package_output_identity,
    _guard_hosted_contract_output_identity,
    _guard_submission_ready_package_output_identity,
    _read_artifact_bundle,
    _read_final_package,
    _write_artifact_bundle_output,
    _write_final_package_output,
    _write_hosted_contract_bundle_output,
    _write_submission_ready_package_output,
)
from med_autogrant.domain_runtime_parts.shared import SUBMISSION_READY_PACKAGE_SCHEMA_FILE


class DomainRuntimePackageSurfaceMixin:
    def build_final_package(
        self,
        *,
        input_path: str | Path,
        artifact_bundle_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        context = _require_workspace_context(document)
        active_draft = context.active_draft
        artifact_bundle = _read_artifact_bundle(
            artifact_bundle_path,
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            draft_id=active_draft["draft_id"],
            lifecycle_stage=document.get("lifecycle_stage"),
        )
        final_package = build_final_package_document(
            document=document,
            artifact_bundle=artifact_bundle,
        )
        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_final_package_output_identity(
            resolved_output_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        _write_final_package_output(resolved_output_path, final_package)
        return {
            "ok": True,
            "command": "build-final-package",
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "lifecycle_stage": final_package["lifecycle_stage"],
            "output_path": str(resolved_output_path),
            "final_package": final_package,
        }

    def build_hosted_contract_bundle(
        self,
        *,
        final_package_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        final_package = _read_final_package(final_package_path)
        _validate_required_final_package_fields(final_package)
        current_program_contract = _read_current_program_contract()
        program_id = _read_program_id()
        hosted_contract_bundle = build_hosted_contract_bundle_document(
            final_package=final_package,
            program_id=program_id,
            runtime_substrate_contract=_build_runtime_substrate_contract(
                current_program_contract=current_program_contract,
            ),
            runtime_state_contract=_build_runtime_state_contract(),
            operator_contract=_build_operator_contract(),
            domain_entry_contract=build_domain_entry_contract(),
            schema_contract=_build_schema_contract(),
            authoring_contract=_build_hosted_authoring_contract(),
        )
        _validate_hosted_contract_bundle(
            hosted_contract_bundle,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_hosted_contract_output_identity(
            resolved_output_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            program_id=program_id,
        )
        _write_hosted_contract_bundle_output(resolved_output_path, hosted_contract_bundle)
        return {
            "ok": True,
            "command": "build-hosted-contract-bundle",
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "output_path": str(resolved_output_path),
            "hosted_contract_bundle": hosted_contract_bundle,
        }

    def build_submission_ready_package(
        self,
        *,
        input_path: str | Path,
        output_dir: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        artifact_bundle = build_artifact_bundle_document(document=document)
        final_package = build_final_package_document(
            document=document,
            artifact_bundle=artifact_bundle,
        )
        current_program_contract = _read_current_program_contract()
        program_id = _read_program_id()
        hosted_contract_bundle = build_hosted_contract_bundle_document(
            final_package=final_package,
            program_id=program_id,
            runtime_substrate_contract=_build_runtime_substrate_contract(
                current_program_contract=current_program_contract,
            ),
            runtime_state_contract=_build_runtime_state_contract(),
            operator_contract=_build_operator_contract(),
            domain_entry_contract=build_domain_entry_contract(),
            schema_contract=_build_schema_contract(),
            authoring_contract=_build_hosted_authoring_contract(),
        )
        _validate_hosted_contract_bundle(
            hosted_contract_bundle,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        submission_ready_package = build_submission_ready_package_document(
            document=document,
            artifact_bundle=artifact_bundle,
            final_package=final_package,
            hosted_contract_bundle=hosted_contract_bundle,
            program_id=program_id,
        )
        if not submission_ready_package["submission_ready"]:
            issue_ids = [
                item["issue_id"]
                for item in submission_ready_package["blocking_issues"]
                if isinstance(item, dict) and isinstance(item.get("issue_id"), str)
            ]
            raise WorkspaceStateError(
                f"submission ready package blocked: {', '.join(issue_ids)}",
                errors=[],
                grant_run_id=final_package["grant_run_id"],
                workspace_id=final_package["workspace_id"],
                lifecycle_stage=final_package["lifecycle_stage"],
            )
        _validate_contract_schema(
            submission_ready_package,
            schema_file=SUBMISSION_READY_PACKAGE_SCHEMA_FILE,
            context="submission_ready_package",
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )

        resolved_output_dir = Path(output_dir).expanduser().resolve()
        artifact_bundle_path = resolved_output_dir / "artifact-bundle.json"
        final_package_path = resolved_output_dir / "final-package.json"
        hosted_contract_bundle_path = resolved_output_dir / "hosted-contract-bundle.json"
        submission_ready_package_path = resolved_output_dir / "submission-ready-package.json"

        _guard_artifact_bundle_output_identity(
            artifact_bundle_path,
            grant_run_id=artifact_bundle["grant_run_id"],
            workspace_id=artifact_bundle["workspace_id"],
            draft_id=artifact_bundle["draft_id"],
            lifecycle_stage=artifact_bundle["lifecycle_stage"],
        )
        _guard_final_package_output_identity(
            final_package_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        _guard_hosted_contract_output_identity(
            hosted_contract_bundle_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            program_id=program_id,
        )
        _guard_submission_ready_package_output_identity(
            submission_ready_package_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            program_id=program_id,
        )

        _write_artifact_bundle_output(artifact_bundle_path, artifact_bundle)
        _write_final_package_output(final_package_path, final_package)
        _write_hosted_contract_bundle_output(hosted_contract_bundle_path, hosted_contract_bundle)
        _write_submission_ready_package_output(submission_ready_package_path, submission_ready_package)
        return {
            "ok": True,
            "command": "build-submission-ready-package",
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "lifecycle_stage": final_package["lifecycle_stage"],
            "output_dir": str(resolved_output_dir),
            "output_paths": {
                "artifact_bundle": str(artifact_bundle_path),
                "final_package": str(final_package_path),
                "hosted_contract_bundle": str(hosted_contract_bundle_path),
                "submission_ready_package": str(submission_ready_package_path),
            },
            "submission_ready_package": submission_ready_package,
        }
