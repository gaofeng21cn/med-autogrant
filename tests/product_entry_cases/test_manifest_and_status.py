from __future__ import annotations

import unittest

from product_entry_cases.test_manifest_and_status_cases.authority_handoff import (
    assert_authority_handoff,
)
from product_entry_cases.test_manifest_and_status_cases.context import (
    run_manifest_status_scenarios,
)
from product_entry_cases.test_manifest_and_status_cases.manifest_shell import (
    assert_manifest_shell,
)
from product_entry_cases.test_manifest_and_status_cases.readiness import (
    assert_readiness_surfaces,
)
from product_entry_cases.test_manifest_and_status_cases.runtime_control import (
    assert_runtime_control,
)
from product_entry_cases.test_manifest_and_status_cases.standard_agent import (
    assert_standard_agent_contract,
)
from product_entry_cases.test_manifest_and_status_cases.start_surfaces import (
    assert_start_surfaces,
)
from product_entry_cases.test_manifest_and_status_cases.status_projection import (
    assert_status_projection,
)


class ProductEntryManifestStatusTest(unittest.TestCase):
    def test_product_entry_manifest_projects_current_grant_shell_and_shared_handoff(self) -> None:
        run_manifest_status_scenarios(
            self,
            [
                ("manifest shell", assert_manifest_shell),
                ("runtime control", assert_runtime_control),
                ("authority handoff", assert_authority_handoff),
                ("standard domain agent contract", assert_standard_agent_contract),
                ("status projection", assert_status_projection),
                ("start surfaces", assert_start_surfaces),
                ("readiness surfaces", assert_readiness_surfaces),
            ],
        )
