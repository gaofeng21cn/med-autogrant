# 当前状态

Date: `2026-04-13`

## 当前角色

- 仓库角色：医学 `Grant Ops` 的 author-side / proposal-facing `Domain Harness OS` 方向。
- 当前执行口径：`CLI-first + real upstream Hermes-Agent runtime substrate`。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。
- 当前入口真相：`operator entry` 与 `agent entry` 已存在；共享 envelope 的 lightweight `product entry` shell 已由 `build-product-entry` 落地；`product-entry-manifest` 现在会把当前 shell、shared handoff 模板、mainline snapshot、`product_entry_status` 状态摘要，以及显式的 `frontdesk_surface`、`operator_loop_surface`、`operator_loop_actions` 与 `recommended_shell / recommended_command` 冻结成 machine-readable discovery surface；当前 direct frontdesk 与 operator loop 都明确收口为 `grant-user-loop`，并把 `open_loop / inspect_progress / inspect_cockpit / build_direct_entry` 冻结成当前用户动作面；`grant-progress / grant-cockpit` 已把第一棒 controller-owned、read-only 的 direct-product projection 落地，而成熟的 grant-facing UX 仍未落地
- 当前 direct-entry 真相：`grant-direct-entry` 现在也已经 landed；它会把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 组合成新的 controller-owned product contract，但仍不是新的 domain executor
- 当前 user-loop 真相：`mainline-status`、`mainline-phase` 与 `grant-user-loop` 现在也已经 landed；其中 `grant-user-loop` 会把 repo mainline snapshot、`grant-direct-entry` 与 route-derived next action 收成当前 inbox-like shell，但仍不是新的 domain executor、也不是成熟 Web UI
- 当前统一协作模型：`Hermes-Agent` 持有 runtime substrate / orchestration，`Med Auto Grant` 持有 grant 对象边界、author-side domain truth 与 executor routing；单步 critique / revision / packaging 仍按 route 选择具体执行逻辑
- 当前 critique executor 真相：`critique` route 已 landed 到 `execute-critique-pass`，执行器是 `Codex CLI autonomous executor`；`critique_execution.executor` 会固定导出 `kind=codex_cli`，并把 `model_selection / reasoning_selection` 默认收口到 `inherit_local_codex_default`（仅当显式设置 `MED_AUTOGRANT_CODEX_MODEL` / `MED_AUTOGRANT_CODEX_REASONING_EFFORT` 时才覆盖）
- 当前 Hermes-native 边界：只有“带 session substrate、route orchestration、domain mutation 与 durable state transition 的 full agent loop”才算 Hermes-native；单纯 chat relay / prompt relay 不算 landed Hermes-native executor
- 当前 contract 口径：`build-product-entry`、`stage_action_envelope.executor_routing_contract`、`grant-progress`、`grant-cockpit`、`grant-user-loop` 与 `build-hosted-contract-bundle` 都已经是 schema-backed contract 或 repo-tracked controller surface，并在生成时 fail-closed；其中 projection / user loop 对应 `grant-progress.schema.json` / `grant-cockpit.schema.json` / `grant-user-loop.schema.json`，hosted bundle 现在额外显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，而共享 `domain_entry_contract` 现在还会固定 `supported_commands` 与 `command_contracts`
- 当前 external caller 口径：hosted caller / 外部 caller 已经可以直接消费上述合同，并按 `supported_commands` / `command_contracts` 调用已 landed route，无需 repo-local helper
- 当前 direct-product projection 口径：`grant-progress / grant-cockpit` 当前只消费 `summarize-workspace`、`stage-route-report`、`critique-summary` 与 `build-product-entry` 的合同信息；它们通过 `grant-progress.schema.json` / `grant-cockpit.schema.json` 受 generation-time fail-closed 校验，且故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前 direct-entry composition 口径：`grant-direct-entry` 当前会复用 `grant-progress`、`grant-cockpit`、`build-product-entry(entry_mode=direct)` 与 `build-product-entry(entry_mode=opl-handoff)`，并通过 `grant-direct-entry.schema.json` 受 generation-time fail-closed 校验；它同样故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前 direct user loop 口径：`grant-user-loop` 当前会复用 `mainline-status`、`mainline-phase` 与 `grant-direct-entry`，并把推荐 route 的 landed command / pending-handoff surface 投影成当前 next-action 卡片；其中 `drafting -> critique` 已是 landed command `execute-critique-pass`，其余未落地 route 继续维持 pending-handoff；`grant-user-loop` 通过 `grant-user-loop.schema.json` 受 generation-time fail-closed 校验，并且同样故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前用户动作面口径：`product-entry-manifest` 新增的 `frontdesk_surface`、`operator_loop_actions` 与 `grant-user-loop` 保持同一真相；外部 caller 可以先定位 direct frontdesk，再直接消费 `open_loop / inspect_progress / inspect_cockpit / build_direct_entry`，而不必自己猜 grant-facing 第一棒命令组合

## OPL family orchestration contracts（对齐方向）

- `OPL` 顶层将冻结 5 类 family contracts：family event envelope、family checkpoint lineage、family action graph、family human gate、family product-entry manifest v2。
- `Med Auto Grant` 当前优先对齐面：`grant-progress / grant-cockpit / grant-direct-entry / grant-user-loop`，并对齐到 family action graph / family human gate / family product-entry manifest v2；domain 侧继续保持 `workspace / draft / program` 的真相边界。
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
  - `docs/specs/2026-04-13-critique-codex-cli-autonomous-executor-current-truth.md`
  - `docs/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md`
  - `docs/specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md`
  - `docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
  - `docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`

## 当前阶段（active mainline）

- Current phase：`P4 mature direct grant product entry`
- Active tranche：`P4.D critique Codex CLI autonomous executor landing`
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

## 长线目标（规划层）

- 保持上游 `Hermes-Agent` 继续作为 runtime substrate owner，而不是退回 repo-local helper 主责。
- 保留旧 `CLI-first + host-agent` 本地 runtime 作为已验证基线、兼容桥和回归 oracle，而不是长期终态。
- 在真实上游 substrate 上继续延续 `workspace -> critique -> revision -> final package -> hosted contract bundle` 这条 author-side grant mainline。
- 在不改写 grant 对象边界的前提下，把 `Med Auto Grant Product Entry` 与 `OPL` handoff 壳补到真实 runtime substrate 之上。

## 当前优先事项

1. 保持真实 upstream substrate、service-safe domain entry、`build-product-entry`、`grant-progress / grant-cockpit`、`grant-direct-entry`、`grant-user-loop`、`build-hosted-contract-bundle`、external caller consumption proof 与 author-side artifact/export surface 持续全绿。
2. 下一步：把 `grant-progress / grant-cockpit / grant-direct-entry / grant-user-loop` 对齐到 family action graph / family human gate / family product-entry manifest v2，并继续维护 domain-owned truth。
3. 继续沿 `docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md` 的口径推进，不把 repo-local adapter 重新写回 runtime owner。
4. 项目级 `.runtime-program/` 已退役；机器本地 session / log / report / prompt 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
5. 已 landed 的 lightweight `product entry` / `OPL -> Med Auto Grant` handoff shell 现在由 `build-product-entry` 承载；后续只允许沿同一 shared envelope 继续收口，不回头扩写 repo-local runtime owner 叙事。
6. `stage_action_envelope` 与 `build-product-entry` 现在都带同一份 `executor_routing_contract`；其中 `critique / revision / artifact_bundle / final_package / hosted_contract_bundle` 都是已 landed route，其他 authoring stage 才是 `pending / handoff-required`。
7. `execute-critique-pass` 当前执行器固定为 `Codex CLI autonomous executor`；默认 `model / reasoning` 继承本机 Codex 默认（`inherit_local_codex_default`），显式环境变量覆盖仍受控保留。
8. 所有仍 pending 的 authoring route 继续带 route-specific `handoff_requirements`；`critique-summary` 只在 source workspace 已经位于 `critique / revision / frozen` review context 时才会被要求。
9. Hermes-native 口径只认 full agent loop，不认 chat relay；后续若替换 critique / revision / export 执行器，必须按 route 单独拿 truth 和 proof。
10. `service-safe-domain-surface.schema.json`、`pending-handoff-requirements.schema.json`、`executor-routing-contract.schema.json`、`product-entry.schema.json` 与 `hosted-contract-bundle.schema.json` 现在已经进入 repo-tracked schema index；任何后续 product-entry / routing / hosted contract bundle 变更都必须同步更新 schema、tests 与 current truth。
11. `P3` 已经证明 external hosted caller / `OPL` caller 可以直接消费已冻结的 `domain_entry_contract`、`schema_contract`、`authoring_contract`、`supported_commands` 与 `command_contracts`；后续继续沿 `P4` 的诚实 product 面推进，而不是回头重新发明新的 repo-local hosted helper。
12. `P4.A / P4.B / P4.C / P4.D` 当前只允许沿 controller-owned 的 product 面继续推进：`grant-progress`、`grant-cockpit`、`grant-direct-entry`、`grant-user-loop` 与 `execute-critique-pass` 现在虽然都已经是 schema-backed、generation-time fail-closed 的 product contract 或 controller surface，但仍不能被误写成新的 service-safe domain executor、hosted bundle command catalog 项，或已落地的 Web UI / hosted runtime。

## 默认验证

- 默认最小验证：`scripts/verify.sh`（`make test-fast`）。
- meta 验证：`scripts/verify.sh meta`。
- CLI smoke：`scripts/verify.sh cli-smoke`。
- full 验证：`scripts/verify.sh full`。
