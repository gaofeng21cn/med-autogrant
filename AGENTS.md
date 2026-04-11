# AGENTS 工作方式规则

## 适用范围

本文件适用于仓库根目录及其所有子目录；若更深层目录存在 `AGENTS.md`，以更近者为准。

## 定位

- AGENTS 只管工作方式，不承载项目真相、规格或阶段判断。
- 项目骨架与现状以 `docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md` 与 `README*` 为准。

## 核心文档骨架

- `docs/project.md`：项目定位与边界。
- `docs/architecture.md`：系统结构与核心数据流。
- `docs/invariants.md`：必须长期保持的约束与不变量。
- `docs/decisions.md`：关键决策记录与变更原因。
- `docs/status.md`：当前阶段、活跃 tranche 与近期进度。

## 文档分类

- `README*` 与 `docs/README*`：默认公开入口与索引。
- `docs/*.(project|architecture|invariants|decisions|status).md`：核心骨架，不与 activation package / current truth 混写。
- `docs/specs/**`：repo-tracked current truth、activation package、设计冻结文档与硬门槛描述。
- `docs/plans/**`：历史规划工件，仅用于追溯。
- `docs/history/**`：历史归档入口（含 OMX）。

## Worktree 规则

- 牵涉多文件或多步骤变更，默认从 `main` 新建独立 worktree 再实现。
- 共享根 checkout 只用于审阅、吸收、提交、push 与清理，不承担重型实现。

## 验证规则

- `scripts/verify.sh` 默认执行 `make test-fast`；`scripts/verify.sh full` 执行 `make test-full`。
- `make test-fast` 是默认开发验证，并默认排除 `meta` 套件。
- `make test-meta` 仅用于 repo-tracked program control 与 repo hygiene 检查。
- `make test-cli-smoke` 是 CLI/local-runtime smoke lane，`make test-full` 是 clean-clone baseline。
- 更新验证命令、控制面或测试入口时，必须同步更新 `Makefile`、`pyproject.toml`、`README*`、`docs/README*`、`scripts/verify.sh` 与相关 tests。

## 变更同步

- 涉及 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 的语义或表述变更，必须同步更新核心骨架、current truth 与相关 tests。

## 本地控制面（.runtime-program）

- `.runtime-program/**` 与 `.codex/**` 为本地工具/控制面状态，必须保持未跟踪。
- `.runtime-program/` 是本地控制面，不是产品 runtime，也不是 repo-tracked current truth。
- `.runtime-program/local/AGENTS.local.md` 仅允许本机 overlay，不进入 repo-tracked 主线。
