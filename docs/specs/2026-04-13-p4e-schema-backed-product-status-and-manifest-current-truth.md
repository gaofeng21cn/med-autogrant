# P4.E Schema-Backed Product status And Manifest Current Truth

Date: `2026-04-13`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.E schema-backed product status and manifest contract landing`
- Status: `landed / current truth`

## Goal

把 `product-entry-manifest` 与 `product-status` 从“已经有输出 shape 的 controller surface”进一步收口成独立的 schema-backed、generation-time fail-closed direct product entry contract，并继续保持以下边界不变：

- `Codex CLI` 继续是默认 concrete executor
- `Hermes-Agent` 只作为显式 OPL receipt/proof lane，不持有默认 runtime、authoring executor、grant truth 或 quality verdict
- `Med Auto Grant` 继续持有 grant domain truth、author-side route 与导出物 owner
- `product-entry-manifest` / `product-status` 继续只是 controller-owned product entry / discovery contract，而不是新的 domain executor 或 mature Web UI

## Landed Facts

### 1. `product-entry-manifest` 与 `product-status` 现在各自拥有独立 schema

当前 product entry contract 现在新增两份独立 schema：

- `schemas/v1/product-entry-manifest.schema.json`
- `schemas/v1/product-status.schema.json`

并且它们已经登记进：

- `schemas/v1/schema-index.json`

这意味着当前 direct grant product entry 不再只是“有文档说明、有测试样例”的 surface，而是与 `product-entry`、`grant-progress`、`grant-cockpit`、`grant-direct-entry`、`grant-user-loop` 并列的 repo-tracked、machine-readable contract。

### 2. manifest / product status 现在在生成时 fail-closed

`product_entry.py` 当前在生成：

- `build_product_entry_manifest(...)`
- `build_product_product status(...)`

之后，会分别立即执行对应的 contract 校验。

因此当前 product entry contract 的 truth 约束不再只靠：

- 文档描述
- 调用侧约定
- 测试样例

而是直接由生成期 schema 校验 fail-closed 兜住。

### 3. `family_orchestration` companion 的 route status 已回到共享 truth 单源

此前 `family_orchestration` companion 在 `grant-progress` / `product-entry-manifest` / `product-status` 上仍可能使用本地过期的 landed-route 集合判断 gate / route status。

当前已经统一改成直接读取共享 author-side route contract。

这意味着像：

- `question_refinement`
- `argument_building`
- `fit_alignment`
- `outline`
- `drafting`

这类在 `P4.D` 已经 landed 的 authoring route，不会再在 product entry companion 上被误投成 `pending / requested`。

### 4. `product_entry_overview` 已进入同一份 product entry contract

`product-entry-manifest` 与 `product-status` 现在还会共同暴露 `product_entry_overview` companion，用同一份结构收起：

- 当前入口摘要
- `product status_command`
- `recommended_command`
- `operator_loop_command`
- `progress_surface`
- `resume_surface`
- `recommended_step_id`
- `next_focus`
- `remaining_gaps_count`
- `human_gate_ids`

这层 overview 是 `product_entry_status`、`product_entry_quickstart` 与 `family_orchestration` companion 之上的用户侧摘要面，用来让 direct caller 不必再分别拼 progress / resume / gate id。

### 5. `grant_authoring_readiness` 现在显式回答“全自动 / 能用 / 好用”

`product-entry-manifest` 与 `product-status` 现在还会共同暴露 `grant_authoring_readiness` companion，用同一份 machine-readable 结构回答用户视角的成熟度问题：

- `fully_automatic = false`
- `usable_now = true`
- `good_to_use_now = false`
- 当前 verdict：`agent_assisted_cli_ready_not_full_autopilot`
- 当前体验层级：`usable_for_agent_assisted_cli_authoring_not_yet_polished_product`

这条 verdict 的含义是：当前系统可以作为 Agent 协同的 CLI/controller 标书写作主线使用，但还不是无需人工材料、无需判断、可直接交付的全自动国自然标书产品。

`grant_authoring_readiness.workflow_coverage` 会把人工国自然写作流程映射到当前能力面：

- 从已有积累中筛选方向：landed route
- 筛选可嵌入的热点：partially supported
- 锚定具体临床问题：landed route
- 设计创新点和跨尺度框架：landed route
- 搭建整体课题并反复校验主线：landed route
- 先写研究意义，再写研究背景：landed route
- 补足预实验、研究基础和前期结果：partially supported
- 完善预期结果与研究进度：partially supported
- 全文反复检查并补图补结果：partially supported

因此后续不能再笼统宣称“已经全自动写标书”；必须用这份 readiness companion 区分“可用的 Agent-assisted CLI 主线”和“尚未完成的 mature product / submission-ready autopilot”。

### 6. 当前 direct grant product entry 已形成一致的 contract 组合

现在 direct grant product entry 的 machine-readable 组合至少包括：

- `product-entry-manifest`
- `product-status`
- `grant-progress`
- `grant-cockpit`
- `grant-direct-entry`
- `grant-user-loop`

其中：

- `product-entry-manifest` 负责 discovery / overview / readiness / quickstart / mainline snapshot
- `product-status` 负责 direct product entry / operator loop / projection action surface
- 其余 projection / loop surface 继续承载 progress、cockpit、composition 与 inbox-like user loop

它们现在共同对齐的是：

- 同一份 mainline snapshot
- 同一份 controller-owned product entry truth
- 同一份 shared author-side route truth

## Verification

本 tranche 至少覆盖：

- `uv run pytest tests/test_schema_registry.py tests/test_product_entry.py -q`
- `uv run pytest tests/test_mainline_status.py tests/test_program_control_surfaces.py tests/test_cli_validate_workspace.py -q`
- `scripts/verify.sh`

重点验证：

- 新 schema 已进入 `schema-index.json`
- manifest / product status 在生成时执行 fail-closed 校验
- `product_entry_overview` 在 manifest / product status schema 中保持同一份结构化 companion contract
- `grant_authoring_readiness` 在 manifest / product status schema 中保持同一份“全自动 / 能用 / 好用”成熟度判断 contract
- `family_orchestration` companion 在 product entry / projection surface 上与 landed route truth 保持一致
- `current-program`、`mainline-status`、README / docs / tests 对当前 `P4.E` 口径保持同步

## Honest Boundary

这条 current truth 只说明：

- `product-entry-manifest` 与 `product-status` 已 landed 为独立 schema-backed contract
- `product_entry_overview` 已成为 direct grant product entry contract 的结构化 companion
- `grant_authoring_readiness` 已成为 direct grant product entry contract 的结构化成熟度 companion
- 当前 product entry / projection / user loop 看到的是同一份 shared route truth
- 当前 direct grant product entry 的 machine-readable contract 边界已经进一步冻结

它不意味着：

- mature direct grant Web UI / hosted runtime 已完成
- `OPL Gateway` 已在本仓落地
- 当时语境下的 family product-entry manifest v2、event envelope、checkpoint lineage 已经落地；当前 provider-backed / stage-led 口径下，这不等于 Temporal provider、Codex stage activity runner、human-gate Signal/Query 或真实 long-run soak 已完成
