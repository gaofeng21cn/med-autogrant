# Med Auto Grant 仓库协作规范

## 适用范围

本文件适用于仓库根目录及其所有子目录；若更深层目录存在 `AGENTS.md`，以更近者为准。

## 项目定位

- `Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 方向/系统。
- 当前默认本地执行形态是 `Codex-default host-agent runtime`；当前 repo-tracked 主线按 `Auto-only` 理解。
- 当前 formal-entry matrix 固定为：默认正式入口 `CLI`、支持协议层 `MCP`（future layer）、内部控制面 `controller`。

## 非目标

- 不把仓库误写成成熟 autopilot、reviewer-owned surface 或 `Research Ops` 论文写作分支。
- 不把 `.runtime-program/` 这样的本地 control-plane 当成产品 runtime 本体。
- 不把历史 OMX 交接模型继续写成当前活跃开发入口。

## 开发优先级

- 第一优先级：继续打磨本地 `CLI-first + host-agent` runtime，收紧 contract、validation、audit、persistence 与 gate。
- 第二优先级：把 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 的边界写清楚并守住。
- 第三优先级：在当前 `R1 -> R5` 基线已吸收到 `R5.A` 的前提下，只推进诚实的后续 hardening，不虚构主线。

## 主要入口与真相面

- 默认人类/AI 入口：`README.md`、`README.zh-CN.md`、`docs/README.md`、`docs/README.zh-CN.md`
- 项目定位与当前边界：`docs/domain-harness-os-positioning.md`、`docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`、`docs/specs/2026-04-07-durability-model-clarification.md`
- 关键身份与 durable surface：`grant_run_id`、`workspace_id`、`draft_id`、`program_id`；`summarize-workspace`、`critique-summary`、`stage-route-report`
- `.runtime-program/context/**`、`.runtime-program/plans/**`、`.runtime-program/reports/**` 是本地 operator control-plane，不是 repo-tracked 产品真相。

## 文档规则

- `README*` 与 `docs/README*` 是默认公开入口。
- 公开文档保持中英双语；内部技术、规划、实现和历史记录默认中文。
- 历史 OMX 资料统一从 `docs/history/omx/README.md` 与 `docs/history/omx/README.zh-CN.md` 进入，不再直接作为活跃入口。
- narrative 规则放根 `AGENTS.md`、`docs/README*` 和项目定位/当前真相文档；不再保留 narrative 的 `contracts/project-truth/AGENTS.md` 层。

## 变更与验证

- 保持 diff 小、可审查、可回退。
- 能删就别加；能复用现有模式就别新起抽象。
- 没有明确必要不要新增依赖。
- 修改 formal-entry、验证命令、runtime handle、artifact/export surface 或 control-plane 语义时，必须同步改 README、docs、测试和相关实现。
- 默认测试入口：`make test-fast`；`make test-meta` 与 `make test-cli-smoke` 是显式 lane；`make test-full` 是 clean-clone 基线。

## 并行开发与工作树

- 大改动、长链路工作、并行多 AI 开发，默认先从当前 `main` 开独立 worktree，再在 worktree 内实现和验证。
- 共享根 checkout 只用于轻量阅读、评审、吸收验证后提交、push 和清理，不应长期承担重型实现。
- 新 lane 开始前先确认 owner worktree 干净，并清理陈旧 `.runtime-program/state/sessions/*`、tmux session 与 stale `skill-active` 状态。

## 本地状态

- `.runtime-program/` 与 `.codex/` 都是本地工具状态，必须保持未跟踪。
- `.runtime-program/local/AGENTS.local.md` 只允许作为机器私有 overlay 存在，不进入 repo-tracked 主线。
