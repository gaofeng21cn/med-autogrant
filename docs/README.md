# 文档索引

这个目录是 `Med Auto Grant` 的第二层技术阅读面。
仓库首页应优先写给申请人、领域专家和非技术读者。
而这里负责承接其后的技术记录、追溯记录、参考说明和实现历史。

## 按读者类型进入

| 读者 | 建议起点 | 目的 |
| --- | --- | --- |
| 潜在用户与领域专家 | [仓库首页](../README.md)、[领域定位](./domain-positioning.md)、[MVP 范围](./mvp-scope.md) | 先理解这条基金主线是干什么的，再决定是否进入技术细节 |
| 技术规划者、架构读者、方向同步读者 | [项目概览](./project.md)、[当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md)、[决策记录](./decisions.md)、[合同说明](../contracts/README.md) | 快速抓住当前技术形态、边界和主线方向 |
| 开发者与维护者 | [Specs 索引](./specs/README.md)、[Specs lifecycle map](./specs/specs_lifecycle_map.md)、[References 目录](./references/)、[Active baton 与当前计划](./active/README.md)、[历史归档](./history/README.md) | 查看技术记录、内部参考、active baton 材料和归档材料 |

## OPL 系列分层

OPL 系列项目的全局主参考是 `/Users/gaofeng/workspace/one-person-lab/docs/active/opl-family-development-reference.md`。它维护 OPL Framework 的全局目标、全局差距、通用能力上收边界、App/workbench 目标和跨仓开发顺序。

MAG 本仓只维护 grant domain agent 的目标、当前差距、grant truth、fundability/quality/export authority、direct app skill path、OPL-hosted sidecar/projection/receipt 边界，以及哪些通用 workspace/source intake、memory locator、artifact/package lifecycle、quality/readiness projection 和 observability primitive 应上收到 OPL。MAS、RCA、MDS 或 OPL-owned App/workbench 的并行 backlog 不写入 MAG 活跃计划。

## 当前技术图景

- `Med Auto Grant` 是独立的医学基金 domain agent，对外第一主语是单一 `Med Auto Grant` app skill；其下稳定 capability surface 由 `CLI`、`MedAutoGrantDomainEntry`、本地脚本与 schema-backed contract 组成。
- formal-entry matrix 继续固定为 `CLI`、`MCP` 与 `controller`。
- OPL 是 stage-led、以 Agent executor 为最小执行单位的完整智能体运行框架。它可以把 MAG 作为外部领域依赖托管；除非活跃合同显式选择其他 provider，`Codex CLI` 是 stage attempt 的最小执行单元。
- OPL 可以消费 MAG 的 runtime_control、runtime_continuity、workspace projection、artifact locator 与 explicit wakeup/TODO queue，用于调度、唤醒、交接、回执、重试和投影；它不持有 MAG grant truth、authoring execution、fundability judgment、quality verdict 或 submission-ready export authority。
- 旧 `OPL Runtime Manager`、Temporal、Hermes-first、gateway 与本地 host runtime 说明作为历史追溯或 provider-specific 实现记录保留；默认 MAG/OPL 边界由核心文档和 active specs 持有。
- [Docs portfolio consolidation boundary](./docs_portfolio_consolidation.md) 是当前文档生命周期 owner，记录逐分区当前 owner、已吸收内容和历史归位理由；旧 OPL Runtime Manager 与 lightweight handoff 说明已归入 history。
- 历史 program 记录与迁移说明统一从 `docs/history/` 进入；较早 dated specs 可以继续留在 `docs/specs/` 作为 provenance，但机器可读面通过语义化 `human_doc:*` 标识引用它们，而不是把旧路径钉成稳定接口。
- product status、user-loop、projection 与本地 `submission-ready` package 已作为 app skill 下的内部 command contract 与 direct-product projection 落地；当前任务边界已明确区分“科学待审就绪”和更严格的本地导出 gate，外部基金官网 portal submission 仍是单独的人类监督步骤；未来 hosted 产品扩展只有在确属活跃计划时才放入 `docs/active/`。
- `OPL` family routing 与 `Codex` skill activation 继续消费同一套 MAG capability surface；MAG 负责 grant-domain truth、direct grant entry 与 execution routing。
- MAG 当前任务边界锁定在“指定基金任务正文 authoring”；“科学完成”与“形式/客观补件完成”是显式分层。
- 科学层交付的是可待审包，用于同任务内作者/评审决策。
- 形式/客观补件默认按 `TODO + 显式唤醒` 管理；除非直接破坏正文科学成立，否则不作为正文 authoring blocker。
- 人工 gate 只作用于同一基金任务内的作者决策，不扩展成跨 funder 重选。
- 当前 controller-owned、read-only 的 projection 继续包括 `workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`，并在作者侧主线之上保持 schema-backed 边界。
- MAG 现在通过 `controlled_domain_memory_apply_proof`、`owner_receipt_contract` 与 `lifecycle_guarded_apply_proof` 暴露 controlled grant-stage domain memory 与 owner/lifecycle receipt apply proof：consumed grant strategy memory refs、writeback proposal、MAG accept/reject decision、owner/no-regression receipt refs、lifecycle receipt refs、runtime receipt evidence、operator receipt projection 与 repo-source layout audit 都可验证，但不把 memory body、grant artifact、export verdict 或 receipt instance 存入 repo source。
- 当前 grouped shell 也已经把 `product build-entry`、`product manifest`、`product status` 与 `package submission-ready` 暴露成 skill-backed CLI 命令面。
- 当前轻量 grant `product entry` shell 是 app skill 背后的内部产品入口 shell 与 domain/API catalog builder；未来 hosted 产品形态在活跃阶段放入 `docs/active/`，完成后归入 history。
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

- [仓库首页](../README.md)
- [领域定位](./domain-positioning.md)
- [MVP 范围](./mvp-scope.md)

这些文件构成默认公开入口；是否继续保留根层公开双语入口由 public/product 需求单独判断，不要求 `docs/**` 继续维护双语镜像。
root public-doc allowlist 保持稀疏：

- `README*` 是公开第一入口。
- `docs/domain-positioning*` 继续 current，用于说明 MAG owner、公开主语和 OPL/provider 边界。
- `docs/mvp-scope*` 继续 current，用于说明 NSFC MVP 范围与非目标。

## 技术记录

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs 索引](./specs/README.md)
- [Specs lifecycle map](./specs/specs_lifecycle_map.md)
- [AI-first 质量边界 current truth](./specs/2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./specs/2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md)
- [合同说明](../contracts/README.md)
- [Grant Strategy Memory Policy](./references/grant_strategy_memory_policy.md)

当前 grant product-entry shell 继续作为 app skill 背后的 domain/API catalog builder，也是稳定可调用面的一部分；当前 schema-backed 冻结也会把 `hosted contract bundle`、`domain_entry_contract`、`supported_commands` 与 `command_contracts` 作为集成/参考面暴露给 hosted caller / 外部 caller 使用。
fundability、specific aims、reviewer grammar 和 template strategy 这类经验按自然语言 memory 管理；`domain_memory_descriptor_locator`、`controlled_domain_memory_apply_proof`、`owner_receipt_contract` 与 `lifecycle_guarded_apply_proof` 现在只投影 writeback proposal / accept-reject / owner / no-regression / lifecycle runtime receipt evidence refs 和 repo-source layout audit，不把真实 memory entry、grant artifact 或 export verdict 写进 repo。`workspace quality-scorecard`、`grant-quality-closure-dossier`、autonomy controller report 和 submission-ready package 继续保持结构化权威。
质量治理与自治 controller schema 已进入 [`schema-index.json`](../schemas/v1/schema-index.json) 和 current-program truth surface。
完整 repo-tracked truth surface 清单以 [`current-program.json`](../contracts/runtime-program/current-program.json) 的 `repo_tracked_truth_surfaces` 为准；contract/schema/source surface 保持 repo path，叙述文档使用语义化 `human_doc:*` 标识。Specs 索引与 specs lifecycle map 共同区分 active boundary records、support records 和 historical provenance records。

## 追溯记录

- [References 目录](./references/)
- [历史归档](./history/README.md)
- [历史 specs 索引](./history/specs/README.md)
- [历史 plans 索引](./history/plans/README.md)
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
runtime/session、hosted/export、product-entry 与 provenance-oracle 回归覆盖归入
`./scripts/verify.sh regression`；显式 Hermes hosted/proof 检查归入
`./scripts/verify.sh proof` 并使用 `proof` extra；product-entry
case 模块直接由 `tests/product_entry_cases/` 收集，旧
`tests/test_product_entry.py` 聚合入口已删除；完整基线继续由 `./scripts/verify.sh full` 承担。

仓库目录治理通过 `tests/test_repository_hygiene.py` 纳入 meta 验证面。repo-tracked
主线不得包含 `dist/`、`build/`、`out/`、`__pycache__`、`*.egg-info`、`.DS_Store`、
`.codex/`、`.omx/`、`.runtime-program/`、`runtime-state/` 或
`.agent-contract-baseline.json` 这类生成物 / 本地状态；`.agents/` 下唯一允许跟踪的
入口是 `.agents/plugins/marketplace.json`。同一测试也继续约束 tracked source/test
line budget，新增或增长的超长文件应拆分，而不是扩大单文件基线。

## Active baton 与历史规划工件

- [Active baton 与当前计划](./active/README.md)
- [历史 plans](./history/plans/README.md)

旧 `docs/plans/**` 活跃计划层已退役。当前执行、当前计划、当前差距、
active baton 与 closeout evidence 进入 `docs/active/**`；已完成或被替代的规划工件进入
`docs/history/plans/**`。
当前主线真相继续以核心文档、`docs/specs/README.md` 中列出的 active specs 和 [`current-program.json`](../contracts/runtime-program/current-program.json) 为准。

## 文档规则

- 继续把 [仓库首页](../README.md) 保持成申请人和非技术专家可读的入口。
- `docs/**` 是中文内部开发与维护参考。稳定文档路径优先使用无语言后缀 `.md` 承载中文 canonical 内容。
- `docs/specs/README.md` 中列出的 active specs 继续承担具体技术边界的权威记录，但不能取代用户入口首页。
- references、plans 和 history 可以保留，但不能占据默认公开阅读路径。
- `README*` 与 `docs/**` 默认是人读材料。脚本、测试、runtime status 和 contracts 不应依赖它们的具体路径；机器面需要表达文档关系时，使用 schema/source path 或语义化 `human_doc:*` 标识。
- 每条 docs lane 都应能说明 `owner`、`purpose`、`state` 和 `machine boundary`。
- `state=current` 只用于公开入口、核心文档、active specs 和当前合同指针；稳定说明材料用 `state=reference`，追溯材料用 `state=history`。

## 治理说明

- 文档治理统一冻结在 [系列项目文档治理清单](./references/series-doc-governance-checklist.md)、技术工作集和仓库跟踪的 contract/doc surface 中，而不再只写在 `AGENTS.md`。
- `README*` 与 `docs/README.md` 是默认入口；根层 `README*` 是否保留公开双语由 public/product 需求决定。
- MAG 采用 OPL-family canonical docs taxonomy：
  `active/public/product/runtime/delivery/source/policies/specs/references/history`。
- `docs/active/**` 承接当前执行、当前计划、当前差距与 active baton；旧 `docs/plans/**`
  活跃计划层已退役。
- `docs/public/**` 承接公开叙事索引；当前 root public allowlist 暂由
  `docs/domain-positioning*` 与 `docs/mvp-scope*` 保持路径稳定。
- `docs/product/**`、`docs/runtime/**`、`docs/delivery/**`、`docs/source/**`
  分别承接 direct product entry、runtime、submission/package delivery 与 workspace/source intake 支撑。
- `docs/policies/**` 承接稳定规则；`docs/specs/**` 承载 active 技术记录和较早
  provenance specs；`docs/references/**` 承载内部参考说明；`docs/history/**`
  承载已完成计划和历史追溯材料。
