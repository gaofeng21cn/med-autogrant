# Runtime-First R1 To R5 Boundary Map

Date: `2026-04-08`

## Purpose

这份文档把 `Med Auto Grant` 当前 `runtime-first productization` program 的未来边界一次性预冻结到 `R5`。

它的作用不是把所有 tranche 误写成已实现，而是明确：

- 从当前 latest absorbed runtime slice 往后，哪些 future tranche 可以被 `OMX` 继续打开
- 每一棒分别属于哪一层能力面
- 什么时候可以实现
- 什么时候必须重分类到更后面的阶段
- 什么时候必须诚实停车

## Current Anchor

当前 latest absorbed slice 为：

- `R2.A / Artifact Bundle Production Surface`
- upstream absorbed anchor：
  - `R1.A / Local Main Loop Entry And Stop Reason`
  - freeze absorb：`38b5347`
  - implementation absorb：`8e087dc`
- `R1.B` activation freeze absorb：`2b193da`
- `R1.B` implementation absorb：`2953026`
- `R2.A` activation freeze absorb：`424ded0`
- `R2.A` implementation：absorbed in current mainline truth

当前已 landed 的 surface：

- `run-local`
- `resume-local`
- machine-readable `stop_reason`
- durable JSON run journal
- machine-readable `stage_action_envelope`
- `latest_stage_action_envelope`
- `build-artifact-bundle`
- machine-readable `artifact_bundle`

## One-Shot Autonomous Continuation Contract

这份边界图冻结后，`OMX` 被授权：

1. 从当前 latest absorbed slice 出发，持续做 honest delta audit
2. 把新识别到的 delta 与下面仍未 absorbed 的 `R3.A / R4.A / R5.A` 边界进行匹配
3. 如果匹配成功：
   - 先把对应 tranche freeze 到 active `CURRENT_PROGRAM + PRD + test-spec + implementation + reports`
   - 必要时补 repo-tracked internal spec
   - 再实现、验证、absorb，并继续下一棒
4. 如果新 delta 实际属于更后面的 stage：
   - 不强行停留在当前 stage 编造中间 tranche
   - 允许直接重分类到更后面的 pre-frozen activation package
5. 只有在没有 honest delta，或 delta 无法在当前 frozen truth 内归类时，才允许停车

这意味着：

- `OMX` 不需要每到一个小阶段就回头要新提示词
- 但也不被允许跨边界瞎写实现

## Global Invariants

所有 future tranche 都必须同时满足：

- formal entry 仍只有 `CLI`
- `MCP` 仍只是 future protocol layer
- `controller` 仍只是 internal surface
- `grant_run_id / workspace_id / draft_id / program_id` 边界不漂移
- `RevisionPlan.execution_status / pre_revision_version_label / post_revision_version_label / comparison_summary / frozen_question_id` 不漂移
- `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 不漂移
- `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 不漂移
- `verification_checkpoint / checkpoint_status` 不漂移
- 旧五个 canonical CLI surfaces 继续是 verifier / audit baseline
- 不得提前进入 `P5.A / P5.B`
- 不得提前实现 same-repo `Human-in-the-loop`
- 不得提前实现 web / hosted runtime

## Boundary Map

### R1.B / Stage Action Executor Envelope

## Activation Status

- absorbed
- current status：已实现并 absorbed；它把 `stage_action_required` 收紧成 machine-readable `stage_action_envelope`，但没有越界到 artifact writing / revision execution / export / hostedization

## Scope

- 把 `run-local` 已得到的 `stage_action_required` 类 stop reason 收紧成 machine-readable `stage_action_envelope`
- 让 runtime 能对“下一动作是什么”形成稳定、结构化、可恢复的执行 envelope
- 只处理 runtime 编排、route continuation、journal append、resume decision

## Required Inputs

- `stage-route-report`
- `next-step`
- 当前 workspace 的 `current_selection`
- 当前 run journal

## Required Verification

- 新的 action envelope contract regression tests
- canonical `run-local / resume-local` examples 保持全绿
- `stage_action_required` 对应的 envelope 字段与 stop reason 对齐
- `git diff --check`

## Promotion Invariants

- 不生成新的方向、问题、论证链、提纲、草稿内容
- 不执行 critique / revision 内容改写
- 不改变 `ApplicationDraft` 内容层对象
- 只允许围绕 runtime orchestration 和 machine-readable action envelope 扩展

## Honest Reclassification Rules

如果下一新增能力需要：

- 生成或更新方向 / 问题 / 论证链 / 适配度 / 提纲 / 草稿
  - 这不是 `R1.B`
  - 必须重分类到 `R2.A / Artifact Bundle Production Surface`
- 执行 critique / revision / re-review 内容变更
  - 这不是 `R1.B`
  - 必须重分类到 `R3.A / Critique Revision Executor Surface`
- 形成 final package / freeze manifest / export package
  - 这不是 `R1.B`
  - 必须重分类到 `R4.A / Final Freeze And Export Package`

## Excluded Scope

- artifact writing
- revision execution
- final export
- hostedization

### R2.A / Artifact Bundle Production Surface

## Activation Status

- absorbed
- current status：已实现并 absorbed；它把当前 active workspace 的 canonical objects 写成 machine-readable local `artifact_bundle`，但没有越界到 critique / revision executor、final export 或 hostedization

## Scope

- 把方向、问题、论证链、适配度、提纲、草稿收成稳定 artifact bundle
- 增加 artifact manifest、lineage、version、bundle summary
- 让本地 runtime 不再只会给下一步建议，而是能稳定写出可复用申请材料

## Required Inputs

- `current_selection`
- `selected_direction_id`
- `selected_question_id`
- `active_fit_mapping_id`
- `active_draft_id`
- `ArgumentChain`
- `ApplicantFitMapping`
- `ApplicationDraft.outline`

## Required Verification

- artifact bundle schema / manifest tests
- direction -> question -> argument -> fit -> outline -> draft lineage consistency tests
- canonical artifact-producing examples（`build-artifact-bundle`）
- `test_*.py`
- `git diff --check`

## Promotion Invariants

- 不得改写 `frozen_question_id`
- 不得在 artifact 生产阶段偷偷执行 critique / revision
- 不得跳过 manifest / lineage / version
- 生成的 artifact bundle 必须能映射回同一 `grant_run_id` 与同一 draft lineage

## Honest Reclassification Rules

如果下一新增能力已经需要：

- critique intake
- revision plan execution
- re-review evidence 更新
- forced rollback 执行

则这不是纯 `R2.A`，必须重分类到 `R3.A / Critique Revision Executor Surface`。

## Excluded Scope

- critique revision executor
- final package / export
- hostedization

### R3.A / Critique Revision Executor Surface

## Activation Status

- pre-frozen
- current status：尚未实现；当下一 honest delta 已经进入 critique / revision autoloop 时允许激活

## Scope

- 执行 `critique -> revision -> re-review -> rollback / freeze`
- 让 revision loop 从“被动描述”变成 runtime 真行为
- 保持 `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 的连续证据链

## Required Inputs

- `MentorCritique`
- `RevisionPlan`
- `ApplicationDraft`
- `reviewed_revision_evidence`
- `forced_rollback_stage`
- `forced_rollback_reason`

## Required Verification

- major revision / rollback / freeze-ready canonical examples
- critique -> revision -> re-review loop tests
- rollback and presubmission gate regression
- `test_*.py`
- `git diff --check`

## Promotion Invariants

- critique、revision、re-review 必须有 evidence trace
- `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 不得弱化成自由文本
- revised draft 必须继续沿用正确的 draft lineage
- 不得在这一层伪装 final package 已生成

## Honest Reclassification Rules

如果下一新增能力已经要求：

- 形成 submission-facing final package
- freeze manifest
- export summary

则这不是 `R3.A`，必须重分类到 `R4.A / Final Freeze And Export Package`。

## Excluded Scope

- final package export
- hostedization
- federation / second family

### R4.A / Final Freeze And Export Package

## Activation Status

- pre-frozen
- current status：尚未实现；当本地 runtime 已能稳定跑过 artifact + critique revision loop 时允许激活

## Scope

- 形成 submission-facing 的本地 final package
- 冻结 final version identity、freeze manifest、checkpoint summary、export summary
- 输出结构化 local delivery package，而不是一段说明文字

## Required Inputs

- 完整 artifact bundle
- critique / revision loop 终态
- `verification_checkpoint`
- `checkpoint_status`
- freeze-ready / presubmission-frozen gate evidence

## Required Verification

- final package completeness tests
- freeze manifest consistency tests
- export package structure tests
- canonical freeze-ready / presubmission-frozen examples
- `test_*.py`
- `git diff --check`

## Promotion Invariants

- final package 必须与 `verification_checkpoint` 对齐
- export 只能发生在本地 submission-facing surface
- 不得把本地 export 误写成 hosted runtime 已完成

## Honest Reclassification Rules

如果下一新增能力已经不再是本地 export，而是：

- 会话托管
- state store 抽象
- artifact / audit 的 hosted-friendly contract

则这不是 `R4.A`，必须重分类到 `R5.A / Hosted-Friendly Session Boundary`。

## Excluded Scope

- web runtime
- hosted platform
- credits / billing
- second-family / federation

### R5.A / Hosted-Friendly Session Boundary

## Activation Status

- pre-frozen
- current status：尚未实现；仅在 `R1 -> R4` absorbed 后允许激活

## Scope

- 抽离 host/runtime boundary
- 定义 hosted-friendly 的 session / state / artifact / audit contract
- 让当前本地 runtime 的关键对象能迁移到未来托管环境

## Required Inputs

- 已吸收的本地 runtime surface
- final package / export surface
- run journal / reports / artifact bundle / checkpoint surfaces

## Required Verification

- hosted-friendly contract tests
- state / artifact / audit boundary schema tests
- local runtime 与 hosted-friendly contract 对齐测试
- `test_*.py`
- `git diff --check`

## Promotion Invariants

- 只做 contract prep，不做 web runtime 实装
- 不改写 domain contract
- 不改写 formal entry matrix
- 不进入 `P5.A / P5.B`

## Excluded Scope

- actual hosted runtime
- web UI
- multi-tenant platform
- credits / billing
- federation expansion

## Honest Stop Conditions

以下情况必须诚实停车：

- 当前没有新的 concrete delta 可以匹配到任何 pre-frozen package
- 下一步需要新 formal entry、仓外 readiness、外部凭据或平台语义
- 下一步需要改写 `P5.A / P5.B`
- 下一步只能靠启发式、临时补丁或模糊故事推进
