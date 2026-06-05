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

由本归档入口承接的历史分组：

- 2026-04-06 foundation design 与 OMX bridge 记录：`./2026-04-06-*.md`
- 2026-04-07 P2/P3 mainline 与 review-gate tranche 记录：已归档到本目录的 `./2026-04-07-p2*.md` 与 `./2026-04-07-p3a*.md`；formal-entry 与 durability support guard 仍留在 `../../specs/`。
- 2026-04-08 P3/P4 rollback、verification gate 与 checkpoint tranche 记录：已归档到本目录的 `./2026-04-08-p3*.md` 与 `./2026-04-08-p4*.md`；P5 future activation 与 R1/R3 runtime-productization packages 位于本目录的 `./2026-04-08-p5*.md`、`./2026-04-08-r*.md` 和 `./2026-04-08-runtime-first-*.md`。
- 2026-04-09 R3/R5 与 post-R5A hardening briefs：`./2026-04-09-*.md`
- 2026-04-10 post-R5A fail-closed hardening activation packages 与 local-runtime walkthrough：`./2026-04-10-post-r5a-final-package-*.md`、`./2026-04-10-post-r5a-hosted-contract-bundle-*.md`、`./2026-04-10-post-r5a-local-runtime-validation-*.md`、`./2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`、`./2026-04-10-post-r5a-revised-*.md`、`./2026-04-10-post-r5a-stage-route-*.md` 和 `./2026-04-10-post-r5a-worktree-aware-*.md`
- 2026-04-11 Hermes/reset 与 local-runtime closeout 记录：已退役 provider proof 位于本目录的 `2026-04-11-hermes-backed-*.md` 与 `2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`；local-runtime honest-stop 记录位于 `./2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`，只作为 fail-closed / honest-stop provenance 阅读。
- 2026-04-12 hosted-caller、OPL alignment、product-entry、route snapshot 与 handoff 记录：已退役 upstream Hermes fast-cutover board/current-truth、author-side executor routing snapshot、OPL alignment historical snapshot、hosted caller consumption、hosted contract bundle export 与 lightweight product-entry handoff 记录均位于本目录，只作为 provenance 阅读；当前 contract export、product-entry、OPL generated/hosted caller 和 App/workbench 边界回到核心文档、active gap plan、contracts/schema/source 与 `current-program.json`。
- 2026-04-12/13 P4 product-entry / package support 记录：`./2026-04-12-p4a-*`、`./2026-04-12-p4b-*`、`./2026-04-12-p4c-*`、`./2026-04-13-p4e-*` 和 `./2026-04-13-p4f-*`；当前 support 读法回到 `../../specs/product-entry-support-record.md`。
- 2026-04-13 authoring route landing、默认 executor vocabulary 与 submission-ready 记录：`../../specs/2026-04-13-*.md` 中的 active/support records；已退役 Hermes-native proof tombstone：`./2026-04-13-hermes-native-critique-proof-tombstone.md`

Active specs 继续列在 [Specs 索引](../../specs/README.md)。
若 dated spec 与核心文档或 `current-program.json` 冲突，除非它被明确列为 active boundary record，否则按 provenance 处理。

本页不再维护逐文件长清单。需要找具体历史文件时，按文件名前缀或主题运行：

```bash
find docs/history/specs -maxdepth 1 -type f | sort
```

需要判断生命周期时，回到 [Specs 生命周期地图](../../specs/specs_lifecycle_map.md)。需要把历史规则恢复为 current owner 时，先抽取到核心五件套、active gap plan、support record、contract/schema/source 或对应薄入口；不要在历史文件中追加当前状态。
