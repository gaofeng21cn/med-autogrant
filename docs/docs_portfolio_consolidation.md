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

`product-entry-manifest.ideal_state_closure_status.mag_owned_transition_oracle` 现在把该 gap 投影为 `domain_spec_landed_external_runner_gate`，并通过 focused test 固定 oracle fixture -> domain_handler `stage-attempt/closeout` -> owner/no-regression receipt refs 的 repo-local no-regression closeout case。OPL 仍不能从 provider completion 推断 `fundability_ready`、`authoring_quality_ready` 或 `submission_ready_export_ready`，该 proof 也不声明 production long-run soak 完成。

## Coverage ledger

### 2026-05-26 thin support index coverage tranche

本轮逐段覆盖 MAG thin support index：

- `docs/product/README.md`：仍是 `domain_product_entry_support`，只索引 direct product-entry、product status、user loop、operator guide 与 app-skill 支撑；不复制 grant truth、quality/export verdict 或 product-entry manifest 机器状态。
- `docs/runtime/README.md`：仍是 `grant_runtime_support`，只索引 runtime/control/projection 和 direct/hosted 边界；`contracts/runtime-program/current-program.json`、`MagDomainRuntime.describe_topology()`、`product-entry-manifest.opl_provider_runtime_contract`、`domain_handler_export` 与 `opl_substrate_adapter_export` 共同确认 runtime owner 是 OPL/Temporal，MAG 不内置 daemon、scheduler、attempt loop 或 attempt ledger。
- `docs/delivery/README.md`：仍是 `grant_delivery_support`，只索引 submission-ready package、export 与 delivery 支撑；MAG 持有 fundability、quality、export verdict 与 package authority，外部门户提交不写成本仓完成状态。
- `docs/source/README.md`：仍是 `grant_source_workspace_support`，只索引 workspace/source refs；`build_source_provenance_surface()` 和 `domain_handler_export.source_provenance` 确认 OPL 只消费 `docs/source/README.md`、historical fixture、explicit archive import command 和 parity oracle 这类 body-free refs。
- `docs/policies/README.md`：仍是 `stable_policy_index`，只索引长期治理规则；一次性计划、旧接口退役和 provider proof 继续进入 `docs/active/` 或 `docs/history/**`，不迁入 policies。

Live truth inputs：`AGENTS.md`、`TASTE.md`、核心五件套、本文件、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md`、`contracts/runtime-program/current-program.json`、`contracts/private_functional_surface_policy.json`、`contracts/production_acceptance/mag-production-acceptance.json`、`contracts/runtime-program/opl-family-contract-adoption.json`、`MedAutoGrantDomainEntry`、`MagDomainRuntime.describe_topology()`、`build_product_entry_manifest()`、`build_domain_handler_export()`、`build_source_provenance_surface()`、`build_opl_substrate_adapter_export()` 和 MAG CLI help。

Edited docs：仅本文件记录 coverage ledger。五个 thin support index 保持原文，因为它们已经具备 owner / purpose / state / machine boundary，且未发现 runtime owner、source truth、delivery authority、policy owner 或 product-entry authority 泄漏。

Archived / tombstoned / deleted docs：无。本轮没有发现这五个 thin index 下需要归档、tombstone 或删除的文档；对应目录当前只有 README 索引，薄状态符合 portfolio 职责。

Uncovered docs：本条 ledger 只关闭 `docs/product/README.md`、`docs/runtime/README.md`、`docs/delivery/README.md`、`docs/source/README.md` 与 `docs/policies/README.md` 的逐段覆盖。MAG 其余 README/docs 覆盖状态继续以 OPL series 全局 coverage ledger 和后续 tranche 为准，不由本条本地 ledger 重新声明全仓完成。

Remaining stale / retire candidates：后续若在这些目录新增正文，必须继续保持 thin support role，不得把 `product-entry-manifest`、`domain_handler_export`、source provenance、delivery package 或 policies 写成第二 active truth、MAG-owned generic runtime/workbench/scheduler、旧 Gateway/frontdoor/compat alias 路线，或 production/domain readiness 结论。

Next tranche write scope：继续按 OPL series coverage ledger 推进未覆盖 repo/section；MAG 侧若再进入本地写入，优先处理 specs/support current-truth map、references/history residual stale wording，或由 OPL 全局 ledger 指向的下一段 MAG 文档。

### 2026-05-26 2026-04-07 authoring / review history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-07 P2/P3A authoring / review 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 `Current Truth` 标题、CLI-only early authoring route、mentor verdict freeze 或 early audit surface 误读成当前 route owner、runtime owner、quality/export/submission-ready verdict、compatibility interface 或 active backlog。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-07-p2a-intake-direction-question-mainline-current-truth.md`, `docs/history/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`, `docs/history/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`, `docs/history/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`.
- Machine truth surfaces: `contracts/runtime-program/current-program.json`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior.

Fresh semantic result：

- All four reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- P2.A / P2.B / P2.C are correctly scoped as `historical_authoring_flow_provenance`; P3.A is correctly scoped as `historical_review_gate_provenance`.
- The files explicitly route current route truth、authoring pass、executor boundary、review / quality boundary、OPL/Temporal runtime owner and machine behavior back to current core docs、active specs、contracts/schema/source、CLI/API behavior and `contracts/runtime-program/current-program.json`.
- Stale-risk scan found no unguarded Hermes/Gateway/local-manager/local-runtime/attempt-ledger/default-runtime wording in this batch. The only `Current Truth` wording is in historical titles and is already guarded by file-level lifecycle notes.
- No body rewrite was needed. This tranche records paragraph coverage and confirms the existing lifecycle guard is sufficient.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-07 history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, status and current-program runtime owner fields. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的历史 provenance；不需要移动、tombstone 或正文删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch and this 2026-04-07 P2/P3A batch are not paragraph-governed in this tranche.
- Higher-risk remaining batches include 2026-04-08 P3/P4 rollback / verification gate records, 2026-04-08 P5 / R-series activation packages, 2026-04-09 R3/R4/R5 / post-R5A records, 2026-04-10 fail-closed / hosted-bundle records, 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted/OPL handoff records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later OPL global ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-07 specs as current route registry, runtime owner, default CLI/API contract, quality/export/submission-ready verdict, physical-delete authority or compatibility-interface source is stale pollution.
- `ready_for_submission` in P3.A remains historical verdict semantics only. Current submission-ready / export / human-gate authority must come from MAG-owned active specs, contracts/source, owner receipt or typed blocker surfaces.
- P2/P3 authoring-flow route examples remain provenance. They must not override current OPL/Temporal default runtime ownership, current active route catalog, AI-first quality boundary or product-entry / domain-handler source.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing 2026-04-08 P3/P4 rollback / verification records or 2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale provider wording risk is higher there.
- Or switch to OPL/RCA/App full README/docs coverage when their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-08 P3/P4 rollback / verification history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-08 P3/P4 rollback、presubmission、verification gate 与 checkpoint 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 `Current Truth` 标题、裸 `stage-route-report` verification command、CLI-only validation surface、MCP/controller future scope、`ready_for_submission` / `presubmission_frozen` 或 checkpoint vocabulary 误读成当前 public CLI shape、runtime owner、submission/export authority、production readiness、compatibility interface 或 active backlog。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`, `docs/history/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`, `docs/history/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`, `docs/history/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/route_report.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/cli.py`, `src/med_autogrant/domain_entry.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior.
- Fresh CLI/read-model probes: `med_autogrant --help`, `med_autogrant workspace --help`, `workspace route-report` on gate-open and gate-closed examples, `workspace next-step` on forced-rollback example, and `MagDomainRuntime().describe_topology()`.

Fresh semantic result：

- All four reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- P3.B / P3.C are correctly scoped as historical review / rollback / presubmission provenance; P4.A / P4.B are correctly scoped as historical verification-gate / checkpoint provenance.
- Current public CLI shape is grouped: `med_autogrant workspace route-report`, not the historical bare `stage-route-report` command examples. The historical examples remain useful provenance but must not be copied into current operator docs without mapping through `public_cli`.
- Current checkpoint aggregation is source-owned by `route_report.build_stage_route_report()` / `build_verification_checkpoint()` and domain entry dispatch; representative fresh probes returned `freeze_ready`, `submission_frozen`, and `argument_building` for the expected gate-open, gate-closed and forced-rollback examples.
- `MagDomainRuntime().describe_topology()` still reports `runtime_owner=one-person-lab`, `can_claim_generic_runtime_owner=False`, `default_formal_entry=CLI`, `supported_protocol_layer=MCP`. These historical specs therefore do not grant MAG a generic runtime, controller, provider, submission-ready or production-ready authority.
- Stale-risk scan found no unguarded Hermes/Gateway/local-manager/local-runtime/attempt-ledger/default-runtime wording in this batch. `Current Truth`, `ready_for_submission`, `MCP/controller`, formal-entry and submission wording appears in historical titles/body text and is guarded by file-level lifecycle notes.
- No body rewrite was needed. This tranche records paragraph coverage and confirms the existing lifecycle guard plus specs lifecycle map are sufficient.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-08 P3/P4 history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner fields, route-report source, domain runtime topology, public CLI mapping and representative CLI outputs. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone 或正文删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch、2026-04-07 P2/P3A batch and this 2026-04-08 P3/P4 batch are not paragraph-governed in this tranche.
- Higher-risk remaining MAG batches include 2026-04-08 P5 / R-series activation packages, 2026-04-09 R3/R4/R5 / post-R5A records, 2026-04-10 fail-closed / hosted-bundle records, 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted/OPL handoff records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later OPL global ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-08 specs as current public CLI command shape, runtime owner, default CLI/API contract, controller capability, submission-ready/export-ready verdict, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical bare `stage-route-report` command examples must be mapped through current public CLI as `workspace route-report`; otherwise they are old verification-package provenance, not active operator docs.
- `ready_for_submission`, `presubmission_frozen`, `freeze_ready`, `submission_frozen` and rollback checkpoint vocabulary remain route/checkpoint semantics. They must not be upgraded to final external submission, export authorization, grant package authority, human-gate approval, provider completion, App/release readiness or production-ready claims.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing 2026-04-08 P5/R activation packages or 2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale provider/hosted wording risk is higher there.
- Or switch to RCA uncovered reference bodies or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-08 P5/R1 activation history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-08 P5 second-family / federation future activation packages 与 R1 local-runtime activation packages。目标是确认这些 direct-file 历史入口不会把旧 future P5、Gateway/federation、local `runtime-run` / `runtime-resume`、run journal、stage action envelope、MCP/controller 或 runtime-productization 词汇误读成当前 active P5 backlog、federation-ready、public CLI command、MAG-owned generic runtime、daemon/scheduler/attempt-loop、attempt ledger、production readiness、compatibility interface 或 active implementation plan。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-08-p5a-second-grant-family-onboarding-activation-package.md`, `docs/history/specs/2026-04-08-p5b-federation-contract-freeze-activation-package.md`, `docs/history/specs/2026-04-08-r1a-local-main-loop-entry-and-stop-reason-activation-package.md`, `docs/history/specs/2026-04-08-r1b-stage-action-executor-envelope-activation-package.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, `tests/test_domain_entry.py`, `tests/product_entry_cases/test_functional_closure.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh read-model probe: `MagDomainRuntime().describe_topology()` plus `public_cli_command("stage-route-report", ...)` and `PUBLIC_GROUP_COMMANDS["workspace"]`.

Fresh semantic result：

- All four reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- P5.A / P5.B are correctly scoped as `future_activation_history` / historical second-family and federation activation provenance. They are not current second-family admitted claims, active P5 backlog, Gateway-ready / federation-ready claims, cross-domain runtime owner claims or public runtime entries.
- R1.A / R1.B are correctly scoped as `historical_activation_package` / local runtime and stage action envelope provenance. They are not current MAG-owned daemon, scheduler, attempt loop, attempt ledger, public `runtime-run` / `runtime-resume` command, local runtime product plan or generic runtime authority.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, and `mag_owns_attempt_ledger=false`.
- `MagDomainRuntime().describe_topology()` still reports `runtime_owner=one-person-lab`, `can_claim_generic_runtime_owner=False`, `default_formal_entry=CLI`, `supported_protocol_layer=MCP`, `internal_controller_surface=controller`, and `optional_proof_executor_boundary=explicit opt-in only`.
- Current public CLI shape remains grouped; historical bare `stage-route-report` maps through `public_cli` as `workspace route-report`. `runtime-run`、`runtime-resume` 和 `probe-upstream-hermes` are covered by no-resurrection source/tests and must not be restored as active public/domain commands.
- Stale-risk scan found P5/R1 risk terms only inside lifecycle-guarded history/provenance text, explicit future-scope/precondition/stop-condition guardrails, or no-resurrection surfaces. No body rewrite was needed; this tranche records paragraph coverage and confirms the existing lifecycle guard plus specs lifecycle map are sufficient.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-08 P5/R1 history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, status, current-program runtime owner fields, public CLI mapping, domain runtime topology and retired command no-resurrection surfaces. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone 或正文删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch、2026-04-07 P2/P3A batch、2026-04-08 P3/P4 batch and this 2026-04-08 P5/R1 batch are not paragraph-governed in this tranche.
- Higher-risk remaining MAG batches include 2026-04-08 R2/R3/runtime-first program records, 2026-04-09 R3/R4/R5 / post-R5A records, 2026-04-10 fail-closed / hosted-bundle records, 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted/OPL handoff records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later OPL global ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these P5/R1 specs as current public CLI command shape, runtime owner, default runtime, Gateway/federation readiness, controller capability, local run journal authority, attempt ledger, submission/export-ready verdict, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical `runtime-run` / `runtime-resume` / run journal / stage action envelope vocabulary must remain provenance unless a current active owner and source/contract/tests explicitly re-admit it; current no-resurrection tests guard these commands from reappearing as active public/domain commands.
- P5 second-family and federation language must not be upgraded to admitted family, Grant Foundry readiness, Gateway route, OPL generated/hosted caller readiness, App/release readiness or production-ready claims.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing 2026-04-08 R2/R3/runtime-first records or 2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale local-runtime/provider/hosted wording risk is higher there.
- Or switch to RCA uncovered reference bodies or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-08 R2/R3 runtime-first history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-08 runtime-first program、R1-to-R5 boundary map、R2 artifact-bundle 和 R3 critique/revision executor 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 runtime-first ladder、local runtime、`runtime-run` / `runtime-resume`、run journal、host-agent、hostedization、R2/R3 activation package、artifact bundle、revision executor 或 R1-R5 honest-stop 词汇误读成当前执行顺序、MAG-owned generic runtime、active local runtime plan、public runtime commands、attempt ledger、OPL/App production readiness、submission/export-ready verdict、compatibility interface 或 active implementation queue。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-08-runtime-first-productization-program.md`, `docs/history/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`, `docs/history/specs/2026-04-08-r2a-artifact-bundle-production-surface-activation-package.md`, `docs/history/specs/2026-04-08-r3a-critique-revision-executor-surface-activation-package.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, `tests/test_domain_entry.py`, `tests/product_entry_cases/test_functional_closure.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh read-model probes: `MagDomainRuntime().describe_topology()`, `public_cli_command("build-artifact-bundle", ...)`, `public_cli_command("execute-revision-pass", ...)`, `PUBLIC_GROUP_COMMANDS["package"]`, `PUBLIC_GROUP_COMMANDS["pass"]`, `med_autogrant package --help`, and `med_autogrant pass --help`.

Fresh semantic result：

- All four reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- `2026-04-08-runtime-first-productization-program.md` and `2026-04-08-runtime-first-r1-to-r5-boundary-map.md` are correctly scoped as historical runtime-first program / boundary-map provenance. They are not current execution order, current local runtime ladder, active R1-R5 backlog, default runtime owner, hosted runtime claim or P5 expansion authority.
- R2.A and R3.A are correctly scoped as `historical_activation_package` records. Their current machine behavior must be read through grouped public CLI/source/contracts: `build-artifact-bundle` maps to `package artifact-bundle`; `execute-revision-pass` maps to `pass revision`.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, and `mag_owns_attempt_ledger=false`.
- `MagDomainRuntime().describe_topology()` still reports `runtime_owner=one-person-lab`, `can_claim_generic_runtime_owner=False`, `default_formal_entry=CLI`, `supported_protocol_layer=MCP`, `internal_controller_surface=controller`, and `optional_proof_executor_boundary=explicit opt-in only`.
- Current public CLI shape is grouped: R2 package behavior is under `package artifact-bundle`; R3 revision behavior is under `pass revision`; historical bare command examples remain provenance and must not be copied into current operator docs without mapping through `public_cli`.
- `runtime-run`、`runtime-resume`、`run-local` and `probe-upstream-hermes` remain retired/no-resurrection terms covered by source/tests; they must not be restored as active public/domain commands from these history docs.
- Stale-risk scan found R2/R3/runtime-first risk terms only inside lifecycle-guarded history/provenance text, explicit future-scope/precondition/stop-condition guardrails, current-source CLI mapping, or no-resurrection surfaces. No body rewrite was needed; this tranche records paragraph coverage and confirms the existing lifecycle guard plus specs lifecycle map are sufficient.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-08 R2/R3/runtime-first history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, status, current-program runtime owner fields, grouped public CLI mapping, domain runtime topology and retired command no-resurrection surfaces. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone 或正文删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch、2026-04-07 P2/P3A batch、2026-04-08 P3/P4 batch、2026-04-08 P5/R1 batch and this 2026-04-08 R2/R3/runtime-first batch are not paragraph-governed in this tranche.
- Higher-risk remaining MAG batches include 2026-04-09 R3/R4/R5 / post-R5A records, 2026-04-10 fail-closed / hosted-bundle records, 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted/OPL handoff records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later OPL global ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these runtime-first docs as current execution order, active local runtime ladder, runtime owner, default runtime, public `runtime-run` / `runtime-resume`, local run journal, attempt ledger, hosted runtime readiness, P5 expansion, controller capability, submission/export-ready verdict, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical bare `build-artifact-bundle` and `execute-revision-pass` command examples must be mapped through current grouped public CLI as `package artifact-bundle` and `pass revision`; otherwise they are old local-runtime provenance, not active operator docs.
- `artifact_bundle`、revision executor、final package and hosted-friendly vocabulary must remain within grant/package/export authority and grouped CLI boundaries. They must not be upgraded to generic OPL artifact lifecycle owner, App/release readiness, production-ready claim, external submission authorization or provider-hosted completion.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing 2026-04-09 R3/R4/R5 / post-R5A records or 2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale local-runtime/provider/hosted wording risk is higher there.
- Or switch to RCA uncovered reference bodies or App docs once their main checkout and active worktrees are safe.
