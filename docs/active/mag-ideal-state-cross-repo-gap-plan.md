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
| 3 | 消除 domain command catalog 双重真相 | done | 100% | contract、CLI 与 dispatch 由 service-safe command catalog派生 |
| 4 | 删除重复 hosted bundle payload builder | done | 100% | payload construction只有一个 owner；runtime仅组装和校验 |
| 5 | 删除 compatibility re-export、alias、wrapper 与退休 helper | done | 100% | patch bridge、private facade和 compatibility alias已退役 |
| 6 | 合并重复 index/dedupe/count helpers到标准库 | done | 100% | index owner唯一；dedupe使用 `dict.fromkeys`；计数使用 `Counter` |
| 7 | 删除 editable bootstrap与 import-time path injection | done | 100% | 依赖由 `uv`/package config管理；repo source不再注入路径 |
| 8 | 移除 ProductEntry/DomainRuntime 单实现 mixin树 | done | 100% | ProductEntry/MRO实现细节面退役；保留直接 `MagDomainRuntime` |
| 9 | 由 registry驱动 CLI parser与dispatch | done | 100% | command specs、field arguments与统一 handlers为当前 owner |
| 10 | 删除 runtime consumer-thinning/functional-closure自审计层 | done | 100% | OPL conformance/CI持有静态审计；MAG runtime不再投影自审计产品面 |
| 11 | 删除 MAG 私有 product/status/user-loop/runtime/workbench平台面 | done | 100% | direct domain handler + OPL generated/hosted handoff |
| 12 | 删除私有 OPL pack compiler与tracked generated aggregate | done | 100% | `agent/`/root contracts是声明源；OPL Pack生成 family stage plane |
| 13 | 将 cycle/rollback/resume/dispatch/output编排迁入 OPL StageRun | done | 100% | MAG只保留 selector、quality、transition oracle与 authority receipt |

结构规划完成度：`13/13 done`。这只证明源码、contracts、docs与结构边界已经收口，不证明运行态 ready。

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

- OPL canonical：`104a36d7a50aec237ec6e2340e445f093d4e9184`；local、`origin/main` 与 SSH443 `refs/heads/main` 一致。
- OPL conformance：`status=passed`、`matched_source_behavior_count=0`、`blockers=[]`、`allowed_source_behavior_count=10`、`unclassified_generic_behavior_count=0`、`active_private_generic_residue_count=0`。
- OPL route/Runway：action route与 refs-only `domain_output` ABI已进入 canonical main；真实 OMA create -> fixture-run -> query保留 selected action/route、object metadata与 output ref，OPL不读取 domain output body。
- OPL full residual：唯一 `system-seed-manifest` 失败在 candidate/base均为相同 `10/11` 与 `2 != 0`，不属于 MAG/Runway候选回归；其余 focused、MAG integration、smoke与静态门通过。
- Shared consumer dependency pin保持 `e1e734031ab3ea45596c6ce131f611f296ca9746`。
- MAG production closeout candidate：descriptor contract通过；CLI smoke `8 passed`；fast `124 passed + 60 subtests`；meta `36 passed`；full `235 passed + 177 subtests`。

Allowed matches：

| Path | Signature | Classification |
| --- | --- | --- |
| `src/med_autogrant/codex_cli.py` | `repo_owned_codex_executor_envelope` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_handler.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_handler_contract.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_handler_dispatch.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/domain_memory_runtime.py` | `repo_owned_product_status_session_shell` | `memory_accept_reject / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/domain_memory_runtime.py` | `repo_owned_receipt_observability_shell` | `memory_accept_reject / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/owner_receipt_common.py` | `repo_owned_product_status_session_shell` | `owner_receipt_signer / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/owner_receipt_writers.py` | `repo_owned_product_status_session_shell` | `owner_receipt_signer / minimal_authority_function` |
| `src/med_autogrant/product_entry_parts/primitives.py` | `repo_owned_product_status_session_shell` | `grant_native_helper / refs_only_domain_adapter` |
| `src/med_autogrant/product_entry_parts/typed_blocker_projection.py` | `repo_owned_product_status_session_shell` | `owner_receipt_signer / minimal_authority_function` |

MAG production SHA、tests-only replay分账与最终 worktree cleanup在本生产 closeout提交发布并吸收 tests-only候选后追加。最终 canonical SHA由Git readback给出，不在自身提交内容中自引用。
