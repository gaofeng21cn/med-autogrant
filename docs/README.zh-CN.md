# 文档索引

[English](./README.md) | **中文**

这个目录是 `Med Auto Grant` 的第二层技术阅读面。
仓库首页应优先写给申请人、领域专家和非技术读者。
而这里负责承接其后的技术记录、追溯记录、参考说明和实现历史。

## 按读者类型进入

| 读者 | 建议起点 | 目的 |
| --- | --- | --- |
| 潜在用户与领域专家 | [仓库首页](../README.zh-CN.md)、[领域定位](./domain-positioning.zh-CN.md)、[MVP 范围](./mvp-scope.zh-CN.md) | 先理解这条基金主线是干什么的，再决定是否进入技术细节 |
| 技术规划者、架构读者、方向同步读者 | [项目概览](./project.md)、[当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md)、[决策记录](./decisions.md)、[合同说明](../contracts/README.md) | 快速抓住当前技术形态、边界和主线方向 |
| 开发者与维护者 | [Specs 索引](./specs/README.zh-CN.md)、[Specs lifecycle map](./specs/specs_lifecycle_map.md)、[References 目录](./references/)、[活跃 plans](./plans/README.zh-CN.md)、[历史归档](./history/README.zh-CN.md) | 查看技术记录、内部参考、未来工作和归档材料 |

## 当前技术图景

- `Med Auto Grant` 是独立的医学基金 domain agent，对外第一主语是单一 `Med Auto Grant` app skill；其下稳定 capability surface 由 `CLI`、`MedAutoGrantDomainEntry`、本地脚本与 schema-backed contract 组成。
- formal-entry matrix 继续固定为 `CLI`、`MCP` 与 `controller`。
- 默认正文执行与默认 runtime owner 继续继承本机 `Codex CLI` / `codex_cli` 默认；`Hermes-Agent` 相关路径只保留在显式 hosted/proof lane 或技术参考层，默认安装不拉取 `hermes-agent`，不改写默认公开 capability contract。
- `OPL Runtime Manager` 是目标形态中的 OPL 侧薄管理层，位于外部 `Hermes-Agent` substrate 之上；它可以消费 MAG runtime_control、runtime_continuity、workspace projection、artifact locator 与 explicit wakeup/TODO queue，但不持有 MAG grant truth 或 authoring execution。
- 历史 program 记录与迁移说明统一从 `docs/history/` 进入；较早 dated specs 可以继续留在 `docs/specs/` 作为 provenance，但机器可读面通过语义化 `human_doc:*` 标识引用它们，而不是把旧路径钉成稳定接口。
- product status、user-loop、projection 与本地 `submission-ready` package 已落地，但它们都是 app skill 下的内部 command contract 与 direct-product projection；当前任务边界已明确区分“科学待审就绪”和更严格的本地导出 gate，且本地导出 gate 不代表外部基金官网 portal submission 已完成；未来 hosted 产品扩展只有在确属活跃计划时才放入 `docs/plans/`。
- `OPL` family routing 与 `Codex` skill activation 继续消费同一套 MAG capability surface；MAG 负责 grant-domain truth、direct grant entry 与 execution routing。
- MAG 当前任务边界锁定在“指定基金任务正文 authoring”；“科学完成”与“形式/客观补件完成”是显式分层。
- 科学层交付的是可待审包，用于同任务内作者/评审决策。
- 形式/客观补件默认按 `TODO + 显式唤醒` 管理；除非直接破坏正文科学成立，否则不作为正文 authoring blocker。
- 人工 gate 只作用于同一基金任务内的作者决策，不扩展成跨 funder 重选。
- 当前 controller-owned、read-only 的 projection 继续包括 `workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`，并在作者侧主线之上保持 schema-backed 边界。
- 当前 grouped shell 也已经把 `product build-entry`、`product manifest`、`product status` 与 `package submission-ready` 暴露成 skill-backed CLI 命令面。
- 当前轻量 grant `product entry` shell 是 app skill 背后的内部产品入口 shell 与 domain/API catalog builder；未来 hosted 产品形态在活跃阶段放入 `docs/plans/`，完成后归入 history。
- 质量治理已经通过 `workspace quality-scorecard` 与 `workspace quality-diff` 收成 schema-backed surface。
- 长时间自治已经通过 `pass autonomy-controller` 暴露为正式入口，并输出结构化 blocker 与 evidence-gap report。
- 通用 grant grammar 与 funder-specific family profile 规则继续在 `grant_family_registry.py` 分层；跨 funder 重选不进入默认正文 authoring gate 语义。

## 技术工作集

开始改仓库状态前，先读这些文件：

- [项目概览](./project.md)
- [当前状态](./status.md)
- [架构](./architecture.md)
- [不变量](./invariants.md)
- [决策记录](./decisions.md)
- [合同说明](../contracts/README.md)
- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs lifecycle map](./specs/specs_lifecycle_map.md)

机器本地 runtime state 继续统一放在 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

## 默认公开入口

- [仓库首页](../README.zh-CN.md)
- [领域定位](./domain-positioning.zh-CN.md)
- [MVP 范围](./mvp-scope.zh-CN.md)

这些文件构成默认公开入口；凡是属于公开表面的内容，应在适用时保持中英双语镜像。
root public-doc allowlist 保持稀疏：

- `README*` 是公开第一入口。
- `docs/domain-positioning*` 继续 current，用于说明 MAG owner、公开主语和 OPL/Hermes 边界。
- `docs/mvp-scope*` 继续 current，用于说明 NSFC MVP 范围与非目标。

## 技术记录

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs 索引](./specs/README.zh-CN.md)
- [Specs lifecycle map](./specs/specs_lifecycle_map.md)
- [AI-first 质量边界 current truth](./specs/2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./specs/2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md)
- [合同说明](../contracts/README.md)

当前 grant product-entry shell 继续作为 app skill 背后的 domain/API catalog builder，也是稳定可调用面的一部分；当前 schema-backed 冻结也会把 `hosted contract bundle`、`domain_entry_contract`、`supported_commands` 与 `command_contracts` 作为集成/参考面暴露给 hosted caller / 外部 caller 使用。
质量治理与自治 controller schema 已进入 [`schema-index.json`](../schemas/v1/schema-index.json) 和 current-program truth surface。
完整 repo-tracked truth surface 清单以 [`current-program.json`](../contracts/runtime-program/current-program.json) 的 `repo_tracked_truth_surfaces` 为准；contract/schema/source surface 保持 repo path，叙述文档使用语义化 `human_doc:*` 标识。Specs 索引与 specs lifecycle map 共同区分 active boundary records、support records 和 historical provenance records。

## 追溯记录

- [References 目录](./references/)
- [历史归档](./history/README.zh-CN.md)
- [历史 specs 索引](./history/specs/README.zh-CN.md)
- [历史 plans 索引](./history/plans/README.zh-CN.md)
- [Docs portfolio consolidation boundary](./docs_portfolio_consolidation.md)

## 结构质量验证

Sentrux 作为 advisory 架构信号进入仓库。维护者在吸收结构性变更前应运行
`sentrux gate .`；涉及依赖方向、package/export builder、runtime adapter
或 product-entry 内部结构时，应同时运行 `sentrux check .`。CI 工作流当前保持
advisory 模式，现有基线通过聚焦 cleanup lane 逐步收紧。合入判断优先看产品语义
和 repo-native 验证：大幅且无法解释的结构退化、cycle 回归、rules 违规或测试失败
应阻止吸收；若依赖 ownership 更清楚，Sentrux 分数小幅波动可以接受。

本地 `structure` lane 与 advisory workflow 还会在 `artifacts/opl-quality-details/`
写入 OPL quality details sidecar：通过
`/Users/gaofeng/workspace/one-person-lab/bin/opl quality details --root . --format markdown --limit 20`
生成 markdown，通过同一命令的 `--format json` 生成 JSON，并额外保留完整
`.sentrux/rules.toml` sidecar。若 Sentrux gate/check 失败，脚本会先生成并打印这些
诊断，再报告 Sentrux 失败。

默认本地验证入口是 `./scripts/verify.sh`。它只运行一次 line-budget，然后运行小
`smoke` lane 与不需要 optional proof dependency 的非重型 fast core lane。矩阵型、
runtime/session、hosted/export、product-entry 与兼容性覆盖归入
`./scripts/verify.sh regression`；显式 Hermes hosted/proof 检查归入
`./scripts/verify.sh proof` 并使用 `proof` extra；product-entry
case 模块直接由 `tests/product_entry_cases/` 收集，`tests/test_product_entry.py`
只保留兼容导入面；完整基线继续由 `./scripts/verify.sh full` 承担。

仓库目录治理通过 `tests/test_repository_hygiene.py` 纳入 meta 验证面。repo-tracked
主线不得包含 `dist/`、`build/`、`out/`、`__pycache__`、`*.egg-info`、`.DS_Store`、
`.codex/`、`.omx/`、`.runtime-program/`、`runtime-state/` 或
`.agent-contract-baseline.json` 这类生成物 / 本地状态；`.agents/` 下唯一允许跟踪的
入口是 `.agents/plugins/marketplace.json`。同一测试也继续约束 tracked source/test
line budget，新增或增长的超长文件应拆分，而不是扩大单文件基线。

## Plans 与历史规划工件

- [活跃 plans](./plans/README.zh-CN.md)
- [历史 plans](./history/plans/README.zh-CN.md)

已完成的规划工件现已统一迁入 `docs/history/plans/`。
当前主线真相继续以核心文档、`docs/specs/README.zh-CN.md` 中列出的 active specs 和 [`current-program.json`](../contracts/runtime-program/current-program.json) 为准。

## 文档规则

- 继续把 [仓库首页](../README.zh-CN.md) 保持成申请人和非技术专家可读的入口。
- 继续把默认公开文档保持成中英双语镜像。
- `docs/specs/README.zh-CN.md` 中列出的 active specs 继续承担具体技术边界的权威记录，但不能取代用户入口首页。
- references、plans 和 history 可以保留，但不能占据默认公开阅读路径。
- `README*` 与 `docs/**` 默认是人读材料。脚本、测试、runtime status 和 contracts 不应依赖它们的具体路径；机器面需要表达文档关系时，使用 schema/source path 或语义化 `human_doc:*` 标识。
- 每条 docs lane 都应能说明 `owner`、`purpose`、`state` 和 `machine boundary`。
- `state=current` 只用于公开入口、核心文档、active specs 和当前合同指针；稳定说明材料用 `state=reference`，追溯材料用 `state=history`。

## 治理说明

- 文档治理统一冻结在 [系列项目文档治理清单](./references/series-doc-governance-checklist.md)、技术工作集和仓库跟踪的 contract/doc surface 中，而不再只写在 `AGENTS.md`。
- `README*` 与 `docs/README*` 是默认公开入口。
- `docs/specs/**` 承载 active 技术记录和较早 provenance specs；`docs/history/specs/` 是较早 dated records 的历史阅读索引。
- `docs/references/**` 承载内部参考说明。
- `docs/plans/**` 只保留活跃未来工作；`docs/history/**` 承载已完成计划和历史追溯材料。
