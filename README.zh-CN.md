<p align="center">
  <img src="assets/branding/medautogrant-logo.png" alt="Med Auto Grant Logo" width="132" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

<!--
Owner: Med Auto Grant
Purpose: public repository entry
State: current_public
Machine boundary: Human-readable entry only. Machine truth remains in contracts, schemas, source, CLI/API behavior, product-entry manifest, runtime receipts, and grant workspace artifacts.
-->

# Med Auto Grant

**面向医学基金申请书的 AI 写作工作台 —— 把选题、正文、批注、修订和待审包放在同一条可追踪的申请线上。**

医学基金申请不是简单填模板。一个真正可送审的本子，往往要把目标基金、研究基础、科学问题、技术路线、申请人优势和评审关注点反复对齐。

当 AI 从“一次帮我润色”进入“陪我把一个本子写到能评审”时，几个问题会很快出现：

- 目标基金已经确定，现有论文、预实验和个人基础怎么收成一条清楚的科学故事？
- 改了很多轮后，哪一版解决了什么问题，哪些硬伤还没关掉？
- 能不能像基金评审一样指出薄弱处，并直接推动下一版正文？
- 形式材料、门户补件和正文科学质量能不能分开管理，避免互相拖住？
- 人暂时离开后，长时间写作和修订能否继续推进，并留下可检查的进度和阻塞？

`Med Auto Grant` 正是围绕这些问题设计的。它面向已经明确的基金任务，把材料整理、正文生成、评审式批注、修订回合和待审包交付放在同一个工作区里，让申请书从草稿逐步推进到“可以拿给专家看的版本”。

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

<p align="center">
  <img src="assets/branding/medautogrant-overview-v2.png" alt="Med Auto Grant 主示意图" width="100%" />
</p>

## 核心亮点

**围绕指定基金持续写作**<br/>
它不是泛泛给建议，而是在同一个目标基金下持续整理材料、重写正文、关闭问题和推进版本。

**从材料到待审包**<br/>
已有论文、预实验、个人基础和限制条件会被组织进标题、摘要、研究内容、技术路线和申请人叙事中，最终形成可审阅的申请书包。

**像评审一样发现问题**<br/>
每一轮都能围绕科学问题、必要性、创新性、技术路线、申请人适配和证据缺口给出批注，并把批注转成下一版修改。

**进度和版本可回看**<br/>
工作区保留草稿、批注、版本变化、质量评分和证据缺口，让团队知道当前本子推进到了哪一步。

**正文与补件分层管理**<br/>
门户提交、形式材料和客观补件作为单独待办管理；默认先保证正文科学上成立，再进入提交前补件。

## 一句话快速启动

你可以直接这样说：

- “按这个国自然项目和我当前草稿，重写标题、摘要、研究内容和方法，保证科学叙事自洽。”
- “在不改目标基金的前提下，按主张和证据的缺口审稿，并直接改掉正文薄弱段落。”
- “按评审视角审一遍这份草稿，指出最影响中标的硬伤，并直接给我一版修改建议。”

## 适合处理的工作

- 在指定基金任务下，把既有论文、预实验和个人基础收成更清楚的标题、摘要、研究内容和技术路线。
- 在同一工作区里持续跟踪批注、修订轮次和版本变化。
- 用结构化评分卡、版本差异和证据缺口报告比较申请书质量。
- 运行较长的写作和修订周期，按当前质量判断继续、回退或带阻塞原因停止。
- 先交付科学上可审阅的申请书包，再进入门户提交前的形式和客观材料补件。
- 把形式/客观补件作为显式待办和提醒管理，默认不阻塞正文写作。

## 工作方式

- 申请人提供目标基金任务、已有材料、限制条件和最终判断。
- AI 助手负责该任务内的科学结构整理、正文草拟、批注整合和修订推进。
- 工作区持续保存版本、评审意见和交付文件，方便回看与比较。
- 新建材料接收工作区采用目录结构：`workspace.json` 是权威工作区文件，轻量合同和产物可以被 Git 跟踪，本地运行输出保持忽略。

## 当前边界

- `Med Auto Grant` 是独立的医学基金领域智能体，不是 `OPL` 仓库里的内部模块。
- 公开发布定位：`Foundry Agent / OPL-compatible package built on OPL Framework`。
- 对外第一入口是单一 `Med Auto Grant` 技能；`Codex`、`OPL` 和其他通用智能体可以通过这个入口，或直接通过 `CLI` / `MedAutoGrantDomainEntry` 访问稳定能力面。
- 仓库根层 OPL standard pack 是 OPL generated-interface 的来源；OPL 将该 pack 编译为 generated CLI / MCP / Skill / product-entry / tool descriptors，本地 CLI、`MedAutoGrantDomainEntry`、产品入口/投影命令与 schema-backed 本地脚本/合同仍是这些 descriptor 背后的 MAG-owned action target 和 authority function。
- OPL/Temporal hosted autonomous runtime 是标准 OPL Agent 任务启动后的默认运行驻留；MAG 不实现自己的 daemon、scheduler、attempt loop 或 attempt ledger，`Codex CLI` 继续是默认具体 stage executor。
- `product entry/product status/direct-entry/user-loop` 保持为技能下的内部命令合同与直接产品投影，不写成对外第一主语。
- 统一发布形态由 app skill catalog、MAG-owned stage control plane、hosted-contract-bundle 交接导出和本地 `submission-ready` 交付导出共同组成。
- MAG 当前任务边界锁定在“指定基金任务正文写作”。
- “科学完成”交付面是可待审包；“形式/客观补件完成”是并行分层，不与正文语义混写。
- 形式/客观补件默认按 `TODO + 显式唤醒` 处理，除非直接破坏正文科学成立，否则不升级为正文阻塞项。
- `hosted-contract-bundle` 与 `runtime_control` 仅保留集成/参考面，用于 machine-readable handoff，不作为默认公开入口。
- 人工 gate 仅限同一基金任务内的作者决策，不写成跨基金重选。
- 外部基金官网提交由人工监督完成。

<details>
  <summary><strong>技术层 OPL / executor 边界</strong></summary>

- `OPL` 是 stage-led 的完整智能体运行框架，MAG 可以作为外部领域依赖接入。
- 在这套框架中，Agent executor 是最小执行单位；`Codex CLI` 是当前第一公民 executor。Hermes-Agent 等其他 executor 是显式 opt-in adapter，必须产出可审计回执，不默认承诺行为或质量效果与 Codex CLI 等价。
- OPL 可以提供阶段调度、唤醒、队列、交接、回执、重试和投影支撑，但 MAG 继续持有基金阶段包、提示、技能、可资助性/写作质量门槛、正文真相和可提交包导出权威。
- MAG 继续独立持有 grant truth、fundability verdict、authoring quality verdict、route owner 与 submission/export authority。
- Domain memory 与 owner/lifecycle receipt apply 只允许投影 consumed memory refs、writeback proposal、MAG accept/reject decision、owner/no-regression receipt refs、lifecycle receipt refs、runtime receipt evidence、operator receipt projection 与 repo-source layout audit；不把 fundability verdict、真实 grant artifact、memory body、export verdict 或 receipt instance 写进 repo source。
- 旧 `OPL Runtime Manager`、Hermes-first、gateway 和本地 host runtime 表述只作为历史追溯或实现 provider 细节保留；Temporal 作为 OPL production substrate 的必需性由 OPL Framework 持有，并且是任务启动后的默认托管自治 runtime substrate，但不由 MAG 改写为 grant-domain runtime truth。

</details>

## 这个仓库应该怎么读

1. 潜在用户先读当前首页，再继续看 [文档索引](./docs/README.md)、[领域定位](./docs/public/domain-positioning.md) 和 [最小可用范围](./docs/public/mvp-scope.md)。
2. 技术规划、架构判断和方向同步，继续读 [项目概览](./docs/project.md)、[当前状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md)、[决策记录](./docs/decisions.md) 以及 [合同说明](./contracts/README.md)。
3. 开发者和维护者再进入 `docs/active/`、`docs/specs/`、`docs/references/` 与 [历史归档索引](./docs/history/README.md)。

## 给 Agent 和技术操作者的快速入口

<details>
  <summary><strong>如果你准备把这个仓直接交给 Codex 或其他 Agent，先看这里</strong></summary>

- 不会自动安装。单独 clone 这个仓不会把 OPL Framework 或托管运行时一起装好。要把 MAG 用到能用，先准备好当前的 `one-person-lab` checkout 或 release bundle，然后再用下面这些 repo-local clean runner 命令查看 skill surface 或导出 domain handler。
- 先读 [文档索引](./docs/README.md)。这里已经把当前技术全景、formal-entry matrix、稳定 capability surface 和 repo-tracked 真相所在位置收口好了。
- 然后读 [合同说明](./contracts/README.md) 和 [`contracts/runtime-program/current-program.json`](./contracts/runtime-program/current-program.json)。这是恢复 active product-entry shell、schema-backed surface 和当前 mainline 指针的最快路径。
- 在改 route、入口 wording 或公开表述前，把 [项目概览](./docs/project.md)、[当前状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md) 和 [决策记录](./docs/decisions.md) 当成公开与技术真相集。
- 当前 formal-entry matrix 是 `CLI`、`MCP` 和 `controller`。`CLI` / `MedAutoGrantDomainEntry` 是 agent entry；`product entry/product status/direct-entry/user-loop`、本地脚本与 schema-backed contract 共同构成 app skill 下的内部 command contract 和 direct-product projection。OPL/Temporal 托管自治 runtime 是任务启动后的默认运行驻留；非默认 executor / proof backend 只在显式 opt-in 集成 lane 中出现。
- MAG 可以通过 Codex app skill 直接调用，也可以通过 OPL 托管调用。两条路径必须回到同一套 MAG-owned route、quality、workspace 和 export surface。
- 如果外部 agent 或 OPL 需要直接读取 repo-tracked handler surface，用 repo-local clean runner：`<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli domain-handler export --input <input_path> --format json`；返回的是 MAG domain-handler export、authority refs、typed blocker refs 与 generated-surface handoff refs，并且不会把 Python 副产物写回 checkout。
- pre-authoring intake 用 `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli workspace initialize-intake --input <selection_input> --workspace-root <workspace_dir> --format json`；目录会带 workspace-local Git boundary，`workspace.json` 是 MAG canonical document。
- 当前单一 skill descriptor 已携带可直接消费的 `runtime_continuity` envelope，并复用既有 `session_continuity` / `progress_projection` / `artifact_inventory` / `runtime_control` truth。
- 当前 product-entry manifest 也携带 `controlled_domain_memory_apply_proof`、`owner_receipt_contract` 与 `lifecycle_guarded_apply_proof`，让 OPL 或 direct caller 可以审计 consumed grant-strategy memory refs、writeback proposal、accept/reject decision、owner/no-regression receipt refs、lifecycle receipt refs、runtime receipt evidence、operator receipt projection 与 repo-source layout，而不会拿到 memory body 或 grant artifact。
- 当前可机读治理面包括 `workspace quality-scorecard`、`workspace quality-diff` 和 `pass autonomy-controller`。

</details>

## 维护者验证

- 默认本地门禁使用 `./scripts/verify.sh`，它会运行 line-budget、最小 smoke lane 和非重型 fast core lane。
- Makefile 中的 Python / pytest lane 通过 `scripts/run-python-clean.sh` / `scripts/run-pytest-clean.sh` 执行，把 bytecode 与 pytest cache 导向 checkout 外部。
- 快速入口健康检查使用 `./scripts/verify.sh smoke` 或 `make test-cli-smoke`。
- 矩阵型、product-entry、runtime/session、hosted/export 与回归覆盖使用 `./scripts/verify.sh regression`。Product-entry case 现在直接放在 `tests/product_entry_cases/` 下收集；旧 `tests/test_product_entry.py` 聚合面已删除。
- repo 治理、结构检查和 clean-clone/full-suite 基线分别使用 `./scripts/verify.sh meta`、`./scripts/verify.sh structure` 与 `./scripts/verify.sh full`。

## 延伸阅读

- [文档索引](./docs/README.md)
- [领域定位](./docs/public/domain-positioning.md)
- [最小可用范围](./docs/public/mvp-scope.md)
- [项目概览](./docs/project.md)
- [当前状态](./docs/status.md)
- [架构](./docs/architecture.md)
- [不变量](./docs/invariants.md)
- [决策记录](./docs/decisions.md)
- [合同说明](./contracts/README.md)
