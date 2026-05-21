# Hosted Caller Consumption Proof Current Truth

> 生命周期注记（`2026-05-21`）：这份 dated spec 已从 `docs/specs/` 退到 `docs/history/specs/`，只保留为 hosted caller 消费冻结 contract catalog 的历史 provenance。当前 runtime owner、OPL provider、App/workbench、production/default caller 和 grant readiness 结论回到核心五件套、active plan、contracts/schema/source 与 `contracts/runtime-program/current-program.json`；旧 `Current Truth` 标题、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance。

Date: `2026-04-12`

## Activation Status

- Phase: `P3 hosted caller / OPL consumption proof`
- Status: `history_provenance`

## Goal

这条 current truth 不新增 repo-local hosted helper，也不把 `OPL Gateway` 写成已落地。

它只解决一件事：

- 证明 external hosted caller / future `OPL` caller 现在已经可以直接消费 repo 冻结好的：
  - `domain_entry_contract`
  - `schema_contract`
  - `authoring_contract`

并且能在不读取仓内 Python helper、不发明新的 handoff semantics 的前提下，稳定调用已 landed 的 author-side route。

## Landed Facts

### 1. `product_entry` 与 hosted bundle 现在共享同一份 `domain_entry_contract`

当前：

- `build-product-entry.product_entry.return_surface_contract.domain_entry_contract`
- `build-hosted-contract-bundle.hosted_contract_bundle.domain_entry_contract`

都会导出同一份冻结 entry contract。

因此 external caller 不需要区分：

- direct grant entry 读取哪份 entry contract
- hosted / `OPL` handoff 读取哪份 entry contract

而是可以直接消费同一份 machine-readable contract truth。

### 2. `domain_entry_contract` 现在已经显式导出 command catalog

当前 `domain_entry_contract` 除了已有的：

- `entry_adapter`
- `service_safe_surface_kind`
- `product_entry_builder_command`
- `product_entry_kind`
- `supported_entry_modes`

之外，还会额外显式导出：

- `supported_commands`
- `command_contracts`

其中：

- `supported_commands` 冻结当前全部已支持的 domain entry command 名单
- `command_contracts` 为每个 command 显式列出：
  - `command`
  - `required_fields`
  - `optional_fields`

这意味着 future hosted caller 现在已经不需要靠 repo-local helper 猜参数形状。

### 3. external caller proof 现在已经 landed

当前 proof 会同时证明：

- external caller 可以从 `product_entry.return_surface_contract.domain_entry_contract` 读取 command catalog
- external caller 可以从 hosted bundle 读取 `domain_entry_contract`、`schema_contract`、`authoring_contract`
- external caller 可以只依赖 `command_contracts`，用 generic request builder 直接拼出 request
- external caller 可以沿已 landed route 继续完成：
  - `stage-route-report`
  - `build-artifact-bundle`
  - `build-final-package`
  - `build-hosted-contract-bundle`

也就是说，这条 proof 的真实含义是：

- external caller can consume the frozen contracts **without repo-local helper**

而不是：

- repo 里又新增了一层 hosted wrapper
- 仓内已经落地 actual hosted runtime

### 4. 这条 proof 没有改写 route owner 和 landed 边界

当前 proof 继续只允许消费已经冻结的 route truth：

- landed：
  - `critique`
  - `revision`
  - `artifact_bundle`
  - `final_package`
  - `hosted_contract_bundle`
- pending / handoff-required：
  - `direction_screening`
  - `question_refinement`
  - `argument_building`
  - `fit_alignment`
  - `outline`
  - `drafting`
  - `frozen`

因此这条 current truth 不是在：

- 把 pending route 提前写成 landed
- 为未冻结 route 发明新的 handoff semantics
- 把 `Hermes-Agent` substrate owner 偷换成 repo-local hosted executor

### 5. `P3` 现在可以诚实标成 completed

按 `OPL` 对齐后的 phase map，`P3` 的目标就是：

- hosted caller / `OPL` caller 直接消费已冻结 contract

当前这条 proof 已经落地，因此当前 phase map 应更新为：

- `P1` completed
- `P2` completed
- `P3` completed
- `P4` next

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_product_entry.py tests/test_hosted_contract_bundle.py tests/test_domain_entry.py -q`
- `uv run pytest tests/test_domain_runtime.py tests/test_program_control_surfaces.py -q`

并验证：

- `product_entry.return_surface_contract` 必须携带 `domain_entry_contract`
- hosted bundle 的 `domain_entry_contract` 必须携带 `supported_commands`
- hosted bundle 的 `domain_entry_contract` 必须携带 `command_contracts`
- external caller 可以只依赖 `command_contracts` 构造 request
- proof route 不需要 repo-local helper 即可完成已 landed export chain

## Honest Boundary

这条 current truth 只说明：

- `P3 hosted caller / OPL consumption proof` 已 landed
- external caller 现在可以直接消费冻结好的 contract catalog

它不意味着：

- actual hosted runtime 已完成
- 旧 `OPL Gateway` landed wording 只保留为 provenance，不是 current owner line
- mature direct grant product entry 已完成
- future `Human-in-the-loop` sibling 已开工
