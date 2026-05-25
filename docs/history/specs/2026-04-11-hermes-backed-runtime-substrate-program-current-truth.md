# Hermes-Backed Runtime Substrate Program Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 `superseded_provider_proof` / historical provenance。它不定义当前 MAG runtime owner、provider owner、compatibility bridge 或 required runnable path。当前 owner line 是 `codex_cli` default executor + MAG-owned grant truth / quality / route / export authority + OPL stage-led framework consuming MAG descriptor/projection。`hermes_agent` 只表示显式非默认 executor/proof/provenance lane。

Owner: `Med Auto Grant`
Purpose: `historical_hermes_runtime_substrate_program_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-11 Hermes-backed runtime substrate program、runtime-state provenance 与 fail-closed migration lessons。当前 MAG runtime owner、default provider、OPL/Temporal hosted execution、attempt ledger 与机器行为以核心五件套、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

当前处置：

- Superseded：Hermes-backed runtime substrate as mainline owner、local host-agent compatibility bridge、future Hermes host compatibility handoff。
- Retained：proof vocabulary、fail-closed lessons、runtime-state provenance，以及解释为什么 Hermes-first 没有保留为默认路线的 audit path。
- Direct retirement posture：任何只为保留 Hermes-backed owner 或 compatibility bridge 的旧 module/interface/test，都应迁到当前 owner surface；没有 active caller 后删除或归档。

Date: `2026-04-11`

## Goal

本文记录 2026-04-11 曾经尝试把 `Med Auto Grant` 的产品 runtime 主线从旧的 `CLI-first + host-agent runtime` closeout 转向 `CLI-first + Hermes-backed runtime substrate` program。该路线现在只作 historical/provider proof 读取。

这里冻结的不是：

- actual hosted runtime 已完成；
- `MCP` 或 `controller` 已变成 public runtime formal entry；
- submission-grade autopilot 已成立。

当时冻结的是：

- `Hermes-backed runtime substrate` 作为当时设想的新 runtime owner；
- 旧 local host-agent runtime 作为当时设想的 migration baseline、compatibility bridge、regression oracle；
- `CLI / MCP / controller / Hermes substrate / MedAutoGrant domain logic` 的边界；
- `contracts/runtime-program/current-program.json` 成为 repo-tracked current-program pointer；
- 机器本地 session / log / report / prompt 状态统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`；
- `runtime-run / runtime-resume` 的默认 journal durable surface 固定为 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/<grant_run_id>.json`；
- `build-hosted-contract-bundle` 当时需要显式导出 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract`，作为 future Hermes host 的 handoff contract；
- 在当前 repo 内哪些能力可以诚实迁入 Hermes，哪些必须继续留在 domain logic。

## Current Pointer

- Repo-tracked current-program pointer: `contracts/runtime-program/current-program.json`
- Current `program_id`: `med-autogrant-mainline`
- Previous absorbed baseline: `R5.A / Hosted-Friendly Session Boundary`
- Previous truthful closeout: `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
- Historical phase: `Hermes Runtime Substrate Program`
- Historical tranche: `H1 / Hermes-Owned Runtime Path`
- Current owner line: superseded; see `docs/status.md`, `docs/decisions.md`, and `docs/specs/specs_lifecycle_map.md`

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP` 继续作为历史 closeout truth 保留，但它现在只回答：

- 旧 local host-agent runtime 线已经没有新的自然续推 delta；
- 因而主线若要继续前进，必须先切换到新的 Hermes tranche truth。

## Runtime Topology

当时冻结的产品 runtime topology 是：

`operator / agent -> CLI -> Hermes-backed runtime substrate -> MedAutoGrant domain logic -> durable artifacts / final package / hosted contract bundle`

各层边界固定如下：

### 1. formal entry

- `CLI` 仍是唯一 formal entry。
- 旧五个 canonical CLI surfaces 继续是 verifier / audit baseline：
  - `validate-workspace`
  - `summarize-workspace`
  - `next-step`
  - `critique-summary`
  - `stage-route-report`

### 2. supported protocol layer

- `MCP` 继续保留为 supported protocol layer。
- 当前仍不是 repo-verified public runtime formal entry。

### 3. internal controller surface

- `controller` 继续只属于 internal surface。
- 它不变成 public runtime entry，也不替代 `Hermes substrate`。

### 4. Hermes substrate

`Hermes-backed runtime substrate` 当时被设想负责：

- workspace/final-package 输入加载与 runtime dispatch；
- canonical audit path dispatch：
  - `validate-workspace`
  - `summarize-workspace`
  - `next-step`
  - `critique-summary`
  - `stage-route-report`
- `runtime-run / runtime-resume` 的 runtime handle、journal、stop reason、stage action envelope orchestration；
- `runtime-run / runtime-resume` 默认 journal 根解析到 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`，且显式 `--journal` 继续保持优先；
- revision / artifact / final / hosted contract 的 execution dispatch；
- `build-hosted-contract-bundle` 继续由 Hermes substrate 注入 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract` 所需的 substrate/runtime-state/operator truth；
- 保持 fail-closed runtime path，不允许 hidden fallback 或 silent downgrade。

当前 repo 内，上述 owner surface 由 `src/med_autogrant/domain_runtime.py` 承担；历史 runtime alias / wrapper 线已经退役。
其中 `execute-revision-pass` 的 revised-workspace output identity guard 与输出 handoff、`build-artifact-bundle` 的 output identity guard 与输出 handoff、`build-final-package` 的 artifact-bundle 输入加载与 output handoff、以及 `build-hosted-contract-bundle` 的 final-package 输入加载、`program_id` control-plane 解析、identity guard 与输出 handoff，都已经切到 Hermes substrate owner path。

### 5. MedAutoGrant domain logic

以下语义继续明确留在 Grant domain logic，而不是被 Hermes 重写：

- workspace schema 与 runtime constraint validation；
- stage routing、checkpoint vocabulary、critique/revision/final/export semantics；
- `RevisionPlan` 的 deterministic mutation contract；
- artifact bundle / final package / hosted contract bundle 的 object boundary 与 fail-closed validation；
- `grant_run_id / workspace_id / draft_id / program_id` 的边界。

### 6. host-agent bridge / oracle

旧 `Codex-default host-agent runtime` 在当时路线中只保留为：

- migration baseline；
- compatibility bridge；
- regression oracle。

这段已经被当前 OPL stage-led framework + executor adapter 边界取代；不能据此恢复 compatibility bridge 或把 Hermes-backed runtime 写回当前 owner。

## Promotion Invariants

以下 invariants 在 Hermes tranche 内继续固定：

- `CLI` 仍是 formal entry；
- `MCP` 仍只是 supported protocol layer；
- `controller` 仍只是 internal surface；
- 主线仍按 `Auto-only` 理解；
- `grant_run_id / workspace_id / draft_id / program_id` 不漂移；
- `stage-route-report` 仍是唯一 canonical route / checkpoint aggregation surface；
- `verification_checkpoint / checkpoint_status` 仍保持单一 truth source；
- `critique / revision / final / export / gate` semantics 不漂移；
- `workspace / draft / run / artifact_bundle / final_package / hosted_contract_bundle` 对象边界不漂移；
- 旧 local host-agent runtime 不得再被写成长期产品 runtime。

## Required Verification

当前 tranche 至少要求：

1. `scripts/verify.sh`
2. `scripts/verify.sh cli-smoke`
3. `scripts/verify.sh meta`
4. `uv run pytest -q tests/test_domain_runtime.py`
5. canonical CLI examples 继续可运行
6. `git diff --check`

## Excluded Scope

以下能力继续明确排除在当前 tranche 外：

- actual hosted runtime
- remote execution
- Web UI / multi-tenant / billing
- same-repo `Human-in-the-loop`
- `MCP` public runtime formal entry
- `controller` public runtime formal entry
- 新 authoring semantics
- submission-grade autopilot 宣称

## Honest Stop Conditions

满足任一条件时必须诚实停车：

1. 下一步需要发明新的 authoring semantics；
2. 下一步需要把 `MCP` 或 `controller` 升为 public runtime entry；
3. 下一步已经需要 actual hosted runtime、remote execution 或 `P5` expansion；
4. 继续前进只能靠 hidden fallback、silent downgrade 或 synthetic truth rewrite。
