<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**面向申请人侧医学基金申请的独立 domain agent，用来持续推进题目、结构和正式申请稿**

> `Med Auto Grant` 是独立的医学基金领域 agent。它把选题、既有成果、预实验、草稿、批注、修订和本地提交准备放在同一条申请线上，方便持续推进和审阅。

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>适用人群</strong><br/>
      准备申请人侧医学基金的医生、课题负责人、青年教师、医学研究者和临床团队
    </td>
    <td width="33%" valign="top">
      <strong>适用问题</strong><br/>
      方向很多、材料不少、修改轮次也多，希望把题目、草稿、批注和版本收在同一个工作区里
    </td>
    <td width="33%" valign="top">
      <strong>如何开始</strong><br/>
      直接说明准备申请的项目、题目方向、已有成果、预实验和希望形成的申请包
    </td>
  </tr>
</table>

## 一句话快速启动

你可以直接这样说：

- “帮我把这个方向整理成一份国自然申请，先判断题目值不值得做，再给我标题、摘要和研究内容框架。”
- “根据我现有论文、预实验和个人基础，帮我筛三个最值得写的申请方向，并说明各自的创新点和风险。”
- “按评审视角审一遍这份草稿，指出最影响中标的硬伤，并直接给我一版修改建议。”

## 适合处理的工作

- 从多个方向里筛出值得正式写作的申请题目。
- 把既有论文、预实验和个人基础收成更清楚的标题、摘要、研究内容和技术路线。
- 在同一工作区里持续跟踪批注、修订轮次和版本变化。
- 在终审前整理出更完整的本地申请包，方便团队继续审稿和收口。

## 工作方式

- 申请人提供目标项目、已有材料、限制条件和最终判断。
- AI 助手负责题目提纯、结构整理、正文草拟、批注整合和修订推进。
- 工作区持续保存版本、评审意见和交付文件，方便回看与比较。

## 当前边界

- `Med Auto Grant` 是独立的医学基金 domain agent，不是 `OPL` 内部工作区模块。
- 它可以通过 `CLI` / `MedAutoGrantDomainEntry` 被 `Codex` 或其他通用 agent 直接调用，也可以被 `OPL` 以 federation 方式调用。
- 它负责题目收敛、申请书写作、批注修订和本地提交包准备。
- `OPL` 只保留 family-level 的 session/runtime/projection 与 shared modules/contracts/indexes。
- 最终题目取舍、申报策略和是否正式提交由申请人团队决定。
- 外部基金官网提交由人工监督完成。

## 这个仓库应该怎么读

1. 潜在用户先读当前首页，再继续看 [文档索引](./docs/README.zh-CN.md)、[领域定位](./docs/domain-positioning.zh-CN.md) 和 [最小可用范围](./docs/mvp-scope.zh-CN.md)。
2. 技术规划、架构判断和方向同步，继续读 [项目概览](./docs/project.md)、[当前状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md)、[决策记录](./docs/decisions.md) 以及 [合同说明](./contracts/README.md)。
3. 开发者和维护者再进入 `docs/specs/`、`docs/references/`、`docs/plans/` 与 [历史归档索引](./docs/history/README.zh-CN.md)。

## 给 Agent 和技术操作者的快速入口

<details>
  <summary><strong>如果你准备把这个仓直接交给 Codex 或其他 Agent，先看这里</strong></summary>

- 先读 [文档索引](./docs/README.zh-CN.md)。这里已经把当前技术全景、formal-entry matrix 和 repo-tracked 真相所在位置收口好了。
- 然后读 [合同说明](./contracts/README.md) 和 [`contracts/runtime-program/current-program.json`](./contracts/runtime-program/current-program.json)。这是恢复 active product-entry shell、schema-backed surface 和当前 mainline 指针的最快路径。
- 在改 route、入口 wording 或公开表述前，把 [项目概览](./docs/project.md)、[当前状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md) 和 [决策记录](./docs/decisions.md) 当成公开与技术真相集。
- 当前 formal-entry matrix 是 `CLI`、`MCP` 和 `controller`。`CLI` / `MedAutoGrantDomainEntry` 是 agent entry，`product entry/frontdesk/direct-entry/user-loop` 是 lightweight direct entry / projection shell。

</details>

## 延伸阅读

- [文档索引](./docs/README.zh-CN.md)
- [领域定位](./docs/domain-positioning.zh-CN.md)
- [最小可用范围](./docs/mvp-scope.zh-CN.md)
- [项目概览](./docs/project.md)
- [当前状态](./docs/status.md)
- [架构](./docs/architecture.md)
- [不变量](./docs/invariants.md)
- [决策记录](./docs/decisions.md)
- [合同说明](./contracts/README.md)
