# Post-R5A Final Package Malformed Artifact Bundle Fail-Closed Activation Package

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `post-R5A local runtime hardening`
- Active slice: `build-final-package malformed artifact bundle fail-closed hardening`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` walkthrough / output-consistency / validation-failed local runtime hardening slices 已 absorbed
  - `build-final-package` 继续只属于本地 final/export boundary

## Goal

在不改写 `build-final-package` object boundary、不新增 runtime command、也不打开 actual hosted runtime / `P5` / 新 formal entry 的前提下，把一个已经可直接复现的本地 fail-open / traceback gap 收紧成 repo-tracked fail-closed contract：

- 当 artifact bundle identity 虽然匹配、但缺少 `manifest`、`artifacts` 或其他 `R2.A` 冻结 required fields 时，`build-final-package` 必须稳定抛出 `WorkspaceStateError`
- 不得再出现：
  - 原生 `KeyError` traceback
  - 结构不完整却被当成合法 bundle 继续导出 final package
- `build-final-package` 继续只消费完整 artifact bundle；不放宽 `R2.A -> R4.A` 的输入 contract

## Trigger Evidence

当前 landed 实现中：

- `_read_artifact_bundle(...)` 只校验：
  - 顶层 object
  - `bundle_kind`
  - `grant_run_id / workspace_id / draft_id` identity
- 但后续 `build_final_package_payload(...)` 直接消费：
  - `artifact_bundle["manifest"]`
  - `artifact_bundle.get("artifacts", {})`

这导致两个 concrete gap：

1. identity 正确但缺 `manifest` 时，CLI 直接抛 `KeyError` traceback，而不是 fail-closed JSON error surface；
2. identity 正确、缺 `artifacts` 时，当前实现会把它静默当成 `{}`，继续导出 final package，形成 fail-open。

## In Scope

### 1. artifact bundle required-field validation

`build-final-package` 在读取 artifact bundle 后，至少必须显式校验并 fail-closed：

- `manifest`
- `artifacts`

并且应与 `R2.A` 已冻结的最小字段集保持一致，不允许把明显结构残缺的 bundle 视为合法输入。

### 2. stable WorkspaceStateError surface

对 malformed artifact bundle：

- 必须抛出 `WorkspaceStateError`
- CLI 必须继续返回当前 repo 既有的 machine-readable error payload
- 不得再出现裸 traceback / 原生 `KeyError`

### 3. no semantic drift

这条 slice 只收紧 `build-final-package` 的输入 fail-closed 语义，不改写：

- `checkpoint_status` final gate 词汇表
- `final_package` payload shape
- `build-artifact-bundle` 的写入语义
- `build-hosted-contract-bundle` 的 hosted contract export 边界

## Out Of Scope

- actual hosted runtime
- remote execution / Web UI / multi-tenant
- `P5.A / P5.B`
- same-repo `Human-in-the-loop`
- 新 formal entry
- 放宽 `R2.A` artifact bundle contract

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
4. 构造 identity 正确但缺 `manifest` 的 bundle，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-final-package ... --format json`
   - 断言返回 repo-native fail-closed JSON，而不是 traceback
5. 构造 identity 正确但缺 `artifacts` 的 bundle，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-final-package ... --format json`
   - 断言 fail-closed，而不是成功导出 final package
6. 保持 canonical happy path：
   - `build-artifact-bundle -> build-final-package -> build-hosted-contract-bundle`
7. `git diff --check`

## Promotion Invariants

- `build-final-package` 继续只消费完整 artifact bundle，不放宽 `R2.A` 输入 contract
- malformed artifact bundle 只能 fail-closed，不能 fallback、不能补默认值掩盖结构缺口
- `build-final-package` 继续属于本地 final/export surface，不得借机扩成 hosted/runtime 语义

## Honest Stop Rule

如果这条 slice 完成后，剩余事项已经需要：

- actual hosted runtime
- `P5.A / P5.B`
- 新 formal entry
- 或 final package 之外的新对象边界改写

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
