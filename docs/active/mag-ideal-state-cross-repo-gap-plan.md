# MAG 外部 Owner Evidence

Owner: `Med Auto Grant`
Purpose: `active_external_evidence_gaps`
State: `active_evidence_tail`
Machine boundary: 本文是当前证据缺口索引。机器状态归 root contracts、runtime receipts、workspace artifacts 与 owner receipts。

## 当前状态

MAG 当前由 Declarative Grant Pack、OPL generated/hosted surfaces 和最小 MAG authority functions 组成。仓内结构清理已经关闭，`contracts/runtime-program/current-program.json` 的当前 tranche 是 `external_owner_evidence_gated`。

Stage repair 与 Meta Review route-back 预算由 `contracts/stage_quality_cycle_policy.json` 声明，由 OPL StageRun 执行并回读。当前仓库没有待实现的本地结构 gap。

## 开放证据

| Evidence lane | 需要的证据 | Owner |
| --- | --- | --- |
| OPL-hosted grant attempts | 同一身份的 StageRun/Attempt 与 runtime receipt refs | OPL runtime + MAG stage owner |
| Submission human gate | 人工决定回执与 accepted owner answer | MAG submission + human owner |
| Quality and export | fresh independent review、MAG verdict 与 exact artifact refs | MAG quality/export owner |
| Sustained consumption | App/operator default-caller readback 与 no-regression evidence | App/operator + MAG owner |
| Production operation | restart/retry/dead-letter/long-soak evidence与 owner answer | OPL provider + MAG production owner |

这些证据到位前，当前状态保持为未完成对应的 grant、quality、export、submission 或 production readiness。

## 更新路径

新的 owner evidence 到达后：

1. 校验 StageRun/Attempt、workspace、artifact 与 owner identity。
2. 更新对应 owner surface：`contracts/live_stage_run_progress_evidence.json` 或 `contracts/production_acceptance/mag-production-acceptance.json`。
3. 同步本表与 `docs/status.md` 中直接受影响的状态。
4. 运行 lane-specific validator、`./scripts/verify.sh` 和相关 OPL readback。

跨仓 Package 组合迁移的阶段、顺序和验收由 App 的 [总体迁移 SSOT](https://github.com/gaofeng21cn/one-person-lab-app/blob/main/docs/active/opl-package-platform-composition-migration.md) 持有。

## 结构回读

- `./scripts/verify.sh`
- `./scripts/verify.sh full`
- OPL `agents scaffold --validate`
- OPL `agents interfaces`
- OPL `agents source-closure`
- OPL `agents conformance --json`

结构验证只回答结构与接口问题；live readiness 仍以上表的 owner evidence 为准。
