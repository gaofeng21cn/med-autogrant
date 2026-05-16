# 历史 Specs

本索引是旧技术 specs 与 tranche 记录的历史入口。部分 path-stable
源文件仍保留在 `docs/specs/`，这样旧审计链接、current-program 指针和历史绝对路径说明仍可读；明确退役的 provider proof、tombstone 和 superseded
handoff 文件可以物理归档到本目录。

阅读旧 program 背景时从这里进入。当前真相请回到 [Specs 索引](../../specs/README.md)、核心五件套与 `current-program.json`。

生命周期信号：

- `owner`：MAG 维护者。
- `purpose`：保留旧 specs、activation package、provider proof、tombstone 和 path-stable provenance 的历史入口。
- `state`：`history`。
- `machine boundary`：本目录只做人读 provenance。机器面必须使用当前 contracts/schema/source path、CLI/API behavior 或语义化 `human_doc:*` id。

由本归档入口承接的历史分组：

- 2026-04-06 foundation design 与 OMX bridge 记录：`../../specs/2026-04-06-*.md`
- 2026-04-07 P1/P2/P3 entry、durability 与 mainline tranche 记录：`../../specs/2026-04-07-*.md`
- 2026-04-08 verification、P5 future activation 与 R1/R3 runtime-productization packages：`../../specs/2026-04-08-*.md`
- 2026-04-09 R3/R5 与 post-R5A hardening briefs：`../../specs/2026-04-09-*.md`
- 2026-04-10 post-R5A fail-closed hardening activation packages：`../../specs/2026-04-10-*.md`
- 2026-04-11 Hermes/reset 与 local-runtime closeout 记录：已退役 provider proof 位于本目录的 `2026-04-11-hermes-backed-*.md` 与 `2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`；仍留在 `../../specs/` 的 2026-04-11 local-runtime honest-stop 记录只作为 fail-closed / honest-stop provenance 阅读。
- 2026-04-12 hosted-caller、OPL alignment、product-entry 与 handoff 记录：已退役 upstream Hermes fast-cutover board/current-truth 位于本目录；仍留在 `../../specs/` 的 hosted contract、caller consumption、OPL alignment 和 product-entry 细节只作为 support/provenance 阅读，旧 gateway/federation/provider 说法按历史处理。
- 2026-04-13 authoring route landing、默认 executor vocabulary 与 submission-ready 记录：`../../specs/2026-04-13-*.md`；已退役 Hermes-native proof tombstone：`./2026-04-13-hermes-native-critique-proof-tombstone.md`

Active specs 继续列在 [Specs 索引](../../specs/README.md)。
若 dated spec 与核心文档或 `current-program.json` 冲突，除非它被明确列为 active boundary record，否则按 provenance 处理。

已物理归档的 provider-proof specs：

- [Hermes-backed runtime capability migration map](./2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md)
- [Hermes-backed runtime substrate program](./2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md)
- [Upstream Hermes-Agent truth reset](./2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md)
- [Upstream Hermes-Agent fast cutover board](./2026-04-12-upstream-hermes-agent-fast-cutover-board.md)
- [Upstream Hermes-Agent fast cutover current truth](./2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md)
