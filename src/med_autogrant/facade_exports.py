from __future__ import annotations

from types import ModuleType
from typing import Any


def re_export_public_names(module: ModuleType, namespace: dict[str, Any]) -> None:
    names = getattr(module, "__all__", None)
    if names is None:
        names = [name for name in vars(module) if not name.startswith("_")]
    for name in names:
        namespace[name] = getattr(module, name)
