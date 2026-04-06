[English](./domain-positioning.md) | **中文**

# Med Auto Grant Domain Positioning

## 它是什么

`Med Auto Grant` 是 `Grant Foundry` 在医学场景下的未来实现 repo scaffold。
它的目标角色是面向申请人侧、proposal-facing 的医学 `Grant Ops` domain gateway 与 harness。

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
- 在同一套共享基座上支持两种模式：
  - `Auto`
  - `Human-in-the-loop`

## 当前公开面状态

当前状态：

- repo scaffold 已建立
- 顶层公开文档已建立
- 中文内部设计与计划文档已建立
- runtime 实现暂缓到 MVP schema 与执行主线进一步冻结后再推进

