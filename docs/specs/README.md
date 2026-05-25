# Specs 索引

Owner: `Med Auto Grant`
Purpose: `specs_index`
State: `current_index`
Machine boundary: 本文是人读 specs 索引。机器消费者必须使用 `contracts/runtime-program/current-program.json`、schemas、source files、CLI/API behavior 或语义化 `human_doc:*` id。

本目录保留 `Med Auto Grant` 的当前技术记录层。它不是旧
Hermes/Gateway/local-runtime 文档的兼容保留区；明确 superseded 的 provider
proof、activation package、local-runtime closeout 和 tombstone 进入
`docs/history/specs/`。

生命周期信号：

- `owner`：MAG maintainers，以及每份 active spec 对应的 runtime/product-governance lane。
- `purpose`：索引 active current-truth records，并把较早 dated records 导向历史阅读入口。
- `state`：下方列出的 active specs 为 `current`；仍留在本目录的 dated specs
  只能是 support current-truth、integration reference 或 path-stable provenance。
  已物理移动到 `../history/specs/` 的 dated specs 为 `history`。
- `machine boundary`：specs 是人读 current-truth records。机器消费者应使用 `contracts/runtime-program/current-program.json`、schema、source file 或语义化 `human_doc:*` 标识，而不是依赖 prose path。

当前优先级最高、仍由 docs guide 或 status 直接引用的 active current-truth specs 只有四份：

- [Critique executor vocabulary current truth](./2026-04-13-critique-codex-cli-executor-current-truth.md)
- [AI-first 质量边界 current truth](./2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./2026-04-22-quality-autonomy-family-grammar-current-truth.md)

密集 specs 组合的生命周期分类见 [Specs Lifecycle Map](./specs_lifecycle_map.md)。编辑或移动任何 dated spec 前，先用这份 map 的 file-level lifecycle table 区分 active record、support current-truth record、integration reference、historical activation package、historical route snapshot 与 superseded provider proof。

当前 specs lifecycle map 已覆盖 `docs/specs/*.md` 与 `docs/history/specs/*.md` 的文件级归位。保留在本目录的 dated specs 只按两类处理：

- `active_current_spec`：仅四份，承担明确命名的当前边界。
- `support_current_truth`：只在仍 current 的 subsection 内支撑 schema、product-entry、package/export 或 executor routing 读法。

`2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
与
`2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`
已经移动到 `../history/specs/`。它们只记录 post-R5A local-runtime
closeout / honest-stop provenance，不再位于 current specs 层。
`2026-04-07-p2*`、`2026-04-07-p3a*`、`2026-04-08-p3*` 与
`2026-04-08-p4*` 也已经移动到 `../history/specs/`。它们只记录
早期 authoring-flow、review/rollback 与 verification gate 形成过程；当前 route、quality、
checkpoint 和验证边界由核心五件套、active specs、contracts/schema/source 与
`current-program.json` 持有。

因此，本目录不再保留纯历史 activation package、R/P/post-R5A tranche 或 fail-closed hardening notes。直接打开任何 dated support spec 时，第一屏 lifecycle note 优先于标题里的 `Current Truth`、`Activation Package` 或 tranche label。
`2026-04-12-author-side-executor-routing-contract-current-truth.md` 已移动到 `../history/specs/`，因为当前 route catalog 已由 `2026-04-13-full-grant-authoring-executor-current-truth.md`、contracts、schema 和 source 接管。
`2026-04-12-hosted-caller-consumption-proof-current-truth.md`、
`2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md` 与
`2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`
也已经移动到 `../history/specs/`。它们只记录旧 hosted / OPL handoff
形成过程；当前 contract export、product-entry、OPL generated/hosted caller 和
App/workbench 边界由核心五件套、active gap plan、contracts/schema/source 与
`current-program.json` 持有。

`contracts/runtime-program/current-program.json` 仍是完整 repo-tracked truth-surface 清单的 canonical pointer。它可能引用少量 support `human_doc:*` 或 specs，但这种引用不提升整份 dated spec 为当前 owner。Hermes-backed、Hermes reset、Gateway、future P5、runtime-first activation、post-R5A hardening 和旧 provider specs 只保留 history / provenance / audit path；只有 lifecycle map 明确列为 active 的 subsection 才能作为当前边界阅读。已经归档到 `../history/specs/` 的文件不再是 `docs/specs/` support surface。

当前 OPL 口径集中在核心文档：OPL 是 stage-led、以 Agent executor 为最小执行单位的完整运行框架，可以消费 MAG-owned descriptor/projection。旧 spec 中出现的 `OPL Runtime Manager`、Temporal target、上游 Hermes 作为默认 provider 的旧口径、active adapter、gateway、compatibility bridge、local journal 或 attempt ledger 说法，除非被当前 owner 文档显式提升，否则都按 provider-specific 迁移背景或历史 proof 阅读；不得据此恢复旧接口、旧 CLI alias、旧测试聚合入口或旧 provider owner。

`hosted contract bundle` 继续是 integration/reference export surface。Hosted runtime、Web UI、public MCP runtime 与外部官网提交各自需要当前 owner evidence；旧 gateway/federation wording 只作为 history/provenance 阅读，不再作为目标产品面。

更早的 dated `P*`、`R*`、`post-R5A`、activation-package、migration-board 与已被 supersede 的 tranche current-truth 文件属于历史技术记录，已移动到历史目录。统一阅读入口是：

- [历史 specs 索引](../history/specs/README.md)

当前产品真相不能只按文件名日期取最新 spec。请先读核心五件套和 `current-program.json`，再按需要读取 active specs 所冻结的具体边界。历史文件可以保留旧任务 wording、旧路径和已被 supersede 的 tranche label。
