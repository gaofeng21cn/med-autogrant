from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import unittest

from med_autogrant.product_entry import MedAutoGrantProductEntry

from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


@dataclass(frozen=True)
class ManifestStatusContext:
    payload: dict[str, Any]
    manifest: dict[str, Any]


def build_manifest_status_context() -> ManifestStatusContext:
    payload = MedAutoGrantProductEntry().build_product_entry_manifest(
        input_path=str(CRITIQUE_EXAMPLE_PATH),
    )

    return ManifestStatusContext(
        payload=payload,
        manifest=payload["product_entry_manifest"],
    )


def run_manifest_status_scenarios(
    test_case: unittest.TestCase,
    scenario_assertions: list[tuple[str, Any]],
) -> None:
    context = build_manifest_status_context()
    for scenario_name, assert_scenario in scenario_assertions:
        with test_case.subTest(scenario=scenario_name):
            assert_scenario(test_case, context)
