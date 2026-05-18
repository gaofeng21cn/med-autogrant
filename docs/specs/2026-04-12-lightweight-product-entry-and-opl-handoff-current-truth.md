# Lightweight Product Entry And OPL Handoff Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-12`

## Activation Status

- Phase: `Lightweight Product Entry / OPL Handoff Shell`
- Status: `landed / current truth`

## Goal

在已经 landed 的：

- `CLI-first + Codex CLI default runtime owner, with explicit Hermes-Agent proof lane`
- `MedAutoGrantDomainEntry`

之上，落一层轻量结构化 `product entry` shell，让：

- `direct`
- `opl-handoff`

共用同一套 entry envelope，同时不改写 author-side grant mainline 的对象边界与语义。

## Landed Facts

### 1. 仓库现在已有显式的 lightweight product-entry shell

- 新增 `src/med_autogrant/product_entry.py`
- 新增 CLI 命令：`build-product-entry`
- `build-product-entry` 当前支持：
  - `--entry-mode direct`
  - `--entry-mode opl-handoff`

### 2. `direct` 与 `opl-handoff` 现在共用同一套 envelope

当前共享 envelope 至少包括：

- `target_domain_id`
- `task_intent`
- `entry_mode`
- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`

grant 域在这层共享 envelope 之上继续补充：

- `workspace_id`
- `draft_id`
- `funding_call`

### 3. 这层 shell 明确复用已 landed 的 domain/runtime contract

- `build-product-entry` 当前通过 `MedAutoGrantDomainEntry` 读取：
  - `stage-route-report`
  - `summarize-workspace`
- `runtime_session_contract` 继续复用：
  - `grant_run_id`
  - `start_entry=runtime-run`
  - `resume_entry=runtime-resume`
  - `runtime_substrate_contract`
  - `runtime_state_contract`
- `return_surface_contract` 继续复用：
  - `MedAutoGrantDomainEntry`
  - `domain_entry_contract`
    - `supported_commands`
    - `command_contracts`
  - `stage-route-report`
  - `operator_contract`
- `executor_routing_contract` 现在与 `stage_action_envelope` 共享同一份 route truth：
  - `current_stage_route`
  - `recommended_executor_route`
  - `author_side_route_catalog`

### 4. 当前 author-side route catalog 已经全部收口为 landed route

- `direction_screening`
  - `route_status = landed`
  - `execution_surface.command = execute-direction-screening-pass`
- `question_refinement`
  - `route_status = landed`
  - `execution_surface.command = execute-question-refinement-pass`
- `argument_building`
  - `route_status = landed`
  - `execution_surface.command = execute-argument-building-pass`
- `fit_alignment`
  - `route_status = landed`
  - `execution_surface.command = execute-fit-alignment-pass`
- `outline`
  - `route_status = landed`
  - `execution_surface.command = execute-outline-pass`
- `drafting`
  - `route_status = landed`
  - `execution_surface.command = execute-drafting-pass`
- `critique`
  - `route_status = landed`
  - `execution_surface.command = execute-critique-pass`
  - 当前默认 concrete executor 是 `Codex CLI autonomous`
  - 默认 `model / reasoning` 都继承本机 Codex 默认（`inherit_local_codex_default`）
- `revision`
  - `route_status = landed`
  - `execution_surface.command = execute-revision-pass`
- `frozen`
  - `route_status = landed`
  - `execution_surface.command = execute-freeze-pass`
- `artifact_bundle`
  - `route_status = landed`
  - `execution_surface.command = build-artifact-bundle`
- `final_package`
  - `route_status = landed`
  - `execution_surface.command = build-final-package`
- `hosted_contract_bundle`
  - `route_status = landed`
  - `execution_surface.command = build-hosted-contract-bundle`

### 5. 当前实现是 fail-closed 的

- 空白 `task_intent` 会直接拒绝
- 缺失 `workspace_id`、`grant_run_id`、`checkpoint_status` 或 `recommended_next_stage` 的 route snapshot 会直接拒绝
- 非 valid workspace 不允许生成 product entry shell

## What Did Not Change

- formal entry 仍是 `CLI`
- `supported_protocol_layer` 仍是 `MCP`
- `internal_controller_surface` 仍是 `controller`
- `domain_runtime.py` 仍只是 repo-side domain adapter / orchestrator，而不是 runtime substrate owner
- 不扩 `P5` federation / second family / Human-in-the-loop sibling
- 这层 landed shell 不等于成熟最终 UX，也不等于 actual hosted runtime

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_product_entry.py tests/test_domain_runtime.py tests/test_program_control_surfaces.py tests/test_test_command_surfaces.py -q`
- `uv run python -m med_autogrant build-product-entry --input examples/nsfc_workspace_p2c_critique.json --entry-mode direct --task-intent tighten-grant-mainline --format json`

## Honest Boundary

这条 current truth 只说明：

- 轻量结构化 `product entry` shell 已 landed
- `direct` 与 `opl-handoff` 现在共享同一套 envelope
- `opl-handoff` 只作为 internal handoff/reference entry mode 阅读，不是兼容入口
- 这层 shell 明确建立在 `MedAutoGrantDomainEntry` 与默认 `codex_cli` runtime contract 之上；Hermes 只作为显式 proof lane
- external caller 现在还可以直接从 `return_surface_contract.domain_entry_contract` 读取 `supported_commands` / `command_contracts`
- 这层 shell 会显式告诉 caller：当前 author-side route catalog 已经全部 landed，并且都收口到同一份 service-safe command surface
- 对 canonical 的 `revision(completed revised switch) -> critique` 返场路径，这层 shell 也已经能在 `recommended_executor_route` 里稳定导出 landed `execute-critique-pass`

它不意味着：

- 最终用户产品前台已经成熟
- 当时语境下的 `OPL Gateway` 完整消费链已全部落地；当前应按 `OPL stage-led family runtime provider -> MAG-owned product sidecar / domain entry` 重新解读，不代表生产级 Temporal stage execution 已完成
- actual hosted runtime 已完成
- submission-grade autopilot 已完成
