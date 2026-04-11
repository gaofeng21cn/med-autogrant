# 决策记录

## 2026-04-11：统一文档骨架

- 采用核心五件套：`project/architecture/invariants/decisions/status`。
- `docs/README*` 以核心骨架为首读入口，其次是 `specs/`、`plans/`、`history/`。

## 2026-04-11：AGENTS 仅保留工作方式

- `AGENTS.md` 不再承载项目事实与阶段判断，统一回收至核心骨架与 specs。

## 2026-04-11：OMX 仅保留历史入口

- OMX 相关内容只作为历史入口保留在 `docs/history/omx/**`，不再作为活跃执行入口。

## 2026-04-11：移除 OMX-era 外部验证入口

- `omx-project-installer` 相关的外部 verifier 不再出现在 repo-tracked current truth 的验证表述中。
- 如需追溯历史来源，仅在历史说明或本文件记录，不再作为当前验证或 hard gate 入口。

## 2026-04-11：统一最小验证入口

- `scripts/verify.sh` 作为默认最小验证入口，保持分层 lane 与 `Makefile` 一致。

## 2026-04-11：冻结 post-R5A 本地 runtime 上限与 honest stop

- 在当前 repo-tracked truth 下，`R1 -> R5.A` 本地 runtime ladder 与 post-`R5.A` fail-closed hardening 已达到当前可验证上限。
- 当前 owner line 固定为 `post-R5A local runtime closeout / honest stop`，closeout verdict 固定为 `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`。
- 继续推进时必须先新增并冻结 tranche truth；不得把未冻结的 hosted/runtime/submission-grade reality 写成当前已有主线。

## 2026-04-11：目标 substrate 优先于旧本地 runtime 延长线

- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态，而不是继续把旧本地 runtime 深磨成长期产品终态。
- 当前本地 runtime 保留为迁移桥、兼容层与回归 oracle；任何新 tranche 都必须显式说明是在延续旧基线，还是在服务新的目标形态。

## 2026-04-11：切换到 Hermes-backed runtime substrate 主线

- 新的产品 runtime owner 固定为 `Hermes-backed runtime substrate`。
- 旧 `CLI-first + host-agent runtime` 线只保留为 compatibility bridge / regression oracle。
- `CLI / MCP / controller / Hermes substrate / MedAutoGrant domain logic` 的边界必须显式保留，不得偷换 formal entry 或 authoring semantics。

## 2026-04-11：冻结 Hermes capability migration map

- `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report / run-local / resume-local` 的产品主线改为 Hermes-owned runtime path。
- revision / final package / hosted contract bundle 继续挂在 Hermes runtime 上运行，但对象边界、checkpoint truth 与 fail-closed contract 保持在 MedAutoGrant domain logic 中。
