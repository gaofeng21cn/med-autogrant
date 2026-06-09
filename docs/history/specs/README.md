# 历史 Specs

Owner: `Med Auto Grant`
Purpose: `historical_specs_index`
State: `history_index`
Machine boundary: 本文是人读历史 specs 索引。历史 specs 只保存形成过程、tombstone 和 provenance；机器面必须使用当前 contracts/schema/source path、CLI/API behavior、runtime receipt 或语义化 `human_doc:*` id。

本索引是旧技术 specs 与 tranche 记录的历史入口。纯历史 activation package、future P5、runtime-first R/P tranche、post-R5A fail-closed hardening、退役 provider proof、tombstone 和 superseded handoff 文件都归档在本目录。`docs/specs/` 只保留 active current spec、support current-truth record 和 integration reference。

阅读旧 program 背景时从这里进入。当前真相请回到 [Specs 索引](../../specs/README.md)、核心五件套与 `current-program.json`。

目录级生命周期信号：

- owner：MAG 维护者。
- purpose：保留旧 specs、activation package、provider proof、tombstone 和 path-stable provenance 的历史入口。
- state：`history`。
- machine boundary：本目录只做人读 provenance。机器面必须使用当前 contracts/schema/source path、CLI/API behavior、runtime receipt 或语义化 `human_doc:*` id。

本目录下没有单独 lifecycle 头的历史 spec 默认继承上面的目录级信号。旧 `Current Truth`、`Activation Status`、Hermes/Gateway/local-runtime wording 和 dated completion claim 都不能覆盖当前核心五件套、active gap plan、contracts/schema/source 与 `current-program.json`。

本归档入口按语义主题承接历史记录，不再维护日期顺序或逐文件长清单：

| 主题 | 本目录保留的内容 | 当前 owner / 阅读动作 |
| --- | --- | --- |
| Foundation、object model、early mainline 与 OMX bridge | MAG 早期顶层设计、NSFC 主流程、对象模型和旧 Codex App / OMX 交接 provenance。 | 当前 MAG role、runtime owner、OPL/Temporal 边界和 active specs 回到核心五件套、`../../specs/README.md`、`../../specs/specs_lifecycle_map.md` 与 `current-program.json`。 |
| Authoring、review、rollback 与 verification tranche | P2/P3/P4 grant authoring、mentor verdict、revision、rollback、verification gate 和 checkpoint surface 形成过程。 | 当前 authoring route、quality verdict、completion semantics 和 verification entry 回到 active/current specs、source/contracts/tests 与 `current-program.json`。 |
| Runtime-first、local-runtime、Gateway/federation 与 provider proof | R/P/post-R5A runtime-productization packages、local-runtime hardening、honest-stop、Gateway/federation future activation、Hermes-backed proof 和 upstream Hermes reset records。 | 只作为 retired provider proof / migration lesson。默认 runtime owner、provider-backed substrate、queue、attempt ledger、App/workbench 和 executor adapter 边界回到 OPL/core docs、active gap plan、contracts/source/tests。 |
| Package/export、hosted contract bundle 与 fail-closed hardening | final-package artifact bundle、hosted contract bundle、route checkpoint shape、workspace validator 和 package/export fail-closed hardening provenance。 | 当前 package/export authority、schema behavior 和 fail-closed gates 回到 package/export source、schemas、tests、support record 与 owner receipts；不恢复旧 hosted runtime 或 Gateway route。 |
| Product-entry、OPL handoff、hosted caller 和 route snapshots | lightweight product-entry envelope、schema-backed product status、grant user-loop、hosted caller consumption、author-side routing snapshot 和 OPL alignment snapshots。 | 当前 product-entry / package support 读法回到 `../../specs/product-entry-support-record.md`、core docs、active gap plan、contracts/schema/source 与 `current-program.json`。 |
| Tombstones and no-resurrection proof | Hermes-native critique proof tombstone and path-stable retired-surface evidence refs that are still used by contracts/source/tests. | Keep as history/provenance only. Machine refs may point here for tombstone evidence, but that does not elevate the historical spec into current truth. |

Active specs 继续列在 [Specs 索引](../../specs/README.md)。
若 dated spec 与核心文档或 `current-program.json` 冲突，除非它被明确列为 active boundary record，否则按 provenance 处理。

## 压缩记录

- author-side route / executor envelope / pending handoff 历史 specs 已压缩为本主题索引和 coverage ledger 记录；原 4 个逐阶段 route/handoff 历史文件已删除。当前 route truth 回到 `../../specs/2026-04-13-full-grant-authoring-executor-current-truth.md`、`../../specs/2026-04-13-critique-codex-cli-executor-current-truth.md`、`../../specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`、`../../specs/product-entry-support-record.md`、`src/med_autogrant/domain_runtime_parts/contracts.py`、`src/med_autogrant/product_entry_parts/entry.py`、`schemas/v1/executor-routing-contract.schema.json`、`tests/test_domain_runtime.py`、product-entry cases、hosted bundle tests、核心五件套和 `current-program.json`。
- 该压缩只退役历史 route snapshot / stage action envelope / pending handoff matrix 的 Markdown 长清单，不改变 `direction_screening -> hosted_contract_bundle` landed route catalog、Codex CLI 默认 executor、schema-backed `executor_routing_contract`、product-entry / hosted bundle route output 或 negative guards。不要恢复 `runtime-run`、`runtime-resume`、local run journal、`stage_action_envelope` durable path、`handoff_requirements`、pending route matrix、Gateway/Hermes default-runtime wording、compatibility route alias 或旧 public CLI surface。
- 2026-04-06 MAG foundation / NSFC main flow / top-level design 历史 specs 已压缩为本主题索引和 coverage ledger 记录；原 2 个早期 foundation 历史文件已删除。当前 truth 回到 `contracts/runtime-program/current-program.json`、核心五件套、`../../references/med-auto-grant-ideal-state.md`、`../../active/mag-ideal-state-cross-repo-gap-plan.md`、`../../specs/README.md`、`../../specs/specs_lifecycle_map.md`、`agent/` Declarative Grant Pack、stage control plane、quality gates、source/contracts/tests 与 MAG-owned owner receipt / typed blocker / package authority surfaces。
- 该压缩只退役早期 Grant Foundry / NSFC 流程 / host-agent / same-repo HITL / local runtime 形成过程的长篇 Markdown provenance，不改变 grant stage pack、authoring route、fundability / quality / export verdict、package authority、memory accept/reject、owner receipt 或 typed blocker 行为。不要把这些历史文件重建为 active spec、Grant Foundry roadmap、host-agent/local-runtime 默认路径、同仓 HITL 产品计划、readiness evidence、compatibility entry 或当前 truth owner。
- P2/P3/P4 authoring / review / rollback / verification 历史 specs 已压缩为本主题索引和 coverage ledger 记录；原 8 个逐 tranche 长正文历史文件已删除。当前 truth 回到 `contracts/runtime-program/current-program.json`、核心五件套、`../../active/mag-ideal-state-cross-repo-gap-plan.md`、`../../specs/README.md`、`../../specs/specs_lifecycle_map.md`、active current specs、formal-entry / durability support specs、source/contracts/schemas/tests、quality / route / verification owners、package/export support record 和 owner receipts。
- 该压缩只退役 P2.A intake-direction-question、P2.B argument-fit-outline、P2.C draft-critique-revision skeleton、P3.A mentor verdict、P3.B re-review、P3.C forced rollback / presubmission gate、P4.A verification gate、P4.B checkpoint surface 的逐文件 Markdown 长清单，不改变 current route objects、quality verdict、authoring completion semantics、verification checkpoint behavior、schema/source/test 行为，也不恢复旧 `Current Truth` 文件为 current owner、compatibility spec、runtime owner、HITL claim、Gateway/federation route 或 prose oracle。
- runtime-first R1-R5 boundary map 与 R1.A / R2.A / R3.A / R4.A / R5.A activation package 历史 specs 已压缩为本主题索引和 coverage ledger 记录；原 6 个逐 slice 长正文历史文件已删除。当前 truth 回到 `contracts/runtime-program/current-program.json`、核心五件套、`../../active/mag-ideal-state-cross-repo-gap-plan.md`、`../../specs/README.md`、`../../specs/specs_lifecycle_map.md`、`docs/history/specs/2026-04-08-runtime-first-productization-program.md`、`docs/history/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`、package/export source、schemas、tests、product-entry manifest 和 owner receipts。
- 该压缩只退役 R1-R5 boundary / local main loop / artifact bundle / critique revision executor / final freeze / hosted-friendly session 的逐文件 Markdown activation 长清单，不改变 `stage-route-report`、`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle`、schema/source/test 行为，也不恢复 `runtime-run`、`runtime-resume`、local run journal、attempt ledger、Gateway/local-manager route、Hermes default-runtime wording、hosted runtime claim、compatibility alias 或旧 public CLI surface。
- post-R5A local-runtime / worktree-root / route-checkpoint 历史 specs 已压缩为本主题索引和 coverage ledger 记录；原 5 个逐 slice 历史文件已删除。当前 truth 回到 `contracts/runtime-program/current-program.json`、`src/med_autogrant/route_report.py`、`src/med_autogrant/control_plane.py`、`src/med_autogrant/domain_runtime_parts/contracts.py`、`src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`、`src/med_autogrant/mainline_status.py`、`tests/test_cli_validate_workspace_revision_cases.py`、`tests/test_domain_entry.py`、`tests/test_hosted_contract_bundle_control_plane.py`、核心五件套、active gap plan、runtime support index 和 active/support specs lifecycle map。
- 该压缩只退役 post-R5A local runtime 形成过程的逐文件 Markdown 长清单，不恢复 `runtime-run`、`runtime-resume`、`run-local`、`probe-upstream-hermes`、local journal、attempt ledger、main-worktree `.runtime-program` fallback、Gateway/local-manager route 或 hosted runtime claim，也不改变 `stage-route-report`、CURRENT_PROGRAM contract、hosted-contract-bundle 或 package/export 行为。
- `2026-04-10-post-r5a-final-package-*.md` 中的 final-package artifact-bundle per-field fail-closed activation packages 已压缩为本主题索引和 coverage ledger 记录；原 15 个逐字段历史文件已删除。当前 fail-closed truth 回到 `src/med_autogrant/artifact_bundle_validation.py`、`src/med_autogrant/final_package.py`、`schemas/v1/submission-ready-package.schema.json`、`schemas/v1/hosted-contract-bundle.schema.json`、`tests/test_final_package.py` 和 package/export owner docs。
- 该压缩只退役历史长清单文件，不改变 `build-final-package` / `build-artifact-bundle` / `build-hosted-contract-bundle` 行为，不授权 hosted runtime、Gateway route、grant readiness、fundability verdict、quality/export verdict 或 submission-ready approval。
- `2026-04-10-post-r5a-hosted-contract-bundle-*final-package*.md` 中的 hosted-contract-bundle final-package per-field fail-closed activation packages 已压缩为本主题索引和 coverage ledger 记录；原 6 个逐字段历史文件已删除。当前 fail-closed truth 回到 `src/med_autogrant/hosted_contract_bundle.py`、`src/med_autogrant/final_package_validation.py`、`schemas/v1/hosted-contract-bundle.schema.json`、`tests/test_hosted_contract_bundle.py` 和 `tests/test_hosted_contract_bundle_checkpoint_cases.py`。
- 该压缩只退役历史长清单文件，不改变 `build-hosted-contract-bundle` 行为，不授权 public hosted runtime、App release readiness、production readiness、Gateway/local-manager route 或 hosted caller long-soak completion。
- Hermes-backed runtime substrate / capability split 与 upstream Hermes truth-reset / fast-cutover provider-proof 历史 specs 已压缩为本主题索引和 coverage ledger 记录；原 5 个逐文件长正文已删除。当前 runtime owner、executor registry、explicit `hermes_agent` proof lane 和 no-resurrection truth 回到核心五件套、`../../active/mag-ideal-state-cross-repo-gap-plan.md`、`../../specs/README.md`、`../../specs/specs_lifecycle_map.md`、`contracts/runtime-program/current-program.json`、executor/default contracts、source/tests 和仍被机器面引用的 `2026-04-13-hermes-native-critique-proof-tombstone.md`。
- 该压缩只退役旧 Hermes-backed default provider proposal、upstream fast-cutover board、repo-local runtime ladder 和 Gateway/local-manager planning 长正文，不改变 `hermes_agent` 作为显式非默认 executor/proof/provenance lane 的行为，不恢复 `runtime-run`、`runtime-resume`、`probe-upstream-hermes`、local journal、attempt ledger、Hermes-backed default provider、Gateway/local-manager route、compatibility bridge 或 production hosted readiness claim。
- hosted caller / OPL handoff / P4 product-entry support 历史 specs 已压缩为本主题索引、`../../specs/product-entry-support-record.md` 和 coverage ledger 记录；原 9 个逐文件长正文已删除。当前 product-entry、product status、direct-entry、user-loop、manifest、hosted contract bundle support 和 package/export support truth 回到核心五件套、`../../active/mag-ideal-state-cross-repo-gap-plan.md`、`../../specs/README.md`、`../../specs/specs_lifecycle_map.md`、`../../specs/product-entry-support-record.md`、`contracts/runtime-program/current-program.json`、product-entry manifest、schemas/source/tests 和 owner receipts。
- 该压缩只退役 hosted caller proof、lightweight OPL handoff、OPL-aligned phase map、P4A/P4B/P4C/P4E/P4F support specs 的逐文件 Markdown 长清单，不改变 `build-product-entry`、`build-hosted-contract-bundle`、mainline status、grant user loop、product-entry manifest 或 submission package behavior，不授权 public hosted runtime、App/workbench readiness、production readiness、Gateway/local-manager route、grant readiness、fundability verdict、quality/export verdict 或 portal submission completion。

本页不再维护逐文件长清单。需要找具体历史文件时，按文件名前缀或主题运行：

```bash
find docs/history/specs -maxdepth 1 -type f | sort
```

需要判断生命周期时，回到 [Specs 生命周期地图](../../specs/specs_lifecycle_map.md)。需要把历史规则恢复为 current owner 时，先抽取到核心五件套、active gap plan、support record、contract/schema/source 或对应薄入口；不要在历史文件中追加当前状态。
