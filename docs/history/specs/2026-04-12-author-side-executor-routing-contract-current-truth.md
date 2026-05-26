# Author-Side Executor Routing Contract Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_author_side_executor_routing_snapshot`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-12 author-side executor routing contract 快照与 pending route 迁移语义。当前 route catalog、executor routing schema/source、Codex CLI default executor、OPL/Temporal runtime owner 与机器行为以核心五件套、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

Date: `2026-04-13`

## Activation Status

- Phase: `Upstream Hermes-Agent Fast Cutover`
- Active tranche: `Author-side executor routing contract`
- Status: `historical snapshot / superseded on 2026-04-13`

## Superseded Note

这份文档保留的是 `2026-04-12` 当天的 route contract 快照：当时 `critique / revision / export` 已 landed，而前半程 authoring route 仍在 `pending / handoff-required` matrix 中。

自 `2026-04-13` 起，当前主线真相已经切到：

- [docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md](../../specs/2026-04-13-full-grant-authoring-executor-current-truth.md)

也就是说，下面保留的是历史迁移语义，不再代表当前 landed route catalog。

Post-2026-05 reading guard:

- `runtime-run` / `runtime-resume` are retired runtime command vocabulary, not current public CLI or domain-entry commands.
- Historical bare commands such as `build-artifact-bundle` and `build-final-package` map through the current grouped CLI as `package artifact-bundle` and `package final-package` when used by operators.
- Current route catalog, executor defaults and hosted authoring contract are source / contract owned by `src/med_autogrant/public_cli.py`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/domain_entry_contract.py`, `src/med_autogrant/hosted_contract_bundle.py`, active specs and `contracts/runtime-program/current-program.json`.

## Goal

在已经 landed 的：

- `CLI-first + explicit upstream Hermes-Agent proof/provenance lane`
- `MedAutoGrantDomainEntry`
- lightweight `product entry` shell

之上，冻结一份 machine-readable `executor_routing_contract`，明确：

- `Codex CLI` 继续是默认 concrete executor
- `Hermes-Agent` 只作为显式 OPL receipt/proof lane，不持有默认 runtime、authoring executor、grant truth 或 quality verdict
- `Med Auto Grant` 继续持有 grant author-side route truth
- 哪些 executor route 已经 landed
- 哪些 route 已经是 landed command surface
- 当前 author-side route catalog 的 landed command truth

## Landed Facts

### 1. 两个现有 surface 现在共享同一份 routing contract

下面两个 surface 现在都会输出 `executor_routing_contract`：

- `runtime-run` 返回的 `stage_action_envelope`
- `build-product-entry` 返回的 `product_entry`

当前最小合同字段是：

- `contract_version`
- `current_stage_route`
- `recommended_executor_route`

其中 `build-product-entry` 还会额外导出：

- `author_side_route_catalog`

### 2. `current_stage_route` 与 `recommended_executor_route` 显式分开

这样做是为了避免把：

- 当前 workspace 所在 stage

和：

- 当前下一步真正应该调度的 executor route

混成一个字段。

例如对 `critique -> revision` 的 workspace：

- `current_stage_route.route_id = critique`
- `current_stage_route.route_status = landed`
- `current_stage_route.execution_surface.command = execute-critique-pass`

同时：

- `recommended_executor_route.route_id = revision`
- `recommended_executor_route.route_status = landed`
- `recommended_executor_route.execution_surface.command = execute-revision-pass`

而对 canonical 的：

- `revision(completed revised switch) -> critique`

返场路径：

- `current_stage_route.route_id = revision`
- `current_stage_route.route_status = landed`
- `recommended_executor_route.route_id = critique`
- `recommended_executor_route.route_status = landed`
- `recommended_executor_route.execution_surface.command = execute-critique-pass`

对 canonical 的：

- `drafting -> critique`

推荐路径同样已经固定为：

- `recommended_executor_route.route_id = critique`
- `recommended_executor_route.route_status = landed`
- `recommended_executor_route.execution_surface.command = execute-critique-pass`

### 3. 全部 author-side route 已经冻结为 landed route catalog

当前 `author_side_route_catalog` 的真实状态是：

- `direction_screening`
  - `route_status = landed`
  - `execution_surface.command = execute-direction-screening-pass`
- `question_refinement`
  - `route_status = landed`
  - `execution_surface.command = execute-question-refinement-pass`
- `argument_building`
  - `route_status = landed`
  - `execution_surface.command = execute-argument-building-pass`
- `fit_alignment`
  - `route_status = landed`
  - `execution_surface.command = execute-fit-alignment-pass`
- `outline`
  - `route_status = landed`
  - `execution_surface.command = execute-outline-pass`
- `drafting`
  - `route_status = landed`
  - `execution_surface.command = execute-drafting-pass`
- `critique`
  - `route_status = landed`
  - `execution_surface.command = execute-critique-pass`
  - `execution_surface.entry_adapter = MedAutoGrantDomainEntry`
  - 当前默认 concrete executor 是 `Codex CLI autonomous`
  - 默认 `model / reasoning` 都继承本机 Codex 默认（`inherit_local_codex_default`）
- `revision`
  - `route_status = landed`
  - `execution_surface.command = execute-revision-pass`
- `frozen`
  - `route_status = landed`
  - `execution_surface.command = execute-freeze-pass`
- `artifact_bundle`
  - `route_status = landed`
  - `execution_surface.command = build-artifact-bundle`
- `final_package`
  - `route_status = landed`
  - `execution_surface.command = build-final-package`
- `hosted_contract_bundle`
  - `route_status = landed`
  - `execution_surface.command = build-hosted-contract-bundle`

这些 landed route 现在统一通过：

- `surface_kind = service-safe-domain-entry-command`
- `entry_adapter = MedAutoGrantDomainEntry`

### 4. 非 landed stage 不再出现在当前主线 route truth

当前 route contract 只承认已经 repo-tracked、可直接调用的 landed command surface；历史 pending handoff matrix 已经退到 superseded 历史材料。

而不能因为 substrate 已统一，就自动被写成“已有 landed executor route”。

## What Did Not Change

- `Hermes-Agent` 仍然只代表 upstream external runtime / proof backend，可通过显式 OPL executor adapter 接入
- `domain_runtime.py` 仍然只是 repo-side domain adapter / orchestrator
- 这份 contract 不是在宣称 critique / revision / export 已经全部 Hermes-native
- `Hermes-native` 只有 full agent loop 才算；chat relay / 单次 chat completion 不算
- 不扩 `Human-in-the-loop` sibling
- 不扩新的 grant family
- 不展开 `P5` federation / platform story

## Verification

本 tranche 至少已覆盖：

- `uv run pytest tests/test_domain_runtime.py tests/test_product_entry.py tests/test_domain_entry.py tests/test_hosted_contract_bundle.py -q`

并验证：

- `stage_action_envelope` 会输出 `executor_routing_contract`
- `build-product-entry` 会输出 `executor_routing_contract`
- `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle` 都继续保持当前 landed surface
- `drafting -> critique` 与 `revision(completed revised switch) -> critique` 都会落到 `execute-critique-pass`
- 当前默认 `critique` executor 会显式继承本机 Codex 默认配置

## Honest Boundary

这条 current truth 只说明：

- author-side executor routing contract 已经冻结成 machine-readable surface
- 所有仍 pending 的 authoring route 现在都已具备 route-specific handoff semantics
- critique、revision 与 export 主线的 landed route 已经被显式列出

它不意味着：

- 这些 landed route 已经替换成 Hermes-native full agent loop
- drafting / frozen gate 已经拥有新的 executor surface
- product UX 已经成熟
- actual hosted runtime 已完成
