# Pending Authoring Route Handoff Matrix Current Truth

> 生命周期注记（`2026-05-25`）：这份 dated spec 已归档为 `historical_handoff_snapshot`，只保留 2026-04-12 pending authoring route handoff matrix。当前 `direction_screening -> frozen` authoring route 已由 2026-04-13 full authoring executor landing 接管；本文中的 Hermes/Gateway/pending wording 只作 provenance。

Owner: `Med Auto Grant`
Purpose: `historical_pending_authoring_route_handoff_snapshot`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 pending authoring route handoff matrix 与 `pending-handoff-requirements.schema.json` 的追溯背景。当前 authoring route catalog、executor routing schema/source、Codex CLI default executor 与机器行为以核心五件套、`docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

Date: `2026-04-13`

## Activation Status

- Phase: `Upstream Hermes-Agent Fast Cutover`
- Active tranche: `Pending authoring route handoff matrix`
- Status: `historical snapshot / superseded on 2026-04-13`

## Superseded Note

这份文档保留的是 `2026-04-12` 当天仍存在 pending authoring route 时的 handoff matrix 快照。

自 `2026-04-13` full authoring executor landing 起，当前主线已经把 `direction_screening -> frozen` 全部提升为 landed command，因此这份 matrix 只再承担两层意义：

- 历史迁移说明
- `pending-handoff-requirements.schema.json` 的兼容追溯背景

当前 authoring 主线真相请以：

- [docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md](../../specs/2026-04-13-full-grant-authoring-executor-current-truth.md)

为准。

Post-2026-05 reading guard:

- The pending matrix below is historical; current `direction_screening -> frozen` routes are landed service-safe commands.
- Historical `summarize-workspace`, `stage-route-report` and `critique-summary` surface names map through the current grouped CLI as `workspace summarize`, `workspace route-report` and `workspace critique-summary` when used by operators.
- Historical Hermes / Gateway / pending handoff wording must not be read as current runtime owner, default executor owner, compatibility interface, App readiness or production readiness.

## Goal

在已经 landed 的：

- `CLI-first + real upstream Hermes-Agent runtime substrate`
- `MedAutoGrantDomainEntry`
- lightweight `product entry` shell
- author-side executor routing contract

之上，把所有还没有 landed executor 的 authoring route 冻成 route-specific、machine-readable 的 `handoff_requirements`，让 future `OPL` / gateway / Hermes collaborator 可以直接协作，而不是继续脑补新的 repo-local executor。

## Landed Facts

### 1. pending handoff matrix 现在不再包含 critique

当前下面这些 pending authoring route 都会带 `handoff_requirements`：

- `direction_screening`
- `question_refinement`
- `argument_building`
- `fit_alignment`
- `outline`
- `drafting`
- `frozen`

已 landed 的 route 继续保持：

- `critique`
- `revision`
- `artifact_bundle`
- `final_package`
- `hosted_contract_bundle`

### 2. handoff matrix 只引用已经存在的 domain surfaces

pending route 合同没有引入新的 surface。
当前只允许复用：

- `summarize-workspace`
- `stage-route-report`
- `critique-summary`

其中：

- `summarize-workspace` 与 `stage-route-report` 是所有 pending route 的基础 surface
- `critique-summary` 只在 source workspace 已经进入 review context 时才会被要求
  - 即 source stage 属于 `critique / revision / frozen`

### 3. review-context pending route 继续按真实上下文 fail-closed

当前已经明确区分：

- `drafting` 这类 pre-review pending route
  - 只能要求：
    - `summarize-workspace`
    - `stage-route-report`
  - 不能错误要求 `critique-summary`
- `frozen` 或其他 review-context pending route
  - 可以继续要求：
    - `summarize-workspace`
    - `critique-summary`
    - `stage-route-report`

### 4. 每条 pending route 现在还会显式声明最小字段要求

当前 `handoff_requirements` 至少包含：

- `contract_kind`
- `workspace_surface_kind`
- `required_domain_surfaces`
- `required_identity_fields`
- `required_summary_fields`
- `required_gate_fields`

其中：

- `required_summary_fields` 只引用 `summarize-workspace` 已存在的字段路径
- `required_gate_fields` 只引用 `summarize-workspace.gates.*`
- `required_identity_fields` 会按 source stage 决定是否还必须保留 `draft_id`

### 5. `author_side_route_catalog` 现在是完整 authoring matrix

`build-product-entry.product_entry.executor_routing_contract.author_side_route_catalog` 当前已经不再只是：

- `critique + revision + export routes`

而是完整列出：

- 所有 pending authoring route
- 所有 landed revision / export routes

这样 `OPL` 或 future gateway caller 不需要先猜“哪些 route 其实还没冻结”。

## What Did Not Change

- `Hermes-Agent` 仍然只代表 runtime substrate / orchestration owner
- `Med Auto Grant` 仍然持有 grant object boundary 与 author-side route truth
- 这条 matrix 不是在宣称任何 remaining pending route 已经 landed executor
- `critique` 已经被提升到 landed route，因此不再属于这条 pending matrix
- 不新增新的 repo-local helper family
- 不扩 `Human-in-the-loop` sibling / family expansion / federation story

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_hermes_runtime.py tests/test_product_entry.py -q`

并验证：

- `drafting` current-stage route 现在也会带 route-specific `handoff_requirements`
- review-context pending route 继续会在需要时要求 `critique-summary`
- `author_side_route_catalog` 会列出完整 route matrix
- `frozen` current-stage route 也会带 route-specific `handoff_requirements`

## Honest Boundary

这条 current truth 只说明：

- pending authoring route handoff matrix 已经冻结成 machine-readable contract
- future caller 现在可以围绕真实 domain surfaces 直接协作

它不意味着：

- 这些 pending route 已经拥有 landed executor
- `critique` 仍然属于 pending route
- 更成熟的 product UX 已经完成
- actual hosted runtime 已完成
