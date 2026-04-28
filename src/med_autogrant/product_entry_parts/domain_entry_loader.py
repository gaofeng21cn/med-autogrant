from __future__ import annotations

from importlib import import_module
from typing import Any


def build_default_domain_entry() -> Any:
    domain_entry_module = import_module("med_autogrant.domain_entry")
    return domain_entry_module.MedAutoGrantDomainEntry()
