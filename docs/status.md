# 当前状态

Date: `2026-04-12`

## 当前角色

- 仓库角色：医学 `Grant Ops` 的 author-side / proposal-facing `Domain Harness OS` 方向。
- 当前执行口径：`CLI-first + real upstream Hermes-Agent runtime substrate`。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。
- 当前入口真相：`operator entry` 与 `agent entry` 已存在；共享 envelope 的 lightweight `product entry` shell 已由 `build-product-entry` 落地，但成熟的 grant-facing UX 仍未落地
- 当前统一协作模型：`Hermes-Agent` 持有 runtime substrate / orchestration，`Med Auto Grant` 持有 grant 对象边界、author-side domain truth 与 executor routing；单步 critique / revision / packaging 仍按 route 选择具体执行逻辑
- 当前 contract 口径：`build-product-entry` 与 `stage_action_envelope.executor_routing_contract` 都已经是 schema-backed contract，并在生成时 fail-closed

## 当前基线（repo-verified）

- Latest absorbed runtime slice：`Upstream Hermes-Agent Fast Cutover`
- Historical owner line：`post-R5A local runtime closeout / honest stop`
- Previous truthful closeout baseline：`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
- repo-tracked current truth 入口：
  - `contracts/runtime-program/current-program.json`
  - `docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md`
  - `docs/specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`
  - `docs/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`
  - `docs/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md`
  - `docs/specs/2026-04-12-critique-pending-handoff-contract-current-truth.md`
  - `docs/specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md`
  - `docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
  - `docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`

## 当前阶段（active mainline）

- Current phase：`Upstream Hermes-Agent Fast Cutover`
- Active tranche：`Real Hermes substrate / service-safe domain entry / fresh proof`
- Current owner line：`CLI-first with real upstream Hermes-Agent runtime substrate`

## 长线目标（规划层）

- 保持上游 `Hermes-Agent` 继续作为 runtime substrate owner，而不是退回 repo-local helper 主责。
- 保留旧 `CLI-first + host-agent` 本地 runtime 作为已验证基线、兼容桥和回归 oracle，而不是长期终态。
- 在真实上游 substrate 上继续延续 `workspace -> critique -> revision -> final package -> hosted contract bundle` 这条 author-side grant mainline。
- 在不改写 grant 对象边界的前提下，把 `Med Auto Grant Product Entry` 与 `OPL` handoff 壳补到真实 runtime substrate 之上。

## 当前优先事项

1. 保持真实 upstream substrate、service-safe domain entry、`build-product-entry` 与 author-side artifact/export surface 持续全绿。
2. 继续沿 `docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md` 的口径推进，不把 repo-local adapter 重新写回 runtime owner。
3. 项目级 `.runtime-program/` 已退役；机器本地 session / log / report / prompt 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
4. 已 landed 的 lightweight `product entry` / `OPL -> Med Auto Grant` handoff shell 现在由 `build-product-entry` 承载；后续只允许沿同一 shared envelope 继续收口，不回头扩写 repo-local runtime owner 叙事。
5. `stage_action_envelope` 与 `build-product-entry` 现在都带同一份 `executor_routing_contract`；当前 `critique` 继续诚实标为 `pending / handoff-required`，而 `revision / artifact_bundle / final_package / hosted_contract_bundle` 才是已 landed route。
6. 所有 pending authoring route 现在都额外带 route-specific `handoff_requirements`；当前不再只有 critique 拥有 machine-readable handoff contract。
7. `critique-summary` 只在 source workspace 已经位于 `critique / revision / frozen` review context 时才会被要求；`drafting -> critique` 这类 handoff 继续只要求 `summarize-workspace / stage-route-report`。
8. 后续若继续替换 critique / revision / export 的具体执行器，必须按 route 单独拿 truth 和 proof；不允许因为 substrate 已统一就自动改写 authoring semantics。
9. `service-safe-domain-surface.schema.json`、`pending-handoff-requirements.schema.json`、`executor-routing-contract.schema.json` 与 `product-entry.schema.json` 现在已经进入 repo-tracked schema index；任何后续 product-entry / routing contract 变更都必须同步更新 schema、tests 与 current truth。

## 默认验证

- 默认最小验证：`scripts/verify.sh`（`make test-fast`）。
- meta 验证：`scripts/verify.sh meta`。
- CLI smoke：`scripts/verify.sh cli-smoke`。
- full 验证：`scripts/verify.sh full`。
