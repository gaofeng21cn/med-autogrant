# Quality, Autonomy Boundary, And Family Grammar

Owner: `Med Auto Grant`
Purpose: `quality_autonomy_family_grammar_active_spec`
State: `active_current_spec`
Machine boundary: 本文是人读 active spec。机器真相归 quality/autonomy schemas、source、tests、stage contracts 与 `contracts/runtime-program/current-program.json`。
Last reviewed: `2026-07-10`

## Quality Surfaces

- `grant-quality-scorecard` 持有 workspace-version quality judgment。
- `grant-quality-closure-dossier` 从 scorecard派生 closure packages，不建立第二条评分路径。
- `grant-quality-diff` 比较版本间 score、dimension、issue lineage 与 evidence movement。
- critique/mainline authoring pass 可以消费这些 MAG-owned quality surfaces；OPL/provider completion不能生成 quality/export verdict。

对应 schema：

- `schemas/v1/grant-quality-scorecard.schema.json`
- `schemas/v1/grant-quality-closure-dossier.schema.json`
- `schemas/v1/grant-quality-diff.schema.json`

AI-backed candidate status 必须携带独立 review provenance；projection-only 或 reviewer evidence 缺失时保持 fail closed。

## Autonomy Boundary

`execute-grant-autonomy-controller` 当前是 thin direct adapter，不是 long-running scheduler。Controller v4：

- 读取 request identity 与可选 OPL stage-attempt owner chain；
- 不运行 discovery/profile/intake/mainline/quality callback loop；
- 不拥有 budget cycle、rollback、resume、attempt ledger 或 stage transition；
- 返回 `failed_closed`、body-free workspace identity 与 MAG typed blocker；
- 有合法 OPL attempt 时要求通过 OPL runtime controller继续；缺少 attempt 时要求补齐 OPL provider owner chain。

对应 schema：

- `schemas/v1/grant-autonomy-controller-input.schema.json`
- `schemas/v1/grant-autonomy-controller-report.schema.json`

Report 必须包含 `workspace_identity`、`controller_execution_boundary` 与 `authority_return`。它不再包含旧 `controller_plan`、`tranche_history`、closure queue 或 private quality evaluator output。

## Family Grammar

`grant_family_registry.py`、project profile selector 与 workspace grammar contracts 持有 common grammar、funder profile 与 target-lock semantics。已锁定 funding call 后，authoring/quality/package path不得 opportunistic切换 funder。

旧 `grant_governance_adapter.py` 无 production caller，已随 private autonomy controller planning退役。Family-specific policy 继续作为 declarative profile/context输入，由具体 grant stage 与 quality owner消费，不恢复 controller-local hydration 或 closure-queue排序层。

## Evidence Boundary

Schema、tests、controller typed blocker 或 OPL conformance pass 只证明对应 contract/structural gate；不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。
