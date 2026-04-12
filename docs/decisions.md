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

## 2026-04-11：`Hermes-Agent` 只指上游外部 runtime substrate

- 后续凡是提到 `Hermes-Agent`，只能指上游外部 runtime 项目 / 服务本体。
- 仓内 `hermes_runtime.py` 只代表 repo-local migration scaffold，不得写成“已接入 Hermes-Agent”。

## 2026-04-12：runtime substrate 与 grant executor 明确分层

- 决策：既然上游 `Hermes-Agent` 已承担 runtime substrate owner，后续不把这件事偷换成“grant authoring 的每个单步都必须立刻迁成 Hermes-native executor”。
- 理由：当前已经跑通的是长期在线 runtime substrate，不是 authoring semantics 的完全替换。若把二者混在一起，只会让已验证的 grant critique / revision / packaging 主线失去稳定边界。
- 影响：repo-side domain logic、artifact assembly、identity guard 与 executor routing 继续保留为 domain owner；未来若要替换单步执行器，必须以新的 route truth 单独推进。

## 2026-04-11：当前主线回到“本地 runtime 诚实 + 上游 Hermes-Agent 目标”

- 当前可执行 runtime owner 仍是 repo-local code。
- 旧 `CLI-first + host-agent runtime` 线只保留为 compatibility bridge / regression oracle。
- 当前 `hermes_runtime.py` 路径只保留为本地迁移 scaffold。
- `CLI / MCP / controller / upstream Hermes-Agent target / MedAutoGrant domain logic` 的边界必须显式保留，不得偷换 formal entry 或 authoring semantics。

## 2026-04-11：旧 Hermes 命名材料降级为历史本地迁移工件

- `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report / run-local / resume-local` 当前仍运行在 repo-local runtime path 上。
- 旧的 Hermes 命名 program/spec 文档继续保留为历史迁移材料，但不再作为“上游 Hermes-Agent 已落地”的 current truth。

## 2026-04-11：final package / hosted contract 继续保持本地 owner，等待真实上游集成

- `execute-revision-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle` 当前仍由 repo-local helper 持有输入加载、identity guard 与输出 handoff。
- `revision_executor.py`、`artifact_bundle.py`、`final_package.py` 继续保留 domain document assembly 责任，不被误写成上游 substrate 已接管。
- 如果未来这些责任要迁到上游 `Hermes-Agent`，必须以新的 repo-tracked truth 重新冻结。
