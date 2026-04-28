from __future__ import annotations

from med_autogrant.product_entry_parts import shared as _product_entry_shared
from med_autogrant.product_entry_parts.entry import MedAutoGrantProductEntry
from med_autogrant.facade_exports import re_export_public_names


re_export_public_names(_product_entry_shared, globals())

__all__ = ["MedAutoGrantProductEntry", *getattr(_product_entry_shared, "__all__", ())]
