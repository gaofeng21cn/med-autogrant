# Med Auto Grant 仓库协作规范

这个根目录 `AGENTS.md` 是仓库默认入口规范。直接从仓库根进入的 Codex 会话，应先遵循这里；更深层 `AGENTS.md` 只补充更细分目录的规则。

## 适用范围

适用于仓库根目录及其子目录；如果更深层目录存在 `AGENTS.md`，则以更近者为准。

## 项目定位

- `Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 方向/系统。
- 它不是成熟 autopilot，不是 reviewer-owned surface，也不是 `Research Ops` 论文写作分支。
- 当前默认本地执行形态是 `Codex-default host-agent runtime`；当前 repo-tracked 产品主线按 `Auto-only` 理解。
- 当前 formal-entry matrix 固定为：`CLI` 为默认正式入口，`MCP` 为 future protocol layer，`controller` 为内部控制面。

## 开发优先级

- 优先做成熟的本地 `CLI-first + host-agent` runtime，再做 hostedization prep。
- 代码优先负责 contract、validation、audit、persistence、gate 和 host bridge，不要重新抢回高层 grant authoring 主导权。
- workspace、stage route、critique / revision artifact 等核心对象必须走显式结构契约，不能依赖隐式 prompt 漂移。
- `.runtime-program/` 属于开发控制面与 report-routing 面，不是产品 runtime 本体。

## 关键边界

- `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 不能互相替代。
- 当前 repo-verified durable report / audit surface 继续以 `summarize-workspace`、`critique-summary`、`stage-route-report` 为准。
- `stage-route-report` 必须继续输出 `verification_checkpoint`，把 validation、route recommendation、reviewed revision evidence、forced rollback 与 presubmission gate 聚合到同一个 machine-readable checkpoint surface。
- 未来迁移到 managed web runtime 时，只能迁移宿主形态，不能改写 domain contract 与 substrate 约束。

## 工作树纪律

- Heavy 长链路工作必须在基于当前 `main` 创建的独立 worktree 中完成。
- 共享根 checkout 保持在 `main`，只用于轻量读取、评审、吸收到 `main`、push 和清理，不要把它变成长时间 owner checkout。
- 如果需要多条长链路主线，就创建多个 worktree，不要依赖 session 级隔离硬撑。
- 新 lane 开始前，确认 owner worktree 干净，且没有陈旧 `.runtime-program/state/sessions/*`、残留 tmux session 和 stale `skill-active` 状态。
- lane 结束后，要么吸收已验证提交回 `main`，要么明确放弃，并清理 worktree、分支和相关本地状态。

## 测试面治理

- `make test-fast` 是默认开发测试面，并继续排除 `meta`。
- `make test-meta` 保留给 repo-tracked program-control 与 repository-hygiene 检查，不要让这些检查漂回普通 smoke。
- `make test-cli-smoke` 是 CLI / local-runtime 的专用 smoke lane，`make test-full` 继续作为 clean-clone 基线。
- 任何 repo-tracked 文件一旦改测试命令，要同步更新 `Makefile`、`pyproject.toml`、`README*`、runtime prompt docs 与 command-surface tests。

## 文档与附录

- 根文档负责默认协作规则；`contracts/project-truth/AGENTS.md` 是更细的项目边界附录，不再是默认必读前置。
- `docs/domain-harness-os-positioning.md` 是项目定位补充文档，`docs/specs/**` 是阶段冻结和边界规划记录。
- 对外公开、给人看的文档保持中英双语；内部开发、计划、实现细节默认中文。
- `.runtime-program/context/**`、`.runtime-program/plans/**`、`.runtime-program/reports/**` 是当前 active program 的 durable 控制面，不是一次性聊天记录。

## 通用协作约束

- 保持 diff 小、可审查、可回退。
- 能删就别加；能复用现有模式就别新起抽象。
- 没有明确理由不要新增依赖。
- 完成前必须运行与改动相匹配的测试、类型检查和验证命令。
- 最终说明需要交代改了什么，以及仍存在哪些风险或缺口。

## 本地状态

- `.runtime-program/` 与 `.codex/` 是本地工具状态，必须保持未跟踪。
- `.runtime-program/local/AGENTS.local.md` 预留给机器私有 overlay，不进入 repo-tracked 主线。
