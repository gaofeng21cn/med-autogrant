# MAG Active Truth：外部 Owner Evidence Tail

Owner: `Med Auto Grant`
Purpose: `single_active_truth_plan`
State: `active_evidence_tail`
Machine boundary: 本文只维护当前人读摘要、仍开放的 evidence gap 和下一轮执行入口。结构、源码、运行、包与 owner 真相分别归 current-program、root contracts、source/tests、OPL readback、runtime receipts、workspace artifacts 与 MAG owner receipts。

## Current State Summary

- MAG 当前形态是 Declarative Grant Pack、OPL generated/hosted surfaces 与最小 MAG authority functions。
- `contracts/runtime-program/current-program.json` 将结构阶段声明为 `structural_cleanup_closed`，当前 tranche 是 `external_owner_evidence_gated`。
- 已关闭结构工作的详细过程不在 active 层维护；历史入口是 [2026-07-11 结构与测试 closeout](../history/plans/2026-07-11-mag-structural-and-tests-closeout.md) 和 Git history。
- 当前没有选中的 repo-local 功能或结构 gap。只有真实 runtime、human gate、quality/export、持续消费、long-soak 与 owner acceptance evidence 仍开放。
- 因此不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。

## Current-State vs Ideal-State Gaps

| Gap | Current state | Required evidence | Truth owner / route |
| --- | --- | --- | --- |
| OPL-hosted grant attempts | `owner_evidence_required` | same-identity StageRun/Attempt 与 runtime receipt refs | OPL runtime owner + MAG stage owner |
| Submission human gate | `owner_evidence_required` | 真实 human-gate receipt 和 accepted owner answer | MAG submission owner / human owner |
| Quality and export | `owner_evidence_required` | fresh independent review、MAG quality/export verdict 与 exact artifact refs | MAG quality/export authority |
| Sustained default-caller consumption | `owner_evidence_required` | App/operator consumption 与 no-regression readback | App/operator owner + MAG owner |
| Provider long soak and production acceptance | `owner_evidence_required` | restart/retry/dead-letter/long-soak evidence、owner receipt 或 typed blocker | OPL provider owner + MAG production owner |

这些 gap 不能通过新增 wrapper、snapshot、read model、文档、focused tests、schema completeness、package existence 或 conformance pass 关闭。若没有新的 owner/live evidence，本计划保持薄状态，不生成替代 backlog。

## Structural Readback

结构 currentness 不在本文冻结 commit、digest、测试数量、source graph counters 或 worktree closeout。需要判断当前结构时，直接读取：

- `contracts/runtime-program/current-program.json`
- `contracts/functional_privatization_audit.json`
- `contracts/private_functional_surface_policy.json`
- `contracts/source_closure_audit.json`
- `contracts/standard_agent_conformance_profile.json`
- repo source/tests 与 fresh `./scripts/verify.sh`
- OPL `agents scaffold|interfaces|source-closure|conformance --json` readback

私有面与 retained authority 的人读导航见 [私有面 owner map](./opl-private-implementation-migration-inventory.md)。它只路由到 machine owners，不复制 path inventory 或 scanner count。

## Next-Round Agent Prompt

Owner: `Med Auto Grant`

Objective: 只在出现新的 external owner/live evidence 时，选择一个能改变上表状态的单一 evidence lane；验证 exact refs、owner authority 与 false-ready boundary，并把结果折回对应 machine/owner surface。

Trigger: 新的 StageRun/Attempt receipt、human-gate answer、quality/export verdict、持续 App/operator readback、provider long-soak evidence、owner receipt、typed blocker 或 route-back ref。

Write scope: 只有在 MAG owner authority 与 exact evidence refs 已确认时，才可更新 `contracts/live_stage_run_progress_evidence.json`、`contracts/production_acceptance/mag-production-acceptance.json`、本计划的对应 gap 行，以及直接受影响的 `docs/status.md` 或索引指针。OPL runtime、App/operator 与 human-owned evidence 只作为只读输入，必须由各自 owner lane 写入。

Non-goals: 不为制造进展而新增 MAG-local runtime、projection、compiler、queue、scheduler、session 或 package lifecycle；不恢复已退役接口、旧调用路线或转接层；不改写不属于 MAG 的 runtime、release、App/operator 或 human authority。

Live truth inputs: current-program、live progress、production acceptance、owner receipt contract、exact workspace/artifact refs、OPL runtime readback 和当前 lane 的 owner evidence。

Required actions: 验证 evidence 与同一 StageRun/Attempt、workspace、artifact 和 owner identity 绑定；确认该 evidence 只能关闭一个现有 gap；先更新对应 machine/owner surface，再删除或重写本计划中的已关闭 gap；把执行流水和一次性计数留在 receipt、history 或 Git history。

Verification commands: 运行 lane-specific owner validator 和 `./scripts/verify.sh`；结构 claim 变化时，另运行 OPL `agents scaffold --validate`、`agents interfaces`、`agents source-closure` 与 isolated `agents conformance --json`。只按实际证据层报告结果。

Stop condition: 没有新的 owner/live evidence，owner 或 currentness 不明，写集冲突，exact refs 不完整，或验证不能在 final bytes 上运行时停止；保留 blocker、owner、合法入口与重新进入条件，不做 fallback edit。

Completion gate: exact owner evidence 已落到 canonical machine/owner surface，受影响 gap 已删除或重写，过程材料未进入 active 层，最终 `main` 字节验证通过。只完成一次文档或 focused-test 更新不能关闭 evidence gap。

Foldback target: durable current fact 折回 `docs/status.md`；当前 gap 和下一轮执行入口只保留在本文；一次性执行流水进入 receipt、`docs/history/**` 或 Git history。

## Coverage Boundary

- 本文覆盖当前摘要、外部 evidence gaps 与下一轮执行 baton。
- durable current status owner 是 `docs/status.md`；north-star 是 `docs/references/med-auto-grant-ideal-state.md`；本文持有当前摘要、外部 evidence gap 与下一轮执行 baton。
- 私有面机器分类归 root contracts；历史完成过程归 `docs/history/**` 与 Git history。
- paper/grant 内容、质量、export、submission、owner acceptance 与 production readiness 始终由对应 MAG/human owner surface 决定。
