# Hosted Contract Bundle Entry And Route Catalog Current Truth

Date: `2026-04-12`

## Activation Status

- Phase: `Upstream Hermes-Agent Fast Cutover`
- Active tranche: `Hosted contract bundle entry and route catalog`
- Status: `landed / current truth`

## Goal

在已经 landed 的：

- `CLI-first + real upstream Hermes-Agent runtime substrate`
- `MedAutoGrantDomainEntry`
- schema-backed `product_entry`
- schema-backed `executor_routing_contract`

之上，把 `build-hosted-contract-bundle` 继续收口成 future hosted / `OPL` caller 可直接消费的 contract bundle。

这条 current truth 解决的是：

- hosted contract bundle 不再只携带 runtime / state / operator pointer
- future caller 可以直接拿到稳定的 `domain_entry_contract`
- future caller 可以直接拿到 repo-tracked 的 `schema_contract`
- future caller 可以直接拿到完整 author-side route matrix 的 `authoring_contract`
- 整份 bundle 必须 schema-backed、truth-backed、fail-closed

## Landed Facts

### 1. hosted contract bundle 现在已经进入 repo-tracked schema registry

当前 `schemas/v1/schema-index.json` 已显式索引：

- `hosted-contract-bundle.schema.json`

它和下面这些已冻结 contract 共享同一套 repo-tracked schema registry：

- `service-safe-domain-surface.schema.json`
- `executor-routing-contract.schema.json`
- `product-entry.schema.json`
- `nsfc-workspace.schema.json`

因此当前 `build-hosted-contract-bundle.hosted_contract_bundle` 不再只是“导出一个文档”，而是正式 schema-backed contract。

### 2. 既有 runtime / state / operator surface 继续保留

当前 bundle 继续显式保留：

- `runtime_substrate_contract`
- `runtime_state_contract`
- `operator_contract`
- `execution_identity`
- `session_contract`
- `state_contract`
- `artifact_contract`
- `audit_contract`

这意味着：

- `grant_run_id / workspace_id / draft_id / program_id` 继续保持 canonical
- `stage-route-report` 继续是 checkpoint / verification 聚合面
- hosted bundle 仍然只是在导出托管友好的 handoff contract，而不是把 repo 写成 actual hosted runtime

### 3. hosted bundle 现在额外显式导出 entry / schema / route catalog

除了已有 surface 之外，当前 bundle 现在还必须显式导出：

- `domain_entry_contract`
  - `entry_adapter = MedAutoGrantDomainEntry`
  - `service_safe_surface_kind = service-safe-domain-entry-command`
  - `product_entry_builder_command = build-product-entry`
  - `product_entry_kind = med_auto_grant_product_entry`
  - `supported_entry_modes = [direct, opl-handoff]`
  - `supported_commands`
  - `command_contracts`
- `schema_contract`
  - `schema_version = v1`
  - `schema_index_path = schemas/v1/schema-index.json`
  - `aggregate_root_schema = nsfc-workspace.schema.json`
  - `contract_schema_files`
    - `service-safe-domain-surface.schema.json`
    - `executor-routing-contract.schema.json`
    - `product-entry.schema.json`
    - `hosted-contract-bundle.schema.json`
- `authoring_contract`
  - `route_contract_version = 1`
  - `route_catalog_kind = author_side_route_catalog`
  - `author_side_route_catalog` 继续列出完整 author-side route matrix

也就是说，future hosted / `OPL` caller 现在可以直接从同一个 hosted contract bundle 读取：

- 怎么调用已 landed 的 service-safe entry
- 应该读哪套 schema registry
- 当前 author-side route catalog 已经全部 landed
- 以及当前每个 landed command 需要哪些字段才能由 external caller 直接发起调用

### 4. authoring_contract 只打包已经冻结的 route truth

当前 `authoring_contract.author_side_route_catalog` 继续复用同一份已冻结 route matrix：

- landed：
  - `critique -> execute-critique-pass`
  - `revision -> execute-revision-pass`
  - `artifact_bundle -> build-artifact-bundle`
  - `final_package -> build-final-package`
  - `hosted_contract_bundle -> build-hosted-contract-bundle`
- pending / handoff-required：
  - `direction_screening`
  - `question_refinement`
  - `argument_building`
  - `fit_alignment`
  - `outline`
  - `drafting`
  - `frozen`

因此这条 truth 不是在：

- 发明新的 repo-local executor
- 改写 critique / drafting / frozen 的 owner
- 把 pending route 提前写成 landed

而只是在 hosted bundle 里，把已经冻结好的 route truth 原样带出去。

### 5. 整份 bundle 现在必须 fail-closed

当前 `HermesRuntimeSubstrate.build_hosted_contract_bundle(...)` 在写出前会同时执行：

- final package 输入边界校验
- `hosted-contract-bundle.schema.json` 校验
- 冻结 truth 比对

因此如果有人：

- 漏掉 `domain_entry_contract`
- 漏掉 `schema_contract`
- 漏掉 `authoring_contract`
- 改坏 `author_side_route_catalog`
- 把 bundle 写成和当前 repo-tracked contract 不一致

都会直接 fail-closed，而不是静默漂移。

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_schema_registry.py tests/test_hosted_contract_bundle.py tests/test_hermes_runtime_truth.py -q`

并验证：

- `schema-index.json` 会追踪 `hosted-contract-bundle.schema.json`
- `build-hosted-contract-bundle` 输出必须携带 `domain_entry_contract`
- `build-hosted-contract-bundle` 输出必须携带 `schema_contract`
- `build-hosted-contract-bundle` 输出必须携带 `authoring_contract`
- malformed hosted contract bundle 会被 `HermesRuntimeSubstrate` fail-closed 拒绝

## Honest Boundary

这条 current truth 只说明：

- hosted contract bundle 现在已经成为 schema-backed、truth-backed 的 contract catalog
- future hosted / `OPL` caller 可以直接消费 entry / schema / route truth
- current hosted caller 还可以直接读取 `supported_commands` / `command_contracts`，无需 repo-local helper
- author-side grant mainline 没有因为 hosted export 而漂移

它不意味着：

- actual hosted runtime 已完成
- `OPL Gateway` 已在本仓落地
- landed route 已经自动升级成 Hermes-native full agent loop
- pending authoring route 已经拥有新的执行器
