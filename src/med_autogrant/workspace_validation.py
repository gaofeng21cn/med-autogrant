from __future__ import annotations

from datetime import datetime
from typing import Any

from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace_parts import _validate_runtime_constraints
from med_autogrant.workspace_types import ValidationIssue, ValidationResult, WorkspaceStateError


def validate_workspace_document(document: dict[str, Any]) -> ValidationResult:
    issues: list[ValidationIssue] = []
    issues.extend(_validate_schema(document))
    if not issues:
        issues.extend(_validate_runtime_constraints(document))
    return ValidationResult(errors=issues)


def _validate_schema(document: dict[str, Any]) -> list[ValidationIssue]:
    validator = _SchemaSubsetValidator(SchemaStore())
    return validator.validate(document, "nsfc-workspace.schema.json")


class _SchemaSubsetValidator:
    def __init__(self, store: SchemaStore) -> None:
        self._store = store
        self._cache: dict[str, dict[str, Any]] = {}

    def validate(self, document: Any, schema_file: str) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        schema = self._load_schema(schema_file)
        self._validate_node(document, schema, schema_file, "", issues)
        return issues

    def _load_schema(self, file_name: str) -> dict[str, Any]:
        if file_name not in self._cache:
            self._cache[file_name] = self._store.load_json(file_name)
        return self._cache[file_name]

    def _resolve_ref(self, ref: str, base_file: str) -> tuple[dict[str, Any], str]:
        file_name, _, fragment = ref.partition("#")
        target_file = file_name or base_file
        schema = self._load_schema(target_file)
        if fragment:
            schema = self._resolve_pointer(schema, fragment)
        if not isinstance(schema, dict):
            raise WorkspaceStateError(f"无法解析 schema ref: {ref}")
        return schema, target_file

    def _resolve_pointer(self, schema: dict[str, Any], fragment: str) -> dict[str, Any]:
        pointer = fragment.removeprefix("/")
        current: Any = schema
        if not pointer:
            return schema
        for part in pointer.split("/"):
            token = part.replace("~1", "/").replace("~0", "~")
            current = current[token]
        if not isinstance(current, dict):
            raise WorkspaceStateError("schema pointer 未指向 object。")
        return current

    def _validate_node(
        self,
        value: Any,
        schema: dict[str, Any],
        base_file: str,
        path: str,
        issues: list[ValidationIssue],
    ) -> None:
        if "$ref" in schema:
            resolved, resolved_file = self._resolve_ref(schema["$ref"], base_file)
            merged = dict(resolved)
            for key, item in schema.items():
                if key != "$ref":
                    merged[key] = item
            self._validate_node(value, merged, resolved_file, path, issues)
            return

        resolved_type = self._resolve_schema_type(value=value, schema=schema, path=path, issues=issues)
        if resolved_type == "object":
            if not isinstance(value, dict):
                issues.append(ValidationIssue(path or "$", "必须是 object。"))
                return
            required = schema.get("required", [])
            for name in required:
                if name not in value:
                    issues.append(ValidationIssue(_join_path(path, name), "缺少必填字段。"))
            properties = schema.get("properties", {})
            if schema.get("additionalProperties") is False:
                for extra in value.keys() - properties.keys():
                    issues.append(ValidationIssue(_join_path(path, extra), "存在未声明字段。"))
            for name, child_schema in properties.items():
                if name in value:
                    self._validate_node(value[name], child_schema, base_file, _join_path(path, name), issues)
        elif resolved_type == "array":
            if not isinstance(value, list):
                issues.append(ValidationIssue(path or "$", "必须是 array。"))
                return
            min_items = schema.get("minItems")
            if isinstance(min_items, int) and len(value) < min_items:
                issues.append(ValidationIssue(path or "$", f"数组长度必须至少为 {min_items}。"))
            item_schema = schema.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(value):
                    self._validate_node(item, item_schema, base_file, f"{path}[{index}]" if path else f"[{index}]", issues)
        elif resolved_type == "string":
            if not isinstance(value, str):
                issues.append(ValidationIssue(path or "$", "必须是 string。"))
                return
            min_length = schema.get("minLength")
            if isinstance(min_length, int) and len(value) < min_length:
                issues.append(ValidationIssue(path or "$", f"字符串长度必须至少为 {min_length}。"))
            if schema.get("format") == "date-time":
                try:
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    issues.append(ValidationIssue(path or "$", "必须是合法的 date-time。"))
        elif resolved_type == "integer":
            if isinstance(value, bool) or not isinstance(value, int):
                issues.append(ValidationIssue(path or "$", "必须是 integer。"))
                return
            minimum = schema.get("minimum")
            maximum = schema.get("maximum")
            if isinstance(minimum, int) and value < minimum:
                issues.append(ValidationIssue(path or "$", f"必须大于等于 {minimum}。"))
            if isinstance(maximum, int) and value > maximum:
                issues.append(ValidationIssue(path or "$", f"必须小于等于 {maximum}。"))
        elif resolved_type == "boolean":
            if not isinstance(value, bool):
                issues.append(ValidationIssue(path or "$", "必须是 boolean。"))
                return
        elif resolved_type == "null":
            if value is not None:
                issues.append(ValidationIssue(path or "$", "必须是 null。"))
                return

        const_value = schema.get("const")
        if const_value is not None and value != const_value:
            issues.append(ValidationIssue(path or "$", f"必须等于 {const_value!r}。"))
        enum_values = schema.get("enum")
        if isinstance(enum_values, list) and value not in enum_values:
            issues.append(ValidationIssue(path or "$", "取值不在允许枚举内。"))

    def _resolve_schema_type(
        self,
        *,
        value: Any,
        schema: dict[str, Any],
        path: str,
        issues: list[ValidationIssue],
    ) -> str | None:
        expected_type = schema.get("type")
        if isinstance(expected_type, str):
            return expected_type
        if not isinstance(expected_type, list):
            return None

        allowed_types = [item for item in expected_type if isinstance(item, str)]
        if not allowed_types:
            return None

        actual_type = self._infer_json_type(value)
        if actual_type in allowed_types:
            return actual_type

        issues.append(
            ValidationIssue(
                path or "$",
                f"必须是 {' 或 '.join(allowed_types)}。",
            )
        )
        return None

    def _infer_json_type(self, value: Any) -> str | None:
        if value is None:
            return "null"
        if isinstance(value, dict):
            return "object"
        if isinstance(value, list):
            return "array"
        if isinstance(value, str):
            return "string"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "integer"
        return None


def _join_path(prefix: str, name: str) -> str:
    return f"{prefix}.{name}" if prefix else name

