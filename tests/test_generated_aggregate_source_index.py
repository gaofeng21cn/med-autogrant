from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import scripts.check_generated_aggregate_sources as aggregate_checker
from med_autogrant.opl_standard_pack import build_standard_pack


pytestmark = pytest.mark.meta

REPO_ROOT = aggregate_checker.REPO_ROOT
SOURCE_INDEX_PATH = aggregate_checker.INDEX_PATH


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def _source_index() -> dict[str, object]:
    return json.loads(SOURCE_INDEX_PATH.read_text(encoding="utf-8"))


def test_generated_aggregate_source_index_declares_leaf_source_policy() -> None:
    payload = _source_index()

    assert payload["surface_kind"] == "mag_generated_aggregate_source_index"
    assert payload["version"] == "mag-generated-aggregate-source-index.v1"
    assert payload["target_domain_id"] == "med-autogrant"
    assert payload["manual_edit_policy"] == "edit_leaf_sources_then_regenerate_or_update_pinned_schema_record"
    assert payload["consumer_path_policy"] == "aggregate_paths_remain_stable_for_existing_consumers"
    assert payload["line_budget_policy"] == "do_not_relax_line_budget_for_large_aggregate_surfaces"

    aggregate_ids = {item["aggregate_id"] for item in payload["aggregates"]}
    assert aggregate_ids == {
        "stage_control_plane",
        "functional_privatization_audit",
        "product_entry_manifest_schema",
    }


def test_generated_aggregates_match_canonical_builder_outputs() -> None:
    payload = _source_index()
    generated = build_standard_pack()

    generated_items = [
        item
        for item in payload["aggregates"]
        if item["maintenance_shape"] == "generated_aggregate"
    ]
    assert generated_items

    for item in generated_items:
        aggregate_path = item["aggregate_path"]
        builder_key = item["builder_output_key"]
        assert _read_json(aggregate_path) == generated[builder_key]


def test_aggregate_leaf_source_refs_exist_and_do_not_point_back_to_aggregate() -> None:
    payload = _source_index()

    for item in payload["aggregates"]:
        aggregate_path = item["aggregate_path"]
        leaf_sources = item["leaf_source_refs"]
        assert leaf_sources, aggregate_path
        assert aggregate_path not in leaf_sources
        for leaf_source in leaf_sources:
            assert (REPO_ROOT / leaf_source).exists(), f"{aggregate_path} leaf source missing: {leaf_source}"


def test_product_entry_manifest_schema_is_pinned_when_no_safe_generator_exists() -> None:
    payload = _source_index()
    schema_record = next(
        item
        for item in payload["aggregates"]
        if item["aggregate_id"] == "product_entry_manifest_schema"
    )

    assert schema_record["maintenance_shape"] == "pinned_aggregate_schema"
    assert schema_record["safe_generator_available"] is False
    assert schema_record["builder_output_key"] is None
    assert schema_record["manual_edit_allowed"] is False
    assert schema_record["checker_policy"] == (
        "check_leaf_source_refs_and_schema_registry_consumers_until_a_schema_generator_lands"
    )


def test_generated_aggregate_checker_runs_cleanly() -> None:
    result = subprocess.run(
        [
            str(REPO_ROOT / "scripts" / "run-python-clean.sh"),
            "scripts/check_generated_aggregate_sources.py",
        ],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "generated aggregate source index ok" in result.stdout


def test_meta_lane_runs_generated_aggregate_checker() -> None:
    verify_script = (REPO_ROOT / "scripts" / "verify.sh").read_text(encoding="utf-8")
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    assert "make test-meta" in verify_script
    assert "test-generated-aggregate-sources:" in makefile
    assert "$(PYTHON_CLEAN) scripts/check_generated_aggregate_sources.py" in makefile
    assert "$(MAKE) test-generated-aggregate-sources" in makefile
