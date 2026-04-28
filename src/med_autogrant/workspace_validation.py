from __future__ import annotations

from typing import Any

from med_autogrant.schema_loader import SchemaStore
from med_autogrant.schema_subset_validator import SchemaSubsetValidator as _SchemaSubsetValidator
from med_autogrant.workspace_runtime_constraints import _validate_runtime_constraints
from med_autogrant.workspace_types import ValidationIssue, ValidationResult


def validate_workspace_document(document: dict[str, Any]) -> ValidationResult:
    issues: list[ValidationIssue] = []
    issues.extend(_validate_schema(document))
    if not issues:
        issues.extend(_validate_runtime_constraints(document))
    return ValidationResult(errors=issues)


def _validate_schema(document: dict[str, Any]) -> list[ValidationIssue]:
    validator = _SchemaSubsetValidator(SchemaStore())
    return validator.validate(document, "nsfc-workspace.schema.json")
