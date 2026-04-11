# 项目概览

## 使命

`Med Auto Grant` 是面向医学 `Grant Ops` 的 `Domain Harness OS`，目标是在 CLI-first 的本地 runtime 上形成可验证、可审计、可复用的提案生产与修订能力。

## 范围与非目标

- 仅冻结 CLI-first 的本地运行时与其验证/审计面。
- 不把 `MCP` 或 `controller` 解释为已经公开支持的 runtime formal entry。
- 不把 `.runtime-program/**` 当作产品 runtime 或 repo-tracked truth。
- 不把 `P5.*` hosted/federation 扩展写成当前已开工的范围。

## 当前形态

- 当前活跃主线：`Runtime Productization Program`。
- 最新 absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`。
- 当前 owner line：`post-R5A local runtime hardening`。
- 默认入口：CLI（validator、summarize、next-step、critique、route + local runtime）。

## 文档骨架

本仓库的核心骨架由以下文件组成：

- `docs/project.md`：项目定位与边界。
- `docs/architecture.md`：系统结构与核心数据流。
- `docs/invariants.md`：必须长期保持的约束与不变量。
- `docs/decisions.md`：关键决策记录与变更原因。
- `docs/status.md`：当前阶段、活跃 tranche 与近期进度。
