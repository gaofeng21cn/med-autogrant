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

### 2026-05-29 Hermes/reset/local-runtime history specs revalidation tranche

本轮在 OPL series fresh hygiene scan 后，重新验证 MAG
`docs/history/specs/` 下已由 2026-05-26 ledger 覆盖过的 4 份 2026-04-11
Hermes/reset/local-runtime 历史 specs。目标是确认 recent main 语境下，这些
direct-file 历史入口仍不会把旧 Hermes-backed runtime substrate、upstream
Hermes-Agent reset、post-R5A local runtime honest-stop、`runtime-run` /
`runtime-resume`、local journal、host-agent、Gateway/local-manager 或
compatibility bridge wording 误读成当前 MAG runtime owner、default provider、
attempt ledger、local runtime command alias、production hosted path、
App/workbench readiness、production readiness、submission/export-ready verdict、
physical-delete authority 或 active backlog。本轮不改 active truth，不关闭
OPL series 全局 `/goal`。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、
  `docs/active/mag-ideal-state-cross-repo-gap-plan.md`、
  `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、
  `docs/history/specs/README.md` 和本文件。
- Reviewed history specs:
  `docs/history/specs/2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md`,
  `docs/history/specs/2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md`,
  `docs/history/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`,
  `docs/history/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`。
- Machine/source/test truth:
  `contracts/runtime-program/current-program.json`,
  `contracts/production_acceptance/mag-production-acceptance.json`,
  `contracts/runtime-program/opl-family-contract-adoption.json`,
  `tests/test_repository_hygiene.py`, `tests/test_opl_standard_pack.py` and
  `tests/test_production_acceptance.py`。
- Fresh repo state: MAG tranche worktree created from `origin/main` at
  `e8ae6c23ede3`; branch `codex/mag-doc-governance-20260529-0411-history`
  started clean and aligned with `origin/main`; remote-only
  `origin/feature/ai-narration-contracts` remains preserved as external,
  non-codex history.

Fresh semantic result：

- All four reviewed files carry `Owner` / `Purpose` / `State` /
  `Machine boundary` metadata and are already in `State: history`. Their
  lifecycle notes route current truth back to core docs, active plan, specs
  lifecycle map, contracts/schema/source/CLI behavior and
  `current-program.json`.
- The two `hermes-backed-*` files remain superseded provider-proof provenance.
  They describe a historical proposal for Hermes-backed runtime substrate /
  capability split, not the current default runtime owner, provider owner,
  compatibility bridge or required runnable path. `hermes_agent` remains only
  an explicit non-default executor / proof / provenance lane.
- The post-R5A local runtime honest-stop file remains historical local-runtime
  closeout provenance. Its old command catalog, local journal, host-agent ladder
  and bare command examples do not re-admit MAG-owned daemon、scheduler、attempt
  loop、attempt ledger、local runtime command alias、Hermes-backed default
  provider or hosted runtime readiness.
- The upstream Hermes-Agent truth-reset file remains retired provider-proof
  provenance. It records the 2026-04-11 reset that repo-local runtime helper
  code did not equal upstream Hermes-Agent integration; it is not a current
  instruction to restore Hermes/Gateway/local-manager ownership.
- Current machine truth still says OPL/Temporal is the default task runtime
  owner, `Codex CLI` is the default stage executor, MAG does not implement
  daemon/scheduler/attempt loop/attempt ledger, physical delete is not
  authorized, OPL/provider completion cannot authorize grant/fundability/
  submission readiness, and Temporal/provider long-soak remains open.
- Focused tests reinforce the same boundary: repository hygiene and standard
  pack tests keep retired public commands, generated surface ownership and
  physical delete authority guarded; production acceptance tests reject
  provider-completion upgrades to fundability/domain/submission readiness.
- No prose body rewrite was needed. The 2026-05-26 ledger remains the original
  body-coverage closeout for this batch; this tranche records fresh
  currentness revalidation against current contracts/tests/source guards.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Fresh revalidation read of all four 2026-04-11 Hermes/reset/local-runtime history specs; support read of specs lifecycle map, specs index, history specs index, core docs, active plan, current-program runtime owner fields, production acceptance contract, OPL-family contract adoption contract and focused boundary tests. | this coverage ledger |

Archived / tombstoned / deleted docs：无。这 4 份文件仍是有用的 history
provenance；不需要移动、tombstone、删除或正文重写。

Uncovered docs：

- `med-autogrant`: this revalidation opened no new uncovered `README*` /
  `docs/**/*.md` path in the current recorded MAG governance scope. Future MAG
  docs or source/contract changes can still reopen specific sections.
- Other OPL-series repos remain governed by the global coverage ledger and the
  final six-repo sweep. OPL、MAS、RCA、`opl-meta-agent` and App status must be
  carried from their own current ledgers and active worktree safety before the
  global `/goal` can close.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-11 files as current default
  provider, MAG-owned generic runtime, Hermes/Gateway/local-manager active
  route, compatibility bridge, local command alias, attempt ledger owner,
  production hosted path, App/workbench readiness, production readiness,
  submission/export-ready verdict or physical-delete authority is stale
  pollution.
- Historical `runtime-run` / `runtime-resume`、local journal、host-agent、
  Gateway、Hermes-backed substrate、future Hermes host、truth-reset "next step"
  wording and local runtime helper claims must remain provenance unless current
  source/contracts/tests and active owner docs explicitly re-admit an exact
  boundary.
- MAG implementation/evidence tails remain source/test/receipt work: physical
  delete authorization, production long-soak, submission-ready human gate,
  sustained real App/operator consumption and long-soak evidence.

Next tranche write scope：

- Prefer OPL / MAS / RCA safe document clusters for the next OPL-series tranche
  while App release docs remain tied to dirty or conflicting release lanes.
- Return to MAG only if new MAG docs appear, later code/contract changes reopen
  a section, or an implementation/evidence owner lane closes one of the
  remaining runtime/evidence/physical-cleanup tails and requires doc foldback.

### 2026-05-29 post-R5A fail-closed / hosted-bundle history specs tranche

本轮在 OPL series fresh hygiene scan 后，覆盖 MAG `docs/history/specs/`
下 26 份 `2026-04-10-post-r5a-*.md` 历史 specs。目标是确认这些
direct-file 历史入口不会把旧 local-runtime hardening、`ready for implementation`
状态、fail-closed activation package、hosted-contract bundle、Gateway、host-agent、
bare runtime command 或 worktree/root-resolution wording 误读成当前 runtime owner、
formal entry、hosted runtime completion、App/workbench readiness、production readiness、
submission/export-ready verdict、physical-delete authority 或 active backlog。本轮不改
active truth，不关闭 OPL series 全局 `/goal`。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、
  `docs/active/mag-ideal-state-cross-repo-gap-plan.md`、
  `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、
  `docs/history/specs/README.md` 和本文件。
- Reviewed history specs: all 26 files matching
  `docs/history/specs/2026-04-10-post-r5a-*.md`, grouped as 15
  final-package artifact-bundle fail-closed specs, 6 hosted-contract-bundle
  final-package fail-closed specs, and 5 local-runtime / stage-route /
  revised-workspace / worktree-aware root-resolution records.
- Machine/source/test truth:
  `contracts/runtime-program/current-program.json`,
  `contracts/production_acceptance/mag-production-acceptance.json`,
  `contracts/runtime-program/opl-family-contract-adoption.json`,
  `tests/test_repository_hygiene.py`, `tests/test_opl_standard_pack.py`, and
  `tests/test_production_acceptance.py`.
- Fresh repo state: MAG `main...origin/main = 0 0`, root checkout clean before
  this edit, no extra local MAG worktree, and the only remote-only branch is
  non-codex `origin/feature/ai-narration-contracts`, retained as external
  history.

Fresh semantic result：

- All 26 reviewed files carry `Owner` / `Purpose` / `State` /
  `Machine boundary` metadata and are already in `State: history`. Their first
  screen lifecycle notes or machine boundaries route current truth back to core
  docs, active plan, specs lifecycle map, contracts/schema/source/CLI behavior
  and `current-program.json`.
- The 15 final-package artifact-bundle files remain historical fail-closed
  hardening provenance for `build-final-package` input validation. Their
  Promotion Invariants keep `build-final-package` as local finalization/export
  surface and explicitly prevent fallback, default-value patching, new formal
  entry, `P5` expansion or actual hosted runtime semantics.
- The 6 hosted-contract-bundle files remain historical fail-closed hardening
  provenance for `build-hosted-contract-bundle` consuming a complete final
  package. Their machine boundaries say current hosted/default task runtime
  owner is OPL/Temporal, hosted-contract bundle is local hostedization-prep /
  export provenance, and the files do not declare public hosted runtime、App
  release ready or production ready.
- The local-runtime validation, local walkthrough, stage-route checkpoint,
  revised-workspace/operator and worktree-aware root-resolution records remain
  local closeout / path-resolution / checkpoint-output provenance. Current
  route checkpoint aggregation, validation behavior, runtime owner and grouped
  CLI behavior stay with core docs、active plan、contracts/schema/source/tests
  and `current-program.json`.
- Current machine truth still says OPL/Temporal is the default task runtime
  owner, `Codex CLI` is the default stage executor, MAG does not implement
  daemon/scheduler/attempt loop/attempt ledger, physical delete is not
  authorized, OPL/provider completion cannot authorize grant/fundability/
  submission readiness, and Temporal/provider long-soak remains open.
- Focused tests reinforce the same boundary: repository hygiene blocks retired
  compatibility/local-state revival claims; standard-pack tests keep generated
  surface ownership in OPL and physical delete unauthorized; production
  acceptance requires MAG owner receipt / typed blocker / no-regression refs
  and rejects provider-readiness upgrades.
- No prose body rewrite was needed. This tranche records full paragraph-level
  coverage over the 2026-04-10 post-R5A fail-closed / hosted-bundle history
  body batch.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of all 26 `docs/history/specs/2026-04-10-post-r5a-*.md` bodies; support read of specs lifecycle map, specs index, history specs index, core docs, active plan, current-program runtime owner fields, production acceptance contract, OPL-family contract adoption contract and focused boundary tests. | this coverage ledger |

Archived / tombstoned / deleted docs：无。这 26 份文件仍是有用的 history
provenance；不需要移动、tombstone、删除或正文重写。

Uncovered docs：

- `med-autogrant`: this tranche closes the 2026-04-10 post-R5A fail-closed /
  hosted-bundle history body batch. Remaining higher-risk history body batches
  still include 2026-04-08 P5 / R-series activation packages,
  2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted / OPL
  handoff records unless covered by prior date/topic tranche entries.
- Other OPL-series repos remain governed by the global coverage ledger. OPL、
  MAS、RCA and App still need their own remaining section-level coverage /
  safe-lane reconciliation before the global `/goal` can close.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-10 files as current formal entry,
  MAG-owned generic runtime, actual hosted runtime completion, App/workbench
  readiness, production readiness, submission/export-ready verdict,
  physical-delete authority, active Gateway/local-manager route, old bare
  runtime command contract or compatibility-interface source is stale pollution.
- Historical `runtime-run` / `runtime-resume`、host-agent、Gateway、
  hostedization prep、`ready for implementation` and local-runtime hardening
  vocabulary must remain provenance unless current source/contracts/tests and
  active owner docs explicitly re-admit an exact boundary.
- MAG implementation/evidence tails remain source/test/receipt work: physical
  delete authorization, production long-soak, submission-ready human gate,
  sustained real App/operator consumption and long-soak evidence.

Next tranche write scope：

- Continue MAG history body coverage only if needed by global coverage,
  prioritizing 2026-04-11 Hermes/reset/local-runtime records or 2026-04-12
  hosted / OPL handoff specs because stale provider and hosted wording risk is
  higher there.
- Prefer OPL / MAS / RCA safe document clusters for the next OPL-series tranche
  while App release docs remain tied to dirty or conflicting release lanes.

### 2026-05-29 P3/P4 rollback and verification history specs tranche

本轮在 OPL series branch/worktree hygiene 后，覆盖 MAG `docs/history/specs/`
下 2026-04-08 P3/P4 rollback、presubmission、verification gate 与 checkpoint
历史 specs。目标是确认这些 direct-file 历史入口不会把旧 `Current Truth`
标题、CLI-only verification gate、presubmission hard gate、checkpoint vocabulary
或 activation status 误读成当前 runtime owner、formal entry、submission/export
ready、App/workbench readiness、production readiness、physical delete authority
或 active backlog。本轮不改 active truth，不关闭 OPL series 全局 `/goal`。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、
  `docs/active/mag-ideal-state-cross-repo-gap-plan.md`、
  `docs/references/med-auto-grant-ideal-state.md`、
  `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、
  `docs/history/specs/README.md` 和本文件。
- Reviewed history specs:
  `docs/history/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`,
  `docs/history/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`,
  `docs/history/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`,
  `docs/history/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`。
- Machine/source/test truth:
  `contracts/runtime-program/current-program.json`,
  `contracts/production_acceptance/mag-production-acceptance.json`,
  `tests/test_repository_hygiene.py`, `tests/test_opl_standard_pack.py`,
  and `tests/test_production_acceptance.py`。
- Fresh repo state: MAG `main...origin/main = 0 0`, no open PR,
  previously stale clean `codex/mag-doc-governance-20260529` worktree/branch
  was already equal to `main` and removed before this tranche; doctor
  `finding_count=0` / active truth `pass`。

Fresh semantic result：

- All four reviewed specs already carry first-screen lifecycle notes plus
  `Owner` / `Purpose` / `State` / `Machine boundary`. Their old `Current Truth`
  titles are explicitly subordinated to current core docs, active specs,
  contracts/schema/source, CLI/API behavior and `current-program.json`.
- P3.B remains historical revision transition / re-review evidence provenance.
  Current critique/revision and AI-first quality boundaries live in active specs,
  source/contracts/tests, not this dated file.
- P3.C remains historical forced rollback / presubmission gate provenance.
  Current authoring completion, rollback and `submission_ready_export_gate`
  ownership stay with active specs, package/export support surfaces,
  owner receipt / typed blocker contracts and current status docs.
- P4.A remains historical verification gate surface provenance. Current
  verification entry is `scripts/verify.sh` plus current CLI/API/source/tests;
  historical command lists do not become today's formal verification contract.
- P4.B remains historical checkpoint surface provenance. `VerificationCheckpoint`
  is historical planning context unless current source/contracts/read-model
  expose a live route checkpoint; it is not a new formal entry, runtime identity,
  controller capability or schema owner.
- `docs/specs/specs_lifecycle_map.md`, `docs/specs/README.md` and
  `docs/history/specs/README.md` still route this whole P3/P4 batch to
  `historical_review_gate_provenance` / `historical_verification_gate_provenance`
  and point current route、quality、checkpoint and verification truth back to
  core docs、active specs、contracts/schema/source and `current-program.json`.
- Current machine truth still says OPL/Temporal is the default task runtime
  owner, `Codex CLI` is the default stage executor, MAG does not implement
  daemon/scheduler/attempt loop/attempt ledger, OPL/provider completion cannot
  authorize grant/fundability/submission readiness, and physical delete remains
  unauthorized.
- Repository hygiene / standard-pack / production-acceptance tests reinforce the
  same boundary: retired compatibility claims must not reappear; OPL default
  caller evidence does not grant delete authority; production acceptance accepts
  MAG owner receipt / typed blocker / no-regression refs only.
- No prose body rewrite was needed. This tranche records full paragraph-level
  coverage over the P3/P4 rollback and verification history body batch.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-08 P3/P4 history specs listed above; support read of specs lifecycle map, specs index, history specs index, core docs, active plan, ideal-state reference, current-program runtime owner fields, production acceptance contract and focused boundary tests. | this coverage ledger |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history
provenance；不需要移动、tombstone、删除或正文重写。

Uncovered docs：

- `med-autogrant`: this tranche closes the current P3/P4 rollback and
  verification history body batch. Remaining higher-risk history body batches
  still include 2026-04-08 P5 / R-series activation packages, 2026-04-10
  post-R5A fail-closed / hosted-bundle records, 2026-04-11
  Hermes/reset/local-runtime records and 2026-04-12 hosted / OPL handoff records
  unless covered by prior date/topic tranche entries.
- Other OPL-series repos remain governed by the global coverage ledger. OPL、
  MAS、RCA and App still need their own remaining section-level coverage /
  safe-lane reconciliation before the global `/goal` can close.

Remaining stale / retire candidates：

- Any future direct-file use of these P3/P4 specs as current formal entry,
  runtime owner, public CLI command shape, active verification contract,
  submission/export-ready verdict, production readiness, App/workbench readiness,
  physical-delete authority or compatibility-interface source is stale pollution.
- Historical `ready_for_submission`、`presubmission_frozen`、`VerificationCheckpoint`
  and checkpoint vocabulary must remain provenance unless current source,
  contracts, tests and active owner docs explicitly re-admit the exact boundary.
- MAG implementation/evidence tails remain source/test/receipt work: physical
  delete authorization, production long-soak, submission-ready human gate,
  sustained real App/operator consumption and long-soak evidence.

Next tranche write scope：

- Continue MAG history body coverage only if needed by global coverage,
  prioritizing 2026-04-10 fail-closed / hosted-bundle records or
  2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale provider
  and hosted wording risk is higher there.
- Prefer OPL / MAS / RCA safe document clusters for the next OPL-series tranche
  while App release docs remain tied to dirty or conflicting release lanes.

### 2026-05-29 specs lifecycle / history direct-reader currentness tranche

本轮在 OPL series fresh hygiene scan 后，复核 MAG specs lifecycle map、
active specs、history specs/plans 索引和相关 machine guards。目标是确认
direct-file reader 仍会被引回当前核心五件套、active plan、current-program、
contracts/schema/source/tests，而不会把旧 `Current Truth` 标题、Hermes/Gateway
/ local-runtime wording、hosted proof 或 historical activation package 误读成
当前 runtime owner、retired interface surface、production readiness、physical
delete authorization 或 active backlog。本轮不关闭 MAG evidence tails，不重写产品事实，
不声明全仓 docs/global `/goal` complete。

Live truth inputs：

- MAG repo guidance and current docs: `AGENTS.md`, `TASTE.md`, core five docs,
  `docs/README.md`, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, and
  this docs portfolio ledger.
- Specs / history docs: `docs/specs/README.md`,
  `docs/specs/specs_lifecycle_map.md`, the four active specs listed there,
  `docs/history/specs/README.md`, and `docs/history/plans/README.md`.
- Machine/source/test truth:
  `contracts/runtime-program/current-program.json`,
  `contracts/production_acceptance/mag-production-acceptance.json`,
  `contracts/runtime-program/opl-family-contract-adoption.json`,
  `tests/test_repository_hygiene.py`, `tests/test_opl_standard_pack.py`, and
  `tests/test_production_acceptance.py`.
- Fresh repo state: MAG `main...origin/main = 0 0`, root checkout clean before
  this docs-governance worktree, open PR scan `[]`, and doctor
  `finding_count=0` / active truth `pass`.

Fresh semantic result：

- `docs/specs/README.md` and `docs/specs/specs_lifecycle_map.md` still make the
  active current specs explicit: critique Codex CLI executor vocabulary,
  AI-first quality boundary, authoring completion semantics, and
  quality/autonomy/family grammar. Each active spec has owner/purpose/state and
  machine-boundary headers, and scopes its authority to a named boundary rather
  than all product/runtime/readiness truth.
- The specs lifecycle map still classifies remaining support records by current
  subsection and routes pure historical P/R/post-R5A/provider/handoff records to
  `docs/history/specs/`.
- `docs/history/specs/README.md` and `docs/history/plans/README.md` continue to
  mark historical specs/plans as provenance. Their directory-level machine
  boundaries prevent old `Current Truth`, activation status, Hermes/Gateway,
  hosted, local-runtime, `runtime-run`, `runtime-resume`, local journal and
  attempt-ledger wording from becoming current owner lines.
- Current machine refs still say OPL/Temporal is the default task runtime owner,
  `codex_cli` is the default stage executor, MAG does not implement daemon /
  scheduler / attempt loop / attempt ledger, OPL cannot authorize grant or
  fundability readiness, provider completion is not submission-ready, and
  Temporal/provider long-soak remains open.
- Tests reinforce the same boundary: repository hygiene blocks local-state and
  retired-interface revival claims; standard-pack tests keep retired aliases
  disabled and physical delete unauthorized; production-acceptance tests require
  MAG owner receipt / typed blocker refs and reject OPL/provider readiness
  upgrades.
- No body rewrite was needed. This tranche records paragraph-level currentness
  coverage over the specs lifecycle owner/index layer and the active-spec
  boundary set.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Specs lifecycle owner/index layer: `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, active specs for critique executor vocabulary, AI-first quality boundary, authoring completion semantics and quality/autonomy/family grammar, plus `docs/history/specs/README.md`, `docs/history/plans/README.md`, core docs and machine/test refs listed above. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。本轮未发现 specs lifecycle map、active specs
或 history indexes 需要移动、tombstone、删除或正文重写。

Uncovered docs：

- `med-autogrant`: this tranche does not claim a full paragraph reread of every
  `docs/history/specs/*.md` body. It closes the current specs lifecycle owner /
  direct-reader guard layer and the four active current-spec bodies.
- Remaining higher-risk history body batches still include 2026-04-08 P3/P4
  rollback / verification gate records, 2026-04-08 P5 / R-series activation
  packages, 2026-04-09 R3/R4/R5 / post-R5A records, 2026-04-10 fail-closed /
  hosted-bundle records, 2026-04-11 Hermes/reset/local-runtime records and
  2026-04-12 hosted/OPL handoff records unless covered by prior specific
  tranche entries.

Remaining stale / retire candidates：

- Future specs or history prose that upgrades lifecycle map entries, active spec
  titles, hosted proof, OPL projection, provider completion, refs-only payload /
  ledger verification or historical activation-package completion into
  grant-domain ready, fundability ready, submission/export ready, production
  ready, MAG-owned generic runtime, App/workbench ownership, physical delete
  authority, or retired interface revival is stale pollution.
- MAG evidence/implementation tails remain source/test/receipt work: physical
  delete authorization, production long-soak, submission-ready human gate,
  sustained real App/operator consumption and long-soak evidence.

Next tranche write scope：

- Continue OPL series whole-docs coverage outside MAG, or return to MAG for
  remaining high-risk history body batches / newly changed docs / source or
  contract changes that reopen a specs boundary.

### 2026-05-28 MAG current entry / core index revalidation tranche

本轮在 OPL series fresh hygiene scan 后，重新复核 MAG 当前入口与核心索引簇，确认 2026-05-28 sustained-consumption payload follow-through 之后，MAG docs 仍保持 single active truth owner、single north-star reference、history/specs lifecycle guard 和 thin support index 边界。本轮不重写产品事实、不关闭 MAG evidence tails、不声明全仓 docs/global `/goal` complete。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、root `README.md`、`README.zh-CN.md`、`agent/README.md`、`contracts/README.md`、`runtime/README.md`、`docs/README.md`、核心五件套、`docs/active/README.md`、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/active/opl-private-implementation-migration-inventory.md`、`docs/docs_portfolio_consolidation.md`、thin support indexes、specs/history indexes 和 north-star reference `docs/references/med-auto-grant-ideal-state.md`。
- Machine/source truth：`contracts/runtime-program/current-program.json`、`contracts/domain_descriptor.json`、`contracts/pack_compiler_input.json`、`contracts/functional_privatization_audit.json`、`contracts/production_acceptance/mag-manifest-sustained-consumption-evidence-20260528.json`、`contracts/stage_control_plane.json`、package/test entry inventory 和 OPL Doc Governance doctor。
- Fresh repo state：MAG `main...origin/main = 0 0`、root checkout clean、no local MAG extra worktree before this docs-governance worktree、open PR scan `[]`、doctor `finding_count=0` and active truth `pass`。

Fresh semantic result：

- Root `README*` remains a public entry; `docs/README.md` remains the second-level technical routing index; core five docs hold current role/status/architecture/invariants/decisions; `docs/active/mag-ideal-state-cross-repo-gap-plan.md` remains the single active truth owner for current progress、gaps and next-round prompt.
- `docs/references/med-auto-grant-ideal-state.md` remains the north-star target-state reference. `docs/active/opl-private-implementation-migration-inventory.md` remains the physical morphology / private platform residue inventory; it does not replace the active gap plan.
- `agent/README.md` is the human index for the Declarative Grant Pack. Non-README `agent/**/*.md` files are pack semantic inputs consumed through `contracts/pack_compiler_input.json`; they are not docs-lifecycle owner docs and do not need separate owner/purpose/state/machine-boundary headers.
- `contracts/README.md` and `runtime/README.md` continue to index machine contracts and runtime descriptor boundaries without making prose paths machine interfaces.
- Thin support indexes under `docs/product/`、`docs/runtime/`、`docs/delivery/`、`docs/source/` and `docs/policies/` still only route readers to current owner docs/contracts; they do not duplicate active truth.
- `docs/specs/README.md` and `docs/specs/specs_lifecycle_map.md` still guard active/support specs; `docs/history/**` indexes still keep historical `Current Truth` titles and Hermes/Gateway/local-runtime wording inside provenance context.
- Current contracts still say OPL/Temporal owns the default task runtime, `Codex CLI` is the default stage executor, MAG does not implement daemon/scheduler/attempt loop/attempt ledger, physical delete is not authorized, and production long-soak is not complete. MAG docs must continue to treat sustained-consumption payload response and OPL record/verify as refs-only evidence, not grant-ready、submission-ready、App sustained-consumption complete or production-ready proof.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Current entry/core index cluster: root `README*`, `agent/README.md`, `contracts/README.md`, `runtime/README.md`, `docs/README.md`, core five docs, active README/plan/inventory, docs portfolio, thin support indexes, specs/history indexes and north-star reference; support read of key contracts/source/test inventory and doctor risk map. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。本轮未发现当前入口或核心索引簇需要移动、tombstone、删除或正文重写。

Uncovered docs：

- `med-autogrant`: this tranche only revalidates the current entry/core index cluster. It does not claim a new full paragraph reread of every historical spec body beyond previously recorded MAG date/topic coverage and exact inventory reconcile entries.
- Other OPL-series repos remain governed by the global coverage ledger; global `/goal` stays active.

Remaining stale / retire candidates：

- MAG evidence/implementation tails remain open as source/test/receipt work: physical delete authorization、production long-soak、submission-ready human gate、sustained real App/operator consumption and long-soak evidence.
- Future MAG prose that upgrades refs-only payload/ledger verification、zero docs inventory gap、OPL projection、Temporal provider completion、support README indexes or optional Hermes proof lane into grant-domain ready、fundability ready、submission/export ready、production ready、MAG-owned generic runtime、App/workbench ownership or physical delete authority is stale pollution.

Next tranche write scope：

- Continue OPL series whole-docs coverage outside MAG, or return to MAG only if new MAG docs appear, source/contract changes reopen a section, or an implementation/evidence owner lane closes one of the remaining runtime/evidence/physical-cleanup tails and needs doc foldback.

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

### 2026-05-26 2026-04-09 R3/R4/R5 post-R5A history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-09 R3 revision mutation、R4 final freeze/export、R5 hosted-friendly session boundary 与 post-R5A local runtime hardening 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 machine-applicable revision contract、final package、hosted contract bundle、local runtime ladder、`runtime-run` / `runtime-resume`、run journal、host-agent、hostedization 或 post-R5A hardening owner line 误读成当前 public CLI shape、MAG-owned generic runtime、active local runtime plan、attempt ledger、actual hosted runtime、OPL/App production readiness、submission/export-ready verdict、compatibility interface 或 active implementation queue。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`, `docs/history/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`, `docs/history/specs/2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md`, `docs/history/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/cli.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/final_package.py`, `src/med_autogrant/hosted_contract_bundle.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, `tests/test_domain_entry.py`, `tests/test_final_package.py`, `tests/test_hosted_contract_bundle.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh read-model probes: `MagDomainRuntime().describe_topology()`, `public_cli_command()` mapping for `execute-revision-pass` / `build-artifact-bundle` / `build-final-package` / `build-hosted-contract-bundle`, `PUBLIC_GROUP_COMMANDS["package"]`, `PUBLIC_GROUP_COMMANDS["pass"]`, retired public command scan, `med_autogrant package --help`, and `med_autogrant pass --help`.

Fresh semantic result：

- All four reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- R3.A is correctly scoped as historical revision mutation contract provenance. Current revision behavior must be read through source/tests and grouped public CLI: `execute-revision-pass` maps to `pass revision`; this history file does not authorize runtime queue、attempt ledger、hosted runtime owner、final package/export authority or a new authoring engine.
- R4.A is correctly scoped as historical final freeze/export activation provenance. Current package/export behavior must be read through MAG package authority, source/tests and grouped public CLI: `build-final-package` maps to `package final-package`; final package vocabulary must not be upgraded to hosted runtime、external submission approval、App/release readiness or production-ready claims.
- R5.A is correctly scoped as historical hosted-friendly session boundary provenance. Current hosted/default task runtime owner remains OPL/Temporal, and current hosted contract behavior is grouped as `package hosted-contract-bundle`; the file does not grant actual hosted runtime、Gateway owner、daemon、scheduler、attempt ledger、multi-tenant platform、credits/billing or federation authority.
- Post-R5A local runtime hardening is correctly scoped as historical local-runtime closeout / honest-stop provenance. Its local runtime ladder and host-agent wording are not current owner line; current owner line in `current-program.json` is OPL/Temporal hosted autonomous runtime default, with `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, and `mag_owns_attempt_ledger=false`.
- `MagDomainRuntime().describe_topology()` still reports `runtime_owner=one-person-lab`, `can_claim_generic_runtime_owner=False`, `default_formal_entry=CLI`, `supported_protocol_layer=MCP`, `internal_controller_surface=controller`, and `optional_proof_executor_boundary=explicit opt-in only`.
- Current public CLI shape is grouped: revision is under `pass revision`; package behavior is under `package artifact-bundle`, `package final-package`, `package hosted-contract-bundle`, and `package submission-ready`. Historical bare command examples remain provenance and must not be copied into current operator docs without mapping through `public_cli`.
- `run-local`、`runtime-run`、`runtime-resume` and `probe-upstream-hermes` remain retired/no-resurrection terms. The retired command scan returned `state=passed`, no active domain-entry command matches, and no active grouped public CLI command matches.
- Stale-risk scan found R3/R4/R5/post-R5A risk terms only inside lifecycle-guarded history/provenance text, explicit future-scope/precondition/stop-condition guardrails, current-source CLI mapping, or no-resurrection surfaces. No body rewrite was needed; this tranche records paragraph coverage and confirms the existing lifecycle guard plus specs lifecycle map are sufficient.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-09 history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner fields, grouped public CLI mapping, domain runtime topology, final package / hosted contract source, and retired command no-resurrection surfaces. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone 或正文删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch、2026-04-07 P2/P3A batch、2026-04-08 P3/P4 batch、2026-04-08 P5/R1 batch、2026-04-08 R2/R3/runtime-first batch and this 2026-04-09 R3/R4/R5/post-R5A batch are not paragraph-governed in this tranche.
- Higher-risk remaining MAG batches include 2026-04-10 fail-closed / hosted-bundle records, 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted/OPL handoff records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later OPL global ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-09 specs as current public CLI command shape, runtime owner, default runtime, active local runtime ladder, hosted runtime owner, run journal, attempt ledger, Gateway/federation readiness, controller public formal entry, submission/export-ready verdict, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical bare `execute-revision-pass`、`build-artifact-bundle`、`build-final-package` and `build-hosted-contract-bundle` examples must be mapped through current grouped public CLI as `pass revision`, `package artifact-bundle`, `package final-package` and `package hosted-contract-bundle`; otherwise they are old local-runtime provenance, not active operator docs.
- `final_package`、`hosted_contract_bundle`、hosted-friendly and post-R5A hardening vocabulary must remain within grant package/export authority, hosted-contract export reference, and history/provenance boundaries. They must not be upgraded to generic OPL artifact lifecycle owner, actual hosted runtime, App/release readiness, external submission authorization, provider-hosted completion or production-ready claim.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing 2026-04-10 fail-closed / hosted-bundle records or 2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale provider/hosted wording risk is higher there.
- Or switch to RCA uncovered reference bodies or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-10 hosted-contract bundle fail-closed history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-10 hosted-contract-bundle final-package fail-closed 与 worktree-aware root resolution 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 hostedization prep、host-agent、Gateway、final package malformed/fail-closed validation、worktree-aware control-plane root resolution 或 `CURRENT_PROGRAM` root lookup 词汇误读成当前 actual hosted runtime、MAG-owned generic runtime、public hosted runtime、App release ready、production ready、daemon/scheduler/attempt ledger、compatibility interface 或 active implementation queue。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-10-post-r5a-hosted-contract-bundle-final-package-checkpoint-semantics-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-hosted-contract-bundle-final-package-freeze-manifest-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-hosted-contract-bundle-final-package-lineage-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-hosted-contract-bundle-final-package-required-nested-fields-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-hosted-contract-bundle-final-package-required-scalar-fields-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-hosted-contract-bundle-malformed-final-package-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-worktree-aware-hosted-contract-control-plane-root-resolution-activation-package.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/hosted_contract_bundle.py`, `src/med_autogrant/final_package_validation.py`, `src/med_autogrant/domain_runtime_parts/contracts.py`, `src/med_autogrant/public_cli.py`, `tests/test_hosted_contract_bundle.py`, `tests/test_hosted_contract_bundle_checkpoint_cases.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh verification probes: `med_autogrant package --help`, `public_cli_command()` mapping for `build-final-package` / `build-hosted-contract-bundle`, retired public command scan, and focused pytest for hosted-contract bundle fail-closed cases.

Fresh semantic result：

- All seven reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- The five `hosted-contract-bundle-final-package-*` specs and the malformed final-package spec are correctly scoped as historical post-R5A hosted-contract final-package fail-closed provenance. Current behavior is source/test owned by `hosted_contract_bundle.build_hosted_contract_bundle_payload()` and `final_package_validation._validate_required_final_package_fields()`, which validate supported package version, required scalar/object fields, required freeze manifest and lineage fields, allowed draft/checkpoint statuses, and checkpoint status consistency before hosted bundle export.
- The worktree-aware root resolution spec is correctly scoped as historical control-plane root resolution provenance. It only describes deterministic `CURRENT_PROGRAM` lookup hardening; it does not change `program_id` semantics, final package identity, hosted bundle payload shape, formal entry, hosted runtime semantics, or runtime owner.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_owner=configured_family_runtime_provider`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, `mag_owns_attempt_ledger=false`, `default_stage_executor=codex_cli`, and `optional_hosted_carriers=["hermes_agent"]`.
- Current public CLI shape is grouped: `build-final-package` maps to `package final-package`; `build-hosted-contract-bundle` maps to `package hosted-contract-bundle`. Historical bare command examples remain provenance and must not be copied into current operator docs without mapping through `public_cli`.
- Focused hosted-contract bundle verification passed: `tests/test_hosted_contract_bundle.py` and `tests/test_hosted_contract_bundle_checkpoint_cases.py` returned 21 pytest cases plus 30 subtests passed. `med_autogrant package --help` shows `artifact-bundle`, `final-package`, `hosted-contract-bundle`, and `submission-ready` as current package commands.
- No body rewrite was needed. This tranche records paragraph coverage and confirms the existing lifecycle guard plus specs lifecycle map are sufficient.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the seven 2026-04-10 hosted-contract bundle fail-closed / worktree-aware history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner fields, hosted contract source, final package validation source, grouped public CLI mapping and focused hosted bundle tests. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。这七份文件仍是有用的 history provenance；不需要移动、tombstone 或正文删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch、2026-04-07 P2/P3A batch、2026-04-08 P3/P4 batch、2026-04-08 P5/R1 batch、2026-04-08 R2/R3/runtime-first batch、2026-04-09 R3/R4/R5/post-R5A batch and this 2026-04-10 hosted-contract bundle fail-closed batch are not paragraph-governed in this tranche.
- Higher-risk remaining MAG batches include 2026-04-10 local-runtime validation / stage-route / revised / walkthrough records, 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted/OPL handoff records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later OPL global ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-10 specs as current public CLI command shape, runtime owner, default runtime, actual hosted runtime, public hosted runtime, Gateway/federation readiness, daemon/scheduler/attempt ledger, controller public formal entry, submission/export-ready verdict, App release readiness, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical bare `build-final-package` and `build-hosted-contract-bundle` examples must be mapped through current grouped public CLI as `package final-package` and `package hosted-contract-bundle`; otherwise they are old local-runtime / hostedization-prep provenance, not active operator docs.
- `final_package` malformed/fail-closed, hosted-contract bundle and worktree-aware `CURRENT_PROGRAM` lookup vocabulary must remain within grant package/export authority, hosted-contract export reference, deterministic root resolution and history/provenance boundaries. They must not be upgraded to generic OPL artifact lifecycle owner, actual hosted runtime, App/release readiness, external submission authorization, provider-hosted completion or production-ready claim.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing remaining 2026-04-10 local-runtime validation / stage-route / revised / walkthrough records or 2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale local-runtime/provider/hosted wording risk is higher there.
- Or switch to RCA uncovered reference bodies, OPL uncovered docs, or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-10 local-runtime / stage-route history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-10 revised workspace validator、validation-failed local-runtime route/checkpoint shape、stage-route checkpoint output consistency 与 local-runtime walkthrough 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 `runtime-run` / `runtime-resume`、local journal、local runtime ladder、bare command walkthrough、stage-route mirror、same-repo HITL、MCP/controller public formal entry 或 post-R5A hardening wording 误读成当前 public CLI command shape、MAG-owned generic runtime、attempt ledger、actual hosted runtime、App/release readiness、production readiness、compatibility interface 或 active implementation queue。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md`, `docs/history/specs/2026-04-10-post-r5a-local-runtime-validation-failed-route-checkpoint-shape-alignment-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-stage-route-report-checkpoint-status-output-consistency-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/route_report.py`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/cli.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, `tests/test_domain_entry.py`, `tests/test_revision_executor.py`, `tests/test_cli_validate_workspace_revision_cases.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh verification probes: `med_autogrant workspace --help`, `med_autogrant pass --help`, `med_autogrant package --help`, `workspace route-report` on `examples/nsfc_workspace_p2c_critique.json`, `pass revision` on `examples/nsfc_workspace_p3b_re_review_major_revision.json` followed by `workspace validate` and `workspace route-report`, `public_cli_command()` mapping, focused route/revision/domain-entry pytest, and retired public command scan.

Fresh semantic result：

- All four reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- `2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md` needed one small post-2026-05 reading guard because its body still used imperative `runtime-run` / `runtime-resume` language in the historical local runtime ladder. The added note keeps the historical text as provenance and routes current executable operator path to grouped CLI plus no-resurrection scan.
- The validation-failed route/checkpoint, stage-route checkpoint output consistency and local-runtime walkthrough files are correctly scoped as historical local-runtime closeout / fail-closed / output-consistency provenance. Existing lifecycle headers and `specs_lifecycle_map.md` are sufficient for these files; no body rewrite was needed.
- Current route checkpoint behavior is source-owned by `route_report.build_stage_route_report()`: it returns top-level `checkpoint_status` and `verification_checkpoint.checkpoint_status` from the same checkpoint object. Fresh `workspace route-report` on the critique example returned matching `forward_progress` values and a populated route object.
- Generated revised workspace still re-enters current validator/route surfaces. Fresh `pass revision` on the P3.B re-review example followed by `workspace validate` and `workspace route-report` returned `validate.ok=True` and matching `forward_progress` checkpoint values.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_owner=configured_family_runtime_provider`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, `mag_owns_attempt_ledger=false`, `default_stage_executor=codex_cli`, `optional_hosted_carriers=["hermes_agent"]`, and `historical_baseline=NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`.
- Current public CLI shape is grouped: workspace behavior is under `workspace validate|summarize|next-step|critique-summary|route-report`; revision is under `pass revision`; package behavior is under `package artifact-bundle|final-package|hosted-contract-bundle|submission-ready`. Historical bare command examples remain provenance and must not be copied into current operator docs without mapping through `public_cli`.
- `run-local`、`runtime-run`、`runtime-resume` and `probe-upstream-hermes` remain retired/no-resurrection terms. The retired public command scan returned `state=passed` and each retired command was absent from active domain-entry and grouped public CLI catalogs.
- Current verification gap discovered during the audit: `tests/test_cli_validate_workspace_revision_cases.py` still contains two tests for `workspace cockpit` and `product direct-entry`, while current CLI help and parser do not expose those grouped commands. The same focused file passes when those two existing drifted cases are excluded; `tests/test_revision_executor.py` and `tests/test_domain_entry.py` pass. This is a pre-existing product/CLI test drift outside this docs coverage tranche, not a failure of the four history specs' lifecycle classification.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-10 local-runtime / stage-route / revised / walkthrough history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner fields, grouped public CLI mapping, route-report source, domain runtime topology, retired command no-resurrection scan and focused route/revision/domain-entry tests. | this coverage ledger; `docs/history/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md` |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone 或删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch、2026-04-07 P2/P3A batch、2026-04-08 P3/P4 batch、2026-04-08 P5/R1 batch、2026-04-08 R2/R3/runtime-first batch、2026-04-09 R3/R4/R5/post-R5A batch、2026-04-10 hosted-contract bundle fail-closed batch and this 2026-04-10 local-runtime/stage-route/revised/walkthrough batch are not paragraph-governed in this tranche.
- Higher-risk remaining MAG batches include 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted/OPL handoff records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later OPL global ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-10 specs as current public CLI command shape, runtime owner, default runtime, active local runtime ladder, local journal, `runtime-run` / `runtime-resume`, Gateway/federation readiness, daemon/scheduler/attempt ledger, controller public formal entry, submission/export-ready verdict, App release readiness, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical bare `validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report`、`execute-revision-pass`、`build-artifact-bundle`、`build-final-package` and `build-hosted-contract-bundle` examples must be mapped through current grouped public CLI as `workspace validate`、`workspace summarize`、`workspace next-step`、`workspace critique-summary`、`workspace route-report`、`pass revision`、`package artifact-bundle`、`package final-package` and `package hosted-contract-bundle`.
- `stage-route-report` checkpoint mirror and revised workspace validation vocabulary must remain workspace route/checkpoint semantics. They must not be upgraded to actual hosted runtime, generic OPL artifact lifecycle owner, App/release readiness, external submission authorization, provider-hosted completion or production-ready claim.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing 2026-04-11 Hermes/reset/local-runtime records or 2026-04-12 hosted/OPL handoff specs because stale provider/hosted wording risk is higher there.
- Separately route the pre-existing `workspace cockpit` / `product direct-entry` CLI test drift to a source/test owner lane before treating `tests/test_cli_validate_workspace_revision_cases.py` as a fully green focused suite.
- Or switch to RCA uncovered reference bodies, OPL uncovered docs, or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-11 Hermes/reset/local-runtime history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-11 Hermes-backed runtime capability migration map、Hermes-backed runtime substrate program、post-R5A local-runtime upper-bound honest-stop 与 upstream Hermes-Agent truth reset 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 Hermes-first provider proposal、Hermes substrate owner path、repo-local runtime helper、`runtime-run` / `runtime-resume`、local journal、host-agent compatibility bridge、future Hermes host 或 “接入上游 Hermes-Agent” 词汇误读成当前 default runtime owner、active provider owner、MAG-owned daemon/scheduler/attempt-loop、attempt ledger、public runtime command、compatibility bridge、hosted runtime readiness、App/release readiness、production readiness、physical-delete authority 或 active implementation queue。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md`, `docs/history/specs/2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md`, `docs/history/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`, `docs/history/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, `src/med_autogrant/critique_executor.py`, `src/med_autogrant/hermes_native_executor.py`, `tests/test_domain_entry.py`, `tests/test_critique_executor.py`, `tests/test_hermes_native_executor.py`, `tests/test_program_control_surfaces.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh read-model probes: `MagDomainRuntime().describe_topology()`, grouped public CLI help for root/workspace/pass/package, `PUBLIC_GROUP_COMMANDS`, `INTERNAL_TO_PUBLIC_COMMAND`, `SERVICE_SAFE_DOMAIN_COMMANDS`, and `retired_public_command_scan`.

Fresh semantic result：

- All four reviewed files carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- `2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md` is correctly scoped as `historical_hermes_capability_split_provenance`; its Hermes capability split and command mapping are proof/provenance, not current runtime owner、default provider、public command catalog、hosted runtime readiness or compatibility target.
- `2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md` needed a small post-2026-05 reading guard because the body still used direct owner-path wording such as `Hermes-backed runtime substrate`、`runtime-run` / `runtime-resume`、local host-agent compatibility bridge and “切到 Hermes substrate owner path”。The added guard keeps those terms in 2026-04-11 proposal/proof context and routes current task runtime、attempt ledger、queue/wakeup/resume and production provider to OPL/Temporal.
- `2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md` needed a small post-2026-05 reading guard because the “Current Repo-Verified Local Runtime Surface” section listed old local runtime commands. The added guard makes that section an honest-stop historical snapshot, not the current executable command catalog.
- `2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md` needed a small post-2026-05 reading guard because “当前真实状态”、“仍然成立的本地能力”、“长线目标” and “下一步允许做什么” were easy to misread as current Hermes integration direction. The added guard keeps them in 2026-04-11 truth-reset context and states that upstream Hermes-Agent is now only an explicit executor/proof/provenance lane.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_owner=configured_family_runtime_provider`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, `mag_owns_attempt_ledger=false`, `default_stage_executor=codex_cli`, and `optional_hosted_carriers=["hermes_agent"]`.
- `MagDomainRuntime().describe_topology()` still reports `runtime_owner=one-person-lab`, `can_claim_generic_runtime_owner=False`, `default_formal_entry=CLI`, `supported_protocol_layer=MCP`, `internal_controller_surface=controller`, `optional_proof_executor=Hermes-Agent`, and `optional_proof_executor_boundary=explicit opt-in only`.
- Current public CLI shape is grouped. Root help exposes only `workspace`、`mainline`、`domain-handler`、`authority`、`pass` and `package`; workspace help lists `validate`、`summarize`、`next-step`、`critique-summary` and `route-report`; pass help lists `revision` and the authoring passes; package help lists `artifact-bundle`、`final-package`、`hosted-contract-bundle` and `submission-ready`.
- `run-local`、`runtime-run`、`runtime-resume` and `probe-upstream-hermes` remain retired/no-resurrection terms. Fresh scan returned `state=passed`, no active domain-entry command matches, no active grouped public CLI command matches, and each retired command was absent from both `SERVICE_SAFE_DOMAIN_COMMANDS` and `INTERNAL_TO_PUBLIC_COMMAND`.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-11 Hermes/reset/local-runtime history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner fields, grouped public CLI mapping, domain runtime topology, explicit Hermes proof lane source/tests, and retired command no-resurrection surfaces. | this coverage ledger; `docs/history/specs/2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md`; `docs/history/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`; `docs/history/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md` |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone 或删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the 2026-04-06 foundation batch、2026-04-07 P2/P3A batch、2026-04-08 P3/P4 batch、2026-04-08 P5/R1 batch、2026-04-08 R2/R3/runtime-first batch、2026-04-09 R3/R4/R5/post-R5A batch、2026-04-10 hosted-contract bundle fail-closed batch、2026-04-10 local-runtime/stage-route/revised/walkthrough batch and this 2026-04-11 Hermes/reset/local-runtime batch are not paragraph-governed in this tranche.
- Higher-risk remaining MAG batches include 2026-04-12 hosted/OPL handoff and upstream Hermes fast-cutover records.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later MAG or OPL ledger entry.
- Other OPL-series repos remain under the global coverage ledger; App docs stay delayed while active release / GUI lanes are dirty.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-11 specs as current runtime owner、default provider、Hermes-backed default route、public `runtime-run` / `runtime-resume`、local run journal、attempt ledger、host-agent bridge、compatibility target、hosted runtime readiness、App/release readiness、production readiness、physical-delete authority or active implementation queue is stale pollution.
- Historical bare command examples must be mapped through current grouped public CLI where a mapped public command exists; `runtime-run`、`runtime-resume`、`run-local` and `probe-upstream-hermes` have no current grouped public command and must remain retired.
- `hermes_agent` vocabulary must remain explicit opt-in executor / receipt / proof lane vocabulary. It must not be upgraded to default task runtime owner、provider owner、grant truth owner、quality/export verdict owner or long-soak completion claim.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing 2026-04-12 hosted/OPL handoff and upstream Hermes fast-cutover records because stale hosted/provider wording risk remains high.
- Separately route the pre-existing `workspace cockpit` / `product direct-entry` CLI test drift to a source/test owner lane.
- Or choose RCA uncovered reference bodies, OPL uncovered docs, or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-12 hosted / OPL handoff / fast-cutover history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-12 hosted caller consumption、hosted contract bundle / route catalog、lightweight product-entry / OPL handoff、OPL-aligned phase map 与 upstream Hermes fast-cutover 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 hosted caller proof、hosted bundle export、`direct` / `opl-handoff` envelope、P1-P4 phase map、Hermes fast-cutover、`runtime-run` / `runtime-resume`、SessionDB attempt durability、`probe-upstream-hermes` 或 future `OPL Gateway` 语义误读成当前 default runtime owner、actual hosted runtime、active public/domain command catalog、App/workbench readiness、production/default caller completion、grant/submission readiness、physical-delete authority 或 compatibility interface。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`, `docs/history/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md`, `docs/history/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`, `docs/history/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md`, `docs/history/specs/2026-04-12-upstream-hermes-agent-fast-cutover-board.md`, `docs/history/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/domain_entry_contract.py`, `src/med_autogrant/domain_runtime_parts/contracts.py`, `src/med_autogrant/hosted_contract_bundle.py`, `src/med_autogrant/public_cli.py`, `tests/test_domain_entry.py`, `tests/test_hosted_contract_bundle.py`, `tests/test_program_control_surfaces.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh read-model probe: clean Python import of `SERVICE_SAFE_DOMAIN_COMMANDS`, `build_domain_entry_contract()` and `build_hosted_authoring_contract()`.

Fresh semantic result：

- All six reviewed files already carried first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- All six files needed small post-2026-05 reading guards because their bodies still contain high-risk direct-file wording: hosted caller proof completed, hosted contract bundle route catalog, `direct` / `opl-handoff`, P1/P3 completed, Hermes substrate cutover, `runtime-run` / `runtime-resume`, `probe-upstream-hermes`, SessionDB attempt durability and future `OPL Gateway`.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_substrate=temporal`, `default_stage_executor=codex_cli`, `optional_hosted_carriers=["hermes_agent"]`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, and `mag_owns_attempt_ledger=false`.
- Fresh command-catalog probe found `SERVICE_SAFE_DOMAIN_COMMANDS` and `domain_entry_contract.supported_commands` both contain 30 current commands. `run-local`、`runtime-run`、`runtime-resume` and `probe-upstream-hermes` are absent from both active domain-entry and grouped public CLI catalogs.
- Fresh hosted authoring contract probe returned the current route id set `direction_screening`, `question_refinement`, `argument_building`, `fit_alignment`, `outline`, `drafting`, `critique`, `revision`, `frozen`, `artifact_bundle`, `final_package`, `hosted_contract_bundle`; historical early landed / pending route splits in these files remain 2026-04-12 snapshots and must not override current source/contracts/tests.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the six 2026-04-12 hosted / OPL handoff / fast-cutover history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner fields, domain-entry contract source, hosted authoring contract source, hosted bundle source and retired command no-resurrection surfaces. | this coverage ledger; `docs/history/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`; `docs/history/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md`; `docs/history/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`; `docs/history/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md`; `docs/history/specs/2026-04-12-upstream-hermes-agent-fast-cutover-board.md`; `docs/history/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md` |

Archived / tombstoned / deleted docs：无。这六份文件仍是有用的 history provenance；不需要移动、tombstone 或删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside recorded batches remain open for paragraph-level governance, including `2026-04-12-author-side-executor-routing-contract-current-truth.md`, `2026-04-12-critique-pending-handoff-contract-current-truth.md`, `2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md`, `2026-04-13-hermes-native-critique-proof-tombstone.md`, and the large 2026-04-10 final-package artifact-bundle fail-closed family not yet covered by a focused tranche.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later MAG or OPL ledger entry.
- OPL, MAS, RCA and App repo-wide coverage remains open outside recorded chunks. OMA is covered by its earlier full README/docs tranche.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-12 specs as current runtime owner, default provider, Hermes default route, public `runtime-run` / `runtime-resume`, `probe-upstream-hermes`, local run journal, attempt ledger, hosted runtime readiness, App/release readiness, production readiness, physical-delete authority or active implementation queue is stale pollution.
- Historical `P1` / `P2` / `P3` completed and P4.A/B/C landed wording must remain proof / contract-consumption / product-entry snapshot vocabulary. It must not be upgraded to domain-ready、production-ready、grant-ready、submission-ready、App/workbench ready or physical-delete-ready.
- Historical early route splits and supported-command lists must not override current service-safe command catalog, grouped public CLI or current route catalog. Retired runtime commands have no current grouped public command and must remain retired.
- `direct` / `opl-handoff` vocabulary in these files remains historical product-entry handoff shape. It is not a compatibility interface, production hosted caller, App release gate or external default-caller completion claim.

Verification before absorb：

- `git diff --check` passed.
- Strict README/docs/contracts conflict-marker scan passed.
- OPL Doc Governance doctor passed with `finding_count=0` and active truth `pass`.
- Focused tests passed: `tests/test_domain_entry.py`, `tests/test_hosted_contract_bundle.py`, and `tests/test_program_control_surfaces.py` returned 39 pytest cases plus 34 subtests passed.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing the remaining 2026-04-12 route/handoff snapshots, 2026-04-13 Hermes-native tombstone, or the large 2026-04-10 final-package artifact-bundle fail-closed family.
- Separately route the pre-existing `workspace cockpit` / `product direct-entry` CLI test drift to a source/test owner lane.
- Or choose RCA uncovered reference bodies, OPL uncovered docs, or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-10 final-package artifact-bundle fail-closed history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-10 post-R5A final-package artifact-bundle fail-closed 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 `build-final-package` malformed artifact bundle hardening、artifact object/list value-type validation、package export proof 或 local runtime wording 误读成当前 active implementation queue、public CLI shape、generic OPL artifact owner、submission-ready/export-ready verdict、App release ready、production ready、actual hosted runtime 或 compatibility interface。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-list-element-linked-object-ids-field-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-list-element-linked-object-ids-list-element-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-list-element-required-string-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-list-element-shapes-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-list-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-linkage-id-fields-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-primary-id-fields-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-required-list-element-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-required-list-fields-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-required-string-fields-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-required-nested-fields-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-required-scalar-value-types-fail-closed-activation-package.md`, `docs/history/specs/2026-04-10-post-r5a-final-package-artifact-bundle-summary-count-value-types-fail-closed-activation-package.md`, and `docs/history/specs/2026-04-10-post-r5a-final-package-malformed-artifact-bundle-fail-closed-activation-package.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `contracts/generated_surface_handoff.json`, `contracts/production_acceptance/mag-production-acceptance.json`, `contracts/external_evidence/mag-evidence-receipt-ledger.json`, `src/med_autogrant/final_package.py`, `src/med_autogrant/final_package_validation.py`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/domain_entry_contract.py`, `src/med_autogrant/hosted_contract_bundle.py`, `tests/test_final_package.py`, `tests/test_hosted_contract_bundle.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh read-model probes: grouped public CLI / domain-entry command catalog, `build_domain_entry_contract()`, `_build_hosted_authoring_contract()`, and current package command mapping.

Fresh semantic result：

- All 15 reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- These files are correctly scoped as historical post-R5A final-package artifact-bundle fail-closed provenance. They record how malformed artifact bundle inputs were hardened, not current active implementation work.
- Current behavior is source/test owned by `final_package.build_final_package_payload()`, `final_package_validation` / artifact bundle validation helpers, and focused tests in `tests/test_final_package.py`. The tests cover missing manifest/artifacts, required nested/scalar fields, summary count value types, artifact list/object shapes, primary/linkage ids, required string/list fields, list element values and malformed artifact bundle fail-closed behavior.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_owner=configured_family_runtime_provider`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, `mag_owns_attempt_ledger=false`, `default_stage_executor=codex_cli`, and `optional_hosted_carriers=["hermes_agent"]`.
- `contracts/production_acceptance/mag-production-acceptance.json` keeps `provider_completion_equals_submission_ready=false`, `structural_conformance_equals_domain_ready=false`, `claims_package_existence_is_submission_ready=false`, and MAG-owned package / submission-ready authority. Current external evidence is refs-only and does not include grant artifact body, package archive body or submission-ready verdict body.
- Current public CLI shape is grouped. Internal historical labels such as `build-artifact-bundle`, `build-final-package`, `build-hosted-contract-bundle`, and `build-submission-ready-package` map to the package group as current operator commands: `package artifact-bundle`, `package final-package`, `package hosted-contract-bundle`, and `package submission-ready`.
- Fresh command-catalog probe found `domain_entry_contract.supported_commands` contains 30 current commands, and retired runtime commands `run-local`, `runtime-run`, `runtime-resume`, and `probe-upstream-hermes` are absent from active command surfaces.
- No body rewrite was needed. The existing lifecycle guard, `docs/specs/specs_lifecycle_map.md`, and `docs/history/specs/README.md` are sufficient for this batch; this tranche records paragraph coverage and current machine-evidence alignment.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the 15 final-package artifact-bundle fail-closed history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner fields, production acceptance authority boundaries, generated surface handoff, external evidence ledger, final package source/tests, hosted bundle source/tests, grouped public CLI mapping and command catalog. | this coverage ledger only |

Archived / tombstoned / deleted docs：无。这 15 份文件仍是有用的 history provenance；不需要移动、tombstone 或正文删除。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside recorded batches remain open for paragraph-level governance, including `2026-04-12-author-side-executor-routing-contract-current-truth.md`, `2026-04-12-critique-pending-handoff-contract-current-truth.md`, `2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md`, `2026-04-13-hermes-native-critique-proof-tombstone.md`, and older final-package / presubmission / R2 artifact-bundle provenance not yet covered by focused later ledgers.
- MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later MAG or OPL ledger entry.
- OPL, MAS, RCA and App repo-wide coverage remains open outside recorded chunks. OMA is covered by its earlier full README/docs tranche.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-10 specs as current implementation queue, public CLI command shape, runtime owner, default runtime, active local runtime ladder, actual hosted runtime, App/release readiness, external portal submission authorization, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical bare `build-artifact-bundle`, `build-final-package`, `build-hosted-contract-bundle`, and `build-submission-ready-package` wording must be mapped through current grouped public CLI as `package artifact-bundle`, `package final-package`, `package hosted-contract-bundle`, and `package submission-ready`.
- `final_package` and `artifact_bundle` fail-closed vocabulary must remain within MAG package/export authority, source/test validation evidence and history/provenance boundaries. It must not be upgraded to generic OPL artifact lifecycle ownership, provider-hosted completion, domain ready, grant ready, fundability ready or submission-ready export verdict.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches, prioritizing remaining 2026-04-12 route/handoff snapshots, `2026-04-13-hermes-native-critique-proof-tombstone.md`, or MAG non-index references such as grant strategy memory policy and OPL family contract adoption.
- Keep the pre-existing `workspace cockpit` / `product direct-entry` CLI test drift routed to a source/test owner lane, not docs-governance closeout.
- Or choose RCA uncovered reference bodies, OPL uncovered docs, or App docs once their main checkout and active worktrees are safe.

### 2026-05-26 2026-04-12 route / handoff snapshots and 2026-04-13 Hermes tombstone coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下剩余 2026-04-12 route / handoff snapshots 和 2026-04-13 Hermes-native critique proof tombstone。目标是确认这些 direct-file 历史入口不会把旧 author-side route snapshot、pending handoff matrix、`runtime-run`、裸 package command、`hermes_native_proof`、Hermes / Gateway wording 或 experimental proof lane 误读成当前 route catalog、public CLI shape、default executor owner、default runtime owner、compatibility interface、App/release readiness、production readiness 或 physical-delete authority。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md`。
- Reviewed history specs: `docs/history/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md`, `docs/history/specs/2026-04-12-critique-pending-handoff-contract-current-truth.md`, `docs/history/specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md`, and `docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/domain_entry.py`, `src/med_autogrant/domain_entry_contract.py`, `src/med_autogrant/hosted_contract_bundle.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/critique_executor.py`, `src/med_autogrant/hermes_native_executor.py`, `tests/test_domain_entry.py`, `tests/test_critique_executor.py`, `tests/test_program_control_surfaces.py`, active specs listed by `docs/specs/README.md`, schemas/source/CLI/API behavior。
- Fresh read-model probes: `contracts/runtime-program/current-program.json` runtime owner / executor defaults, `MagDomainRuntime().describe_topology()`, `build_domain_entry_contract()`, `_build_hosted_authoring_contract()`, grouped public CLI mapping, active service-safe command catalog, current critique executor vocabulary and retired command absence.

Fresh semantic result：

- All four reviewed files carry first-screen lifecycle signals plus `Owner` / `Purpose` / `State` / `Machine boundary`.
- `2026-04-12-author-side-executor-routing-contract-current-truth.md` remains useful historical author-side executor routing snapshot. It needed one post-2026-05 reading guard because the body still mentions `runtime-run` and bare `build-*` commands. Current operator commands map through grouped CLI, and current route catalog / hosted contract truth is source / contract owned.
- `2026-04-12-critique-pending-handoff-contract-current-truth.md` is already a concise superseded critique pending snapshot. Existing lifecycle guard is sufficient; no body rewrite was needed.
- `2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md` remains useful historical pending handoff matrix. It needed one post-2026-05 reading guard because the body still describes pending authoring routes, Hermes / Gateway collaboration and old surface names. Current `direction_screening -> frozen` routes are landed service-safe commands, and historical workspace surface names map through grouped CLI.
- `2026-04-13-hermes-native-critique-proof-tombstone.md` remains a historical proof tombstone. It needed one post-2026-05 reading guard because the body still uses the superseded `hermes_native_proof` vocabulary. Current explicit non-default executor vocabulary is `executor_kind=hermes_agent`, default critique executor is still `codex_cli`, and non-default executor use requires OPL `AgentExecutionReceipt` style proof with no silent fallback or equivalence claim.
- `contracts/runtime-program/current-program.json` still states `default_task_runtime_owner=one-person-lab`, `default_runtime_owner=configured_family_runtime_provider`, `default_runtime_substrate=temporal`, `default_stage_executor=codex_cli`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, `mag_owns_attempt_ledger=false`, and optional hosted carrier `hermes_agent`.
- Current public CLI shape is grouped. Historical `summarize-workspace`, `stage-route-report`, `critique-summary`, `build-artifact-bundle`, `build-final-package`, `build-hosted-contract-bundle` and `build-submission-ready-package` map to `workspace summarize`, `workspace route-report`, `workspace critique-summary`, `package artifact-bundle`, `package final-package`, `package hosted-contract-bundle` and `package submission-ready`.
- Fresh command-catalog probe found `SERVICE_SAFE_DOMAIN_COMMANDS` has 30 active commands; `run-local`, `runtime-run`, `runtime-resume` and `probe-upstream-hermes` remain absent from active service-safe and grouped public command catalogs.
- Fresh hosted authoring contract probe returned current route ids `direction_screening`, `question_refinement`, `argument_building`, `fit_alignment`, `outline`, `drafting`, `critique`, `revision`, `frozen`, `artifact_bundle`, `final_package`, and `hosted_contract_bundle`; historical pending / landed split text must not override current source/contracts/tests.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, current-program runtime owner / executor defaults, domain-entry contract source, hosted authoring contract source, critique executor source/tests, explicit Hermes adapter proof source/tests and retired command no-resurrection surfaces. | this coverage ledger; `docs/history/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md`; `docs/history/specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md`; `docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md` |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone 或删除。

Uncovered docs：

- `med-autogrant`: focused MAG history specs batches recorded so far now cover the 2026-04-12 hosted / OPL handoff / fast-cutover group, the remaining 2026-04-12 route / handoff snapshots, the 2026-04-13 Hermes-native critique proof tombstone, and the 2026-04-10 final-package artifact-bundle fail-closed family. Remaining MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist still need paragraph-level checks against current contracts/source unless already covered by a later MAG or OPL ledger entry.
- OPL, MAS, RCA and App repo-wide coverage remains open outside recorded chunks. OMA is covered by its earlier full README/docs tranche.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-12 / 2026-04-13 files as current route catalog, public CLI command shape, default executor owner, default runtime owner, active `runtime-run` / `runtime-resume`, Gateway/federation readiness, production hosted caller, App release gate, compatibility interface, domain ready, production ready or physical-delete authority is stale pollution.
- `hermes_agent` vocabulary must remain explicit opt-in executor / receipt / proof lane vocabulary. It must not be upgraded to default task runtime owner, provider owner, grant truth owner, quality/export verdict owner, Codex-equivalent executor, long-soak completion or production-ready claim.
- Historical pending matrix and early route split wording must remain 2026-04-12 migration provenance. Current route truth comes from active specs, contracts/source, hosted authoring contract and tests.

Next tranche write scope：

- Continue MAG non-index references such as grant strategy memory policy, OPL family contract adoption and governance checklist; or switch to RCA uncovered reference bodies, OPL uncovered docs, or App docs once their main checkout and active worktrees are safe.
- Keep the pre-existing `workspace cockpit` / `product direct-entry` CLI test drift routed to a source/test owner lane, not docs-governance closeout.

### 2026-05-26 MAG non-index references coverage tranche

本轮覆盖 MAG `docs/references/**` 下剩余非索引支撑文档：grant strategy memory policy、OPL family contract adoption 和 series doc governance checklist，并复核 references index。目标是确认这些 support references 不把 memory body、fundability/quality/export verdict、submission-ready authority、OPL runtime ownership、App/workbench scope、OMA role 或旧四仓治理范围误读成当前 MAG owner truth。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md`、本文件和 `docs/references/README.md`。
- Reviewed references：`docs/references/grant_strategy_memory_policy.md`、`docs/references/integration/opl-family-contract-adoption.md`、`docs/references/governance/series-doc-governance-checklist.md`、`docs/references/README.md`。
- Machine/source truth surfaces：`contracts/runtime-program/current-program.json`、`contracts/runtime-program/opl-family-contract-adoption.json`、`contracts/memory_descriptor.json`、`contracts/pack_compiler_input.json`、`contracts/stage_control_plane.json`、`src/med_autogrant/product_entry_parts/*memory*`、`src/med_autogrant/product_entry_parts/opl_substrate_adapter.py`、`src/med_autogrant/product_entry_parts/manifest_builder.py`、`tests/test_opl_family_contract_adoption.py` 与 product-entry memory / receipt focused tests。
- Cross-repo support truth：`/Users/gaofeng/workspace/one-person-lab/docs/references/operating-governance/family-domain-memory-governance.md` 存在，继续作为 family-level memory governance reference。

Fresh semantic result：

- `grant_strategy_memory_policy.md` 已按 single-role reference 读取：它只说明 prose-first grant strategy memory、stage-specific retrieval、MAG accept/reject 和 OPL refs / receipt projection 边界。`contracts/memory_descriptor.json` 确认 `memory_body_owner=med-autogrant`、OPL policy 是 `locator_and_receipt_refs_only`，且 OPL 不能写 memory body 或 accept/reject writeback。无需正文改写。
- `integration/opl-family-contract-adoption.md` 已按 OPL adoption support reference 读取：`contracts/runtime-program/opl-family-contract-adoption.json` 确认 OPL 只是 family-level projection consumer，attempt / quality / incident / product operator projection 都不转移 MAG grant truth、fundability judgment、quality/export verdict 或 submission-ready export gate。无需正文改写。
- `contracts/pack_compiler_input.json` 确认 canonical semantic pack root 是 `agent/`，并列出完整 prompts、stages、skills、quality gates 和 knowledge refs；`contracts/stage_control_plane.json` 确认六个 family stage 与 allowed action refs。当前 Declarative Grant Pack / Stage Control Plane 文档读法仍是 descriptor/projection，不是新的 MAG private runtime。
- `series-doc-governance-checklist.md` 原先仍写“四仓”治理范围；本轮改为当前六仓 scope，并补充 `one-person-lab-app` 是 App/workbench 与 operator projection consumer、`opl-meta-agent` 是 Agent Foundry / new-agent builder-test managed module，不是 domain truth / artifact / owner receipt authority。
- `docs/references/README.md` 已补入治理清单入口，保持 references index 与实际 support reference 集合一致。

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four references listed above; support read of MAG core docs, ideal-state reference, active gap plan, runtime-program owner fields, OPL family adoption contract, memory descriptor, pack compiler input, stage control plane and relevant memory/adoption tests. | this coverage ledger; `docs/references/README.md`; `docs/references/governance/series-doc-governance-checklist.md` |

Archived / tombstoned / deleted docs：无。这些 references 仍是有用的 support material；本轮问题是 stale family scope wording 与 index omission，不是路径退役。

Uncovered docs：

- `med-autogrant`: root README、核心五件套、active plan、ideal-state reference、specs、thin indexes、大部分 history specs 和本轮 non-index references 均已由已记录 tranche 覆盖；剩余未覆盖范围继续以 OPL 全局 coverage ledger 为准，主要是 `docs/history/**` 中未被 focused later ledger 点名的过程/历史正文、新增文档，以及后续变更打开的 support bodies。
- OPL、MAS、RCA 和 App repo-wide coverage remains open outside recorded chunks. OMA is covered by its earlier full README/docs tranche.

Remaining stale / retire candidates：

- Any future reference wording that turns MAG memory into OPL-owned grant strategy content, fundability / quality / export verdict, submission-ready authority, repo-source memory body store or automatic recipe engine is stale pollution.
- Any future adoption wording that turns OPL projection consumption, descriptor index, `agent/` pack, stage control plane or substrate adapter export into MAG private runtime, OPL grant truth owner, quality/export authority, App/workbench readiness, production ready or long-soak completion is stale pollution.
- Any future MAG governance checklist wording that reverts to four-repo scope, omits One Person Lab App, or promotes OPL Meta Agent into domain truth / artifact / owner receipt authority is stale pollution.

Verification before absorb：

- `git diff --check` passed.
- Strict README/docs/contracts conflict-marker scan passed.
- OPL Doc Governance doctor passed with `finding_count=0` and active truth `pass`.
- MAG focused memory/adoption/stage-control tests passed: `tests/test_opl_family_contract_adoption.py`, `tests/product_entry_cases/test_domain_memory_descriptor.py`, `tests/product_entry_cases/test_memory_receipt_projection.py`, `tests/product_entry_cases/test_domain_memory_receipt_evidence.py`, `tests/product_entry_cases/test_family_stage_control_plane.py`, and `tests/product_entry_cases/test_opl_substrate_adapter.py` returned 26 pytest cases plus 45 subtests.
- A broader product family orchestration focused run still exposes a pre-existing product user-loop runtime-state root expectation drift; keep that source/test issue outside this docs-governance tranche.

Next tranche write scope：

- Continue another safe repo/doc cluster: OPL uncovered support docs, MAS remaining repo-wide docs, RCA remaining bodies after external implementation dirt is isolated, or App docs once active App dirty lanes are closed or explicitly assigned.
- Keep the pre-existing `workspace cockpit` / `product direct-entry` / `product user-loop` CLI and runtime-state expectation drift routed to a source/test owner lane, not docs-governance closeout.

### 2026-05-26 MAG non-spec history coverage tranche

本轮覆盖 MAG `docs/history/**` 下非 specs 历史入口：历史 plans、product handoff、runtime owner split、positioning 和 OMX index。目标是确认这些 direct-file 历史入口不会把旧 scaffold/P1 计划、hosted caller proof、Hermes/Gateway/local-runtime/Domain Harness OS 词汇、轻量 product-entry shell 或 `.omx` / `.runtime-program` 语境误读成当前 active backlog、default runtime owner、MAG-owned generic runtime、Gateway-ready、hosted runtime readiness、product maturity、submission-ready / production-ready claim 或 compatibility interface。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md`、`contracts/runtime-program/current-program.json`、`contracts/production_acceptance/mag-production-acceptance.json`。
- Reviewed history docs：`docs/history/README.md`、`docs/history/plans/README.md`、`docs/history/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md`、`docs/history/plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md`、`docs/history/plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md`、`docs/history/plans/2026-04-13-grant-writing-full-coverage-landing-plan.md`、`docs/history/plans/mag-standard-agent-doc-process-history-2026-05.md`、`docs/history/product/lightweight-product-entry-and-opl-handoff.md`、`docs/history/runtime/opl-managed-runtime-three-layer-contract.md`、`docs/history/positioning/domain-harness-os-positioning.md`、`docs/history/omx/README.md`。
- Source/read-model support：`src/med_autogrant/domain_runtime_parts/substrate.py::MagDomainRuntime.describe_topology` reports `runtime_owner="one-person-lab"`, `can_claim_generic_runtime_owner=False`, default stage attempt executor `Codex CLI`, and optional proof executor `Hermes-Agent` with `explicit opt-in only`; `public_cli.PUBLIC_GROUP_COMMANDS` exposes grouped workspace/mainline/domain-handler/authority/pass/package commands.

Fresh semantic result：

- History root, plans index, runtime history, positioning history and OMX index already carry owner / purpose / state / machine-boundary signals or directory inheritance sufficient for direct-file reading.
- The old scaffold, P1 durability, hosted caller and full authoring landing plans are correctly scoped as completed historical plans. Their unchecked task lists, old `docs/plans` paths, `MCP/controller`, `.runtime-program` and hosted proof wording must remain provenance and cannot reopen active backlog.
- `docs/history/product/lightweight-product-entry-and-opl-handoff.md` needed one body rewrite: the old “真实 upstream `Hermes-Agent` substrate 已经 landed” wording is now explicitly a hosted / upstream proof lane and migration-background claim. Current default runtime owner remains OPL/Temporal, and `Hermes-Agent` remains an explicit non-default proof / executor adapter lane.
- `docs/history/runtime/opl-managed-runtime-three-layer-contract.md` already states current OPL stage-led runtime framework and `Codex CLI` executor boundary; no rewrite needed.
- `docs/history/positioning/domain-harness-os-positioning.md` is correctly scoped as Domain Harness OS / UHS historical positioning. Its hosted/runtime maturity wording remains bounded by the first-screen historical note.
- No archive, tombstone or deletion action was needed. These files remain useful provenance once read through the history lifecycle guard.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the history docs listed above; support read of MAG current status, active gap plan, ideal-state reference, runtime-program owner fields, production acceptance authority boundaries, domain runtime topology source and grouped public CLI shape. | this coverage ledger; `docs/history/product/lightweight-product-entry-and-opl-handoff.md` |

Archived / tombstoned / deleted docs：无。这批非 specs history 文件仍是有用 provenance；本轮只修正一处可能被读成当前 Hermes default/runtime-substrate 事实的历史 product wording。

Uncovered docs：

- `med-autogrant`: root README、核心五件套、active plan、ideal-state reference、specs、thin indexes、non-index references、history specs focused batches和本轮 non-spec history 入口均已有记录覆盖。MAG 剩余未覆盖范围继续以 OPL 全局 coverage ledger 为准，主要是后续新增 docs、未被最终 reconcile 点名的历史正文或 later code/contract changes 重新打开的 support bodies。
- Other OPL-series repos remain under the global coverage ledger; OMA full README/docs coverage remains covered by its earlier tranche.

Remaining stale / retire candidates：

- Any future MAG history wording that turns hosted / upstream Hermes proof lane into current default runtime owner, provider owner, production-ready claim or Codex-equivalent executor is stale pollution.
- Any future history plan wording that revives `.omx`, `.runtime-program`, old `docs/plans`, Gateway/local-manager, flat CLI alias, local journal, attempt ledger, product-sidecar or compatibility aggregate tests as active surfaces is stale pollution.
- Any future product handoff wording that turns lightweight product-entry / OPL handoff provenance into mature App/workbench readiness, final UX, grant-ready, submission-ready, export-ready or production-ready evidence is stale pollution.

Next tranche write scope：

- Prefer OPL uncovered support docs or MAS remaining repo-wide docs while RCA/App main checkouts still carry external dirty implementation/release lanes.
- If returning to MAG, run a final inventory/reconcile pass against all `README*` and `docs/**/*.md` to confirm no new docs appeared after the recorded MAG coverage tranches.

### 2026-05-26 MAG final inventory reconcile tranche

本轮对 MAG 当前 `README*` 与 `docs/**/*.md` 做最终 inventory reconcile。目标是把此前按 root / core / specs / references / history batches 记录的 grouped coverage 与当前文件清单对齐，避免把“文件名未逐字点名”误读成未审文档，也避免把 MAG coverage closeout 升级成 runtime、production 或 physical-delete 授权。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md` 和本文件。
- Current inventory script over `README*` and `docs/**/*.md`: `inventory_count=120`。
- Reconcile scan: 26 paths were not literal substrings in this local ledger before this tranche, but all map to earlier grouped coverage: root/agent/contracts/runtime README support, docs/core/active portfolio entry coverage, current specs/thin index coverage, 2026-04-06 history specs coverage, non-spec history coverage, or the later global compaction row.
- Machine/source truth: `contracts/runtime-program/current-program.json`、`contracts/functional_privatization_audit.json`、`contracts/production_acceptance/mag-production-acceptance.json`、`contracts/external_evidence/mag-evidence-receipt-ledger.json`、`MagDomainRuntime.describe_topology()` and `public_cli.PUBLIC_GROUP_COMMANDS`。

Fresh semantic result：

- Current MAG inventory remains 120 markdown files in scope. No new MAG `README*` or `docs/**/*.md` appeared after the recorded MAG coverage tranches.
- The 26 previously not-literal ledger paths are reconciled as covered by grouped entries, not reopened doc gaps:
  - `README.zh-CN.md`、`agent/README.md`、`contracts/README.md`、`docs/README.md`、`docs/active/README.md`、`docs/active/opl-private-implementation-migration-inventory.md`、`docs/docs_portfolio_consolidation.md` and `runtime/README.md` were covered by the docs portfolio entry coverage tranche as MAG entry/support docs.
  - `docs/public/README.md` and all current `docs/specs/*.md` records were covered by the specs / thin index coverage tranche.
  - `docs/history/specs/2026-04-06-*.md` were covered by the 2026-04-06 foundation history specs tranche.
  - `docs/history/plan-completion-audit-2026-05-01.md` falls under non-spec history / compacted final whole-doc reconciliation; it remains provenance and does not reopen active plan truth.
- Current machine truth still prevents overclaiming: OPL/Temporal is the default task runtime owner, MAG does not implement daemon / scheduler / attempt loop / attempt ledger, `claims_domain_repo_physical_delete_authorized=false`, `claims_production_long_run_soak_complete=false`, provider completion is not domain/fundability/submission ready, and MAG does not implement App workbench or OPL runtime.
- Fresh clean-runner probe of `MagDomainRuntime.describe_topology()` reports `runtime_owner="one-person-lab"`, `can_claim_generic_runtime_owner=False`, default stage attempt executor `Codex CLI`, and optional proof executor `Hermes-Agent` with `explicit opt-in only`; `PUBLIC_GROUP_COMMANDS` exposes grouped `workspace`、`mainline`、`domain-handler`、`authority`、`pass` and `package` command groups.
- No prose body needed additional rewrite in this reconcile pass. The effective change is closing the local coverage accounting ambiguity.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Current 120-file `README*` / `docs/**/*.md` inventory reconciled against prior MAG grouped coverage entries; support read of core/active/ideal-state docs, current contract truth, domain runtime topology and grouped public CLI surface. | this coverage ledger |

Archived / tombstoned / deleted docs：无。本轮没有发现新的 MAG doc path 需要归档、tombstone 或删除。

Uncovered docs：

- `med-autogrant`: none in the current 120-file `README*` / `docs/**/*.md` inventory for the recorded MAG governance scope. Future new docs or later source/contract changes can reopen specific sections.
- Other OPL-series repos remain governed by the global coverage ledger: OPL and MAS still have open repo-wide coverage areas, RCA/App writes remain delayed while their main checkouts carry external dirty implementation/release lanes, and OMA remains covered by its earlier full README/docs tranche unless changed later.

Remaining stale / retire candidates：

- MAG runtime/evidence/physical-cleanup tails remain open as implementation/evidence work, not docs uncovered scope: physical delete authorization, production long-soak, submission-ready human gate, sustained real consumption and long-soak evidence.
- Any future MAG docs wording that turns OPL projection, Temporal provider completion, descriptor conformance, history provenance, optional Hermes proof lane or zero open worklist into grant-domain ready、fundability ready、submission/export ready、production ready、MAG-owned generic runtime or App/workbench ownership is stale pollution.

Next tranche write scope：

- Prefer OPL uncovered support docs or MAS remaining repo-wide docs while RCA/App main checkouts still carry external dirty implementation/release lanes.
- Return to MAG only if new MAG docs appear, later code/contract changes reopen a section, or a source/test owner lane closes one of the remaining runtime/evidence/physical-cleanup tails and requires doc foldback.

Verification before absorb：

- MAG docs verification passed in the tranche worktree: `git diff --check` exited 0, strict README/docs/contracts conflict-marker scan had no hits, and OPL Doc Governance doctor returned `finding_count=0`, active truth `pass`.
- MAG clean-runner topology probe passed via `./scripts/run-python-clean.sh`: `MagDomainRuntime.describe_topology()` returned OPL runtime ownership, no generic MAG runtime ownership, `Codex CLI` default executor and explicit opt-in `Hermes-Agent`; `PUBLIC_GROUP_COMMANDS` returned workspace/mainline/domain-handler/authority/pass/package groups.

### 2026-05-27 MAG exact active/spec path reconcile tranche

本轮对 MAG 当前 `README*` 与 `docs/**/*.md` 做 exact-path ledger 对账。目标是关闭上一轮 final inventory reconcile 之后由文件清单变化和 grouped coverage 写法留下的 17 个 exact-string gap，避免把“路径没有逐字出现在本地 ledger”误读成未审文档；本轮不重新声明 MAG runtime、production、grant ready、submission/export ready 或 physical-delete 授权。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md` 和本文件。
- Current inventory script over `README*` and `docs/**/*.md`: `inventory_count=117`。
- Exact-string reconcile scan before this tranche: `missing_by_exact_string=17`。
- First-screen / role read of the 17 paths listed below, plus support read of lifecycle map and current runtime owner surfaces.

Exact paths reconciled：

- `docs/history/specs/2026-04-06-med-auto-grant-top-level-design.md`
- `docs/history/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`
- `docs/history/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`
- `docs/history/specs/2026-04-06-object-model-schema-v1.md`
- `docs/specs/2026-04-07-durability-model-clarification.md`
- `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `docs/specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md`
- `docs/specs/2026-04-12-p4b-direct-grant-entry-composition-current-truth.md`
- `docs/specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md`
- `docs/specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`
- `docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md`
- `docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md`
- `docs/specs/2026-04-13-p4e-schema-backed-product-status-and-manifest-current-truth.md`
- `docs/specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md`
- `docs/specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md`
- `docs/specs/2026-04-23-authoring-completion-semantics-current-truth.md`
- `docs/specs/2026-04-27-ai-first-quality-boundary-current-truth.md`

Fresh semantic result：

- The four `docs/history/specs/2026-04-06-*.md` files already carry first-screen lifecycle notes plus owner / purpose / state / machine-boundary signals. They remain `history` / historical foundation provenance and are governed by the `../history/specs/2026-04-06-*` row in `docs/specs/specs_lifecycle_map.md`.
- `docs/specs/2026-04-07-durability-model-clarification.md` and `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md` remain `support_current_truth` records. They only guard durability / formal-entry vocabulary and explicitly prevent restoration of local journal, attempt ledger, old public runtime commands, Gateway/local-manager path or MAG-owned generic runtime.
- The 2026-04-12 / 2026-04-13 P4 product-entry, route, manifest and local package specs remain support current-truth by subsection. They describe current product-entry / route / package surfaces under source, schemas, product-entry manifest and `contracts/runtime-program/current-program.json`; they do not claim mature App/workbench, hosted runtime completion, external submission, grant ready, production ready or physical-delete authorization.
- The 2026-04-13 critique executor spec, 2026-04-22 quality/autonomy spec, 2026-04-23 authoring-completion spec and 2026-04-27 AI-first quality-boundary spec remain active current specs in the narrow boundaries listed by `docs/specs/specs_lifecycle_map.md`.
- No body rewrite was needed. This tranche records exact coverage only and leaves current machine truth unchanged: OPL/Temporal owns hosted task runtime, `Codex CLI` is the default stage executor, `Hermes-Agent` is explicit opt-in proof / executor adapter provenance, and MAG owns grant truth, quality/export verdicts, package authority, memory decision and owner receipts.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | First-screen / role read of the 17 exact paths listed above; support read of specs lifecycle map, history specs index, core docs, active gap plan and current runtime owner surfaces. | this coverage ledger |

Archived / tombstoned / deleted docs：无。这 17 个 paths 已有合法长期角色；本轮只补 exact-path ledger，不做移动、tombstone、删除或正文重写。

Uncovered docs：

- `med-autogrant`: exact-string inventory now has no uncovered `README*` / `docs/**/*.md` path in the current 117-file scope once this entry is counted. Future new docs or later source/contract changes can reopen specific sections.
- Other OPL-series repos remain governed by the global coverage ledger. OMA and MAS have prior full/exact reconcile coverage recorded; OPL, RCA and App still depend on their own ledger state and active worktree safety before global goal closure.

Remaining stale / retire candidates：

- Any future MAG docs wording that promotes historical foundation specs, support current-truth records, active current specs, lifecycle-map rows, OPL projection, Temporal provider completion, optional Hermes proof lane or zero open worklist into grant-domain ready、fundability ready、submission/export ready、production ready、MAG-owned generic runtime or App/workbench ownership is stale pollution.
- MAG implementation/evidence tails remain separate from docs coverage: physical delete authorization, production long-soak, submission-ready human gate, sustained real consumption and long-soak evidence still require their own source/test/receipt closeout.

Next tranche write scope：

- Continue OPL series whole-docs coverage outside MAG, prioritizing a repo whose main checkout and worktrees are safe for this automation.
- Return to MAG only if new MAG docs appear, later code/contract changes reopen a section, or an implementation/evidence owner lane closes one of the remaining runtime/evidence/physical-cleanup tails and requires doc foldback.

### 2026-05-28 MAG current inventory refresh tranche

本轮在 2026-05-27 MAG owner-payload、workspace receipt scaleout 与 grant-facing user stage log 文档折回之后，重新对 MAG 当前 `README*` 与 `docs/**/*.md` 做 exact inventory refresh。目标是确认 recent `docs/status.md`、`docs/active/mag-ideal-state-cross-repo-gap-plan.md` 与 `docs/decisions.md` 改动没有重新打开文档生命周期缺口，也不把 MAG runtime/evidence tail 误写成生产完成或物理删除授权。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md`、本文件。
- Recent doc-writing commits since 2026-05-27：`b03f0cd`、`68733c0`、`cbda7dd`、`5e9013e`、`c323933`、`e7913dd`、`187d871`。
- Current inventory script over repo-root `README*` and `docs/**/*.md`: `inventory_count=120`、`missing_by_exact_string=0` after previously recorded MAG coverage entries.
- Machine/source truth：`contracts/runtime-program/current-program.json`、`contracts/functional_privatization_audit.json`、`contracts/production_acceptance/mag-production-acceptance.json`、`MagDomainRuntime.describe_topology()`、`public_cli.PUBLIC_GROUP_COMMANDS`。

Fresh semantic result：

- Current MAG inventory has no uncovered exact path in the recorded `README*` / `docs/**/*.md` scope. No new MAG markdown path appeared that lacks a lifecycle role or coverage owner.
- The recent `docs/status.md` and active gap plan edits are current truth foldback for owner-payload response, manifest consumer evidence, workspace receipt scaleout, OPL refs-only verification and grant-facing user stage log contract. They remain bounded by the same authority split: MAG owns grant truth、fundability / quality / export verdict、package authority、memory accept/reject、owner receipt and typed blocker; OPL owns Temporal provider runtime、queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper and App/workbench shell.
- `contracts/runtime-program/current-program.json` still declares `default_task_runtime_owner=one-person-lab`、`default_runtime_substrate=temporal`、`mag_implements_daemon=false`、`mag_implements_scheduler=false`、`mag_implements_attempt_loop=false`、`mag_owns_attempt_ledger=false`、`claims_domain_repo_physical_delete_authorized=false` and `claims_production_long_run_soak_complete=false`. `mag_functional_structure_gap_count=0` remains a structural classification signal, not strict source-purity, production-ready, App sustained-consumption or physical-delete closeout.
- `MagDomainRuntime.describe_topology()` still reports runtime ownership as OPL / one-person-lab, MAG as repo-side domain adapter / grant authority, `Codex CLI` as default stage executor, and `Hermes-Agent` as explicit opt-in proof executor only. `PUBLIC_GROUP_COMMANDS` still exposes grouped `workspace`、`mainline`、`domain-handler`、`authority`、`pass` and `package` commands rather than retired flat runtime aliases.
- No prose body rewrite, archive, tombstone or deletion was needed. This tranche only records exact inventory refresh after recent live-truth doc foldback.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Current 120-file `README*` / `docs/**/*.md` inventory refreshed; support read of recent doc-writing commits, core/active/ideal-state docs, current contract truth, domain runtime topology and grouped public CLI surface. | this coverage ledger |

Archived / tombstoned / deleted docs：无。本轮没有发现新的 MAG doc path 需要归档、tombstone 或删除。

Uncovered docs：

- `med-autogrant`: none in the current 120-file `README*` / `docs/**/*.md` inventory for the recorded MAG governance scope. Future new docs or later source/contract changes can reopen specific sections.
- Other OPL-series repos remain governed by the global coverage ledger. OPL、MAS、RCA and App still need their own remaining section-level coverage / safe-lane reconciliation before the global `/goal` can close.

Remaining stale / retire candidates：

- MAG implementation/evidence tails remain open as source/test/receipt work, not uncovered docs: physical delete authorization, production long-soak, submission-ready human gate, sustained real App/operator consumption and long-soak evidence.
- Any future MAG docs wording that turns OPL projection、Temporal provider completion、owner-payload refs-only verification、workspace receipt scaleout、grant-facing user stage log projection、optional Hermes proof lane or zero exact inventory gap into grant-domain ready、fundability ready、submission/export ready、production ready、MAG-owned generic runtime、App/workbench ownership or physical delete authority is stale pollution.

Next tranche write scope：

- Continue OPL series whole-docs coverage outside MAG, prioritizing OPL / MAS / RCA safe document clusters and delaying App body docs until active App implementation/release lanes are safe or explicitly assigned.
- Return to MAG only if new MAG docs appear, later code/contract changes reopen a section, or an implementation/evidence owner lane closes one of the remaining runtime/evidence/physical-cleanup tails and requires doc foldback.

Verification before absorb：

- `git diff --check` passed.
- Strict README/docs/contracts conflict-marker scan passed.
- OPL Doc Governance doctor returned `finding_count=0`, active truth `pass`.

### 2026-05-28 MAG specs index lifecycle revalidation tranche

本轮在 OPL series hygiene 后重新核对 MAG `docs/specs/` 当前索引、specs lifecycle map 与 live runtime/source-shape 机器边界。目标是确认 `docs/specs/` 没有把 support specs、历史 `Current Truth` 标题、product-entry manifest 支撑记录或 active current specs 误提升为 runtime owner、production-ready、App/workbench ready、submission/export ready 或 physical-delete authority。本轮不改 active truth，不关闭 OPL series 全局 `/goal`。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md` 和本文件。
- Current inventory script over repo-root `README*` and `docs/**/*.md`: `inventory_count=120`.
- Current `docs/specs/*.md` inventory: 15 files, consisting of `README.md`, `specs_lifecycle_map.md`, four `active_current_spec` records and nine `support_current_truth` records.
- Machine/source truth: `contracts/runtime-program/current-program.json`, `contracts/functional_privatization_audit.json`, `src/med_autogrant/product_entry_parts/functional_closure.py`, product-entry manifest schema/tests, and public CLI / domain-entry source refs found by live search.
- OPL Doc Governance doctor output from this run: `finding_count=0`, active truth `pass`.

Fresh semantic result：

- `docs/specs/README.md` still states that only four specs are active current specs: critique executor vocabulary, AI-first quality boundary, authoring completion semantics, and quality/autonomy/family grammar. Those files' first-screen metadata scopes each spec to its narrow active boundary and routes overall product status, runtime owner, App/workbench and evidence gates back to core docs、active plan、contracts/schema/source and `current-program.json`.
- The nine support current-truth records currently in `docs/specs/` retain first-screen lifecycle notes and support-only roles. Formal-entry and durability support records explicitly prevent restoring local journal、attempt ledger、old runtime commands、Gateway/local-manager path or MAG-owned generic runtime. Product-entry / route / package support specs remain bounded to schema/source/product-entry manifest support subsections and do not claim mature App/workbench、hosted runtime completion、external submission、grant-ready、production-ready or physical-delete authority.
- `contracts/runtime-program/current-program.json` still declares OPL/Temporal as task runtime owner: `default_task_runtime_owner=one-person-lab`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, and `mag_owns_attempt_ledger=false`.
- `contracts/functional_privatization_audit.json` still reports `standard_agent_source_shape_status=landed`, nested `functional_followthrough_gap_classification.mag_functional_structure_gap_count=0`, `claims_domain_repo_physical_delete_authorized=false`, and `claims_production_long_run_soak_complete=false`. This remains source-shape / classification evidence only, not strict source-purity, production-ready, App sustained-consumption, bridge-exit or physical-delete closeout.
- Live search confirms product-entry manifest truth is generated by source/schema/tests (`build_product_entry_manifest`, `product-entry-manifest.schema.json`, product-entry cases) and referenced by docs as a machine surface; there is no repo-tracked `contracts/product-entry-manifest.json` to treat as a second static truth source.
- No prose body rewrite, archive, tombstone or deletion was needed. This tranche records fresh specs-index lifecycle validation only.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, first-screen role read of representative active/support specs, support read of core docs、active plan、ideal-state reference、current-program runtime owner fields、functional audit source-shape fields and product-entry manifest source/schema/test refs. | this coverage ledger |

Archived / tombstoned / deleted docs：无。本轮没有发现 `docs/specs/` 下需要移动、tombstone、删除或正文重写的 spec。

Uncovered docs：

- `med-autogrant`: none newly opened in the current `README*` / `docs/**/*.md` inventory for this specs-index lifecycle tranche. This tranche revalidates the specs layer; it does not re-read every historical spec body already covered by prior MAG date/topic batches.
- Other OPL-series repos remain under the global coverage ledger. OPL、MAS、RCA and App still need their own remaining section-level coverage / safe-lane reconciliation before the global `/goal` can close.

Remaining stale / retire candidates：

- Any future MAG specs wording that turns support specs、active current specs、product-entry manifest support records、OPL projection、Temporal provider completion、optional Hermes proof lane or zero docs inventory gap into grant-domain ready、fundability ready、submission/export ready、production ready、MAG-owned generic runtime、App/workbench ownership or physical-delete authority is stale pollution.
- MAG implementation/evidence tails remain source/test/receipt work: physical delete authorization, production long-soak, submission-ready human gate, sustained real App/operator consumption and long-soak evidence.

Next tranche write scope：

- Continue OPL series whole-docs coverage outside MAG, prioritizing OPL / MAS / RCA safe document clusters. App body docs remain delayed while active App implementation/release lanes are dirty or conflicting.
- Return to MAG only if new MAG docs appear, source/contract changes reopen a spec section, or an implementation/evidence owner lane closes one of the remaining runtime/evidence/physical-cleanup tails and requires doc foldback.

### 2026-05-28 MAG 2026-04-09 R3/R4/R5 history specs coverage tranche

本轮覆盖 MAG `docs/history/specs/` 下 2026-04-09 R3/R4/R5 与 post-R5A local-runtime hardening 历史 specs。目标是确认这些 direct-file 历史入口不会把旧 R3/R4/R5 activation package、local runtime ladder、bare CLI command、host-agent、hostedization prep 或 post-R5A hardening 词汇误读成当前执行顺序、MAG-owned generic runtime、public runtime command、attempt ledger、App/workbench readiness、hosted runtime completion、submission/export-ready verdict、physical-delete authority 或 active implementation queue。本轮不改 active truth，不关闭 OPL series 全局 `/goal`。

Live truth inputs：

- MAG `AGENTS.md`、`TASTE.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/references/med-auto-grant-ideal-state.md`、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/specs/README.md` 和本文件。
- Reviewed history specs: `docs/history/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`, `docs/history/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`, `docs/history/specs/2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md`, `docs/history/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`.
- Machine/source truth surfaces: `contracts/runtime-program/current-program.json`, `src/med_autogrant/public_cli.py`, `src/med_autogrant/domain_runtime_parts/substrate.py`, `src/med_autogrant/final_package.py`, `src/med_autogrant/hosted_contract_bundle.py`, `src/med_autogrant/domain_entry.py`, current specs lifecycle map, focused source/test refs found by live search.
- Fresh clean-runner read-model probe: `MagDomainRuntime().describe_topology()`, `public_cli.public_cli_command(...)`, and `PUBLIC_GROUP_COMMANDS` for `workspace` / `pass` / `package`.
- OPL Doc Governance doctor output from this run: `finding_count=0`, active truth `pass`.

Fresh semantic result：

- All four reviewed files already carry first-screen lifecycle notes plus `Owner` / `Purpose` / `State` / `Machine boundary`. No body rewrite was needed.
- R3.A remains historical machine-applicable revision mutation provenance. Current revision behavior is source/test owned: `execute-revision-pass` maps to grouped public CLI `pass revision`; AI-first quality guard requires mutation payloads to be AI-authored and machine-applicable. This does not create a new LLM authoring mode, runtime owner, hosted runtime claim or submission/export verdict.
- R4.A remains historical final freeze / export activation provenance. Current package behavior is source/test owned: `build-final-package` maps to grouped public CLI `package final-package`, `final_package.py` only builds local final package documents from revised/frozen workspaces and allowed checkpoint statuses, and MAG retains package/export authority. This does not authorize external submission, App/release readiness, hosted runtime completion or production readiness.
- R5.A remains historical hosted-friendly contract export provenance. Current hosted-contract bundle behavior is source/test owned: `build-hosted-contract-bundle` maps to grouped public CLI `package hosted-contract-bundle`, `hosted_contract_bundle.py` emits an integration/reference contract bundle with `session_owner=one-person-lab` and MAG authority refs. It does not implement actual hosted runtime, Web UI, remote execution, multi-tenant platform or Gateway/federation route.
- Post-R5A local-runtime hardening brief remains historical local-runtime closeout / honest-stop provenance. Its old `runtime-run` / `runtime-resume` / run journal / host-agent wording is guarded by lifecycle headers and current no-resurrection source/tests; it is not a current MAG-owned daemon, scheduler, attempt loop, attempt ledger or public runtime command.
- `contracts/runtime-program/current-program.json` still declares `default_task_runtime_owner=one-person-lab`, `default_runtime_substrate=temporal`, `mag_implements_daemon=false`, `mag_implements_scheduler=false`, `mag_implements_attempt_loop=false`, and `mag_owns_attempt_ledger=false`.
- Fresh `MagDomainRuntime().describe_topology()` still reports `runtime_owner="one-person-lab"`, `can_claim_generic_runtime_owner=false`, `default_formal_entry="CLI"`, default stage executor `Codex CLI`, and optional proof executor `Hermes-Agent` with `explicit opt-in only`.
- Fresh public CLI mapping confirms old bare command examples must be read through current grouped shape: `stage-route-report -> workspace route-report`, `execute-revision-pass -> pass revision`, `build-artifact-bundle -> package artifact-bundle`, `build-final-package -> package final-package`, `build-hosted-contract-bundle -> package hosted-contract-bundle`.

| repo | reviewed docs/sections | edited docs |
| --- | --- | --- |
| `med-autogrant` | Full paragraph read of the four 2026-04-09 R3/R4/R5/post-R5A history specs listed above; support read of history specs index, specs lifecycle map, active gap plan, ideal-state reference, current-program runtime owner fields, grouped public CLI mapping, domain runtime topology, final package / hosted contract source and retired-command no-resurrection refs. | this coverage ledger |

Archived / tombstoned / deleted docs：无。这四份文件仍是有用的 history provenance；不需要移动、tombstone、删除或正文重写。

Uncovered docs：

- `med-autogrant`: remaining `docs/history/specs/*.md` files outside the previously recorded foundation / P2-P5 / R1-R3 batches and this 2026-04-09 R3/R4/R5 batch remain under later MAG date/topic coverage unless already covered by the exact inventory reconcile entries. Higher-risk remaining direct-file batches include 2026-04-10 post-R5A fail-closed records, 2026-04-11 Hermes/reset/local-runtime records and 2026-04-12 hosted / OPL handoff records.
- Other OPL-series repos remain under the global coverage ledger. OPL, MAS, RCA and App still need their own remaining section-level coverage / safe-lane reconciliation before the global `/goal` can close.

Remaining stale / retire candidates：

- Any future direct-file use of these 2026-04-09 specs as current public CLI command shape, runtime owner, default runtime, local run journal authority, attempt ledger, hosted runtime completion, Web UI/remote execution readiness, submission/export-ready verdict, production readiness, physical-delete authority or compatibility-interface source is stale pollution.
- Historical `runtime-run` / `runtime-resume` / host-agent / hostedization prep vocabulary must remain provenance unless a current active owner and source/contract/tests explicitly re-admit it. Current no-resurrection tests guard retired commands from reappearing as active public/domain commands.
- R4/R5 package and hosted-contract wording must not be upgraded to actual external submission, App/release readiness, Gateway/federation route, OPL generated/hosted caller readiness, production long-soak completion or MAG-owned generic runtime.

Next tranche write scope：

- Continue MAG `docs/history/specs/*.md` in date/topic batches only if needed by global coverage, prioritizing 2026-04-10 post-R5A fail-closed records or 2026-04-11/2026-04-12 Hermes / hosted handoff specs because stale provider/hosted wording risk is higher there.
- Prefer OPL / MAS / RCA safe document clusters for the next OPL-series tranche while App release docs remain tied to dirty/conflicting release lanes.
