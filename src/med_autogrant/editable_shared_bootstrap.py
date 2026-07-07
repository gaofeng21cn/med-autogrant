from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path


_SHARED_HELPER_MODULE_NAME = "opl_harness_shared.editable_consumer_launcher"
_SHARED_PACKAGE_NAME = "opl_harness_shared"


def _module_spec(module_name: str):
    try:
        return importlib.util.find_spec(module_name)
    except ModuleNotFoundError:
        return None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _import_installed_shared_helper():
    if _module_spec(_SHARED_HELPER_MODULE_NAME) is None:
        return None
    return importlib.import_module(_SHARED_HELPER_MODULE_NAME)


def ensure_editable_dependency_paths() -> tuple[Path, ...]:
    helper_module = _import_installed_shared_helper()
    if helper_module is None:
        return ()

    ensure_paths = getattr(helper_module, "ensure_repo_editable_dependency_paths", None)
    if not callable(ensure_paths):
        return ()

    return tuple(
        Path(entry)
        for entry in ensure_paths(
            repo_root=_repo_root(),
            shared_package_name=_SHARED_PACKAGE_NAME,
        )
    )
