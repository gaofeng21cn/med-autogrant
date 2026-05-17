from __future__ import annotations

from typing import Any

__all__ = ["MedAutoGrantProductEntry"]


def __getattr__(name: str) -> Any:
    if name == "MedAutoGrantProductEntry":
        from med_autogrant.product_entry_parts.entry import MedAutoGrantProductEntry

        return MedAutoGrantProductEntry
    raise AttributeError(name)
