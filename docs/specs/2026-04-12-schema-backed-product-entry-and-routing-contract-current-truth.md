# Schema-Backed Product Entry And Routing Contract Current Truth

Owner: `Med Auto Grant`
Purpose: `schema_backed_product_entry_routing_support_record`
State: `support_current_truth`
Machine boundary: 本文只说明 MAG schema/source 与 OPL-generated product-entry surfaces 的边界。机器真相归 source、schemas、contracts 和 `contracts/runtime-program/current-program.json`。
Last reviewed: `2026-07-10`

## Current Boundary

MAG 保留并维护：

- `schemas/v1/service-safe-domain-surface.schema.json`
- `schemas/v1/executor-routing-contract.schema.json`
- `schemas/v1/product-entry.schema.json`
- `MedAutoGrantDomainEntry`、service-safe command catalog 与 grant route truth
- grant truth、quality/fundability/export/package authority 与 owner closeout refs

OPL 生成并托管 product-entry manifest、status、user-loop、progress、cockpit、direct-entry 与 session surfaces。MAG source 中出现的 `/product_entry_manifest/*` 只是在 OPL-generated manifest 内定位 authority/descriptor refs 的 JSON pointer，不表示 MAG 维护本地 manifest schema、builder 或 public product CLI。

## Retired Surfaces

以下 repo-local surfaces 已退役，不再作为 current owner 或 compatibility target：

- `product-entry-manifest.schema.json`
- `product-status.schema.json`
- local product/status/preflight/start/progress/cockpit/direct-entry text renderers
- local `build-product-entry` wrapper
- Upstream Hermes fast-cutover、future OPL Gateway 与 gateway/federation caller wording

旧 caller 应迁到 OPL generated surfaces 或 MAG service-safe/domain-handler authority target；不新增 alias、facade、re-export 或兼容测试。

## Fail-Closed Contract

`product-entry.schema.json` 继续持有：

- domain agent entry spec
- service-safe supported commands 与 command contracts
- workspace locator、runtime session envelope、domain payload 与 stage snapshot
- author-side executor routing contract

MAG 的 workspace/authoring validators 复用 `opl_harness_shared.schema_validation.SchemaSubsetValidator`。OPL hosted contract bundle 复用 `product-entry.schema.json` 中的 domain-entry、operator 与 routing definitions；OPL-owned session/progress/artifact/runtime projection 不再复制进 MAG schema。

## Verification

- `./scripts/run-pytest-clean.sh tests/test_schema_registry.py tests/test_domain_entry.py tests/test_hosted_contract_bundle.py -q`
- `./scripts/run-python-clean.sh scripts/check_descriptor_contracts.py`
- `<opl-repo>/bin/opl agents conformance --agent "mag=$PWD" --json`
- `./scripts/verify.sh full`

这些检查只证明 schema、descriptor、route contract 与 structural conformance；不证明 grant-ready、submission-ready、production-ready 或真实 OPL-hosted stage consumption。
