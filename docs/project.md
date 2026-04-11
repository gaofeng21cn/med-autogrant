# 项目概览

## 项目定位

`Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 方向。
当前仓库主线按 `Auto-only` 理解，本地默认执行口径是 `CLI-first + host-agent` runtime。

## 项目目标

- 明确 `CLI / MCP / controller` 的 formal-entry matrix。
- 稳定 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 与相关 artifact/export surface。
- 在 `R1 -> R5.A` 已 absorbed 的前提下，继续推进诚实的后续 hardening。

## 范围与非目标

- 不把 `MCP` 或 `controller` 解释为已公开支持的 runtime formal entry。
- 不把仓库误写成成熟 autopilot 或 reviewer-owned runtime。
- 不把 `.runtime-program/**` 本地 control-plane 写成 repo-tracked 产品本体。
- 不把 `P5.*` hosted/federation 扩展写成当前已开工的范围。

## 当前形态

- Current phase：`Runtime Productization Program`
- Active tranche：`R5 / Hostedization Prep`
- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Current owner line：`post-R5A local runtime hardening`
- 默认入口：CLI（validator、summarize、next-step、critique、route + local runtime）
