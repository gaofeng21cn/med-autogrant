# Quality, OPL Autonomy Boundary, And Family Grammar

Owner: `Med Auto Grant`
Purpose: `quality_autonomy_family_grammar_active_spec`
State: `active_current_spec`
Machine boundary: 本文是人读 active spec。机器真相归 quality schemas、source、tests、OPL-hosted stage contracts 与 `contracts/runtime-program/current-program.json`。
Last reviewed: `2026-07-10`

## Quality Surfaces

- `grant-quality-scorecard` 持有 workspace-version quality judgment。
- `grant-quality-closure-dossier` 从 scorecard派生 closure packages，不建立第二条评分路径。
- `grant-quality-diff` 比较版本间 score、dimension、issue lineage 与 evidence movement。
- MAG single-pass authoring handlers 可以消费这些 MAG-owned quality surfaces；多步 critique/revision 与 authoring mainline 编排归 OPL StageRun/Runway，OPL/provider completion不能生成 quality/export verdict。

对应 schema：

- `schemas/v1/grant-quality-scorecard.schema.json`
- `schemas/v1/grant-quality-closure-dossier.schema.json`
- `schemas/v1/grant-quality-diff.schema.json`

AI-backed candidate status 必须携带独立 review provenance；projection-only 或 reviewer evidence 缺失时保持 fail closed。

## Autonomy Boundary

当前 autonomy 分工为：

- OPL 持有 stage residency、attempt ledger、budget/retry/resume、queue 与 stage transport；decisive Codex Attempt 持有语义 stage route，OPL StageRun controller 只物化 transition；
- MAG 提供声明式 Stage Pack、single-pass grant handlers，以及 quality/fundability/export/package、memory 和 receipt authority；
- OPL StageRun/Runway 通过 Stage manifest 调用 MAG handler，并持有 owner chain、cycle/rollback/exhaustion 与 output-dir 编排；
- stage closeout 只返回 MAG owner receipt、typed blocker 或 no-regression evidence ref；
- CLI 通过显式静态 dispatch 调用当前 authority/runtime function。

## Family Grammar

`grant_family_registry.py`、project profile selector 与 workspace grammar contracts 持有 common grammar、funder profile 与 target-lock semantics。锁定 funding call 后，authoring、quality 与 package Stage 都沿用该 target。Family-specific policy 作为 declarative profile/context 输入，由具体 grant Stage 与 quality owner 消费。

## Evidence Boundary

Schema、tests、owner typed blocker 或 OPL conformance pass 只证明对应 contract/structural gate；不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。
