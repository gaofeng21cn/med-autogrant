# Durability Model Clarification

Date: `2026-04-07`

## 目标

把 repo-tracked review truth、local durable handoff surfaces、以及当前已 landed 的 local runtime durable surfaces 写清楚，避免 review、恢复、runtime identity、artifact output、final package output、hosted-contract output 继续混写。

## 当前指针

- Current phase: `Runtime Productization Program`
- Active tranche: `R5 / Hostedization Prep`
- Latest absorbed runtime slice: `R5.A / Hosted-Friendly Session Boundary`
- Current owner line: `post-R5A local runtime closeout / honest stop`
- Current truthful closeout: `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`

## repo-tracked review surfaces

当前 reviewer 应能仅凭以下 repo-tracked review surfaces 理解 runtime baseline 的正式合同：

- `README.md`
- `README.zh-CN.md`
- `docs/README.md`
- `docs/README.zh-CN.md`
- `docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`
- `docs/specs/2026-04-06-object-model-schema-v1.md`
- `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `docs/specs/2026-04-07-durability-model-clarification.md`
- `docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- `docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- `docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`
- `docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`
- `docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`
- `docs/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`
- `docs/specs/2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md`
- `docs/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`
- `docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md`
- `docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`
- `schemas/v1/nsfc-workspace.schema.json`
- current canonical examples under `examples/**`
- runtime / verification tests under `tests/**`

这些 surfaces 承担的是 review truth 职责：

- formal entry 是什么
- 哪些能力当前正式支持
- 哪些语义是 future scope
- `grant_run_id / workspace_id / draft_id / program_id` 的边界
- `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 的 rollback / gate 语义
- 当前 repo-native hard gate 命令是什么
- revised workspace / checkpoint / operator walkthrough 是否与 landed runtime ladder 一致

## local durable handoff surfaces

当前恢复与连续执行依赖以下 local durable handoff surfaces：

- `contracts/runtime-program/current-program.json`
- 历史 OMX prompt（如果本机仍保留）只能作为本地迁移背景，不再构成当前活跃入口
- `$CODEX_HOME/projects/med-autogrant/runtime-state/reports/med-autogrant-mainline/LATEST_STATUS.md`
- `$CODEX_HOME/projects/med-autogrant/runtime-state/reports/med-autogrant-mainline/ITERATION_LOG.md`
- `$CODEX_HOME/projects/med-autogrant/runtime-state/reports/med-autogrant-mainline/OPEN_ISSUES.md`

这些 surfaces 承担的是 handoff / resume truth 职责：

- 当前 phase / tranche pointer
- 当前 hard gate 与 closeout criteria
- 当前 bounded delta 是否已冻结
- 当前 verification snapshot
- 当前 open risks / blockers
- 恢复执行的读取顺序

用户级 runtime-state 不能单独发明新的 formal entry、hard gate、identity semantics，或把 control-plane maturity 误写成 actual hosted runtime。

## local runtime durable surface

除用户级 runtime-state 的 control-plane durable handoff 之外，当前产品 runtime 已 landed 的 local runtime durable surface 至少包括：

### 1. local run journal

- `run-local --journal ...`
- `resume-local --journal ...`
- local run journal JSON
- 默认 durable root：`$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/<grant_run_id>.json`

这层负责：

- 为同一 `grant_run_id` durable 回写 `latest_stop_reason`
- 为 `stage_action_required` 类 stop reason durable 回写 `latest_stage_action_envelope`
- durable 回写 `latest_route_report`
- 通过 `attempts` 记录 `run-local / resume-local` 的本地 runtime 进入历史

这层不负责：

- 充当 repo-tracked review truth
- 替代 `.runtime-program/reports/**`
- 发明新的 `program_id` 或 controller pointer

### 2. local revised workspace output

- `execute-revision-pass --output ...`
- revised workspace JSON

这层负责：

- 为同一 `grant_run_id / workspace_id / draft_id` durable 写出当前 deterministic revision pass 的 revised workspace candidate
- 保持 `active_revision_plan_id / reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / pre_revision_version_label / post_revision_version_label / comparison_summary`
- 在 re-review 分支上保留“上一棒 reviewed revision evidence”与“当前这一棒 completed revision plan”的版本链

这层不负责：

- 替代 `.runtime-program/reports/**`
- 重写 `verification_checkpoint / checkpoint_status`
- 发明新的 critique synthesis / hosted runtime semantics

### 3. local artifact durable surface

- `build-artifact-bundle --output ...`
- local artifact bundle JSON

这层负责：

- 为同一 `grant_run_id / workspace_id / draft_id` durable 写出当前 active draft lineage 对应的 bundle
- durable 写出 `manifest / lineage / bundle_summary / artifacts`
- 让 selected direction / question / argument chain / fit mapping / outline / draft sections 形成可复用 bundle

这层不负责：

- 改写 workspace
- 替代 `.runtime-program/reports/**`
- 替代 `verification_checkpoint / checkpoint_status`
- 伪装 final export / freeze manifest 已完成

### 4. local final package durable surface

- `build-final-package --output ...`
- local `final_package` JSON

这层负责：

- durable 写出 machine-readable local `final_package`
- 保持 `freeze_manifest / checkpoint_summary / export_summary / deliverables`
- 对齐 `verification_checkpoint / checkpoint_status` 与 `freeze_ready / submission_frozen`

这层不负责：

- 替代 validator / route / revision surfaces
- 写 `.runtime-program/**`
- 伪装 actual hosted runtime 已完成

### 5. local hosted-contract durable surface

- `build-hosted-contract-bundle --output ...`
- local `hosted_contract_bundle` JSON

这层负责：

- durable 导出 hosted-friendly session / state / artifact / audit contract bundle
- 保持 `execution_identity.grant_run_id / workspace_id / draft_id / program_id`
- 保持 `formal_entry_matrix.default_formal_entry=CLI`

这层不负责：

- 实现 actual hosted runtime
- 实现 remote execution / multi-tenant / billing / federation
- 把 `.runtime-program/reports/**` 伪装成 hosted audit store

## 哪些结论必须 repo-native

以下结论如果要成为正式 review truth，必须进入 repo-tracked review surfaces，而不能只留在用户级 runtime-state 或 machine-local outputs：

- formal entry matrix
- durability model clarification
- hard gate 命令集合
- `grant_run_id / workspace_id / draft_id / program_id` 的正式语义边界
- revised workspace validator truth
- `verification_checkpoint / checkpoint_status` 的 canonical aggregation 语义
- 哪些 outputs 已 landed 为 current local runtime ladder
- operator walkthrough / command matrix 对当前已 landed runtime ladder 的公开表述

## 哪些状态允许只留在 local handoff surfaces

以下信息可以继续只由用户级 runtime-state 承担：

- 当前 active program / phase / tranche pointer
- 当前最新 verification snapshot
- 当前 open risks / blockers
- 当前 resume 顺序与执行提示
- 当前一次 closeout 的 leader notes / iteration log

## Identity Boundary Contract

- `grant_run_id`
  - 语义：单次 grant run 的稳定执行句柄
  - 落点：runtime output、CLI output、reports、recovery context 回显、local runtime artifacts
- `workspace_id`
  - 语义：`NSFCWorkspace` 聚合根身份
  - 落点：workspace object identity
- `draft_id`
  - 语义：`ApplicationDraft` 身份
  - 落点：draft / critique / revision / artifact / final package 链接身份
  - 约束：revision 完成后仍沿用同一 `draft_id`
- `program_id`
  - 语义：control-plane / report-routing 身份
  - 落点：`$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/` 与 `contracts/runtime-program/current-program.json`；hosted-contract export 中只作为 routing identity 保留

这四类 ID 不得互相替代。

## Verification Boundary Contract

- 当前 tranche hard gate：只看 repo-native commands 与 repo-native tests
- external verifier
  - 当前仅为 `advisory external check`
  - 失败必须在 reports 中被记录
  - 但在没有显式改写 active truth surfaces 前，不得重新写成 current hard gate

## 当前 freeze 结论

- formal entry 真相已进入 repo-durable current truth
- durability model 真相已进入 repo-durable current truth
- `grant_run_id / workspace_id / draft_id / program_id` 边界已在 docs / examples / CLI / tests / local outputs 中持续收紧
- `run-local / resume-local / build-artifact-bundle / execute-revision-pass / build-final-package / build-hosted-contract-bundle` 已构成当前 landed local runtime ladder
- post-`R5.A` local runtime hardening 已在当前 truth 下收口为 `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`；任何 further productization 都必须先冻结新的 repo-tracked tranche truth，而不是默认继续当前 ladder
