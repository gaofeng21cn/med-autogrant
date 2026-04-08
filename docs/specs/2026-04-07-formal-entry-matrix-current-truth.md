# Formal Entry Matrix Current Truth

Date: `2026-04-07`

## 目标

在当前 active mainline 下，把正式入口矩阵持续冻结成 repo-durable current truth，避免把 future scope、控制面入口和恢复入口混写成同一种“入口”。

## 当前指针

- Current phase: `P3 / Mentor Critique And Revision Loop Hardening`
- Active tranche: `P3.C / Forced Rollback And Presubmission Gate`

本文件继续冻结当前 formal entry 真相；它不扩 `MCP / controller / write / export / HITL`，也不替代当前 `P3.C` 的 forced rollback / presubmission gate contract。

## Formal Entry Matrix

### 1. user-facing runtime entry

- 正式支持：`CLI`
- 当前入口：
  - `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant next-step --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant critique-summary --input ...`
  - `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input ...`
- 当前 contract：
  - CLI 是当前唯一正式支持的 user-facing runtime entry。
  - CLI 输出必须稳定回显同一 `grant_run_id`，并保持与 `workspace_id`、`draft_id`、`program_id` 分离。
  - `grant_run_id` 是 execution handle，不是新的入口面。
  - 在当前 `P3.C` tranche 内，CLI 的 repo-native audit surface 还必须同时保持：
    - absorbed `P3.B` retained boundary：`active_revision_plan_id`、`reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id`
    - 当前 `P3.C` hard gate boundary：`forced_rollback_stage`、`forced_rollback_reason`、`presubmission_frozen`

### 2. developer control-plane entry

- 正式支持：是
- 当前入口：
  - `OMX_TEAM_PROMPT.md`
  - `CURRENT_PROGRAM.md`
  - `PROGRAM_ROUTING.md`
  - active `PRD / test-spec / implementation`
  - active `LATEST_STATUS / ITERATION_LOG / OPEN_ISSUES`
- 当前 contract：
  - 这是开发控制面入口，不是产品 runtime 入口。
  - 它负责 planning、phase/tranche pointer、verification contract、report sync 与 long-run orchestration。
  - 它不能被叙述成“已经有正式 MCP / controller runtime”。
  - 当前 control-plane truth 还必须显式同时冻结：
    - `active_revision_plan_id`、`reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id` 的 P3.B re-review contract
    - `forced_rollback_stage`、`forced_rollback_reason` 与 `presubmission_frozen` 的 P3.C hard gate contract

### 3. recovery / resume entry

- 正式支持：是
- 当前入口：
  - 先读 `CURRENT_PROGRAM.md`
  - 再读 `PROGRAM_ROUTING.md`
  - 再读 active `PRD / test-spec / implementation`
  - 最后读 active `LATEST_STATUS / ITERATION_LOG / OPEN_ISSUES`
- 当前 contract：
  - recovery / resume 入口与 developer control-plane 使用同一组 durable surfaces。
  - 恢复时必须沿用同一 `grant_run_id` 上下文回显，但不能把 `grant_run_id` 误写成 `program_id` 或 `workspace_id`。
  - 恢复时也不得丢失 absorbed `P3.B` 的 `active_revision_plan_id`、`reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id`，以及当前 `P3.C` 的 `forced_rollback_stage`、`forced_rollback_reason` 与 `presubmission_frozen` 的 machine-readable 边界。

### 4. not-yet-supported / future scope

- `MCP`
  - 当前状态：`not-yet-supported`
  - 说明：当前仓没有把 MCP 冻结成正式 runtime 或 formal entry。
- `controller`
  - 当前状态：`not-yet-supported`
  - 说明：当前仓没有把 controller 冻结成正式 runtime 或 formal entry。

这些面仍属 future scope。任何后续若要把它们升级为正式入口，必须先改写 active truth surfaces，而不是口头默认。

## 当前 hard gate 与 external verifier 裁决

当前 active tranche 的 hard gate 只包含 repo-native 验证命令：

1. `python3 -m unittest discover -s tests -p 'test_*.py'`
2. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_revision.json --format json`
3. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
4. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
5. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
6. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_revision.json --format json`
7. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
8. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
9. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
10. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p2c_revision.json --format json`
11. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
12. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
13. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
14. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_revision.json --format json`
15. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
16. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
17. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
18. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_revision.json --format json`
19. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
20. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
21. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
22. `git diff --check`

external verifier durable 裁决如下：

- `python3 /Users/gaofeng/workspace/omx-project-installer/skills/omx-project-installer/scripts/omx_project_installer.py diff --target /Users/gaofeng/workspace/med-autogrant`
  - 当前状态：`external advisory verifier`
  - 不是当前 tranche hard gate
  - 原因：
    - 它审计的是 installer baseline / scaffold drift，不是当前 runtime baseline 的功能正确性
    - 它依赖仓库外脚本，不属于 repo-native current truth
    - 若未来要重新纳入 hard gate，必须先同步改写 `CURRENT_PROGRAM / PROGRAM_ROUTING / active plans / reports`

## 禁止越界解释

- 不得把“developer control-plane entry 存在”解释成“产品 controller 已正式支持”。
- 不得把 `grant_run_id` 解释成新的 control-plane pointer。
- 不得因为 formal entry matrix 已冻结，就默认宣称 `P3.B / P3.C` 已完成。
