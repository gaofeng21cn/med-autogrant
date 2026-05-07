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


def _relative_test_path(item: pytest.Item) -> str:
    path = Path(str(item.fspath)).resolve()
    return path.relative_to(REPO_ROOT).as_posix()


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    del config
    for item in items:
        relative_path = _relative_test_path(item)
        if relative_path in META_FILES:
            item.add_marker(pytest.mark.meta)
        if relative_path in REGRESSION_FILES:
            item.add_marker(pytest.mark.regression)
        if relative_path in STRUCTURE_FILES:
            item.add_marker(pytest.mark.structure)
