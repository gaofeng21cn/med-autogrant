# Med Auto Grant 长线主线与 Codex App / OMX 交互模型

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_foundation_program_handoff_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-06 长线主线、旧 Codex App / OMX 交接与早期 durable handoff 形成过程。当前 active program、OPL/Temporal runtime owner、runtime-state 边界、active specs 与机器行为以核心五件套、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

> 当前文档面向内部主线规划与运行框架冻结，只保留中文版本。

Date: `2026-04-06`

## 目标

把 `Med Auto Grant` 从“已有最小 runtime baseline 的医学 `Grant Ops` mainline”，继续推进成一条可以长期由 `Codex App + OMX` 连续执行的 active mainline。

这里要解决的不是单轮任务如何写完，而是：

- 长线 north star 是什么
- 每个阶段大概要做什么
- 什么信息必须被 durable 地写下来
- `Codex App` 和 `OMX` 到底怎么交接，而不是靠一次性聊天上下文

这里同样必须严格区分：

- 长线目标
- 当前 phase / tranche
- durable handoff

长线目标回答的是项目理想终态；
当前 phase / tranche 回答的是当前这轮 repo-tracked 收口点；
durable handoff 回答的是控制面如何不断点连续推进。

因此，默认不应把这份文档理解成：

- 每一棒都要停机交棒
- 只有人工再次点名才允许继续
- OMX 只能做 same-phase 收尾

## North Star

`Med Auto Grant` 的长线目标是：

> 构建一个作者侧、proposal-facing、agent-first 的医学 `Grant Ops` 主线系统，先在 `NSFC` 通用骨架上跑通“输入接入 -> 方向收敛 -> 科学问题提纯 -> 论证链条 -> 草稿 -> 导师批注 -> 修订”的闭环，再逐步扩展到证据增强、submission-grade 交付和 `Grant Foundry` 联邦接入。

这个 north star 明确排除以下误解：

- 不是单纯的“自动补全文本模板”
- 不是 reviewer side 审稿系统
- 不是固定代码流程去替代高判断密度创作
- 不是某一种外部 LLM API 的壳

当前还必须补一条固定理解：

- 当前 repo-tracked 产品主线按 `Auto-only` 理解
- 未来若要做高判断密度 `Human-in-the-loop` 产品，应作为兼容 sibling 或 upper-layer product 复用同一 substrate，而不是把当前仓改成同仓双模
- formal-entry matrix 固定为：`CLI` 作为默认 formal entry，`MCP` 作为保留的 future protocol layer，`controller` 作为 internal control surface

## 为什么要固定 Codex App / OMX 双层

如果没有 durable control surface，`OMX` 每次长跑都需要重新理解项目，容易出现三类漂移：

1. 把当前阶段的 guardrail 当成产品目标
2. 把历史一次性讨论当成当前真相
3. 把 runtime 执行状态和产品方向混在一起

因此这个项目固定采用双层：

- `Codex App`
  - 负责规划、truth freeze、阶段验收、切 program / 切 phase、处理 truth conflict
- `OMX`
  - 负责长时间连续执行、lane 拆分、报告回写、断点恢复，并在已冻结边界内自主选择下一棒

交接必须依赖 durable 文件，而不是依赖旧 terminal 和记忆。
但 durable handoff 是为了支持连续执行，不是为了默认逐棒停车。

## Durable 交接机制

### 1. 项目真相层

- `AGENTS.md`

这层定义：

- 项目是什么 / 不是什么
- 当前固定边界
- 当前阶段顺序
- `Codex App` / `OMX` 的责任边界

### 2. 当前 program 指针

- `.runtime-program/context/CURRENT_PROGRAM.md`

这层定义：

- 当前唯一 active program
- 当前 phase / tranche
- long-horizon order
- 当前必须读取的 truth source

### 3. OMX 可执行提示面

- `.runtime-program/context/PROGRAM_ROUTING.md`
- `.runtime-program/context/OMX_TEAM_PROMPT.md`

其中：

- `PROGRAM_ROUTING.md` 负责说明 roadmap、PRD、test-spec、implementation、reports 分别写到哪里
- `OMX_TEAM_PROMPT.md` 负责定义 OMX 实际接力时的读取顺序和执行纪律

这两层都不是产品文档，而是给 `OMX` 的长期执行入口。

它必须明确：

- 先读什么
- 按什么顺序推进
- 什么情况下可以继续连续跑
- 什么情况下必须停下来交回 `Codex App`

### 4. Program 计划层

- `.runtime-program/plans/spec-program-operating-model.md`
- `.runtime-program/plans/prd-med-autogrant-mainline.md`
- `.runtime-program/plans/test-spec-med-autogrant-mainline.md`
- `.runtime-program/plans/implementation-med-autogrant-mainline.md`
- `docs/specs/2026-04-08-runtime-first-productization-program.md`

它们分别回答：

- 协作模型怎么工作
- 当前 long-line 产品目标是什么
- 当前阶段怎么验收
- 当前 tranche 怎么拆执行

### 5. 运行报告层

- `.runtime-program/reports/med-autogrant-mainline/LATEST_STATUS.md`
- `.runtime-program/reports/med-autogrant-mainline/ITERATION_LOG.md`
- `.runtime-program/reports/med-autogrant-mainline/OPEN_ISSUES.md`

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
  - 用来路由 `.runtime-program/reports/<program_id>/` 与 pointer-bearing control surfaces，不等于单次 runtime run

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
  - `.runtime-program/context/**`
  - `.runtime-program/plans/**`
  - `.runtime-program/reports/**`

当前 durability model clarification 的单独 current truth 冻结在 `docs/specs/2026-04-07-durability-model-clarification.md`。

也就是说：

- reviewer 应能仅凭 repo-tracked review surfaces 理解 `grant_run_id` 的正式合同
- `.runtime-program/**` 仍然承担本机 durable handoff 责任，但不是这次提交必须依赖的 review 入口

## 当前固定阶段顺序

这条顺序仍然是 domain maturity order，不等于当前执行优先级。

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

### P4. Verification OS And HITL Layering Preparation

目标：

- 把 evidence augmentation、verification、reports、checkpoint 收成连续运行面
- 让 `CURRENT_PROGRAM + reports + test-spec + implementation` 足以支撑 OMX 长跑
- 为未来 `Human-in-the-loop` sibling 或 upper-layer product 预留可复用的 substrate-compatible contract 与模块边界

停止条件：

- `OMX` 无需重建上下文即可持续推进
- team gate、验证口径和 final verification 稳定
- 上层 `Human-in-the-loop` 产品可复用的边界 durable 可见

当前预冻结 tranche：

- `P4.A / Verification Gate Surface`
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

当前对应的 pre-frozen activation package：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p5a-second-grant-family-onboarding-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p5b-federation-contract-freeze-activation-package.md`

## 当前 active execution priority

当前 active execution priority 不再继续把 `P4.B -> P5.A -> P5.B` 视为唯一长线。

当前改为：

- 先按 runtime-first ladder 做成熟本地产品 runtime
- 再做 hostedization prep
- `P5.A / P5.B` 转为 deferred future expansion

当前 active execution phase：

- `Runtime Productization Program`

当前 active execution tranche：

- `R2 / Artifact Production Surface`

当前 runtime-first ladder：

1. `R1 / Autonomous Main Loop`
2. `R2 / Artifact Production Surface`
3. `R3 / Critique Revision Autoloop`
4. `R4 / Finalization And Export Surface`
5. `R5 / Hostedization Prep`

对应 repo-tracked internal program doc：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`

当前对应的 pre-frozen future boundary map：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`

## Autonomous Longrun Program Mode

当 north star、阶段顺序、硬边界与 stop conditions 已冻结时，当前默认推荐的是：

- `OMX` 在已冻结边界内连续执行
- 每一轮都回写 `CURRENT_PROGRAM + plans + reports`
- 每一轮 tranche 收口后直接 absorb 到 `main`
- 然后继续判断下一棒，而不是默认停机等待人工点名

只有在下面情况出现时，才应交回 `Codex App`：

- frozen truth conflict 无法在现有合同内裁决
- 需要新的产品级方向选择
- 需要改变 phase 顺序或扩大 domain 边界
- 需要外部输入、授权或凭据

这意味着：

- `same-phase auto-promotion` 不再是默认上限语义
- 默认姿势是 `autonomous longrun program mode`
- phase / tranche 仍然是 program pointer，但不等于长线目标本身

## 当前活跃子线

当前唯一 active program：

- `med-autogrant-mainline`

当前 active execution phase：

- `Runtime Productization Program`

当前 active execution tranche：

- `R3 / Critique Revision Autoloop`

当前 latest absorbed slice：

- `R2.A / Artifact Bundle Production Surface`
- upstream `R1.A / Local Main Loop Entry And Stop Reason`
  - freeze absorb：`38b5347`
  - implementation absorb：`8e087dc`
- `R1.B` activation freeze absorb：`2b193da`
- `R1.B` implementation absorb：`2953026`
- `R2.A` activation freeze absorb：`424ded0`
- `R2.A` implementation：absorbed in current mainline truth

当前 future boundary 已预冻结：

1. `R3.A / Critique Revision Executor Surface`
2. `R4.A / Final Freeze And Export Package`
3. `R5.A / Hosted-Friendly Session Boundary`

对应的精确 package / contract：

- `R3.A` activation package：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-r3a-critique-revision-executor-surface-activation-package.md`
- `R3.A` machine-applicable implementation contract：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`
- `R4.A` activation package：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`
- `R5.A` activation package：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md`

对应 repo-tracked boundary map：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`

这组边界的作用是：

1. 允许 `OMX` 从当前 latest absorbed runtime slice 出发，继续做 honest delta audit
2. 允许 `OMX` 把下一增量正确归类到 `R3.A / R4.A / R5.A`
3. 如果下一能力其实已经属于更后面的 stage，允许直接重分类到后面的 pre-frozen package，而不是强行在当前 stage 编造中间 tranche
4. 只有在没有 honest delta 或下一步需要新平台语义 / 外部 readiness 时，才允许停车
5. `P5.A / P5.B` 继续只保留为 deferred future expansion，不属于这条 `R1 -> R5` 本地主线的实现面

### 保留的 P1.B hard boundary：revision transition minimal contract

- `P1.B` 已把 `draft -> revised` 的最小语义写成 durable control surface；当前 `P2.C` 必须继续保留这一 hard boundary，而不是删弱它。
- 触发 gate 固定为 `RevisionPlan.execution_status`；当 `RevisionPlan.execution_status=completed` 时，post-revision 必须继续沿用同一 `draft_id`，保持同一 `frozen_question_id`，并保留当前 argument chain 链接。
- 切换后的最小差异约束固定为：`active_draft.status` 必须显式变成 `revised`，`active_draft.version_label` 必须等于 `post_revision_version_label`，且 `post_revision_version_label` 必须不同于 `pre_revision_version_label`。
- `comparison_summary` 必须非空，用来表达 pre-revision draft 与 post-revision revised draft 的前后版本比较证据。
- 当 `revision` 阶段已经满足上述 contract 并持有 `revised` 草稿时，最小 route 应回到 `critique` 做 re-review；当前 `P3.B` 继续把这条边界收紧成“当前 active revision plan + reviewed completed revision evidence”双锚定合同。

### 当前 P2.B / P2.C / P3.A / P3.B / P3.C / P4.A / P4.B canonical surface

- absorbed P2.B：`docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
- absorbed P2.C：`docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
- absorbed P3.A：`docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`
- absorbed P3.B：`docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- absorbed P3.C：`docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- absorbed P4.A：`docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`
- 当前 P4.B：`docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`
- future P5.A activation package：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p5a-second-grant-family-onboarding-activation-package.md`
- future P5.B activation package：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p5b-federation-contract-freeze-activation-package.md`
- 这七份文件当前共同冻结：
  - `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 的上游绑定
  - `drafting -> critique -> revision` 的 absorbed 主线与 completed revision 回到 critique 的 re-review 边界
  - `major_reframe / major_revision / minor_revision / ready_for_submission` 的 canonical verdict branch
  - `current_selection.active_revision_plan_id`、`MentorCritique.reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id` 与当前 active `RevisionPlan` 的 re-review 双锚定合同
  - `MentorCritique.forced_rollback_stage / forced_rollback_reason` 与 `presubmission_frozen` 的 P3.C hard gate
  - `stage-route-report.verification_checkpoint / checkpoint_status` 与 `ready_for_submission + presubmission_frozen=false` 的 P4.A gate-open checkpoint surface
  - `VerificationCheckpoint` 作为 derived checkpoint object 的 P4.B durable surface，以及它与 reports / control surfaces 的 checkpoint truth 对齐关系
  - second-family onboarding 必须具备的 admission package、verification gate、excluded scope 与 invariants
  - federation contract freeze 必须具备的 package、audit、export、gate semantics 与 admitted-family exact-set 边界

## OMX 长线运行入口

给 `OMX` 的长期执行入口不再是手写一段一次性提示词，而是：

- 先读 `.runtime-program/context/OMX_TEAM_PROMPT.md`
- 再按其中规定读取 `CURRENT_PROGRAM + plans + reports`
- 然后只围绕当前 active program 推进

默认推进姿势应理解为：

- 不停留在“本轮收口完就自然停车”
- 而是在 truth 足够时继续向长线目标逼近

也就是说，“提示词”本身已经被拆成 durable control surface，而不是继续停留在聊天里。

## 当前不做

这一轮明确不做：

- 一口气覆盖所有 grant family
- 为了“让 OMX 好跑”而牺牲项目边界
- 把 `.omx` 报告写成一次性总结，而不维护持续状态
- 把 `Codex App` 与 `OMX` 的职责重新混回一个对话里
- 把 future tranche map 误当成当前 phase 的执行许可
