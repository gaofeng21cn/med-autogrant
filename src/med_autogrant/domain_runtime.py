from __future__ import annotations

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap
from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime


_editable_shared_bootstrap.ensure_editable_dependency_paths()

__all__ = ["MagDomainRuntime"]
