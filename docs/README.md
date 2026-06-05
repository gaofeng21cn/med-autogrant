# 文档索引

Owner: `Med Auto Grant`
Purpose: `docs_index_and_reader_routing`
State: `current`
Machine boundary: 本文是人读索引。机器真相继续归 contracts、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 grant workspace artifacts；文档关系需要机器引用时使用语义化 `human_doc:*` id。

这个目录是 `Med Auto Grant` 的第二层技术阅读面。
仓库首页应优先写给申请人、领域专家和非技术读者。
而这里负责承接其后的技术记录、追溯记录、参考说明和实现历史。

## 按读者类型进入

| 读者 | 建议起点 | 目的 |
| --- | --- | --- |
| 潜在用户与领域专家 | [仓库首页](../README.md)、[领域定位](./public/domain-positioning.md)、[MVP 范围](./public/mvp-scope.md) | 先理解这条基金主线是干什么的，再决定是否进入技术细节 |
| 技术规划者、架构读者、方向同步读者 | [项目概览](./project.md)、[当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md)、[决策记录](./decisions.md)、[合同说明](../contracts/README.md) | 快速抓住当前技术形态、边界和主线方向 |
| 开发者与维护者 | [Specs 索引](./specs/README.md)、[Specs lifecycle map](./specs/specs_lifecycle_map.md)、[References 目录](./references/)、[Active baton 与当前计划](./active/README.md)、[历史归档](./history/README.md) | 查看技术记录、内部参考、active baton 材料和归档材料 |

## 入口职责

| 层 | 职责 |
| --- | --- |
| 核心五件套 | 当前角色、架构边界、不变量、决策和状态摘要。 |
| `docs/active/` | 当前 gap、当前计划、证据门和 private implementation inventory。 |
| `docs/public/` | 仓库首页之后的公开补充入口。 |
| `docs/product/` | App skill / product-entry / user-loop / operator support 的人读索引。 |
| `docs/runtime/` | OPL/Temporal runtime boundary、domain-handler/projection/receipt 支撑索引。 |
| `docs/delivery/` | package/export/submission-ready delivery 支撑索引。 |
| `docs/source/` | workspace/source intake 与 source refs 支撑索引。 |
| `docs/policies/` | 稳定治理规则入口。 |
| `docs/specs/` | active spec 与 support current-truth subsection；不能按 dated 文件名直接推断当前状态。 |
| `docs/references/` | north-star、OPL adoption、memory policy 和治理 checklist。 |
| `docs/history/` | 旧路线、旧 provider/runtime proof、已完成计划、coverage ledger 和 tombstone provenance。 |

Active/support/history 的边界由 [MAG 文档组合治理](./docs_portfolio_consolidation.md) 与 [Specs lifecycle map](./specs/specs_lifecycle_map.md) 统一维护。`README*`、`docs/**` 和参考文档都是人读面；脚本、测试、runtime status 和 contracts 不应依赖 Markdown prose path 或章节标题作为机器接口。

## OPL 系列分层

OPL 系列项目的全局主参考是 `/Users/gaofeng/workspace/one-person-lab/docs/active/opl-family-development-reference.md`。它维护 OPL Framework 的全局目标、全局差距、通用能力上收边界、App/workbench 目标和跨仓开发顺序。

MAG 本仓只维护 grant domain agent 的目标、当前差距、grant truth、fundability/quality/export authority、direct app skill path、OPL-hosted domain-handler/projection/receipt 边界，以及哪些通用 workspace/source intake、memory locator、artifact/package lifecycle、quality/readiness projection 和 observability primitive 应上收到 OPL。MAS、RCA、MDS 或 OPL-owned App/workbench 的并行 backlog 不写入 MAG 活跃计划。

## Workspace / file lifecycle 边界

MAG 的 repo-source layout 按标准 domain agent 职责读取：`agent/` 持有 grant declarative pack，`contracts/` 持有机器合同和 schema/index，`runtime/authority_functions/` 只作为最小 grant authority function 的 runtime-facing descriptor/receipt-ref 边界，`src/` 持有 domain handler、authority adapter 与 native helper，`docs/` 持有人读治理说明。真实 grant workspace state、runtime artifact、receipt instance、submission/export package、临时 build/cache/venv/pycache/pytest cache/install sync 副产物不进入开发 checkout；它们必须落到 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

MAG repo source 只保存 locator、index、schema、receipt ref、restore/retention policy 和 no-forbidden-write 证据。grant truth、fundability/quality/export verdict、package authority、grant strategy memory body accept/reject 与 owner receipt 仍归 MAG owner chain；OPL 只上收通用 workspace/file lifecycle primitive、scheduler/runner/session/workbench shell 和 projection。

## 当前技术入口摘要

本页只做 reader routing，不承载当前状态 ledger。当前技术真相按下面入口读取：

- `Med Auto Grant` 的角色、默认运行 owner、任务边界和证据门：读 [当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md) 和 [`current-program.json`](../contracts/runtime-program/current-program.json)。
- 当前唯一 active gap / plan：读 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)。
- per-surface private implementation residue：读 [MAG 私有实现与 OPL 迁移台账](./active/opl-private-implementation-migration-inventory.md)。
- active/support specs 的可读 subsection：读 [Specs 索引](./specs/README.md) 与 [Specs lifecycle map](./specs/specs_lifecycle_map.md)。
- 旧 `OPL Runtime Manager`、Hermes-first、Gateway/federation、local-runtime、hosted-caller proof、lightweight handoff 和 dated completion claim：只从 [历史归档](./history/README.md) 与 [历史 specs](./history/specs/README.md) 进入。

若本文、历史 specs 或 `current-program.json` 中的 `human_doc:*` 语义引用看起来仍指向旧 dated 文件，阅读时仍以核心五件套、active gap plan、contracts/schema/source 和 specs lifecycle map 的当前 owner 标注为准。语义引用不把整份旧文件提升成 current owner。

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
- [领域定位](./public/domain-positioning.md)
- [MVP 范围](./public/mvp-scope.md)

这些文件构成 docs 层默认公开补充入口；是否继续保留根层公开双语入口由 public/product 需求单独判断，不要求 `docs/**` 继续维护双语镜像。
public-doc allowlist 保持稀疏：

- `README*` 是公开第一入口。
- `docs/public/domain-positioning.md` 继续 current，用于说明 MAG owner、公开主语和 OPL/provider 边界。
- `docs/public/mvp-scope.md` 继续 current，用于说明 NSFC MVP 范围与非目标。

## 技术记录

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs 索引](./specs/README.md)
- [Specs lifecycle map](./specs/specs_lifecycle_map.md)
- [AI-first 质量边界 current truth](./specs/2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./specs/2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md)
- [合同说明](../contracts/README.md)
- [Grant Strategy Memory Policy](./references/grant_strategy_memory_policy.md)

完整 repo-tracked truth surface 清单以 [`current-program.json`](../contracts/runtime-program/current-program.json) 的 `repo_tracked_truth_surfaces` 为准；contract/schema/source surface 保持 repo path，叙述文档使用语义化 `human_doc:*` 标识。Specs 索引与 specs lifecycle map 共同区分 active boundary records、support records 和 historical provenance records；已移动到 `docs/history/specs/` 的 provider proof、local-runtime closeout、hosted handoff 和 fail-closed tranche 不参与 current/support specs 阅读路径。

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

默认本地验证入口是 `./scripts/verify.sh`。它只运行一次 line-budget，然后通过
repo-local clean runner 运行小 `smoke` lane 与不需要 optional proof dependency
的非重型 fast core lane；Python bytecode、pytest cache 和临时同步副产物不得写回开发 checkout。
矩阵型、
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
active baton 与当前完成门槛进入 `docs/active/**`；已完成或被替代的规划工件进入
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

- 文档治理统一冻结在 [系列项目文档治理清单](./references/governance/series-doc-governance-checklist.md)、技术工作集和仓库跟踪的 contract/doc surface 中，而不再只写在 `AGENTS.md`。
- `README*` 与 `docs/README.md` 是默认入口；根层 `README*` 是否保留公开双语由 public/product 需求决定。
- MAG 采用 OPL-family canonical docs taxonomy：
  `active/public/product/runtime/delivery/source/policies/specs/references/history`。
- `docs/active/**` 承接当前执行、当前计划、当前差距与 active baton；旧 `docs/plans/**`
  活跃计划层已退役。
- `docs/public/**` 承接公开叙事索引；当前公开补充文档固定为
  `docs/public/domain-positioning.md` 与 `docs/public/mvp-scope.md`。
- `docs/product/**`、`docs/runtime/**`、`docs/delivery/**`、`docs/source/**`
  分别承接 direct product entry、runtime、submission/package delivery 与 workspace/source intake 支撑。
- `docs/policies/**` 承接稳定规则；`docs/specs/**` 承载 active 技术记录和较早
  provenance specs；`docs/references/**` 承载内部参考说明；`docs/history/**`
  承载已完成计划和历史追溯材料。
