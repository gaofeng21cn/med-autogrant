#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.opl_standard_pack import build_standard_pack


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "contracts" / "generated_aggregate_source_index.json"
GENERATED_SHAPE = "generated_aggregate"
PINNED_SCHEMA_SHAPE = "pinned_aggregate_schema"


def main() -> int:
    index = _load_json(INDEX_PATH)
    _validate_index_header(index)
    generated = build_standard_pack()

    errors: list[str] = []
    for aggregate in _require_list(index, "aggregates", context="source_index"):
        if not isinstance(aggregate, Mapping):
            errors.append("source_index.aggregates contains a non-object item")
            continue
        errors.extend(_validate_aggregate(aggregate, generated=generated))

    if errors:
        print("generated aggregate source index check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("generated aggregate source index ok")
    return 0


def _validate_index_header(index: Mapping[str, Any]) -> None:
    expected = {
        "surface_kind": "mag_generated_aggregate_source_index",
        "version": "mag-generated-aggregate-source-index.v1",
        "target_domain_id": "med-autogrant",
    }
    for field, value in expected.items():
        if index.get(field) != value:
            raise SystemExit(
                f"generated aggregate source index invalid {field}: {index.get(field)!r}"
            )


def _validate_aggregate(
    aggregate: Mapping[str, Any],
    *,
    generated: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    aggregate_id = _string(aggregate.get("aggregate_id"), "aggregate_id", errors)
    aggregate_path = _string(aggregate.get("aggregate_path"), "aggregate_path", errors)
    maintenance_shape = _string(
        aggregate.get("maintenance_shape"),
        f"{aggregate_id}.maintenance_shape",
        errors,
    )
    leaf_source_refs = _string_list(
        aggregate.get("leaf_source_refs"),
        f"{aggregate_id}.leaf_source_refs",
        errors,
    )

    if not aggregate_path:
        return errors
    path = REPO_ROOT / aggregate_path
    if not path.is_file():
        errors.append(f"{aggregate_id}: aggregate_path does not exist: {aggregate_path}")
        return errors
    if aggregate_path in leaf_source_refs:
        errors.append(f"{aggregate_id}: leaf_source_refs must not include the aggregate path")
    for leaf_source in leaf_source_refs:
        if not (REPO_ROOT / leaf_source).exists():
            errors.append(f"{aggregate_id}: leaf source missing: {leaf_source}")
    consumer_refs = _string_list(
        aggregate.get("consumer_refs"),
        f"{aggregate_id}.consumer_refs",
        errors,
    )
    for consumer_ref in consumer_refs:
        if not (REPO_ROOT / consumer_ref).exists():
            errors.append(f"{aggregate_id}: consumer ref missing: {consumer_ref}")

    if maintenance_shape == GENERATED_SHAPE:
        errors.extend(_validate_generated_aggregate(aggregate, generated=generated))
    elif maintenance_shape == PINNED_SCHEMA_SHAPE:
        errors.extend(_validate_pinned_schema_aggregate(aggregate))
    else:
        errors.append(f"{aggregate_id}: unsupported maintenance_shape: {maintenance_shape!r}")
    return errors


def _validate_generated_aggregate(
    aggregate: Mapping[str, Any],
    *,
    generated: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    aggregate_id = str(aggregate["aggregate_id"])
    aggregate_path = str(aggregate["aggregate_path"])
    builder_output_key = _string(
        aggregate.get("builder_output_key"),
        f"{aggregate_id}.builder_output_key",
        errors,
    )
    if aggregate.get("safe_generator_available") is not True:
        errors.append(f"{aggregate_id}: generated aggregate must declare safe_generator_available=true")
    if aggregate.get("manual_edit_allowed") is not False:
        errors.append(f"{aggregate_id}: generated aggregate must forbid manual edits")
    if aggregate.get("checker_policy") != "aggregate_must_equal_builder_output":
        errors.append(f"{aggregate_id}: generated aggregate checker_policy mismatch")
    if not builder_output_key:
        return errors
    if builder_output_key not in generated:
        errors.append(f"{aggregate_id}: builder_output_key not emitted by build_standard_pack")
        return errors

    actual = _load_json(REPO_ROOT / aggregate_path)
    expected = json.loads(json.dumps(generated[builder_output_key], ensure_ascii=False))
    if actual != expected:
        errors.append(
            f"{aggregate_id}: {aggregate_path} is stale; run "
            "scripts/run-python-clean.sh -m med_autogrant.opl_standard_pack"
        )
    return errors


def _validate_pinned_schema_aggregate(aggregate: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    aggregate_id = str(aggregate["aggregate_id"])
    if aggregate.get("safe_generator_available") is not False:
        errors.append(f"{aggregate_id}: pinned schema must declare safe_generator_available=false")
    if aggregate.get("builder_output_key") is not None:
        errors.append(f"{aggregate_id}: pinned schema must not declare a builder_output_key")
    if aggregate.get("manual_edit_allowed") is not False:
        errors.append(f"{aggregate_id}: pinned schema must forbid direct manual edits")
    expected_policy = "check_leaf_source_refs_and_schema_registry_consumers_until_a_schema_generator_lands"
    if aggregate.get("checker_policy") != expected_policy:
        errors.append(f"{aggregate_id}: pinned schema checker_policy mismatch")
    return errors


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_list(payload: Mapping[str, Any], key: str, *, context: str) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise SystemExit(f"{context}.{key} must be a list")
    return value


def _string(value: Any, field: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value:
        errors.append(f"{field} must be a non-empty string")
        return ""
    return value


def _string_list(value: Any, field: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{field} must be a non-empty string list")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            errors.append(f"{field} contains a non-string item")
            continue
        result.append(item)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
