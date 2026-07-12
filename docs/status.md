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

Stage contract 当前保持 6 个 top-level Stage，不做拆分。Stage Pack v2 的 manifest allow-list、action catalog 与 pack input parity 已由 contract test 固定；3 个 mutating action 声明 manifest 对齐的 ordered `stage_route`，2 个 read-only action 不声明执行 route。Manifest 的 5 条正常前进边均由 grant transition oracle 覆盖，全部 8 条合法 transition 各有唯一且 source-stage 对齐的 fixture。Human decision 使用 `completed_and_wait_owner` 与 `human_gate_ref`，普通 repair/rollback 使用 `route_back_ref`；typed blocker 只保留给真实语义或 authority 缺口。

OPL/App 负责 generated product/status/user-loop/workbench caller。

`contracts/standard_agent_conformance_profile.json` 现由 MAG 声明六阶段 ordinary golden path、唯一默认阶段 `call_and_candidate_intake`、12 项 physical morphology 分类，以及 generated default caller / OPL Python executor client / no-forbidden-write parity gates。OPL conformance 只通用读取该 profile，不再内置 MAG stage 或 morphology 分支。

当前结构阶段已关闭，`current-program` 为 `structural_cleanup_closed`。后续 tranche 只接收 external owner/live evidence，不再恢复 MAG 私有 runtime、projection、compiler 或 self-audit 平台面。

## Machine State

| Surface | Current owner/readback | 状态 |
| --- | --- | --- |
| Current program | `contracts/runtime-program/current-program.json` | 3 handler actions、8 authority IDs |
| Agent pack | root contracts + `agent/` | declarative, OPL consumable |
| Standard conformance profile | `contracts/standard_agent_conformance_profile.json` | MAG-owned golden path / morphology，OPL generic validator消费 |
| Foundry consumer + source behavior | OPL conformance scanner | thin consumer ABI passed；matched 0；blockers 0；allowed 9 |
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

## Structural Closeout

- Foundry consumer ABI基线：OPL `45eff07ab2a3db722c05cf64b50bab4597ac76c8`；`contracts/foundry_agent_series.json` 只保留 MAG identity/domain delta、canonical policy refs 和 `opl-generated:family_stage_control_plane` locator，不复制 OPL policy body。
- OPL StageRun 持有 cycle、rollback、resume、dispatch、attempt ledger 与 output orchestration；MAG 只返回 domain refs、verdict、typed blocker 与 owner receipt。
- Final source-behavior scanner：`status=passed`、`matched_source_behavior_count=0`、`blockers=[]`、`allowed_source_behavior_count=9`。
- Allowed matches只覆盖 typed executor closeout adapter、domain handler、memory accept/reject、owner receipt signer与 typed blocker projection；没有 repo-local executor transport、unclassified generic behavior或 active private generic residue。
- Framework Python helper 由 OPL 在 `opl_framework` namespace 托管；MAG manifest / lock 不声明或锁定 OPL implementation。
- MAG production base为 `3fd7cd3dc5bd3102ac8bf95b33a90a439b82e7fc`；tests-only consolidation `c755594d7a005176fab1e687de58f42a49ab0ece` 已线性吸收，严格只改 `tests/**`，净删 `1695` 行。
- Final tests boundary：`sys.path.insert` 为0，6个 retired owner tests未复活；fresh focused、smoke、fast、meta与full均为零失败，independent review `ACCEPT`。
- Tests replay与三个 superseded tests clones已完成 absorption audit并清理；无关 `stage-size-mag` lane继续保留。

## 仍开放的 Evidence Gate

- 真实 OPL-hosted grant stage attempts
- submission human-gate receipt
- real quality/export receipt
- sustained App/operator/default-caller consumption
- provider long-soak evidence
- owner acceptance或 production success/no-regression evidence

因此当前不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。

## Skill 与安装

`agent/primary_skill/SKILL.md` 是 canonical source；`plugins/med-autogrant/skills/med-autogrant/SKILL.md` 是 byte-identical materialized carrier。Canonical agent id 与 OPL Agent Package id 都是 `mag`；安装 locator/skill name 是 `med-autogrant`，module/CLI locator 是 `medautogrant`。这些 locator 不形成兼容 alias 或第二个 package identity。

## 验证入口

- `./scripts/verify.sh`
- `./scripts/verify.sh full`
- `make test-descriptor-contracts`
- OPL: `./bin/opl agents conformance --agent mag=<repo> --json`

测试通过和 structural conformance 只证明对应 gate 通过，不提升 readiness。
