# P4.C Mainline Status And Grant User Loop Current Truth

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-12`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.C mainline status and grant user loop`
- Status: `landed / current truth`

## Goal

这条 current truth 不发明新的 repo-local executor，也不把成熟 Web UI、hosted runtime 或 `OPL Gateway` 写成已完成。

它只解决两件事：

- 把 repo 主线当前到底在哪个 phase、离理想形态还有哪些缺口，收成可直接消费的 `mainline-status / mainline-phase` controller surface
- 在 `grant-direct-entry` 之上，再把当前 direct grant user loop 与推荐 next action 收成一份 controller-owned 的 `grant-user-loop`

## Landed Facts

### 1. `mainline-status` 与 `mainline-phase` 已 landed

当前仓库已新增两条 repo 级 CLI controller surface：

- `mainline-status`
- `mainline-phase`

它们会直接读取 repo-tracked `contracts/runtime-program/current-program.json`，并投影：

- 理想目标 owner split
- phase ladder
- 当前 active phase / tranche
- completed tranches
- remaining gaps
- explicitly not now

因此用户不再需要自己翻多份 docs 才知道“现在离理想形态还有多远、当前在哪个阶段、下一步该看什么”。

### 2. `grant-user-loop` 已 landed

当前仓库已新增一条新的 CLI product surface：

- `grant-user-loop`

它由 `src/med_autogrant/product_entry.py` 中的 `MedAutoGrantProductEntry.build_grant_user_loop(...)` 提供，并通过 `src/med_autogrant/cli.py` 暴露给 caller。

### 3. 这条 surface 是 controller-owned 的 user loop，而不是新的 executor

当前 `grant-user-loop` 只负责：

- 读取 `mainline-status`
- 读取 `mainline-phase`
- 读取 `grant-direct-entry`
- 根据 `grant_direct_entry.recommended_executor_route` 投影当前 `next_action`
- 把 mainline snapshot、direct-entry contract 与 next action 收成一份 inbox-like user loop

它不负责：

- 持有 runtime substrate owner
- 改写 author-side route owner
- 新增 service-safe domain executor
- 新增 hosted bundle command catalog

### 4. 这份 contract 现在已经 schema-backed、fail-closed

当前 `schemas/v1/schema-index.json` 已显式索引：

- `grant-user-loop.schema.json`

同时 `grant-user-loop` 在返回前会执行：

- `grant-user-loop.schema.json` 校验
- `grant_user_loop.task_intent` 与 `grant_direct_entry.task_intent` 一致性校验
- `next_action.route_id / route_status` 与 `grant_direct_entry.recommended_executor_route` 一致性校验
- landed route 与 pending handoff 两种 `next_action` shape 的 fail-closed 校验

因此如果有人改坏：

- mainline snapshot 的 phase / tranche 字段
- `grant_direct_entry` 与 `next_action` 的 route 对齐关系
- landed route 与 pending handoff 的 command / handoff surface 语义

都会直接 fail-closed。

### 5. `grant-user-loop` 当前输出什么

当前至少会稳定输出：

- `mainline_snapshot`
- `grant_direct_entry`
- `next_action`
- `user_loop`

其中：

- `mainline_snapshot` 会给出当前 active phase / tranche、phase map、next focus 与 remaining gaps
- `grant_direct_entry` 继续复用已冻结的 `grant-direct-entry` contract
- `next_action` 会在 landed route 时直接给出 executor command template，在 pending route 时给出 handoff surface command 集合
- `user_loop` 会直接给出 `mainline-status`、`mainline-phase`、`grant-cockpit`、`grant-direct-entry` 与 route execution template 的命令回路

### 6. 这条 surface 仍然不进入 service-safe domain command catalog

当前 `grant-user-loop` 故意不是：

- `MedAutoGrantDomainEntry` 的 service-safe domain command
- hosted contract bundle 的 command catalog 项
- 新的 route executor

因此它继续不进入：

- 不进入 `domain_entry_contract.supported_commands`
- 不进入 hosted contract bundle 的 command catalog

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_mainline_status.py tests/test_product_entry.py tests/test_cli_validate_workspace.py tests/test_schema_registry.py -q`
- `uv run pytest tests/test_program_control_surfaces.py tests/test_domain_runtime.py -q`

并验证：

- `mainline-status / mainline-phase` CLI dispatch 已 landed
- `grant-user-loop` CLI dispatch 已 landed
- `grant-user-loop.schema.json` 已进入 schema registry
- critique workspace 的 landed next action command 会被正确投影为 `execute-revision-pass`
- drafting workspace 的 pending critique route 不会被伪造为 landed executor，而是只输出 required handoff surface commands
- core docs、phase map 与 current-program pointer 已同步到 `P4.C` 口径

## Honest Boundary

这条 current truth 只说明：

- `P4.C mainline status and grant user loop` 已 landed
- 当前 repo 已经能直接投影理想目标 / phase ladder / remaining gaps，并把 direct grant user loop 收成当前 inbox-like shell

它不意味着：

- `P4 mature direct grant product entry` 整体已完成
- mature Web UI 已落地
- hosted runtime 已完成
- `OPL Gateway` 已在本仓落地
- pending authoring route 已拥有新的 landed executor
