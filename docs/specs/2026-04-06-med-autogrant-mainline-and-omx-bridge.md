# Med Auto Grant 长线主线与 Codex App / OMX 交互模型

> 当前文档面向内部主线规划与运行框架冻结，只保留中文版本。

Date: `2026-04-06`

## 目标

把 `Med Auto Grant` 从“已经有一点 schema 和 CLI 的 repo scaffold”，推进成一条可以长期由 `Codex App + OMX` 接力推进的 active mainline。

这里要解决的不是单轮任务如何写完，而是：

- 长线 north star 是什么
- 每个阶段大概要做什么
- 什么信息必须被 durable 地写下来
- `Codex App` 和 `OMX` 到底怎么交接，而不是靠一次性聊天上下文

## North Star

`Med Auto Grant` 的长线目标是：

> 构建一个作者侧、proposal-facing、agent-first 的医学 `Grant Ops` 主线系统，先在 `NSFC` 通用骨架上跑通“输入接入 -> 方向收敛 -> 科学问题提纯 -> 论证链条 -> 草稿 -> 导师批注 -> 修订”的闭环，再逐步扩展到证据增强、submission-grade 交付和 `Grant Foundry` 联邦接入。

这个 north star 明确排除以下误解：

- 不是单纯的“自动补全文本模板”
- 不是 reviewer side 审稿系统
- 不是固定代码流程去替代高判断密度创作
- 不是某一种外部 LLM API 的壳

## 为什么要固定 Codex App / OMX 双层

如果没有 durable control surface，`OMX` 每次长跑都需要重新理解项目，容易出现三类漂移：

1. 把当前阶段的 guardrail 当成产品目标
2. 把历史一次性讨论当成当前真相
3. 把 runtime 执行状态和产品方向混在一起

因此这个项目固定采用双层：

- `Codex App`
  - 负责规划、阶段验收、切 program / 切 phase、处理 truth conflict
- `OMX`
  - 负责长时间连续执行、lane 拆分、报告回写、断点恢复

交接必须依赖 durable 文件，而不是依赖旧 terminal 和记忆。

## Durable 交接机制

### 1. 项目真相层

- `contracts/project-truth/AGENTS.md`

这层定义：

- 项目是什么 / 不是什么
- 当前固定边界
- 当前阶段顺序
- `Codex App` / `OMX` 的责任边界

### 2. 当前 program 指针

- `.omx/context/CURRENT_PROGRAM.md`

这层定义：

- 当前唯一 active program
- 当前 phase / tranche
- long-horizon order
- 当前必须读取的 truth source

### 3. OMX 可执行提示面

- `.omx/context/PROGRAM_ROUTING.md`
- `.omx/context/OMX_TEAM_PROMPT.md`

其中：

- `PROGRAM_ROUTING.md` 负责说明 roadmap、PRD、test-spec、implementation、reports 分别写到哪里
- `OMX_TEAM_PROMPT.md` 负责定义 OMX 实际接力时的读取顺序和执行纪律

这两层都不是产品文档，而是给 `OMX` 的长期执行入口。

它必须明确：

- 先读什么
- 按什么顺序推进
- 什么情况下可以不停机继续跑
- 什么情况下必须停下来交回 `Codex App`

### 4. Program 计划层

- `.omx/plans/spec-program-operating-model.md`
- `.omx/plans/prd-med-autogrant-mainline.md`
- `.omx/plans/test-spec-med-autogrant-mainline.md`
- `.omx/plans/implementation-med-autogrant-mainline.md`

它们分别回答：

- 协作模型怎么工作
- 当前 long-line 产品目标是什么
- 当前阶段怎么验收
- 当前 tranche 怎么拆执行

### 5. 运行报告层

- `.omx/reports/med-autogrant-mainline/LATEST_STATUS.md`
- `.omx/reports/med-autogrant-mainline/ITERATION_LOG.md`
- `.omx/reports/med-autogrant-mainline/OPEN_ISSUES.md`

这层负责把运行中的项目状态 durable 化，避免恢复时只能看旧 pane。

## P0：正式执行句柄（`grant_run_id`）合同

当前 mainline 在 `P1.B` 已冻结并在当前 tranche 继续保持如下边界：

- `grant_run_id`
  - 当前 grant run 的稳定执行句柄
  - 必须由 workspace 输入显式提供
  - CLI 输出、runtime reports 与未来恢复入口必须回显同一个 `grant_run_id`
- `workspace_id`
  - `NSFCWorkspace` 聚合根身份
  - 回答“这是哪个 grant workspace”，不是“这是哪一次运行”
- `draft_id`
  - `ApplicationDraft` 身份
  - `revision` 完成后仍沿用同一 `draft_id`，不借由 run handle 生成新草稿身份
- `program_id`
  - `med-autogrant-mainline` 这一长期 active mainline 的控制面句柄
  - 用来路由 `.omx/reports/<program_id>/` 与 pointer-bearing control surfaces，不等于单次 runtime run

当前需要保持的 formal durable entry 真相是：

- runtime / user-facing formal entry 仍以当前 CLI 为准
- `OMX` 的恢复入口仍是 `OMX_TEAM_PROMPT + CURRENT_PROGRAM + PROGRAM_ROUTING + active plans + active reports`
- `grant_run_id` 只负责把同一次运行绑到同一输出与恢复上下文，不扩成新的 MCP / controller surface
- 上述 formal entry matrix 的单独 current truth 冻结在 `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`

针对这次 `grant_run_id` 合同，还要固定 review / handoff 边界：

- repo-tracked review surfaces
  - `README*`
  - `docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`
  - `docs/specs/2026-04-06-object-model-schema-v1.md`
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `schemas/v1/nsfc-workspace.schema.json`
  - `examples/nsfc_workspace_minimal.json`
- local durable handoff surfaces
  - `.omx/context/**`
  - `.omx/plans/**`
  - `.omx/reports/**`

当前 durability model clarification 的单独 current truth 冻结在 `docs/specs/2026-04-07-durability-model-clarification.md`。

也就是说：

- reviewer 应能仅凭 repo-tracked review surfaces 理解 `grant_run_id` 的正式合同
- `.omx/**` 仍然承担本机 durable handoff 责任，但不是这次提交必须依赖的 review 入口

## 当前固定阶段顺序

### P1. Reality Convergence And NSFC Baseline Freeze

目标：

- 建立分层合同
- 固定 current program
- 把最小 runtime baseline 与验证门收紧
- 让 `Codex App` 与 `OMX` 可以围绕同一批文件接力

当前包含：

- schema / workspace 最小 baseline
- CLI 最小命令集
- `.omx` control surfaces
- `.codex/AGENTS.md`

停止条件：

- 主线文档冻结
- installer baseline 不漂移
- 最小 CLI 与测试命令通过
- `OMX` 可以不靠一次性长提示词恢复并继续推进

### P2. NSFC Authoring Mainline Freeze

目标：

- 把 `NSFC` 通用申请主线做成真实可运行 loop
- 从结构化输入推进到：
  - 方向候选
  - 科学问题
  - argument chain
  - 草稿
  - critique
  - revision plan
- 在不提前硬化 `P3` verdict / rollback 语义的前提下，收通第一轮 `critique / revision` skeleton

停止条件：

- 能用结构化 workspace 驱动一条完整 `NSFC` authoring loop
- 闭环里的对象引用、gate 和 route 清晰稳定
- critique / revision 不是散文，而是结构化 artifact

当前预冻结 tranche：

- `P2.A / Intake-Direction-Question Mainline`
- `P2.B / Argument-Fit-Outline Mainline`
- `P2.C / Draft-Critique-Revision Skeleton`

### P3. Mentor Critique And Revision Loop Hardening

目标：

- 把 `60/30/10` 导师批注与修订闭环做成 machine-readable 主线
- 编码 `major_reframe / major_revision / ready_for_submission`
- 编码 `draft -> revised`、re-review 与 presubmission gate
- 把强制回退到 direction / question / argument 的条件收紧成可执行 route

停止条件：

- critique -> revision -> re-review 闭环 machine-readable
- 回退规则有 route 和验证支撑
- 批注不再停留在自由文本点评层

当前预冻结 tranche：

- `P3.A / Mentor Verdict Contract Freeze`
- `P3.B / Revision Transition And Re-Review Hardening`
- `P3.C / Forced Rollback And Presubmission Gate`

### P4. Dual-Mode Harness And Verification OS

目标：

- 把 evidence augmentation、`Human-in-the-loop`、verification、reports、checkpoint 收成连续运行面
- 让 `CURRENT_PROGRAM + reports + test-spec + implementation` 足以支撑 OMX 长跑
- 让 `Auto` / `Human-in-the-loop` 双模共享同一 substrate

停止条件：

- `OMX` 无需重建上下文即可持续推进
- team gate、验证口径和 final verification 稳定
- 人接管与 agent 接管边界 durable 可见

当前预冻结 tranche：

- `P4.A / Dual-Mode Gate Surface`
- `P4.B / Verification OS And Checkpoint Surface`

### P5. Grant Ops Gateway Expansion And Federation

目标：

- 让 `Med Auto Grant` 成为 `Grant Foundry` 的正式医学节点
- 准备第二类 grant family / project family 的接入能力
- 与 `Research Ops` / `Med Auto Science` 形成稳定共享基座和边界

停止条件：

- 至少完成一个非 `NSFC` 通用骨架的扩展示例
- 共享基座与 domain-specific logic 边界清楚
- 联邦接入 contract 明确，不是口头约定

当前预冻结 tranche：

- `P5.A / Second Grant Family Onboarding`
- `P5.B / Federation Contract Freeze`

## Future Same-Phase Auto-Promotion Envelope

- future `P2 / P3` 只在对应 phase 已先由 `Codex App` 激活时，才允许 `OMX` 在同一 phase 内执行 `same-phase auto-promotion`
- `same-phase auto-promotion` 只允许推进到已预冻结的下一 tranche，不允许顺手补写新的产品语义
- `OMX` 在该 envelope 内只能改写 pointer-bearing control surfaces 与 reports；phase promotion 仍必须交回 `Codex App`
- `P4 / P5` 当前只冻结 tranche map，不开放 `same-phase auto-promotion`

## 当前活跃子线

当前唯一 active program：

- `med-autogrant-mainline`

当前 phase：

- `P2 / NSFC Authoring Mainline Freeze`

当前 tranche：

- `P2.B / Argument-Fit-Outline Mainline`

其中：

1. `P1.A / authoritative NSFC workspace baseline` 与 `P1.B / runtime baseline hardening` 已完成 repo-native baseline、formal entry、durability 与 `grant_run_id` 合同冻结
2. 当前 `P2.B` 只继续收通 `argument_building -> fit_alignment -> outline`，并保持当前 hard boundary不漂移
3. 当前允许做的是 P2.B runtime / CLI / tests / reports / docs 的同轴收口，不允许偷跑 `P2.C / P3+`；future tranche map 与 `same-phase auto-promotion` 只作为后续 phase activation 的预冻结合同存在

### 保留的 P1.B hard boundary：revision transition minimal contract

- `P1.B` 已把 `draft -> revised` 的最小语义写成 durable control surface；当前 `P2.B` 必须继续保留这一 hard boundary，而不是删弱它。
- 触发 gate 固定为 `RevisionPlan.execution_status`；当 `RevisionPlan.execution_status=completed` 时，post-revision 必须继续沿用同一 `draft_id`，保持同一 `frozen_question_id`，并保留当前 argument chain 链接。
- 切换后的最小差异约束固定为：`active_draft.status` 必须显式变成 `revised`，`active_draft.version_label` 必须等于 `post_revision_version_label`，且 `post_revision_version_label` 必须不同于 `pre_revision_version_label`。
- `comparison_summary` 必须非空，用来表达 pre-revision draft 与 post-revision revised draft 的前后版本比较证据。
- 当 `revision` 阶段已经满足上述 contract 并持有 `revised` 草稿时，最小 route 应回到 `critique` 做 re-review；更完整的多轮 hardening 仍留给 future `P3.B / Revision Transition And Re-Review Hardening`。

### 当前 P2.B canonical surface

- `docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
- 该文件当前冻结：
  - `argument_building -> fit_alignment -> outline`
  - `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 的显式绑定
  - `outline -> drafting` 的 transition contract

## OMX 长线运行入口

给 `OMX` 的长期执行入口不再是手写一段一次性提示词，而是：

- 先读 `.omx/context/OMX_TEAM_PROMPT.md`
- 再按其中规定读取 `CURRENT_PROGRAM + plans + reports`
- 然后只围绕当前 active program 推进

也就是说，“提示词”本身已经被拆成 durable control surface，而不是继续停留在聊天里。

## 当前不做

这一轮明确不做：

- 一口气覆盖所有 grant family
- 为了“让 OMX 好跑”而牺牲项目边界
- 把 `.omx` 报告写成一次性总结，而不维护持续状态
- 把 `Codex App` 与 `OMX` 的职责重新混回一个对话里
- 把 future tranche map 误当成当前 phase 的执行许可
