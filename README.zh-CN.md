<p align="center">
  <img src="assets/branding/medautogrant-logo.svg" alt="Med Auto Grant Logo" width="132" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**通过单一 Med Auto Grant app skill 暴露的独立医学基金 domain agent**

> `Med Auto Grant` 是独立的医学基金领域 agent。它把“指定基金任务的正文写作、批注、修订和科学待审包交付”放在同一条申请线上，方便持续推进和审阅。

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>适用人群</strong><br/>
      准备申请人侧医学基金的医生、课题负责人、青年教师、医学研究者和临床团队
    </td>
    <td width="33%" valign="top">
      <strong>适用问题</strong><br/>
      指定基金任务已确定，希望把正文草稿、批注、版本与待审包放在同一个工作区里
    </td>
    <td width="33%" valign="top">
      <strong>如何开始</strong><br/>
      直接说明目标基金、当前草稿与材料、要支撑的科学主张，以及希望形成的待审包
    </td>
  </tr>
</table>

## 一句话快速启动

你可以直接这样说：

- “按这个国自然项目和我当前草稿，重写标题、摘要、研究内容和方法，保证科学叙事自洽。”
- “在不改目标基金的前提下，按 claim-evidence 缺口审稿并直接改掉正文薄弱段落。”
- “按评审视角审一遍这份草稿，指出最影响中标的硬伤，并直接给我一版修改建议。”

## 适合处理的工作

- 在指定基金任务下，把既有论文、预实验和个人基础收成更清楚的标题、摘要、研究内容和技术路线。
- 在同一工作区里持续跟踪批注、修订轮次和版本变化。
- 用结构化 scorecard、版本差异和证据缺口报告比较申请书质量。
- 运行更长的 controller-led 写作周期，按质量 gate 判断继续、回退或带 blocker 停止。
- 先交付“科学完成”的可待审包，再进入门户提交前的形式/客观补件。
- 把形式/客观补件作为显式 `TODO + 唤醒` 队列管理，默认不阻塞正文 authoring。

## 工作方式

- 申请人提供目标基金任务、已有材料、限制条件和最终判断。
- AI 助手负责该任务内的科学结构整理、正文草拟、批注整合和修订推进。
- 工作区持续保存版本、评审意见和交付文件，方便回看与比较。

## 当前边界

- `Med Auto Grant` 是独立的医学基金 domain agent，不是 `OPL` 内部工作区模块。
- 对外第一主语是单一 `Med Auto Grant` app skill；`Codex`、`OPL` 和其他通用 agent 可以通过这个 skill 入口，或直接通过 `CLI` / `MedAutoGrantDomainEntry` 访问稳定能力面。
- 这个 app skill 背后的稳定可调用面是本地 CLI、`MedAutoGrantDomainEntry`、本地脚本、product-entry/projection commands 与 schema-backed contract。
- `product entry/frontdesk/direct-entry/user-loop` 保持为 app skill 下的内部 command contract 与 direct-product projection，不再写成对外第一主语。
- MAG 当前任务边界锁定在“指定基金任务正文 authoring”。
- “科学完成”交付面是可待审包；“形式/客观补件完成”是并行分层，不与正文语义混写。
- 形式/客观补件默认按 `TODO + 显式唤醒` 处理，除非直接破坏正文科学成立，否则不升级为正文 blocker。
- `OPL` 只保留 family-level 的 session/runtime/projection 与 shared modules/contracts/indexes。
- `hosted-contract-bundle` 与 `runtime_control` 仅保留集成/参考面，用于 machine-readable handoff，不作为默认公开入口。
- 人工 gate 仅限同一基金任务内的作者决策，不写成跨 funder 重选。
- 外部基金官网提交由人工监督完成。

## 这个仓库应该怎么读

1. 潜在用户先读当前首页，再继续看 [文档索引](./docs/README.zh-CN.md)、[领域定位](./docs/domain-positioning.zh-CN.md) 和 [最小可用范围](./docs/mvp-scope.zh-CN.md)。
2. 技术规划、架构判断和方向同步，继续读 [项目概览](./docs/project.md)、[当前状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md)、[决策记录](./docs/decisions.md) 以及 [合同说明](./contracts/README.md)。
3. 开发者和维护者再进入 `docs/specs/`、`docs/references/`、`docs/plans/` 与 [历史归档索引](./docs/history/README.zh-CN.md)。

## 给 Agent 和技术操作者的快速入口

<details>
  <summary><strong>如果你准备把这个仓直接交给 Codex 或其他 Agent，先看这里</strong></summary>

- 先读 [文档索引](./docs/README.zh-CN.md)。这里已经把当前技术全景、formal-entry matrix、稳定 capability surface 和 repo-tracked 真相所在位置收口好了。
- 然后读 [合同说明](./contracts/README.md) 和 [`contracts/runtime-program/current-program.json`](./contracts/runtime-program/current-program.json)。这是恢复 active product-entry shell、schema-backed surface 和当前 mainline 指针的最快路径。
- 在改 route、入口 wording 或公开表述前，把 [项目概览](./docs/project.md)、[当前状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md) 和 [决策记录](./docs/decisions.md) 当成公开与技术真相集。
- 当前 formal-entry matrix 是 `CLI`、`MCP` 和 `controller`。`CLI` / `MedAutoGrantDomainEntry` 是 agent entry；`product entry/frontdesk/direct-entry/user-loop`、本地脚本与 schema-backed contract 共同构成 app skill 下的内部 command contract 和 direct-product projection。hosted / proof backend 只在显式 opt-in 集成 lane 中出现，不构成默认公开合同。
- 如果外部 agent 或 OPL 需要直接读取 repo-tracked skill surface，用 `medautogrant product skill-catalog --input <input_path> --format json`；返回的是一个 Med Auto Grant app skill 加底层 command contracts。
- 当前单一 skill descriptor 已携带可直接消费的 `runtime_continuity` envelope，并复用既有 `session_continuity` / `progress_projection` / `artifact_inventory` / `runtime_control` truth。
- 当前可机读治理面包括 `workspace quality-scorecard`、`workspace quality-diff` 和 `pass autonomy-controller`。

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
