# Post-R5A Hosted Contract Bundle Final Package Freeze Manifest Value Types Fail-Closed Activation Package

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `post-R5A local runtime hardening`
- Active slice: `build-hosted-contract-bundle final package freeze_manifest value-type fail-closed hardening`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` walkthrough / output-consistency / worktree-aware hosted-contract / local-runtime validation-failed / final-package malformed artifact bundle / hosted-contract malformed final-package object-field / hosted-contract final-package required scalar-field / hosted-contract final-package required nested-field / hosted-contract final-package checkpoint-semantics / hosted-contract final-package lineage value-type slices 已 absorbed
  - `build-hosted-contract-bundle` 继续只属于本地 hostedization-prep export boundary

## Goal

在不改写 `build-hosted-contract-bundle` object boundary、不新增 runtime command、也不打开 actual hosted runtime / `P5` / 新 formal entry 的前提下，把当前 final package `freeze_manifest` value-type 路径上的 fail-open gap 收紧成 repo-tracked fail-closed contract：

- 当 final package `freeze_manifest` 的 required scalar fields 不是预期 value-shape 时，`build-hosted-contract-bundle` 必须稳定抛出 `WorkspaceStateError`
- 不得再出现：
  - `freeze_manifest.draft_version_label=""` 却仍成功导出 hosted contract bundle
  - `freeze_manifest.active_revision_plan_id=[]` 却仍成功导出 hosted contract bundle
  - `freeze_manifest.critique_id=""` 却仍成功导出 hosted contract bundle
  - `freeze_manifest.presubmission_frozen="false"` 却仍成功导出 hosted contract bundle
- `build-hosted-contract-bundle` 继续只消费 value-shape 正确的 `freeze_manifest`；不放宽 `R4.A -> R5.A` 的输入 contract

## Trigger Evidence

当前 landed 实现中：

- `_read_final_package(...)` 已开始校验 `freeze_manifest` required fields 是否存在
- 也已校验：
  - `freeze_manifest.draft_status`
  - `freeze_manifest.checkpoint_status`
- 但仍未显式校验：
  - `freeze_manifest.draft_version_label`
  - `freeze_manifest.active_revision_plan_id`
  - `freeze_manifest.critique_id`
  - `freeze_manifest.presubmission_frozen`

这些字段当前都还没有被强制为 repo-tracked 预期 value-shape。

这导致多个 concrete gap：

1. `freeze_manifest.draft_version_label=""` 时，CLI 仍会成功导出 hosted contract bundle；
2. `freeze_manifest.active_revision_plan_id=[]` 时，CLI 仍会成功导出 hosted contract bundle；
3. `freeze_manifest.critique_id=""` 时，CLI 仍会成功导出 hosted contract bundle；
4. `freeze_manifest.presubmission_frozen="false"` 时，CLI 仍会成功导出 hosted contract bundle。

## In Scope

### 1. final package freeze_manifest value-type validation

`build-hosted-contract-bundle` 在读取 final package 后，至少必须显式校验并 fail-closed：

- `freeze_manifest.draft_version_label`
- `freeze_manifest.active_revision_plan_id`
- `freeze_manifest.critique_id`

并要求这些字段都必须是非空字符串。

同时必须显式校验：

- `freeze_manifest.presubmission_frozen`

并要求它必须是布尔值。

### 2. stable WorkspaceStateError surface

对 malformed final package：

- 必须抛出 `WorkspaceStateError`
- CLI 必须继续返回当前 repo 既有的 machine-readable error payload
- 不得继续成功导出 hosted contract bundle 掩盖 `freeze_manifest` value-shape 缺口

### 3. no semantic drift

这条 slice 只收紧 `build-hosted-contract-bundle` 的输入 fail-closed 语义，不改写：

- `formal_entry_matrix`
- `execution_identity` 的字段集合
- `artifact_contract / audit_contract` payload shape
- `build-final-package` 的写入语义
- actual hosted runtime / control-plane formal entry 边界

## Out Of Scope

- actual hosted runtime
- remote execution / Web UI / multi-tenant
- `P5.A / P5.B`
- same-repo `Human-in-the-loop`
- 新 formal entry
- 放宽 `R4.A` final package contract

## Object Boundary

当前 slice 只允许收紧：

- `src/med_autogrant/hosted_contract_bundle.py`
- `tests/test_hosted_contract_bundle.py`
- 如有必要：`tests/test_program_control_surfaces.py`

不允许顺带改写：

- `final_package` 写入逻辑
- `artifact_bundle`
- `local_runtime`
- `route_report`
- `formal_entry_matrix`

## Required Verification

至少覆盖：

1. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
2. `python3 -m unittest discover -s tests -p 'test_hosted_contract_bundle.py'`
3. `python3 -m unittest discover -s tests -p 'test_*.py'`
4. 构造 `freeze_manifest` required scalar fields 为空、类型非法或布尔值漂移的 final package，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle ... --format json`
   - 断言 fail-closed，而不是成功导出 hosted contract bundle
5. 保持 canonical happy path：
   - `build-artifact-bundle -> build-final-package -> build-hosted-contract-bundle`
6. `git diff --check`

## Promotion Invariants

- `build-hosted-contract-bundle` 继续只消费 value-shape 正确的 `freeze_manifest`，不放宽 `R4.A -> R5.A` 输入 contract
- malformed final package 只能 fail-closed，不能 fallback、不能补默认值掩盖 `freeze_manifest` value-type 缺口
- `build-hosted-contract-bundle` 继续只是本地 hostedization-prep export surface，不得借机扩成 actual hosted runtime 语义

## Honest Stop Rule

如果这条 slice 完成后，剩余事项已经需要：

- actual hosted runtime
- `P5.A / P5.B`
- 新 formal entry
- 或 hosted contract bundle 之外的新对象边界改写

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
