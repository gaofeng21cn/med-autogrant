# Post-R5A Final Package Artifact Bundle Artifacts Object Required List Fields Fail-Closed Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `post-R5A local runtime hardening`
- Active slice: `build-final-package artifact bundle artifacts object required list fields fail-closed hardening`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` walkthrough / output-consistency / worktree-aware hosted-contract / local-runtime validation-failed / final-package malformed artifact bundle / hosted-contract malformed final-package / hosted-contract final-package required scalar-field / hosted-contract final-package required nested-field / hosted-contract final-package checkpoint-semantics / hosted-contract final-package lineage value-type / hosted-contract final-package freeze_manifest value-type / final-package artifact-bundle required nested-field / final-package artifact-bundle required scalar value-type / final-package artifact-bundle summary count value-type / final-package artifact-bundle artifacts list value-type / final-package artifact-bundle artifacts object value-type / final-package artifact-bundle artifacts object primary-id field / final-package artifact-bundle artifacts list element-shape / final-package artifact-bundle artifacts object linkage-id field / final-package artifact-bundle artifacts object required string-field slices 已 absorbed
  - `build-final-package` 继续只属于本地 finalization / export boundary

## Goal

在不改写 `build-final-package` object boundary、不新增 runtime command、也不打开 actual hosted runtime / `P5` / 新 formal entry 的前提下，把 artifact bundle object payload 里当前 remaining required list fields 的 drift 收紧成 repo-tracked fail-closed contract：

- 当以下字段缺失、或 value 不是 `list` 时，`build-final-package` 必须稳定抛出 `WorkspaceStateError`：
  - `artifacts.selected_direction.required_evidence_ids`
  - `artifacts.selected_question.subquestions`
  - `artifacts.selected_question.linked_evidence_ids`
  - `artifacts.argument_chain.linked_evidence_ids`
  - `artifacts.fit_mapping.linked_evidence_ids`
- 不得再出现：
  - `artifacts.selected_direction.required_evidence_ids=None` 或缺失 却仍成功产出 final package
  - `artifacts.selected_question.subquestions={}` 或缺失 却仍成功产出 final package
  - `artifacts.selected_question.linked_evidence_ids=None` 或缺失 却仍成功产出 final package
  - `artifacts.argument_chain.linked_evidence_ids={}` 或缺失 却仍成功产出 final package
  - `artifacts.fit_mapping.linked_evidence_ids=None` 或缺失 却仍成功产出 final package
- 以上字段都必须存在且是 `list`。

## Trigger Evidence

当前 landed 实现中：

- `_read_artifact_bundle(...)` 已开始校验：
  - object payload 自身是 `dict`
  - primary-id fields
  - linkage-id fields
  - required descriptive string fields
- 但仍未显式校验这些 object payload 的 remaining required list fields

这导致多个 concrete gap：

1. `artifacts.selected_direction.required_evidence_ids=None` 时，CLI 仍会成功产出 final package；
2. `artifacts.selected_question.subquestions={}` 时，CLI 仍会成功产出 final package；
3. `artifacts.selected_question.linked_evidence_ids=None` 时，CLI 仍会成功产出 final package；
4. `artifacts.argument_chain.linked_evidence_ids={}` 时，CLI 仍会成功产出 final package；
5. `artifacts.fit_mapping.linked_evidence_ids=None` 时，CLI 仍会成功产出 final package；
6. 进一步缺字段审计显示，上述五个 required list fields 缺失时也都会 fail-open。

## In Scope

### 1. object required list field validation

`build-final-package` 在读取 artifact bundle 后，至少必须显式校验并 fail-closed：

- `artifacts.selected_direction.required_evidence_ids`
- `artifacts.selected_question.subquestions`
- `artifacts.selected_question.linked_evidence_ids`
- `artifacts.argument_chain.linked_evidence_ids`
- `artifacts.fit_mapping.linked_evidence_ids`

以上字段都必须存在且是 `list`。

### 2. stable WorkspaceStateError surface

对 malformed artifact bundle：

- 必须抛出 `WorkspaceStateError`
- CLI 必须继续返回当前 repo 既有的 machine-readable error payload
- 不得继续成功产出 final package 掩盖 object required-list drift

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
- 上述 list fields 的 element value-type / element shape 校验
- object payload `metadata` 校验

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
4. 构造非法 object required list fields，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-final-package ... --format json`
   - 断言 fail-closed，而不是成功产出 final package
5. 保持 canonical happy path：
   - `build-artifact-bundle -> build-final-package -> build-hosted-contract-bundle`
6. `git diff --check`

## Promotion Invariants

- `build-final-package` 继续只消费上述 object required list fields 为 `list` 的 artifact bundle，不放宽 `R2.A -> R4.A` 输入 contract
- malformed artifact bundle 只能 fail-closed，不能 fallback、不能补默认值掩盖 object required-list drift
- `build-final-package` 继续只是本地 finalization / export surface，不得借机扩成 actual hosted runtime 语义

## Honest Stop Rule

如果这条 slice 完成后，剩余事项已经需要：

- actual hosted runtime
- `P5.A / P5.B`
- 新 formal entry
- 或新对象边界改写

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
