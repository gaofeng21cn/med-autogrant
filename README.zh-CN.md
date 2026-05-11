<p align="center">
  <img src="assets/branding/medautogrant-logo.svg" alt="Med Auto Grant Logo" width="132" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**通过单一 Med Auto Grant 技能入口推进医学基金写作的独立领域智能体**

> `Med Auto Grant` 面向医学基金申请写作。它把指定基金任务的正文写作、评审式批注、修订和待审包交付放在同一条申请线上，方便医生、课题负责人和科研团队持续推进。

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
- “在不改目标基金的前提下，按主张和证据的缺口审稿，并直接改掉正文薄弱段落。”
- “按评审视角审一遍这份草稿，指出最影响中标的硬伤，并直接给我一版修改建议。”

## 适合处理的工作

- 在指定基金任务下，把既有论文、预实验和个人基础收成更清楚的标题、摘要、研究内容和技术路线。
- 在同一工作区里持续跟踪批注、修订轮次和版本变化。
- 用结构化评分卡、版本差异和证据缺口报告比较申请书质量。
- 运行较长的自动写作周期，按质量门槛判断继续、回退或带阻塞原因停止。
- 先交付科学上可审阅的申请书包，再进入门户提交前的形式和客观材料补件。
- 把形式/客观补件作为显式 `TODO + 唤醒` 队列管理，默认不阻塞正文 authoring。

## 工作方式

- 申请人提供目标基金任务、已有材料、限制条件和最终判断。
- AI 助手负责该任务内的科学结构整理、正文草拟、批注整合和修订推进。
- 工作区持续保存版本、评审意见和交付文件，方便回看与比较。
- 新建材料接收工作区采用目录结构：`workspace.json` 是权威工作区文件，轻量合同和产物可以被 Git 跟踪，本地运行输出保持忽略。

## 当前边界

- `Med Auto Grant` 是独立的医学基金领域智能体，不是 `OPL` 仓库里的内部模块。
- 对外第一入口是单一 `Med Auto Grant` 技能；`Codex`、`OPL` 和其他通用智能体可以通过这个入口，或直接通过 `CLI` / `MedAutoGrantDomainEntry` 访问稳定能力面。
- 这个技能背后的稳定可调用面是本地 CLI、`MedAutoGrantDomainEntry`、本地脚本、产品入口/投影命令与 schema-backed 合同。
- `product entry/product status/direct-entry/user-loop` 保持为技能下的内部命令合同与直接产品投影，不写成对外第一主语。
- MAG 当前任务边界锁定在“指定基金任务正文写作”。
- “科学完成”交付面是可待审包；“形式/客观补件完成”是并行分层，不与正文语义混写。
- 形式/客观补件默认按 `TODO + 显式唤醒` 处理，除非直接破坏正文科学成立，否则不升级为正文阻塞项。
- `OPL` 是 Codex-first、stage-led 的完整智能体运行框架，MAG 可以作为外部领域依赖接入。
- 在这套框架中，`Codex CLI` 是最小执行单元；OPL 可以提供阶段调度、唤醒、队列、交接、回执、重试和投影支撑，但 MAG 继续持有基金阶段包、提示、技能、可资助性/写作质量门槛、正文真相和可提交包导出权威。
- 旧 `OPL Runtime Manager`、Temporal、Hermes-first、gateway 和本地 host runtime 表述只作为历史追溯或实现 provider 细节保留，除非新的活跃合同显式提升它们。
- `hosted-contract-bundle` 与 `runtime_control` 仅保留集成/参考面，用于 machine-readable handoff，不作为默认公开入口。
- 人工 gate 仅限同一基金任务内的作者决策，不写成跨基金重选。
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
- 当前 formal-entry matrix 是 `CLI`、`MCP` 和 `controller`。`CLI` / `MedAutoGrantDomainEntry` 是 agent entry；`product entry/product status/direct-entry/user-loop`、本地脚本与 schema-backed contract 共同构成 app skill 下的内部 command contract 和 direct-product projection。hosted / proof backend 只在显式 opt-in 集成 lane 中出现，不构成默认公开合同。
- MAG 可以通过 Codex app skill 直接调用，也可以通过 OPL 托管调用。两条路径必须回到同一套 MAG-owned route、quality、workspace 和 export surface。
- 如果外部 agent 或 OPL 需要直接读取 repo-tracked skill surface，用 repo-local launcher：`uv run --directory <med-autogrant-repo> medautogrant product skill-catalog --input <input_path> --format json`；返回的是一个 Med Auto Grant app skill 加底层 command contracts。
- pre-authoring intake 用 `uv run --directory <med-autogrant-repo> medautogrant workspace initialize-intake --input <selection_input> --workspace-root <workspace_dir> --format json`；目录会带 workspace-local Git boundary，`workspace.json` 是 MAG canonical document。
- 当前单一 skill descriptor 已携带可直接消费的 `runtime_continuity` envelope，并复用既有 `session_continuity` / `progress_projection` / `artifact_inventory` / `runtime_control` truth。
- 当前可机读治理面包括 `workspace quality-scorecard`、`workspace quality-diff` 和 `pass autonomy-controller`。

</details>

## 维护者验证

- 默认本地门禁使用 `./scripts/verify.sh`，它会运行 line-budget、最小 smoke lane 和非重型 fast core lane。
- 快速入口健康检查使用 `./scripts/verify.sh smoke` 或 `make test-cli-smoke`。
- 矩阵型、product-entry、runtime/session、hosted/export 与兼容性回归使用 `./scripts/verify.sh regression`。Product-entry case 现在直接放在 `tests/product_entry_cases/` 下收集；`tests/test_product_entry.py` 只保留兼容导入面。
- repo 治理、结构检查和 clean-clone/full-suite 基线分别使用 `./scripts/verify.sh meta`、`./scripts/verify.sh structure` 与 `./scripts/verify.sh full`。

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
