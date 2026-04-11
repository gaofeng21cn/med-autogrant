[English](./domain-positioning.md) | **中文**

# Med Auto Grant Domain Positioning

## 它是什么

`Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向申请人侧且 proposal-facing 的医学 `Grant Ops` 主线。
它的角色是医学 `Grant Ops` 的 domain gateway 与 harness，当前产品 runtime 主线已经冻结为 `CLI-first + Hermes-backed runtime`。
此前已 absorbed 的 `Codex-default host-agent` 线现在只保留为 migration 期间的 compatibility bridge / regression oracle。

## 它不是什么

`Med Auto Grant` 不是：

- `Research Ops` 的论文写作分支
- reviewer-owned 的基金评审 surface
- 只会填章节的模板补全器
- 已经完成全部 runtime 实现的证明

## 边界

它的核心边界是医学场景下申请人侧的基金写作闭环：

- 申请人画像与履历
- 可复用项目证据与预实验
- 方向与题目收敛
- 科学问题提纯
- 论证链构建
- 申请书草稿生成
- 导师式批注与修订规划

## 与 Research Ops 的关系

`Med Auto Grant` 预期会复用大量来自医学 `Research Ops` 的上游资产，例如：

- 论文与既有交付物
- 项目证据
- 预实验结果
- 文献记忆
- 审计与治理语言

但它仍保持独立边界，因为基金申请并不等于研究执行，也不等于论文投稿。

## 执行原则

仓库当前遵循两条共享架构原则：

- 默认采用 `Agent-first`，而不是 `fixed-code-first`
- 当前仓库主线按 `Auto-only` 理解
- 未来 `Human-in-the-loop` 产品应作为兼容 sibling 或 upper-layer product 复用同一 substrate，而不是把当前仓改成同仓双模

其 formal-entry matrix 为：

- `default_formal_entry`：`CLI`
- `supported_protocol_layer`：`MCP`（当前保留为 future layer，尚未 repo-verified）
- `internal_controller_surface`：`controller`

## 当前公开面状态

当前状态：

- 顶层公开文档已建立
- 中文内部设计与 current-truth 文档已建立
- 最小 runtime baseline 已存在
- 当前仓库正在执行 `Hermes Runtime Substrate Program`；旧的 `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP` 只作为 host-agent 历史基线保留，而不是当前产品 runtime 主线
- future managed web runtime 只是同一 substrate 上的后续部署演进，不代表项目仍停留在前置筹备期
