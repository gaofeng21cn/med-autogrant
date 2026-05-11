# Specs 索引

本目录保留 `Med Auto Grant` 的当前技术记录层。

生命周期信号：

- `owner`：MAG maintainers，以及每份 active spec 对应的 runtime/product-governance lane。
- `purpose`：索引 active current-truth records，并把较早 dated records 导向历史阅读入口。
- `state`：下方列出的 active specs 为 `current`；留在本目录用于路径 provenance 的较早 dated specs 为 `history`。
- `machine boundary`：specs 是人读 current-truth records。机器消费者应使用 `contracts/runtime-program/current-program.json`、schema、source file 或语义化 `human_doc:*` 标识，而不是依赖 prose path。

当前优先级最高、仍由 docs guide 或 status 直接引用的 active current-truth specs 是：

- [Critique executor vocabulary current truth](./2026-04-13-critique-codex-cli-executor-current-truth.md)
- [AI-first 质量边界 current truth](./2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./2026-04-22-quality-autonomy-family-grammar-current-truth.md)

密集 specs 组合的生命周期分类见 [Specs Lifecycle Map](./specs_lifecycle_map.md)。编辑或移动任何 dated spec 前，先用这份 map 区分 active record、support current-truth record 与 historical provenance。

`contracts/runtime-program/current-program.json` 仍是完整 repo-tracked truth-surface 清单的 canonical pointer。部分 route、executor-vocabulary、hosted-caller、product-entry 与 Hermes reset specs 仍留在本目录，是因为 current-program 或历史审计路径仍直接引用这些原路径。

当前 OPL 口径集中在核心文档：OPL 是 Codex-first、stage-led 的完整运行框架，可以消费 MAG-owned descriptor/projection。旧 spec 中出现的 `OPL Runtime Manager`、Temporal target、Hermes-first、active adapter、gateway 或 monorepo 说法，除非被当前 owner 文档显式提升，否则都按 provider-specific 迁移背景阅读。

`hosted contract bundle` 继续是 integration/reference export surface。hosted runtime、Web UI、public MCP runtime、外部官网提交和成熟 gateway/federation 各自需要当前 owner evidence。

更早的 dated `P*`、`R*`、`post-R5A`、activation-package、migration-board 与已被 supersede 的 tranche current-truth 文件属于历史技术记录。它们继续留在本目录作为 repo-tracked provenance，避免大范围重写旧审计路径；统一阅读入口改为：

- [历史 specs 索引](../history/specs/README.zh-CN.md)

当前产品真相不能只按文件名日期取最新 spec。请先读核心五件套和 `current-program.json`，再按需要读取 active specs 所冻结的具体边界。历史文件可以保留旧任务 wording、旧路径和已被 supersede 的 tranche label。
