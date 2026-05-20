# Full Grant Authoring Executor Current Truth

> 生命周期注记（`2026-05-20`）：这份 dated spec 留在 `docs/specs/` 仅作为 `support_current_truth`，只在 landed authoring route catalog 与默认 `Codex CLI` executor vocabulary 仍由当前 contracts/schema/source 支撑的 subsection 内有效。当前 public identity、runtime owner、App/workbench、production evidence 和 grant readiness 结论回到核心五件套、active plan 与 `contracts/runtime-program/current-program.json`。

Date: `2026-04-13`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.D full grant authoring executor landing`
- Status: `support_current_truth_by_subsection`

## Goal

把此前只在 route matrix 里冻结、仍被写成 `pending / handoff-required` 的前半程 authoring route，全部收口成可执行、可验证、可审计的 landed service-safe command surface，并保持以下边界不变：

- `Codex CLI` 继续是默认 concrete executor
- `Hermes-Agent` 只作为显式 OPL receipt/proof lane，不持有默认 runtime、authoring executor、grant truth 或 quality verdict
- `Med Auto Grant` 继续持有 grant domain truth、author-side route 与导出物 owner
- `grant-user-loop` / `build-product-entry` / hosted bundle 继续只投影和导出 route truth，不发明新的产品层 executor

## Landed Facts

### 1. `direction_screening -> frozen` 现在已经形成完整 landed route catalog

当前 route contract / product entry / hosted contract bundle 共享的 landed command catalog 现在至少包括：

- `direction_screening -> execute-direction-screening-pass`
- `question_refinement -> execute-question-refinement-pass`
- `argument_building -> execute-argument-building-pass`
- `fit_alignment -> execute-fit-alignment-pass`
- `outline -> execute-outline-pass`
- `drafting -> execute-drafting-pass`
- `critique -> execute-critique-pass`
- `revision -> execute-revision-pass`
- `frozen -> execute-freeze-pass`
- `artifact_bundle -> build-artifact-bundle`
- `final_package -> build-final-package`
- `hosted_contract_bundle -> build-hosted-contract-bundle`

这意味着：

- `executor_routing_contract.current_stage_route`
- `executor_routing_contract.recommended_executor_route`
- `author_side_route_catalog`
- `grant-user-loop.next_action`
- hosted bundle 内的 `authoring_contract`

现在看到的是同一份“全链 landed authoring executor truth”，而不是“前半程 pending、后半程 landed”的分裂口径。

### 2. `grant-user-loop` 现在对整条 authoring 主线直接投影 landed command

`grant-user-loop` 当前不再只对 `drafting -> critique` 给 landed command。

现在只要推荐 route 已经进入上述 landed catalog，`next_action` 就会直接返回：

- `action_kind = execute_landed_route`
- 对应的 `uv run python -m med_autogrant <command> ... --format json`
- `--output` 不再是 `<...-output-path>` 占位符，而是指向 `$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/<grant_run_id>/<workspace_id>/<draft_id-or-no-draft>/...` 的具体建议输出文件

因此从 `direction_screening` 开始，当前 direct grant user loop 就能一路把用户送到：

- 问题提纯
- 立项依据构建
- fit 对齐
- 提纲冻结
- 正文起草
- 导师批注
- 结构化修订
- 送审前冻结

### 3. 前半程 rerun 现在会显式清掉下游对象，并清理失效支持引用

当前 landed authoring executor 在改写上游对象后，会显式清掉不再可信的下游对象：

- 方向重筛后清空 question / argument / fit / draft / critique / revision
- 问题重塑后清空 argument / fit / draft / critique / revision
- 立项依据重建后清空 fit / draft / critique / revision
- fit 重建后清空 draft / critique / revision
- drafting 重跑后清空 critique / revision

除此之外，executor 现在还会同步清理 `preliminary_evidence_pack.evidence_items[].supports` 中已经失效的旧下游引用，避免 rerun 后留下悬挂的旧 `question_id / argument_chain_id / fit_mapping_id / draft_id`。

### 4. 当前执行器身份是“前半程 Codex CLI + 冻结 deterministic freeze”

当前 landed executor 的 concrete owner 是：

- `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique`
  - 默认 concrete executor：`Codex CLI`
  - `executor.kind = codex_cli`
  - `model / reasoning_effort` 默认继续继承本机 Codex 默认
- `revision`
  - 当前仍是 repo-side deterministic section-level revision contract
- `frozen`
  - 当前是 deterministic domain freeze pass

因此当前 landed 的是“完整可执行 route truth”，不是“所有单步都已经 Hermes-native”。

### 5. `pending_handoff_requirements` 已退出当前主线 route output

`product-status.schema.json` 继续只保留为历史兼容与旧真相追溯材料。

当前主线 route output 的真实口径已经是：

- full landed route catalog
- full service-safe command surface
- full user-loop landed command projection

## Verification

本 tranche 至少覆盖：

- `uv run pytest tests/test_authoring_executor.py -q`
- `uv run pytest tests/test_domain_entry.py tests/test_product_entry.py tests/test_domain_runtime.py tests/test_hosted_contract_bundle.py -q`
- `scripts/verify.sh`

重点验证：

- 前半程 executor 能产出合法 workspace
- landed route catalog 与 schema / product entry / hosted bundle 保持一致
- `grant-user-loop` 对前半程 route 直接投影带 runtime-state 输出路径的 landed command，而不是要求用户手填 output path 占位符
- rerun 后失效的下游对象与 `preliminary_evidence_pack.supports` 会被显式清理

## Honest Boundary

这条 current truth 只说明：

- `direction_screening -> frozen` 全链 authoring route 已 landed
- 当前 product loop、hosted bundle 与 route contract 已共享同一份 landed truth
- 当前执行器边界与失效清理规则已经冻结

它不意味着：

- mature direct grant Web UI / hosted runtime 已完成
- 旧 `OPL Gateway` landed wording 只保留为 provenance，不是 current owner line
- 所有 landed route 都已经自动变成 Hermes-native full agent loop
