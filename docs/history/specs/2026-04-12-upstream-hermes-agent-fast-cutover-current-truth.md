# Upstream Hermes-Agent Fast Cutover Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是已物理归档到 `docs/history/specs/` 的 `retired_provider_proof`。请先读取 `docs/status.md`、核心五件套、`docs/specs/specs_lifecycle_map.md` 与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_upstream_hermes_fast_cutover_proof_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-12 upstream Hermes-Agent explicit proof lane、service-safe domain entry 与 fresh proof 形成过程。当前 default runtime owner、OPL/Temporal provider、executor adapter、route catalog、hosted caller boundary 与机器行为以核心五件套、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

Date: `2026-04-12`

## Activation Status

- Phase: `Upstream Hermes-Agent Fast Cutover`
- Active tranche: `Explicit Hermes proof lane / service-safe domain entry / fresh proof`
- Status: `explicit proof lane / historical runtime proof`

## Goal

把 `Med Auto Grant` 从：

- `CLI-first + repo-local runtime baseline`

切到：

- `CLI-first + explicit Hermes-Agent proof lane`

同时保持 author-side grant mainline 不漂移：

- `NSFCWorkspace`
- `grant_run_id / workspace_id / draft_id / program_id`
- `critique-summary`
- `stage-route-report`
- `artifact bundle / final package / hosted contract bundle`

## Landed Runtime Facts

### 1. 真实 upstream 依赖与连接证据已经 repo-tracked

- `pyproject.toml` 现在只在 `proof` optional extra 中声明 `hermes-agent[acp]`；默认安装不拉取上游 Hermes-Agent。
- `[tool.uv.sources]` 把 `hermes-agent` 固定到上游仓库 `NousResearch/hermes-agent` 的 commit `96051955755a83f22afed5e3501d447462fbe9c8`。
- `probe-upstream-hermes` 现在会显式探测并回显：
  - `hermes` CLI
  - `hermes acp`
  - `run_agent.AIAgent`
  - `hermes_state.SessionDB`
  - `acp_adapter.session.SessionManager`
  - runtime root 与 `state.db` 路径

### 2. Hermes session substrate 只保留为显式 proof lane

- `runtime-run` / `runtime-resume` 的 attempt ledger 不再由 repo-local journal 长度主责。
- `src/med_autogrant/upstream_hermes.py` 现在通过真实上游 `hermes_state.SessionDB` 记录 attempt。
- 显式 Hermes proof lane 的 runtime root 固定到：
  - `$CODEX_HOME/projects/med-autogrant/runtime-state/hermes/`
- 如需显式隔离，可通过：
  - `MED_AUTOGRANT_HERMES_HOME`
- valid workspace path 上，Hermes session handle 继续沿用同一 `grant_run_id`。
- `validation_failed` path 上，如果 workspace 缺少合法 `grant_run_id`，则只允许退到 journal-scoped substrate session handle；该 handle 只服务 substrate durability，不得伪造新的 domain `grant_run_id`。

### 3. author-side domain logic 继续留在 repo 内

以下语义继续由仓内 domain code 承担，而不是让 substrate 偷换语义：

- `NSFCWorkspace` validation
- critique / revision / re-review linkage
- stage route / verification checkpoint
- artifact bundle
- final package
- hosted contract bundle

`domain_runtime.py` 在当前真相下应被理解为：

- repo-side domain adapter / orchestrator

而不是：

- runtime substrate owner

### 4. service-safe domain entry 已收口

- 新增 `src/med_autogrant/domain_entry.py`
- `MedAutoGrantDomainEntry` 提供结构化 command dispatch
- 当前支持的 service-safe command 与 CLI 命令面一一对应：
  - `validate-workspace`
  - `summarize-workspace`
  - `next-step`
  - `critique-summary`
  - `stage-route-report`
  - `probe-upstream-hermes`
  - `runtime-run`
  - `runtime-resume`
  - `build-artifact-bundle`
  - `execute-revision-pass`
  - `build-final-package`
  - `build-hosted-contract-bundle`
- CLI 仍然是 formal entry，但现在通过同一条 service-safe adapter 进入 runtime/domain path。
- 这条 adapter 允许未来 `OPL Gateway` 复用同一结构化 entry contract，而不需要先发明自然语言壳。

### 5. author-side executor routing contract 已显式冻结

- `stage_action_envelope` 与 `build-product-entry` 现在都会输出 `executor_routing_contract`
- 这份 contract 明确区分：
  - `current_stage_route`
  - `recommended_executor_route`
- `author_side_route_catalog` 现在会列出完整 authoring matrix，而不只是 critique + landed export routes
- 当前 landed route 继续是：
  - `revision -> execute-revision-pass`
  - `artifact_bundle -> build-artifact-bundle`
  - `final_package -> build-final-package`
  - `hosted_contract_bundle -> build-hosted-contract-bundle`
- 当前 `author_side_route_catalog` 已经全部收口为 landed service-safe command surface。

### 6. product-entry / routing / hosted bundle surface 现在已经收口成 schema-backed contract

- `schemas/v1/service-safe-domain-surface.schema.json`
- `schemas/v1/executor-routing-contract.schema.json`
- `schemas/v1/product-entry.schema.json`
- `schemas/v1/hosted-contract-bundle.schema.json`

这些 schema 现在已经进入 `schemas/v1/schema-index.json`，并且：

- `runtime-run.stage_action_envelope.executor_routing_contract` 会先过 schema 校验，再对照冻结 route truth 做 fail-closed 比对
- `build-product-entry.product_entry` 也会先过 schema 校验，并且内嵌的 `executor_routing_contract` 同样必须与当前冻结 truth 完全一致
- `build-hosted-contract-bundle.hosted_contract_bundle` 现在也会先过 schema 校验，并且要求 bundle 内的 `domain_entry_contract`、`schema_contract`、`authoring_contract` 与当前冻结 truth 完全一致
- 当前这层 schema-backed closeout 只是在把 author-side contract 机器可读化，不是在新增本地 executor surface

## What Did Not Change

- formal entry 仍是 `CLI`
- `supported_protocol_layer` 仍是 `MCP`（future layer，不等于 public runtime 已开放）
- `internal_controller_surface` 仍是 `controller`
- 当前仓库主线仍按 `Auto-only` 理解
- 旧 `Codex-default host-agent runtime` 只保留为 compatibility bridge / regression oracle
- 不扩 `P5` federation / second family / Human-in-the-loop sibling

## Fresh Proof Surface

repo 现在至少有下面这些 fresh proof：

1. `probe-upstream-hermes` 能返回真实 upstream entrypoints 与 runtime root/state db 证据
2. `runtime-run` / `runtime-resume` 能把 attempt ledger 写入真实上游 `SessionDB`
3. `validation_failed` path 仍保留 canonical route/checkpoint shape，并可继续 durable resume
4. `MedAutoGrantDomainEntry` 能在真实 upstream substrate 上完成：
   - critique route proof
   - revision pass
   - run/resume
   - final package
   - hosted contract bundle
5. `executor_routing_contract` 已把完整 author-side route catalog 收口成 landed command surface
6. `drafting -> critique` 已经证明会稳定落到 landed `execute-critique-pass`
7. `revision(completed revised switch) -> critique` 返场路径也已经在 `runtime-run` / `build-product-entry` 上给出一致的 landed critique proof

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_upstream_hermes.py tests/test_local_runtime.py tests/test_domain_runtime.py tests/test_domain_entry.py -q`
- `uv run pytest tests/test_program_control_surfaces.py tests/test_hosted_contract_bundle.py -q`
- invalid workspace 的 `runtime-run / runtime-resume` 实际手工证明

## Honest Boundary

这条 current truth 只说明：

- 真实 upstream Hermes substrate 已经证明可接住显式 proof lane 的 session durability
- service-safe domain entry 已形成
- author-side grant mainline 没有漂移
- product-layer follow-up 需要查看：
  - `docs/history/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`

它不意味着：

- actual hosted runtime 已完成
- public MCP/controller surface 已开放
- `P5` federation / gateway story 已展开
- submission-grade autopilot 已完成
