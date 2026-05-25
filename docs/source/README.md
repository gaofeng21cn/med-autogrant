# Source 文档

Owner: `Med Auto Grant`
Purpose: `grant_source_workspace_support`
State: `active_support`
Machine boundary: 人读索引。Source truth 继续归 grant workspaces、funder/task inputs、schemas、source contracts 与 owner receipts。

本目录承接 workspace/source intake、funder/task material handling 和 source truth consumption 支撑。通用 workspace/source shell 候选应记录为 MAG-to-OPL 上收候选。

当前本目录只做 source/workspace 支撑索引；不复制 workspace truth、funder source state 或 source intake plan。新增内容必须保持真实 grant workspace、source body、memory body、artifact body 与 receipt instance 在 workspace/runtime artifact root 或用户级 runtime-state，repo source 只保存 schema、locator、policy、refs 和 no-forbidden-write 证据。

当前入口先看：

- [架构](../architecture.md)
- [当前状态](../status.md)
- [References](../references/README.md)

当前 OPL 可索引 source refs 入口是 `product-entry-manifest.source_provenance` 与 `product sidecar export` 输出内的 `sidecar_export.source_provenance`。该 surface 只包含 body-free refs：

- `source_provenance_ref`：`docs/source/README.md`
- `historical_fixture_ref`：`examples/nsfc_workspace_p2c_critique.json`
- `explicit_archive_import_ref`：`workspace-initialize-intake` command ref
- `parity_oracle_ref`：`program:mag_declared_grant_pack_source_refs`

这些 refs 只服务 OPL locator/index/projection。MAG 继续持有 grant source truth、workspace truth、fundability / quality / export verdict 和 receipt authority；通用 workspace/source intake shell、runtime、workbench、ledger 与 scheduler 仍归 OPL Framework / shared family layer。
