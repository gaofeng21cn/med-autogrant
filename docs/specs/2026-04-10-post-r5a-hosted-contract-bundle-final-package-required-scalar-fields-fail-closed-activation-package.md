# Post-R5A Hosted Contract Bundle Final Package Required Scalar Fields Fail-Closed Activation Package

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `post-R5A local runtime hardening`
- Active slice: `build-hosted-contract-bundle final package required scalar-field fail-closed hardening`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` walkthrough / output-consistency / worktree-aware hosted-contract / local-runtime validation-failed / final-package malformed artifact bundle / hosted-contract malformed final-package object-field slices 已 absorbed
  - `build-hosted-contract-bundle` 继续只属于本地 hostedization-prep export boundary

## Goal

在不改写 `build-hosted-contract-bundle` object boundary、不新增 runtime command、也不打开 actual hosted runtime / `P5` / 新 formal entry 的前提下，把当前 final package required scalar-field 路径上的 fail-open gap 收紧成 repo-tracked fail-closed contract：

- 当 final package identity 虽然仍是同一个对象、`package_kind` 也正确、object fields 也存在，但 `package_version`、`lifecycle_stage`、`grant_run_id`、`workspace_id`、`draft_id` 缺失或类型非法时，`build-hosted-contract-bundle` 必须稳定抛出 `WorkspaceStateError`
- 不得再出现：
  - 缺 `package_version` 却仍成功导出 hosted contract bundle
  - 缺 `lifecycle_stage` 却仍成功导出 hosted contract bundle
  - `grant_run_id / workspace_id / draft_id` 不是非空字符串，却仍被写进 `execution_identity`
- `build-hosted-contract-bundle` 继续只消费完整 final package；不放宽 `R4.A -> R5.A` 的输入 contract

## Trigger Evidence

当前 landed 实现中：

- `_read_final_package(...)` 已开始校验 `freeze_manifest / checkpoint_summary / lineage` 等 object fields
- 但仍未显式校验：
  - `package_version`
  - `lifecycle_stage`
  - `grant_run_id`
  - `workspace_id`
  - `draft_id`

这导致多个 concrete gap：

1. 缺 `package_version` 时，CLI 仍会成功导出 hosted contract bundle；
2. 缺 `lifecycle_stage` 时，CLI 仍会成功导出 hosted contract bundle；
3. `grant_run_id / workspace_id / draft_id` 不是非空字符串时，当前实现仍会把非法 identity 写进 `execution_identity`，形成 fail-open。

## In Scope

### 1. final package required scalar-field validation

`build-hosted-contract-bundle` 在读取 final package 后，至少必须显式校验并 fail-closed：

- `package_version`
- `lifecycle_stage`
- `grant_run_id`
- `workspace_id`
- `draft_id`

并与 `R4.A` 已冻结的 final package 最小字段集保持一致，不允许把明显结构残缺或 identity 非法的 final package 视为合法输入。

### 2. stable WorkspaceStateError surface

对 malformed final package：

- 必须抛出 `WorkspaceStateError`
- CLI 必须继续返回当前 repo 既有的 machine-readable error payload
- 不得继续成功导出 hosted contract bundle 掩盖输入 contract 缺口

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
4. 构造缺 `package_version` 的 final package，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle ... --format json`
   - 断言 fail-closed，而不是成功导出 hosted contract bundle
5. 构造缺 `lifecycle_stage` 的 final package，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle ... --format json`
   - 断言 fail-closed，而不是成功导出 hosted contract bundle
6. 构造 `grant_run_id / workspace_id / draft_id` 不是非空字符串的 final package，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle ... --format json`
   - 断言 fail-closed，而不是继续把非法 identity 写进 `execution_identity`
7. 保持 canonical happy path：
   - `build-artifact-bundle -> build-final-package -> build-hosted-contract-bundle`
8. `git diff --check`

## Promotion Invariants

- `build-hosted-contract-bundle` 继续只消费完整 final package，不放宽 `R4.A -> R5.A` 输入 contract
- malformed final package 只能 fail-closed，不能 fallback、不能补默认值掩盖结构缺口
- `build-hosted-contract-bundle` 继续只是本地 hostedization-prep export surface，不得借机扩成 actual hosted runtime 语义

## Honest Stop Rule

如果这条 slice 完成后，剩余事项已经需要：

- actual hosted runtime
- `P5.A / P5.B`
- 新 formal entry
- 或 hosted contract bundle 之外的新对象边界改写

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
