# Med Auto Grant Project Truth Contract

This file is the single project truth contract for the repository.
It defines what this project is, what it is not, which boundaries are authoritative, and what structural constraints must survive future refactors.

## Scope

Apply this contract to the repository as a whole unless a deeper `AGENTS.md` explicitly overrides it for a narrower subtree.

This contract is not the repository development entrypoint.
The root `AGENTS.md` remains the development/orchestration entry file, while this file holds the project-specific truth that should not be mixed back into host setup mechanics.

## Project Identity

`Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上，面向医学 `Grant Ops` 的 `Domain Harness OS` 方向/系统。

它当前是：

- 医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 主线
- 共享 substrate 上的 domain harness 实现，而不是独立 substrate
- 作者侧、proposal-facing 的基金申请主线
- `Agent-first` 的 grant authoring 基座
- 以 `Codex-default host-agent runtime` 作为当前默认本地执行形态的最小 runtime baseline
- 当前 formal-entry matrix 固定为：
  - `default_formal_entry`：`CLI`
  - `supported_protocol_layer`：`MCP`（当前保留为 future protocol layer，尚未 repo-verified）
  - `internal_controller_surface`：`controller`
- 当前 repo-tracked 产品主线按 `Auto-only` 理解；未来若做高判断密度 `Human-in-the-loop` 产品，应作为兼容 sibling 或 upper-layer product 复用同一 substrate，而不是把当前仓改成同仓双模

它当前不是：

- 已完成的成熟 runtime 或 submission-grade autopilot
- reviewer-owned surface
- `Research Ops` 的论文写作分支
- 只会补模板、润色措辞的文本生成器
- 绑定某一种外部 LLM API 的固定实现
- 与 `MedAutoScience` 同成熟度阶段的系统

当前成熟度边界：

- 已有最小 runtime baseline，可支撑 `NSFCWorkspace` 冻结契约下的基本闭环验证
- 仍处于 `baseline freeze / runtime hardening` 阶段
- future managed web runtime 仍是同一 substrate 上的后续演进目标，不是已完成形态

人类操作者负责：

- 冻结 north star、阶段顺序和产品边界
- 决定是否切 program、切 phase、或改变 domain 方向
- 在高判断密度节点做最终验收

Agent 负责：

- 读取结构化状态
- 规划 grant-writing loop
- 调用工具、生成中间工件、维护 audit trail
- 在冻结边界内持续推进闭环

平台/runtime 层负责：

- 提供稳定对象模型、controller、tool surface 与 gate 规则
- 在当前阶段承载 `Codex-default host-agent runtime` 的执行稳定性
- 为后续 managed web runtime 预留同构 contract
- 保证 durable artifact、report 和 validation surface 的一致性

## Architecture Priorities

- 默认采用 `Agent-first`，而不是 `fixed-code-first`。
- `Agent-first` 不等于必须走某一种外部 API；`Codex-default host-agent runtime` 是当前正式默认执行形态。
- 未来 managed web runtime 必须复用同一 `Unified Harness Engineering Substrate` contract，不允许分叉成第二套 domain runtime。
- 当前 repo 主线按 `Auto-only` 理解；未来 `Human-in-the-loop` 产品应作为兼容 sibling 或 upper-layer product 复用同一 substrate，不允许在当前仓里强行演化成同仓双模系统。
- `Grant Ops` 保持 author-side、proposal-facing 边界，不折叠进 `Research Ops`，也不伪装成 reviewer-owned surface。
- 第一阶段先做医学 `NSFC` 通用骨架，不提前把系统锁死在单一项目类型细枝末节上。
- 代码负责 contract、validation、audit、persistence、gate 和 host bridge，不负责重新抢回高层创作主导权。
- 当前执行优先级固定为：先做成熟本地 `CLI-first + host-agent` runtime，再做 hostedization prep；second-family / federation 扩张后置。

## Runtime And Control-Plane Boundary

- `Codex App <-> OMX` 协作属于开发控制面（planning、orchestration、report 回写），不是产品 runtime 本体。
- 产品 runtime 指 `Med Auto Grant` domain harness 在 shared substrate 上执行 grant loop 的运行面。
- 不能把“控制面可用”误写成“产品 runtime 已成熟”；两者的成熟度与验收标准必须分开表述。
- 后续迁移到 managed web runtime 时，控制面形态可以变化，但 domain contract 与 substrate 约束不应漂移。

## Execution Handle And Durable Surface Boundary

- `grant_run_id`
  - 单次 hydrated grant run 的正式执行句柄
  - CLI 输出、runtime report 与恢复上下文都必须回显同一个 `grant_run_id`
- `workspace_id`
  - `NSFCWorkspace` 聚合根身份
  - 回答“这是哪个 grant workspace”，不是“这是哪一次执行”
- `draft_id`
  - `ApplicationDraft` 身份
  - revision 完成后继续沿用同一 `draft_id`，不借由 run handle 生成新草稿身份
- `program_id`
  - control-plane / report-routing 身份
  - 用于 `.omx/reports/<program_id>/` 与 active mainline pointer
- 当前 repo-verified durable report / audit surface：
  - `summarize-workspace`
  - `critique-summary`
  - `stage-route-report`
- `stage-route-report` 当前必须输出 `verification_checkpoint`，把 validation、route recommendation、reviewed revision evidence、forced rollback 与 presubmission gate 聚合到同一个 machine-readable checkpoint surface。
- `validate-workspace` 是验证 surface，不是 execution handle，也不是 control-plane pointer。
- 不得把 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 互相替代，也不得把本地 handoff surface 误写成产品 runtime formal entry。

## Stability Rules

- 当前唯一 active mainline 由 `.omx/context/CURRENT_PROGRAM.md` 定义。
- phase 顺序、north star 与 tranche 切换必须先写入 `CURRENT_PROGRAM.md`、对应 `PRD / test-spec / implementation`，再交给 OMX 连续执行。
- 允许在 `main` 上做小而可回退的直接改动；跨阶段或高耦合重构必须先冻结到主线文档。
- 不依赖旧 terminal、旧 team pane、或一次性长提示词作为唯一状态来源；恢复必须从 `.omx/context` 与 `.omx/reports` 开始。

## Documentation Layers

对外公开、给人看的文档保持中英双语：

- `README*`
- `docs/README*`
- `docs/domain-positioning*`
- `docs/mvp-scope*`

内部开发、计划、备忘、实现细节默认只保留中文：

- `docs/documentation-governance.md`
- `docs/domain-harness-os-positioning.md`
- `docs/specs/**`
- `docs/plans/**`
- `.omx/context/**`
- `.omx/plans/**`
- `.omx/reports/**`

不应无边界扩大双语范围。
中文内部文档优先使用完整中文叙述；英文仅保留给固定术语、路径、命令、schema 与代码标识符，避免无意义中英混写。

## Host Collaboration Model

`Codex App` 与 `OMX` 的协作采用固定分工：

- `Codex App`：规划、冻结真相文档、阶段验收、集成判断、冲突裁决
- `OMX`：长时间连续执行、team lane 拆分、验证、report 回写、断点恢复

两者之间的 durable handoff 机制固定为：

1. `contracts/project-truth/AGENTS.md`
2. `.omx/context/CURRENT_PROGRAM.md`
3. `.omx/context/OMX_TEAM_PROMPT.md`
4. `.omx/plans/spec-program-operating-model.md`
5. `.omx/plans/prd-*.md`
6. `.omx/plans/test-spec-*.md`
7. `.omx/plans/implementation-*.md`
8. `.omx/reports/<program-id>/{LATEST_STATUS,ITERATION_LOG,OPEN_ISSUES}.md`

如果这些表面没有同步，就不应假设 `OMX` 与 `Codex App` 对当前 program 的理解一致。

## Data And State Mutation

- 所有重要状态都应先读后写，不允许盲写。
- workspace、schema、stage route、critique/revision artifact 必须走显式结构对象，不允许靠隐式 prompt 文本漂移。
- critique、revision、draft、question、direction 之间的关联必须由稳定 ID 绑定。
- 对逻辑硬伤、缺失引用、gate 不满足的情况，优先显式失败，不做静默纠偏。
- `.omx/reports/**` 是当前 active program 的 durable 运行状态面；不是一次性聊天记录。

## Review Surface

人类优先 review：

- `docs/specs/**`
- `.omx/context/**`
- `.omx/plans/**`
- 关键 grant artifact、critique、revision 与出口包

OMX 持续写回：

- `.omx/reports/**`
- 与当前 tranche 直接相关的实现、测试和验证痕迹

## Domain-Specific Direction

长期 north star：

- 把 `Med Auto Grant` 推进成医学 `Grant Ops` 的长期主线
- 先在 `NSFC` 通用骨架上跑通从输入接入到批注修订闭环
- 再把 evidence augmentation、verification surface、future `Human-in-the-loop` sibling / upper-layer product compatibility、submission-grade surface、federation 依次收进同一基座

当前执行优先级 ladder：

1. `R1 / Autonomous Main Loop`
2. `R2 / Artifact Production Surface`
3. `R3 / Critique Revision Autoloop`
4. `R4 / Finalization And Export Surface`
5. `R5 / Hostedization Prep`

这条 `R1 -> R5` ladder 是当前 active execution priority，不替换上面的 `P1 -> P5` domain maturity order。
在 `R4` 之前，不应把 second-family onboarding、federation contract、web runtime 或平台托管化写成当前主要开发目标。
当前 repo-tracked internal program 文档固定为：
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
当前 repo-tracked future boundary map 固定为：
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`
当前已精确冻结的 runtime continuation docs 固定为：
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-r3a-critique-revision-executor-surface-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md`

当前固定阶段顺序：

1. `P1 / Reality Convergence And NSFC Baseline Freeze`
2. `P2 / NSFC Authoring Mainline Freeze`
3. `P3 / Mentor Critique And Revision Loop Hardening`
4. `P4 / Verification Surface And HITL Layering Preparation`
5. `P5 / Grant Ops Gateway Expansion And Federation`

除非 `CURRENT_PROGRAM.md` 和主线计划一起更新，否则不允许私自改 phase 顺序。

## Conflict Handling

- User instructions override this file.
- Deeper `AGENTS.md` files override this file for narrower scopes.
- OMX or Codex host orchestration rules govern how work executes.
- This file governs what project-specific truth and boundaries must be preserved.
