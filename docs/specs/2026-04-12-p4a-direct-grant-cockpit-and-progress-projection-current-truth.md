# P4.A Direct Grant Cockpit And Progress Projection Current Truth

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-12`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.A direct grant progress / cockpit projection`
- Status: `landed / current truth`

## Goal

这条 current truth 不新增 repo-local hosted helper，也不把成熟 grant-facing 前台写成已落地。

它只解决一件事：

- 在已经 landed 的真实 `Hermes-Agent` substrate、`MedAutoGrantDomainEntry`、`build-product-entry` 之上，
- 先落一个 controller-owned、read-only 的 direct grant product projection，
- 让 direct user / operator / future caller 能用人话看见当前 grant 主线推进状态，
- 同时不改写 runtime owner、domain entry owner、author-side route owner。

## Landed Facts

### 1. `grant-progress` 与 `grant-cockpit` 已 landed，并进入 repo-tracked schema index

当前仓库已新增两条 CLI product projection surface：

- `grant-progress`
- `grant-cockpit`

这两条 surface 当前都由 `src/med_autogrant/product_entry.py` 中的 `MedAutoGrantProductEntry` 提供，并通过 `src/med_autogrant/cli.py` 暴露给 CLI caller。
当前 `schemas/v1/schema-index.json` 还已经显式索引：

- `grant-progress.schema.json`
- `grant-cockpit.schema.json`

因此这两条 projection 现在不只是“有命令、有文档”，而是 repo-tracked 的 schema-backed contract。

### 2. 这两条 surface 的定位是 controller-owned / read-only product projection

当前它们只负责：

- 读取既有 grant truth
- 输出面向用户 / operator / caller 的人话投影
- 给 direct grant product entry 的下一阶段留稳定 read-only projection surface

它们不负责：

- 持有 runtime substrate owner
- 持有 author-side route executor owner
- 改写 workspace / critique / revision / export truth
- 伪装成已落地的 Web UI / hosted runtime

### 3. 这两条 projection 现在会在生成时 schema-backed、fail-closed

当前 `src/med_autogrant/product_entry.py` 中：

- `read_grant_progress(...)` 会在返回前通过 `grant-progress.schema.json`
- `read_grant_cockpit(...)` 会在返回前通过 `grant-cockpit.schema.json`

也就是说，如果有人改坏：

- progress projection 的字段 shape
- cockpit command catalog 的字段 shape
- blocker / alert / focus / workspace overview 的 nullability 与 required 边界

就会直接 fail-closed，而不是静默漂移。

### 4. 它们只消费已冻结的现有 surface

当前 `grant-progress` / `grant-cockpit` 只读取：

- `stage-route-report`
- `summarize-workspace`
- `critique-summary`
  - 仅当 source workspace 已位于 `critique / revision / frozen` review context 时读取

同时它们还会复用：

- `build-product-entry` 的 direct / `opl-handoff` entry contract 信息

因此它们没有发明新的 repo-local truth surface，也没有复制新的 route contract。

### 5. `grant-progress` 当前输出的是 grant 主线的人话 progress projection

当前至少会稳定输出：

- `current_stage`
- `current_stage_summary`
- `checkpoint_status`
- `recommended_next_stage`
- `current_blockers`
- `next_system_action`
- `needs_author_decision`
- `author_decision_summary`
- `focus`
- `product_entry_surface`

其中：

- `focus` 会显式带出 `applicant_name`、`funding_program`、`selected_direction_title`、`selected_question`、`active_draft_title`、`critique_verdict`
- `product_entry_surface` 会显式告诉 caller：
  - `builder_command = build-product-entry`
  - `supported_entry_modes = [direct, opl-handoff]`
  - 当前 workspace path

### 6. `grant-cockpit` 当前输出的是 read-only direct product cockpit projection

当前至少会稳定输出：

- `workspace_overview`
- `workspace_status`
- `workspace_alerts`
- `progress_projection`
- `commands`

其中：

- `commands` 当前会显式给出：
  - `grant-progress`
  - `summarize-workspace`
  - `stage-route-report`
  - `critique-summary`
  - `build-product-entry --entry-mode direct`
  - `build-product-entry --entry-mode opl-handoff`

这意味着 direct user / operator / future caller 现在已经可以先看一层稳定的 read-only cockpit，再决定是否进入 direct entry 或 `OPL` handoff。

### 7. 这两条 surface 没有被写进 `domain_entry_contract.supported_commands`

当前 `grant-progress` / `grant-cockpit` 故意不是：

- `MedAutoGrantDomainEntry` 的 service-safe domain entry command
- future hosted caller 必须调用的执行器 surface

原因是：

- 它们属于 product-facing read-only projection
- 不是 author-side route executor
- 也不是新的 service-safe domain execution contract

因此当前 `domain_entry_contract.supported_commands` 仍然只冻结已 landed 的 domain/runtime command catalog，不把这两条 projection surface 误写成新的 executor surface。
同样地，它们也不进入 hosted contract bundle 的 command catalog；hosted bundle 继续只导出已 landed 的 domain/runtime command contract，而不把 product-facing projection 混成 external executor surface。

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_schema_registry.py tests/test_product_entry.py -q`
- `uv run pytest tests/test_hermes_runtime_truth.py tests/test_program_control_surfaces.py -q`

并验证：

- `grant-progress` / `grant-cockpit` CLI dispatch 已 landed
- `grant-progress.schema.json` / `grant-cockpit.schema.json` 已进入 schema registry
- malformed progress / cockpit projection shape 会被 fail-closed 拒绝
- critique / frozen workspace 的 progress projection shape 已冻结
- cockpit alert / command catalog 已冻结
- core docs 与 current-program pointer 已同步到 `P4.A` 口径
- `domain_entry_contract.supported_commands` 没有把这两条 projection surface 混入 service-safe executor catalog
- hosted contract bundle 的 command catalog 也没有把这两条 projection surface 混进去

## Honest Boundary

这条 current truth 只说明：

- `P4` 的第一棒 `P4.A` 已 landed
- direct grant product entry 现在已有第一层 controller-owned / read-only projection
- 这层 projection 现在已经是 schema-backed、generation-time fail-closed 的 contract surface

它不意味着：

- `P4 mature direct grant product entry` 整体已完成
- grant-facing Web UI 已落地
- actual hosted runtime 已完成
- `OPL Gateway` 已在本仓落地
- pending authoring route 已改写成 landed executor
