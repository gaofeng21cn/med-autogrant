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

## Portfolio 核对规则

本文件不再维护 frozen inventory count、逐日期 coverage 或 proof-by-proof closeout。需要核对当前 portfolio 时，用 `find docs -maxdepth 3 -type f | sort` 读取 live 文件集；生命周期角色按 owner 层读取，而不是按文件名日期读取：

| 文档集合 | 当前角色 | 处理规则 |
| --- | --- | --- |
| 根层 `README.md` / `README.zh-CN.md` | `current_public` | 公开第一入口；不承担技术 truth ledger。 |
| 非 docs README：`agent/README.md`、`contracts/README.md`、`runtime/README.md` | repo-source / machine-surface 人读索引 | 各自只解释目录边界；机器真相仍归对应 contracts/source/runtime evidence。 |
| docs 根入口与核心五件套 | current 人读 truth set | 只保留角色、边界、入口、证据门和决策；不追加 receipt proof、worktree closeout 或 dated proof 清单。 |
| `docs/active/**` | active gap / inventory | `mag-ideal-state-cross-repo-gap-plan.md` 是唯一 active gap plan；`opl-private-implementation-migration-inventory.md` 是 per-surface 明细，不替代 active plan。 |
| `docs/public/product/runtime/delivery/source/policies/**` | 薄 support index | 只做目录职责和下一跳，不把核心事实复制成第二真相源。 |
| `docs/specs/**` | active specs / support records / lifecycle map | 只按 `docs/specs/README.md` 与 `specs_lifecycle_map.md` 标注的 active 或 support subsection 阅读。 |
| `docs/references/**` | reference | north-star、OPL adoption、memory policy、series governance checklist；不承担 current status、docs lifecycle governance 或 active plan。 |
| `docs/history/**` | history / provenance | 保存旧 specs、旧 plans、provider proof、coverage ledger、OMX 和 tombstone；标题中的 `Current Truth` 只能按当时语境阅读。 |

当前没有需要新增 docs 目录或把 history 文件恢复为 active/support owner 的证据。此前 active/status 入口携带的 proof-by-proof 明细已按 owner/gate/status 层压回 `docs/status.md` 与 active gap plan；dated coverage、retirement audit 和 proof 流水继续留在 history 或机器合同。

History 文件不得因为 `current-program.json` 保留 `human_doc:*` 语义 id、文件名含 `current-truth`、或旧审计路径仍可达而恢复为 active/support owner。若仍有 current 规则，先抽取到核心五件套、active plan、support record、contract/schema/source 或对应薄入口，再保留原文件作为 provenance。

## 与 OPL 的分层

OPL 系列项目全局主参考是 `/Users/gaofeng/workspace/one-person-lab/docs/active/opl-family-development-reference.md`。它持有全局 framework 目标、跨仓差距顺序、shared primitive 上收、App/workbench 目标和同名 docs taxonomy。

MAG 文档只维护 grant domain agent 的目标、差距、grant truth、fundability/quality/export authority、direct app skill path、OPL-hosted domain_handler/projection/receipt 边界，以及 MAG-to-OPL 上收候选。MAS、RCA、MDS 或 OPL-owned App/workbench 的并行 backlog 不写入 MAG active docs。

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
| `docs/specs/` | active specs、support records、integration references | 只保留 active current specs、少量 support records 和 lifecycle map；纯历史 R/P/post-R5A/future-P5/provider-proof/hosted-handoff 记录归档到 `docs/history/specs/`。 |
| `docs/references/` | north-star、OPL adoption、memory policy、series governance checklist | 真实承载；不承担 active owner、docs lifecycle governance 或 current status。 |
| `docs/history/` | 完成计划、旧 specs、旧 provider/runtime/OMX/provenance | 真实承载；不承担 current truth。 |

## 非 canonical 目录

旧 `docs/plans/` 已物理退役，不再作为 active owner。完成计划留在 `docs/history/plans/`。如果历史计划仍含 current truth，先抽取内容进入 `active/product/runtime/delivery/source/policies/specs` 的当前 owner，再保留原文件作为 provenance。

`docs/specs/` 是 current/support 技术记录层，不是旧接口兼容层。只有 README 和 `specs_lifecycle_map.md` 明确列为 active 的 specs 才能作为 current owner；其余留在本目录的 dated specs 只按 support subsection 阅读。纯历史 activation package、早期 P2/P3/P4 flow/verification tranche、future P5、runtime-first R/P tranche、post-R5A local-runtime closeout、post-R5A fail-closed hardening、provider proof、hosted handoff、old route snapshot 和 tombstone 应位于 `docs/history/specs/`，不得再被恢复为 active spec、default runtime owner、Gateway/local-manager 路线、flat CLI alias 或 compatibility test 的依据。

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

当前 direct retirement posture 的 active owner 是 `docs/active/mag-ideal-state-cross-repo-gap-plan.md`；per-surface 明细 owner 是 `docs/active/opl-private-implementation-migration-inventory.md`。机器投影回到 `product-entry-manifest.ideal_state_closure_status.direct_retirement_posture`、`product-entry-manifest.physical_skeleton_follow_through`、`controlled_domain_memory_apply_proof.repo_source_layout_audit`、`contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate` 与 `contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy`。维护时先按 active plan 判断当前 gate，再按 inventory 和 machine surface 确认 active caller；不要用旧路径稳定性作为保留兼容壳的理由。

旧 public/domain-entry runtime command family `run-local`、`runtime-run`、`runtime-resume`、`probe-upstream-hermes` 的 dated audit 已压缩到 [MAG retired surface provenance](./history/docs-portfolio-coverage-ledger/retired-surface-provenance.md)。当前文档只保留 no-resurrection 规则：旧 runtime command、local journal、attempt ledger、Gateway/local-manager、flat alias、facade patch bridge 和 compatibility aggregate test 只能出现在 negative guard、tombstone 或 history/provenance 中；无 active caller 后直接删除或归档，不新增 compatibility surface。

## 当前生命周期决策

- 核心五件套 `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md` 与 `docs/decisions.md` 继续承担 current 人读 truth set。它们解释当前边界，但不成为机器接口；其中 `docs/status.md` 只保留当前角色、边界、入口、证据门和下一跳，不承载 dated closeout、receipt ledger 流水或新增 proof 清单。
- `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 是唯一 active gap / plan owner；`docs/active/opl-private-implementation-migration-inventory.md` 是 per-surface inventory，不替代 active plan。
- `docs/public/domain-positioning.md` 与 `docs/public/mvp-scope.md` 是 current public support；它们只补充公开定位和 MVP 范围。hosted / OPL consumption 旧证明只作历史上下文，外部 OPL/App/production caller 消费、direct/hosted parity 和 long-soak 仍归 active evidence gate。
- `docs/references/integration/opl-family-contract-adoption.md` 是 OPL family contract adoption reference；它说明 MAG 如何暴露 descriptor/projection/receipt refs，不声明 production provider-hosted grant soak、App/workbench consumption 或 bridge exit 全部完成。
- `docs/specs/` 当前只保留 active specs、support records 和 lifecycle map；历史 P/R/post-R5A/provider proof/hosted handoff/old route snapshot 统一从 `docs/history/specs/` 阅读。`docs/specs/specs_lifecycle_map.md` 维护聚合生命周期，不再在本文件堆每个 dated tranche。
- `docs/product/`、`docs/runtime/`、`docs/delivery/`、`docs/source/`、`docs/policies/` 保持薄索引职责；不要为了填目录把核心五件套内容拆散成第二真相源。
- 旧 `tests/test_product_entry.py` 聚合入口、`domain_runtime_parts.patch_targets` patch bridge、Gateway/local-manager default path 与 legacy flat CLI shell alias 继续按 direct retirement posture 处理；具体 path-level 状态回到 private inventory 和 machine audit，文档层只保留 history/provenance，不新增兼容入口。

## 长清单治理

MAG 的 dense dated specs 和历史 specs 只能通过 `docs/specs/specs_lifecycle_map.md` 分层读取，不再把每个历史 tranche 当成 active checklist。

- `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 是唯一当前 gap / 完善计划；它只保留当前结构状态、证据门、完善顺序和禁止误写口径。
- `docs/specs/specs_lifecycle_map.md` 是 specs direct-reader guard；它负责告诉读者某个 dated spec 的当前有效 subsection、replacement owner 和历史状态，不新增 implementation backlog；已移动到 `docs/history/specs/` 的 P2/P3/P4 flow/verification 记录只保留形成过程，不再承担 support current-truth。
- `docs/history/specs/` 保存 activation package、provider proof、post-R5A hardening 和 retired proof 记录；这些文件中的 `Current Truth` 标题只能按当时语境读取。
- 如果 support spec 中的某个规则仍 current，应抽取到核心五件套、active gap plan、policy/spec owner、contract 或 source surface；不要继续在同一 dated spec 里追加 2026-05 之后的状态。
- 历史长表若只提供 provenance，保持 history；若仍影响当前行动，合并为 `owner / current state / evidence gate / next action` 四列后进入 active owner。

## Transition / Oracle Gap

MAG-owned grant transition/oracle 后续工作也归 `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 管理。MAG 只定义 grant transition table、fundability / aims / review / package guards、typed blocker、owner action 和 oracle fixtures；generic state-machine runner、matrix runner、queue、retry/dead-letter、provider lifecycle 与 operator workbench 归 OPL Framework。

`product-entry-manifest.ideal_state_closure_status.mag_owned_transition_oracle` 现在把该 gap 投影为 `domain_spec_landed_external_runner_gate`，并通过 focused test 固定 oracle fixture -> domain_handler `stage-attempt/closeout` -> owner/no-regression receipt refs 的 repo-local no-regression closeout case。OPL 仍不能从 provider completion 推断 `fundability_ready`、`authoring_quality_ready` 或 `submission_ready_export_ready`，该 proof 也不声明 production long-run soak 完成。

## Coverage ledger foldback

Dated coverage entries, frozen inventory notes, retirement audits, no-rewrite closeouts and proof/read-model foldback records that previously lived as per-tranche files are compressed under [MAG docs portfolio coverage ledger](./history/docs-portfolio-coverage-ledger/README.md), with durable no-resurrection rules in [MAG retired surface provenance](./history/docs-portfolio-coverage-ledger/retired-surface-provenance.md).

This file now keeps only current lifecycle rules, owner split, direct-retirement posture, long-list governance, and the current transition/oracle gap location. Do not append future frozen inventories, command transcripts, branch/worktree closeout, receipt ledgers, or proof-by-proof tranches here. New dated coverage belongs under `docs/history/docs-portfolio-coverage-ledger/` or another precise `docs/history/**` owner; durable conclusions must be folded back into the core five docs, active gap plan, lifecycle map, contracts, source, or tests.

Current active owner remains [MAG ideal-state cross-repo gap plan](./active/mag-ideal-state-cross-repo-gap-plan.md). Dense specs are read through [Specs 生命周期地图](./specs/specs_lifecycle_map.md); historical specs stay under [历史 specs 索引](./history/specs/README.md).
