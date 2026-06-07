from __future__ import annotations

import unittest

from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.domain_runtime_parts.shared import AUTHOR_SIDE_ROUTE_IDS
from product_entry_cases.support import (
    _expected_route,
    CRITIQUE_EXAMPLE_PATH,
    DRAFTING_EXAMPLE_PATH,
    FROZEN_EXAMPLE_PATH,
    REVISION_EXAMPLE_PATH,
)


class ProductEntryEnvelopeTest(unittest.TestCase):
    def test_product_entry_builds_shared_envelope_for_direct_and_opl_handoff(self) -> None:
        from med_autogrant.domain_entry_contract import build_domain_entry_contract
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()

        direct_payload = entry.build(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        handoff_payload = entry.build(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="opl-handoff",
            task_intent="tighten-grant-mainline",
        )

        direct_envelope = direct_payload["product_entry"]
        handoff_envelope = handoff_payload["product_entry"]

        self.assertEqual(direct_payload["command"], "build-product-entry")
        self.assertEqual(direct_payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(direct_payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(direct_payload["draft_id"], "draft-v1")
        self.assertEqual(direct_payload["lifecycle_stage"], "critique")

        self.assertEqual(direct_envelope["entry_kind"], "med_auto_grant_product_entry")
        self.assertEqual(direct_envelope["entry_version"], 1)
        self.assertEqual(direct_envelope["target_domain_id"], "med-autogrant")
        self.assertEqual(direct_envelope["task_intent"], "tighten-grant-mainline")
        self.assertEqual(direct_envelope["entry_mode"], "direct")
        self.assertEqual(handoff_envelope["entry_mode"], "opl-handoff")

        self.assertEqual(direct_envelope["workspace_locator"], handoff_envelope["workspace_locator"])
        self.assertEqual(direct_envelope["runtime_session_contract"], handoff_envelope["runtime_session_contract"])
        self.assertEqual(direct_envelope["return_surface_contract"], handoff_envelope["return_surface_contract"])
        self.assertEqual(direct_envelope["domain_payload"], handoff_envelope["domain_payload"])
        self.assertEqual(direct_envelope["stage_snapshot"], handoff_envelope["stage_snapshot"])

        self.assertEqual(
            direct_envelope["workspace_locator"],
            {
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
            },
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["session_handle_kind"],
            "grant_run_id",
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["grant_run_id"],
            "grant-run-nsfc-demo-001-baseline-001",
        )
        self.assertEqual(direct_envelope["runtime_session_contract"]["session_owner"], "one-person-lab")
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["generated_session_surface_ref"],
            "opl://generated-surfaces/mag/product-entry-session",
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["generated_resume_surface_ref"],
            "opl://generated-surfaces/mag/product-entry-session#resume",
        )
        self.assertEqual(
            direct_envelope["runtime_session_contract"]["domain_authority_surface_ref"],
            "/product_entry_manifest/owner_receipt_contract",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["entry_adapter"],
            "MedAutoGrantDomainEntry",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["domain_entry_contract"],
            build_domain_entry_contract(),
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["checkpoint_aggregation_surface"],
            "stage-route-report",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["session_continuity"]["surface_kind"],
            "session_continuity",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["progress_projection"]["surface_kind"],
            "progress_projection",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["artifact_inventory"]["surface_kind"],
            "artifact_inventory",
        )
        self.assertEqual(
            direct_envelope["return_surface_contract"]["runtime_control"]["surface_kind"],
            "runtime_control",
        )
        self.assertEqual(
            direct_envelope["domain_payload"],
            {
                "workspace_id": "nsfc-demo-001",
                "draft_id": "draft-v1",
                "funding_call": "nsfc-2026-general",
            },
        )
        self.assertEqual(
            direct_envelope["stage_snapshot"],
            {
                "lifecycle_stage": "critique",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "revision",
            },
        )
        self.assertEqual(
            direct_envelope["executor_routing_contract"],
            {
                "contract_version": 1,
                "current_stage_route": _expected_route("critique", source_stage="critique"),
                "recommended_executor_route": _expected_route("revision", source_stage="critique"),
                "author_side_route_catalog": [
                    _expected_route(route_id, source_stage=route_id)
                    for route_id in AUTHOR_SIDE_ROUTE_IDS
                ],
            },
        )

    def test_product_product_entry_surfaces_revision_completed_reroute_to_critique_handoff(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build(
            input_path=str(REVISION_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )

        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(
            payload["product_entry"]["stage_snapshot"],
            {
                "lifecycle_stage": "revision",
                "checkpoint_status": "forward_progress",
                "recommended_next_stage": "critique",
            },
        )
        self.assertEqual(
            payload["product_entry"]["executor_routing_contract"],
            {
                "contract_version": 1,
                "current_stage_route": _expected_route("revision", source_stage="revision"),
                "recommended_executor_route": _expected_route("critique", source_stage="revision"),
                "author_side_route_catalog": [
                    _expected_route(route_id, source_stage=route_id)
                    for route_id in AUTHOR_SIDE_ROUTE_IDS
                ],
            },
        )

    def test_product_entry_contextualizes_drafting_and_frozen_pending_handoff_matrix(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        drafting_payload = MedAutoGrantProductEntry().build(
            input_path=str(DRAFTING_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        drafting_contract = drafting_payload["product_entry"]["executor_routing_contract"]
        self.assertEqual(
            drafting_contract["current_stage_route"],
            _expected_route("drafting", source_stage="drafting"),
        )
        self.assertEqual(
            drafting_contract["recommended_executor_route"],
            _expected_route("critique", source_stage="drafting"),
        )
        self.assertNotIn("handoff_requirements", drafting_contract["recommended_executor_route"])
        self.assertEqual(
            [
                route["route_id"]
                for route in drafting_contract["author_side_route_catalog"]
            ],
            list(AUTHOR_SIDE_ROUTE_IDS),
        )

        frozen_payload = MedAutoGrantProductEntry().build(
            input_path=str(FROZEN_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
        )
        self.assertEqual(
            frozen_payload["product_entry"]["executor_routing_contract"]["current_stage_route"],
            _expected_route("frozen", source_stage="frozen"),
        )
