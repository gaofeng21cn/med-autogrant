# P4.B Direct Grant Entry Composition Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-12`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.B direct grant entry composition`
- Status: `landed / current truth`

## Goal

这条 current truth 不发明新的 repo-local executor，也不把 mature 前台或 hosted runtime 写成已完成。

它只解决一件事：

- 在已经 landed 的 `grant-progress`、`grant-cockpit`、`build-product-entry` 之上，
- 把 direct grant product entry 继续推进到一份可直接消费的组合式 product contract，
- 让 direct caller 一次拿到当前投影、direct entry envelope 与 `OPL` handoff envelope，
- 同时保持默认 concrete executor 为 `Codex CLI`，`Hermes-Agent` 只作为显式 OPL receipt/proof lane，`Med Auto Grant` 继续是 grant truth / route / export owner。

## Landed Facts

### 1. `grant-direct-entry` 已 landed

当前仓库已新增一条新的 CLI product surface：

- `grant-direct-entry`

它由 `src/med_autogrant/product_entry.py` 中的 `MedAutoGrantProductEntry.build_grant_direct_entry(...)` 提供，并通过 `src/med_autogrant/cli.py` 暴露给 caller。

### 2. 这条 surface 是 controller-owned 的 direct-entry composition，而不是新的 executor

当前 `grant-direct-entry` 只负责：

- 读取 `grant-progress`
- 读取 `grant-cockpit`
- 读取 `build-product-entry(entry_mode=direct)`
- 读取 `build-product-entry(entry_mode=opl-handoff)`
- 把它们收成一份 direct-entry composition contract

它不负责：

- 持有 runtime substrate owner
- 改写 author-side route owner
- 新增 service-safe domain executor
- 新增 hosted bundle command catalog

### 3. 这份 contract 现在已经 schema-backed、fail-closed

当前 `schemas/v1/schema-index.json` 已显式索引：

- `grant-direct-entry.schema.json`

同时 `grant-direct-entry` 在返回前会执行：

- `grant-direct-entry.schema.json` 校验
- direct / `opl-handoff` 子 envelope 的 identity 一致性校验
- direct / `opl-handoff` 子 envelope 的 `entry_mode` 一致性校验
- current / recommended route truth 一致性校验

因此如果有人改坏：

- 子 envelope 的 `entry_mode`
- top-level route card 与子 envelope route truth 的对应关系
- workspace overview / progress projection / alert 的结构

都会直接 fail-closed。

### 4. `grant-direct-entry` 当前输出什么

当前至少会稳定输出：

- `workspace_overview`
- `workspace_status`
- `workspace_alerts`
- `progress_projection`
- `current_stage_route`
- `recommended_executor_route`
- `direct_entry`
- `opl_handoff_entry`

其中：

- `direct_entry` 与 `opl_handoff_entry` 继续复用同一份已冻结的 `product_entry` contract
- `current_stage_route` / `recommended_executor_route` 继续复用同一份已冻结的 `executor_routing_contract` truth
- direct caller 现在可以先看 grant 当前主线与 route，再决定走 direct entry 还是 `OPL` handoff

### 5. 这条 surface 仍然不进入 service-safe domain command catalog

当前 `grant-direct-entry` 故意不是：

- `MedAutoGrantDomainEntry` 的 service-safe domain command
- hosted contract bundle 的 command catalog 项
- 新的 route executor

因此它继续不进入：

- `domain_entry_contract.supported_commands`
- hosted contract bundle 的 command catalog

也就是说，当前它明确：

- 不进入 `domain_entry_contract.supported_commands`
- 不进入 hosted contract bundle 的 command catalog

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_schema_registry.py tests/test_product_entry.py tests/test_cli_validate_workspace.py -q`
- `uv run pytest tests/test_domain_runtime.py tests/test_program_control_surfaces.py -q`

并验证：

- `grant-direct-entry` CLI dispatch 已 landed
- `grant-direct-entry.schema.json` 已进入 schema registry
- critique workspace 的 direct-entry composition shape 已冻结
- malformed child entry mode / route consistency 会被 fail-closed 拒绝
- core docs、phase map 与 current-program pointer 已同步到 `P4.B` 口径

## Honest Boundary

这条 current truth 只说明：

- `P4.B direct grant entry composition` 已 landed
- direct grant product entry 现在不再只有只读 projection，而是多了一份组合式 direct-entry contract

它不意味着：

- `P4 mature direct grant product entry` 整体已完成
- mature Web UI 已落地
- hosted runtime 已完成
- `OPL Gateway` 已在本仓落地
- pending authoring route 已拥有新的 landed executor
