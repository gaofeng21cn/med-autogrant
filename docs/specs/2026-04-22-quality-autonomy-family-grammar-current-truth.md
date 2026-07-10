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

MAG 不再提供 `execute-grant-autonomy-controller` 公共 facade、runtime method 或 controller schema。该 facade 无论输入是否合法都只返回“交给 OPL runtime controller”的 blocker，没有执行 grant authority 行为，因此已直接退役。

当前 autonomy 边界固定为：

- OPL 持有 stage residency、attempt ledger、budget/retry/resume、queue 与 stage transition；
- MAG 只执行 grant-native pass、quality/fundability/export/package authority 与 memory/receipt authority target；
- repo-local `critique-revision-loop` 与 `authoring-mainline-loop` 已物理退役；OPL StageRun/Runway 通过声明化 stage manifest 调用 MAG single-pass handlers，并持有 owner chain、cycle/rollback/exhaustion 与 output-dir 编排；
- stage closeout 只返回 MAG owner receipt、typed blocker 或 no-regression evidence ref；
- CLI 不保留 autonomy alias、wrapper 或兼容测试。

## Family Grammar

`grant_family_registry.py`、project profile selector 与 workspace grammar contracts 持有 common grammar、funder profile 与 target-lock semantics。已锁定 funding call 后，authoring/quality/package path不得 opportunistic切换 funder。

旧 `grant_governance_adapter.py` 与私有 autonomy controller 均无 production authority 行为，已经退役。Family-specific policy 继续作为 declarative profile/context 输入，由具体 grant stage 与 quality owner 消费，不恢复 controller-local hydration、closure queue 或第二控制面。

## Evidence Boundary

Schema、tests、owner typed blocker 或 OPL conformance pass 只证明对应 contract/structural gate；不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。
