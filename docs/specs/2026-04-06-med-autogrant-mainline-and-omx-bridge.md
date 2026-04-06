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

停止条件：

- 能用结构化 workspace 驱动一条完整 `NSFC` authoring loop
- 闭环里的对象引用、gate 和 route 清晰稳定
- critique / revision 不是散文，而是结构化 artifact

### P3. Mentor Critique And Revision Loop Hardening

目标：

- 把 `60/30/10` 导师批注与修订闭环做成 machine-readable 主线
- 编码 `major_reframe / major_revision / ready_for_submission`
- 把强制回退到 direction / question / argument 的条件收紧成可执行 route

停止条件：

- critique -> revision -> re-review 闭环 machine-readable
- 回退规则有 route 和验证支撑
- 批注不再停留在自由文本点评层

### P4. Dual-Mode Harness And Verification OS

目标：

- 把 evidence augmentation、`Human-in-the-loop`、verification、reports、checkpoint 收成连续运行面
- 让 `CURRENT_PROGRAM + reports + test-spec + implementation` 足以支撑 OMX 长跑
- 让 `Auto` / `Human-in-the-loop` 双模共享同一 substrate

停止条件：

- `OMX` 无需重建上下文即可持续推进
- team gate、验证口径和 final verification 稳定
- 人接管与 agent 接管边界 durable 可见

### P5. Grant Ops Gateway Expansion And Federation

目标：

- 让 `Med Auto Grant` 成为 `Grant Foundry` 的正式医学节点
- 准备第二类 grant family / project family 的接入能力
- 与 `Research Ops` / `Med Auto Science` 形成稳定共享基座和边界

停止条件：

- 至少完成一个非 `NSFC` 通用骨架的扩展示例
- 共享基座与 domain-specific logic 边界清楚
- 联邦接入 contract 明确，不是口头约定

## 当前活跃子线

当前唯一 active program：

- `med-autogrant-mainline`

当前 phase：

- `P1 / Reality Convergence And NSFC Baseline Freeze`

当前 tranche：

- `P1.A / authoritative NSFC workspace baseline`

这一 tranche 只做三件事：

1. 冻结长线 north star
2. 冻结 phase 顺序
3. 冻结 `Codex App <-> OMX` 的 durable handoff 机制

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
