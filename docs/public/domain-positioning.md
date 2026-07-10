# Med Auto Grant Domain Positioning

Owner: `Med Auto Grant`
Purpose: `public_domain_positioning`
State: `current_public_support`
Machine boundary: 本文是人读公开定位补充。产品与机器真相归核心文档、current-program、root contracts、schemas、source、CLI/API 行为、runtime receipts 与 grant workspace artifacts。

## 它是什么

`Med Auto Grant` 是独立的、面向申请人侧且 proposal-facing 的医学 `Grant Ops` domain agent。
对外第一主语是单一 `Med Auto Grant` app skill。`CLI` / `MedAutoGrantDomainEntry` 与 direct domain handler 提供稳定 agent entry；product/status/user-loop/workbench 由 OPL/App generated surfaces 提供。当前公开 capability contract 是 `CLI/domain-entry stable capability surface + Codex-default execution + explicit hosted runtime carriers`。
MAG 可以作为 OPL stage-led framework 中的外部 domain agent 被发现、托管、唤醒和投影，但 OPL 不持有 MAG grant truth、authoring execution 或 submission-ready export gate。

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

仓库当前遵循三条共享架构原则：

- 默认采用 `Agent-first`，而不是 `fixed-code-first`
- 当前仓库主线按 `Auto-only` 理解
- 未来 `Human-in-the-loop` 产品应作为兼容 sibling 或 upper-layer product 复用同一 substrate，而不是把当前仓改成同仓双模

其 formal-entry matrix 为：

- `default_formal_entry`：`CLI`
- `supported_protocol_layer`：`MCP`
- `CLI` / `MedAutoGrantDomainEntry`：agent entry
- `product/status/direct-entry/user-loop/workbench`：OPL/App generated surface，回调 MAG grant-native handler

## 当前公开面状态

当前状态：

- 顶层公开文档已建立
- 中文内部设计与 current-truth 文档已建立
- 默认 Codex 执行 + 稳定 capability surface 已落地
- 对外第一身份已收口为独立 medical grant domain agent（可 direct，也可被 `OPL` 托管、唤醒和投影）
- product/status/direct-entry/user-loop/workbench 位于 app skill 与 OPL generated caller 之下，不作为 MAG 私有 runtime
- 当前阶段、活跃 tranche、open evidence gate 与执行顺序以 `docs/status.md` 和 `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 为准；本文不冻结易漂移阶段标签。
- 旧 hosted caller / OPL consumption proof 只作为历史落地上下文保留；当前外部 OPL/App/production caller 消费、direct/hosted parity 和 long-soak 仍按 active evidence gate 处理
- future hosted 产品部署继续作为同一路由/导出合同之上的后续演进
