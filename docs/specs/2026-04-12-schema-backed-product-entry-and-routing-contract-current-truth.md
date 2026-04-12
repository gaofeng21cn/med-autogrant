# Schema-Backed Product Entry And Routing Contract Current Truth

Date: `2026-04-12`

## Activation Status

- Phase: `Upstream Hermes-Agent Fast Cutover`
- Active tranche: `Schema-backed product entry / routing contract`
- Status: `landed / current truth`

## Goal

在已经 landed 的：

- `CLI-first + real upstream Hermes-Agent runtime substrate`
- `MedAutoGrantDomainEntry`
- lightweight `product entry` shell
- author-side executor routing contract

之上，把当前 direct / `OPL` handoff 会直接消费的关键 surface 继续收口成 schema-backed contract，并在生成时 fail-closed。

这条 current truth 解决的是：

- `product_entry`、`executor_routing_contract`、`pending_handoff_requirements` 不再只是“代码里手工拼 dict + 文档约定”
- future `OPL Gateway` / domain caller 可以直接消费 repo-tracked schema
- pending route、route catalog、nullability 与 landed/pending 边界不会悄悄漂移

## Landed Facts

### 1. 四份核心 contract schema 已经进入 repo-tracked index

当前 `schemas/v1/schema-index.json` 已显式索引：

- `service-safe-domain-surface.schema.json`
- `pending-handoff-requirements.schema.json`
- `executor-routing-contract.schema.json`
- `product-entry.schema.json`

这四份 schema 现在和 `nsfc-workspace.schema.json` 一起留在同一套 repo-tracked schema registry 里。

### 2. schema subset validator 已经扩到当前 contract 真正需要的边界

`workspace.py` 内部的 `_SchemaSubsetValidator` 当前已补齐：

- `type: ["object", "null"]`
- `type: ["string", "null"]`
- `null`
- `minItems`

因此当前 contract 已经可以诚实表达：

- pending route 的 `execution_surface = null`
- early-stage `product_entry.domain_payload.draft_id = null`
- 非空 route catalog / required_domain_surfaces / required_gate_fields

### 3. `run-local` 的 routing surface 现在会 schema-backed fail-closed

当前 `run-local.stage_action_envelope.executor_routing_contract` 在返回前会同时通过：

- `executor-routing-contract.schema.json`
- 冻结 truth 比对

这意味着：

- `current_stage_route`
- `recommended_executor_route`

不仅要结构合法，还必须与当前冻结的 author-side route truth 完全一致。

如果有人误把：

- `pending` route 写成 `landed`
- critique handoff surface 写错
- `current_stage_route` / `recommended_executor_route` 对调

都会直接 fail-closed。

### 4. `build-product-entry` 现在也会 schema-backed fail-closed

当前 `build-product-entry.product_entry` 在写出前会通过：

- `product-entry.schema.json`
- 内嵌 `executor_routing_contract` 的同一套 schema + truth 校验

因此下面这些字段现在都不只是“最好如此”，而是正式合同：

- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`
- `domain_payload`
- `stage_snapshot`
- `executor_routing_contract.author_side_route_catalog`

### 5. 这层 schema-backed closeout 没有改写 owner 边界

当前新增的只是 machine-readable contract 与 fail-closed validation：

- 没有新增 repo-local executor
- 没有把 pending route 提前写成 landed
- 没有把 `Hermes-Agent` 写回 author-side executor owner
- 没有把 `OPL` / gateway story 扩成新的平台叙事

也就是说，这条 truth 仍然只服务：

- 上游 Hermes substrate 持有 runtime substrate owner
- `Med Auto Grant` 持有 author-side grant contract truth
- future `OPL Gateway` / domain caller 通过统一 envelope 直接协作

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_schema_registry.py tests/test_product_entry.py tests/test_hermes_runtime.py -q`
- `uv run pytest tests/test_hermes_runtime_truth.py -q`

并验证：

- schema registry 会追踪四份新 contract schema
- `product_entry` 遇到非法 `executor_routing_contract` 会 fail-closed
- `run-local` 遇到非法 `executor_routing_contract` 会 fail-closed
- `author_side_route_catalog` 必须继续等于当前冻结 route matrix
- current `product_entry` / route handoff 仍保持 direct + `OPL` envelope truth 不漂移

## Honest Boundary

这条 current truth 只说明：

- 当前 `product_entry` / `executor_routing_contract` / `pending_handoff_requirements` 已经升级成 schema-backed contract
- repo 现在会在生成时 fail-closed，阻止 contract drift

它不意味着：

- mature product UX 已完成
- critique executor 已 landed
- hosted runtime 已完成
- `OPL Gateway` 全链路已在本仓落地
