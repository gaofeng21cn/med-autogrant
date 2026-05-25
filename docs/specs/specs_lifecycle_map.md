# Specs 生命周期地图

Status: `active_specs_governance`
Owner: `Med Auto Grant`
Purpose: `specs_lifecycle_map`
State: `current_index`
Machine boundary: 本文是人读生命周期索引。机器面必须使用 `contracts/runtime-program/current-program.json`、schemas、source files、CLI/API behavior 或语义化 `human_doc:*` id。

## 为什么保留这份地图

`docs/specs/` 只保留 current truth records、support current-truth records 和 integration references。纯历史 activation package、早期 P2/P3/P4 flow/verification tranche、R/P/post-R5A tranche、local-runtime closeout、fail-closed hardening note、future P5 记录和 superseded provider proof 已物理归档到 `docs/history/specs/`。

当前规则是 index-first 生命周期治理：

- 当 support specs 仍被 current-program、history 或旧审计证据引用时，可以继续留在 `docs/specs/`，但必须有明确 current subsection。
- 生命周期状态统一在本文和 `docs/specs/README.md` 标清。
- dated support specs 第一屏必须保留生命周期注记，避免 direct-file reader 把旧 `Current Truth` 标题误读成当前 owner line。
- 不再默认新增 dated root specs；只有明确被接纳为 current owner surface 的文件才进入 active specs。
- 纯历史 spec 一律进入 `docs/history/specs/`；不得为了旧审计路径稳定性在 current specs 层保留旧调用入口。

## Active Current Specs

这些记录仍由 docs guide 或 current status 直接链接，并定义特定 active boundary。它们只在第二列列出的边界内是 current；整体产品状态仍由核心文档和 `current-program.json` 持有。

| Spec | Active boundary |
| --- | --- |
| [Critique Codex CLI Executor Current Truth](./2026-04-13-critique-codex-cli-executor-current-truth.md) | critique executor vocabulary 与 Codex CLI route |
| [AI-first Quality Boundary Current Truth](./2026-04-27-ai-first-quality-boundary-current-truth.md) | AI-first quality ownership 与 projection boundary |
| [Authoring Completion Semantics Current Truth](./2026-04-23-authoring-completion-semantics-current-truth.md) | authoring completion semantics |
| [Quality Governance, Autonomy Controller, And Family Grammar Current Truth](./2026-04-22-quality-autonomy-family-grammar-current-truth.md) | quality governance、autonomy controller 与 family grammar |

## 文件级生命周期表

这张表是 dense specs set 的 direct-reader guard。active owner 或高风险单文件使用精确文件名；生命周期、owner 和下一跳一致的批次使用精确 filename family。纯历史文件位于 `docs/history/specs/`；current specs 层不再用 path stability 保留旧 activation package 或 fail-closed tranche。

| 文件或精确 family | 生命周期 | 当前 owner / replacement | 阅读动作 |
| --- | --- | --- | --- |
| `2026-04-13-critique-codex-cli-executor-current-truth.md` | `active_current_spec` | active spec + core docs | 只读 critique executor vocabulary 与 Codex CLI route。 |
| `2026-04-27-ai-first-quality-boundary-current-truth.md` | `active_current_spec` | active spec + quality owner docs | 只读 AI-first quality boundary。 |
| `2026-04-23-authoring-completion-semantics-current-truth.md` | `active_current_spec` | active spec + authoring completion owner docs | 只读 completion semantics。 |
| `2026-04-22-quality-autonomy-family-grammar-current-truth.md` | `active_current_spec` | active spec + current quality/autonomy docs | 只读 quality governance、autonomy controller 和 family grammar。 |
| `2026-04-07-formal-entry-matrix-current-truth.md` | `support_current_truth` | core five + `current-program.json` | 作为 formal-entry 支撑 guard 阅读；旧 runtime-run/resume、journal 和 attempt ledger 只能按 history/provenance 读。 |
| `2026-04-07-durability-model-clarification.md` | `support_current_truth` | architecture/status + runtime-state docs | 只读 durability boundary guard；不恢复 local journal、attempt ledger 或 MAG-owned generic runtime。 |
| `../history/specs/2026-04-07-p2a-*`, `../history/specs/2026-04-07-p2b-*`, `../history/specs/2026-04-07-p2c-*` | `historical_authoring_flow_provenance` | current authoring pass docs、route catalog、core docs | 只作为 P2 authoring-flow 形成历史阅读；当前 route truth 在 source/contracts。 |
| `../history/specs/2026-04-07-p3a-*`, `../history/specs/2026-04-08-p3b-*`, `../history/specs/2026-04-08-p3c-*` | `historical_review_gate_provenance` | current critique/revision and quality docs | 只作为 mentor/review/rollback 历史阅读；不要恢复 phase backlog。 |
| `../history/specs/2026-04-08-p4a-*`, `../history/specs/2026-04-08-p4b-*` | `historical_verification_gate_provenance` | current verification scripts、route checkpoint source、core docs | 只读 verification gate / checkpoint 形成历史；当前验证口径在 scripts/source/contracts。 |
| `2026-04-12-p4a-*`, `2026-04-12-p4b-*`, `2026-04-12-p4c-*`, `2026-04-13-p4e-*`, `2026-04-13-p4f-*` | `support_current_truth` | product-entry/product-status/user-loop/package owners | 作为 product-entry internals 阅读；public identity 仍是单一 MAG app skill。 |
| `2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md` | `support_current_truth` | schemas/source + product-entry manifest | 作为 schema-backed route/product-entry contract 支撑阅读。 |
| `2026-04-13-full-grant-authoring-executor-current-truth.md` | `support_current_truth` | route-selected executor docs + default Codex CLI owner | 作为 landed authoring executor scope 阅读；不提升 hosted proof lanes。 |
| `../history/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md` | `historical_route_snapshot` | full grant authoring executor spec + executor routing schema/source | 只作为 2026-04-12 route snapshot 阅读；当前 route catalog 已由 2026-04-13 full route landing 接管。 |
| `../history/specs/2026-04-12-critique-pending-handoff-contract-current-truth.md`, `../history/specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md` | `historical_handoff_snapshot` | full grant authoring executor spec + critique Codex CLI executor spec | 只作为 pending handoff 形成历史阅读；当前 critique 与前半程 authoring routes 已由 2026-04-13 specs/source 接管。 |
| `../history/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`, `../history/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md` | `historical_hosted_contract_provenance` | current contracts/schema/source + core docs | 只作为 hosted caller consumption proof 形成历史阅读；不表示 public hosted runtime 成熟。 |
| `../history/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md` | `historical_product_entry_handoff_provenance` | product-entry manifest + core docs | 只作为 OPL handoff shape 形成历史阅读；旧 Gateway wording 是 provenance。 |
| `../history/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md` | `historical_opl_alignment_snapshot` | OPL stage-led framework roadmap + MAG status | 只作为 2026-04-12 对齐快照阅读；不得作为 active phase map 或 hosted target。 |
| `../history/specs/2026-04-06-*` | `historical_provenance` | core five + history/specs index | 只作为 early foundation design 阅读。 |
| `../history/specs/2026-04-08-p5a-*`, `../history/specs/2026-04-08-p5b-*` | `future_activation_history` | domain admission/future planning owners | 不作为 active P5 backlog。 |
| `../history/specs/2026-04-08-r1a-*`, `../history/specs/2026-04-08-r1b-*`, `../history/specs/2026-04-08-r2a-*`, `../history/specs/2026-04-08-r3a-*`, `../history/specs/2026-04-09-r3a-*`, `../history/specs/2026-04-09-r4a-*`, `../history/specs/2026-04-09-r5a-*` | `historical_activation_package` | current pass/package/runtime docs + history/specs index | 作为 activation provenance 阅读；当前行为在 source/contracts。 |
| `../history/specs/2026-04-08-runtime-first-productization-program.md`, `../history/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md` | `historical_program_record` | core docs + history/specs index | 作为 R1-R5 形成历史阅读，不作为当前执行顺序。 |
| `../history/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`, `../history/specs/2026-04-10-post-r5a-local-runtime-validation-*`, `../history/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`, `../history/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md` | `historical_local_runtime_closeout` | core docs + route/runtime owner docs | 只从 history 阅读 fail-closed / honest-stop lessons；当前 runtime owner wording 在核心文档和 active/support guards。 |
| `../history/specs/2026-04-10-post-r5a-final-package-*`, `../history/specs/2026-04-10-post-r5a-hosted-contract-bundle-*`, `../history/specs/2026-04-10-post-r5a-stage-route-*`, `../history/specs/2026-04-10-post-r5a-worktree-aware-*`, `../history/specs/2026-04-10-post-r5a-revised-*` | `historical_fail_closed_record` | package/export schemas + history/specs index | 作为 fail-closed provenance 阅读；不得恢复旧 local runtime、hosted bundle 或 Gateway owner。 |
| `../history/specs/2026-04-11-hermes-backed-*`, `../history/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`, `../history/specs/2026-04-12-upstream-hermes-agent-fast-cutover-*` | `retired_provider_proof` | current core docs + explicit hosted/proof refs | 只能从 history 阅读；不得恢复 Hermes-backed owner、Gateway/local-manager、旧兼容别名或 default-runtime wording。 |

## Support Current-Truth Records

这些记录仍解释当前或近期落地的机制，但不是默认阅读路径。阅读时必须放在核心文档和 `current-program.json` 之下。

Support records 只在仍 current 的 subsection 内有效。若其中包含旧 provider、gateway、hosted 或 pending-route wording，除非当前 owner doc 明确提升，否则按历史内容阅读。

| 分组 | Records |
| --- | --- |
| Formal entry / durability | `2026-04-07-formal-entry-matrix-current-truth.md`, `2026-04-07-durability-model-clarification.md`；只读 current support guard，不恢复旧 local runtime。 |
| Historical P2-P4 grant flow / verification provenance | `../history/specs/2026-04-07-p2a-*`, `../history/specs/2026-04-07-p2b-*`, `../history/specs/2026-04-07-p2c-*`, `../history/specs/2026-04-07-p3a-*`, `../history/specs/2026-04-08-p3b-*`, `../history/specs/2026-04-08-p3c-*`, `../history/specs/2026-04-08-p4a-*`, `../history/specs/2026-04-08-p4b-*`；只读 provenance，不作为 support current-truth。 |
| Local runtime closeout / output consistency | `../history/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`, `../history/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`；只读 fail-closed 与 honest-stop provenance；当前 runtime owner wording 在核心文档和 active/support guards。 |
| Hosted / OPL handoff provenance | `../history/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`, `../history/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md`, `../history/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`；只读 contract consumption 与 route/export handoff 形成历史；旧 `OPL Gateway` 或 hosted-product completion language 仍是 provenance。 |
| Product entry and package surfaces | `2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`, `2026-04-12-p4a-*`, `2026-04-12-p4b-*`, `2026-04-12-p4c-*`, `2026-04-13-full-grant-authoring-executor-current-truth.md`, `2026-04-13-p4e-*`, `2026-04-13-p4f-*` |
| Historical route / handoff snapshots | `../history/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md`, `../history/specs/2026-04-12-critique-pending-handoff-contract-current-truth.md`, `../history/specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md` |

## Provider 与 Hosted 旧词处置

当前生命周期治理把旧 provider-runtime 词族归为以下状态：

| 词族 | 当前处置 |
| --- | --- |
| historical `2026-04-11-hermes-backed-*` specs 中的 `Hermes-backed runtime substrate owner` | 已退役 provider proof / provenance，位于 `docs/history/specs/`。`hermes_agent` 只表示显式非默认 executor/proof/provenance lane，不是 active provider owner、compatibility target 或 default runtime path。 |
| `upstream Hermes-Agent fast cutover` board 与 proof records | 历史 / proof context，已物理归档到 `docs/history/specs/`。它们只支撑 proof-lane vocabulary 和 fail-closed evidence；默认 execution、runtime ownership 和 OPL handoff boundary 在当前 owner docs。 |
| `OPL Gateway`、`gateway/federation`、`future P5` language | 历史或 future activation context。当前没有需要保留的 active Gateway/federation/compat surface；新 caller 使用 OPL stage-led framework + MAG descriptor/projection path。 |
| `OPL Runtime Manager`、Temporal target、provider-backed runtime、active-adapter、compatibility-bridge、local journal、attempt ledger wording | 历史 / provider-specific migration context。当前 MAG 口径是 OPL 作为 stage-led framework，以 Agent executor 为最小执行单位，消费 MAG-owned descriptor/projection；MAG 保留 grant truth、quality、route 和 export authority。 |
| `hosted contract bundle` | 当前 integration/reference export surface。Hosted runtime、Web UI 和 external portal submission 需要单独 current owner evidence。 |

## Historical Provenance Records

这些记录已物理归档到 `docs/history/specs/`。除非另一个 active surface 明确指向仍有效的 subsection，否则它们不定义 current truth。

| 分组 | Records |
| --- | --- |
| Foundation design | `2026-04-06-*` |
| Future activation packages | `2026-04-08-p5a-*`, `2026-04-08-p5b-*` |
| Historical P2-P4 authoring / review / verification tranche | `2026-04-07-p2a-*`, `2026-04-07-p2b-*`, `2026-04-07-p2c-*`, `2026-04-07-p3a-*`, `2026-04-08-p3b-*`, `2026-04-08-p3c-*`, `2026-04-08-p4a-*`, `2026-04-08-p4b-*` |
| Runtime-first R packages | `2026-04-08-r1a-*`, `2026-04-08-r1b-*`, `2026-04-08-r2a-*`, `2026-04-08-r3a-*`, `2026-04-08-runtime-first-*` |
| R3/R4/R5 activation packages | `2026-04-09-*` |
| Post-R5A fail-closed artifact-bundle notes | `2026-04-10-post-r5a-final-package-*`, `2026-04-10-post-r5a-hosted-contract-bundle-*`, malformed/fail-closed variants |
| Other post-R5A activation notes | `2026-04-10-post-r5a-local-runtime-validation-*`, `2026-04-10-post-r5a-revised-*`, `2026-04-10-post-r5a-stage-route-*`, `2026-04-10-post-r5a-worktree-aware-*` |
| Retired Hermes/provider records | `../history/specs/2026-04-11-hermes-backed-*`, `../history/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`, `../history/specs/2026-04-12-upstream-hermes-agent-fast-cutover-board.md`, `../history/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md` |
| OPL alignment snapshot | `../history/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md` |

这些分组的归档阅读入口是 [历史 specs](../history/specs/README.md)。

## 准入规则

新的技术记录不应默认继续新增 dated file 到 `docs/specs/`。

按下面路径判断落点：

1. 如果改变 current public role、runtime boundary、authoring quality 或 active command semantics，先更新核心五件套、`current-program.json`、schemas/source；只有该边界需要叙述说明时才新增小型 active spec。
2. 如果是仍在进行中的 implementation work，active 期间放入 `docs/active/`，closeout 后移入 `docs/history/plans/`。
3. 如果是背景、OPL handoff、distribution 或 support material，放入 `docs/references/`。
4. 如果是 completed activation package、migration record 或 superseded tranche，放入 `docs/history/`，或在本文标记为 historical 后 path-stable 留在 `docs/specs/`。
