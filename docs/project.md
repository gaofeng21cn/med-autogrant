# 项目概览

## 项目定位

`Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 方向。
当前仓库主线按 `Auto-only` 理解，已经有一条可运行的本地 `CLI` runtime 基线；旧 `CLI-first + host-agent` 线只保留为历史迁移基线，而当前 `hermes_runtime.py` 路径仍是 repo-local migration scaffold。

## 项目目标

- 明确 `CLI / MCP / controller` 的 formal-entry matrix。
- 稳定 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 与相关 artifact/export surface。
- 在 `R1 -> R5.A` 已 absorbed 的前提下，把当前 post-`R5.A` honest stop 作为迁移基线保留，并把 runtime substrate 责任迁到真实的上游 `Hermes-Agent`。

## 范围与非目标

- 不把 `MCP` 或 `controller` 解释为已公开支持的 runtime formal entry。
- 不把仓库误写成成熟 autopilot 或 reviewer-owned runtime。
- 不把用户级 runtime-state 或其他 machine-local control-plane 写成 repo-tracked 产品本体。
- 不把 `P5.*` hosted/federation 扩展写成当前已开工的范围。

## 当前形态

- Current phase：`Truth Reset / Upstream Hermes-Agent Pilot Prep`
- Active tranche：`Local Runtime Honesty + Upstream Substrate Migration`
- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Current owner line：`repo-local runtime baseline with upstream Hermes-Agent pending`
- Historical owner line：`post-R5A local runtime closeout / honest stop`
- Previous truthful closeout baseline：`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
- 默认入口：CLI（validator、summarize、next-step、critique、route + repo-local runtime dispatch）
