# 当前状态

Date: `2026-04-18`

## 当前角色

- 仓库角色：`OPL` 顶层 GUI / management shell 下的一级医学基金 domain module / agent，负责 author-side grant truth、route、review gate 与 package export。
- 当前执行口径：Codex 是默认交互与执行路径；`Hermes-Agent` 是显式选择时的备用模式、长期在线网关与 proof lane。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。
- 当前入口真相：用户路径收口为 `product frontdesk` -> `product user-loop` -> `workspace progress / workspace cockpit` -> `product direct-entry` -> landed `pass` / `package` commands。`product build-entry` 与 lightweight `product entry` shell 继续作为 machine-readable domain/API catalog 的构建层。
- 当前 frontdesk 真相：`product frontdesk` 是 controller-owned direct frontdoor contract，读取当前 user loop、projection 与 route truth，并通过 `product-frontdesk.schema.json` generation-time fail-closed 校验。
- 当前 direct-entry 真相：`product direct-entry` 组合 `workspace progress`、`workspace cockpit` 与 direct / `opl-handoff` entry mode，是 controller-owned product contract；`OPL -> Med Auto Grant` 相关 wording 只作为兼容 entry-mode 和内部参考存在。
- 当前 user-loop 真相：`mainline status`、`mainline phase` 与 `product user-loop` 把 repo mainline snapshot、direct-entry composition 与 route-derived next action 收成当前 inbox-like shell，负责下一步可执行 command 的可见性。
- 当前默认执行真相：`direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle` 都已进入 landed route catalog；前半程默认走 Codex CLI，`critique` 默认走 `Codex CLI autonomous executor`，`revision` 与各导出物继续保持既有 deterministic / repo-side contract，`frozen` 保持 deterministic freeze pass。
- 当前 Hermes-Agent 真相：`Hermes-Agent` 保留为显式备用模式、长期在线网关与 `hermes_native_proof` proof lane。`pass critique --executor hermes_native_proof` 会调用 `run_agent.AIAgent.run_conversation(...)`，并要求完整 agent loop 与真实工具事件；默认执行器仍是 Codex。
- 当前 shared helper 真相：从 `2026-04-18` 起，MAG 复用 `one-person-lab` 持有的 `opl-harness-shared` 来生成 managed runtime / family orchestration / product-frontdesk 相关公共 payload helper；用户认知中心仍是 OPL 壳、MAG domain agent、Codex default、Hermes backup。
- 当前 contract 口径：`product build-entry`、`product manifest`、`product frontdesk`、`stage_action_envelope.executor_routing_contract`、`workspace progress`、`workspace cockpit`、`product user-loop`、`package hosted-contract-bundle` 与 `package submission-ready` 都已经是 schema-backed contract、repo-tracked controller surface 或正式 command surface，并在生成时 fail-closed；其中 frontdoor / projection / user loop / local delivery 对应 `product-entry-manifest.schema.json` / `product-frontdesk.schema.json` / `grant-progress.schema.json` / `grant-cockpit.schema.json` / `grant-user-loop.schema.json` / `submission-ready-package.schema.json`，hosted bundle 额外导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，共享 `domain_entry_contract` 固定 `supported_commands` 与 `command_contracts`。
- 当前 external caller 口径：hosted caller / 外部 caller 可以直接消费上述合同，并按 `supported_commands` / `command_contracts` 调用已 landed route，无需 repo-local helper。
- 当前 direct-product projection 口径：`workspace progress / workspace cockpit` 是 controller-owned、read-only product projection，消费 `workspace summarize`、`workspace route-report`、`workspace critique-summary` 与 `product build-entry` 的合同信息，并通过 `grant-progress.schema.json` / `grant-cockpit.schema.json` generation-time fail-closed 校验。

## OPL family orchestration contracts（对齐方向）

- `OPL` 是顶层 GUI / management shell，负责 family navigation、domain module visibility、task visibility 与 human gate 可见性。
- `Med Auto Grant` 是一级 grant domain module / agent，优先对齐 `workspace progress / workspace cockpit / product direct-entry / product user-loop`，并把 `workspace / draft / program` 作为 domain truth 边界。
- `Codex` 是默认交互与执行路径；`Hermes-Agent` 是备用模式与长期在线网关；MAG 继续保留 grant 质量门控、review gate、package gate 与 route truth。

## 当前基线（repo-verified）

- Latest absorbed runtime slice：`Upstream Hermes-Agent Fast Cutover`
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

- Current phase：`P4 mature direct grant frontdesk / user-loop`
- Active tranche：`P4.F local submission-ready package landing`
- Current execution line：`OPL shell + MAG domain agent + Codex default execution + Hermes-Agent backup gateway`

## OPL 对齐的理想目标与阶段图

- 理想目标：
  - `OPL` 保持 family-level 顶层 GUI / management shell
  - `Med Auto Grant` 作为一级 domain module / agent
  - `Codex` 保持默认交互与执行路径
  - `Hermes-Agent` 保持备用模式与长期在线网关
  - `Med Auto Grant` 保持 author-side grant truth / route / export owner
- 阶段图：
  - `P1` `Hermes substrate cutover`：已完成，作为内部运行时历史与备用网关基础保留
  - `P2` `service-safe domain contract convergence`：已完成
  - `P3` `hosted caller / OPL consumption proof`：已完成
  - `P4` `mature direct grant frontdesk / user-loop`：下一阶段
  - 当前已 landed 的第一棒：`P4.A direct grant progress / cockpit projection`
  - 当前已 landed 的第二棒：`P4.B direct grant entry composition`
  - 当前已 landed 的第三棒：`P4.C mainline status and grant user loop`
  - 当前已 landed 的第四棒：`P4.D full grant authoring executor landing`
  - 当前已 landed 的第五棒：`P4.E schema-backed frontdesk and manifest contract landing`
  - 当前已 landed 的第六棒：`P4.F local submission-ready package landing`

## 长线目标（规划层）

- 把用户认知主线固定为 `OPL` 壳下的 MAG domain agent，并以 Codex 作为默认交互与执行。
- 保持 `Hermes-Agent` 作为备用模式与长期在线网关，在显式 route / proof lane 中使用。
- 继续延续 `workspace -> critique -> revision -> final package -> hosted contract bundle` 这条 author-side grant mainline。
- 保持 `Med Auto Grant` 的 grant 对象边界：`workspace_id`、`draft_id`、`grant_run_id`、`program_id`、route catalog、review gate 与 package gate。

## 当前优先事项

1. 保持 service-safe domain entry、`product build-entry`、`product frontdesk`、`workspace progress / workspace cockpit`、`product direct-entry`、`product user-loop`、`package hosted-contract-bundle`、`package submission-ready`、external caller consumption proof 与 author-side artifact/export surface 持续全绿。
2. 下一步：在已 landed 的本地 submission-ready 交付面基础上，继续把 Word/PDF 定稿、图件生产、最终格式审查与外部提交边界拆成新的 repo-tracked truth。
3. 继续沿 Codex-default 的 authoring execution 路线推进，把 `Hermes-Agent` 明确保留为备用模式、长期在线网关与显式 proof lane。
4. 项目级 `.runtime-program/` 已退役；机器本地 session / log / report / prompt 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
5. 已 landed 的 lightweight `product entry` / `OPL -> Med Auto Grant` shell 现在由 `product build-entry` 承载；后续把这层作为内部兼容 entry mode 与 domain/API catalog 维护。
6. `stage_action_envelope` 与 `product build-entry` 现在都带同一份 `executor_routing_contract`；其中 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle` 都已经是已 landed route。
7. `pass critique` 当前默认执行器固定为 `Codex CLI autonomous executor`；默认 `model / reasoning` 继承本机 Codex 默认（`inherit_local_codex_default`），显式环境变量覆盖仍受控保留；同时现在新增了 `executor_kind=hermes_native_proof` 的 experimental proof lane，但它不改写默认执行器。
8. `pending-handoff-requirements.schema.json` 现在只保留历史追溯用途；当前主线 route output 已完全收口为 landed route catalog。
9. Hermes-native 口径只认 full agent loop，不认 chat relay；当前 `critique` 的 experimental proof lane 已经通过 `run_agent.AIAgent.run_conversation(...)` 落到一条真实 full-loop route，但若本机 Hermes 仍走 `custom + chat_completions`，当前只承认 `FULL_AGENT_LOOP_PRESENT_BUT_NOT_YET_EQUIVALENT_TO_CODEX / PROVIDER_REASONING_NOT_PROVED_KEEP_DEFAULT`，不会把它误写成默认 executor 已替代。
10. `service-safe-domain-surface.schema.json`、`executor-routing-contract.schema.json`、`product-entry.schema.json`、`product-entry-manifest.schema.json`、`product-frontdesk.schema.json` 与 `hosted-contract-bundle.schema.json` 现在已经进入 repo-tracked schema index；任何后续 product-entry / frontdoor / routing / hosted contract bundle 变更都必须同步更新 schema、tests 与 current truth。
11. `P3` 已经证明 external hosted caller / `OPL` caller 可以直接消费已冻结的 `domain_entry_contract`、`schema_contract`、`authoring_contract`、`supported_commands` 与 `command_contracts`；后续继续沿 `P4` 的诚实 product 面推进。
12. `P4.A / P4.B / P4.C / P4.D / P4.E / P4.F` 当前只允许沿 controller-owned 的 product 面与已冻结的 service-safe route catalog 继续推进：`workspace progress`、`workspace cockpit`、`product direct-entry`、`product user-loop`、`product manifest`、`product frontdesk`、`package submission-ready` 与 `pass direction-screening` 到 `package hosted-contract-bundle` 这一整套 surface 现在都是 schema-backed、generation-time fail-closed 的 product contract、controller surface 或 landed command；Web UI、hosted runtime、`OPL Gateway` 和官网自动提交器继续作为外部产品边界管理。

## 默认验证

- 默认最小验证：`scripts/verify.sh`（`make test-fast`）。
- meta 验证：`scripts/verify.sh meta`。
- CLI smoke：`scripts/verify.sh cli-smoke`。
- full 验证：`scripts/verify.sh full`。
