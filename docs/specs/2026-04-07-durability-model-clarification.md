# Durability Model Clarification

Date: `2026-04-07`

## 目标

在当前 active mainline 下，把 repo-durable review truth、local durable handoff truth 与对象身份边界写清楚，避免 review、恢复和 runtime identity 三类语义继续混写。

## 当前指针

- Current phase: `P2 / NSFC Authoring Mainline Freeze`
- Active tranche: `P2.B / Argument-Fit-Outline Mainline`

## repo-tracked review surfaces

当前 reviewer 应能仅凭以下 repo-tracked surfaces 理解 runtime baseline 的正式合同：

- `README.md`
- `README.zh-CN.md`
- `docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`
- `docs/specs/2026-04-06-object-model-schema-v1.md`
- `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `docs/specs/2026-04-07-durability-model-clarification.md`
- `docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
- `schemas/v1/nsfc-workspace.schema.json`
- `schemas/v1/argument-chain.schema.json`
- `schemas/v1/applicant-fit-mapping.schema.json`
- `schemas/v1/application-draft.schema.json`
- `examples/nsfc_workspace_minimal.json`
- `examples/nsfc_workspace_p2b_argument_building.json`
- `examples/nsfc_workspace_p2b_fit_alignment.json`
- `examples/nsfc_workspace_p2b_outline.json`
- `tests/test_cli_validate_workspace.py`
- `tests/test_stage_router.py`
- `tests/test_workspace_summary.py`
- `tests/test_program_control_surfaces.py`

这些 surface 承担的是 review truth 职责：

- formal entry 是什么
- 哪些能力当前正式支持
- 哪些语义是 future scope
- `grant_run_id / workspace_id / draft_id / program_id` 的边界
- 当前 repo-native hard gate 命令是什么
- `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 的 object linking 如何冻结

## local durable handoff surfaces

当前恢复与连续执行依赖以下 local durable handoff surfaces：

- `.omx/context/CURRENT_PROGRAM.md`
- `.omx/context/PROGRAM_ROUTING.md`
- `.omx/context/OMX_TEAM_PROMPT.md`
- `.omx/context/OMX_EXECUTION_PROMPT.md`
- `.omx/plans/spec-program-operating-model.md`
- `.omx/plans/prd-med-autogrant-mainline.md`
- `.omx/plans/test-spec-med-autogrant-mainline.md`
- `.omx/plans/implementation-med-autogrant-mainline.md`
- `.omx/reports/med-autogrant-mainline/LATEST_STATUS.md`
- `.omx/reports/med-autogrant-mainline/ITERATION_LOG.md`
- `.omx/reports/med-autogrant-mainline/OPEN_ISSUES.md`

这些 surface 承担的是 handoff / resume truth 职责：

- 当前 phase / tranche pointer
- 当前 hard gate 与 exit criteria
- 当前 verification snapshot
- 当前 active blocker / risk
- 恢复执行的读取顺序

## 哪些结论必须 repo-native

以下结论如果要成为正式 review truth，必须进入 repo-tracked surface，而不能只留在 `.omx/**`：

- formal entry matrix
- durability model clarification
- verification contract 中的 hard gate 命令集合
- `grant_run_id / workspace_id / draft_id / program_id` 的正式语义边界
- `CLI`、`MCP`、`controller` 各自是否正式支持
- `ApplicantFitMapping` 是否进入当前 canonical route
- `outline -> drafting` 是否只是 transition contract

## 哪些状态允许只留在 local handoff surfaces

以下信息可以继续只由 `.omx/**` 承担：

- 当前 active program / phase / tranche pointer
- 当前最新 verification snapshot
- 当前 open risks / blockers
- 当前 resume 顺序与执行提示
- 当前一次 closeout 的 leader notes 与 iteration log

但 `.omx/**` 不能单独发明新的 formal entry、verification hard gate 或 identity semantics。

## Identity Boundary Contract

- `grant_run_id`
  - 语义：单次 grant run 的稳定执行句柄
  - 落点：runtime output、CLI output、reports、recovery context 回显
- `workspace_id`
  - 语义：`NSFCWorkspace` 聚合根身份
  - 落点：workspace object identity
- `draft_id`
  - 语义：`ApplicationDraft` 身份
  - 落点：draft / critique / revision 链接身份
  - 约束：`revision` 完成后仍沿用同一 `draft_id`
- `program_id`
  - 语义：control-plane / report-routing 身份
  - 落点：`.omx/reports/<program_id>/` 与 active mainline pointer

这四类 ID 不得互相替代。

## Verification Boundary Contract

- 当前 tranche hard gate：只看 repo-native commands 与 repo-native tests
- external verifier `omx_project_installer.py diff --target ...`
  - 当前仅为 advisory external check
  - 失败必须在 reports 中被记录
  - 但在没有显式改写 active truth surfaces 前，不得重新写成 current hard gate

## 当前 freeze 结论

- formal entry 真相已进入 repo-durable current truth
- durability model 真相已进入 repo-durable current truth
- `grant_run_id / workspace_id / draft_id / program_id` 边界已在 docs / schema / example / CLI / tests / reports 中一致
- `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 已进入当前 P2.B canonical route
- 当前 freeze 继续作为 `P2.B` 的硬边界存在，但不构成 `P2.C` activation
