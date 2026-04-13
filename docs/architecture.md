# 架构概览

## 主链路

当前主链路是 `CLI-first + real upstream Hermes-Agent runtime substrate`：

`operator / agent / direct product projection / future gateway caller -> CLI or MedAutoGrantDomainEntry -> upstream Hermes session substrate -> MedAutoGrant domain logic -> critique / export / stage surfaces -> durable artifacts`

formal-entry matrix 继续固定为：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。

## 入口 taxonomy 与 OPL handoff

当前需要明确区分三层入口：

- `operator entry`
  - 给人类操作同事使用的命令、workspace 准备、检查与显式 gate
- `agent entry`
  - 给 `Codex`、Claude Code、OpenClaw 等 host-agent 使用的 `CLI` / `MedAutoGrantDomainEntry`
- `product entry`
  - 给最终用户直接进入的产品入口

当前真实状态是：前两层已经存在，第三层的轻量结构化 shell 与第一棒 read-only product projection 也已经 landed，但成熟用户级前台仍未落地。

目标中的 domain 级链路应是：

`User -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> Hermes Kernel -> Med Auto Grant Domain Harness OS`

与 `OPL` 的家族级衔接应是：

`User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

`OPL -> Med Auto Grant` 的最小 handoff envelope 至少包括：

- `target_domain_id`
- `task_intent`
- `entry_mode`
- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`

在这层公共 envelope 之上，grant 域继续补充 `workspace_id`、`draft_id`、`funding_call` 等 domain payload。

按 `OPL` 对齐后的理想目标，这条链路的 owner 固定为：

- `OPL Gateway`：family-level route / gateway owner
- `Med Auto Grant Product Entry`：domain direct entry owner
- `Hermes-Agent`：runtime substrate owner
- `Med Auto Grant`：author-side grant truth / route / export owner

当前并不宣称 `OPL Gateway` 已在本仓落地；当前只是在为 future caller 冻结稳定 contract。

## OPL family orchestration contracts（adoption 方向）

`OPL` 顶层计划冻结 5 类 family contracts：

- family event envelope
- family checkpoint lineage
- family action graph
- family human gate
- family product-entry manifest v2

对 `Med Auto Grant` 来说，优先 adoption 的面是 `grant-progress / grant-cockpit / grant-direct-entry / grant-user-loop`，并与 family action graph / family human gate / family product-entry manifest v2 对齐；domain 侧继续保持 `workspace / draft / program` 的真相边界。

这轮对齐不引入 `CrewAI` 依赖，也不把 `OPL` 写成 runtime owner，更不宣称已完成跨仓 runtime core ingest。当前真实状态仍是上游 `Hermes-Agent` 作为 runtime substrate owner，MAG 聚焦 family-level contract-first 对齐与 domain-owned truth 维持。

## Hermes substrate 与 grant executor 的分工

在当前架构里，`Hermes-Agent` 已经承担：

- session substrate
- runtime state / attempt ledger durability
- gateway / interrupt / resume / scheduling 这类长期在线 runtime 能力

`Med Auto Grant` 自己继续承担：

- workspace / draft / critique / revision / export 的 domain truth
- author-side object model 与 identity guard
- stage routing、artifact assembly 与 hosted handoff contract

因此，这里真实成立的是：

- runtime substrate owner 已切到上游 `Hermes-Agent`
- repo-side `domain logic + executor adapter` 仍然负责 grant authoring 流程

这不等于“所有单步 authoring 都已经迁成 Hermes-native executor”。
如果未来某条 critique / revision / export route 要替换执行器，也必须按 route 单独冻结 truth 与 proof，而不是因为 substrate 已统一就自动把 authoring semantics 一起改掉。

## 入口与执行

- CLI 仍是唯一 formal entry：`validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report`、`mainline-status`、`mainline-phase`、`grant-progress`、`grant-cockpit`、`grant-direct-entry`、`grant-user-loop`，以及 `execute-direction-screening-pass`、`execute-question-refinement-pass`、`execute-argument-building-pass`、`execute-fit-alignment-pass`、`execute-outline-pass`、`execute-drafting-pass`、`execute-critique-pass`、`execute-revision-pass`、`execute-freeze-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle`、`build-submission-ready-package`。
- `src/med_autogrant/domain_entry.py` 现在提供结构化 `MedAutoGrantDomainEntry`，把 CLI 与 future gateway caller 收口到同一条 service-safe command contract。
- `src/med_autogrant/product_entry.py` 现在提供 `MedAutoGrantProductEntry`；`build-product-entry` 通过 `MedAutoGrantDomainEntry` 复用已 landed 的 route / summary / runtime contract，统一生成 `direct` 与 `opl-handoff` 共用的 shared envelope，并显式导出 `executor_routing_contract`。
- `MedAutoGrantProductEntry` 现在还提供 `grant-progress` 与 `grant-cockpit`：它们是 controller-owned、read-only 的 product projection，复用 `summarize-workspace`、`stage-route-report`、`critique-summary` 与 `build-product-entry` contract 信息，并分别受 `schemas/v1/grant-progress.schema.json` 与 `schemas/v1/grant-cockpit.schema.json` 约束、在生成时 fail-closed，但故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog。
- `MedAutoGrantProductEntry` 现在还提供 `grant-direct-entry`：它会把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 收成一份 controller-owned 的 direct-entry composition，并受 `schemas/v1/grant-direct-entry.schema.json` 约束、在生成时 fail-closed；它同样不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog。
- `mainline-status` / `mainline-phase` 现在把 `current-program` 里的理想目标、phase ladder、当前 tranche 与 remaining gaps 投影成 repo 级 controller surface；`grant-user-loop` 则把这份 mainline snapshot、`grant-direct-entry` 与 route-derived next action 收成当前 inbox-like user loop，并受 `schemas/v1/grant-user-loop.schema.json` 约束、在生成时 fail-closed；它同样不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog。
- `product-entry-manifest` 与 `product-frontdesk` 现在也由 `MedAutoGrantProductEntry` 直接输出为 controller-owned 的 frontdoor contract，并分别受 `schemas/v1/product-entry-manifest.schema.json` 与 `schemas/v1/product-frontdesk.schema.json` 约束、在生成时 fail-closed；其中 `family_orchestration` companion 的 route status 统一读取共享 author-side route truth。
- `build-product-entry.product_entry` 与 `run-local.stage_action_envelope.executor_routing_contract` 现在都已经收口成 schema-backed contract：前者对应 `schemas/v1/product-entry.schema.json`，后者对应 `schemas/v1/executor-routing-contract.schema.json`，并且两者都会在生成时 fail-closed。
- `build-product-entry.product_entry.return_surface_contract.domain_entry_contract` 现在会与 hosted bundle 共享同一份 command catalog，并显式固定 `supported_commands` 与每个 command 的 `command_contracts`。
- `src/med_autogrant/upstream_hermes.py` 负责真实 upstream 依赖探测、runtime root 决议与基于 `hermes_state.SessionDB` 的 attempt ledger。
- `run-local` 与 `resume-local` 继续以 journal 串联多次 pass，但 attempt index 现在来自真实上游 Hermes session substrate。
- 对 valid workspace，Hermes session handle 继续沿用 `grant_run_id`；对 `validation_failed` path，只允许使用 journal-scoped substrate session handle 持续 durability，不得伪造新的 domain `grant_run_id`。
- `src/med_autogrant/hermes_runtime.py` 现在应被理解为 repo-side domain adapter / orchestrator，而不是 runtime substrate owner。
- `src/med_autogrant/local_runtime.py` 只保留 compatibility bridge 责任。
- `execute-direction-screening-pass`、`execute-question-refinement-pass`、`execute-argument-building-pass`、`execute-fit-alignment-pass`、`execute-outline-pass`、`execute-drafting-pass`、`execute-critique-pass`、`execute-revision-pass`、`execute-freeze-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle`、`build-submission-ready-package` 继续由 repo-side domain logic 持有输入加载、identity guard 与输出 handoff。
- `execute-critique-pass` 当前默认走 `Codex CLI autonomous executor`：具体由 `critique_executor.py -> run_codex_exec(...)` 调起 `codex exec`，默认 `model / reasoning` 都继承本机 Codex 默认（`inherit_local_codex_default`），只有显式环境变量覆盖才会传 override。
- 同一条 `execute-critique-pass` 现在也支持显式 `executor_kind=hermes_native_proof`：这条 experimental lane 会通过 `hermes_native_executor.py -> read_hermes_agent_contract(...) -> run_agent.AIAgent.run_conversation(...)` 真实调用上游 Hermes full agent loop；它会显式读取本机 `~/.hermes/config.yaml` 的 model/provider/base_url/api_mode/reasoning_effort，并且只有在完成整轮 loop、拿到真实工具事件和合法 JSON 结果时才通过，否则 fail-closed。
- `build-hosted-contract-bundle` 继续把 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract` 一并导出，并额外显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，形成 future host / `OPL` caller 可直接消费的 hosted contract catalog。
- `build-submission-ready-package` 继续复用 `artifact_bundle -> final_package -> hosted_contract_bundle` 这条导出链，但会额外对 mandatory sections、evidence gaps、representative outputs、active projects 与 freeze gate 做 fail-closed 审核，只在全部满足时写出本地 `submission_ready_package`；它不替代外部官网提交。
- 当前 external caller 只需要读取 `domain_entry_contract.supported_commands` 与 `domain_entry_contract.command_contracts`，就能按统一 contract 构造 request，而不需要 repo-local helper。
- 当前 direct-product projection caller 则可以读取 `grant-progress / grant-cockpit` 的只读投影结果，先看当前 grant 主线、blocker 与 direct / `OPL` entry command catalog，再决定是否进入真正的 domain entry / product entry 调用。
- `build-hosted-contract-bundle.hosted_contract_bundle` 现在也受 `schemas/v1/hosted-contract-bundle.schema.json` 约束，并在写出前执行 schema + 冻结 truth 的 fail-closed 校验。
- 当前 author-side executor routing 继续按 route 单独冻结：`direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle` 现在都已经有 landed service-safe command surface，并共享同一份 route catalog truth。
- `pending-handoff-requirements.schema.json` 仍保留在 schema contract 中，但现在只承担历史兼容与旧真相追溯角色；当前主线 route output 已不再依赖它表达 authoring 主线推进。
- `critique-summary` 继续只在 source workspace 已经位于 `critique / revision / frozen` review context 时作为 review-context audit surface 有意义；当前 full landed authoring catalog 不再依赖 pending handoff contract 才能进入 `critique`。
- 这里的 `critique` landed 只表示当前默认 concrete executor 已统一到 `Codex CLI autonomous`；现在虽然已经有一条 `hermes_native_proof` 的 experimental critique lane，但只有带 session substrate、route orchestration、domain mutation 与 durable state transition 的 full agent loop 才算 `Hermes-native`，chat relay 不算。若本机 Hermes 当前仍走 `custom + chat_completions`，这条 lane 也只证明 full-loop 存在，不证明 provider 侧 reasoning 语义已经等价于 Codex CLI。
- 产物面：`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle`、`build-submission-ready-package`。

## 数据与对象模型

- `schemas/v1/nsfc-workspace.schema.json` 定义 workspace 结构与关键对象。
- `schemas/v1/service-safe-domain-surface.schema.json`、`schemas/v1/pending-handoff-requirements.schema.json`、`schemas/v1/executor-routing-contract.schema.json`、`schemas/v1/product-entry.schema.json`、`schemas/v1/product-entry-manifest.schema.json`、`schemas/v1/product-frontdesk.schema.json`、`schemas/v1/grant-progress.schema.json`、`schemas/v1/grant-cockpit.schema.json`、`schemas/v1/grant-direct-entry.schema.json`、`schemas/v1/grant-user-loop.schema.json`、`schemas/v1/hosted-contract-bundle.schema.json` 与 `schemas/v1/submission-ready-package.schema.json` 定义当前 product entry / frontdoor discovery / route handoff 历史兼容 / direct projection / direct-entry composition / direct user loop / hosted bundle / local submission-ready delivery / service-safe surface 的 schema-backed contract。
- `grant_run_id` 仅作为执行句柄；`workspace_id`、`draft_id`、`program_id` 保持边界分离。
- `workspace.py`、`stage_router.py`、`revision_executor.py`、`final_package.py` 等继续承载 MedAutoGrant 的 author-side domain logic；它们不应被未来的上游 substrate 目标或当前 repo-local helper 偷换成新的 authoring semantics。

## 控制面与报告

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer。
- 机器本地 runtime state 统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`，用于 session / log / report / prompt 等非仓库真相面状态。
- `grant-progress / grant-cockpit` 当前属于 controller-owned / read-only product projection；它们不替代 durable truth surface，也不构成新的 service-safe domain entry contract，并且不会被镜像进 hosted contract bundle 的 command catalog。
- `grant-direct-entry` 当前属于 controller-owned 的 direct-entry composition；它不会改写 route owner，也不会被镜像进 hosted contract bundle 的 command catalog。
- `grant-user-loop` 当前属于 controller-owned 的 user-loop composition；它不会改写 route owner，也不会被镜像进 hosted contract bundle 的 command catalog。
- `run-local / resume-local` 的默认 local run journal 落点固定为 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/<grant_run_id>.json`；显式 `--journal` 仍可覆盖该默认值。
- Hermes substrate state db 默认落在 `$CODEX_HOME/projects/med-autogrant/runtime-state/hermes/state.db`；如需显式隔离，可通过 `MED_AUTOGRANT_HERMES_HOME` 覆盖。
- 旧 local host-agent runtime 只保留为 compatibility bridge / regression oracle，不再作为长期产品 runtime owner。

## 文档层次

- Public surface：`README*`、`docs/README*`、`docs/domain-positioning*`、`docs/mvp-scope*`。
- 核心骨架：`docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md`。
- Repo-tracked current truth 与 activation package：`docs/specs/**`。
- 历史规划：`docs/plans/**`；历史归档：`docs/history/**`。

## 历史边界

- OMX 已退场，仅保留历史入口。
