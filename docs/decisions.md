# 决策记录

## 2026-04-13：critique route 升级为 Codex CLI autonomous landed route

- 决策：把 `critique` route 从历史上的 `pending / handoff-required` 正式提升为已 landed 的 `execute-critique-pass` route。
- 理由：实现层 (`hermes_runtime.py` / `critique_executor.py` / `codex_cli.py`) 与现有 route tests 已经稳定落在 landed 口径；继续把它写成 pending 会制造第二真相。
- 影响：`current-program`、status/architecture/current-truth specs、hosted bundle route catalog 与 meta tests 全部改写为 `critique = landed`；当前 landed author-side route 变成 `critique / revision / artifact_bundle / final_package / hosted_contract_bundle`。

## 2026-04-13：critique 的默认 concrete executor 继承本机 Codex 默认

- 决策：`execute-critique-pass` 的默认模型与默认 reasoning effort 统一收口到 `inherit_local_codex_default`，不在 repo 内固定 `gpt-5.4 / xhigh`。
- 理由：当前真实入口是 `read_codex_cli_contract()` + `run_codex_exec(...)`；未显式配置环境变量覆盖时，本就应该跟随本机 Codex 默认配置，避免四仓未来一起追着改 model pin。
- 影响：文档、current-program 与 current-truth 必须显式写出 `default_model / default_reasoning_effort = inherit_local_codex_default`；只有设置 `MED_AUTOGRANT_CODEX_MODEL` / `MED_AUTOGRANT_CODEX_REASONING_EFFORT` 时才会覆盖。

## 2026-04-13：Hermes-native 只指完整 agent loop

- 决策：文档层统一声明，只有带 session substrate、route orchestration、domain mutation 与 durable state transition 的 full agent loop 才算 `Hermes-native`。
- 理由：如果把 chat relay / 单次 chat completion 也写成 `Hermes-native`，就会把 substrate owner 与单步 executor 混写，误导后续跨仓收敛。
- 影响：当前 `critique` landed 只能写成 `Codex CLI autonomous executor landed`，不能写成 `Hermes-native landed`；后续若切到 Hermes executor，必须额外拿 full-loop truth 与 proof。

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
- 影响：这条 contract 仍是 route truth 的锚点；但其中关于 `critique = pending / handoff-required` 的历史表述，已被 `2026-04-13` 的 critique landed 决策 supersede。未来继续替换任何 route，都必须先改这份 contract truth。

## 2026-04-12：为 critique pending route 冻结直接协作 handoff contract

- 决策：在保持 `critique` 继续为 `pending / handoff-required` 的前提下，为它补一份 machine-readable `handoff_requirements`，明确 future Hermes-side collaborator 必须先读取哪些 domain surfaces。
- 理由：如果 pending route 只有一个状态字段，future host 很容易绕开 grant domain truth，或者误以为需要仓内新增本地 critique helper。把 handoff 要求显式冻结出来，能让“直接协作”与“新 executor 已 landed”保持清楚分层。
- 影响：这份 pending handoff contract 现已退为历史 superseded note；`2026-04-13` 之后的 current truth 已改成 `critique -> execute-critique-pass` landed。旧 contract 只保留作历史迁移说明。

## 2026-04-12：冻结全 pending authoring route handoff matrix

- 决策：不再只为 `critique` 单独定义 pending handoff，而是把 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / frozen` 全部冻结成 route-specific `handoff_requirements`。
- 理由：最终目标是让 `Hermes` 负责 substrate、让 `OPL` / domain 通过统一 envelope 直接协作，而不是继续脑补新的 repo-local executor。没有完整 matrix，future caller 仍会在其他未 landed route 上重新发明 handoff semantics。
- 影响：`author_side_route_catalog` 继续保留完整 pending + landed route matrix；但 `critique` 已在 `2026-04-13` 被提升出 pending matrix，当前仍属 pending 的是 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / frozen`。

## 2026-04-12：冻结 schema-backed product entry / routing contract

- 决策：把已 landed 的 `service-safe domain surface`、`pending_handoff_requirements`、`executor_routing_contract` 与 `product_entry` 从“文档冻结 + 运行时 dict”进一步收口成 schema-backed contract，并在 `run-local` / `build-product-entry` 生成时 fail-closed。
- 理由：`OPL Gateway` 与 future domain caller 最终消费的是 machine-readable contract，而不是 repo 内部约定。如果这些 surface 只有 current truth 没有 schema，后续最容易在 pending route、route catalog、draft-bearing/nullability 边界上悄悄漂移。
- 影响：`schemas/v1/schema-index.json` 现在会显式索引这四份 schema；`product_entry` 与 `stage_action_envelope.executor_routing_contract` 必须同时满足 schema 校验和冻结 truth 比对；后续任何 contract 变更都必须同步更新 schema、tests、docs 与 current-program pointer。

## 2026-04-12：冻结 hosted contract bundle entry and route catalog

- 决策：`build-hosted-contract-bundle` 不再只导出 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract`，还要显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并受 `hosted-contract-bundle.schema.json` 的 fail-closed 约束。
- 理由：future hosted caller / `OPL` caller 真正要消费的不只是 runtime/state/operator pointer，还需要稳定的 service-safe entry、schema registry 与 author-side route catalog；如果这些合同不随 bundle 一起冻结，后续就会在 bundle 外重新发明 handoff semantics。
- 影响：hosted bundle 现在只打包已经冻结好的 domain entry / schema / route truth，不新增 repo-local executor，也不把 hosted runtime、`OPL Gateway` 或 pending route 写成已落地。

## 2026-04-12：冻结 OPL 对齐的理想目标与阶段图

- 决策：把 `Med Auto Grant` 的长线理想目标固定为 `OPL` 顶层入口、`Hermes-Agent` substrate owner、`Med Auto Grant` domain truth owner 的分层结构，并把主线阶段固定成 `P1 completed / P2 completed / P3 completed / P4 next`。
- 理由：如果不把 “理想目标” 和 “当前完成态” 分开冻结，后续最容易一边拿 `OPL` 理想型讲话，一边把未完成的 hosted caller / direct product entry 写成 landed。
- 影响：`current-program` 现在额外携带 `ideal_target` 与 `phase_map`；当前 `P3 hosted caller / OPL consumption proof` 已通过冻结合同与 proof test 落地，后续推进默认转向 `P4 mature direct grant product entry`，而不是回头重写 repo-local helper 或跳到 product overclaim。

## 2026-04-12：冻结 hosted caller contract consumption proof

- 决策：external caller / future `OPL` caller 必须直接消费仓库已经冻结好的 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并且只通过 `supported_commands` 与 `command_contracts` 构造 request；不新增 repo-local hosted helper。
- 理由：如果 external caller 还要回头读仓内 helper 或手写参数拼装逻辑，那么 `P3` 其实并没有完成，合同也还不算真正 machine-readable。
- 影响：`product_entry.return_surface_contract.domain_entry_contract` 与 hosted bundle 的 `domain_entry_contract` 现在共享同一份 command catalog；`P3` 可以诚实标成 completed，而 `P4` 成为下一个 honest phase。

## 2026-04-12：`P4.A` 只落 controller-owned / read-only direct product projection

- 决策：`grant-progress` 与 `grant-cockpit` 当前只作为 controller-owned、read-only 的 direct grant product projection 落地，不进入 `domain_entry_contract.supported_commands`，也不被写成新的 service-safe executor surface。
- 理由：`P4` 的第一棒需要先给 direct user / operator / future caller 一个稳定的人话 projection，但如果把这两条 surface 混进 domain entry command catalog，就会再次把 product projection、domain execution 与 hosted caller contract 语义搅在一起。
- 影响：当前 direct-product projection 只允许读取 `summarize-workspace`、`stage-route-report`、`critique-summary` 与 `build-product-entry` 的既有合同信息；它们不改写 route owner，不新增 repo-local hosted helper，也不等于成熟前台 / hosted runtime。

## 2026-04-12：冻结 `P4.A` direct product projection contract

- 决策：`grant-progress` 与 `grant-cockpit` 不只停留在 CLI projection，而是进一步通过 `grant-progress.schema.json` 与 `grant-cockpit.schema.json` 冻结成 schema-backed、generation-time fail-closed 的 projection contract。
- 理由：如果 `P4.A` 只有命令和 current truth，没有独立 schema，那么 direct product projection 的 shape、blocker 语义、command catalog 展示面和 nullability 边界都可能悄悄漂移；而这两条 surface 又必须和 service-safe domain command catalog 保持严格分层。
- 影响：`read_grant_progress(...)` 与 `read_grant_cockpit(...)` 现在都会在返回前执行 schema 校验；这两条 projection 继续不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-12：冻结 `P4.B` direct entry composition contract

- 决策：在 `P4.A` 的基础上新增 `grant-direct-entry`，把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 组合成一份 schema-backed、generation-time fail-closed 的 direct-entry contract。
- 理由：理想形态中的 `Med Auto Grant Product Entry` 不能永远停在“只读投影 + 单独 build shell”两个分散 surface 上；但当前又不能发明新的 executor 或 handoff semantics。最诚实的推进方式，就是把已冻结 surface 组合成一份 direct-entry contract。
- 影响：`grant-direct-entry` 继续只复用既有 route truth、grant truth 与 `product_entry` envelope，不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-12：冻结 `P4.C` mainline status 与 grant user loop

- 决策：在 `P4.B` 的基础上新增 `mainline-status`、`mainline-phase` 与 `grant-user-loop`，把 repo 主线快照、当前 `grant-direct-entry` 组合面，以及 route-derived next action 收成当前 controller-owned 的 user loop。
- 理由：如果用户仍要自己翻 `current-program`、phase-map docs 和 route contract 才知道“现在在哪个阶段、下一步该执行什么”，那么 `P4` 仍停留在分散 surface；但当前又不能越界把它写成成熟 Web UI、hosted runtime 或新的 executor。
- 影响：`grant-user-loop` 现在通过 `grant-user-loop.schema.json` 受 generation-time fail-closed 校验；`mainline-status / mainline-phase / grant-user-loop` 继续只投影已冻结 truth，不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

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
