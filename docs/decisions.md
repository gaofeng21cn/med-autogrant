# 决策记录

## 2026-05-19：清理 stale generic runtime retirement lane

- 决策：`.worktrees/retire-generic-runtime-surfaces` / `codex/retire-mag-generic-runtime-surfaces` 只作为已吸收过的历史 lane 处理，不再向当前 `main` 重放。该 worktree 的有效删除目标已由 `7d877b8 Retire MAG local runtime surfaces` 覆盖；保留下来的差异只是不应重放的旧树状态与非语义格式差异。
- 理由：该分支基点 `fd48dc6` 已是当前 `main` 的祖先。直接合入会重新引入 `upstream_hermes.py`、`test_local_runtime.py`、`test_upstream_hermes.py` 等旧 local runtime / Hermes proof surface，并会反向删除当前 `contracts/stage_control_plane.json` 与 `src/med_autogrant/stage_control_plane.py` 的 stage runtime event refs。
- 影响：MAG 当前 generic runtime cleanup 继续以 active source、`functional_privatization_audit`、product-entry manifest、sidecar export、current-program 和 OPL family adoption contract 为准；剩余 gap 是 OPL/App/production caller 外部证据，不在 MAG 仓内恢复 local journal、attempt ledger、scheduler/daemon、Hermes probe 或 compatibility alias。

## 2026-05-18：把 MAG retained functions 硬化为 AI-first authority surfaces

- 决策：`mag_consumer_thinning_contract.minimal_authority_functions` 继续保留既有 `function_id` 兼容字段，但新增 `authority_surface_id`、`work_mode`、`judgment_owner`、`programmatic_role`、`ai_stage_artifact_required`、`mechanical_decision_forbidden` 和 `programmatic_verdict_generation_allowed=false`。pack compiler input 同步投影 minimal authority surface taxonomy 与逐项 surface contract。
- 理由：fundability、quality、export 和 strategy memory accept/reject 是 AI-first grant judgment，不应被表达成 MAG 私有函数直接计算 ready verdict。程序面只允许验证 AI/domain stage artifact、materialize refs、签 receipt、返回 typed blocker 或 safe action metadata；package、owner receipt 和 grant helper 是 programmatic guard，也不能生成 verdict。
- 影响：MAG 仍持有 grant truth、verdict refs、package authority、memory accept/reject、owner receipt 和 grant helper authority，但这些保留面现在按 AI-first judgment surface / programmatic authority guard 分层。该决策不实现 OPL generic runtime、scheduler、workbench、memory transport 或 package lifecycle shell，也不声明 OPL production caller、App workbench 消费或 long-run soak 完成。

## 2026-05-18：落地 MAG external evidence request pack

- 决策：`mag_consumer_thinning_contract` 新增 `external_evidence_request_pack`，并由 product-entry manifest、sidecar export、schema、`functional_privatization_audit`、`current-program` 与 `opl-family-contract-adoption` 共同投影。该 pack 只请求 OPL/App/production caller 返回 refs、receipt shapes、typed blocker、no-regression evidence 和 parity evidence。
- 理由：MAG repo 侧功能/结构 gap 已收敛到 handler/ref-only/minimal authority 边界；剩余缺口属于外部 OPL generated/hosted caller、Codex App workbench、production/default caller、Temporal provider long-soak 和 continuous live receipt reconciliation 证据。用 request pack 可以把这些需求机器化，同时避免在 MAG 内重建 OPL runtime、generic runner、queue、attempt ledger 或 App workbench。
- 影响：current truth 现在明确 `active_caller_owner=med-autogrant` / `mag_direct_domain_entry_until_opl_caller_evidence`，并继续声明 `claims_opl_replacement_exists=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false`。该决策不关闭任何外部证据门，不把 provider completion、receipt request 或 package refs 写成 fundability-ready、quality-ready、export-ready 或 production soak success。

## 2026-05-17：退役 MAG 本地 runtime / Hermes probe active surface

- 决策：`runtime-run`、`runtime-resume` 与 `probe-upstream-hermes` 从 MAG public CLI、`MedAutoGrantDomainEntry` service-safe catalog、product-entry session continuity、hosted bundle schema 和默认 smoke 断言中移除；session/resume 入口改由 OPL generated surface refs 表达。
- 理由：本地 journal runtime、attempt ledger 和 upstream Hermes probe 属于通用 session/runtime/proof 外围。标准 OPL Agent 目标态要求这类 shell 由 OPL generated/hosted surface 持有，MAG 只提交 declarative grant pack、refs 和最小 authority function。
- 影响：MAG 继续保留 grant route truth、fundability/quality/export verdict、package authority、grant transition oracle、memory accept/reject、owner receipt 和 grant-native helper；旧 runtime/probe 面从 active source、active contract 与默认测试中物理删除，只能在 `docs/history` / provenance 语境中解释来源，不能作为 compatibility alias、标准模板或默认入口恢复。

## 2026-05-16：收紧 MAG thin surface 输出层的私有功能状态 guard

- 决策：`mag_consumer_thinning_contract.thin_surface_output_guard` 现在显式列出 `private_functional_state_output_classes_forbidden`，禁止 MAG sidecar / manifest 输出 local runtime journal、local attempt ledger、attention queue、stage attempt ledger、package lifecycle、source intake、operator workbench、scheduler daemon 和 Hermes state-db runtime state。
- 理由：只把私有功能模块分类为 OPL-owned replacement 不够；输出层也必须 fail-closed，避免 MAG 通过 sidecar/product surface 继续泄露或固化 repo-local runtime state，从而重新形成私有 generic runtime owner。
- 影响：MAG 仍可输出 grant-owned refs、owner receipt、typed blocker、verdict refs 和 domain action metadata；OPL 继续持有这些私有功能状态对应的 generic ledger、queue、source/lifecycle/workbench/scheduler/observability shell。该 guard 不删除仍承担 domain thin adapter 或 explicit proof lane 的 active code path，也不声明 production long-run soak 完成。

## 2026-05-16：落地 MAG privatized functional module audit

- 决策：`mag_consumer_thinning_contract` 新增 `privatized_functional_module_audit`，并由 sidecar export 同步投影。2026-05-17 后该审计面不再把通用功能面长期标成 replacement/tombstone，而是分成四类：`declarative_pack_surface`、`refs_only_adapter`、`minimal_authority_function`、`legacy_proof_tombstone`。
- 理由：MAG 需要让 OPL 统一审计读取非知识层面的功能边界，同时不能把 grant `lifecycle_stage`、package readiness / submission-ready、fundability / quality / export verdict、grant transition oracle、owner receipt 或 strategy memory accept/reject 误判成可删除的通用 runtime 面。
- 影响：runtime registration、task lifecycle、source intake 作为 declarative grant pack 输入；lifecycle/observability/sidecar/package/workbench 只作为 refs-only adapter；grant lifecycle、fundability/quality/export verdict、package authority、transition oracle、owner receipt 和 memory accept/reject 是最小 authority function；旧 Hermes/Gateway/local-manager、local journal/attempt ledger、patch bridge、compat aggregate test、legacy shell alias 和 repo-owned scheduler/daemon 是 no-active-caller legacy proof tombstone。本决策不声明 OPL generated/hosted surface 已生产接入，也不声明 production long-run soak 完成。

## 2026-05-16：落地 MAG consumer/thinning contract

- 决策：`product-entry-manifest` 新增 `mag_consumer_thinning_contract`，`product sidecar export` 同步投影该 surface。该合同把 MAG adapter 角色固定为 grant domain authority pack + thin program surface，只输出 grant-owned refs、owner receipt、typed blocker、verdict refs 和 domain action metadata。
- 理由：当前优先级是让 MAG 配合 OPL-led program 收薄，而不是在 MAG 内继续实现 workspace/source intake shell、memory locator/writeback transport、package/export lifecycle shell、generic transition runner、operator workbench/observability/SLO 或 agent scaffold template。OPL replacement 如果尚未存在，MAG 只能写 contract expectation / handoff note / guard，不能删除仍承担真实功能的 active path。
- 影响：`ideal_state_closure_status` 的 phase map 按 active plan 调整为 P1 adapter thinning、P2 package/export lifecycle handoff、P3 memory locator/writeback handoff、P4 scaffold/legacy cleanup、P5 focused hosted receipt verification、P6 live soak。该决策不声明 OPL replacement 已存在，不声明 production long-run soak 完成，也不改变 MAG 对 fundability、quality、export verdict 和 owner receipt 的 authority。

## 2026-05-16：补齐 MAG-owned refs-only handoff projections

- 决策：MAG 新增 `lifecycle-receipt-bundle`、`memory-receipt-projection`、`package-lifecycle-handoff` 与 `continuous-receipt-reconciliation` 四个 product-entry / grouped CLI surface。它们分别把 cleanup/restore/retention lifecycle receipt refs、accepted/rejected memory receipt refs、package/export lifecycle handoff refs，以及 focused hosted receipt verification + inventory + observability projection 汇总成 OPL shell 可消费的 read projection。
- 理由：这些仍属于 MAG domain package 的 thin program surface：MAG 必须给 OPL 提供 refs、receipt、typed blocker、gap/export verdict refs、manual portal boundary 和 reconciliation counts，才能让 OPL generic shell 消费；但 MAG 不能在仓内实现 OPL memory transport、artifact/package lifecycle shell、attempt ledger、generic runner、operator workbench、repair 或 live reconciliation daemon。
- 影响：P2/P3/P5 的 MAG repo-local surface gap 进一步关闭，剩余变为真实 workspace/runtime receipt 泛化、OPL/App shell 生产消费、持续 live receipt reconciliation 和 long-run soak evidence。本决策不声明 OPL replacement 已生产接入，不把 receipt verification、no-regression evidence、provider completion 或 continuous snapshot 写成 fundability-ready、quality-ready、export-ready 或 production long-run soak。

## 2026-05-16：跟进 OPL conflict / observability / workbench projection surface

- 决策：`mag_consumer_thinning_contract` 对齐 OPL 最新 standard scaffold generator 与 runtime projection surface，把 `artifact_package_lifecycle_shell`、`operator_workbench_drilldown_shell`、`observability_repair_projection`、family conflict envelope、stage-attempt usage/control-loop 和 runtime observability export 写成 MAG 只读消费/refs 投影边界。
- 理由：OPL 新增的 conflict/blocker、observability、usage/control-loop 与 product-operator projection 都是 framework/control-plane surface。MAG 可以提供 receipt、typed blocker、artifact/memory refs、safe action refs 和 grant transition oracle ref，但不能复制 OPL ledger、repair、workbench 或 SLO owner。
- 影响：MAG schema、current-program、sidecar export 和 focused tests 现在禁止 `provider_completion_is_grant_ready`、`mag_executes_opl_repair`、generic workspace/source intake、generic artifact gallery、generic operator workbench 与 generic observability/SLO owner。该决策仍不声明 OPL replacement 已生产存在，也不关闭 grant-stage live soak。

## 2026-05-15：落地 MAG-owned grant transition oracle table / oracle fixtures

- 决策：`product-entry-manifest` 新增顶层 `grant_transition_oracle`，并让 `ideal_state_closure_status.mag_owned_transition_oracle` 指向同一 MAG-owned surface。该 surface 固化 grant transition table、oracle fixtures、stage/action/ref validation 和 OPL 不可裁决 fundability / authoring quality / submission-ready export 的边界。
- 理由：MAG gap plan 中的 transition/oracle 缺口已经可以由 MAG 自己落成 domain spec；generic state-machine runner、matrix runner、queue、retry/dead-letter 和 provider attempt 仍归 OPL。把 MAG 语义先落成 schema-backed manifest surface，可以让后续 OPL runner ingest 有稳定输入，同时避免在 MAG 内复制通用 runner。
- 影响：transition table / oracle fixtures 不再是 `not_landed` gap；剩余 gate 是 OPL runner ingest、真实 provider-hosted transition attempt、retry/dead-letter 和 live receipt 对账。本决策不声明 OPL-hosted production long-run soak 完成，也不改变 MAG 对 grant truth、fundability、authoring quality 和 export verdict 的 owner authority。

## 2026-05-15：把 transition/oracle gap 与 direct-retirement posture 投影到 ideal-state closure status

- 决策：`product-entry-manifest.ideal_state_closure_status` 新增 `mag_owned_transition_oracle` 与 `direct_retirement_posture`。前者先把 MAG-owned transition table / oracle fixture 记录为 planned spec gap，并把 generic runner / matrix runner / queue / retry-dead-letter 边界留给 OPL；后者把 active plan 中的 direct retirement posture 变成机器可读投影。随后同日 follow-through 已把 `mag_owned_transition_oracle` 升级为 landed domain spec surface。
- 理由：当前可落地工作是把 gap plan 的 MAG-owned 后续边界固化到 manifest、schema、测试和文档索引，而不是伪造真实 long-run soak 或在 MAG 仓里建设通用 runner。OPL 可以执行 MAG 声明的 transition spec，但不能解释 fundability-ready、quality-ready 或 export-ready。
- 影响：MAG 后续 transition/oracle 实施有单一 active plan 入口和 manifest surface；旧 compatibility alias、facade patch bridge、re-export facade、compatibility-only 聚合测试和 legacy flat shell alias 不再作为保留目标。本决策本身不声明 OPL-hosted production long-run soak 完成。

## 2026-05-14：把 MAG ideal-state plan 收成机器可读 closure status

- 决策：`product-entry-manifest` 新增顶层 `ideal_state_closure_status`，sidecar export 同步投影该 surface；它把 `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 的 P0-P5 拆成 MAG repo 已落地 surface 与外部 evidence gate。
- 理由：计划中的 P1/P2/P3/P4 同时包含 OPL-hosted live soak、OPL generic primitive 生产消费、真实 workspace memory body migration 和 lifecycle receipt 对账，这些不能由 MAG repo 内代码伪造成完成。MAG 应把可负责的 owner surface、receipt writer、schema 与 authority boundary 落到 manifest，并把真实运行证据明确留作 typed gate。
- 影响：MAG repo 内不再把该 plan 当作未实现代码清单；本轮已补 OPL ledger / MAG runtime receipt 的 controlled no-regression evidence 对账，后续推进应补 workspace memory body / lifecycle receipt 泛化、legacy active-path scan 和真实长时 live soak 证据。`ideal_state_closure_status.claims_production_long_run_soak_complete=false`，OPL 仍不能写 grant truth、memory body、artifact 或 export-ready verdict。

## 2026-05-14：退役 domain runtime facade patch bridge

- 决策：删除 `domain_runtime_parts.patch_targets`，runtime parts 直接引用真实 owner module；测试 patch target 收回到 `domain_runtime_parts.*` owner 模块或实例方法。
- 理由：`domain_runtime.py` 已经收敛为薄 facade / public import surface，继续允许 runtime parts 反向读取 facade 上的 monkeypatch target 会把旧聚合模块重新变成兼容注入层，和当前拆分后的 owner 边界冲突。
- 影响：`med_autogrant.domain_runtime.*` 不再是 runtime 内部依赖替换面；CLI regression tests 也同步迁到当前 grouped public command tokens。内部 flat command names 只保留在 payload / schema / dispatch contract 中。

## 2026-05-14：补齐 owner / lifecycle runtime receipt evidence path

- 决策：MAG 新增 `product owner-receipt-evidence` 与 `product lifecycle-receipt-evidence`，并让 sidecar `stage-attempt/closeout` 与 `lifecycle/receipt` 写出 MAG-owned runtime receipt evidence instance。
- 理由：`owner_receipt_contract` 和 `lifecycle_guarded_apply_proof` 已经固定 return shape 与 authority boundary，但 production closure 需要可调用的 receipt writer，让 OPL-hosted attempt closeout、typed blocker、no-regression evidence 和 cleanup/restore/retention guarded apply 都能落到 runtime receipt instance，同时仍不让 OPL 写 grant truth、memory body、quality verdict 或 submission-ready verdict。
- 影响：MAG repo 内 P1/P4 所需的 receipt evidence path 已可执行；OPL ledger 已能把 MAG sidecar 的 no-regression evidence ref 聚合进 controlled apply / production closeout read model。真实 production closure 仍需要 live soak、workspace memory body / lifecycle apply 泛化和持续 owner-chain 证据。新 writer 属于 MAG product-entry/sidecar callable surface，不提升为公开第一入口，也不改变 Codex CLI 默认 executor。

## 2026-05-13：落地 MAG production functional closure 最小可用 surfaces

- 决策：MAG 在 `product-entry-manifest`、sidecar export、`current-program` 与 OPL family adoption contract 中落地 `owner_receipt_contract`、`controlled_domain_memory_apply_proof.controlled_receipt_instances`、`lifecycle_guarded_apply_proof` 和 `physical_skeleton_follow_through`。
- 理由：OPL production functional closure 需要同构 owner receipt envelope、domain-memory accepted/rejected receipt shape、cleanup/restore/retention guarded apply proof 和 `agent/contracts/runtime/docs` physical skeleton anchor，但 MAG 仍必须持有 grant truth、fundability/authoring quality 和 submission-ready export authority。
- 影响：这是同日 follow-through 前的 minimum surface decision；随后 `product domain-memory-receipt-evidence` 已把 accepted/rejected receipt 从 shape proof 推进到 workspace/runtime evidence path。OPL 仍只能消费 MAG owner receipt refs、typed blocker、no-regression evidence、locator 和 audit refs；真实 OPL-hosted controlled grant-stage attempt、no-regression evidence 和更大范围 source path migration 继续以 typed blocker、direct/hosted parity、restore/provenance proof 与 no-active-caller proof 推进。

## 2026-05-13：补齐 domain-memory runtime receipt evidence path

- 决策：MAG 新增 `product domain-memory-receipt-evidence`，并让 sidecar `domain-memory/decide` 在 MAG accept/reject decision 后写出 runtime receipt evidence instance。
- 理由：minimum proof 只能证明 accepted/rejected receipt shape；functional follow-through 需要真实 workspace/runtime evidence path，但仍不得把 memory body、grant artifact、fundability/quality verdict 或 submission-ready verdict 写入 repo source。
- 影响：`controlled_domain_memory_apply_proof.controlled_receipt_instances.state` 升级为 `runtime_receipt_evidence_path_verified`；`repo_source_layout_audit` 把 legacy active-path residue 固定为 `tombstone_only` 或 `physically_removed_from_active_source`。这不等于 OPL-hosted production long-run soak 已完成。

## 2026-05-12：MAG controlled soak 暂以 typed blocker 收口

- 决策：MAG 在 `product-entry-manifest` 中新增 `controlled_soak_no_regression_attempt`，作为 OPL Temporal controlled stage attempt apply contract 已开放但 MAG domain owner receipt / no-regression evidence 尚未产出时的机器可读 deferred blocker。
- 理由：MAG 不能把未运行的 OPL-hosted production soak 写成成功 receipt，也不能把 fundability、authoring quality 或 submission-ready export verdict 迁给 OPL。该 surface 只暴露 no-regression refs、owner boundary 与下一跳 contract gap。
- 影响：`controlled_soak_no_regression_attempt.state=deferred_typed_blocker`，blocker source 是 `opl_temporal_controlled_stage_attempt_apply_contract`；当前 required return shapes 为 domain owner receipt、typed blocker 或 no-regression evidence。真实 controlled soak 要由 MAG-owned surface 产出 domain receipt 或 no-regression evidence 后才能关闭。

## 2026-05-12：落地 controlled grant-stage domain memory apply proof

- 决策：MAG 在 `product-entry-manifest` 中新增 `controlled_domain_memory_apply_proof`，把 consumed grant strategy memory refs、writeback proposal、MAG accept/reject decision、operator receipt projection 和 repo-source layout audit 收成一个可验证 proof surface。
- 理由：OPL family memory index 已能解析 MAG domain memory descriptor，但 MAG 仍需要 repo-source 级证据说明 controlled grant-stage memory apply 只路由 refs 与 receipt projection，不写真实 memory body、grant artifact、fundability verdict、authoring quality verdict 或 submission-ready export verdict。
- 影响：`contracts/runtime-program/opl-family-contract-adoption.json`、`current-program.json`、manifest schema、sidecar export 与核心文档共同指向该 proof；真实 accepted/rejected receipt instance 仍只允许由 workspace/runtime artifact root 产生。默认 Hermes/Gateway/local-manager active path 继续退役为 explicit proof/provenance/history。

## 2026-05-11：MAG 对齐 OPL 完整 stage-led runtime framework

- 决策：MAG 的 OPL 关系更新为 `OPL stage-led runtime framework -> MAG-owned descriptor/projection -> Med Auto Grant app skill / CLI / MedAutoGrantDomainEntry`。OPL 是可作为外部依赖使用的完整智能体运行框架，不再只写成薄 Runtime Manager；Agent executor 是 stage attempt 的最小执行单位，`Codex CLI` 是当前第一公民 executor，除非活跃合同显式选择其他 provider。
- 理由：OPL 当前定位已经上移为完整 agent runtime framework，负责 stage lifecycle、queue/wakeup、handoff、receipt、retry/dead-letter、operator projection、shared contracts/indexes 与 provider 编排。MAG 仍必须持有 grant stage pack、prompt/skill、fundability judgment、authoring quality gate、workspace truth 和 submission-ready export authority。
- 影响：旧 `OPL Runtime Manager`、Hermes-first、gateway 和 local host runtime 说法降为历史追溯或 provider-specific 实现记录；后续公开/核心文档默认使用 OPL stage-led framework 口径，并把 Temporal 写成 OPL-hosted production path 的必需 substrate。MAG 的 skill/direct CLI 路径继续是一等入口。

## 2026-05-12：MAG 采用 OPL 统一 Agent Executor Adapter 边界

- 决策：MAG 的 product-entry manifest、runtime registration 与 current-program 明确采用 OPL generic Agent Executor Adapter / registry 口径；默认 concrete executor owner 固定为 `codex_cli`，`hermes_agent` 与 `claude_code` 只能作为显式 opt-in backend。`execute-critique-pass --executor hermes_agent` 必须产生 OPL `AgentExecutionReceipt` 风格 proof。
- 理由：跨仓统一后，generic executor adapter 归 OPL；MAG 不应把自己写成 generic executor owner。MAG 只持有 grant route truth、quality/fundability gate、workspace/artifact truth 与 export authority。
- 影响：非默认 executor 只承诺可接入、可回执、可审计、fail-closed，不承诺效果等价；product-entry `executor_owner` 表示默认 concrete executor，OPL adapter owner 通过独立 `executor_defaults` / `executor_adapter_contract` surface 表达。
- 当前状态：除真实 production-hosted grant-stage soak 外，本决策已落地到 manifest/runtime registration/current-program/sidecar/receipt proof 边界；旧 Hermes/Gateway/local-manager active path 已降为 explicit proof/provenance/history，默认 caller 仍是 Codex CLI。

## 2026-05-10：MAG 对齐 OPL Temporal-backed production runtime，Temporal 为 OPL 生产必需 substrate

- 状态：已被 `2026-05-11` OPL 完整 stage-led runtime framework 口径吸收，并被 OPL 的 Temporal-required production substrate 口径校准。保留本段用于解释 provider-backed / Temporal 迁移背景。

- 决策：MAG 的 OPL 长期托管口径更新为 `OPL Product Entry -> OPL stage-led family runtime provider -> MAG product sidecar export/dispatch -> MAG domain entry/projection`。Temporal 是 OPL production online runtime 的必需 substrate；Hermes-Agent 作为可选 Agent executor adapter、显式 hosted/proof backend 或 executor proof lane。
- 理由：MAG 需要长期 authoring stage attempt、human gate、retry/dead-letter、TODO wakeup 和 operator projection，但 grant truth、fundability judgment、authoring quality gate、workspace truth 和 submission-ready export authority 必须仍由 MAG 持有。
- 影响：`product sidecar export|dispatch` 继续是 OPL provider 到 MAG owner surface 的受控桥接。OPL/Temporal/Hermes/local provider 只能 enqueue、dispatch、signal、query、投影 attempt/receipt，不得写 grant truth、fundability verdict、authoring quality gate、workspace canonical document 或 submission-ready export gate。下方 Hermes-first sidecar adapter 决策保留为迁移背景，后续新投入按 Temporal-backed production runtime 解释。

## 2026-05-10：声明 MAG 的 OPL family Stage Control Plane projection

- 决策：在 `contracts/runtime-program/opl-family-contract-adoption.json` 中新增 `stage_control_projection`，把 OPL family stage pack 映射回 MAG 已有 `input_intake`、`direction_screening`、`question_refinement`、`argument_building`、`fit_alignment`、`outline`、`drafting`、`critique`、`revision`、`freeze/frozen` 与 `package submission-ready` surface。
- 理由：OPL family Stage Control Plane 需要统一 stage descriptor，MAG 也需要保持自己的 author-side grant truth、fundability judgment、route truth 与 submission-ready export gate。用 descriptor/projection 可以让 OPL 读取 stage pack，而不复制或改写 MAG grant route truth。
- 影响：`OPL` 只消费 stage descriptor/projection；MAG 继续持有 funding-call intake、fundability strategy、specific aims/structure、proposal authoring、review/rebuttal 与 local submission-ready export 的 authority。该变更不重写 autonomy controller、grant route truth 或 submission-ready gate。

## 2026-05-10：MAG 作为 OPL stage-led framework 上的独立 domain agent

- 决策：MAG 的 OPL 对齐口径固定为：MAG 是可被 Codex App skill 直接调用、也可由 OPL stage-led family framework 托管的独立 medical grant domain agent。OPL 只持有 stage descriptor discovery、queue、wakeup、handoff、receipt、approval/retry-dead-letter、trace/projection 和 parity；MAG 持有 grant stage pack、prompt/skill、route truth、fundability / authoring quality gates、workspace truth 和 submission-ready export authority。
- 理由：基金申请质量依赖 funder/call 语境、申请人基础、科学问题、specific aims、评审风险和正文质量闭环。OPL framework 可以提供可靠运行支撑，但不能替代 MAG 做 fundability judgement、authoring route 或 export readiness。
- 影响：后续流程优化优先改 MAG stage pack、prompt、quality scorecard、autonomy controller 和 export gate；不得把 grant route 逻辑搬到 OPL 机械脚本。direct skill path 保持一等入口。

## 2026-05-10：落地 Hermes-first OPL Family Runtime 的 MAG product sidecar adapter

- 状态：已被同日 Temporal-backed production runtime 决策 supersede。保留本段用于解释 Hermes-first sidecar adapter 的迁移背景和当前 legacy provider 口径。

- 决策：新增 `product sidecar export` 与 `product sidecar dispatch`，把 MAG 的 `runtime_control`、`runtime_continuity`、TODO/explicit wakeup、autonomy-controller 与 user-loop attention queue 投影成 OPL typed family queue 可消费的 sidecar surface。
- 理由：迁移期 Hermes-first family runtime 需要 24h 在线 substrate 与 typed queue/control-plane，但 MAG 仍必须持有 grant truth、quality gate 与 artifact/export owner。sidecar adapter 让 OPL provider 消费结构化 runtime/wakeup/control projection，同时不复制或改写 grant truth。
- 影响：dispatch 只允许 `status/read`、`user-loop/wakeup`、`autonomy-controller/dry-run`、`autonomy-controller/guarded-run`、`notification/receipt` 这组 MAG-owned guarded actions；`hermes_agent` proof executor 仍是显式 opt-in，不成为默认 authoring executor。

## 2026-04-26：MAG 对齐 OPL Runtime Manager 薄管理层

- 状态：已被 `2026-05-11` OPL 完整 stage-led runtime framework 口径 supersede。保留本段用于追溯薄管理层阶段。

- 决策：MAG 与 OPL 的长期托管对齐曾采用 `OPL Product Entry -> OPL Runtime Manager -> configured family runtime provider -> MAG product-entry/runtime-control projection -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`；该薄管理层 route 已被当前 `OPL Product Entry -> OPL stage-led family runtime provider -> MAG product sidecar export/dispatch -> MAG domain entry/projection` 口径 supersede。外部 `Hermes-Agent` 只作为显式 hosted/proof carrier 或 legacy provider 接入。MAG 只提供 domain entry contract、runtime_control、runtime_continuity、workspace projection、artifact locator 与 explicit wakeup/TODO queue；旧 `OPL Runtime Manager` 只作为历史薄管理层名词保留。
- 理由：MAG 的核心价值在 author-side grant truth、route/export contract、quality gate 和 submission-ready export gate。把长期在线管理先放在 OPL Runtime Manager 这一薄层，可以保持默认 `Codex CLI` / `codex_cli` runtime owner 清晰，并为显式 hosted/proof carrier 与未来自有 sidecar 预留 promotion 边界，同时不制造第二套 grant truth。
- 影响：`current-program.json` 增加 runtime manager boundary；后续 docs/contracts 若提到 OPL 长期托管，必须明确 Runtime Manager 不是 MAG 的 scheduler kernel、session store、memory store、grant truth owner、authoring executor 或 private Hermes fork。

## 2026-04-24：公开主语收口为单一 app skill 与内部 command contract

- 决策：公开文案与技术索引的第一主语收口为单一 `Med Auto Grant` app skill；`CLI` / `MedAutoGrantDomainEntry` 保持底层 agent entry，而 `product entry/product status/direct-entry/user-loop` 统一降级为这个 app skill 下的内部 command contract / direct-product projection。
- 理由：此前的公开叙事把 product status、user-loop、runtime_control 和 hosted bundle 写得过于靠前，容易让读者把内部投影面误判成产品第一入口，也会削弱单一 app skill 的对外定位。
- 影响：README、docs 索引、项目/状态/架构/合同说明与 app skill 文档需要同步保持这一层级；`hosted-contract-bundle` 与 `runtime_control` 仅保留 integration/reference 角色，不再暗示 OPL 或 hosted caller 是默认主入口。

## 2026-04-23：默认公开能力面收口为稳定 capability surface

- 决策：当前对外默认合同优先冻结为 `CLI`、`MedAutoGrantDomainEntry`、本地脚本、product-entry/projection commands 与 schema-backed contract；默认正文执行与默认 runtime owner 继续继承本机 `Codex CLI` / `codex_cli` 配置。
- 理由：如果继续把 hosted runtime carrier 写成默认公开主语，就会把真正稳定、可调用、可被 `Codex` / `OPL` skill activation 复用的能力面淹没掉。
- 影响：`Hermes-Agent` 相关 lane 继续保留为显式 hosted/proof backend 或技术参考；默认公开口径回到稳定 capability surface，避免把 backend 位置误写成产品第一身份。

## 2026-04-23：完成语义收口到 authoring quality 主线（P4.G）

- 决策：当前 tranche 收口为 `P4.G authoring-quality-first completion semantics alignment`，主任务完成语义以正文科学性与 authoring quality 为主。
- 理由：如果把 `submission-ready` 本地导出能力写成主任务唯一完成条件，容易把“交付包可导出”误写成“正文科学论证已闭环”。
- 影响：`package submission-ready` 继续保留为更严格的本地提交包导出面，但不作为 authoring 主任务唯一完成判据；`current-program`、`mainline-status`、`status` 与 current-truth spec 统一对齐此口径。

## 2026-04-23：形式审查/客观补件采用 TODO + 显式唤醒链路

- 决策：形式审查项与客观补件项默认进入 `TODO` 与显式唤醒链路，不默认阻塞正文 authoring。
- 理由：多数形式补件属于可排程闭环事项，默认 hard-block 会打断正文主线推进并降低主任务收敛效率。
- 影响：只有当缺口直接破坏科学论证成立性时，才升级为正文 authoring blocker；其余场景保持可追踪待办与显式恢复点。

## 2026-04-23：锁定 funder 任务线禁止 opportunistic 跨 funder 切换叙事

- 决策：已锁定 funder/family 的任务线保持同一 funder 语义闭环推进，不写成 opportunistic 跨 funder 切换。
- 理由：跨 funder opportunistic 切换会破坏已锁定材料、评审语境与质量治理闭环的一致性。
- 影响：current-truth 文案与 projection 输出默认保持 locked-funder continuity；跨 funder 变更必须作为显式重规划事件处理。

## 2026-04-21：公开主语收口为独立 medical grant domain agent

- 决策：公开文案与 machine-readable 描述统一收口为 `Med Auto Grant` 是独立 medical grant domain agent，可被 `Codex` / `OPL` / 其他通用 agent 直接调用；`OPL` 只保留 family-level session/runtime/projection 与 shared modules/contracts/indexes。
- 理由：此前公开叙述里仍混入了“位于 OPL 内部 workspace”或把 `gateway / harness` 作为第一身份的表达，容易让 caller 误判 MAG 的独立边界与 direct-entry 能力。
- 影响：`CLI` / `MedAutoGrantDomainEntry` 继续固定为 agent entry；`product entry/product status/direct-entry/user-loop` 继续固定为 lightweight direct entry / projection；旧 `gateway / harness` wording 只作为历史迁移语境保留，当前架构术语回到 single app skill、CLI/domain-entry 与 OPL stage-led framework。

## 2026-04-17：冻结托管运行时三层 owner contract

- 决策：把当前主线统一明确成三层 owner：默认 runtime owner 是 `Codex CLI` / `codex_cli`，显式 hosted/proof carrier 可以由外部 `Hermes-Agent` 或 OPL provider 承担，`Med Auto Grant` 只持有 grant-domain governance / progress / review / package gate truth，而 route-selected executor 只持有具体 authoring execution。
- 理由：如果只写成“上游 runtime substrate + repo-side domain logic”，仍然容易把 domain supervision、默认 runtime owner 和具体 executor 混成一层，后续跨仓对齐时也会反复漂移。
- 影响：文档、spec 与入口 wording 都必须显式区分 runtime owner、domain owner 与 executor owner；这轮只冻结 contract / 文档 / 入口同构，不宣称跨仓共享代码模块已抽离完成。

## 2026-04-13：把本地 submission-ready 交付导出收口成正式 command surface

- 决策：新增 `build-submission-ready-package`，把 `artifact_bundle -> final_package -> hosted_contract_bundle` 这条导出链再向前收口成一个正式的本地交付命令，并新增 `submission-ready-package.schema.json` 作为独立的 repo-tracked contract。
- 理由：从用户视角看，“能不能把当前冻结且材料齐备的国自然标书一次性导出成可交付目录”已经不该再靠人工拼三四个命令；同时这一步又必须 fail-closed，不能对缺章节、缺证据或有 gaps 的 frozen workspace 勉强导出。
- 影响：`build-submission-ready-package` 现在已经进入 CLI / domain entry / hosted bundle / product product entry command catalog；`current-program`、`mainline-status`、核心骨架、README、`contracts/README` 与测试都要同步进入 `P4.F` 口径，并明确“本地 package 导出”不等于“外部官网提交已完成”。

## 2026-04-13：把 `product-entry-manifest` 与 `product-status` 升级为独立 schema-backed contract

- 决策：把 `product-entry-manifest` 与 `product-status` 从“复用 product-entry shell 的 controller surface”进一步收口成独立 schema-backed、generation-time fail-closed 的 direct product entry contract，并把它们显式登记进 `schema-index.json`。
- 理由：当前 direct grant product entry 已经不只是几段人话描述，而是 future caller / `OPL` 需要直接消费的 machine-readable product entry contract；如果没有独立 schema，manifest/product status 的 shape、companion 字段与 quickstart 结构仍可能在不知不觉中漂移。
- 影响：`product_entry.py` 现在会在生成 `product-entry-manifest` / `product-status` 后直接做 fail-closed schema 校验；`schemas/v1/product-entry-manifest.schema.json` 与 `schemas/v1/product-status.schema.json` 成为新的 repo-tracked truth surface；`current-program`、`mainline-status`、核心骨架、README 与测试都要同步进入 `P4.E` 口径。

## 2026-04-13：`family_orchestration` 的 route status 统一回到共享 author-side route truth

- 决策：`grant-progress`、`product-entry-manifest` 与 `product-status` 上的 `family_orchestration` companion，不再使用本地过期的 landed-route 集合判断 human gate 状态，而是统一读取共享 author-side route contract。
- 理由：`direction_screening -> frozen` 已经在 `P4.D` 收口为 landed route catalog；如果 product entry companion 还继续看旧集合，就会把诸如 `question_refinement` 这类已 landed route 错标成 `pending/requested`，制造第二真相。
- 影响：当前 product entry / projection / user loop 看到的是同一份 route status；后续继续向 family action graph / human gate / manifest v2 深压时，必须保持这种“共享 route truth 单源读取”的做法。

## 2026-04-13：full authoring executor 升级为全链 landed route catalog

- 决策：把 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / frozen` 从历史上的 `pending / handoff-required` 一次性提升为 landed 的 service-safe command surface，并与 `critique / revision / artifact_bundle / final_package / hosted_contract_bundle` 收敛成完整 author-side route catalog。
- 理由：人工整理的国自然写作流程已经能稳定映射到现有 stage 梯子，而实现层、CLI、domain entry、product loop 与 hosted bundle 也都已经具备同一套 route truth；继续把前半程写成 pending，只会制造第二真相。
- 影响：`current-program`、`mainline-status`、`status/project/architecture/current-truth specs`、`grant-user-loop`、`domain_entry_contract`、hosted bundle route catalog 与 tests 全部改写为 full landed truth；`product-status.schema.json` 退为历史兼容与追溯材料，并退出 schema index 与当前 contract surface。

## 2026-04-13：critique route 升级为 Codex CLI landed route

- 决策：把 `critique` route 从历史上的 `pending / handoff-required` 正式提升为已 landed 的 `execute-critique-pass` route。
- 理由：实现层 (`domain_runtime.py` / `critique_executor.py` / `codex_cli.py`) 与现有 route tests 已经稳定落在 landed 口径；继续把它写成 pending 会制造第二真相。
- 影响：`current-program`、status/architecture/current-truth specs、hosted bundle route catalog 与 meta tests 全部改写为 `critique = landed`；而在同日的 full authoring landing 之后，当前 landed author-side route 已进一步扩展成 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle`。

## 2026-04-13：critique 的 Codex CLI executor 继承本机 Codex 默认

- 决策：`execute-critique-pass` 的默认模型与默认 reasoning effort 统一收口到 `inherit_local_codex_default`，不在 repo 内固定 `gpt-5.4 / xhigh`。
- 理由：当前真实入口是 `read_codex_cli_contract()` + `run_codex_exec(...)`；未显式配置环境变量覆盖时，本就应该跟随本机 Codex 默认配置，避免四仓未来一起追着改 model pin。
- 影响：文档、current-program 与 current-truth 必须显式写出 `default_model / default_reasoning_effort = inherit_local_codex_default`；只有设置 `MED_AUTOGRANT_CODEX_MODEL` / `MED_AUTOGRANT_CODEX_REASONING_EFFORT` 时才会覆盖。

## 2026-04-13：Hermes-native 只指完整 agent loop

- 决策：文档层统一声明，只有带 session substrate、route orchestration、domain mutation 与 durable state transition 的 full agent loop 才算 `Hermes-native`。
- 理由：如果把 chat relay / 单次 chat completion 也写成 `Hermes-native`，就会把 substrate owner 与单步 executor 混写，误导后续跨仓收敛。
- 影响：当前 `critique` landed 只能写成 `Codex CLI` landed route，默认模式是 `autonomous`，不能写成 `Hermes-native landed`；后续若切到 Hermes executor，必须额外拿 full-loop truth 与 proof。

## 2026-04-13：先在 critique route 落一条 Hermes-Agent experimental proof lane

- 决策：不新增第二条 critique command，也不改默认执行器；而是在现有 `execute-critique-pass` 上增加显式 `executor_kind=hermes_agent` 的 experimental proof lane。
- 理由：这样既能保持 service-safe command surface、route catalog 与 hosted contract 不漂移，也能在同一条 route 上真实验证 `Hermes-native` 是否具备 full agent loop 能力，而不是继续停留在纯文档讨论。
- 影响：当前 `execute-critique-pass` 默认仍是 `Codex CLI`，默认模式是 `autonomous`；只有显式 opt-in 时才会走 `run_agent.AIAgent.run_conversation(...)`，并且必须以“读取本机 Hermes config + 真实工具事件 + 完整 loop + 合法 JSON”四重 fail-closed 门槛来证明自己。

## 2026-04-13：Hermes-Agent proof 必须显式读取本机 Hermes 默认配置

- 决策：`hermes_agent` proof lane 不在 repo 内硬编码 `gpt-5.4 / xhigh`，而是显式读取 `~/.hermes/config.yaml` 里的 `model.default / provider / base_url / api_mode / agent.reasoning_effort`；只有设置 `MED_AUTOGRANT_HERMES_*` 环境变量时才覆盖。
- 理由：当前真实环境里，直接裸实例化 `AIAgent()` 并不会稳定自动补齐 `model.default`，provider 会直接报 `model is required`。如果不显式读取本机 Hermes config，这条 proof lane 根本不成立。
- 影响：repo-tracked truth 必须诚实写明“这条 lane 继承本机 Hermes 默认，而不是 repo-local pin”；同时若运行环境仍是 `custom + chat_completions`，当前只能证明 full-loop 存在，不能把 provider 侧 reasoning 语义直接写成已证明。

## 2026-04-11：统一文档骨架

- 采用核心五件套：`project/architecture/invariants/decisions/status`。
- `docs/README*` 以核心骨架为首读入口，其次是 active specs、active plans、references 与 history 索引。

## 2026-04-11：AGENTS 仅保留工作方式

- `AGENTS.md` 不再承载项目事实与阶段判断，统一回收至核心骨架与 specs。

## 2026-04-11：OMX 仅保留历史入口

- OMX 相关内容只作为历史入口保留在 `docs/history/omx/**`，不再作为活跃执行入口。

## 2026-04-11：移除 OMX-era 外部验证入口

- `omx-project-installer` 相关的外部 verifier 不再出现在 repo-tracked current truth 的验证表述中。
- 如需追溯历史来源，仅在历史说明或本文件记录，不再作为当前验证或 hard gate 入口。

## 2026-04-11：统一最小验证入口

- `scripts/verify.sh` 作为默认最小验证入口，保持分层 lane 与 `Makefile` 一致。

## 2026-04-11：冻结历史本地 runtime closeout 边界

- 在当前 repo-tracked truth 下，`R1 -> R5.A` 本地 runtime ladder 与 post-`R5.A` fail-closed hardening 已达到当前可验证上限。
- 当天 closeout 材料固定了一组历史本地 runtime closeout label 与 baseline，用于归档追溯。
- 继续推进时必须先新增并冻结 tranche truth；不得把未冻结的 hosted/runtime/submission-grade reality 写成当前已有主线。

## 2026-04-11：目标 substrate 优先于旧本地 runtime 延长线

- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态，而不是继续把旧本地 runtime 深磨成长期产品终态。
- 当前本地 runtime 只保留在归档追溯材料里；任何新 tranche 都必须显式说明是在延续旧基线，还是在服务新的目标形态。

## 2026-04-11：`Hermes-Agent` 只指上游外部 runtime substrate

- 状态：已被 2026-05-11 OPL stage-led framework 口径与 2026-05-12 OPL 统一 Agent Executor Adapter 口径 supersede。当前 `hermes_agent` 只表示显式非默认 executor/proof/provenance lane，不是 MAG 当前 runtime substrate target、compatibility bridge 或 default provider owner。
- 后续凡是提到 `Hermes-Agent`，只能指上游外部 runtime 项目 / 服务本体。
- 仓内 `domain_runtime.py` 只代表 repo-local migration scaffold，不得写成“已接入 Hermes-Agent”。

## 2026-04-12：runtime substrate 与 grant executor 明确分层

- 状态：已被 2026-05-12 OPL 统一 Agent Executor Adapter 口径 supersede；保留本段用于解释早期 Hermes proof 语境。
- 决策：`Hermes-Agent` 只作为显式 OPL receipt/proof lane 或历史 provenance 读取；默认 concrete executor 固定为 `Codex CLI`，MAG 继续持有 grant route truth、quality/fundability gate、workspace/artifact truth 与 export authority。
- 理由：当前需要证明的是非默认 executor 可接入、可回执、可审计、fail-closed，而不是把 runtime substrate owner 或 authoring semantics 交给 MAG repo-local Hermes 路径。
- 影响：repo-side domain logic、artifact assembly、identity guard 与 executor routing 继续保留为 domain owner；未来若要替换单步执行器，必须以新的 route truth 和 OPL receipt proof 单独推进。

## 2026-04-12：冻结 author-side executor routing contract

- 决策：`stage_action_envelope` 与 `build-product-entry` 必须共享同一份 `executor_routing_contract`，明确当前 stage、下一步 executor route，以及已 landed 的 author-side route catalog。
- 理由：如果只写“substrate 已统一”，却不把 critique / revision / export 的 route status 显式冻结下来，后续最容易把 `pending` route 误写成“已 landed executor”。
- 影响：这条 contract 仍是 route truth 的锚点；其中关于“前半程 pending、`critique = landed`”的 `2026-04-12` 快照，已经被 `2026-04-13` 的 full authoring executor landed 决策 supersede。未来继续替换任何 route，都必须先改对应 contract truth。

## 2026-04-12：为 critique pending route 冻结直接协作 handoff contract

- 决策：在保持 `critique` 继续为 `pending / handoff-required` 的前提下，为它补一份 machine-readable `handoff_requirements`，明确 future Hermes-side collaborator 必须先读取哪些 domain surfaces。
- 理由：如果 pending route 只有一个状态字段，future host 很容易绕开 grant domain truth，或者误以为需要仓内新增本地 critique helper。把 handoff 要求显式冻结出来，能让“直接协作”与“新 executor 已 landed”保持清楚分层。
- 影响：这份 pending handoff contract 现已退为历史 superseded note；`2026-04-13` 之后的 current truth 已改成 `critique -> execute-critique-pass` landed。旧 contract 只保留作历史迁移说明。

## 2026-04-12：冻结全 pending authoring route handoff matrix

- 决策：不再只为 `critique` 单独定义 pending handoff，而是把 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / frozen` 全部冻结成 route-specific `handoff_requirements`。
- 理由：最终目标是让 `Hermes` 负责 substrate、让 `OPL` / domain 通过统一 envelope 直接协作，而不是继续脑补新的 repo-local executor。没有完整 matrix，future caller 仍会在其他未 landed route 上重新发明 handoff semantics。
- 影响：这份 pending matrix 在 `2026-04-12` 为 future caller 提供了完整 handoff 语义；但到 `2026-04-13` full authoring executor landing 后，整份 matrix 已退为历史迁移说明，当前主线不再存在 remaining pending authoring route。

## 2026-04-12：冻结 schema-backed product entry / routing contract

- 决策：把已 landed 的 `service-safe domain surface`、`executor_routing_contract` 与 `product_entry` 从“文档冻结 + 运行时 dict”进一步收口成 schema-backed contract，并在 `build-product-entry` / hosted bundle 生成时 fail-closed。
- 理由：future OPL / domain caller 最终消费的是 machine-readable contract，而不是 repo 内部约定。如果这些 surface 只有 current truth 没有 schema，后续最容易在 pending route、route catalog、draft-bearing/nullability 边界上悄悄漂移。
- 影响：`schemas/v1/schema-index.json` 现在会显式索引当前主线正在公开承诺的 contract schema；`product_entry` 与 `executor_routing_contract` 必须同时满足 schema 校验和冻结 truth 比对；后续任何 contract 变更都必须同步更新 schema、tests、docs 与 current-program pointer。

## 2026-04-12：冻结 hosted contract bundle entry and route catalog

- 决策：`build-hosted-contract-bundle` 不再只导出 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract`，还要显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并受 `hosted-contract-bundle.schema.json` 的 fail-closed 约束。
- 理由：future hosted caller / `OPL` caller 真正要消费的不只是 runtime/state/operator pointer，还需要稳定的 service-safe entry、schema registry 与 author-side route catalog；如果这些合同不随 bundle 一起冻结，后续就会在 bundle 外重新发明 handoff semantics。
- 影响：hosted bundle 现在只打包已经冻结好的 domain entry / schema / route truth，不新增 repo-local executor，也不把 hosted runtime、`OPL Gateway` 或 pending route 写成已落地。

## 2026-04-12：冻结 OPL 对齐的理想目标与阶段图

- 状态：已被 2026-05-11/2026-05-12 的 OPL stage-led framework 与统一 Agent Executor Adapter 口径 supersede。
- 决策：把 `Med Auto Grant` 的长线理想目标固定为 `OPL` stage-led framework、默认 `Codex CLI` concrete executor、显式 optional executor adapter/proof lane、`Med Auto Grant` domain truth owner 的分层结构，并把主线阶段固定成 `P1 completed / P2 completed / P3 completed / P4 next`。
- 理由：如果不把 “理想目标” 和 “当前完成态” 分开冻结，后续最容易一边拿 `OPL` 理想型讲话，一边把未完成的 hosted caller / direct product entry 写成 landed。
- 影响：`current-program` 现在额外携带 `ideal_target` 与 `phase_map`；当前 `P3 hosted caller / OPL consumption proof` 已通过冻结合同与 proof test 落地，后续推进默认转向 `P4 mature direct grant product entry`，而不是回头重写 repo-local helper 或跳到 product overclaim。

## 2026-04-12：冻结 hosted caller contract consumption proof

- 决策：external caller / future `OPL` caller 必须直接消费仓库已经冻结好的 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并且只通过 `supported_commands` 与 `command_contracts` 构造 request；不新增 repo-local hosted helper。
- 理由：如果 external caller 还要回头读仓内 helper 或手写参数拼装逻辑，那么 `P3` 其实并没有完成，合同也还不算真正 machine-readable。
- 影响：`product_entry.return_surface_contract.domain_entry_contract` 与 hosted bundle 的 `domain_entry_contract` 现在共享同一份 command catalog；`P3` 可以诚实标成 completed，而 `P4` 成为下一个 honest phase。

## 2026-04-12：`P4.A` 只落 controller-owned / read-only direct product projection

- 决策：`grant-progress` 与 `grant-cockpit` 当前只作为 controller-owned、read-only 的 direct grant product projection 落地，不进入 `domain_entry_contract.supported_commands`，也不被写成新的 service-safe executor surface。
- 理由：`P4` 的第一棒需要先给 direct user / operator / future caller 一个稳定的人话 projection，但如果把这两条 surface 混进 domain entry command catalog，就会再次把 product projection、domain execution 与 hosted caller contract 语义搅在一起。
- 影响：当前 direct-product projection 只允许读取 `summarize-workspace`、`stage-route-report`、`critique-summary` 与 `build-product-entry` 的既有合同信息；它们不改写 route owner，不新增 repo-local hosted helper，也不等于成熟前台 / hosted runtime。

## 2026-04-12：冻结 `P4.A` direct product projection contract

- 决策：`grant-progress` 与 `grant-cockpit` 不只停留在 CLI projection，而是进一步通过 `grant-progress.schema.json` 与 `grant-cockpit.schema.json` 冻结成 schema-backed、generation-time fail-closed 的 projection contract。
- 理由：如果 `P4.A` 只有命令和 current truth，没有独立 schema，那么 direct product projection 的 shape、blocker 语义、command catalog 展示面和 nullability 边界都可能悄悄漂移；而这两条 surface 又必须和 service-safe domain command catalog 保持严格分层。
- 影响：`read_grant_progress(...)` 与 `read_grant_cockpit(...)` 现在都会在返回前执行 schema 校验；这两条 projection 继续不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-12：冻结 `P4.B` direct entry composition contract

- 决策：在 `P4.A` 的基础上新增 `grant-direct-entry`，把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 组合成一份 schema-backed、generation-time fail-closed 的 direct-entry contract。
- 理由：理想形态中的 `Med Auto Grant Product Entry` 不能永远停在“只读投影 + 单独 build shell”两个分散 surface 上；但当前又不能发明新的 executor 或 handoff semantics。最诚实的推进方式，就是把已冻结 surface 组合成一份 direct-entry contract。
- 影响：`grant-direct-entry` 继续只复用既有 route truth、grant truth 与 `product_entry` envelope，不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-12：冻结 `P4.C` mainline status 与 grant user loop

- 决策：在 `P4.B` 的基础上新增 `mainline-status`、`mainline-phase` 与 `grant-user-loop`，把 repo 主线快照、当前 `grant-direct-entry` 组合面，以及 route-derived next action 收成当前 controller-owned 的 user loop。
- 理由：如果用户仍要自己翻 `current-program`、phase-map docs 和 route contract 才知道“现在在哪个阶段、下一步该执行什么”，那么 `P4` 仍停留在分散 surface；但当前又不能越界把它写成成熟 Web UI、hosted runtime 或新的 executor。
- 影响：`grant-user-loop` 现在通过 `grant-user-loop.schema.json` 受 generation-time fail-closed 校验；`mainline-status / mainline-phase / grant-user-loop` 继续只投影已冻结 truth，不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-11：当前主线回到“本地 runtime 诚实 + 上游 Hermes-Agent 目标”

- 状态：已被 2026-05-11 OPL stage-led framework + 2026-05-12 executor adapter boundary supersede。保留本段仅为解释当时从 Hermes 命名误读回到 repo-local truth 的校准过程；不得把“上游 Hermes-Agent 目标”恢复为 current mainline。
- 当时可执行 runtime owner 仍是 repo-local code；当前已被 OPL generated/hosted session refs 与 MAG domain authority refs 替代。
- 旧 `CLI-first + host-agent runtime` 线只保留为归档参考材料。
- `domain_runtime.py` 路径当前只保留 grant-native domain handler / authoring-export authority，不再承担本地 runtime substrate。
- `CLI / MCP / controller / upstream Hermes-Agent target / MedAutoGrant domain logic` 的边界必须显式保留，不得偷换 formal entry 或 authoring semantics。

## 2026-04-11：旧 Hermes 命名材料降级为历史本地迁移工件

- 当时 `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report / runtime-run / runtime-resume` 仍运行在 repo-local runtime path 上；当前 `runtime-run / runtime-resume` 已退役，其他命令保留为 grant-native domain surfaces。
- 旧的 Hermes 命名 program/spec 文档继续保留为历史迁移材料，但不再作为“上游 Hermes-Agent 已落地”的 current truth。

## 2026-04-11：final package / hosted contract 继续保持本地 owner，等待真实上游集成

- `execute-revision-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle` 当前仍由 repo-local helper 持有输入加载、identity guard 与输出 handoff。
- `revision_executor.py`、`artifact_bundle.py`、`final_package.py` 继续保留 domain document assembly 责任，不被误写成上游 substrate 已接管。
- 如果未来这些责任要迁到上游 `Hermes-Agent`，必须以新的 repo-tracked truth 重新冻结。
