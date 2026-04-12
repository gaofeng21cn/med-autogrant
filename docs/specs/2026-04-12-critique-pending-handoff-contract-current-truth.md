# Critique Pending Handoff Contract Current Truth

Date: `2026-04-12`

## Activation Status

- Phase: `Upstream Hermes-Agent Fast Cutover`
- Active tranche: `Critique pending handoff contract`
- Status: `landed / current truth`

## Goal

在不把 `critique` route 误写成“已 landed executor”的前提下，把当前和 `Hermes-Agent` 直接协作所需的最小 handoff 要求冻结成 machine-readable contract。

这条 truth 解决的是：

- `critique` 继续是 `pending / handoff-required`
- 但 future host / gateway / Hermes-side collaborator 不再只看到一个空的 pending 标记
- 而是能明确知道当前应该读取哪些 domain surfaces，才能对 grant 草稿做导师式 critique

## Landed Facts

### 1. critique pending route 现在自带 `handoff_requirements`

当前下面两个 surface 里的 `critique` route 都会显式带上：

- `run-local` 的 `stage_action_envelope.executor_routing_contract.current_stage_route`
- `build-product-entry` 的 `product_entry.executor_routing_contract.current_stage_route`

如果某个 workspace 的下一步又回到：

- `recommended_executor_route.route_id = critique`

那同一份 `handoff_requirements` 也会出现在：

- `recommended_executor_route`

### 2. 当前冻结的 critique handoff 合同字段

当前 `handoff_requirements` 至少包括：

- `contract_kind = critique-pending-handoff`
- `workspace_surface_kind = nsfc_workspace`
- `required_domain_surfaces`
- `required_identity_fields`

其中 `required_domain_surfaces` 当前固定为：

- `summarize-workspace`
- `critique-summary`
- `stage-route-report`

并且都统一声明为：

- `surface_kind = service-safe-domain-entry-command`
- `entry_adapter = MedAutoGrantDomainEntry`

### 3. 这份 handoff contract 明确服务“直接协作”，不是“本地 executor 已替换”

这条 contract 的意思是：

- future Hermes-side collaborator 如果要做 critique，不应绕开 grant domain truth
- 应先通过现有 service-safe domain surfaces 读取：
  - workspace summary
  - critique summary
  - route / checkpoint snapshot
- 并继续保留：
  - `grant_run_id`
  - `workspace_id`
  - `draft_id`

它不是在宣称：

- 仓库里已经有 `execute-critique-pass`
- critique 已经变成 Hermes-native mutation executor
- repo-local helper 已经完成新的 critique runtime owner 接管

## What Did Not Change

- `critique` route 仍然是 `pending`
- `handoff_contract_kind` 仍然是 `handoff-required`
- 已 landed 的 route 仍然只有：
  - `revision`
  - `artifact_bundle`
  - `final_package`
  - `hosted_contract_bundle`
- `Med Auto Grant` 继续持有 author-side critique / revision / export truth
- `Hermes-Agent` 继续只持有 runtime substrate / orchestration owner

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_hermes_runtime.py tests/test_product_entry.py tests/test_hermes_runtime_truth.py -q`

并验证：

- `critique` current-stage route 会带 `handoff_requirements`
- `product entry` route catalog 里的 `critique` 也会带同一份 `handoff_requirements`
- handoff 要求会固定列出：
  - `summarize-workspace`
  - `critique-summary`
  - `stage-route-report`

## Honest Boundary

这条 current truth 只说明：

- critique pending route 现在有 machine-readable 的 handoff requirements
- future host / gateway / Hermes collaborator 已经能更诚实地和当前 grant domain 直接协作

它不意味着：

- critique executor 已经 landed
- critique mutation surface 已经新增
- 更成熟的 grant-facing UX 已完成
