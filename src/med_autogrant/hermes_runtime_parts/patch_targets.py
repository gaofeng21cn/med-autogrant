from __future__ import annotations

import sys
from typing import Any


def resolve_runtime_patch_target(name: str, default: Any) -> Any:
    runtime_module = sys.modules.get("med_autogrant.hermes_runtime")
    if runtime_module is not None:
        return getattr(runtime_module, name, default)
    return default
