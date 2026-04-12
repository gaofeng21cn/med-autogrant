# Lightweight Product Entry And OPL Handoff Current Truth

Date: `2026-04-12`

## Activation Status

- Phase: `Lightweight Product Entry / OPL Handoff Shell`
- Status: `landed / current truth`

## Goal

在已经 landed 的：

- `CLI-first + real upstream Hermes-Agent runtime substrate`
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
  - `start_entry=run-local`
  - `resume_entry=resume-local`
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

### 4. 当前 critique / revision / export route 的状态已经诚实冻结

- 所有未 landed 的 authoring route
  - `route_status = pending`
  - `handoff_contract_kind = handoff-required`
  - `handoff_requirements`
    - 至少会列出：
      - `required_domain_surfaces`
      - `required_identity_fields`
      - `required_summary_fields`
      - `required_gate_fields`
- `critique`
  - 在 `drafting -> critique` 这类 pre-review 上下文里，只要求：
    - `summarize-workspace`
    - `stage-route-report`
  - 在 `critique / revision / frozen` review context 里，才额外要求：
    - `critique-summary`
- `revision`
  - `route_status = landed`
  - `execution_surface.command = execute-revision-pass`
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
- `hermes_runtime.py` 仍只是 repo-side domain adapter / orchestrator，而不是 runtime substrate owner
- 不扩 `P5` federation / second family / Human-in-the-loop sibling
- 这层 landed shell 不等于成熟最终 UX，也不等于 actual hosted runtime

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_product_entry.py tests/test_hermes_runtime_truth.py tests/test_program_control_surfaces.py tests/test_test_command_surfaces.py -q`
- `uv run python -m med_autogrant build-product-entry --input examples/nsfc_workspace_p2c_critique.json --entry-mode direct --task-intent tighten-grant-mainline --format json`

## Honest Boundary

这条 current truth 只说明：

- 轻量结构化 `product entry` shell 已 landed
- `direct` 与 `opl-handoff` 现在共享同一套 envelope
- 这层 shell 明确建立在 `MedAutoGrantDomainEntry` 与真实 Hermes substrate contract 之上
- external caller 现在还可以直接从 `return_surface_contract.domain_entry_contract` 读取 `supported_commands` / `command_contracts`
- 这层 shell 还能显式告诉 caller：当前哪些 author-side route 已 landed，哪些还只是 `pending / handoff-required`
- 对 `critique` 这类仍未 landed 的 route，这层 shell 现在还会直接导出 `handoff_requirements`，告诉 caller 应先读取哪些 domain surfaces 再协作
- 这层 shell 现在还会把 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / frozen` 一并纳入同一份 `author_side_route_catalog`
- 对 canonical 的 `revision(completed revised switch) -> critique` 返场路径，这层 shell 也已经能在 `recommended_executor_route` 里稳定导出同一份 critique handoff contract

它不意味着：

- 最终用户产品前台已经成熟
- `OPL Gateway` 完整消费链已全部落地
- actual hosted runtime 已完成
- submission-grade autopilot 已完成
