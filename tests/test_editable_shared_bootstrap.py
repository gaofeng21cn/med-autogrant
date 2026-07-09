from __future__ import annotations

import importlib
import json
import subprocess
import sys
import types
from pathlib import Path

import med_autogrant.editable_shared_bootstrap as module


def test_package_import_does_not_bootstrap_shared_paths() -> None:
    code = """
import json
import sys

before = list(sys.path)
import med_autogrant
print(json.dumps({
    "same_sys_path": before == sys.path,
    "bootstrap_imported": "med_autogrant.editable_shared_bootstrap" in sys.modules,
}))
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload == {
        "same_sys_path": True,
        "bootstrap_imported": False,
    }


def test_bootstrap_delegates_to_importable_shared_helper_without_touching_sys_path(monkeypatch) -> None:
    original_sys_path = list(sys.path)
    imported_module_names: list[str] = []
    helper_module = types.SimpleNamespace(
        ensure_repo_editable_dependency_paths=lambda **_: (module._repo_root() / "delegated-src",),
    )
    monkeypatch.setattr(
        module,
        "_module_spec",
        lambda module_name: object() if module_name == "opl_harness_shared.editable_consumer_launcher" else None,
    )
    monkeypatch.setattr(
        module.importlib,
        "import_module",
        lambda module_name: imported_module_names.append(module_name) or helper_module,
    )

    try:
        added = module.ensure_editable_dependency_paths()
    finally:
        sys.path[:] = original_sys_path

    assert added == (module._repo_root() / "delegated-src",)
    assert sys.path == original_sys_path
    assert imported_module_names == ["opl_harness_shared.editable_consumer_launcher"]


def test_bootstrap_returns_empty_when_shared_helper_is_not_importable(monkeypatch) -> None:
    original_sys_path = list(sys.path)
    imported_module_names: list[str] = []
    monkeypatch.setattr(module, "_module_spec", lambda module_name: None)
    monkeypatch.setattr(
        module.importlib,
        "import_module",
        lambda module_name: imported_module_names.append(module_name),
    )

    try:
        added = module.ensure_editable_dependency_paths()
    finally:
        sys.path[:] = original_sys_path

    assert added == ()
    assert sys.path == original_sys_path
    assert imported_module_names == []


def test_shared_dependency_entrypoints_are_resolvable_from_current_checkout() -> None:
    original_sys_path = list(sys.path)
    try:
        module.ensure_editable_dependency_paths()
        required_modules = (
            "opl_harness_shared.editable_consumer_launcher",
            "opl_harness_shared.family_entry_contracts",
            "opl_harness_shared.product_entry_companions",
            "opl_harness_shared.status_narration",
            "opl_harness_shared.workspace_boundary",
        )
        for module_name in required_modules:
            assert importlib.util.find_spec(module_name) is not None
            imported = importlib.import_module(module_name)
            assert getattr(imported, "__file__", None)
    finally:
        sys.path[:] = original_sys_path


def test_cli_and_contract_entrypoints_still_parse() -> None:
    from med_autogrant import cli
    from med_autogrant.domain_entry_contract import build_domain_entry_contract
    from opl_harness_shared.workspace_boundary import (
        DEFAULT_WORKSPACE_DOCUMENT,
        resolve_workspace_document_path,
    )

    parser = cli.build_parser()
    parsed = parser.parse_args(["foundry", "status"])
    contract = build_domain_entry_contract()

    assert parsed.command == "foundry-status"
    assert contract["product_entry_kind"] == "med_auto_grant_product_entry"
    workspace_path = resolve_workspace_document_path(
        Path.cwd(),
        default_filename=DEFAULT_WORKSPACE_DOCUMENT,
    )
    assert workspace_path.name == "workspace.json"
