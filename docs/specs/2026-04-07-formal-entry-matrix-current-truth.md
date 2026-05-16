# Formal Entry Matrix Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-07`

## 目标

把当前 active mainline 的正式入口矩阵持续冻结成 repo-durable current truth，避免把 future scope、developer control-plane entry、恢复入口、以及已 landed 的本地 runtime ladder 混写成同一种“入口”。

## 当前指针

- Current phase: `Runtime Productization Program`
- Active tranche: `R5 / Hostedization Prep`
- Latest absorbed runtime slice: `R5.A / Hosted-Friendly Session Boundary`
- Current owner line: `post-R5A local runtime closeout / honest stop`
- Current truthful closeout: `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`

本文件冻结的是当前 formal entry 真相；它不把 actual hosted runtime、`P5.A / P5.B`、same-repo `Human-in-the-loop`、`MCP / controller` public runtime entry 写进当前 scope。

## Formal Entry Matrix

### 1. `default_formal_entry`

- 当前冻结值：`CLI`
- 当前入口 family：
  - baseline verifier / audit surfaces
    - `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input ...`
    - `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input ...`
    - `PYTHONPATH=src python3 -m med_autogrant next-step --input ...`
    - `PYTHONPATH=src python3 -m med_autogrant critique-summary --input ...`
    - `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input ...`
  - local runtime entry / recovery
    - `PYTHONPATH=src python3 -m med_autogrant runtime run --input ... --journal ...`
    - `PYTHONPATH=src python3 -m med_autogrant runtime resume --journal ...`
  - local artifact / revision / finalization / hostedization-prep surfaces
    - `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input ... --output ...`
    - `PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input ... --output ...`
    - `PYTHONPATH=src python3 -m med_autogrant build-final-package --input ... --artifact-bundle ... --output ...`
    - `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle --final-package ... --output ...`

当前 contract：

- `CLI` 仍是当前唯一 repo-verified 的 user-facing runtime formal entry。
- 旧五个 canonical CLI surfaces 继续是 verifier / audit baseline，不得被新命令替代。
- 所有 CLI 输出都必须稳定回显同一 `grant_run_id`，并保持与 `workspace_id`、`draft_id`、`program_id` 分离。
- `grant_run_id` 是 execution handle，不是新的 formal entry family，也不是新的 controller pointer。
- `stage-route-report` 继续是 canonical route / checkpoint aggregation surface，并稳定输出 `verification_checkpoint / checkpoint_status`。
- `runtime-run` 只在既有 route / checkpoint surface 之上增加 machine-readable `stop_reason`、`stage_action_envelope` 与 local run journal。
- `runtime-resume` 只允许从同一 journal 恢复 `input_path`、沿用同一 `grant_run_id` 重新进入一次 local runtime pass。
- `build-artifact-bundle` 只允许把当前 active workspace 的 canonical objects 写成 machine-readable local bundle，不写回 workspace，不写 `.runtime-program/**`。
- `execute-revision-pass` 已 landed，但仍只允许在 repo-frozen `R3.A` deterministic mutation contract 内写出 revised workspace candidate；它不扩成 question / argument 级 mutation，不改写 formal entry。
- `build-final-package` 已 landed，但仍只允许在 `freeze_ready / submission_frozen` gate 上组装 machine-readable local `final_package`；它不替代 validator / route / revision surfaces。
- `build-hosted-contract-bundle` 已 landed，但仍只导出 hosted-friendly contract bundle；它不授权 actual hosted runtime，也不把 `.runtime-program/**` 写成 hosted audit store。
- 已 absorbed 的 post-`R5.A` hardening 继续要求：
  - revised workspace validator / checkpoint truth 与 landed local outputs 对齐；
  - re-review revised output 不得因为保留 `reviewed_revision_plan_id / reviewed_revision_evidence` 而被错误判 invalid；
  - operator walkthrough / command matrix 必须诚实展示当前已 landed 的本地 runtime ladder，而不是停留在 `R3.A` 前的旧口径。
- 在当前 formal-entry truth 下，当前 closeout 结论已经是 `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`；若要继续推进，必须先新增并冻结下一条 tranche truth。

### 2. `supported_protocol_layer`

- 当前冻结值：`MCP`
- 当前状态：`reserved future layer / not-yet-supported`
- 当前 contract：
  - `MCP` 在统一 formal-entry matrix 中保留为 supported protocol layer。
  - 当前仓库尚未把 `MCP` 冻结成 repo-verified public runtime formal entry。
  - 在没有 repo-tracked current truth 改写前，不得把 `MCP` 口头提升成“当前已经正式支持”。

### 3. `internal_controller_surface`

- 当前冻结值：`controller`
- 当前入口：
  - `CURRENT_PROGRAM.md`
  - `PROGRAM_ROUTING.md`
  - active `PRD / test-spec / implementation`
  - active `LATEST_STATUS / ITERATION_LOG / OPEN_ISSUES`

当前 contract：

- `controller` 在当前 formal-entry matrix 中属于 internal control surface，不是产品 runtime formal entry。
- 它负责 planning、active pointer、verification contract、report sync 与 long-run orchestration。
- 它不能被叙述成“已经有正式 MCP / controller runtime”。
- developer control-plane entry 的存在，不等于 public runtime formal entry 已存在。

### 4. recovery / resume entry

- 正式支持：是
- 当前入口：
  - `PYTHONPATH=src python3 -m med_autogrant runtime resume --journal ...`
  - developer control-plane recovery 改为依赖 repo-tracked `contracts/runtime-program/current-program.json` 与用户级 `$CODEX_HOME/projects/med-autogrant/runtime-state/`

当前 contract：

- `runtime-resume` 是当前产品 runtime 的本地 recovery / resume entry；它从 journal 恢复 `input_path`、沿用同一 `grant_run_id`，并 append 新 `attempt`。
- 当当前 stop reason 为 `stage_action_required` 时，恢复入口必须继续 durable 回写 machine-readable `stage_action_envelope`。
- developer control-plane entry 的恢复读取顺序仍是：
  1. `CURRENT_PROGRAM.md`
  2. `PROGRAM_ROUTING.md`
  3. active `PRD / test-spec / implementation`
  4. active `LATEST_STATUS / ITERATION_LOG / OPEN_ISSUES`
- 恢复时必须继续保留：
  - `active_revision_plan_id`
  - `reviewed_revision_plan_id`
  - `reviewed_revision_evidence`
  - `source_critique_id`
  - `forced_rollback_stage`
  - `forced_rollback_reason`
  - `presubmission_frozen`
  - `verification_checkpoint`
  - `checkpoint_status`

### 5. not-yet-supported / future public entry scope

- `MCP public runtime entry`
  - 当前状态：`not-yet-supported`
- `controller public runtime entry`
  - 当前状态：`not-yet-supported`

这些面仍属 future scope。任何后续若要把它们升级为正式入口，必须先改写 active truth surfaces，而不是口头默认。

## 当前 repo-native hard gate 裁决

当前 active tranche 的 hard gate 继续只包含 repo-native verification：

- `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
- `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
- `python3 -m unittest discover -s tests -p 'test_artifact_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_revision_executor.py'`
- `python3 -m unittest discover -s tests -p 'test_final_package.py'`
- `python3 -m unittest discover -s tests -p 'test_hosted_contract_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- 当前 canonical CLI examples
- `git diff --check`

post-`R5.A` local runtime hardening 额外要求：

- `execute-revision-pass` on `examples/nsfc_workspace_p3b_re_review_major_revision.json`
- `validate-workspace` on revised output
- `stage-route-report` on revised output
## 禁止越界解释

- 不得把 `supported_protocol_layer=MCP` 解释成“当前 public runtime 已正式支持 MCP”。
- 不得把 developer control-plane entry 的存在解释成“产品 controller 已正式支持”。
- 不得把 `grant_run_id` 解释成新的 control-plane pointer 或新的 public entry。
- 不得把 `build-hosted-contract-bundle` 解释成 actual hosted runtime 已完成。
- 不得把当前 post-`R5.A` hardening closeout 解释成 `P5` expansion 开工许可。
