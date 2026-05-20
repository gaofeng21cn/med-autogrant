from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.product_entry_parts.primitives import (
    _require_mapping,
)
from med_autogrant.product_entry_parts.runtime_contracts import PRODUCT_STATUS_SCHEMA_FILE
from med_autogrant.product_entry_parts.loop_contracts import _validate_product_status_contract
from med_autogrant.product_entry_parts.manifest_builder import ProductEntryManifestBuilderMixin

from opl_harness_shared.product_entry_companions import (
    build_family_product_entry_surface_from_manifest as _build_shared_family_product_entry_surface_from_manifest,
)



class ProductEntryManifestMixin(ProductEntryManifestBuilderMixin):

    def build_skill_catalog(
        self,
        *,
        input_path: str | Path,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        manifest_payload = self.build_product_entry_manifest(
            input_path=input_path,
            funding_call=funding_call,
        )
        return {
            "ok": True,
            "command": "skill-catalog",
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
            "skill_catalog": dict(
                _require_mapping(
                    manifest_payload["product_entry_manifest"],
                    "skill_catalog",
                    context="product_entry_manifest",
                )
            ),
        }

    def build_product_status(
        self,
        *,
        input_path: str | Path,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        manifest_payload = self.build_product_entry_manifest(
            input_path=input_path,
            funding_call=funding_call,
        )
        manifest = _require_mapping(
            manifest_payload,
            "product_entry_manifest",
            context="product_status",
        )
        product_status = _build_shared_family_product_entry_surface_from_manifest(
            recommended_action="inspect_or_prepare_grant_loop",
            product_entry_manifest=dict(manifest),
            shell_aliases={
                "status": "product_status",
                "grant_progress": "grant_progress",
                "grant_cockpit": "grant_cockpit",
                "grant_direct_entry": "grant_direct_entry",
                "grant_user_loop": "grant_user_loop",
            },
            schema_ref=f"contracts/schemas/v1/{PRODUCT_STATUS_SCHEMA_FILE}",
            notes=[
                "This status surface is an OPL generated/hosted caller read model over MAG domain handler refs.",
                "It does not claim that mature Web UI or hosted runtime is already landed.",
            ],
            extra_payload={
                "grant_authoring_readiness": dict(_require_mapping(
                    manifest,
                    "grant_authoring_readiness",
                    context="product_status.product_entry_manifest",
                )),
                "session_continuity": dict(_require_mapping(
                    manifest,
                    "session_continuity",
                    context="product_status.product_entry_manifest",
                )),
                "progress_projection": dict(_require_mapping(
                    manifest,
                    "progress_projection",
                    context="product_status.product_entry_manifest",
                )),
                "artifact_inventory": dict(_require_mapping(
                    manifest,
                    "artifact_inventory",
                    context="product_status.product_entry_manifest",
                )),
                "runtime_control": dict(_require_mapping(
                    manifest,
                    "runtime_control",
                    context="product_status.product_entry_manifest",
                )),
            },
        )
        product_status["surface_kind"] = "product_status"
        product_status["caller_owner_contract"] = {
            "active_caller_owner": "med-autogrant",
            "active_caller_surface": "mag_product_status_handler_until_opl_caller_evidence",
            "target_caller_owner": "one-person-lab",
            "target_caller_surface": "opl_generated_or_hosted_status_read_model",
            "domain_handler_target": "med-autogrant",
            "domain_handler_owner": "med-autogrant",
            "mag_role": "status_handler_target_and_grant_authority_refs_only",
            "claims_fully_cleaned": False,
            "mag_handler_boundary_ready": True,
            "external_opl_generated_or_hosted_caller_evidence_required": True,
        }
        product_status["generated_hosted_default_caller_proof"] = dict(
            _require_mapping(
                _require_mapping(
                    manifest,
                    "mag_consumer_thinning_contract",
                    context="product_status.product_entry_manifest",
                ),
                "generated_hosted_default_caller_proof",
                context="product_status.mag_consumer_thinning_contract",
            )
        )
        product_status["product_entry_surfaces"] = product_status.pop("entry_surfaces")

        payload = {
            "ok": True,
            "command": "product-status",
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
            "product_status": product_status,
        }
        _validate_product_status_contract(
            payload,
            grant_run_id=manifest_payload["grant_run_id"],
            workspace_id=manifest_payload["workspace_id"],
            lifecycle_stage=manifest_payload["lifecycle_stage"],
        )
        return payload

    def build_product_entry_start(
        self,
        *,
        input_path: str | Path,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        manifest_payload = self.build_product_entry_manifest(
            input_path=input_path,
            funding_call=funding_call,
        )
        manifest = _require_mapping(
            manifest_payload,
            "product_entry_manifest",
            context="product_start",
        )
        return {
            "ok": True,
            "command": "product-start",
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
            "product_entry_start": dict(
                _require_mapping(
                    manifest,
                    "product_entry_start",
                    context="product_start.product_entry_manifest",
                )
            ),
        }
