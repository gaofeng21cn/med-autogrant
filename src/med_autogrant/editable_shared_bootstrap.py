from __future__ import annotations

import importlib
import importlib.util
import os
import sys
import tempfile
from pathlib import Path


_SHARED_HELPER_MODULE_NAME = "opl_harness_shared.editable_consumer_launcher"
_SHARED_HELPER_MODULE_FILE = "editable_consumer_launcher.py"
_SHARED_PACKAGE_NAME = "opl_harness_shared"


def _module_spec(module_name: str):
    try:
        return importlib.util.find_spec(module_name)
    except ModuleNotFoundError:
        return None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _candidate_repo_site_packages_roots() -> tuple[Path, ...]:
    repo_root = _repo_root()
    external_root = Path(
        os.environ.get("MED_AUTOGRANT_EDITABLE_SHARED_ENV_ROOT", "")
        or Path(tempfile.gettempdir()) / "med-autogrant-editable-shared" / repo_root.name
    ).expanduser()
    venv_root = external_root / "venv"
    versioned_site_packages = (
        venv_root / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    )
    windows_site_packages = venv_root / "Lib" / "site-packages"
    return (
        versioned_site_packages,
        windows_site_packages,
    )


def _candidate_shared_src_roots() -> tuple[Path, ...]:
    repo_root = _repo_root()
    candidate_base_roots = [repo_root.parent]
    for ancestor in repo_root.parents:
        if ancestor.name in {".worktrees", "worktrees"} and ancestor.parent.parent not in candidate_base_roots:
            candidate_base_roots.append(ancestor.parent.parent)

    unique_base_roots: list[Path] = []
    for candidate in candidate_base_roots:
        if candidate not in unique_base_roots:
            unique_base_roots.append(candidate)

    return tuple(
        base_root / "one-person-lab" / "python" / "opl-harness-shared" / "src"
        for base_root in unique_base_roots
    )


def _explicit_shared_src_roots_from_sys_path() -> tuple[Path, ...]:
    roots: list[Path] = []
    for entry in sys.path:
        if not entry:
            continue
        candidate = Path(entry).expanduser()
        if not (candidate / _SHARED_PACKAGE_NAME / _SHARED_HELPER_MODULE_FILE).exists():
            continue
        resolved = candidate.resolve()
        if resolved not in roots:
            roots.append(resolved)
    return tuple(roots)


def _candidate_shared_helper_module_paths() -> tuple[Path, ...]:
    return tuple(
        candidate_root / _SHARED_PACKAGE_NAME / _SHARED_HELPER_MODULE_FILE
        for candidate_root in _candidate_shared_src_roots()
    )


def _prepend_path(candidate_root: Path) -> bool:
    if not candidate_root.exists():
        return False
    candidate_root_str = str(candidate_root)
    if candidate_root_str in sys.path:
        return False
    sys.path.insert(0, candidate_root_str)
    importlib.invalidate_caches()
    return True


def _prefer_existing_package_path(candidate_root: Path) -> None:
    package = sys.modules.get(_SHARED_PACKAGE_NAME)
    if package is None or not hasattr(package, "__path__"):
        return
    package_root = str(candidate_root / _SHARED_PACKAGE_NAME)
    existing = [entry for entry in package.__path__ if entry != package_root]
    package.__path__[:] = [package_root, *existing]


def _evict_stale_package_modules(candidate_root: Path) -> None:
    preferred_package_root = (candidate_root / _SHARED_PACKAGE_NAME).resolve()
    stale_module_names: list[str] = []
    for module_name, module in list(sys.modules.items()):
        if module_name != _SHARED_PACKAGE_NAME and not module_name.startswith(f"{_SHARED_PACKAGE_NAME}."):
            continue
        module_file = getattr(module, "__file__", None)
        if not isinstance(module_file, str) or not module_file.strip():
            continue
        try:
            resolved_module_file = Path(module_file).resolve()
        except OSError:
            stale_module_names.append(module_name)
            continue
        if preferred_package_root not in resolved_module_file.parents and resolved_module_file != preferred_package_root:
            stale_module_names.append(module_name)
    for module_name in stale_module_names:
        sys.modules.pop(module_name, None)
    if stale_module_names:
        importlib.invalidate_caches()


def _load_shared_helper_module_from_path(helper_path: Path):
    spec = importlib.util.spec_from_file_location(
        f"{_SHARED_PACKAGE_NAME}_editable_consumer_launcher_{abs(hash(helper_path))}",
        helper_path,
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_sibling_shared_helper(added_paths: list[Path]):
    for helper_path in _candidate_shared_helper_module_paths():
        if not helper_path.exists():
            continue
        shared_src_root = helper_path.parent.parent
        inserted = _prepend_path(shared_src_root)
        _prefer_existing_package_path(shared_src_root)
        _evict_stale_package_modules(shared_src_root)
        if inserted:
            added_paths.append(shared_src_root)
        return _load_shared_helper_module_from_path(helper_path)
    return None


def _import_installed_shared_helper():
    if _module_spec(_SHARED_HELPER_MODULE_NAME) is None:
        return None
    return importlib.import_module(_SHARED_HELPER_MODULE_NAME)


def ensure_editable_dependency_paths() -> tuple[Path, ...]:
    repo_root = _repo_root()
    added_paths: list[Path] = []
    for explicit_root in _explicit_shared_src_roots_from_sys_path():
        _prepend_path(explicit_root)
        _prefer_existing_package_path(explicit_root)
        _evict_stale_package_modules(explicit_root)
        return (explicit_root,)
    helper_module = _load_sibling_shared_helper(added_paths)
    if helper_module is None:
        for candidate_root in _candidate_repo_site_packages_roots():
            if _prepend_path(candidate_root):
                added_paths.append(candidate_root)
        helper_module = _import_installed_shared_helper()
    if helper_module is None:
        return tuple(added_paths)

    ensure_paths = getattr(helper_module, "ensure_repo_editable_dependency_paths", None)
    if not callable(ensure_paths):
        return tuple(added_paths)

    delegated_added_paths = tuple(
        Path(entry)
        for entry in ensure_paths(
            repo_root=repo_root,
            shared_package_name=_SHARED_PACKAGE_NAME,
        )
    )
    if delegated_added_paths:
        return delegated_added_paths
    return tuple(added_paths)
