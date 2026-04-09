# Med Auto Grant 顶层设计

> 当前文档面向内部设计收敛，只保留中文版本。

Date: `2026-04-06`

## 命名冻结

- 顶层线名：`Grant Foundry`
- 医学首实现名：`Med Auto Grant`
- 代码标识：`MedAutoGrant`
- repo slug：`med-autogrant`

## 文档语言范围

- 对外公开、给人看的文档：保持中英双语
- 内部开发、计划、备忘、实现细节：默认只保留中文

双语范围不应无限扩大。

## 角色定位

`Med Auto Grant` 是 `Grant Foundry` 在医学场景下的首个 repo-native active mainline，也是当前医学 `Grant Ops` 的 domain gateway 与 harness baseline。

在 `OPL` 语义里，它当前仍不应被误写成成熟、submission-grade 的 admitted domain runtime；
但这不等于它还是尚未开始的 future surface。更准确的表述是：

- 它已经是当前医学 `Grant Ops` 的 repo-native mainline
- 它已有最小 runtime baseline
- 它仍处于 `baseline freeze / runtime hardening`

当前阶段的仓库角色是：

- current truth 先行
- 契约先行
- 最小可验证基座先行

而不是立刻承诺成熟 runtime。

## 当前执行优先级

当前最优先的不是继续往 second family、federation 或托管平台扩张，而是先把本地产品 runtime 做成熟。

固定顺序是：

1. 先做成熟本地 `CLI-first + host-agent` runtime
2. 再做 finalization / export surface
3. 然后才做 hostedization prep
4. second-family / federation expansion 后置

当前内部 program 采用的 ladder 见：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`

当前已精确冻结的 continuation docs 为：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-r3a-critique-revision-executor-surface-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md`

## 边界

`Med Auto Grant` 负责的是作者侧、proposal-facing 的基金申请闭环，重点不是“自动补齐一个申请书模板”，而是围绕科学问题、论证链条与申请人适配度组织整个 grant-writing loop。

它覆盖的核心对象包括：

- 申请人画像
- 前期基础与代表性成果
- 在研项目与可复用证据
- 预实验与待补证据
- 方向候选
- 科学问题
- 立项依据与必要性链条
- 申请书草稿包
- 导师批注 / 模拟评审
- 修订计划

它不应被写成：

- `Research Ops` 的论文写作分支
- reviewer-owned surface
- 只会补模板和润色句子的文本生成器

## 核心方法论

### 1. Agent-first

`Med Auto Grant` 默认应按 `Agent-first` 设计，而不是按固定代码流水线设计。

这里的含义不是“必须直接调用某一种模型 API”，而是：

- Agent 负责读状态、规划步骤、调用工具、组织中间产物与审计痕迹
- 代码负责提供稳定对象模型、controller、tool surface、gate 规则与交付接口
- domain 能力应围绕可编排的 agent runtime 展开，而不是围绕硬编码流程分支展开

### 2. 产品分层复用

当前 repo-tracked 主线按 `Auto-only` 理解：

- 当前仓先把全自动 author-side 主线做成熟，用于端到端闭环、基座测试、评估与优化
- 未来若要做高判断密度 `Human-in-the-loop` 产品，应作为兼容 sibling 或 upper-layer product 复用同一 substrate 与执行模块

也就是说：

- 当前仓不做同仓双模
- 当前仓的首要任务是把 `CLI-first + host-agent` 本地 runtime 做成熟
- 未来的人在回路产品，应复用这条自动主线的对象、执行、audit 与 artifact 基座，而不是在当前仓里把判断逻辑强行混成一套

## 与 Research Ops 的关系

`Med Auto Grant` 与 `Research Ops -> Med Auto Science` 会共享大量输入与底层能力，但边界不能折叠：

- 可共享：申请人画像、论文与成果、实验记录、预实验、领域记忆、审计与治理语言
- 不可折叠：基金方向选择、科学问题提纯、立项依据、申请人-问题适配度判断、申请书结构化交付、作者侧模拟评审与修订闭环

简言之，`Research Ops` 更偏“研究执行与论文交付”，`Grant Ops` 更偏“问题定义、论证打磨与正式申请书交付”。

## MVP 范围

第一阶段 MVP 先做医学场景下的 `NSFC` 通用骨架，不先绑定单一项目类型。

这样做的理由是：

- 青年项目与面上项目在核心科学问题提炼上高度相通
- 先冻结通用对象模型与评审语言，更利于后续扩展到不同项目类型
- 先避免为某个项目类别过早抽象出大量模板特化逻辑

### MVP 输入

- 申请人简历 / 学术画像
- 已有代表性成果
- 正在进行的项目与可复用材料
- 预实验结果或预实验缺口
- 目标申请方向与候选主题
- 国自然申请要求与章节框架

### MVP 输出

- 方向候选与收敛建议
- 凝练后的科学问题表述
- 必要性 / 科学价值论证链
- 申请人与课题的适配度说明
- 申请书关键章节草稿
- “导师批注”式诊断
- 修订计划与差距清单

## MVP 评审内核

第一版评审内核先按下列权重冻结：

- `60%` 必要性与科学价值：科学问题是否成立
- `30%` 胜任力与独特性：为什么应由该申请人来做
- `10%` 可行性：技术路线是否逻辑通顺

MVP 必须严格区分：

- 真正的科学问题
- 工程任务
- 临床需求

也就是说，MVP 不能停留在：

- 做一个系统
- 提高准确率
- 解决某个实际难题

而必须逼近：

- 现有知识边界在哪里
- 未知机制或关键缺口是什么
- 本项目拟用什么视角或方法突破这个边界

## 下一步

- 把本地 `CLI-first + host-agent` runtime 做成熟，先收通连续主循环
- 把 artifact production、critique / revision autoloop、finalization / export 接成真正产品 runtime
- 在本地 runtime 成熟后，再做 hostedization prep
