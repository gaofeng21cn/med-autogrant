# Post-R5A Final Package Artifact Bundle Required Scalar Value Types Fail-Closed Activation Package

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `post-R5A local runtime hardening`
- Active slice: `build-final-package artifact bundle required scalar value types fail-closed hardening`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` walkthrough / output-consistency / worktree-aware hosted-contract / local-runtime validation-failed / final-package malformed artifact bundle / hosted-contract malformed final-package object-field / hosted-contract final-package required scalar-field / hosted-contract final-package required nested-field / hosted-contract final-package checkpoint-semantics / hosted-contract final-package lineage value-type / hosted-contract final-package freeze_manifest value-type / final-package artifact-bundle required nested-field slices 已 absorbed
  - `build-final-package` 继续只属于本地 finalization / export boundary

## Goal

在不改写 `build-final-package` object boundary、不新增 runtime command、也不打开 actual hosted runtime / `P5` / 新 formal entry 的前提下，把当前 artifact bundle required scalar nested values 路径上的 fail-open gap 收紧成 repo-tracked fail-closed contract：

- 当 artifact bundle 的 required scalar nested values 不是非空字符串时，`build-final-package` 必须稳定抛出 `WorkspaceStateError`
- 不得再出现：
  - `selection.selected_direction_id=""` 却仍成功产出 final package
  - `selection.active_fit_mapping_id=[]` 却仍成功产出 final package
  - `manifest.direction_id=""`、`manifest.draft_version_label=None`、`manifest.draft_status={}` 却仍成功产出 final package
  - `lineage.frozen_question_id=""`、`lineage.argument_chain_id={}`、`lineage.draft_id=0` 却仍成功产出 final package
- `build-final-package` 继续只消费 scalar nested values 完整且类型正确的 artifact bundle；不放宽 `R2.A -> R4.A` 的输入 contract

## Trigger Evidence

当前 landed 实现中：

- `_read_artifact_bundle(...)` 已开始校验：
  - `selection / manifest / lineage / bundle_summary / artifacts` top-level object fields 存在
  - 这些 object 内的 required nested fields 存在
- 但仍未显式校验 `selection / manifest / lineage` 内 required scalar nested values 必须是非空字符串

这导致多个 concrete gap：

1. `selection.selected_direction_id=""` 时，CLI 仍会成功产出 final package；
2. `selection.selected_question_id=None`、`selection.active_fit_mapping_id=123`、`selection.active_draft_id=[]` 时，CLI 仍会成功产出 final package；
3. `manifest.direction_id=""`、`manifest.question_id=False`、`manifest.argument_chain_id=0`、`manifest.fit_mapping_id={}`、`manifest.draft_id=[]`、`manifest.draft_version_label=None`、`manifest.draft_status={}` 时，CLI 仍会成功产出 final package；
4. `lineage.frozen_question_id=""`、`lineage.argument_chain_id={}`、`lineage.fit_mapping_id=[]`、`lineage.draft_id=0` 时，CLI 仍会成功产出 final package。

## In Scope

### 1. artifact bundle required scalar nested value validation

`build-final-package` 在读取 artifact bundle 后，至少必须显式校验并 fail-closed：

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

以上字段都必须是**非空字符串**。

### 2. stable WorkspaceStateError surface

对 malformed artifact bundle：

- 必须抛出 `WorkspaceStateError`
- CLI 必须继续返回当前 repo 既有的 machine-readable error payload
- 不得继续成功产出 final package 掩盖 artifact bundle scalar value drift

### 3. no semantic drift

这条 slice 只收紧 `build-final-package` 的输入 fail-closed 语义，不改写：

- final package payload shape
- `checkpoint_summary` canonical source
- `build-artifact-bundle` 写入语义
- `build-hosted-contract-bundle` export 边界
- actual hosted runtime / control-plane formal entry 边界

## Out Of Scope

- actual hosted runtime
- remote execution / Web UI / multi-tenant
- `P5.A / P5.B`
- same-repo `Human-in-the-loop`
- 新 formal entry
- `bundle_summary` 的 count value-type 校验
- `artifacts` object/list value-type 校验

## Object Boundary

当前 slice 只允许收紧：

- `src/med_autogrant/final_package.py`
- `tests/test_final_package.py`
- 如有必要：`tests/test_program_control_surfaces.py`

不允许顺带改写：

- `artifact_bundle` 写入逻辑
- `local_runtime`
- `route_report`
- `hosted_contract_bundle`
- `formal_entry_matrix`

## Required Verification

至少覆盖：

1. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
2. `python3 -m unittest discover -s tests -p 'test_final_package.py'`
3. `python3 -m unittest discover -s tests -p 'test_*.py'`
4. 构造非法 artifact bundle scalar nested values，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-final-package ... --format json`
   - 断言 fail-closed，而不是成功产出 final package
5. 保持 canonical happy path：
   - `build-artifact-bundle -> build-final-package -> build-hosted-contract-bundle`
6. `git diff --check`

## Promotion Invariants

- `build-final-package` 继续只消费 scalar nested values 完整且类型正确的 artifact bundle，不放宽 `R2.A -> R4.A` 输入 contract
- malformed artifact bundle 只能 fail-closed，不能 fallback、不能补默认值掩盖 scalar value drift
- `build-final-package` 继续只是本地 finalization / export surface，不得借机扩成 actual hosted runtime 语义

## Honest Stop Rule

如果这条 slice 完成后，剩余事项已经需要：

- actual hosted runtime
- `P5.A / P5.B`
- 新 formal entry
- 或新对象边界改写

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
