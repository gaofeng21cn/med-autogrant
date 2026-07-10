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
| CLI/bootstrap/alias/proof lane cleanup | done | 100% | `medautogrant` only、clean runner、CLI smoke |
| Tests 去实现细节/快照绑定 | done | 100% | focused suites + collect/full gate |
| OPL structural/source behavior | done | 100% | latest OPL scanner: overall pass, matched 0, blockers 0 |
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
- Consumer dependency pin保持 release cohort commit；OPL conformance检查使用当时 latest OPL main。
