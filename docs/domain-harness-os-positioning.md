# Med Auto Grant 在 Unified Harness Engineering Substrate 中的 Domain Harness OS 定位（内部）

## 1. 项目位置：Shared Substrate 上的医学 Domain Harness OS

`Med Auto Grant` 的定位不是“独立平台”，而是共享 `Unified Harness Engineering Substrate` 之上的医学 `Grant Ops` `Domain Harness OS` 方向/系统。

它承担的是医学基金申请（author-side、proposal-facing）场景下的 domain harness 职责，包括：

- 领域对象与状态契约（workspace、stage route、critique/revision artifact）
- 领域 gate 与 runtime 约束
- 面向 agent 的可审计执行闭环

它不承担“重新定义 substrate”或“另起一套基础 runtime”的职责。

## 2. 共享约束：必须继承的 Substrate Contract

在该共享 substrate 上，`Med Auto Grant` 需要保持以下不变约束：

- 对象模型、controller、tool surface、gate 规则走显式结构契约，不依赖隐式 prompt 漂移
- 关键状态先读后写，跨阶段迁移遵循冻结顺序与审计轨迹
- 当前 repo 主线按 `Auto-only` 理解；未来 `Human-in-the-loop` 产品应作为兼容 sibling 或 upper-layer product 复用同一 substrate，而不是把当前仓改成同仓双模
- durable artifact、validation surface、report 语义保持一致，避免不同执行形态下语义漂移

## 3. Domain-Specific Contract：医学 Grant Ops 边界

本项目的 domain contract 固定在医学 `Grant Ops`，并保持以下边界：

- 申请人侧（author-side）、proposal-facing
- 优先围绕 `NSFC` 通用骨架推进
- 目标是“问题提纯 -> 论证链收敛 -> 导师式批注 -> 修订闭环”的可治理流程

明确不做：

- reviewer-owned surface
- `Research Ops` 论文写作主线
- 仅模板填充或措辞润色工具

## 4. 当前默认 Runtime 形态

当前默认本地执行形态是 `Codex-default host-agent runtime`。

当前 formal-entry matrix 固定为：

- `default_formal_entry`：`CLI`
- `supported_protocol_layer`：`MCP`（当前保留为 future layer，尚未 repo-verified）
- `internal_controller_surface`：`controller`

该形态下，项目已有最小 runtime baseline，可覆盖以下基线能力：

- 冻结 `NSFCWorkspace` 契约下的结构化校验
- 基于 `lifecycle_stage` 与 gate 的下一步建议
- critique/revision 路由中的关键一致性检查与显式失败
- 基础 machine-readable 路由与批注摘要输出

这意味着“最小 baseline 已存在”，不意味着“完整产品 runtime 已完成”。

## 4.1 执行句柄与 durable surface 边界

为了和 shared substrate 上其他业务仓逐步对齐，这里需要把当前已经存在的身份与表面合同写得更明确：

- `grant_run_id`
  - 单次 hydrated grant run 的执行句柄
  - 当前 CLI 输出、runtime report 与恢复上下文都必须显式回显它
- `workspace_id`
  - `NSFCWorkspace` 聚合根身份
  - 不得被误写成 run handle 或 report-routing pointer
- `draft_id`
  - `ApplicationDraft` 的持久身份
  - critique / revision / re-review 都围绕同一 `draft_id` 绑定，不在每轮 run 中漂移
- `program_id`
  - control-plane 与 report-routing 身份
  - 负责 `.runtime-program/reports/<program_id>/` 与 active mainline 指针

当前 repo-verified durable report / audit surfaces 也已经明确为：

- `summarize-workspace`
- `critique-summary`
- `stage-route-report`

其中 `stage-route-report` 当前还是 canonical verification / checkpoint 聚合面，必须稳定输出：

- `verification_checkpoint`
- `checkpoint_status`

而 `validate-workspace` 负责 validation，不应被误写成新的 execution handle 或新的 formal entry。

## 5. 未来托管形态：Managed Web Runtime（同一 Substrate）

未来可演进为 managed web runtime，但该演进应满足以下前提：

- 仍复用同一 `Unified Harness Engineering Substrate` contract
- 不改写既有 domain object、gate 与审计语义
- 仅改变托管与交付形态，不把控制面描述成产品 runtime 完成度

换言之，未来托管形态是“同构迁移”，不是“另起炉灶”。

## 6. 当前成熟度边界（克制表述）

当前阶段应统一表述为：

- 已有最小 runtime baseline
- 正在 `baseline freeze / runtime hardening`
- 未完成端到端 submission-grade authoring runtime

成熟度比较边界：

- 当前不应表述为与 `MedAutoScience` 同成熟度
- 两个项目可共享 substrate，但阶段目标、runtime 完整度与验证深度不同

对外或对内文档若出现“已完成托管 runtime”“已达 submission-grade 自动驾驶”等表述，应视为超前叙述并回退到上述边界。
