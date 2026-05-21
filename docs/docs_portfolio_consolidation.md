# MAG 文档组合治理

Status: `active_docs_governance`
Owner: `Med Auto Grant`
Purpose: `docs_lifecycle_governance`
State: `active_support`
Machine boundary: 本文是人读治理入口。MAG 机器真相继续归 `contracts/runtime-program/current-program.json`、schema、source、CLI/API 行为、product-entry manifest、runtime receipts 和语义化 `human_doc:*` id。

## 当前结论

`docs/**` 是 MAG 的中文内部开发与维护参考，不再维护 docs 层双语镜像。稳定路径优先使用无语言后缀 `.md` 承载中文 canonical 内容。历史文件可以保留旧双语或旧路径描述作为 provenance，但 active/reference 索引必须指向当前无后缀路径。

MAG 采用 OPL-family canonical docs taxonomy：

`active/public/product/runtime/delivery/source/policies/specs/references/history`

这个目录集合按长期职责保留，不按当前文件数量决定。MAG 当前真实 owner 主要在核心五件套、`active/`、`references/`、`specs/` 和 `history/`；`public/product/runtime/delivery/source/policies` 当前较薄，但都有长期职责，后续按 current 内容小批量吸收。

## 与 OPL 的分层

OPL 系列项目全局主参考是 `/Users/gaofeng/workspace/one-person-lab/docs/active/opl-family-development-reference.md`。它持有全局 framework 目标、跨仓差距顺序、shared primitive 上收、App/workbench 目标和同名 docs taxonomy。

MAG 文档只维护 grant domain agent 的目标、差距、grant truth、fundability/quality/export authority、direct app skill path、OPL-hosted sidecar/projection/receipt 边界，以及 MAG-to-OPL 上收候选。MAS、RCA、MDS 或 OPL-owned App/workbench 的并行 backlog 不写入 MAG active docs。

## 目录职责

| 目录 | 长期职责 | 当前 MAG 承载 |
| --- | --- | --- |
| `docs/` root | docs 入口、核心五件套、docs governance | `README.md`、核心五件套、本文件。 |
| `docs/active/` | 当前计划、当前 gap、active baton、当前完成门槛 | `mag-ideal-state-cross-repo-gap-plan.md`。 |
| `docs/public/` | public narrative index 与 MAG 默认公开补充说明 | `domain-positioning.md`、`mvp-scope.md`。新增公开正文前先确认 public/product 需求。 |
| `docs/product/` | app skill、product status、user-loop、direct entry、operator guidance | 当前较薄；后续从 core docs/specs/contracts 抽取仍 current 的 product-entry 内容。 |
| `docs/runtime/` | runtime/control/projection、OPL-hosted boundary、receipt/projection 支撑 | 当前较薄；runtime truth 仍在 contracts/source/status/specs。 |
| `docs/delivery/` | submission-ready package、export、delivery、manual portal boundary | 当前较薄；grant artifact/export authority 仍 MAG-owned。 |
| `docs/source/` | funder/task/source intake、workspace canonical document、source truth consumption | 当前较薄；后续承接 workspace/source intake 和 funder-source 边界。 |
| `docs/policies/` | 稳定治理规则、文档规则、repo-local operating discipline | 当前较薄；长期规则可从 invariants/decisions/governance checklist 抽取。 |
| `docs/specs/` | active specs、support current-truth records、integration references | 只保留当前或仍支撑当前 subsection 的技术记录；纯历史 R/P/post-R5A/future-P5/provider-proof 记录已归档到 `docs/history/specs/`。 |
| `docs/references/` | north-star、OPL adoption、memory policy、governance checklist | 真实承载；不承担 active owner。 |
| `docs/history/` | 完成计划、旧 specs、旧 provider/runtime/OMX/provenance | 真实承载；不承担 current truth。 |

## 非 canonical 目录

旧 `docs/plans/` 已物理退役，不再作为 active owner。完成计划留在 `docs/history/plans/`。如果历史计划仍含 current truth，先抽取内容进入 `active/product/runtime/delivery/source/policies/specs` 的当前 owner，再保留原文件作为 provenance。

`docs/specs/` 是 current/support 技术记录层，不是旧接口兼容层。只有 README 和 `specs_lifecycle_map.md` 明确列为 active 的 specs 才能作为 current owner；其余留在本目录的 dated specs 只按 support/provenance subsection 阅读。纯历史 activation package、早期 P2/P3/P4 flow/verification tranche、future P5、runtime-first R/P tranche、post-R5A local-runtime closeout、post-R5A fail-closed hardening、provider proof 和 tombstone 已经移动到 `docs/history/specs/`，不得再被恢复为 active spec、default runtime owner、Gateway/local-manager 路线、flat CLI alias 或 compatibility test 的依据。

## 内容级整合规则

1. 当前 public identity 和 product boundary 回到 `docs/public/`、核心五件套和 current-program。
2. 当前 gap 和计划留在 `docs/active/`；evidence request / receipt ledger 的机器细节留在 contracts、source、manifest 或 history，`docs/status.md` 只保留 current boundary 摘要。
3. Product-entry、user-loop、operator guidance 进入 `docs/product/`；grant truth 不迁出 MAG。
4. Runtime/control/projection 支撑进入 `docs/runtime/`；machine truth 仍归 contracts/source/runtime evidence。
5. Submission-ready package/export/delivery 支撑进入 `docs/delivery/`；fundability、quality、export verdict 和 package authority 仍归 MAG。
6. Funder/source/workspace 支撑进入 `docs/source/`；generic shell 候选记录为 MAG-to-OPL 上收边界。
7. 稳定规则进入 `docs/policies/`；一次性计划不得放入 policies。

## Direct Retirement

当旧模块、旧接口、旧 CLI alias、旧 wrapper、旧 facade、patch bridge、旧测试入口或旧文档入口已被当前 owner surface 替代时，默认直接退役。迁移 active caller 后删除旧面；需要来龙去脉时只保留 history/tombstone/provenance，不新增 compatibility shim、别名、re-export facade 或 compatibility-only 聚合测试。

当前 direct retirement posture 的 active owner 是 `docs/active/mag-ideal-state-cross-repo-gap-plan.md`，机器投影是 `product-entry-manifest.ideal_state_closure_status.direct_retirement_posture`。维护时应先看 manifest 中的 `physical_skeleton_follow_through` 与 `controlled_domain_memory_apply_proof.repo_source_layout_audit`，确认旧面已经没有 active caller，再删除或归档；不要用旧路径稳定性作为保留兼容壳的理由。

## 当前生命周期决策

- 核心五件套 `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md` 与 `docs/decisions.md` 现在显式标注 `owner/purpose/state/machine boundary`，继续承担 current 人读 truth set。它们解释当前边界，但不成为机器接口；其中 `docs/status.md` 只保留当前角色、边界、入口、证据门和下一跳，不承载 dated machine-surface closeout、receipt ledger 流水或新增 proof 清单。
- `docs/public/domain-positioning.md` 与 `docs/public/mvp-scope.md` 是 current public support；它们只补充公开定位和 MVP 范围。hosted / OPL consumption 旧证明只作历史上下文，外部 OPL/App/production caller 消费、direct/hosted parity 和 long-soak 仍归 active evidence gate。
- `docs/references/integration/opl-family-contract-adoption.md` 是 OPL family contract adoption reference；它说明 MAG 如何暴露 descriptor/projection/receipt refs，不声明 production provider-hosted grant soak、App/workbench consumption 或 bridge exit 全部完成。
- 原 `docs/specs/2026-04-06-*`、`2026-04-07-p2*`、`2026-04-07-p3a*`、`2026-04-08-p3*`、`2026-04-08-p4*`、`2026-04-08-p5*`、`2026-04-08-r*`、`2026-04-08-runtime-first-*`、`2026-04-09-*`、大部分 `2026-04-10-post-r5a-*`、`2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`、`2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`、`2026-04-11-hermes-backed-*`、`2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`、`2026-04-12-upstream-hermes-agent-fast-cutover-*`、`2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md`、`2026-04-12-hosted-caller-consumption-proof-current-truth.md`、`2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md` 与 `2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md` 已无 active owner 角色，物理移动到 `docs/history/specs/`。
- package/export、formal-entry、authoring completion、AI-first quality、quality/autonomy/family grammar 和 current product-entry support specs 仍留在 `docs/specs/`，但只按 lifecycle map 标注的具体 subsection 阅读；它们不承担 public identity、runtime owner 或 production soak 结论。local runtime honest-stop 与旧 hosted/handoff 相关文件只从 `docs/history/specs/` 阅读。
- `docs/product/`、`docs/runtime/`、`docs/delivery/`、`docs/source/`、`docs/policies/` 当前保持薄索引职责；不要为了填目录把核心五件套内容拆散成第二真相源。
- 旧 `tests/test_product_entry.py` 聚合入口、`domain_runtime_parts.patch_targets` patch bridge、Gateway/local-manager default path 与 legacy flat CLI shell alias 继续按 direct retirement posture 处理；文档层只保留 history/provenance，不新增兼容入口。

## 长清单治理

MAG 的 dense dated specs 和历史 specs 只能通过 `docs/specs/specs_lifecycle_map.md` 分层读取，不再把每个历史 tranche 当成 active checklist。

- `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 是唯一当前 gap / 完善计划；它只保留当前结构状态、证据门、完善顺序和禁止误写口径。
- `docs/specs/specs_lifecycle_map.md` 是 specs direct-reader guard；它负责告诉读者某个 dated spec 的当前有效 subsection、replacement owner 和历史状态，不新增 implementation backlog；已移动到 `docs/history/specs/` 的 P2/P3/P4 flow/verification 记录只保留形成过程，不再承担 support current-truth。
- `docs/history/specs/` 保存 activation package、provider proof、post-R5A hardening 和 retired proof 记录；这些文件中的 `Current Truth` 标题只能按当时语境读取。
- 如果 support spec 中的某个规则仍 current，应抽取到核心五件套、active gap plan、policy/spec owner、contract 或 source surface；不要继续在同一 dated spec 里追加 2026-05 之后的状态。
- 历史长表若只提供 provenance，保持 history；若仍影响当前行动，合并为 `owner / current state / evidence gate / next action` 四列后进入 active owner。

## Transition / Oracle Gap

MAG-owned grant transition/oracle 后续工作也归 `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 管理。MAG 只定义 grant transition table、fundability / aims / review / package guards、typed blocker、owner action 和 oracle fixtures；generic state-machine runner、matrix runner、queue、retry/dead-letter、provider lifecycle 与 operator workbench 归 OPL Framework。

`product-entry-manifest.ideal_state_closure_status.mag_owned_transition_oracle` 现在把该 gap 投影为 `domain_spec_landed_external_runner_gate`，并通过 focused test 固定 oracle fixture -> sidecar `stage-attempt/closeout` -> owner/no-regression receipt refs 的 repo-local no-regression closeout case。OPL 仍不能从 provider completion 推断 `fundability_ready`、`authoring_quality_ready` 或 `submission_ready_export_ready`，该 proof 也不声明 production long-run soak 完成。
