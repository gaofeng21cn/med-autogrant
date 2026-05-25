# Post-R5A Local Runtime Validation-Failed Route Checkpoint Shape Alignment Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_post_r5a_validation_failed_route_checkpoint_alignment_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-10 validation-failed route checkpoint shape alignment activation package 的形成过程。当前 route checkpoint、validation behavior、runtime owner 与 stage executor 以核心五件套、active gap plan、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准；本文不恢复 local runtime owner、journal、attempt ledger 或 hosted runtime claim。

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `post-R5A local runtime hardening`
- Active slice: `runtime-run / runtime-resume validation-failed route + checkpoint shape alignment`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` walkthrough / revised-workspace validator / checkpoint output consistency truth 已 absorbed
  - worktree-aware hosted-contract control-plane root resolution 已 absorbed

## Goal

在不打开 actual hosted runtime、不改写 `stage-route-report` 的 canonical success contract、也不发明新的 formal entry / `P5` 语义的前提下，把 `runtime-run / runtime-resume` 在 `validation_failed` 路径上的 output shape 收紧为与当前 route/checkpoint surface 一致的 fail-closed contract：

- `runtime-run` / `runtime-resume` 遇到 invalid workspace 时，`route_report` 仍必须显式保留 `route`、`verification_checkpoint`、顶层 `checkpoint_status`
- 该失败态仍必须保持：
  - `stop_reason.code = validation_failed`
  - `stage_action_envelope = null`
  - 不写出伪造的 successful route / critique semantics
- `stage-route-report` 继续是 success-path 的唯一 canonical checkpoint aggregation surface；本 slice 只要求 local runtime fail path 不再因为 shape 漂移而脱离同一套 route/checkpoint schema

## Trigger Evidence

当前 landed 实现中，`runtime-run` / `runtime-resume` 的 valid path 走：

- `build_stage_route_report(document)`
- `route_report.route`
- `route_report.verification_checkpoint`
- `route_report.checkpoint_status`
- `stop_reason`
- `stage_action_envelope`

但 invalid path 仍手工拼出一个特例 payload：

- `route_report` 缺少 `route`
- `route_report` 缺少顶层 `checkpoint_status`
- `route_report.verification_checkpoint = null`
- `stop_reason.checkpoint_status = null`

这会导致：

1. `runtime-run` / `runtime-resume` 在失败态不再沿用当前 canonical route/checkpoint shape；
2. journal 中的 `latest_route_report` 与 valid path drift；
3. post-`R5.A` 本地 output consistency 审计无法把 local runtime fail path 视为同一条诚实的 control surface。

## In Scope

### 1. invalid local runtime route_report shape tightening

对 `runtime-run` / `runtime-resume` 的 `validation_failed` 路径，`route_report` 最小必须显式保留：

- `ok = false`
- `grant_run_id`
- `workspace_id`
- `lifecycle_stage`
- `route`
  - `validate_workspace`
  - `summarize_workspace = null`
  - `next_step`
  - `critique_summary = null`
- `checkpoint_status = null`
- `verification_checkpoint`
  - `checkpoint_status = null`
  - `validation_ok = false`
  - 其余只允许保留 deterministic / null-filled 的 fail-closed fields，不得伪造成功态语义

### 2. stop_reason consistency

- `stop_reason.code` 继续固定为 `validation_failed`
- `stop_reason.reason` 必须来自 canonical validation error
- `stop_reason.current_stage / recommended_next_stage` 可以继续停留在当前 document stage
- `stop_reason.checkpoint_status` 必须与 `route_report.checkpoint_status` 一致，当前为 `null`

### 3. no second checkpoint truth

- `stage-route-report` 继续是 success-path 的 canonical checkpoint aggregation surface
- local runtime invalid path 只做 schema-shape 对齐
- 不得把此 slice 改写成新的 checkpoint vocabulary、hosted runtime 语义、或更高阶 route synthesis

## Out Of Scope

- actual hosted runtime
- remote execution / Web UI / multi-tenant
- `P5.A / P5.B`
- same-repo `Human-in-the-loop`
- 新 formal entry
- 把 invalid workspace 伪装成 successful `stage-route-report`
- 改写 valid-path `checkpoint_status` 词汇表

## Object Boundary

当前 slice 只允许收紧：

- `src/med_autogrant/domain_runtime.py`
- `tests/test_local_runtime.py`
- 如有必要：`tests/test_program_control_surfaces.py`

不允许顺带改写：

- `build-final-package`
- `build-hosted-contract-bundle`
- `execute-revision-pass`
- `formal_entry_matrix`
- `grant_run_id / workspace_id / draft_id / program_id` 的既有分工

## Required Verification

至少覆盖：

1. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
2. `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
3. `python3 -m unittest discover -s tests -p 'test_*.py'`
4. 构造一个 invalid workspace，执行：
   - `PYTHONPATH=src python3 -m med_autogrant runtime run --input <invalid> --journal <journal> --format json`
   - `PYTHONPATH=src python3 -m med_autogrant runtime resume --journal <journal> --format json`
5. 断言 invalid path 上：
   - `route_report.route.validate_workspace` 存在
   - `route_report.checkpoint_status is null`
   - `route_report.verification_checkpoint.checkpoint_status is null`
   - `route_report.verification_checkpoint.validation_ok is false`
   - `stop_reason.code == validation_failed`
   - `stage_action_envelope is null`
6. `git diff --check`

## Promotion Invariants

- `runtime-run / runtime-resume` 继续只是 local runtime loop entry / recovery
- `validation_failed` 继续是 stop-reason vocabulary，而不是新的 hosted/runtime tranche
- `checkpoint_status` 在 invalid path 只能保持 `null` mirror；不得被偷偷扩成新的 semantic enum
- `stage-route-report` 仍是 success-path 的唯一 canonical route/checkpoint aggregation surface

## Honest Stop Rule

如果这条 slice 完成后，剩余问题已经需要：

- 更高阶 critique / route 语义改写
- actual hosted runtime
- `P5.A / P5.B`
- 或新的 formal entry / public controller surface

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
