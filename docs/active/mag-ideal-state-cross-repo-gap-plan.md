# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `active_gap_and_completion_plan`
State: `active`
Machine boundary: 本文是人读计划。机器真相归 current-program、root contracts、source、runtime receipts、live progress 与 workspace/package artifacts。

## 目标态

`Declarative Grant Pack + OPL generated/hosted surfaces + minimal MAG authority functions`

## 完成度审计

| 条目 | 状态 | 完成度 | Fresh machine owner / 缺口 |
| --- | --- | ---: | --- |
| 私有 OPL pack/compiler/source scanner 退役 | done | 100% | OPL conformance scanner；MAG source 不再含 private compiler |
| Product/status/user-loop/runtime/workbench wrapper 退役 | done | 100% | direct handler + OPL generated handoff |
| Domain handler 收到 3 actions | done | 100% | current-program + handler contract/export |
| 八项 authority ID 对齐 | done | 100% | functional audit、pack input、current-program、handler export |
| Owner receipt shape 与 refs 对齐 | done | 100% | owner receipt contract + writer focused tests |
| CLI/bootstrap/alias/proof lane cleanup | done | 100% | canonical agent id `mag`；`medautogrant` executable only；clean runner、CLI smoke |
| Tests 去实现细节/快照绑定 | done | 100% | focused suites + collect/full gate |
| OPL structural/source behavior | done | 100% | OPL `673eac1f` scanner: overall pass, matched 0, blockers 0 |
| 真实 OPL-hosted stage attempts | blocked | 0% | 需要 runtime attempt/receipt evidence |
| Submission human gate | blocked | 0% | 需要真实 human-gate receipt |
| Quality/export live receipt | blocked | 0% | 需要真实 attempt 的 MAG owner receipt |
| App/operator sustained consumption | blocked | 0% | 需要 owner/default-caller readback |
| Provider long soak 与 owner acceptance | blocked | 0% | 需要 live/readback evidence |

结构 `100%` 只表示 executable structural gate 已关闭，不表示 grant-ready、submission-ready 或 production-ready。

## 当前行动

1. OPL/App owner 产生真实 hosted stage attempt refs。
2. MAG owner 对 quality/export/package 与 human gate 返回 receipt 或 typed blocker。
3. App/operator/default caller记录 sustained consumption。
4. Temporal/provider owner提供 long-soak 与 success/no-regression readback。
5. `contracts/live_stage_run_progress_evidence.json` 在收到真实 closing refs 后更新。

## Stop Condition

- 不再通过添加 wrapper、snapshot、read model 或 test-only proof推进 readiness。
- 没有真实 owner/live evidence 时保持 typed blocker 和 `domain_owned_closing_ref=null`。
- Consumer dependency pin保持 release cohort commit；本轮 OPL conformance 固定绑定 `673eac1f8193296ed371aeef7fe82f14bd441370`，不追逐未纳入本任务的后续 dev HEAD。

## 2026-07-10 Structural Cleanup Closeout Evidence

- MAG base main：`689881c438b7c87393be042584675638e9a16689`。
- OPL consumer binding：`673eac1f8193296ed371aeef7fe82f14bd441370`；conformance `status=passed`、source behavior `matched=0`、blockers `0`、allowed matches `10`。
- Canonical identity：OPL agent id `mag`；`medautogrant` 只作为 executable command，`med-autogrant` 只作为 repo/package/plugin/skill locator。
- Tests-only：当前 Python test source 为 `8,807` 行，相对严格 Python 基线 `20,261` 行减少 `11,454`；若包含稳定的 1 行 `tests/.gitkeep`，则 tracked `tests/**` 为 `8,808` 行，相对同口径严格基线 `20,262` 行同样净减 `11,454`。
- Path-filtered diff：相对严格基线提交 `0268a89c01240a7303ee032745af7b0ef08724e8`，`tests/** +1,527 / -12,981 / net -11,454`；相对本任务 main 基线 `17,692` 行，`tests/** +410 / -9,294 / net -8,884`。`src/**`、`contracts/**`、schemas、docs 与 README 的删除不计入 tests-only 收益。
- Fresh owner evidence：focused `50 passed + 128 subtests`；CLI smoke `11 passed`；fast `148 passed + 67 subtests`；meta `35 passed`；full `258 passed + 183 subtests`；descriptor contract、diff-check 与 OPL scanner通过。

完整 `tests/**` numstat（`additions deletions path`）：

```text
0 11 tests/conftest.py
0 1 tests/opl_family_contract_adoption_cases/__init__.py
0 41 tests/opl_family_contract_adoption_cases/controlled_soak.py
0 50 tests/opl_family_contract_adoption_cases/test_consumer_thinning.py
0 270 tests/product_entry_cases/support.py
42 79 tests/product_entry_cases/test_authority_surface_boundaries.py
0 115 tests/product_entry_cases/test_codex_stage_receipts.py
0 40 tests/product_entry_cases/test_controlled_soak.py
116 248 tests/product_entry_cases/test_domain_handler.py
0 208 tests/product_entry_cases/test_domain_memory_descriptor.py
7 9 tests/product_entry_cases/test_domain_memory_receipt_evidence.py
0 221 tests/product_entry_cases/test_executor_first_closeout_bundle.py
0 221 tests/product_entry_cases/test_external_evidence_consumption_ledger.py
0 144 tests/product_entry_cases/test_external_evidence_request_pack.py
0 110 tests/product_entry_cases/test_failure_modes.py
0 222 tests/product_entry_cases/test_family_orchestration_manifest.py
0 143 tests/product_entry_cases/test_grant_transition_oracle.py
0 61 tests/product_entry_cases/test_human_gate_typed_blocker.py
0 93 tests/product_entry_cases/test_loop_and_readiness.py
0 183 tests/product_entry_cases/test_opl_owner_payload_response.py
0 262 tests/product_entry_cases/test_opl_owner_payload_response_cli.py
0 314 tests/product_entry_cases/test_production_live_acceptance.py
0 222 tests/product_entry_cases/test_receipt_readiness.py
0 140 tests/product_entry_cases/test_status_start_cases.py
0 242 tests/support/grant_autonomy_controller.py
1 1 tests/support/hosted_contract_bundle.py
0 126 tests/test_active_path_scan_policy_guard.py
0 35 tests/test_ai_first_quality_boundary.py
0 56 tests/test_capability_map.py
8 15 tests/test_cli_smoke.py
0 286 tests/test_cli_validate_workspace.py
0 305 tests/test_cli_validate_workspace_product_entry_cases.py
23 20 tests/test_codex_plugin.py
0 125 tests/test_cognitive_kernel_adoption_contract.py
22 0 tests/test_control_plane.py
26 425 tests/test_domain_entry.py
0 390 tests/test_domain_runtime_autonomy.py
0 181 tests/test_domain_runtime_split.py
0 124 tests/test_editable_shared_bootstrap.py
0 304 tests/test_executor_first_landing_program.py
0 120 tests/test_generated_aggregate_source_index.py
0 86 tests/test_grant_autonomy_cli.py
0 65 tests/test_grant_autonomy_common.py
0 460 tests/test_grant_autonomy_controller.py
0 163 tests/test_grant_autonomy_loop_parts.py
0 125 tests/test_grant_autonomy_loop_shell.py
0 133 tests/test_grant_autonomy_quality_payload.py
0 258 tests/test_grant_governance_adapter.py
1 1 tests/test_line_budget.py
0 31 tests/test_live_stage_run_progress_evidence.py
0 126 tests/test_mainline_status.py
31 65 tests/test_opl_family_contract_adoption.py
0 152 tests/test_opl_ledger_artifact_registration.py
0 122 tests/test_opl_standard_pack.py
0 67 tests/test_opl_standard_pack_physical_morphology.py
30 250 tests/test_owner_chain_live_progress_evidence.py
2 2 tests/test_plan_completion_audit.py
65 201 tests/test_production_acceptance.py
33 60 tests/test_program_control_surfaces.py
0 1 tests/test_project_profile_selector.py
0 47 tests/test_repository_hygiene.py
0 123 tests/test_runtime_cli_structural_helpers.py
0 7 tests/test_schema_registry.py
0 302 tests/test_schema_registry_product_entry_surfaces.py
0 128 tests/test_source_purity_guard_readback.py
0 23 tests/test_stage_artifact_kernel_adoption_contract.py
0 111 tests/test_stage_folder_lifecycle_contract.py
3 21 tests/test_test_command_surfaces.py
0 1 tests/test_workspace_summary.py
```
