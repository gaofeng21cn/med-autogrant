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


def test_bootstrap_adds_external_site_packages_when_shared_helper_imports_from_site_packages(
    monkeypatch,
    tmp_path: Path,
) -> None:
    fake_site_packages = tmp_path / "shared-env" / "venv" / "lib" / "python3.12" / "site-packages"
    fake_site_packages.mkdir(parents=True)
    fake_site_packages_str = str(fake_site_packages)
    original_sys_path = list(sys.path)
    sys.path[:] = [item for item in sys.path if item != fake_site_packages_str]
    imported_module_names: list[str] = []
    helper_module = types.SimpleNamespace(
        ensure_repo_editable_dependency_paths=lambda **_: (),
    )

    def fake_module_spec(module_name: str):
        if module_name != "opl_harness_shared.editable_consumer_launcher":
            return importlib.util.find_spec(module_name)
        if fake_site_packages_str not in sys.path:
            return None
        return object()

    monkeypatch.setattr(module, "_candidate_repo_site_packages_roots", lambda: (fake_site_packages,))
    monkeypatch.setattr(module, "_candidate_shared_helper_module_paths", lambda: ())
    monkeypatch.setattr(module, "_module_spec", fake_module_spec)
    monkeypatch.setattr(
        module.importlib,
        "import_module",
        lambda module_name: imported_module_names.append(module_name) or helper_module,
    )

    try:
        added = module.ensure_editable_dependency_paths()
    finally:
        sys.path[:] = original_sys_path

    assert added == (fake_site_packages,)
    assert imported_module_names == ["opl_harness_shared.editable_consumer_launcher"]


def test_bootstrap_delegates_to_sibling_owner_when_present(monkeypatch, tmp_path: Path) -> None:
    fake_repo_root = tmp_path / "med-autogrant" / ".worktrees" / "codex" / "bootstrap-thin"
    fake_repo_root.mkdir(parents=True)
    helper_root = tmp_path / "one-person-lab" / "python" / "opl-harness-shared" / "src"
    helper_path = helper_root / "opl_harness_shared" / "editable_consumer_launcher.py"
    helper_path.parent.mkdir(parents=True)
    helper_path.write_text(
        "from pathlib import Path\n"
        "def ensure_repo_editable_dependency_paths(*, repo_root, shared_package_name='opl_harness_shared'):\n"
        "    marker = Path(repo_root) / 'shared-helper-called.txt'\n"
        "    marker.write_text(shared_package_name, encoding='utf-8')\n"
        "    return (Path(repo_root) / 'delegated-src',)\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "_repo_root", lambda: fake_repo_root)
    monkeypatch.setattr(module, "_candidate_repo_site_packages_roots", lambda: ())
    monkeypatch.setattr(module, "_candidate_shared_src_roots", lambda: (helper_root,))

    original_sys_path = list(sys.path)
    try:
        added = module.ensure_editable_dependency_paths()
    finally:
        sys.path[:] = original_sys_path
        for module_name in list(sys.modules):
            if module_name == "opl_harness_shared" or module_name.startswith("opl_harness_shared."):
                sys.modules.pop(module_name, None)

    assert added == (fake_repo_root / "delegated-src",)
    assert (fake_repo_root / "shared-helper-called.txt").read_text(encoding="utf-8") == "opl_harness_shared"


def test_bootstrap_delegates_to_importable_shared_helper_without_touching_sys_path(monkeypatch) -> None:
    original_sys_path = list(sys.path)
    imported_module_names: list[str] = []
    helper_module = types.SimpleNamespace(
        ensure_repo_editable_dependency_paths=lambda **_: (),
    )
    monkeypatch.setattr(module, "_candidate_shared_helper_module_paths", lambda: ())
    monkeypatch.setattr(
        module,
        "_module_spec",
        lambda module_name: object() if module_name == "opl_harness_shared.editable_consumer_launcher" else None,
    )
    monkeypatch.setattr(module, "_candidate_repo_site_packages_roots", lambda: ())
    monkeypatch.setattr(
        module.importlib,
        "import_module",
        lambda module_name: imported_module_names.append(module_name) or helper_module,
    )

    try:
        added = module.ensure_editable_dependency_paths()
    finally:
        sys.path[:] = original_sys_path

    assert added == ()
    assert sys.path == original_sys_path
    assert imported_module_names == ["opl_harness_shared.editable_consumer_launcher"]


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
    from med_autogrant.workspace_scaffold import resolve_mag_directory_workspace_document_path

    parser = cli.build_parser()
    parsed = parser.parse_args(["foundry", "status"])
    contract = build_domain_entry_contract()

    assert parsed.command == "foundry-status"
    assert contract["product_entry_kind"] == "med_auto_grant_product_entry"
    assert resolve_mag_directory_workspace_document_path("workspace-root").name == "workspace.json"
