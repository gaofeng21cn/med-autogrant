# Schema-Backed Product Entry And Routing Contract Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 只在仍被当前 owner surfaces 引用的 schema-backed product-entry / route contract subsection 内是 `support_current_truth`。当前 owner 是 MAG schema/source/product-entry manifest 与 `contracts/runtime-program/current-program.json`；OPL 只通过当前 stage-led framework path 消费 MAG descriptor/projection。下方旧 `Current Truth`、Upstream Hermes fast-cutover、`future OPL Gateway`、host-agent 或 federation wording 是 provenance，不是当前 owner line 或 compatibility target。

当前处置：

- Keep：schema-backed `product_entry` / `executor_routing_contract` validation 和 fail-closed drift guard。
- Superseded：`Upstream Hermes-Agent Fast Cutover`、`future OPL Gateway`、Hermes substrate runtime owner、gateway/federation caller language。
- Direct retirement posture：如果旧 module/interface/test 只为保留 superseded Gateway/Hermes wording 且没有 current caller，应把 caller 迁到 MAG schema/source/product-entry manifest，并删除或归档旧 surface；不新增 compatibility aliases。

Date: `2026-04-12`

## Activation Status

- Phase: `schema-backed product-entry support record`
- Active boundary: `MAG product-entry / executor-routing contract schema validation`
- Status: `support_current_truth_by_subsection`

## Goal

在已经 landed 的：

- `CLI-first + Codex-default execution plus explicit Hermes-Agent proof/provenance lane`
- `MedAutoGrantDomainEntry`
- lightweight `product entry` shell
- author-side executor routing contract

之上，把当前 direct / `OPL` handoff 会直接消费的关键 surface 继续收口成 schema-backed contract，并在生成时 fail-closed。

这条 current truth 解决的是：

- `product_entry` 与 `executor_routing_contract` 不再只是“代码里手工拼 dict + 文档约定”
- OPL stage-led framework / domain caller 可以通过当前 MAG descriptor/projection 和 repo-tracked schema 消费这层 contract
- landed route catalog、nullability 与 route truth 边界不会悄悄漂移

## Landed Facts

### 1. 四份核心 contract schema 已经进入 repo-tracked index

当前 `schemas/v1/schema-index.json` 已显式索引：

- `service-safe-domain-surface.schema.json`
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

- early-stage `product_entry.domain_payload.draft_id = null`
- 非空 route catalog

### 3. route contract surfaces 现在会 schema-backed fail-closed

当前 product-entry / route contract 在返回前会同时通过：

- `executor-routing-contract.schema.json`
- 冻结 truth 比对

这意味着：

- `current_stage_route`
- `recommended_executor_route`
- `author_side_route_catalog`

不仅要结构合法，还必须与当前冻结的 author-side route truth 完全一致。

如果有人误把：

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
  - `domain_entry_contract`
    - `supported_commands`
    - `command_contracts`
- `domain_payload`
- `stage_snapshot`
- `executor_routing_contract.author_side_route_catalog`

### 5. 这层 schema-backed closeout 没有改写 owner 边界

当前新增的只是 machine-readable contract 与 fail-closed validation：

- 没有新增 repo-local executor
- 没有把 pending route 提前写成 landed
- 没有把 `Hermes-Agent` 写回 author-side executor owner
- 没有把 `OPL` / gateway story 扩成新的平台叙事

也就是说，这条 support truth 仍然只服务：

- MAG 持有 author-side grant contract truth、schema/source、product-entry manifest 和 route truth
- OPL stage-led framework / domain caller 通过统一 envelope 消费 MAG descriptor/projection
- 旧 Hermes/Gateway 叙事只作 provenance，不恢复为 runtime owner 或 compatibility layer

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_schema_registry.py tests/test_product_entry.py tests/test_domain_runtime.py -q`
- `uv run pytest tests/test_domain_runtime.py -q`

并验证：

- schema registry 会追踪四份新 contract schema
- `product_entry` 遇到非法 `executor_routing_contract` 会 fail-closed
- product-entry / route contract 遇到非法 `executor_routing_contract` 会 fail-closed
- `author_side_route_catalog` 必须继续等于当前冻结 route matrix
- current `product_entry` / route handoff 仍保持 direct + `OPL` envelope truth 不漂移

## Honest Boundary

这条 current truth 只说明：

- 当前 `product_entry` / `executor_routing_contract` 已经升级成 schema-backed contract
- repo 现在会在生成时 fail-closed，阻止 contract drift

它不意味着：

- mature product UX 已完成
- critique executor 已 landed
- hosted runtime 已完成
- 旧 `OPL Gateway` landed wording 只保留为 provenance，不是 current owner line
- Hermes-backed runtime owner、Gateway/federation caller 或 compatibility bridge 不是当前目标
