# MAG 理想目标态差距与完成度审计

Owner: `Med Auto Grant`
Purpose: `active_gap_and_completion_audit`
State: `active_evidence_tail`
Machine boundary: 本文是人读完成度索引。机器真相归 current-program、root contracts、source、OPL conformance、runtime receipts、live progress 与 workspace/package artifacts。

## 目标态

`Declarative Grant Pack + OPL generated/hosted surfaces + minimal MAG authority functions`

## 原始过度设计规划

| # | 原始条目 | 状态 | 完成度 | Current evidence |
| ---: | --- | --- | ---: | --- |
| 1 | 删除未使用的 `hermes-agent[acp]` 依赖 | done | 100% | dependency/lock surface只保留 release-cohort OPL shared package |
| 2 | 删除正式入口不可达的 9 个模块 | done | 100% | continuous reconciliation、memory projection、family shared release等 cohort 已物理退役 |
| 3 | 消除 domain command catalog 双重真相 | done | 100% | public hosted action 只来自 closed `family-action-catalog.v2`；repo-local direct handler 只保留 MAG authority dispatch |
| 4 | 删除重复 hosted bundle payload builder | done | 100% | payload construction只有一个 owner；runtime仅组装和校验 |
| 5 | 删除 compatibility re-export、alias、wrapper 与退休 helper | done | 100% | patch bridge、private facade和 compatibility alias已退役 |
| 6 | 合并重复 index/dedupe/count helpers到标准库 | done | 100% | index owner唯一；dedupe使用 `dict.fromkeys`；计数使用 `Counter` |
| 7 | 删除 editable bootstrap与 import-time path injection | done | 100% | 依赖由 `uv`/package config管理；repo source不再注入路径 |
| 8 | 移除 ProductEntry/DomainRuntime 单实现 mixin树 | done | 100% | ProductEntry/MRO实现细节面退役；保留直接 `MagDomainRuntime` |
| 9 | 由 registry驱动 CLI parser与dispatch | done | 100% | command specs 只声明 parser 字段；执行使用显式静态 dispatch，已删除 `handler` 注入、`runtime_method` 与 `getattr` 动态分派 |
| 10 | 删除 runtime consumer-thinning/functional-closure自审计层 | done | 100% | OPL conformance/CI持有静态审计；MAG runtime不再投影自审计产品面 |
| 11 | 删除 MAG 私有 product/status/user-loop/runtime/workbench平台面 | done | 100% | 3 个 stage-bound hosted action + direct authority handler；progress/cockpit/status/workbench 归 OPL generated/read-model surface |
| 12 | 删除私有 OPL pack compiler与tracked generated aggregate | done | 100% | `agent/`/root contracts是声明源；OPL Pack生成 family stage plane |
| 13 | 将 cycle/rollback/resume/dispatch/output编排迁入 OPL StageRun | done | 100% | MAG只保留 selector、quality 与 authority receipt；Codex 选择语义 route |
| 14 | 将全部 executor transport 上收到 OPL Python client | done | 100% | authoring/critique 的 `codex_cli` 与 `hermes_agent` 均调用 `opl_framework.executor_client.run_agent_execution_request`；repo-local Codex/OPL subprocess、adapter 和 default command 已删除 |
| 15 | 将 Agent Package/Codex carrier 生命周期统一到 OPL Packages | done | 100% | canonical `opl packages install mag`、`opl packages update mag`、`opl packages uninstall mag`；本地 installer/symlink/marketplace mutation 已删除 |
| 16 | 关闭 6 个 generated default-caller retirement tails | done | 100% | 4 个 physically absent surface 声明 retired；`cli/domain_handler` 保留为 authority adapter 并提供 keep/no-write/provenance refs |

结构规划完成度：`16/16 done`。这只证明源码、contracts、docs与结构边界已经收口，不证明运行态 ready。

## Standard Agent Contract V2 收口

| 条目 | 状态 | 完成度 | Fresh evidence / stop condition |
| --- | --- | ---: | --- |
| Closed action catalog v2 | done | 100% | 只保留 `open_grant_user_loop`、`build_direct_entry`、`build_submission_ready_package`；全部使用 exact `stage_binding` 与 closed input schema |
| 私有 command template 退役 | done | 100% | descriptor 不再包含 `entry_command_template`、`manifest_command_template`、`runtime.dispatch_command`；MAG 测试固定 closed interface |
| Generated read model 归位 | done | 100% | `inspect_progress`、`inspect_cockpit` 已退出 action catalog 与 Stage allow-list；由 OPL 生成 progress/cockpit/status/workbench |
| Domain handler registry | done | 100% | `contracts/domain_handler_registry.json` 是 closed 空 registry；当前无 `handler_ref` public action，不通过 registry 暴露私有 runtime shell |
| 七项 authority 对齐 | done | 100% | functional audit、pack input、handler export、tests、core docs 与 skill carrier统一为 7；`ai_route_policy` 不算第八项 authority |
| OPL Packages consumer 声明 | done | 100% | MAG sidecar、测试与 active docs统一到 package id `mag` 的 install/update/uninstall；未修改 OPL Release Set、digest lock 或 lifecycle 实现 |
| Source-closure exact 分类 | done | 100% | final Contract V2 scanner `status=passed`；4 entrypoints、384 reachable symbols、1348 call edges、17 observed effects，unresolved/private generic/unreachable sensitive/audit mismatch 全部为 `0` |
| MAG final structural admission | done | 100% | isolated fresh readback：scaffold `passed`、interfaces `ready`、source closure `passed`、conformance `1 passed / 0 blocked`，structural 与 ordinary-path guard均为 `passed`，MAG blockers `[]` |

Contract V2 结构收口为 `8/8 done`。这只关闭 MAG candidate 对应的非 Live 功能/结构边界；最终吸收后仍须在 promoted OPL main 上重放 currentness，且不能由此声明任何 Live readiness。

## Live Evidence Gate

| 条目 | 状态 | 完成度 | 缺口 |
| --- | --- | ---: | --- |
| 真实 OPL-hosted grant stage attempts | blocked | 0% | 需要 runtime attempt与receipt refs |
| Submission human gate | blocked | 0% | 需要真实 human-gate receipt |
| Quality/export live receipt | blocked | 0% | 需要真实 attempt的 MAG owner receipt |
| App/operator sustained consumption | blocked | 0% | 需要 default-caller长期 readback |
| Provider long soak与 owner acceptance | blocked | 0% | 需要 live/no-regression evidence |

因此不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。

## Stop Condition

- 不通过新增 wrapper、snapshot、read model或 test-only proof推进 readiness。
- 没有真实 owner/live evidence时保持 typed blocker与 `domain_owned_closing_ref=null`。
- Consumer dependency pin保持 shared release cohort commit，不追 OPL dev HEAD。
- Structural currentness必须绑定最终发布的 OPL main：overall passed、source behavior matched 0、blocking 0；allowed matches逐项记录。
- Tests-only收益只按 `tests/**` path-filtered numstat计算，不把 source/contracts/docs删除计入。

## Final Structural Evidence

Contract V2 fresh evidence：

- OPL integration snapshot `eb4634f1f9fa74a8171c7e1cfef492420f2280c4` 上，MAG source closure 为 `status=passed`、`entrypoint_count=4`、`reachable_symbol_count=384`、`call_edge_count=1348`、`observed_effect_count=17`、`unresolved_edge_count=0`、`private_generic_effect_count=0`、`unreachable_sensitive_residue_count=0`、`audit_mismatch_count=0`，closure digest 为 `sha256:d2e91403e3bb4d4c8bf82570da7d41e18ef97bc85a24a6eaf4630349213ddbc1`。
- 同一 snapshot 的 isolated readback 为 scaffold `passed`、interfaces `ready`、source closure `passed`、conformance `1 passed / 0 blocked`、`structural_conformance_status=passed`、`ordinary_path_guard_status=passed`、MAG blockers `[]`。
- Fresh default-callers 为 `8/8` retirement gates closed、blocked/worklist `0`、source closure verified、`keep_as_authority_adapter_observed_no_further_opl_delete_work`；该 refs-only read model仍明确 `physical_delete_authorized=false`。
- Fresh residue-decisions 为 `decision_item_count=0`、`residue_verification_status=verified_zero`，scheduler/queue/session store/workbench/status shell/domain wrapper/runtime watch/agent-lab materializer八类 residue均为 `0`。
- Conformance 使用空的 `OPL_STATE_DIR` 与 `OPL_MODULES_ROOT` 隔离本机历史安装 descriptor；隔离只去除陈旧本地状态污染，不恢复已退役 command template，也不提升 `live_domain_progress_status=owner_evidence_recorded_not_ready_claim`。
- 单 Agent readback 的 Foundry Agent OS family aggregate 会按设计报告 MAS/RCA/OMA/OBF 与 `mas-scholar-skills` 未输入；MAG domain report自身为 `passed`、blockers `[]`。该 family aggregate 必须由最终五 Agent closeout重放，不能伪装成 MAG 私有兼容字段。

以下证据属于 Contract V2 前的已吸收结构基线，仅作 provenance；旧 `matched 0`、`allowed 9` 或旧 OPL SHA 不替代上面的 V2 scanner/readback。

- 2026-07-11 boundary convergence：OPL default-caller readback 为 `8/8` retirement gates closed、active deletion worklist `0`、retired default surface `4`，`cli/domain_handler` owner decision 为 `keep_as_authority_adapter_ref`；OPL conformance 继续满足 structural passed、matched generic behavior `0`、active private generic residue `0`。
- MAG authoring/critique 全部使用 OPL Python `executor_client`；fresh full 为 `170 passed + 231 subtests`，production source executor transport 扫描为 `0`。这只证明结构与行为兼容，不代表 live grant、provider long-soak 或 production readiness。
- Foundry consumer ABI基线：OPL `ddcc3242adac530b03f0a66bfe27a6a83bd835b5`、policy bundle `sha256:2abdcbe6e7c238dfc0bcbff2251fb0eda505647927446a6fbf47ae8b28253415`；MAG 只消费 canonical policy export、policy release pin 和 `opl-generated:family_stage_control_plane`，不复制 Foundry policy bodies。
- OPL conformance：`status=passed`、`matched_source_behavior_count=0`、`blockers=[]`、`allowed_source_behavior_count=9`、`unclassified_generic_behavior_count=0`、`active_private_generic_residue_count=0`。
- OPL route/Runway：action route与 refs-only `domain_output` ABI已进入 canonical main；真实 OMA create -> fixture-run -> query保留 selected action/route、object metadata与 output ref，OPL不读取 domain output body。
- OPL full residual：唯一 `system-seed-manifest` 失败在 candidate/base均为相同 `10/11` 与 `2 != 0`，不属于 MAG/Runway候选回归；其余 focused、MAG integration、smoke与静态门通过。
- Shared consumer dependency pin保持 `e1e734031ab3ea45596c6ce131f611f296ca9746`。
- MAG production canonical：`3fd7cd3dc5bd3102ac8bf95b33a90a439b82e7fc`；descriptor contract通过；CLI smoke `8 passed`；fast `124 passed + 60 subtests`；meta `36 passed`；full `235 passed + 177 subtests`。

V1 allowed matches（provenance）：

| Path | Signature | Classification |
| --- | --- | --- |
| `src/med_autogrant/domain_executor_client.py` | typed MAG request/closeout adapter over OPL client | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/authoring_executor.py` | grant authoring prompts and domain output normalization | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/critique_executor.py` | grant critique prompt and typed closeout normalization | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_handler.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_handler_contract.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_handler_dispatch.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_memory_runtime.py` | `repo_owned_product_status_session_shell` | `memory_accept_reject / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/domain_memory_runtime.py` | `repo_owned_receipt_observability_shell` | `memory_accept_reject / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/owner_receipt_common.py` | `repo_owned_product_status_session_shell` | `owner_receipt_signer / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/owner_receipt_writers.py` | `repo_owned_product_status_session_shell` | `owner_receipt_signer / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/primitives.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/typed_blocker_projection.py` | `repo_owned_product_status_session_shell` | `owner_receipt_signer / minimal_authority_function` |

## Tests-only Final Closeout

- Tests-only commit：`c755594d7a005176fab1e687de58f42a49ab0ece`，parent为 production canonical `3fd7cd3dc5bd3102ac8bf95b33a90a439b82e7fc`。
- 写集严格为 `22` 个 `tests/**` 路径，`+995/-2690`，净删 `1695` 行；source、contracts、docs与scripts变化为 `0`。
- 相对严格基线 `0268a89c0124`：`+2525/-16626`，净删 `14101` 行。
- 相对本任务基线 `689881c438b7`：`+1530/-13061`，净删 `11531` 行。
- Production-only分账保持：严格基线 `+1591/-13997`、净删 `12406`；本任务基线 `+592/-10428`、净删 `9836`。这些 source/contracts/docs混合阶段变化不计入 tests-only收益。
- Final tracked tests：`57` 个文件、`6161` 行；其中 Python `56` 个文件、`6160` 行，另有 `tests/.gitkeep` 1行。
- `rg 'sys.path.insert' tests` 为 `0`；6个 production-retired tests未复活。
- Fresh evidence：changed-owner focused `65 passed + 120 subtests`；smoke `8 passed`；fast `88 passed + 96 subtests`；meta `36 passed`；full `163 passed + 235 subtests`；independent review `ACCEPT, P0-P3=0`。
- Replay lane吸收分类为 `exact-merged`。三个旧 tests candidate clones先被owner判定为 superseded/rejected，再切到 canonical target取得 `exact-merged` cleanup evidence；四个 tests clone及 replay branch均已删除。无关 `stage-size-mag` lane保留。

Per-file tests-only numstat：

```text
0   3   tests/cli_validate_cases.py
32  180 tests/test_cli_validate_workspace_error_cases.py
126 316 tests/test_cli_validate_workspace_revision_cases.py
58  111 historical repo-local Codex transport test (physically retired)
33  74  tests/test_codex_plugin_installer.py
13  116 tests/test_codex_plugin_installer_script.py
0   5   tests/test_critique_policy.py
98  214 tests/test_domain_runtime.py
3   3   tests/test_final_package.py
0   91  tests/test_funding_discovery_cli.py
117 205 tests/test_funding_landscape_discovery.py
83  229 tests/test_grant_quality.py
0   138 tests/test_grant_quality_cli.py
55  180 tests/test_hosted_contract_bundle.py
51  173 tests/test_hosted_contract_bundle_checkpoint_cases.py
19  43  tests/test_opl_agent_lab_longline_migration.py
0   6   tests/test_opl_executor_adapter.py
61  201 tests/test_profile_selection_cli.py
0   8   tests/test_project_profile_selector.py
86  0   tests/test_public_cli_dispatch.py
67  214 tests/test_stage_router.py
93  180 tests/test_stage_run_kernel_profile_contract.py
```

最终 canonical SHA由Git push/readback给出，不在自身提交内容中自引用。
