# 历史 Specs

本索引是旧技术 specs 与 tranche 记录的历史入口。纯历史 activation package、future P5、runtime-first R/P tranche、post-R5A fail-closed hardening、退役 provider proof、tombstone 和 superseded handoff 文件都归档在本目录。`docs/specs/` 只保留 active current spec、support current-truth record 和 integration reference。

阅读旧 program 背景时从这里进入。当前真相请回到 [Specs 索引](../../specs/README.md)、核心五件套与 `current-program.json`。

生命周期信号：

- `owner`：MAG 维护者。
- `purpose`：保留旧 specs、activation package、provider proof、tombstone 和 path-stable provenance 的历史入口。
- `state`：`history`。
- `machine boundary`：本目录只做人读 provenance。机器面必须使用当前 contracts/schema/source path、CLI/API behavior 或语义化 `human_doc:*` id。

由本归档入口承接的历史分组：

- 2026-04-06 foundation design 与 OMX bridge 记录：`./2026-04-06-*.md`
- 2026-04-07 P2/P3 mainline 与 review-gate tranche 记录：已归档到本目录的 `./2026-04-07-p2*.md` 与 `./2026-04-07-p3a*.md`；formal-entry 与 durability support guard 仍留在 `../../specs/`。
- 2026-04-08 P3/P4 rollback、verification gate 与 checkpoint tranche 记录：已归档到本目录的 `./2026-04-08-p3*.md` 与 `./2026-04-08-p4*.md`；P5 future activation 与 R1/R3 runtime-productization packages 位于本目录的 `./2026-04-08-p5*.md`、`./2026-04-08-r*.md` 和 `./2026-04-08-runtime-first-*.md`。
- 2026-04-09 R3/R5 与 post-R5A hardening briefs：`./2026-04-09-*.md`
- 2026-04-10 post-R5A fail-closed hardening activation packages 与 local-runtime walkthrough：`./2026-04-10-post-r5a-final-package-*.md`、`./2026-04-10-post-r5a-hosted-contract-bundle-*.md`、`./2026-04-10-post-r5a-local-runtime-validation-*.md`、`./2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`、`./2026-04-10-post-r5a-revised-*.md`、`./2026-04-10-post-r5a-stage-route-*.md` 和 `./2026-04-10-post-r5a-worktree-aware-*.md`
- 2026-04-11 Hermes/reset 与 local-runtime closeout 记录：已退役 provider proof 位于本目录的 `2026-04-11-hermes-backed-*.md` 与 `2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`；local-runtime honest-stop 记录位于 `./2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`，只作为 fail-closed / honest-stop provenance 阅读。
- 2026-04-12 hosted-caller、OPL alignment、product-entry、route snapshot 与 handoff 记录：已退役 upstream Hermes fast-cutover board/current-truth、author-side executor routing snapshot、OPL alignment historical snapshot、hosted caller consumption、hosted contract bundle export 与 lightweight product-entry handoff 记录均位于本目录，只作为 provenance 阅读；当前 contract export、product-entry、OPL generated/hosted caller 和 App/workbench 边界回到核心文档、active gap plan、contracts/schema/source 与 `current-program.json`。
- 2026-04-13 authoring route landing、默认 executor vocabulary 与 submission-ready 记录：`../../specs/2026-04-13-*.md`；已退役 Hermes-native proof tombstone：`./2026-04-13-hermes-native-critique-proof-tombstone.md`

Active specs 继续列在 [Specs 索引](../../specs/README.md)。
若 dated spec 与核心文档或 `current-program.json` 冲突，除非它被明确列为 active boundary record，否则按 provenance 处理。

已物理归档的历史 specs 包括：

- [Med Auto Grant top-level design](./2026-04-06-med-auto-grant-top-level-design.md)
- [Med Auto Grant mainline and OMX bridge](./2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
- [NSFC main flow and critique loop](./2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [Object model schema v1](./2026-04-06-object-model-schema-v1.md)
- [P2.A intake-direction-question mainline provenance](./2026-04-07-p2a-intake-direction-question-mainline-current-truth.md)
- [P2.B argument-fit-outline mainline provenance](./2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md)
- [P2.C draft-critique-revision skeleton provenance](./2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md)
- [P3.A mentor verdict contract freeze provenance](./2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md)
- [P3.B revision transition and re-review hardening provenance](./2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md)
- [P3.C forced rollback and presubmission gate provenance](./2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md)
- [P4.A verification gate surface provenance](./2026-04-08-p4a-verification-gate-surface-current-truth.md)
- [P4.B verification OS and checkpoint surface provenance](./2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md)
- [Runtime-first productization program](./2026-04-08-runtime-first-productization-program.md)
- [Runtime-first R1 to R5 boundary map](./2026-04-08-runtime-first-r1-to-r5-boundary-map.md)
- [Post-R5A local runtime walkthrough and output consistency](./2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md)
- [Post-R5A local runtime upper-bound honest stop](./2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md)
- [OPL aligned ideal target and phase map historical snapshot](./2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md)
- [Hermes-backed runtime capability migration map](./2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md)
- [Hermes-backed runtime substrate program](./2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md)
- [Upstream Hermes-Agent truth reset](./2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md)
- [Upstream Hermes-Agent fast cutover board](./2026-04-12-upstream-hermes-agent-fast-cutover-board.md)
- [Upstream Hermes-Agent fast cutover current truth](./2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md)
- [Hosted caller consumption proof provenance](./2026-04-12-hosted-caller-consumption-proof-current-truth.md)
- [Hosted contract bundle entry and route catalog provenance](./2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md)
- [Lightweight product-entry and OPL handoff provenance](./2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md)
