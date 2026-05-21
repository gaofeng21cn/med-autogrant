from __future__ import annotations

SIDECAR_EXPORT_KIND = "mag_product_sidecar_export"
SIDECAR_DISPATCH_KIND = "mag_product_sidecar_dispatch"
SIDECAR_ADAPTER_ID = "mag.opl_stage_led.product_sidecar.v1"
SIDECAR_VERSION = 1

ALLOWED_ACTIONS = {
    "domain-memory/propose",
    "domain-memory/decide",
    "stage-attempt/closeout",
    "lifecycle/receipt",
    "closeout/codex-stage-receipts",
    "closeout/operator-readiness",
    "closeout/physical-morphology-guard",
    "closeout/executor-first-bundle",
}
