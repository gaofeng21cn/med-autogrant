# Med Auto Grant Repository Agent Contract

## Scope

Apply this file to the repository root and all descendants unless a deeper `AGENTS.md` overrides it.

## Project Truth

- `Med Auto Grant` 是 `Grant Foundry` 在医学场景下的首个实现 scaffold。
- 当前仓库是文档先行、契约先行的 repo scaffold，不应被描述成已经完成的成熟 runtime。
- 目标方向是未来的 `Grant Ops` 医学 domain gateway 与 harness，但在 `OPL` 语义里仍属于 future domain surface。
- 第一阶段 MVP 聚焦医学场景下的 `NSFC` 通用申请骨架。

## Architecture Priorities

- 默认采用 `Agent-first`，而不是 `fixed-code-first`。
- `Auto` 与 `Human-in-the-loop` 是共享同一基座的两种执行模式，不是两套系统。
- `Grant Ops` 保持 author-side、proposal-facing 边界，不折叠进 `Research Ops`，也不伪装成 reviewer-owned surface。

## Documentation Rules

- 对外公开、给人看的文档保持中英双语。
- 内部开发、计划、备忘、实现细节默认只保留中文。
- 不要无边界扩大双语范围。

## Working Agreements

- 保持 diff 小、可审阅、可回退。
- 避免兜底方案、临时补丁、启发式后处理。
- 不要无理由新增依赖。
- 修改公开文档时，同时维护对应镜像语言版本。
- 在声称完成前，运行与当前改动相关的最小验证。

