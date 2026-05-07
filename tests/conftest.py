from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]

META_FILES = {
    "tests/test_program_control_surfaces.py",
    "tests/test_repository_hygiene.py",
}

REGRESSION_FILES = {
    "tests/test_artifact_bundle.py",
    "tests/test_cli_validate_workspace.py",
    "tests/test_cli_validate_workspace_error_cases.py",
    "tests/test_cli_validate_workspace_product_entry_cases.py",
    "tests/test_cli_validate_workspace_revision_cases.py",
    "tests/test_final_package.py",
    "tests/test_grant_autonomy_controller.py",
    "tests/test_hermes_runtime.py",
    "tests/test_hermes_runtime_split.py",
    "tests/test_hosted_contract_bundle.py",
    "tests/test_hosted_contract_bundle_checkpoint_cases.py",
    "tests/test_hosted_contract_bundle_control_plane.py",
    "tests/test_local_runtime.py",
    "tests/test_product_entry.py",
    "tests/test_submission_ready_package.py",
    "tests/test_upstream_hermes.py",
    "tests/test_workspace_summary.py",
}

STRUCTURE_FILES = {
    "tests/test_line_budget.py",
    "tests/test_runtime_cli_structural_helpers.py",
    "tests/test_sentrux_governance.py",
    "tests/test_structural_direct_coverage.py",
}

PRODUCT_ENTRY_AGGREGATOR = "tests/test_product_entry.py"


def _relative_test_path(item: pytest.Item) -> str:
    path = Path(str(item.fspath)).resolve()
    return path.relative_to(REPO_ROOT).as_posix()


def _is_explicit_path_request(relative_path: str, config: pytest.Config) -> bool:
    target = (REPO_ROOT / relative_path).resolve()
    for arg in config.args:
        requested = arg.split("::", 1)[0]
        if not requested:
            continue
        requested_path = Path(requested)
        if not requested_path.is_absolute():
            requested_path = REPO_ROOT / requested_path
        if requested_path.resolve() == target:
            return True
    return False


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool:
    relative_path = collection_path.resolve().relative_to(REPO_ROOT).as_posix()
    if relative_path == PRODUCT_ENTRY_AGGREGATOR:
        return not _is_explicit_path_request(PRODUCT_ENTRY_AGGREGATOR, config)
    return False


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    del config
    for item in items:
        relative_path = _relative_test_path(item)
        if relative_path in META_FILES:
            item.add_marker(pytest.mark.meta)
        if relative_path in REGRESSION_FILES or relative_path.startswith("tests/product_entry_cases/"):
            item.add_marker(pytest.mark.regression)
        if relative_path in STRUCTURE_FILES:
            item.add_marker(pytest.mark.structure)
