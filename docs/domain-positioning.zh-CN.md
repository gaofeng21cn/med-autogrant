[English](./domain-positioning.md) | **中文**

# Med Auto Grant Domain Positioning

## 它是什么

`Med Auto Grant` 是独立的、面向申请人侧且 proposal-facing 的医学 `Grant Ops` domain agent。
对外第一主语是单一 `Med Auto Grant` app skill。在这个 skill 下面，`CLI` / `MedAutoGrantDomainEntry` 提供稳定 agent entry，product-entry / direct-entry / projection surfaces 继续作为医学基金申请的内部 command contract。当前公开 capability contract 冻结为 `CLI/domain-entry stable capability surface + Codex-default execution + explicit hosted runtime carriers`。
MAG 可以复用 family-level harness contract 与 OPL 侧 runtime-management 约定，但 OPL 不持有 MAG grant truth、authoring execution 或 submission-ready export gate。

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
- `supported_protocol_layer`：`MCP`
- `internal_controller_surface`：`controller`
- `CLI` / `MedAutoGrantDomainEntry`：agent entry
- `product entry/frontdesk/direct-entry/user-loop`：单一 app skill 下的内部 command contract / direct-product projection

## 当前公开面状态

当前状态：

- 顶层公开文档已建立
- 中文内部设计与 current-truth 文档已建立
- 默认 Codex 执行 + 稳定 capability surface 已落地
- 对外第一身份已收口为独立 medical grant domain agent（可 direct，也可被 `OPL` federate）
- product-entry、frontdesk、direct-entry、user-loop 继续位于 app skill 之下，不作为对外第一主语
- 当前活跃 phase 是 `P4 mature direct grant product entry`
- 当前活跃 tranche 是 `P4.G authoring-quality-first completion semantics alignment`
- `P3 hosted caller / OPL consumption proof` 已经完成，现只作为历史落地上下文保留
- future hosted 产品部署继续作为同一路由/导出合同之上的后续演进
