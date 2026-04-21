from __future__ import annotations

from . import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from opl_harness_shared import family_orchestration as _family_orchestration  # noqa: F401

__all__ = ["__version__"]

__version__ = "0.1.0"
