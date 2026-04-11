# Hermes-Backed Runtime Capability Migration Map Current Truth

Date: `2026-04-11`

## Goal

把当前 runtime 主线中哪些能力迁入 `Hermes substrate`、哪些继续保留在 `Grant domain logic`、以及 revision / final package / hosted contract bundle 如何挂到新 runtime 上，冻结成可执行 current truth。

## Capability Split

### A. Hermes substrate owner

下面这些能力当前迁入 `Hermes substrate`：

- `validate-workspace` dispatch
- `summarize-workspace` dispatch
- `next-step` dispatch
- `critique-summary` dispatch
- `stage-route-report` dispatch
- `run-local` runtime orchestration
- `resume-local` runtime orchestration
- revision / artifact / final / hosted export execution dispatch
- runtime input loading、output-path handoff、fail-closed orchestration

### B. Grant domain logic

下面这些能力继续保留在 `Grant domain logic`：

- `validate_workspace_document`
- `summarize_workspace_document`
- `determine_next_step`
- `build_critique_summary`
- `build_stage_route_report`
- `build_revision_execution_payload`
- `build_artifact_bundle_payload`
- `build_final_package_payload`
- `build_hosted_contract_bundle_payload`

换句话说：

- Hermes 负责 runtime path owner；
- MedAutoGrant 继续拥有 author-side semantics。

### C. migration baseline / bridge / oracle

下面这些内容只保留为 migration baseline、compatibility bridge、regression oracle：

- post-`R5.A` honest-stop closeout truth
- 旧 `CLI-first + host-agent runtime` 叙事
- 旧 local operator walkthrough 中的 host-agent framing
- `src/med_autogrant/local_runtime.py` 作为 legacy module wrapper 的桥接入口

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

- `run-local`
  - Hermes substrate：run handle、journal、stop reason、stage action envelope、resume pointer
  - Grant domain logic：route report / checkpoint source
- `resume-local`
  - Hermes substrate：journal re-entry 与同一 `grant_run_id` continuation
  - Grant domain logic：route report / checkpoint source

### revision / export chain

- `execute-revision-pass`
  - Hermes substrate：execution dispatch 与 output handoff
  - Grant domain logic：deterministic section mutation、comparison_summary、re-review evidence preservation
- `build-artifact-bundle`
  - Hermes substrate：execution dispatch 与 durable artifact handoff
  - Grant domain logic：artifact bundle shape、manifest、lineage、identity guard
- `build-final-package`
  - Hermes substrate：execution dispatch
  - Grant domain logic：checkpoint-consistent final package assembly
- `build-hosted-contract-bundle`
  - Hermes substrate：final-package 输入加载、`program_id` control-plane 解析、identity guard、output handoff
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
9. revised workspace `run-local`
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
