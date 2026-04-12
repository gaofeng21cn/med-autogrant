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

## 2026-04-12：冻结 author-side executor routing contract

- 决策：`stage_action_envelope` 与 `build-product-entry` 必须共享同一份 `executor_routing_contract`，明确当前 stage、下一步 executor route，以及已 landed 的 author-side route catalog。
- 理由：如果只写“substrate 已统一”，却不把 critique / revision / export 的 route status 显式冻结下来，后续最容易把 `pending` route 误写成“已 landed executor”。
- 影响：当前 `critique` route 固定为 `pending / handoff-required`；`revision / artifact_bundle / final_package / hosted_contract_bundle` 固定为当前 landed service-safe domain command surface；未来继续替换任何 route，都必须先改这份 contract truth。

## 2026-04-12：为 critique pending route 冻结直接协作 handoff contract

- 决策：在保持 `critique` 继续为 `pending / handoff-required` 的前提下，为它补一份 machine-readable `handoff_requirements`，明确 future Hermes-side collaborator 必须先读取哪些 domain surfaces。
- 理由：如果 pending route 只有一个状态字段，future host 很容易绕开 grant domain truth，或者误以为需要仓内新增本地 critique helper。把 handoff 要求显式冻结出来，能让“直接协作”与“新 executor 已 landed”保持清楚分层。
- 影响：当前 `critique` route 至少要求读取 `summarize-workspace / stage-route-report`，并且只有 source workspace 已进入 `critique / revision / frozen` review context 时才额外要求 `critique-summary`；这仍不是 `execute-critique-pass`。

## 2026-04-12：冻结全 pending authoring route handoff matrix

- 决策：不再只为 `critique` 单独定义 pending handoff，而是把 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / frozen` 全部冻结成 route-specific `handoff_requirements`。
- 理由：最终目标是让 `Hermes` 负责 substrate、让 `OPL` / domain 通过统一 envelope 直接协作，而不是继续脑补新的 repo-local executor。没有完整 matrix，future caller 仍会在其他未 landed route 上重新发明 handoff semantics。
- 影响：`author_side_route_catalog` 现在会列出完整 pending + landed route matrix；每条 pending route 都会显式导出 `required_domain_surfaces / required_identity_fields / required_summary_fields / required_gate_fields`，并且只允许引用 repo 已有 surface。

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
