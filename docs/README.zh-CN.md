# 文档索引

[English](./README.md) | **中文**

这个目录是 `Med Auto Grant` 的技术阅读层。仓库首页继续写给申请人、领域专家和非技术读者；本页服务需要理解当前技术真相、活跃支撑材料、历史追溯和文档生命周期的读者。

## 当前主线

- `Med Auto Grant` 是独立医学基金 domain agent，对外第一主语是单一 `Med Auto Grant` app skill。
- 稳定 capability surface 由 `CLI`、`MCP`、`controller`、`MedAutoGrantDomainEntry`、本地脚本与 schema-backed contracts 组成。
- `OPL` 是 Codex-first、stage-led 的完整智能体运行框架，可以托管 MAG stage attempts；`Codex CLI` 是 stage 内默认最小执行单元。
- MAG 持有 grant truth、authoring execution、fundability / quality verdict、route owner 和 submission-ready export authority；OPL 消费 MAG projection / wakeup / receipt / artifact locator 做调度、唤醒、交接、重试和投影。
- 当前任务边界锁定在“指定基金任务正文 authoring”。科学完成、形式/客观补件完成、本地 export gate 与外部基金官网提交是分层状态。
- 当前 repo-tracked truth surface 入口是 [`contracts/runtime-program/current-program.json`](../contracts/runtime-program/current-program.json)。

## 按读者类型进入

| 读者 | 建议起点 | 目的 |
| --- | --- | --- |
| 潜在用户与领域专家 | [仓库首页](../README.zh-CN.md)、[领域定位](./domain-positioning.zh-CN.md)、[MVP 范围](./mvp-scope.zh-CN.md) | 理解这条基金主线服务什么工作 |
| 技术规划者、架构读者、方向同步读者 | [项目概览](./project.md)、[当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md)、[决策记录](./decisions.md)、[合同说明](../contracts/README.md) | 抓住当前边界、执行模型和 owner split |
| 开发者与维护者 | [Docs portfolio consolidation](./docs_portfolio_consolidation.md)、[Specs 索引](./specs/README.zh-CN.md)、[Specs lifecycle map](./specs/specs_lifecycle_map.md)、[References 目录](./references/)、[活跃 plans](./plans/README.zh-CN.md)、[历史归档](./history/README.zh-CN.md) | 区分 current truth、support reference、active future work 和 history |

## 当前技术真相

| 层级 | 入口 | 说明 |
| --- | --- | --- |
| Core truth | [项目概览](./project.md)、[当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md)、[决策记录](./decisions.md) | 当前产品角色、运行边界、约束和持久决策。 |
| Machine truth | [`current-program.json`](../contracts/runtime-program/current-program.json)、[schema index](../schemas/v1/schema-index.json)、[合同说明](../contracts/README.md) | repo-tracked truth surfaces、schema/source 和可执行合同。 |
| Active specs | [Specs 索引](./specs/README.zh-CN.md)、[Specs lifecycle map](./specs/specs_lifecycle_map.md) | 仍承担 current-truth 的少数技术边界记录。 |
| Active future work | [活跃 plans](./plans/README.zh-CN.md) | 当前为空；未来 hosted/product 扩展只有在确属活跃计划时进入这里，完成后进入 history。 |

## 活跃支撑与参考

- `docs/references/`：策略记忆、cross-repo handoff、维护者治理和其他支撑参考。
- `docs/specs/`：active specs 与因 path provenance 仍留在原位的历史 dated specs；必须通过 README / lifecycle map 区分 current、support 和 history。
- `docs/plans/`：只承载仍未被核心文档、合同面或 history 吸收的活跃计划。
- `$CODEX_HOME/projects/med-autogrant/runtime-state/`：本机 runtime state。

## 历史与追溯

- [历史归档](./history/README.zh-CN.md)
- [历史 specs 索引](./history/specs/README.zh-CN.md)
- [历史 plans 索引](./history/plans/README.zh-CN.md)
- 较早 `OPL Runtime Manager`、Temporal、Hermes-first、gateway、monorepo、active-adapter 和 local host runtime 说明只在 active layer 或 machine-readable contract 显式提升时才作为当前边界；其余作为 provider-specific / historical provenance 阅读。

## 验证与治理

- 默认本地验证入口是 `./scripts/verify.sh`。
- `./scripts/verify.sh regression` 覆盖矩阵型、runtime/session、hosted/export、product-entry 与兼容性范围。
- `./scripts/verify.sh proof` 用于显式 Hermes hosted/proof 检查并使用 `proof` extra。
- 结构质量与 repo hygiene 由 Sentrux advisory、`tests/test_repository_hygiene.py` 和 repo-native verify lane 承接；叙述性 docs 变更默认走人工 review、`git diff --check` 和必要 link spot-check。

## 文档规则

- 文档治理按内容生命周期判断，文件名、日期和路径作为辅助信号。
- 入口文档先写当前状态、层级、新旧关系和下一跳；历史 specs、旧 hosted/provider 说明、已完成 plans 与追溯材料保留为 provenance。
- `README*` 与 `docs/**` 是人读材料。脚本、测试、runtime status 和 contracts 使用 schema/source path、contract path 或语义化 `human_doc:*` 标识表达文档关系。
- 每条 docs lane 都应能说明 `owner`、`purpose`、`state` 和 `machine boundary`。
