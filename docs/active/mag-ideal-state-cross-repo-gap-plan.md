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

## Current Structural Readback

本 active plan 不冻结 OPL/MAG commit、digest、测试计数、numstat、review 结果或 worktree closeout。结构 currentness 由 `contracts/runtime-program/current-program.json`、`contracts/standard_agent_conformance_profile.json`、`contracts/source_closure_audit.json`、repo source/tests，以及 fresh MAG `./scripts/verify.sh` 和 OPL `agents scaffold|interfaces|source-closure|conformance --json` readback共同决定。

2026-07-11 的 Contract V2 snapshot、V1 allowed-match 清单、tests-only consolidation 与 absorption 明细已进入 [历史 closeout](../history/plans/2026-07-11-mag-structural-and-tests-closeout.md)，不能作为当前 SHA、ready 状态或新 backlog 读取。
