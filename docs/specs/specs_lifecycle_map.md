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

## 当前 Specs 生命周期

这张表是 current specs 层的 direct-reader guard。纯历史文件位于 `docs/history/specs/`；current specs 层不再用 path stability 保留旧 activation package、route snapshot、hosted handoff 或 fail-closed tranche。

| 文件 | 生命周期 | 当前 owner / replacement | 阅读动作 |
| --- | --- | --- | --- |
| `2026-04-13-critique-codex-cli-executor-current-truth.md` | `active_current_spec` | active spec + core docs | 只读 critique executor vocabulary 与 Codex CLI route。 |
| `2026-04-27-ai-first-quality-boundary-current-truth.md` | `active_current_spec` | active spec + quality owner docs | 只读 AI-first quality boundary。 |
| `2026-04-23-authoring-completion-semantics-current-truth.md` | `active_current_spec` | active spec + authoring completion owner docs | 只读 completion semantics。 |
| `2026-04-22-quality-autonomy-family-grammar-current-truth.md` | `active_current_spec` | active spec + current quality/autonomy docs | 只读 quality governance、autonomy controller 和 family grammar。 |
| `2026-04-07-formal-entry-matrix-current-truth.md` | `support_current_truth` | core five + `current-program.json` | 作为 formal-entry 支撑 guard 阅读；旧 runtime-run/resume、journal 和 attempt ledger 只能按 history/provenance 读。 |
| `2026-04-07-durability-model-clarification.md` | `support_current_truth` | architecture/status + runtime-state docs | 只读 durability boundary guard；不恢复 local journal、attempt ledger 或 MAG-owned generic runtime。 |
| `product-entry-support-record.md` | `support_current_truth` | product-entry/product-status/user-loop/package owners | 作为 product-entry / package support 汇总阅读；public identity 仍是单一 MAG app skill。 |
| `2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md` | `support_current_truth` | schemas/source + product-entry manifest | 作为 schema-backed route/product-entry contract 支撑阅读。 |
| `2026-04-13-full-grant-authoring-executor-current-truth.md` | `support_current_truth` | route-selected executor docs + default Codex CLI owner | 作为 landed authoring executor scope 阅读；不提升 hosted proof lanes。 |

## 历史 Specs 策略

历史 specs 只通过 [历史 specs 索引](../history/specs/README.md) 进入。历史文件名、标题里的 `Current Truth`、`Activation Package`、旧 hosted/Gateway/Hermes/local-runtime wording、或 `current-program.json` 中的 `human_doc:*` 语义 id 都不能把文件提升回 current owner。

| 历史类别 | 当前 owner / replacement | 阅读动作 |
| --- | --- | --- |
| Foundation / object-model / early mainline records | core five + history/specs index | 只作为早期设计 provenance。 |
| P2/P3/P4 authoring/review/verification tranche | current route, quality and verification owner docs + source/contracts | 只作为 authoring-flow、review/rollback 与 verification gate 形成历史。 |
| Future P5 / federation / gateway records | active gap plan or OPL domain admission owners if reactivated + history/specs compression record | 不作为 active backlog 或 product target；长正文只从 git history 追溯。 |
| Runtime-first R/P packages and post-R5A local runtime closeout | core docs + runtime support index + history/specs index | 只读 fail-closed、honest-stop 和 migration lessons；长正文只从 git history 追溯，不恢复 local runtime owner。 |
| Post-R5A fail-closed hardening notes | package/export schemas + source/tests + history/specs index | 只作为 package/export fail-closed provenance。 |
| Hosted caller, hosted contract bundle, lightweight OPL handoff and old route snapshots | core docs + active plan + product-entry support record + contracts/schema/source + history specs compression record | 只读 historical handoff / route formation；长正文已压缩到历史 specs 索引和 support record，不表示 public hosted runtime、App workbench 或 production soak 完成。 |
| Hermes-backed / upstream Hermes proof records | current executor defaults + explicit non-default proof lane docs + history specs compression record | 只作为 proof/provenance；长正文已压缩到历史 specs 索引，仍被机器面引用的 Hermes-native critique tombstone 单独保留；不得恢复 Hermes-backed owner、Gateway/local-manager、旧兼容别名或 default-runtime wording。 |

## Support Current-Truth Records

这些记录仍解释当前或近期落地的机制，但不是默认阅读路径。阅读时必须放在核心文档和 `current-program.json` 之下。

Support records 只在仍 current 的 subsection 内有效。若其中包含旧 provider、gateway、hosted 或 pending-route wording，除非当前 owner doc 明确提升，否则按历史内容阅读。

| 分组 | Records |
| --- | --- |
| Formal entry / durability | `2026-04-07-formal-entry-matrix-current-truth.md`, `2026-04-07-durability-model-clarification.md`；只读 current support guard，不恢复旧 local runtime。 |
| Product entry and package surfaces | `2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`, `product-entry-support-record.md`, `2026-04-13-full-grant-authoring-executor-current-truth.md` |

## Provider 与 Hosted 旧词处置

当前生命周期治理把旧 provider-runtime 词族归为以下状态：

| 词族 | 当前处置 |
| --- | --- |
| historical `2026-04-11-hermes-backed-*` specs 中的 `Hermes-backed runtime substrate owner` | 已退役 provider proof / provenance，长正文已压缩到 `docs/history/specs/README.md`。`hermes_agent` 只表示显式非默认 executor/proof/provenance lane，不是 active provider owner、compatibility target 或 default runtime path。 |
| `upstream Hermes-Agent fast cutover` board 与 proof records | 历史 / proof context，长正文已压缩到 `docs/history/specs/README.md`；仍被机器面引用的 Hermes-native critique tombstone 继续保留在 history specs。它们只支撑 proof-lane vocabulary 和 fail-closed evidence；默认 execution、runtime ownership 和 OPL handoff boundary 在当前 owner docs。 |
| `OPL Gateway`、`gateway/federation`、`future P5` language | 历史或 future activation context；P5.A / P5.B 长正文已压缩到历史 specs 索引。当前没有需要保留的 active Gateway/federation/compat surface；新 caller 使用 OPL stage-led framework + MAG descriptor/projection path。 |
| `OPL Runtime Manager`、Temporal target、provider-backed runtime、active-adapter、compatibility-bridge、local journal、attempt ledger wording | 历史 / provider-specific migration context。当前 MAG 口径是 OPL 作为 stage-led framework，以 Agent executor 为最小执行单位，消费 MAG-owned descriptor/projection；MAG 保留 grant truth、quality、route 和 export authority。 |
| `hosted contract bundle` | 当前 integration/reference export surface。Hosted runtime、Web UI 和 external portal submission 需要单独 current owner evidence。 |

## 准入规则

新的技术记录不应默认继续新增 dated file 到 `docs/specs/`。

按下面路径判断落点：

1. 如果改变 current public role、runtime boundary、authoring quality 或 active command semantics，先更新核心五件套、`current-program.json`、schemas/source；只有该边界需要叙述说明时才新增小型 active spec。
2. 如果是仍在进行中的 implementation work，active 期间放入 `docs/active/`，closeout 后移入 `docs/history/plans/`。
3. 如果是背景、OPL handoff、distribution 或 support material，放入 `docs/references/`。
4. 如果是 completed activation package、migration record 或 superseded tranche，放入 `docs/history/`，或在本文标记为 historical 后 path-stable 留在 `docs/specs/`。
