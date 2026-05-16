# Post-R5A Stage Route Report Checkpoint Status Output Consistency Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

日期锚点：`2026-04-10`

## 激活目的

在不打开 actual hosted runtime、不改写 formal entry matrix、不进入 `P5`、也不发明新的 runtime command 的前提下，冻结 post-`R5.A` 本地 runtime hardening 的一个最小 concrete delta：

- `stage-route-report` 的成功 JSON payload 必须显式回显顶层 `checkpoint_status`
- 该字段必须与 `verification_checkpoint.checkpoint_status` 严格相等
- `verification_checkpoint` 继续是唯一 canonical checkpoint aggregation object；顶层 `checkpoint_status` 只是 output-consistency mirror，不是第二套 checkpoint source

## 触发证据

当前 repo-tracked truth、public README 与 local walkthrough 已一致写明：

- `stage-route-report` 会输出 `verification_checkpoint`
- `stage-route-report` 会输出 `checkpoint_status`

但当前 landed 实现的成功 JSON payload 实际只有：

- `verification_checkpoint.checkpoint_status`

缺少顶层 `checkpoint_status`，从而导致：

1. operator 按 truth/docs 直接读取 `payload["checkpoint_status"]` 时失败；
2. `verification_checkpoint / checkpoint_status` 的 output shape 与 repo-tracked truth 存在 drift；
3. post-`R5.A` walkthrough / output consistency 审计无法把该 shape 视为完全收口。

## In Scope

1. `stage-route-report` 成功 JSON payload 的 output consistency tightening
2. baseline critique workspace 与 generated revised workspace 的回归测试
3. 保持 `runtime-run / build-final-package` 等现有 consumers 继续基于 `verification_checkpoint` 工作，不引入第二套 canonical source

## Out Of Scope

- actual hosted runtime
- remote execution / Web UI / multi-tenant
- `P5.A / P5.B`
- same-repo `Human-in-the-loop`
- 新 formal entry
- `build-final-package` / `build-hosted-contract-bundle` 的对象边界改写

## Object Boundary

本 slice 只收紧 `stage-route-report` 的成功 JSON payload：

- 继续保留现有字段：
  - `ok`
  - `grant_run_id`
  - `workspace_id`
  - `lifecycle_stage`
  - `route`
  - `verification_checkpoint`
- 新增或显式保留顶层字段：
  - `checkpoint_status`

冻结语义：

- `checkpoint_status == verification_checkpoint.checkpoint_status`
- 若两者不能严格一致，则实现必须视为错误而不是容忍漂移
- text output 可以继续从 canonical checkpoint object 渲染，不要求新增第二套格式化逻辑

## Promotion Invariants

- `verification_checkpoint` 继续是唯一 canonical checkpoint aggregation surface
- 不得把顶层 `checkpoint_status` 扩成可独立漂移的第二真相来源
- 不得改写 `grant_run_id / workspace_id / draft_id / program_id`
- 不得把该 slice 解释成 actual hosted runtime、`P5` 或新的 runtime ladder tranche

## Required Code/Test Surface

- code:
  - `src/med_autogrant/route_report.py`
- tests:
  - `tests/test_cli_validate_workspace.py`
  - `tests/test_revision_executor.py`
  - 如有必要：`tests/test_program_control_surfaces.py`

## Required Verification

至少覆盖：

- `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
- `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
- `python3 -m unittest discover -s tests -p 'test_artifact_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_revision_executor.py'`
- `python3 -m unittest discover -s tests -p 'test_final_package.py'`
- `python3 -m unittest discover -s tests -p 'test_hosted_contract_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- canonical CLI examples
- 至少一条 walkthrough 级 shape check：
  - `stage-route-report` on `examples/nsfc_workspace_p2c_critique.json`
  - `execute-revision-pass` on `examples/nsfc_workspace_p3b_re_review_major_revision.json`
  - `stage-route-report` on generated revised workspace
  - 断言顶层 `checkpoint_status` 与 `verification_checkpoint.checkpoint_status` 一致
- `git diff --check`

## Honest Stop Rule

如果该 slice 完成后，post-`R5.A` 本地 runtime 在当前 hard boundary 内已没有新的 concrete、repo-trackable output consistency delta，则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
