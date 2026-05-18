# P5.A Second Grant Family Onboarding Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-08`

## Activation Status

- Future phase: `P5 / Grant Ops Gateway Expansion And Federation`
- Future tranche: `P5.A / Second Grant Family Onboarding`
- Status: `pre-frozen / not activated`
- Upstream prerequisite: `P4 / Verification OS And HITL Layering Preparation` 必须先完整 absorbed；当前 repo pointer 仍可合法停在 `P4.B / Verification OS And Checkpoint Surface`

## Goal

在不改写当前 `CLI` formal entry、不把 `MCP / controller` 写成已支持 public runtime、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把当前 author-side mainline 改成 reviewer / HITL / submission-grade 产品的前提下，为一个非 `NSFC` 的第二 `grant family` 预冻结 onboarding activation package。

`P5.A` 当前冻结的不是“已经接入第二 family”的事实，而是：

- 第二 family onboarding 必须具备什么 admission package
- 哪些 repo-tracked / local durable surfaces 必须一起改
- 进入实现与 promotion 前必须满足哪些 verification、excluded scope 与 invariants

## Hard Boundary Docs

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`

## Admission Package Boundary

`P5.A` 预冻结的最小 onboarding 单元是 `SecondGrantFamilyAdmissionPackage`。它是 control-surface / review-surface 包，不是新的 runtime identity，也不是新的 public API。

它至少必须包含：

1. 一份 repo-tracked 的 second-family source packet，能够说明该 family 的 author-side 输入约束、核心表单结构、关键 gate 与正式来源
2. 一份 repo-tracked 的 family profile / current-truth 文档，明确该 family 与现有 `NSFCWorkspace` 主线的复用边界、差异边界与禁止推断的范围
3. 至少一个 repo-tracked 的该 family 最小 workspace/example 输入面
4. 对 active `test-spec` 的精确命令补充，覆盖该 family 的 canonical CLI verification
5. 与 `.runtime-program/context/**`、`.runtime-program/plans/**`、`.runtime-program/reports/**` 同步的 pointer / report / audit 变更

没有完整 `SecondGrantFamilyAdmissionPackage`，不得把任何 second family 写成 admitted、supported、ready for federation。

## Canonical Durable Surface

`P5.A` 一旦被激活并进入实现，允许写入的 canonical durable surface 只限：

- repo-tracked review surfaces
  - 一个 second-family source packet
  - 一个 second-family family profile / current-truth 文档
  - 至少一个 second-family example workspace
  - 必要时的 schema 文档或 schema 文件最小增量
- local durable handoff surfaces
  - `CURRENT_PROGRAM.md`
  - active `PRD / test-spec / implementation`
  - `LATEST_STATUS.md`
  - `ITERATION_LOG.md`
  - `OPEN_ISSUES.md`

当前 canonical CLI surfaces 仍只允许沿用：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`

`P5.A` 不授权新增 public CLI command，也不授权把 second family onboarding 包混写成 `controller` 或 `MCP` capability。

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许从 `P4` 进入 `P5.A` 之前，必须同时满足：

1. `P4` 已完整 absorbed，且当前 repo-tracked hard gate 继续全绿
2. active `PRD / test-spec / implementation`、`CURRENT_PROGRAM` 与 reports 已显式引用本 activation package
3. `SecondGrantFamilyAdmissionPackage` 的 object boundary、required artifacts、excluded scope 与 promotion invariants 已写入 repo-tracked 文档
4. `tests/test_program_control_surfaces.py` 已对本 activation package 的存在性与控制面对齐做出断言

### Implementation Promotion Gate

当 `P5.A` 真正进入实现时，必须补齐并通过：

1. `python3 -m unittest discover -s tests -p 'test_*.py'`
2. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
3. 当前 `NSFC` 主线的 canonical CLI examples 继续全绿
4. 基于 admitted second-family example 的精确 CLI 命令集，至少覆盖：
   - `validate-workspace`
   - `summarize-workspace`
   - `next-step`
   - 如该 family 已进入 critique / revision 语义，再追加 `critique-summary` 与 `stage-route-report`
5. `git diff --check`

如果第 4 项还不能写成精确命令，是因为 admitted source packet 仍不存在；此时不得激活 `P5.A`。

## Promotion Invariants

- formal entry 继续固定为 `CLI-first`
- `MCP` 仍只是 supported future protocol layer，`controller` 仍只是 internal control surface
- `grant_run_id / workspace_id / draft_id / program_id` 四个身份边界不得塌缩
- absorbed `P3.B / P3.C / P4.A / P4.B` 的 retained contracts 不得被 second family 覆盖或弱化
- second family onboarding 必须基于 repo-tracked source packet，不允许靠启发式猜测 family 规则
- 如需新增 schema 字段，必须由 source packet 直接支撑，并且不得破坏现有 `NSFC` examples 与 tests
- `P5.A` 只解决“第二 family admitted and runnable”问题，不得偷跑 federation、web runtime、submission-grade autopilot

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `P5.A` implementation：

1. `P4` 已 absorbed，且 `CURRENT_PROGRAM`、active plans、reports 的 pointer 已收口到可继续状态
2. 仓内已经存在一个可引用、可审阅、可验证的 second-family source packet
3. 该 family 仍属于 author-side、proposal-facing、grant authoring 范围
4. 继续推进不需要新增 public formal entry、remote runtime、reviewer-owned surface 或同仓 `Human-in-the-loop`

## Stop Conditions

若出现以下任一情况，必须停车：

- 没有 repo-tracked second-family source packet
- 需要靠启发式推断 second family 的字段、gate、route 或 artifact
- 需要同时引入两个以上新 family 才能让设计成立
- 需要把 `MCP / controller`、web runtime、reviewer / HITL surface 写成当前已支持范围
- 需要为了 second family 改写 `grant_run_id / workspace_id / draft_id / program_id` 边界

## Excluded Scope

- `Grant Foundry` federation contract
- top-level gateway routing
- web runtime / hosted credits / remote execution
- same-repo `Human-in-the-loop`
- reviewer-owned surface
- submission-grade autopilot
- 一次性接入多个 second family
- 无 source packet 的 schema 扩张
