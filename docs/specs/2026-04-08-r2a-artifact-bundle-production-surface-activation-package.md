# R2.A Artifact Bundle Production Surface Activation Package

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-08`

## Activation Status

- Active phase: `Runtime Productization Program`
- Active tranche: `R2 / Artifact Production Surface`
- Active slice: `R2.A / Artifact Bundle Production Surface`
- Status: `frozen / implementation pending`
- Upstream prerequisite:
  - `R1.A / Local Main Loop Entry And Stop Reason` 已 absorbed（freeze `38b5347`；implementation `8e087dc`）
  - `R1.B / Stage Action Executor Envelope` 已 absorbed（freeze `2b193da`；implementation `2953026`）
  - 当前 active hard gate 必须继续全绿

## Goal

在不改写 `CLI` formal entry、不把 `MCP / controller` 写成已支持 public runtime、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把 author-side mainline 改写成 reviewer / HITL / hosted runtime 产品的前提下，冻结 `R2.A` 的最小实现合同：

- 把当前 workspace 中已稳定存在的 direction / question / argument chain / fit mapping / outline / draft 收成 machine-readable local artifact bundle
- 为 bundle 增加 manifest / lineage / version / bundle summary
- 让本地 runtime 第一次具备“围绕已冻结对象写出可复用申请材料包”的最小产品面

这里冻结的不是“生成新内容”的事实，而是：

- 只打包当前已经存在的 canonical objects
- 把 bundle durable 写到调用方显式给定的本地 output path
- 明确 `R2.A` 与 `R3 / R4 / R5` 的 object boundary

这里的 formal-entry 口径继续固定为：

- `CLI`：当前唯一 formal entry
- `MCP`：future protocol layer / `not-yet-supported`
- `controller`：internal surface / `not-yet-supported` public formal entry

## Hard Boundary Docs

必须同时服从：

- `/Users/gaofeng/workspace/med-autogrant/AGENTS.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`

## Object Boundary

`R2.A` 冻结的对象边界是一个 **CLI-first local artifact bundle write pass**：

1. 从当前 workspace 的 `current_selection` 中定位：
   - `selected_direction_id`
   - `selected_question_id`
   - `active_fit_mapping_id`
   - `active_draft_id`
2. 读取当前 canonical objects：
   - `direction_hypotheses[selected_direction_id]`
   - `scientific_question_cards[selected_question_id]`
   - `ArgumentChain`
   - `ApplicantFitMapping`
   - `ApplicationDraft.outline`
   - `ApplicationDraft.sections`
3. 把它们写成 machine-readable local artifact bundle
4. 补 manifest / lineage / version / bundle summary，但不得生成新内容、不得重写 workspace

这意味着：

- `R2.A` 只允许把已存在对象打包出来
- `R2.A` 不允许新增方向、换题、补写正文、执行 revision、生成 final export

## Canonical CLI Surface

`R2.A` 一旦进入实现，只允许新增一个 `CLI-first` 本地 bundle 命令：

1. `build-artifact-bundle`
   - 输入：`--input <workspace-json>`
   - 输出路径：`--output <bundle-json-path>`
   - 输出：本次 bundle 生产的 machine-readable payload

约束：

- 新命令仍属于 `CLI` formal entry，不新增第二 formal entry
- 旧五个 commands 与 `runtime-run / runtime-resume` 继续作为 verifier / audit baseline
- `build-artifact-bundle` 不得替代 `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report`
- `build-artifact-bundle` 只写 bundle output，不写回 workspace，不写 `.runtime-program/**`

## Artifact Bundle Contract

`R2.A` 的 artifact bundle 必须是 machine-readable local bundle；最小字段集冻结为：

- `bundle_version`
- `bundle_kind`
- `grant_run_id`
- `workspace_id`
- `draft_id`
- `lifecycle_stage`
- `selection`
  - `selected_direction_id`
  - `selected_question_id`
  - `active_fit_mapping_id`
  - `active_draft_id`
- `manifest`
  - `direction_id`
  - `question_id`
  - `argument_chain_id`
  - `fit_mapping_id`
  - `draft_id`
  - `draft_version_label`
  - `draft_status`
- `lineage`
  - `frozen_question_id`
  - `argument_chain_id`
  - `fit_mapping_id`
  - `draft_id`
- `bundle_summary`
  - `outline_count`
  - `section_count`
- `artifacts`
  - `selected_direction`
  - `selected_question`
  - `argument_chain`
  - `fit_mapping`
  - `draft_outline`
  - `draft_sections`

冻结语义：

- `bundle_kind` 当前固定为 `artifact_bundle`
- `draft_id` 必须来自当前 active `ApplicationDraft`
- `lineage.frozen_question_id` 必须与当前 active draft 的 `frozen_question_id` 一致
- `artifacts.draft_outline` 只能来自当前 active draft 的 `outline`
- `artifacts.draft_sections` 只能来自当前 active draft 的 `sections`
- `bundle_summary` 只能汇总当前 active draft，不得发明新章节或补全文本

## Local Output Contract

`R2.A` 的本地 output 只能是调用方显式提供的 bundle path：

- `--output <bundle-json-path>` 为必填
- 若 output 已存在且内容与当前 `grant_run_id / workspace_id / draft_id` 不一致，必须 fail-closed
- bundle output 是产品 runtime 的本地 durable artifact，不替代 `.runtime-program/reports/**`

## Relation To Existing Canonical Surfaces

`R2.A` 必须继续围绕以下 surfaces 聚合，不得重写它们的 canonical 语义：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`
- `runtime-run`
- `runtime-resume`
- `verification_checkpoint`
- `checkpoint_status`

关系冻结如下：

- `stage-route-report` 继续是 route / checkpoint aggregation 的 canonical baseline
- `runtime-run / runtime-resume / stage_action_envelope` 继续只处理 runtime orchestration
- `build-artifact-bundle` 只把已存在对象写成 bundle，不覆盖 checkpoint / stop reason / stage_action_envelope

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许进入 `R2.A` implementation 前，必须同时满足：

1. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已显式指向本 activation package
2. `tests/test_program_control_surfaces.py` 已对本 activation package 的存在性与控制面对齐做出断言
3. baseline hard gate 继续全绿：
   - `python3 -m unittest discover -s tests -p 'test_*.py'`
   - `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
   - `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
   - 当前 canonical CLI examples
   - `git diff --check`

### Implementation Promotion Gate

当 `R2.A` 进入实现时，必须补齐并通过以下新增验证：

1. 新的 artifact bundle contract regression tests
2. direction -> question -> argument -> fit -> outline -> draft lineage consistency tests
3. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p2b_outline.json --output "$TMPDIR/r2a-outline-bundle.json" --format json`
4. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p2c_revision.json --output "$TMPDIR/r2a-revision-bundle.json" --format json`
5. `git diff --check`

## Promotion Invariants

- 不得改写 `grant_run_id / workspace_id / draft_id / program_id`
- 不得改写 `frozen_question_id`
- 不得在 bundle 生产阶段执行 critique / revision / re-review
- 不得在 bundle 生产阶段生成 final package / freeze manifest / export summary
- 不得新增 `MCP / controller` formal entry
- 不得把 local bundle output 写成 `.omx` control-plane report

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `R2.A` implementation：

1. `R1.A` 与 `R1.B` 已 absorbed
2. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已把 `R2.A` 写成当前 active next slice
3. 这次新增能力仍然只属于 artifact bundle production，而不是 revision executor / final export / hostedization
4. 当前 baseline hard gate 继续全绿

## Stop Conditions

以下情况出现时，必须诚实停车：

- 当前看似要做的能力其实已经需要执行 critique / revision / re-review
- 当前看似要做的能力其实已经需要 final export / freeze manifest / hosted-friendly session contract
- 必须改写 formal entry、`MCP`、`controller`、或 `P5` 才能让 `R2.A` 成立
- 必须生成新内容而不是打包现有对象，才能让 bundle surface 成立

## Excluded Scope

- critique / revision executor
- rollback execution
- final package / freeze manifest / export summary
- hostedization
- second-family / federation
- same-repo HITL
