# 当前状态

Date: `2026-04-13`

## 当前角色

- 仓库角色：医学 `Grant Ops` 的 author-side / proposal-facing `Domain Harness OS` 方向。
- 当前执行口径：`CLI-first + real upstream Hermes-Agent runtime substrate`。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。
- 当前入口真相：`operator entry` 与 `agent entry` 已存在；共享 envelope 的 lightweight `product entry` shell 已由 `build-product-entry` 落地；`product-entry-manifest` 现在会把当前 shell、shared handoff 模板、mainline snapshot、`product_entry_status` 状态摘要，以及显式的 `frontdesk_surface`、`operator_loop_surface`、`operator_loop_actions` 与 `recommended_shell / recommended_command` 冻结成 machine-readable discovery surface，并受 `schemas/v1/product-entry-manifest.schema.json` 约束、在生成时 fail-closed；当前 direct frontdesk 已明确收口为 controller-owned 的 `product-frontdesk`，而真实 operator loop 继续收口为 `grant-user-loop`，并把 `open_loop / inspect_progress / inspect_cockpit / build_direct_entry / build_submission_ready_package` 冻结成当前用户动作面；其中 `grant-progress / grant-cockpit` 继续是 controller-owned、read-only 的 direct-product projection。当前 manifest 也已经开始带出 `family_orchestration` companion preview，用来暴露 grant frontdoor 的 human gate 与 resume 边界；现在又统一补上了 `product_entry_quickstart` companion，用 step list 回答当前 frontdoor、grant loop 续跑、progress / cockpit 观察以及本地 submission-ready 交付导出的推荐步骤，并额外补上 `product_entry_overview` companion，把当前入口摘要、progress / resume 句柄、remaining gaps 与 human gate id 收成同型用户面；同时再补上轻量 `product_entry_readiness` companion，用来统一回答“现在能不能用、是否已经好用、是不是全自动、建议从哪进、目前还差什么”；更细粒度的 `grant_authoring_readiness` companion 则继续用结构化字段明确说明 author-side 国自然写作主线的深层成熟度与边界；`build-submission-ready-package` 已把 fail-closed 的本地 submission-ready 交付包导出收口成正式 command，而成熟的 grant-facing UX 与外部提交产品面仍未落地
- 当前 frontdoor 真相：`product-frontdesk` 现在也已经 landed；它会把 direct frontdoor、当前 user loop、projection 与 shared handoff builder 收成一份 controller-owned 的 product frontdesk contract，并受 `schemas/v1/product-frontdesk.schema.json` 约束、在生成时 fail-closed；其中 `family_orchestration` companion 的 gate / route status 已统一直接读取共享 author-side route truth，但仍不是新的 domain executor
- 当前 direct-entry 真相：`grant-direct-entry` 现在也已经 landed；它会把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 组合成新的 controller-owned product contract，但仍不是新的 domain executor
- 当前 user-loop 真相：`mainline-status`、`mainline-phase` 与 `grant-user-loop` 现在也已经 landed；其中 `grant-user-loop` 会把 repo mainline snapshot、`grant-direct-entry` 与 route-derived next action 收成当前 inbox-like shell，但仍不是新的 domain executor、也不是成熟 Web UI
- 当前统一协作模型：`Hermes-Agent` 持有 runtime substrate / orchestration，`Med Auto Grant` 持有 grant 对象边界、author-side domain truth 与 executor routing；当前 `direction_screening -> frozen` 的 authoring 主线、`revision` 与各类导出物都继续按 route 选择具体执行逻辑
- 当前 critique executor 真相：`critique` route 已 landed 到 `execute-critique-pass`，默认执行器仍是 `Codex CLI autonomous executor`；`critique_execution.executor` 默认会导出 `kind=codex_cli`，并把 `model_selection / reasoning_selection` 默认收口到 `inherit_local_codex_default`（仅当显式设置 `MED_AUTOGRANT_CODEX_MODEL` / `MED_AUTOGRANT_CODEX_REASONING_EFFORT` 时才覆盖）。与此同时，`execute-critique-pass` 现在也支持显式传入 `executor_kind=hermes_native_proof` 进入 experimental proof lane：它会真实调用 `run_agent.AIAgent.run_conversation(...)`，并且只有在完整 agent loop 跑完且出现真实工具事件时才承认自己是 `Hermes-native`
- 当前 full authoring executor 真相：`direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle` 现在都已经进入 landed route catalog；其中前半程默认走 `Codex CLI`，`revision` 与各导出物继续保持既有 deterministic / repo-side contract，`frozen` 保持 deterministic freeze pass
- 当前 Hermes-native 边界：只有“带 session substrate、route orchestration、domain mutation 与 durable state transition 的 full agent loop”才算 Hermes-native；单纯 chat relay / prompt relay 不算 landed Hermes-native executor
- 当前 contract 口径：`build-product-entry`、`product-entry-manifest`、`product-frontdesk`、`stage_action_envelope.executor_routing_contract`、`grant-progress`、`grant-cockpit`、`grant-user-loop`、`build-hosted-contract-bundle` 与 `build-submission-ready-package` 都已经是 schema-backed contract、repo-tracked controller surface 或正式 command surface，并在生成时 fail-closed；其中 frontdoor / projection / user loop / local delivery 对应 `product-entry-manifest.schema.json` / `product-frontdesk.schema.json` / `grant-progress.schema.json` / `grant-cockpit.schema.json` / `grant-user-loop.schema.json` / `submission-ready-package.schema.json`，hosted bundle 现在额外显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，而共享 `domain_entry_contract` 现在还会固定 `supported_commands` 与 `command_contracts`
- 当前 external caller 口径：hosted caller / 外部 caller 已经可以直接消费上述合同，并按 `supported_commands` / `command_contracts` 调用已 landed route，无需 repo-local helper
- 当前 direct-product projection 口径：`grant-progress / grant-cockpit` 当前只消费 `summarize-workspace`、`stage-route-report`、`critique-summary` 与 `build-product-entry` 的合同信息；它们通过 `grant-progress.schema.json` / `grant-cockpit.schema.json` 受 generation-time fail-closed 校验，且故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前 direct-entry composition 口径：`grant-direct-entry` 当前会复用 `grant-progress`、`grant-cockpit`、`build-product-entry(entry_mode=direct)` 与 `build-product-entry(entry_mode=opl-handoff)`，并通过 `grant-direct-entry.schema.json` 受 generation-time fail-closed 校验；它同样故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前 direct user loop 口径：`grant-user-loop` 当前会复用 `mainline-status`、`mainline-phase` 与 `grant-direct-entry`，并把推荐 route 直接投影成 landed command next-action 卡片；从 `direction_screening` 到 `frozen` 的 authoring 主线现在都能直接返回带具体 runtime-state 输出路径的可执行 command，而不再把前半程写成 pending-handoff 或要求用户手填 `<output-path>`；`grant-user-loop` 通过 `grant-user-loop.schema.json` 受 generation-time fail-closed 校验，并且同样故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前用户动作面口径：`product-entry-manifest` 新增的 `frontdesk_surface`、`operator_loop_actions` 与 `grant-user-loop` 保持同一真相；外部 caller 可以先定位 `product-frontdesk` 这个 direct frontdesk，再直接消费 `open_loop / inspect_progress / inspect_cockpit / build_direct_entry`，而不必自己猜 grant-facing 第一棒命令组合
- 当前 frontdoor companion 口径：`grant-progress` / `product-entry-manifest` / `product-frontdesk` 上的 `family_orchestration` companion 现在统一直接读取共享 author-side route truth，因此像 `question_refinement` 这类已 landed route 不会再被误投成 `pending / requested`

## OPL family orchestration contracts（对齐方向）

- `OPL` 顶层将冻结 5 类 family contracts：family event envelope、family checkpoint lineage、family action graph、family human gate、family product-entry manifest v2。
- `Med Auto Grant` 当前优先对齐面：`grant-progress / grant-cockpit / grant-direct-entry / grant-user-loop`，并对齐到 family action graph / family human gate / family product-entry manifest v2；当前已先落下 `family_orchestration` companion preview，domain 侧继续保持 `workspace / draft / program` 的真相边界。
- 本轮对齐不引入 `CrewAI` 依赖，不把 `OPL` 写成 runtime owner，也不宣称已完成跨仓 runtime core ingest；真实状态仍是上游 `Hermes-Agent` 作为 runtime substrate owner，MAG 维持 family-level contract-first 对齐与 domain-owned truth。

## 当前基线（repo-verified）

- Latest absorbed runtime slice：`Upstream Hermes-Agent Fast Cutover`
- Historical owner line：`post-R5A local runtime closeout / honest stop`
- Previous truthful closeout baseline：`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
- repo-tracked current truth 入口：
  - `contracts/runtime-program/current-program.json`
  - `docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md`
  - `docs/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`
  - `docs/specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md`
  - `docs/specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md`
  - `docs/specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`
  - `docs/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md`
  - `docs/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`
  - `docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md`
  - `docs/specs/2026-04-13-p4e-schema-backed-frontdesk-and-manifest-current-truth.md`
  - `docs/specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md`
  - `docs/specs/2026-04-13-critique-codex-cli-autonomous-executor-current-truth.md`
  - `docs/specs/2026-04-13-hermes-native-critique-proof-current-truth.md`
  - `docs/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md`（`2026-04-12` 历史快照；已被 `2026-04-13-full-grant-authoring-executor-current-truth.md` supersede）
  - `docs/specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md`（`2026-04-12` 历史快照；当前主线只保留其 schema 兼容意义）
  - `docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
  - `docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`

## 当前阶段（active mainline）

- Current phase：`P4 mature direct grant product entry`
- Active tranche：`P4.F local submission-ready package landing`
- Current owner line：`CLI-first with real upstream Hermes-Agent runtime substrate`

## OPL 对齐的理想目标与阶段图

- 理想目标：
  - `OPL` 保持 family-level 顶层入口与 gateway
  - `Med Auto Grant Product Entry` 作为 domain direct entry
  - `Hermes-Agent` 保持 runtime substrate owner
  - `Med Auto Grant` 保持 author-side grant truth / route / export owner
- 阶段图：
  - `P1` `Hermes substrate cutover`：已完成
  - `P2` `service-safe domain contract convergence`：已完成
  - `P3` `hosted caller / OPL consumption proof`：已完成
  - `P4` `mature direct grant product entry`：下一阶段
  - 当前已 landed 的第一棒：`P4.A direct grant progress / cockpit projection`
  - 当前已 landed 的第二棒：`P4.B direct grant entry composition`
  - 当前已 landed 的第三棒：`P4.C mainline status and grant user loop`
  - 当前已 landed 的第四棒：`P4.D full grant authoring executor landing`
  - 当前已 landed 的第五棒：`P4.E schema-backed frontdesk and manifest contract landing`
  - 当前已 landed 的第六棒：`P4.F local submission-ready package landing`

## 长线目标（规划层）

- 保持上游 `Hermes-Agent` 继续作为 runtime substrate owner，而不是退回 repo-local helper 主责。
- 保留旧 `CLI-first + host-agent` 本地 runtime 作为已验证基线、兼容桥和回归 oracle，而不是长期终态。
- 在真实上游 substrate 上继续延续 `workspace -> critique -> revision -> final package -> hosted contract bundle` 这条 author-side grant mainline。
- 在不改写 grant 对象边界的前提下，把 `Med Auto Grant Product Entry` 与 `OPL` handoff 壳补到真实 runtime substrate 之上。

## 当前优先事项

1. 保持真实 upstream substrate、service-safe domain entry、`build-product-entry`、`grant-progress / grant-cockpit`、`grant-direct-entry`、`grant-user-loop`、`build-hosted-contract-bundle`、`build-submission-ready-package`、external caller consumption proof 与 author-side artifact/export surface 持续全绿。
2. 下一步：在已 landed 的本地 submission-ready 交付面基础上，继续把 Word/PDF 定稿、图件生产、最终格式审查与外部提交边界拆成新的 repo-tracked truth，而不是继续口头放大为“已全自动”。
3. 继续沿 `docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md` 的口径推进，不把 repo-local adapter 重新写回 runtime owner。
4. 项目级 `.runtime-program/` 已退役；机器本地 session / log / report / prompt 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
5. 已 landed 的 lightweight `product entry` / `OPL -> Med Auto Grant` handoff shell 现在由 `build-product-entry` 承载；后续只允许沿同一 shared envelope 继续收口，不回头扩写 repo-local runtime owner 叙事。
6. `stage_action_envelope` 与 `build-product-entry` 现在都带同一份 `executor_routing_contract`；其中 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle` 都已经是已 landed route。
7. `execute-critique-pass` 当前默认执行器固定为 `Codex CLI autonomous executor`；默认 `model / reasoning` 继承本机 Codex 默认（`inherit_local_codex_default`），显式环境变量覆盖仍受控保留；同时现在新增了 `executor_kind=hermes_native_proof` 的 experimental proof lane，但它不改写默认执行器。
8. `pending-handoff-requirements.schema.json` 现在只保留历史兼容与旧真相追溯用途；当前主线 route output 已不再依赖 pending handoff contract 推进 authoring 主线。
9. Hermes-native 口径只认 full agent loop，不认 chat relay；当前 `critique` 的 experimental proof lane 已经通过 `run_agent.AIAgent.run_conversation(...)` 落到一条真实 full-loop route，但若本机 Hermes 仍走 `custom + chat_completions`，当前只承认 `FULL_AGENT_LOOP_PRESENT_BUT_NOT_YET_EQUIVALENT_TO_CODEX / PROVIDER_REASONING_NOT_PROVED_KEEP_DEFAULT`，不会把它误写成默认 executor 已替代。
10. `service-safe-domain-surface.schema.json`、`pending-handoff-requirements.schema.json`、`executor-routing-contract.schema.json`、`product-entry.schema.json`、`product-entry-manifest.schema.json`、`product-frontdesk.schema.json` 与 `hosted-contract-bundle.schema.json` 现在已经进入 repo-tracked schema index；任何后续 product-entry / frontdoor / routing / hosted contract bundle 变更都必须同步更新 schema、tests 与 current truth。
11. `P3` 已经证明 external hosted caller / `OPL` caller 可以直接消费已冻结的 `domain_entry_contract`、`schema_contract`、`authoring_contract`、`supported_commands` 与 `command_contracts`；后续继续沿 `P4` 的诚实 product 面推进，而不是回头重新发明新的 repo-local hosted helper。
12. `P4.A / P4.B / P4.C / P4.D / P4.E / P4.F` 当前只允许沿 controller-owned 的 product 面与已冻结的 service-safe route catalog 继续推进：`grant-progress`、`grant-cockpit`、`grant-direct-entry`、`grant-user-loop`、`product-entry-manifest`、`product-frontdesk`、`build-submission-ready-package` 与 `execute-direction-screening-pass` 到 `build-hosted-contract-bundle` 这一整套 surface 现在虽然都已经是 schema-backed、generation-time fail-closed 的 product contract、controller surface 或 landed command，但仍不能被误写成已落地的 Web UI、hosted runtime、`OPL Gateway` 或官网自动提交器。

## 默认验证

- 默认最小验证：`scripts/verify.sh`（`make test-fast`）。
- meta 验证：`scripts/verify.sh meta`。
- CLI smoke：`scripts/verify.sh cli-smoke`。
- full 验证：`scripts/verify.sh full`。
