from __future__ import annotations

from collections.abc import Callable
from typing import Any

ExecutorRunner = Callable[..., dict[str, Any]]

__all__ = ["ExecutorRunner"]
