from __future__ import annotations

from med_autogrant.product_entry_parts.shared import *  # noqa: F401,F403
from med_autogrant.product_entry_parts.manifest_builder import ProductEntryManifestBuilderMixin



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

    def build_product_frontdesk(
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
            context="product_frontdesk",
        )
        product_frontdesk = _build_shared_family_product_frontdesk_from_manifest(
            recommended_action="inspect_or_prepare_grant_loop",
            product_entry_manifest=dict(manifest),
            shell_aliases={
                "frontdesk": "product_frontdesk",
                "grant_progress": "grant_progress",
                "grant_cockpit": "grant_cockpit",
                "grant_direct_entry": "grant_direct_entry",
                "grant_user_loop": "grant_user_loop",
            },
            schema_ref=f"contracts/schemas/v1/{PRODUCT_FRONTDESK_SCHEMA_FILE}",
            notes=[
                "This frontdesk surface is a controller-owned direct grant front door over the landed product-entry shell.",
                "It does not claim that mature Web UI or hosted runtime is already landed.",
            ],
            extra_payload={
                "grant_authoring_readiness": dict(_require_mapping(
                    manifest,
                    "grant_authoring_readiness",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "session_continuity": dict(_require_mapping(
                    manifest,
                    "session_continuity",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "progress_projection": dict(_require_mapping(
                    manifest,
                    "progress_projection",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "artifact_inventory": dict(_require_mapping(
                    manifest,
                    "artifact_inventory",
                    context="product_frontdesk.product_entry_manifest",
                )),
                "runtime_control": dict(_require_mapping(
                    manifest,
                    "runtime_control",
                    context="product_frontdesk.product_entry_manifest",
                )),
            },
        )

        payload = {
            "ok": True,
            "command": "product-frontdesk",
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
            "product_frontdesk": product_frontdesk,
        }
        _validate_product_frontdesk_contract(
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
