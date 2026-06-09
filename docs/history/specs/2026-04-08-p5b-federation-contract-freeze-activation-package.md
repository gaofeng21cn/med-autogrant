# P5.B Federation Contract Freeze Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_federation_contract_activation_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-08 P5.B federation contract freeze activation package 的预冻结边界。当前 admitted domain、federation/future expansion、gateway wording、OPL generated/hosted caller 与 runtime owner 以核心五件套、active gap plan、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准；本文不是 active P5 backlog、federation-ready claim 或 cross-domain runtime owner claim。

Date: `2026-04-08`

## Activation Status

- Future phase: `P5 / Grant Ops Gateway Expansion And Federation`
- Future tranche: `P5.B / Federation Contract Freeze`
- Status: `pre-frozen / not activated`
- Upstream prerequisite: `P5.A / Second Grant Family Onboarding` 必须先完成 admitted second family 的 absorb；没有稳定的多 family 边界，不得进入 federation contract freeze

## Goal

在 `CLI-first`、author-side、proposal-facing 当前真相不漂移的前提下，冻结 `Med Auto Grant` 作为 `Grant Foundry` / top-level gateway 医学节点所需的 federation contract。

`P5.B` 当前冻结的不是“联邦已经运行”，而是：

- 进入 federation freeze 前必须先具备哪些 admitted-domain 证据
- 哪些 handoff / audit / export / gate semantics 可以写成 repo-tracked contract
- 哪些内容仍然必须留在 future platform / web runtime / protocol layer

## Hard Boundary Docs

- `/Users/gaofeng/workspace/med-autogrant/docs/history/specs/README.md` 中的 Foundation / early mainline 压缩记录
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p5a-second-grant-family-onboarding-activation-package.md`

## Federation Contract Boundary

`P5.B` 预冻结的最小联邦单元是 `GrantOpsFederationContractPackage`。它仍然是 contract package，不是新的 runtime owner，也不是新的 public entry。

它至少必须明确：

1. `Med Auto Grant` 在 top-level gateway / `Grant Foundry` 中被 admitted 时所使用的 package identity 与 admissibility boundary
2. 哪些 domain artifacts 可以作为 handoff / export / audit surface
3. 哪些 gate semantics 仍由本仓内 domain mainline 保持 owner，哪些只允许作为 federation-facing summary / package metadata
4. admitted family 列表如何精确绑定，而不是模糊写成“支持多 family”
5. 哪些控制面与报告面需要在 absorb 后同步回写

没有稳定 `GrantOpsFederationContractPackage`，不得把本仓写成 federation-ready、gateway-ready、cross-domain runtime owner。

## Canonical Durable Surface

`P5.B` 一旦被激活并进入实现，允许写入的 canonical durable surface 只限：

- repo-tracked review surfaces
  - federation contract / gateway admission 文档
  - admitted family exact-set 文档
  - export / audit / gate summary 的 canonical surface 说明
  - 必要时的 examples / tests / contract current-truth 文档
- local durable handoff surfaces
  - `CURRENT_PROGRAM.md`
  - active `PRD / test-spec / implementation`
  - `LATEST_STATUS.md`
  - `ITERATION_LOG.md`
  - `OPEN_ISSUES.md`

当前 formal entry 与 runtime baseline 仍保持：

- default formal entry：`CLI`
- supported future protocol layer：`MCP`
- internal control surface：`controller`

`P5.B` 不授权把 federation contract 写成 remote runtime、web runtime、或跨仓统一执行内核已经落地的事实。

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许评估 `P5.B` 之前，必须同时满足：

1. `P5.A` 已 absorbed，且 admitted second family 的 repo-tracked truth 已稳定
2. active `PRD / test-spec / implementation`、`CURRENT_PROGRAM` 与 reports 已显式引用本 activation package
3. `GrantOpsFederationContractPackage` 的 boundary、required artifacts、excluded scope 与 promotion invariants 已写入 repo-tracked 文档
4. `tests/test_program_control_surfaces.py` 已对本 activation package 的存在性与控制面对齐做出断言

### Implementation Promotion Gate

当 `P5.B` 真正进入实现时，必须补齐并通过：

1. `python3 -m unittest discover -s tests -p 'test_*.py'`
2. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
3. admitted family exact-set 的 control-surface / contract tests
4. export / audit / gate summary 的结构化断言，确保它们是 precise package，不是自由文本口头说明
5. `git diff --check`

如果第 3 项或第 4 项仍无法写成精确断言，说明 admitted families 或 federation artifacts 还没有稳定；此时不得激活 `P5.B`。

## Promotion Invariants

- formal entry 继续固定为 `CLI-first`
- `MCP` 仍只是 supported future protocol layer；`controller` 仍只是 internal control surface
- federation 只冻结 contract / package / audit / gate semantics，不改变当前 runtime owner 事实
- admitted families exact-set 必须先稳定，才允许进入 federation contract freeze
- admitted family 必须是 exact-set，不允许“以及其他类似 family”式模糊表述
- handoff / export / audit surface 必须是结构化 package，不允许靠自由文本总结替代
- `grant_run_id / workspace_id / draft_id / program_id` 边界仍保持原义
- 不得把 `P5.B` 写成 unified web runtime、credit system、hosted SaaS、同仓 HITL 或跨仓统一执行内核已经落地

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `P5.B` implementation：

1. `P5.A` 已 absorbed，且本仓至少存在两个 admitted family 的稳定边界：`NSFC` + 一个 second family
2. top-level gateway / federation 所需的上游 truth 已经 repo-tracked，可被引用，而不是口头方向
3. 需要冻结的是 package / audit / gate / export contract，而不是新 runtime surface
4. 继续推进不需要改写当前 formal entry、durability 或 ID-boundary

## Stop Conditions

若出现以下任一情况，必须停车：

- `P5.A` 尚未 absorbed，或 second family 仍未稳定
- 上游 gateway / federation truth 不存在或不可引用
- 需要捏造 admitted package identity、gate summary 或 export semantics
- 需要把 federation contract 包装成 web runtime、remote MCP server、reviewer surface 或统一执行内核已落地
- 需要突破当前 CLI-first / Auto-only mainline 边界

## Excluded Scope

- web runtime / hosted runtime / credit system
- remote `MCP` server 落地
- `controller` public entry
- same-repo `Human-in-the-loop`
- reviewer-owned surface
- 统一平台 runtime 已实现的宣称
- 跨仓共享执行内核的代码抽取
- 没有 admitted family exact-set 的 federation-ready 口径
