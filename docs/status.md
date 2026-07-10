# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相归 current-program、root contracts、source、CLI/API behavior、live progress、runtime receipts 与 workspace/artifact outputs。

## 结论

MAG 已完成 private OPL platform cleanup 的结构收口：私有 standard-pack/compiler、consumer-thinning/self-audit mesh、generic autonomy scheduler、product/status/user-loop/runtime shell、旧 evidence snapshots、editable bootstrap、`mag` console alias 和无 caller receipt/lifecycle wrapper 已退役。

当前 repo-local 程序面是：

- Declarative Grant Pack
- `medautogrant` CLI / `MedAutoGrantDomainEntry`
- direct domain handler 3 actions
- 八项 minimal MAG authority functions
- schema-backed grant authoring/package behavior

OPL/App 负责 generated product/status/user-loop/workbench caller。

## Machine State

| Surface | Current owner/readback | 状态 |
| --- | --- | --- |
| Current program | `contracts/runtime-program/current-program.json` | 3 handler actions、8 authority IDs |
| Agent pack | root contracts + `agent/` | declarative, OPL consumable |
| Source behavior | OPL conformance scanner | stop condition: matched 0, blockers 0 |
| Owner receipt | `contracts/owner_receipt_contract.json` | 3 canonical receipt classes |
| Production acceptance | `contracts/production_acceptance/mag-production-acceptance.json` | provenance only, typed blocker open |
| Live progress | `contracts/live_stage_run_progress_evidence.json` | owner blocker recorded, no ready claim |

## 已退役

- MAG-owned pack compiler、source scanner 与 generated aggregate checker
- private product entry/status/progress/cockpit/user-loop/workbench builders
- generic scheduler/daemon/queue/attempt-ledger/session/lifecycle shells
- stale production/consumer snapshots and patch/worktree closeout ledgers
- compatibility console alias、editable dependency bootstrap、proof-only lane
- implementation-bound and snapshot-bound tests

这些内容不再作为 current source、active contract 或 active docs 入口。历史只能从 `docs/history/**` 或 git history 读取。

## 仍开放的 Evidence Gate

- 真实 OPL-hosted grant stage attempts
- submission human-gate receipt
- real quality/export receipt
- sustained App/operator/default-caller consumption
- provider long-soak evidence
- owner acceptance或 production success/no-regression evidence

因此当前不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。

## Skill 与安装

`agent/primary_skill/SKILL.md` 是 canonical source；`plugins/med-autogrant/skills/med-autogrant/SKILL.md` 是 byte-identical materialized carrier。Canonical agent id 是 `mag`，安装 locator/skill name 是 `med-autogrant`；两者不是兼容 alias 关系。

## 验证入口

- `./scripts/verify.sh`
- `./scripts/verify.sh full`
- `make test-descriptor-contracts`
- OPL: `./bin/opl agents conformance --agent mag=<repo> --json`

测试通过和 structural conformance 只证明对应 gate 通过，不提升 readiness。
