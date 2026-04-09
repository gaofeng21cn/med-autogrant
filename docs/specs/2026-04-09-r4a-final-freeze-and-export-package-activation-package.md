# R4.A Final Freeze And Export Package Activation Package

Date: `2026-04-09`

## Activation Status

- Future phase: `Runtime Productization Program`
- Future tranche: `R4 / Finalization And Export Surface`
- Future slice: `R4.A / Final Freeze And Export Package`
- Status: `pre-frozen / not activated`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A` 必须已 absorbed
  - `R3.A / Critique Revision Executor Surface` implementation 必须已 absorbed
  - `verification_checkpoint / checkpoint_status`、`ready_for_submission` 与 `presubmission_frozen` gate surface 必须继续全绿

## Goal

在不改写 `CLI` formal entry、不把 `MCP / controller` 写成已支持 public runtime、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把 author-side mainline 改写成 reviewer / HITL / hosted runtime 产品的前提下，预冻结 `R4.A` 的最小 finalization contract：

- 把 active revised / frozen workspace 与 active artifact bundle 收成 submission-facing local final package
- 明确 final package、freeze manifest、checkpoint summary 与 export summary 的 machine-readable object boundary
- 让本地 runtime 第一次具备“形成完整申请交付包”的 deterministic local delivery surface

这里冻结的不是“已经实现 final export”的事实，而是：

- 哪些对象必须先存在
- `build-final-package` 的 CLI contract 是什么
- final package 必须长什么样
- 进入实现前必须满足哪些 verification / invariants / stop conditions

当前 formal-entry matrix 继续固定为：

- `CLI`：当前唯一 formal entry
- `MCP`：`not-yet-supported` 的 future protocol layer
- `controller`：`not-yet-supported` 的 internal surface，不是 public formal entry

## Hard Boundary Docs

必须同时服从：

- `/Users/gaofeng/workspace/med-autogrant/contracts/project-truth/AGENTS.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-r2a-artifact-bundle-production-surface-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-r3a-critique-revision-executor-surface-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`

## Object Boundary

`R4.A` 预冻结的对象边界是一个 **CLI-first local final-package write pass**：

1. 从 active workspace 读取：
   - current active `ApplicationDraft`
   - current active `RevisionPlan`
   - current active `MentorCritique`
   - `verification_checkpoint`
   - `checkpoint_status`
   - `gates.presubmission_frozen`
2. 从显式输入的 artifact bundle path 读取：
   - artifact bundle manifest
   - artifact bundle lineage
   - artifact bundle summary
3. 只在以下 gate-open / gate-closed 状态允许进入：
   - `checkpoint_status=freeze_ready`
   - 或 `checkpoint_status=submission_frozen`
4. 输出 machine-readable local final package

这意味着：

- `R4.A` 只处理 final package / freeze manifest / export summary
- `R4.A` 不再执行 critique / revision mutation
- `R4.A` 不得偷偷进入 hosted session / hosted state / federation

## Canonical CLI Surface

`R4.A` 一旦进入实现，只允许先新增一个 `CLI-first` 本地 finalization 命令：

1. `build-final-package`
   - 输入：`--input <workspace-json>`
   - artifact bundle：`--artifact-bundle <bundle-json-path>`
   - 输出路径：`--output <final-package-json-path>`
   - 输出：本次 final package 生产的 machine-readable payload

约束：

- 新命令仍属于 `CLI` formal entry，不新增第二 formal entry
- `build-final-package` 不得替代旧五个 canonical CLI surfaces
- `build-final-package` 不得替代 `run-local / resume-local / build-artifact-bundle / execute-revision-pass`
- `build-final-package` 只写 final package output，不写 `.omx/**`

## Final Package Contract

`R4.A` 的 final package 必须是 machine-readable local delivery package；最小字段集冻结为：

- `package_version`
- `package_kind`
  - 当前固定为 `final_package`
- `grant_run_id`
- `workspace_id`
- `draft_id`
- `lifecycle_stage`
- `freeze_manifest`
  - `draft_version_label`
  - `draft_status`
  - `active_revision_plan_id`
  - `critique_id`
  - `checkpoint_status`
  - `presubmission_frozen`
- `lineage`
  - `frozen_question_id`
  - `selected_direction_id`
  - `selected_question_id`
  - `active_fit_mapping_id`
  - `draft_id`
  - `revision_plan_id`
- `checkpoint_summary`
  - `verification_checkpoint`
  - `checkpoint_status`
- `export_summary`
  - `outline_count`
  - `section_count`
  - `artifact_count`
- `deliverables`
  - `artifact_bundle_manifest`
  - `final_draft_outline`
  - `final_draft_sections`

冻结语义：

- `package_kind` 当前固定为 `final_package`
- `freeze_manifest.draft_status` 只允许 `revised / frozen`
- `freeze_manifest.checkpoint_status` 只允许 `freeze_ready / submission_frozen`
- `deliverables.final_draft_sections` 只能来自当前 active `ApplicationDraft.sections`
- `deliverables.artifact_bundle_manifest` 只能来自显式输入的 artifact bundle
- `checkpoint_summary.verification_checkpoint` 必须与 active workspace 中的 canonical checkpoint surface 一致

## Local Output Contract

`R4.A` 的本地 output 只能是调用方显式提供的 final package path：

- `--output <final-package-json-path>` 为必填
- 若 output 已存在且其 `grant_run_id / workspace_id / draft_id` 与当前不一致，必须 fail-closed
- final package output 是产品 runtime 的本地 durable artifact，不替代 `.omx/reports/**`

## Relation To Existing Canonical Surfaces

`R4.A` 必须继续围绕以下 surfaces 聚合，不得重写它们的 canonical 语义：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`
- `run-local`
- `resume-local`
- `build-artifact-bundle`
- `execute-revision-pass`
- `verification_checkpoint`
- `checkpoint_status`

关系冻结如下：

- `verification_checkpoint / checkpoint_status` 继续是 final gate 的 canonical aggregation surface
- `build-artifact-bundle` 继续只处理 artifact bundle，不替代 final package
- `execute-revision-pass` 继续只处理 revision mutation，不替代 final freeze / export
- `build-final-package` 只组装本地 delivery package，不生成 hosted contract

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许进入 `R4.A` implementation 前，必须同时满足：

1. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已显式引用本 activation package
2. `tests/test_program_control_surfaces.py` 已对本 activation package 的存在性与控制面对齐做出断言
3. baseline hard gate 继续全绿：
   - `python3 -m unittest discover -s tests -p 'test_*.py'`
   - `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
   - `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
   - `python3 -m unittest discover -s tests -p 'test_artifact_bundle.py'`
   - 当前 canonical CLI examples
   - `git diff --check`

### Implementation Promotion Gate

当 `R4.A` 进入实现时，必须补齐并通过以下新增验证：

1. final package contract regression tests
2. freeze manifest consistency tests
3. final package completeness / deliverable alignment tests
4. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3a_ready_for_submission.json --output "$TMPDIR/r4a-freeze-ready-bundle.json" --format json`
5. `PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3a_ready_for_submission.json --artifact-bundle "$TMPDIR/r4a-freeze-ready-bundle.json" --output "$TMPDIR/r4a-freeze-ready-package.json" --format json`
6. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output "$TMPDIR/r4a-frozen-bundle.json" --format json`
7. `PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle "$TMPDIR/r4a-frozen-bundle.json" --output "$TMPDIR/r4a-frozen-package.json" --format json`
8. `git diff --check`

## Promotion Invariants

- 不得改写 `grant_run_id / workspace_id / draft_id / program_id`
- 不得改写 `frozen_question_id`
- final package 必须与 `verification_checkpoint / checkpoint_status` 对齐
- export 只能发生在本地 submission-facing surface
- 不得在这一层引入 `MCP / controller` public formal entry
- 不得把 local final package 误写成 actual hosted runtime 已完成

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `R4.A` implementation：

1. `R1.A / R1.B / R2.A / R3.A` 已 absorbed
2. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已把 `R4.A` 写成当前 active next slice
3. 新增能力仍然只属于 final freeze / export，而不是 hostedization / `P5`
4. 当前 baseline hard gate 继续全绿

## Stop Conditions

以下情况出现时，必须诚实停车：

- 当前看似要做的能力其实已经需要 host/session/state/artifact/audit hosted contract
- artifact bundle 仍不是稳定输入
- `verification_checkpoint / checkpoint_status` 无法作为 final gate 的 canonical source
- 必须改写 formal entry、`MCP`、`controller`、或 `P5` 才能让 `R4.A` 成立

## Excluded Scope

- hosted-friendly session / state / artifact / audit contract
- actual hosted runtime
- web runtime / hosted platform / credits / billing
- second-family / federation
- same-repo HITL
