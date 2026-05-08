from __future__ import annotations

import sys
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

from product_entry_cases.support import *  # noqa: F401,F403
from product_entry_cases.test_cli_dispatch import *  # noqa: F401,F403
from product_entry_cases.test_direct_entry import *  # noqa: F401,F403
from product_entry_cases.test_entry_envelope import *  # noqa: F401,F403
from product_entry_cases.test_failure_modes import *  # noqa: F401,F403
from product_entry_cases.test_progress_cockpit import *  # noqa: F401,F403
from product_entry_cases.test_dependency_structure import *  # noqa: F401,F403
from product_entry_cases.test_loop_and_readiness import *  # noqa: F401,F403
from product_entry_cases.test_manifest_and_status import *  # noqa: F401,F403
from product_entry_cases.test_manifest_readiness import *  # noqa: F401,F403
from product_entry_cases.test_runtime_registration import *  # noqa: F401,F403

__all__ = [name for name in globals() if not name.startswith("__")]
