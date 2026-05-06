# Specs 索引

本目录保留 `Med Auto Grant` 的当前技术记录层。

当前优先级最高、仍由 docs guide 或 status 直接引用的 active current-truth specs 是：

- [AI-first 质量边界 current truth](./2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./2026-04-22-quality-autonomy-family-grammar-current-truth.md)

`contracts/runtime-program/current-program.json` 仍是完整 repo-tracked truth-surface 清单的 canonical pointer。部分 route、hosted-caller、product-entry 与 Hermes reset specs 仍留在本目录，是因为 current-program 或历史审计路径仍直接引用这些原路径。

更早的 dated `P*`、`R*`、`post-R5A`、activation-package、migration-board 与已被 supersede 的 tranche current-truth 文件属于历史技术记录。它们继续留在本目录作为 repo-tracked provenance，避免大范围重写旧审计路径；统一阅读入口改为：

- [历史 specs 索引](../history/specs/README.zh-CN.md)

当前产品真相不能只按文件名日期取最新 spec。请先读核心五件套和 `current-program.json`，再按需要读取 active specs 所冻结的具体边界。历史文件可以保留旧任务 wording、旧路径和已被 supersede 的 tranche label。
