# Med Auto Grant 仓库协作规范

## 适用范围

本文件适用于仓库根目录及其所有子目录；若更深层目录存在 `AGENTS.md`，以更近者为准。

## 定位

- `AGENTS.md` 只约束工作方式，不承载项目知识细节。
- 项目知识默认从 `README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md` 读取。
- `Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 方向。

## 开发原则

- 第一优先级：继续打磨本地 `CLI-first + host-agent` runtime，收紧 contract、validation、audit、persistence 与 gate。
- 第二优先级：把 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 的边界写清楚并守住。
- 第三优先级：只推进诚实的后续 hardening，不虚构主线，也不把历史 OMX 交接模型写回当前入口。
- 不做降级处理、兜底补丁、启发式修补或“先糊住再说”式实现。

## 文档体系

- `README*` 与 `docs/README*` 是默认公开入口。
- `docs/project.md`：项目概览与当前产品角色。
- `docs/architecture.md`：主链路、control-plane、runtime 与 artifact/export surface 的结构边界。
- `docs/invariants.md`：硬约束与不能破坏的边界。
- `docs/decisions.md`：仍有效的关键决策与取舍。
- `docs/status.md`：当前状态、活跃主线、下一步和验证口径。
- `docs/specs/`：repo-tracked current truth、activation package 与技术规格。
- `docs/plans/`：历史计划与规划记录。
- `docs/history/omx/`：OMX 历史资料入口，不再承担活跃 workflow。
- `.runtime-program/context/**`、`.runtime-program/plans/**`、`.runtime-program/reports/**` 是本地 operator control-plane，不是 repo-tracked 产品真相。

## 文档规则

- 公开文档保持中英双语；内部技术、规划、实现和历史记录默认中文。
- 新文档先判断角色，再决定落点；不要把核心知识、current truth、历史计划和历史归档混在同一层。
- 如果某条规则需要长期冻结，应写入 `docs/invariants.md`、相关 `docs/specs/*` 或测试，不要继续堆在 `AGENTS.md`。

## 变更与验证

- 保持 diff 小、可审查、可回退。
- 能删就别加；能复用现有模式就别新起抽象。
- 没有明确必要不要新增依赖。
- 修改 formal-entry、验证命令、runtime handle、artifact/export surface、docs 骨架或 control-plane 语义时，必须同步改 README、docs、测试和相关实现。
- 默认最小验证入口是 `scripts/verify.sh`。
- 默认 smoke 是 `make test-fast`。
- `make test-meta` 与 `make test-cli-smoke` 是显式 lane。
- `make test-full` 是 clean-clone 基线。
- 上述验证入口必须与 `Makefile`、`pyproject.toml`、`README*` 与命令面测试保持一致。

## 并行开发与工作树

- 大改动、长链路工作、并行多 AI 开发，默认先从最新 `main` 开独立 worktree，再在 worktree 内实现和验证。
- 共享根 checkout 只用于轻量阅读、评审、吸收验证后提交、push 和清理，不应长期承担重型实现。
- 新 lane 开始前先确认 owner worktree 干净，并清理陈旧 `.runtime-program/state/sessions/*`、tmux session 与 stale `skill-active` 状态。

## 本地状态

- `.runtime-program/` 与 `.codex/` 都是本地工具状态，必须保持未跟踪。
- `.runtime-program/local/AGENTS.local.md` 只允许作为机器私有 overlay 存在，不进入 repo-tracked 主线。
