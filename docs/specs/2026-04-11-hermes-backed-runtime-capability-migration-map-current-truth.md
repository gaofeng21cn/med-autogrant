# Hermes-Backed Runtime Capability Migration Map Current Truth

Date: `2026-04-11`

## Goal

把当前 runtime 主线中哪些能力归 `Hermes-Agent`、哪些继续保留在 `Med Auto Grant` domain supervision、以及哪些由 route-selected executor 承担，冻结成可执行 current truth。

当前 repo-tracked current-program pointer 固定为 `contracts/runtime-program/current-program.json`；机器本地 runtime state 固定下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

## Capability Split

### A. Hermes-Agent runtime owner

下面这些能力当前由 `Hermes-Agent` 持有：

- `validate-workspace` dispatch
- `summarize-workspace` dispatch
- `next-step` dispatch
- `critique-summary` dispatch
- `stage-route-report` dispatch
- `runtime-run` runtime orchestration
- `runtime-resume` runtime orchestration
- revision / artifact / final / hosted export execution dispatch
- runtime input loading、output-path handoff、fail-closed orchestration

### B. Med Auto Grant domain supervision owner

下面这些能力继续保留在 `Med Auto Grant` domain supervision：

- `validate_workspace_document`
- `summarize_workspace_document`
- `determine_next_step`
- `build_critique_summary`
- `build_stage_route_report`
- `build_revision_execution_document`
- `build_artifact_bundle_document`
- `build_final_package_document`
- `build_hosted_contract_bundle_document`

### C. Route-selected concrete executor

下面这些能力继续由 route-selected concrete executor 承担：

- 单步 authoring pass 的具体执行
- 默认 `Codex CLI autonomous executor`
- 显式 opt-in 的 `Hermes-native` proof lane

换句话说：

- `Hermes-Agent` 负责 runtime path owner；
- `Med Auto Grant` 继续拥有 author-side semantics 与 supervision truth；
- concrete executor 只负责把被放行的 authoring route 跑出来。
- `build_revision_execution_payload / build_artifact_bundle_payload / build_final_package_payload / build_hosted_contract_bundle_payload` 仅保留为 compatibility bridge / regression oracle wrapper，不再拥有产品 runtime path。

### D. migration baseline / bridge / oracle

下面这些内容只保留为 migration baseline、compatibility bridge、regression oracle：

- post-`R5.A` honest-stop closeout truth
- 旧 `CLI-first + host-agent runtime` 叙事
- 旧 local operator walkthrough 中的 host-agent framing
- 历史 runtime alias / wrapper 线作为 bridge 追溯材料

## Command Mapping

### audit path

- `validate-workspace`
  - Hermes substrate：加载 workspace、触发 runtime dispatch
  - Grant domain logic：workspace schema/runtime validation
- `summarize-workspace`
  - Hermes substrate：runtime dispatch
  - Grant domain logic：state snapshot assembly
- `next-step`
  - Hermes substrate：runtime dispatch
  - Grant domain logic：route recommendation / rollback / frozen semantics
- `critique-summary`
  - Hermes substrate：runtime dispatch
  - Grant domain logic：critique/revision evidence summary
- `stage-route-report`
  - Hermes substrate：canonical audit/checkpoint dispatch
  - Grant domain logic：verification_checkpoint / checkpoint_status assembly

### runtime entry

- `runtime-run`
  - Hermes substrate：run handle、journal、stop reason、stage action envelope、resume pointer
  - Hermes substrate：默认 journal durable root 解析到 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`
  - Grant domain logic：route report / checkpoint source
- `runtime-resume`
  - Hermes substrate：journal re-entry 与同一 `grant_run_id` continuation
  - Hermes substrate：显式 `--journal` 缺省时沿用 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`
  - Grant domain logic：route report / checkpoint source

### revision / export chain

- `execute-revision-pass`
  - Hermes substrate：revised-workspace output identity guard 与 output handoff
  - Grant domain logic：deterministic section mutation、comparison_summary、re-review evidence preservation
- `build-artifact-bundle`
  - Hermes substrate：bundle output identity guard、durable artifact handoff
  - Grant domain logic：artifact bundle document assembly、shape、manifest、lineage
- `build-final-package`
  - Hermes substrate：artifact-bundle 输入加载、final package output identity guard、output handoff
  - Grant domain logic：checkpoint-consistent final package document assembly
- `build-hosted-contract-bundle`
  - Hermes substrate：final-package 输入加载、repo-tracked `program_id` contract 解析、identity guard、output handoff
  - Hermes substrate：为 hosted handoff 注入 `runtime_substrate_contract`、`runtime_state_contract`、`operator_contract`
  - Grant domain logic：hosted-friendly contract export 组装、`program_id` routing identity preservation

## Minimal Hermes-Backed Runnable Paths

### 1. critique -> revision -> re-entry path

以下路径当前必须可以在 Hermes runtime 上运行：

1. `validate-workspace`
2. `summarize-workspace`
3. `next-step`
4. `critique-summary`
5. `stage-route-report`
6. `execute-revision-pass`
7. revised workspace fresh `validate-workspace`
8. revised workspace fresh `stage-route-report`
9. revised workspace `runtime-run`
10. revised workspace `build-artifact-bundle`

### 2. frozen -> final -> hosted export path

以下路径当前必须可以在 Hermes runtime 上运行：

1. `validate-workspace`
2. `summarize-workspace`
3. `next-step`
4. `critique-summary`
5. `stage-route-report`
6. `build-artifact-bundle`
7. `build-final-package`
8. `build-hosted-contract-bundle`

## Non-Drift Rules

Hermes migration map 当前明确禁止：

- hidden fallback
- silent downgrade
- synthetic truth rewrite
- 把 `program_id` 改写成 runtime session id
- 把 `MCP` / `controller` 提升成 public runtime formal entry
- 把 `workspace / draft / run / artifact_bundle / final_package / hosted_contract_bundle` 压扁成单对象

## Required Verification

至少覆盖：

1. `uv run pytest -q tests/test_hermes_runtime.py`
2. `uv run pytest -q tests/test_hermes_runtime_truth.py`
3. `scripts/verify.sh`
4. `scripts/verify.sh cli-smoke`
5. `git diff --check`
