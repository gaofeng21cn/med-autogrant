# Full Grant Authoring Executor

Owner: `Med Auto Grant`
Purpose: `full_authoring_route_executor_support_record`
State: `support_current_truth`
Machine boundary: 本文解释 authoring route 与 executor 分工；机器真相归 source、schemas、contracts 和 `contracts/runtime-program/current-program.json`。

## Route Catalog

Authoring route 从方向判断推进到最终 package：

| Route | Command |
| --- | --- |
| `direction_screening` | `execute-strategy-authoring-pass` 或 `execute-direction-screening-pass` |
| `question_refinement` | `execute-question-refinement-pass` |
| `argument_building` | `execute-argument-building-pass` |
| `fit_alignment` | `execute-fit-alignment-pass` |
| `outline` | `execute-outline-pass` |
| `drafting` | `execute-drafting-pass` |
| `critique` | `execute-critique-pass` |
| `revision` | `execute-revision-pass` |
| `frozen` | `execute-freeze-pass` |
| `artifact_bundle` | `build-artifact-bundle` |
| `final_package` | `build-final-package` |
| `hosted_contract_bundle` | `build-hosted-contract-bundle` |

`execute-strategy-authoring-pass` 是前半程默认入口：Codex 在一个 attempt 中共同收敛 direction、question、argument、fit、outline 和 draft，再由 deterministic projection 物化六个 schema-backed checkpoint。原子 pass 用于定点 route-back 和诊断。

## Data Invalidation

上游对象改变时，下游对象和引用随之失效：

- direction 变化使 question、argument、fit、draft、critique、revision 失效；
- question 变化使 argument、fit、draft、critique、revision 失效；
- argument 变化使 fit、draft、critique、revision 失效；
- fit 变化使 draft、critique、revision 失效；
- draft 变化使 critique、revision 失效。

Executor 同步移除 `preliminary_evidence_pack.evidence_items[].supports` 中指向失效对象的引用，避免悬挂 ID。

## Executor Boundary

- Strategy、drafting 与 critique 默认通过 OPL executor client 调用 `codex_cli`。
- Revision handler 应用已明确的局部或 whole-draft mutation。
- Freeze pass 负责 deterministic domain freeze。
- Model invocation 数量是 telemetry；retry、review feedback 和 route-back 可以产生后续 invocation。

## Verification

- `./scripts/run-pytest-clean.sh tests/test_authoring_executor.py -q`
- `./scripts/run-pytest-clean.sh tests/test_domain_entry.py tests/product_entry_cases tests/test_domain_runtime.py tests/test_hosted_contract_bundle.py -q`
- `./scripts/verify.sh`
