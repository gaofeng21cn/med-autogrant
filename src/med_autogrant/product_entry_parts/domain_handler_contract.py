from __future__ import annotations

DOMAIN_HANDLER_EXPORT_KIND = "mag_product_domain_handler_export"
DOMAIN_HANDLER_DISPATCH_KIND = "mag_product_domain_handler_dispatch"
DOMAIN_HANDLER_ADAPTER_ID = "mag.opl_stage_led.domain_handler.v1"
DOMAIN_HANDLER_VERSION = 1

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
