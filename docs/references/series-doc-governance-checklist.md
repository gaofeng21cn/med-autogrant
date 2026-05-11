# 系列项目文档治理清单

## 目标

本清单用于把 `Med Auto Grant` 放进 `One Person Lab`、`Med Auto Science`、`Med Auto Grant`、`RedCube AI` 这组系列项目的统一文档管理口径里做巡检。
它服务跨仓 docs intake、回归与持续对齐，不替代核心五件套、`docs/specs/README*` 列出的 active specs、`docs/specs/specs_lifecycle_map.md`、`schemas/v1/` 或 `contracts/runtime-program/`。

## 一、默认入口

- `README.md` / `README.zh-CN.md` 是默认公开首页。
- `docs/README.md` / `docs/README.zh-CN.md` 是默认 docs 索引。
- 外部读者先走公开入口；AI / 维护者先走核心五件套，再按 `docs/specs/README*` 与 `specs_lifecycle_map.md` 进入 active specs、support specs、schemas 与 `contracts/runtime-program/current-program.json`。

## 二、核心五件套

- `docs/project.md`
- `docs/status.md`
- `docs/architecture.md`
- `docs/invariants.md`
- `docs/decisions.md`

这五件套必须位于 `docs/` 根目录，并被 `docs/README*` 显式链接。
任何涉及当前主线、formal entry、runtime substrate owner、product-entry truth、author-side boundary 的变化，都不能只改某个 dated spec 或 schema/contract，需要同步更新对应核心文档、active specs index 或 `current-program` pointer。

## 三、公开层与内部层

- `README*` 与 `docs/README*` 继续承担双语公开入口。
- `docs/specs/README*` 与 `docs/specs/specs_lifecycle_map.md` 承担 specs 组合治理；只有索引列出的四份 active specs 承担 current boundary。其余 dated specs 是 support reference、integration reference、historical activation package、superseded provider proof 或 provenance。
- `docs/references/**` 承担内部参考说明；默认中文维护。
- `docs/plans/**` 只承担活跃未来计划；`docs/history/**` 承担已完成 plans、历史 specs 索引与归档追溯，不得重新回灌成当前公开入口。
- `schemas/v1/` 与 `contracts/runtime-program/` 继续只承载 machine-readable contract，不承载 narrative second source。
- 长期规则要冻结进核心文档、repo-tracked current truth、reference 或 contract surface；不要把 `AGENTS.md` 继续当第二真相源。

## 四、系列一致性检查

- 文档必须把 `Med Auto Grant` 写成医学 `Grant Ops` 的 author-side / proposal-facing domain agent，明确它可被 `OPL` Codex-first、stage-led agent runtime framework 托管，但不是 `OPL` 内部模块、顶层 gateway 或 runtime substrate owner。
- 系列项目名称与角色要与四仓当前真相同步：`One Person Lab` 是完整的 Codex-first、stage-led agent runtime framework，`Med Auto Science` 是 `Research Ops`，`RedCube AI` 是 visual-deliverable / `Presentation Ops`。
- 若提到 `Hermes-Agent`，只能指上游外部 runtime 项目 / 服务；repo-side adapter、helper、pilot、scaffold 都不能被写成“已接入 Hermes-Agent”。
- 默认公开入口、repo-tracked current truth、内部参考、schema/contract surface 与历史档案必须继续分层。
- 修改 docs skeleton、公开入口、schema-backed frontdoor、runtime program pointer 或 authoring wording 时，必须同步更新相关 contract/test；但不得用测试固定 README/docs prose、标题或状态文案。

## 五、默认验证

- 默认 docs 审计入口：`scripts/verify.sh meta`
- 同义验证入口：`make test-meta`
- 默认 smoke：`scripts/verify.sh`
- 若验证命令、docs index、schema/contract surface 有变化，继续同步 `Makefile`、`scripts/verify.sh`、`README*` 与 `tests/test_*`
