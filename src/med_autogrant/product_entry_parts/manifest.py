from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.product_entry_parts.loop_contracts import _validate_product_status_contract
from med_autogrant.product_entry_parts.manifest_builder import ProductEntryManifestBuilderMixin
from med_autogrant.product_entry_parts.primitives import _require_mapping


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
        manifest = _require_mapping(
            manifest_payload, "product_entry_manifest", context="skill_catalog"
        )
        return _identity_payload(
            manifest_payload,
            command="skill-catalog",
            field="skill_catalog",
            value=dict(_require_mapping(manifest, "skill_catalog", context="product_entry_manifest")),
        )

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
            manifest_payload, "product_entry_manifest", context="product_status"
        )
        shell = _require_mapping(manifest, "product_entry_shell", context="product_entry_manifest")
        status_surface = _require_mapping(
            manifest, "product_entry_status", context="product_entry_manifest"
        )
        product_status = {
            "surface_kind": "product_status",
            "target_domain_id": "med-autogrant",
            "product_entry_status": dict(status_surface),
            "summary": {
                "product_entry_command": shell["product_status"]["command"],
                "recommended_command": shell["grant_user_loop"]["command"],
                "operator_loop_command": shell["grant_user_loop"]["command"],
            },
            "product_entry_surfaces": dict(shell),
            "progress_projection": dict(
                _require_mapping(manifest, "progress_projection", context="product_entry_manifest")
            ),
            "stage_descriptor_ref": "contracts/stage_control_plane.json",
            "owner_receipt_contract": dict(
                _require_mapping(manifest, "owner_receipt_contract", context="product_entry_manifest")
            ),
            "authority_boundary": dict(
                _require_mapping(manifest, "authority_boundary", context="product_entry_manifest")
            ),
            "notes": [
                "This is a thin direct MAG status handler target.",
                "OPL owns the generated/hosted status, user-loop, and workbench shell.",
            ],
        }
        payload = _identity_payload(
            manifest_payload,
            command="product-status",
            field="product_status",
            value=product_status,
        )
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
            manifest_payload, "product_entry_manifest", context="product_start"
        )
        return _identity_payload(
            manifest_payload,
            command="product-start",
            field="product_entry_start",
            value=dict(
                _require_mapping(manifest, "product_entry_start", context="product_entry_manifest")
            ),
        )


def _identity_payload(
    manifest_payload: dict[str, Any],
    *,
    command: str,
    field: str,
    value: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ok": True,
        "command": command,
        "grant_run_id": manifest_payload["grant_run_id"],
        "workspace_id": manifest_payload["workspace_id"],
        "draft_id": manifest_payload["draft_id"],
        "lifecycle_stage": manifest_payload["lifecycle_stage"],
        "input_path": manifest_payload["input_path"],
        field: value,
    }
