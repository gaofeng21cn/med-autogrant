# Formal Entry Matrix Current Truth

Date: `2026-04-07`

## 目标

在当前 active mainline 下，把正式入口矩阵持续冻结成 repo-durable current truth，避免把 future scope、控制面入口和恢复入口混写成同一种“入口”。

## 当前指针

- Current phase: `Runtime Productization Program`
- Active tranche: `R2 / Artifact Production Surface`
- Active slice: `R2.A / Artifact Bundle Production Surface`

本文件继续冻结当前 formal entry 真相；它不扩 `MCP / controller / write / export / HITL`，也不把 `R1.A` 的本地主循环 entry 混写成新的 formal-entry family。

## Formal Entry Matrix

### 1. `default_formal_entry`

- 当前冻结值：`CLI`
- 当前入口：
  - `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant next-step --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant critique-summary --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant run-local --input ... [--journal ...]`
  - `PYTHONPATH=src python3 -m med_autogrant resume-local --journal ...`
  - `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input ... --output ...`
- 当前 contract：
  - `CLI` 是当前唯一 repo-verified 的 user-facing runtime formal entry。
  - CLI 输出必须稳定回显同一 `grant_run_id`，并保持与 `workspace_id`、`draft_id`、`program_id` 分离。
  - `grant_run_id` 是 execution handle，不是新的入口面。
  - `stage-route-report` 当前必须输出 `verification_checkpoint / checkpoint_status`，把 verification、route recommendation、rollback / frozen gate、gate-open ready-for-freeze 状态与 reviewed revision evidence 聚合进同一个 machine-readable checkpoint surface。
  - `run-local` 当前是本地主循环 entry；它只允许在既有 route / checkpoint surface 之上增加 machine-readable `stop_reason`、`stage_action_envelope` 与 local run journal。
  - `resume-local` 当前是本地 runtime recovery entry；它只允许从同一 journal 恢复 `input_path`、沿用同一 `grant_run_id` 重新进入一次 local runtime pass，并在 `stage_action_required` 时继续 durable 回写 `stage_action_envelope`。
  - `build-artifact-bundle` 当前是本地 artifact bundle entry；它只允许把当前 active workspace 的 canonical objects 写成 machine-readable local bundle，并补 manifest / lineage / version / bundle summary，不得写回 workspace、不得写 `.omx/**`、不得偷跑 critique / revision / export。
  - 在当前 `R2.A` slice 内，CLI 的 repo-native runtime / audit surface 还必须同时保持：
    - absorbed `P3.B` retained boundary：`active_revision_plan_id`、`reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id`
    - absorbed `P3.C` retained boundary：`forced_rollback_stage`、`forced_rollback_reason`、`presubmission_frozen`
    - absorbed `P4.A` gate-open boundary：`ready_for_submission + presubmission_frozen=false`
    - absorbed `P4.B` checkpoint durable boundary：`VerificationCheckpoint` 只能作为 `stage-route-report.verification_checkpoint` 的 derived checkpoint object 存在，不能被解释成新的 formal entry、runtime identity 或 controller capability
    - 当前 `R1.B` local runtime boundary：`stage_action_envelope` 只能结构化 `stage_action_required` 的 route continuation，不得替代旧五个 canonical CLI surfaces，也不得把 local run journal 写成 `.omx` control-plane report
    - 当前 `R2.A` local artifact boundary：`build-artifact-bundle` 只能打包当前 `selected_direction / selected_question / ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline / ApplicationDraft.sections`，不得改写 `frozen_question_id`、不得生成新内容、不得把 local bundle output 写成 `.omx` control-plane report

### 2. `supported_protocol_layer`

- 当前冻结值：`MCP`
- 当前状态：`reserved future layer / not-yet-supported`
- 当前 contract：
  - `MCP` 在统一 formal-entry matrix 中保留为 supported protocol layer。
  - 当前仓库尚未把 `MCP` 冻结成 repo-verified public runtime formal entry。
  - 在没有 repo-tracked current truth 改写前，不得把 `MCP` 口头提升成“当前已经正式支持”。

### 3. `internal_controller_surface`

- 当前冻结值：`controller`
- 当前入口：
  - `OMX_TEAM_PROMPT.md`
  - `CURRENT_PROGRAM.md`
  - `PROGRAM_ROUTING.md`
  - active `PRD / test-spec / implementation`
  - active `LATEST_STATUS / ITERATION_LOG / OPEN_ISSUES`
- 当前 contract：
  - `controller` 在当前 formal-entry matrix 中属于 internal control surface，不是产品 runtime formal entry。
  - 它负责 planning、phase/tranche pointer、verification contract、report sync 与 long-run orchestration。
  - 它不能被叙述成“已经有正式 MCP / controller runtime”。
  - 当前 control-plane truth 还必须显式同时冻结：
    - `active_revision_plan_id`、`reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id` 的 P3.B re-review contract
    - `forced_rollback_stage`、`forced_rollback_reason` 与 `presubmission_frozen` 的 P3.C hard gate contract
    - `examples/nsfc_workspace_p3a_ready_for_submission.json` 的 P4.A gate-open contract
    - `VerificationCheckpoint` 的 P4.B checkpoint durable contract

### 4. recovery / resume entry

- 正式支持：是
- 当前入口：
  - `PYTHONPATH=src python3 -m med_autogrant resume-local --journal ...`
  - 对产品 runtime 来说，恢复依赖同一份 local run journal
  - 先读 `CURRENT_PROGRAM.md`
  - 再读 `PROGRAM_ROUTING.md`
  - 再读 active `PRD / test-spec / implementation`
  - 最后读 active `LATEST_STATUS / ITERATION_LOG / OPEN_ISSUES`
- 当前 contract：
  - `resume-local` 是当前产品 runtime 的本地恢复入口；它从 journal 恢复 `input_path`、沿用同一 `grant_run_id`，并 append 新 `attempt`。
  - 当当前 stop reason 为 `stage_action_required` 时，恢复入口还必须能继续 durable 回写 machine-readable `stage_action_envelope`。
  - developer control-plane 的恢复入口继续使用同一组 `.omx` durable surfaces。
  - 恢复时必须沿用同一 `grant_run_id` 上下文回显，但不能把 `grant_run_id` 误写成 `program_id` 或 `workspace_id`。
  - 恢复时也不得丢失 absorbed `P3.B` 的 `active_revision_plan_id`、`reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id`，absorbed `P3.C` 的 `forced_rollback_stage`、`forced_rollback_reason`、`presubmission_frozen`，absorbed `P4.A` 的 gate-open ready-for-freeze 语义，以及 absorbed `P4.B` 的 `VerificationCheckpoint` durable boundary。

### 5. not-yet-supported / future public entry scope

- `MCP public runtime entry`
  - 当前状态：`not-yet-supported`
  - 说明：当前仓没有把 `MCP` 冻结成 repo-verified public runtime formal entry。
- `controller public runtime entry`
  - 当前状态：`not-yet-supported`
  - 说明：当前仓没有把 `controller` 冻结成 public runtime formal entry；它当前只属于 internal controller surface。

这些面仍属 future scope。任何后续若要把它们升级为正式入口，必须先改写 active truth surfaces，而不是口头默认。

## 当前 hard gate 与 external verifier 裁决

当前 active tranche 的 hard gate 只包含 repo-native 验证命令：

1. `python3 -m unittest discover -s tests -p 'test_*.py'`
2. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
3. `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
4. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_revision.json --format json`
5. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
6. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
7. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
8. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
9. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
10. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
11. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
12. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p2c_revision.json --format json`
13. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
14. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
15. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
16. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
17. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_revision.json --format json`
18. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
19. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
20. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
21. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
22. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_revision.json --format json`
23. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
24. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
25. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
26. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
27. `git diff --check`
28. `PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p2c_revision.json --journal "$TMPDIR/r1a-revision.json" --format json`
29. `PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3b_re_review_major_revision.json --journal "$TMPDIR/r1b-major-revision.json" --format json`
30. `PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --journal "$TMPDIR/r1a-rollback.json" --format json`
31. `PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3a_ready_for_submission.json --journal "$TMPDIR/r1a-freeze-ready.json" --format json`
32. `PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3c_presubmission_frozen.json --journal "$TMPDIR/r1a-frozen.json" --format json`
33. `PYTHONPATH=src python3 -m med_autogrant resume-local --journal "$TMPDIR/r1a-revision.json" --format json`
34. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p2b_outline.json --output "$TMPDIR/r2a-outline-bundle.json" --format json`
35. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p2c_revision.json --output "$TMPDIR/r2a-revision-bundle.json" --format json`

external verifier durable 裁决如下：

- `python3 /Users/gaofeng/workspace/omx-project-installer/skills/omx-project-installer/scripts/omx_project_installer.py diff --target /Users/gaofeng/workspace/med-autogrant`
  - 当前状态：`external advisory verifier`
  - 不是当前 tranche hard gate
  - 原因：
    - 它审计的是 installer baseline / scaffold drift，不是当前 runtime baseline 的功能正确性
    - 它依赖仓库外脚本，不属于 repo-native current truth
    - 若未来要重新纳入 hard gate，必须先同步改写 `CURRENT_PROGRAM / PROGRAM_ROUTING / active plans / reports`

## 禁止越界解释

- 不得把 `supported_protocol_layer` 解释成“当前 public runtime 已正式支持 `MCP`”。
- 不得把“developer control-plane entry 存在”解释成“产品 controller 已正式支持”。
- 不得把 `grant_run_id` 解释成新的 control-plane pointer。
- 不得因为 formal entry matrix 已冻结，就默认宣称 `P4.B` implementation 已完成、`MCP / controller` 已支持或 HITL 已实现。
