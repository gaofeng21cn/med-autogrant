# Post-R5A Hosted Contract Bundle Final Package Checkpoint Semantics Fail-Closed Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_post_r5a_hosted_contract_final_package_fail_closed_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-10 post-R5A hosted-contract-bundle final-package fail-closed hardening slice 的形成过程。当前 hosted/default task runtime owner 是 OPL/Temporal；hosted-contract bundle、local hostedization prep、host-agent、Gateway 与 hosted runtime wording 只作 provenance。当前 hosted caller evidence、contract export、package/export behavior、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准；本文不声明 public hosted runtime、App release ready 或 production ready。

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `post-R5A local runtime hardening`
- Active slice: `build-hosted-contract-bundle final package checkpoint-semantics fail-closed hardening`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` walkthrough / output-consistency / worktree-aware hosted-contract / local-runtime validation-failed / final-package malformed artifact bundle / hosted-contract malformed final-package object-field / hosted-contract final-package required scalar-field / hosted-contract final-package required nested-field slices 已 absorbed
  - `build-hosted-contract-bundle` 继续只属于本地 hostedization-prep export boundary

## Goal

在不改写 `build-hosted-contract-bundle` object boundary、不新增 runtime command、也不打开 actual hosted runtime / `P5` / 新 formal entry 的前提下，把当前 final package checkpoint-semantics 路径上的 fail-open gap 收紧成 repo-tracked fail-closed contract：

- 当 final package 的 `freeze_manifest.draft_status`、`freeze_manifest.checkpoint_status`、`checkpoint_summary.checkpoint_status`、`verification_checkpoint.checkpoint_status` 不满足 `R4.A` 已冻结语义时，`build-hosted-contract-bundle` 必须稳定抛出 `WorkspaceStateError`
- 不得再出现：
  - `freeze_manifest.draft_status` 不是 `revised / frozen` 却仍成功导出 hosted contract bundle
  - `freeze_manifest.checkpoint_status` 或 `checkpoint_summary.checkpoint_status` 不是 `freeze_ready / submission_frozen` 却仍成功导出 hosted contract bundle
  - `freeze_manifest.checkpoint_status`、`checkpoint_summary.checkpoint_status`、`verification_checkpoint.checkpoint_status` 彼此不一致，却仍成功导出 hosted contract bundle
- `build-hosted-contract-bundle` 继续只消费 checkpoint truth 一致的 final package；不放宽 `R4.A -> R5.A` 的输入 contract

## Trigger Evidence

当前 landed 实现中：

- `_read_final_package(...)` 已开始校验 top-level fields、required scalar fields、required nested fields
- 但仍未显式校验：
  - `freeze_manifest.draft_status` 只能是 `revised / frozen`
  - `freeze_manifest.checkpoint_status` 只能是 `freeze_ready / submission_frozen`
  - `checkpoint_summary.checkpoint_status` 只能是 `freeze_ready / submission_frozen`
  - `verification_checkpoint.checkpoint_status` 必须存在且与其余 checkpoint statuses 保持一致

这导致多个 concrete gap：

1. `freeze_manifest.draft_status="draft"` 时，CLI 仍会成功导出 hosted contract bundle；
2. `freeze_manifest.checkpoint_status="forward_progress"` 或 `checkpoint_summary.checkpoint_status="forward_progress"` 时，CLI 仍会成功导出 hosted contract bundle；
3. `verification_checkpoint.checkpoint_status` 缺失或与其余 checkpoint statuses 不一致时，CLI 仍会成功导出 hosted contract bundle。

## In Scope

### 1. final package checkpoint-semantics validation

`build-hosted-contract-bundle` 在读取 final package 后，至少必须显式校验并 fail-closed：

- `freeze_manifest.draft_status`
- `freeze_manifest.checkpoint_status`
- `checkpoint_summary.checkpoint_status`
- `verification_checkpoint.checkpoint_status`
- 以上 checkpoint statuses 的内部一致性
- 当三处 checkpoint surfaces 漂移时，必须显式以 `checkpoint_status 不一致` fail-closed

并与 `R4.A` 已冻结的 final package checkpoint semantics 保持一致，不允许把 checkpoint truth 已漂移的 final package 视为合法输入。

### 2. stable WorkspaceStateError surface

对 malformed final package：

- 必须抛出 `WorkspaceStateError`
- CLI 必须继续返回当前 repo 既有的 machine-readable error payload
- 不得继续成功导出 hosted contract bundle 掩盖 checkpoint semantics 缺口

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
4. 构造 `freeze_manifest.draft_status` 非法的 final package，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle ... --format json`
   - 断言 fail-closed，而不是成功导出 hosted contract bundle
5. 构造 `freeze_manifest.checkpoint_status` 或 `checkpoint_summary.checkpoint_status` 非法的 final package，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle ... --format json`
   - 断言 fail-closed，而不是成功导出 hosted contract bundle
6. 构造 `verification_checkpoint.checkpoint_status` 缺失或与其他 checkpoint statuses 不一致的 final package，执行：
   - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle ... --format json`
   - 断言 fail-closed，而不是成功导出 hosted contract bundle
7. 保持 canonical happy path：
   - `build-artifact-bundle -> build-final-package -> build-hosted-contract-bundle`
8. `git diff --check`

## Promotion Invariants

- `build-hosted-contract-bundle` 继续只消费 checkpoint truth 一致的 final package，不放宽 `R4.A -> R5.A` 输入 contract
- malformed final package 只能 fail-closed，不能 fallback、不能补默认值掩盖 checkpoint semantics 缺口
- `build-hosted-contract-bundle` 继续只是本地 hostedization-prep export surface，不得借机扩成 actual hosted runtime 语义

## Honest Stop Rule

如果这条 slice 完成后，剩余事项已经需要：

- actual hosted runtime
- `P5.A / P5.B`
- 新 formal entry
- 或 hosted contract bundle 之外的新对象边界改写

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
