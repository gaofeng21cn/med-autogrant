# Durability Model Support Record

Owner: `Med Auto Grant`
Purpose: `durability_boundary_support_record`
State: `support_current_truth`
Machine boundary: 本文是人读支撑记录。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API behavior、workspace/runtime artifact root、owner receipts 和语义化 `human_doc:*` id。
Last reviewed: `2026-06-12`

## 当前读法

本文件保留早期 durability vocabulary 的 path-stable 支撑位置，但不再承载 local runtime / journal / attempt ledger 的 current truth。MAG 当前 durability 分为四层：

| 层 | 当前 owner | 持久化边界 |
| --- | --- | --- |
| Repo current truth | MAG repo | `contracts/runtime-program/current-program.json`、schemas、contracts、source、核心五件套、active specs。 |
| Grant workspace truth | MAG workspace | `workspace.json`、draft、critique、revision、quality report、package/export artifacts、memory receipt、owner receipt。 |
| User-level runtime state | 用户级 runtime-state | `$CODEX_HOME/projects/med-autogrant/runtime-state/` 下的 log、report、prompt、handoff state、runtime receipt evidence。 |
| OPL generated/hosted runtime | OPL Framework | stage attempt ledger、typed queue、attempt lifecycle、wakeup/resume、retry/dead-letter、operator projection、Temporal-backed production substrate。 |

MAG repo source 不保存真实 memory body、grant artifact private evidence、fundability verdict body、authoring quality verdict body、submission-ready export verdict body 或 runtime receipt instance。

## 当前 durable surfaces

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer。
- Product-entry manifest、domain-handler export、`runtime_control`、`runtime_continuity`、artifact locator、domain memory descriptor、owner receipt contract 和 lifecycle guarded apply proof 只输出 refs、receipt shape、typed blocker、verdict refs 与 safe action metadata。
- `workspace quality-scorecard`、`workspace quality-diff`、`grant-quality-closure-dossier` 和 autonomy controller report 是结构化治理面；它们不能机械生成 fundability-ready、quality-ready、export-ready 或 production-soak verdict。
- User-level runtime-state 可保存本机运行输出和 receipt evidence，但不是 repo-tracked product runtime，也不能单独发明 formal entry。

## 已退役 durability wording

以下旧 durable surfaces 只作为 history/provenance 阅读，不能恢复为 current owner：

- local run journal
- local attempt ledger
- repo-owned scheduler daemon
- `runtime-run --journal`
- `runtime-resume --journal`
- Hermes/Gateway/local-manager default path
- `.runtime-program/**` repo-local state

需要解释旧线索时，从 [历史 specs](../history/specs/README.md) 或 `docs/history/**` 进入；需要判断当前 runtime owner 时，以 `docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/active/mag-ideal-state-cross-repo-gap-plan.md` 和 machine-readable contracts 为准。

## Review order

当前 reviewer 应按下面顺序读取 durability 边界：

1. [当前状态](../status.md)
2. [架构](../architecture.md)
3. [不变量](../invariants.md)
4. [Specs 生命周期地图](./specs_lifecycle_map.md)
5. [`current-program.json`](../../contracts/runtime-program/current-program.json)

历史文件若与这些 owner surface 冲突，按 provenance 处理。
