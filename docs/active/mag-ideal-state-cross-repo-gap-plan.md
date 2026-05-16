# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `ideal_state_gap_plan`
State: `active_plan`
Machine boundary: 本文是人读 gap / completion plan，不是机器真相。机器可读真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、OPL runtime ledger、domain-owned manifest、workspace/runtime artifact root、receipt、质量报告和导出包；MAG repo closure / current status 投影以 `current-program.json`、product-entry manifest 和真实 runtime receipt 为准。
Date: `2026-05-16`
Cleanup posture: 当前计划不再要求保留旧模块、旧接口、旧测试或 compatibility shell。已经被核心文档、合同面、源码或测试替代的旧面，后续按最新 owner surface 直接删除、归档到 history/tombstone，或从测试入口移除；不新增兼容 alias、facade patch bridge 或旧 CLI shell 调用。

## 文档读法

本文是 MAG 的长期 gap plan，不是一次性 repo closeout 记录。已经落地的 receipt writer、sidecar guarded action、descriptor、skeleton descriptor 和 direct-retirement posture 只作为当前基础面阅读；后续维护重点是把这些基础面持续用于真实 grant workspace、OPL-hosted attempt、memory writeback、package/export lifecycle 和 legacy delete audit。

MAG 仓内不再新增兼容层或第二真相源。新增能力必须先归类为三类之一：

- `MAG-owned domain package`：grant truth、fundability / quality / export verdict、stage pack、domain transition spec/table、memory accept/reject、artifact/package authority、descriptor、contract/schema、sidecar/thin adapter、projection builder、artifact locator、receipt schema、tests 和 domain entry。
- `OPL-owned generic framework/runtime`：scheduler、queue、attempt ledger、generic state-machine runner、workspace/source intake shell、memory locator/index、artifact/package lifecycle shell、workbench、observability、SLO、App routing 和 cross-domain projection。
- `OPL-generated surface`：CLI/product-entry/sidecar/status/read-model/workbench/harness wrapper，输入来自 MAG descriptor、stage graph、action metadata、receipt schema、policy table 和 authority function manifest；MAG 手写同类 surface 只能作为迁移桥。

若旧模块、旧接口、旧测试或旧 CLI alias 已被最新 owner surface 替代，处理方式是 direct retirement：改 active caller 到最新 surface 后直接删除或归档到 history/tombstone；不保留 compatibility alias、facade patch bridge、monkeypatch test 或旧 runtime owner wording。

- `定位`：本文是 MAG 的 active gap / implementation order，不是 north-star 目标态本身；目标态回到 `med-auto-grant-ideal-state.md`。
- `当前实态`：MAG 没有发现类似 MAS local LaunchAgent scheduler 的默认运行 owner 残留；MAG 作为 OPL standard scaffold / generic primitives consumer 的功能面 follow-through 已落到 manifest、sidecar projection、schema 和 focused guard。2026-05-17 后目标收紧为 OPL pack compiler / generated surface：MAG repo-local refs-only surface 已覆盖 focused hosted receipt verification、memory receipt read projection、package lifecycle handoff projection、cleanup/restore/retention lifecycle receipt bundle 和 continuous receipt reconciliation snapshot，但这些手写 shell 长期应被 OPL 生成或托管。当前剩余缺口是外部 OPL generated/replacement production consumption、真实 workspace memory/package/lifecycle receipt 泛化、持续 live receipt 对账和 long-run soak。
- `最短路径`：MAG consumer follow-through 已完成；后续先用真实 workspace/runtime evidence 验证 memory/package/lifecycle refs 被 OPL/App shell 消费，再做持续 live receipt reconciliation，最后做 long-run live soak。
- `验收顺序`：focused OPL-hosted receipt verification 在 MAG consumer 功能面收口之后执行；long-run live soak 是最后的 production closure，不是 MAG 侧 contract/manifest/sidecar follow-through 的前置条件。
- `禁写口径`：不能把 descriptor resolved、receipt writer、receipt reconciliation inventory、OPL provider completion 或 no-regression evidence 写成 grant-stage production soak、fundability-ready、quality-ready 或 export-ready。

## 结论

MAG 的理想目标态已经很清晰：MAG 是医学基金申请 domain agent，持有 grant truth、fundability、specific aims、authoring quality、grant strategy memory body/accept-reject、submission-ready package 与 export authority；OPL Framework 提供长期在线、stage attempt、queue/wakeup、human gate、receipt、retry/dead-letter、operator projection、workspace/artifact lifecycle、shared contracts 和 provider-backed runtime。

OPL 系列项目的全局主参考是 `/Users/gaofeng/workspace/one-person-lab/docs/active/opl-family-development-reference.md`。本文只维护 MAG 自己的目标、差距、evidence ledger、grant authority 和 MAG-to-OPL 上收候选；OPL、MAS、RCA、MDS 或 OPL-owned App/workbench 的并行计划回到各自 owner surface。

当前 MAG 已完成 direct app skill / CLI / `MedAutoGrantDomainEntry` / product-entry / sidecar / 6-stage control plane / domain memory descriptor / owner receipt contract / lifecycle guarded apply / standard skeleton descriptor 等基础面。OPL family 当前也已经具备 descriptor-level aligned 的 standard domain-agent 读取模型、stage plane / memory descriptor 读取模型和 Temporal provider proof 基础。具体计数、provider 状态和 live-soak 结论必须以 OPL 当前机器面为准，不在本文固化。

2026-05-16/17 校准：MAG 的功能边界当前没有发现类似 MAS local LaunchAgent scheduler 的默认运行 owner 残留；MAG 主要保留 grant authoring domain entry、product-entry、sidecar、receipt reconciliation、memory/package/export/lifecycle proof surface 和 grant transition oracle。它仍不是“纯知识文件仓”，因为 descriptor、schema、receipt proof、tests、domain entry、fundability / quality / export verdict、package authority、memory accept/reject 和 owner receipt 都是 OPL 需要的 domain authority surface；sidecar、projection builder、product status 和 grouped CLI/API 属于迁移桥，长期应被 OPL generated surface 替代。真正需要上收的是 workspace/source intake shell、memory locator/writeback transport、package/export lifecycle shell、generic transition runner、operator workbench、observability/SLO、provider runtime 和 generated wrapper owner。

2026-05-16 consumer/thinning lane 完成口径：MAG 侧已把上述边界落成 `product-entry-manifest.mag_consumer_thinning_contract`，并由正确入口 `uv run python -m med_autogrant.cli product sidecar-export --input examples/nsfc_workspace_p2c_critique.json --format json` 投影。该合同固定 MAG adapter 只输出 grant-owned refs、owner receipt、typed blocker、verdict refs 和 domain action metadata，并声明消费 OPL `family_scheduler_replacement`、OPL standard scaffold 和 OPL generic primitives；workspace/source intake shell、memory locator/writeback transport、package/export lifecycle shell、generic transition runner、operator workbench/observability/SLO 和 agent scaffold checklist 都是 OPL replacement expectation。MAG 不持 generic scheduler、daemon、lifecycle owner、queue、attempt ledger、generic state-machine runner、generic workbench、generic memory transport 或 generic artifact lifecycle owner 角色，且 sidecar fresh output 明确 `claims_opl_replacement_exists=false`、`claims_production_long_run_soak_complete=false`。同一合同现在暴露 `consumed_opl_standard_surfaces`、`functional_harness_consumer_coverage`、`thin_surface_output_guard` 与 `standard_agent_scaffold_alignment`：`functional_harness_consumer_coverage` 明确 MAG 作为 OPL functional harness consumer 覆盖 memory refs-only writeback chain、queue/stage attempt/typed closeout、generic transition runner、restart/dead-letter/repair/human gate 状态链；`consumed_opl_standard_surfaces` 证明 MAG 是 OPL standard scaffold / generic primitives / functional harness 的消费方；后两者证明 sidecar 只能回传 grant refs / receipts / blocker / verdict refs / action metadata，并证明 MAG 保留必要 domain entry、schema、sidecar 和 focused tests，不退化为纯知识文件仓。该完成口径关闭 MAG 侧 P1-P4 功能面 follow-through；不声明 OPL functional harness 已通过，不把 harness pass 写成 grant-ready 或 export-ready，不关闭真实 workspace memory/package/lifecycle evidence、focused hosted receipt verification 或 live soak。

2026-05-16 OPL surface follow-up：OPL 后续新增 standard scaffold generator、family conflict envelope、stage-attempt usage/control-loop projection、runtime observability export 与 product-operator projection 后，MAG 可跟进的安全范围是继续收窄消费合同，而不是实现这些 OPL generic surface。`mag_consumer_thinning_contract` 现在把 package/export lifecycle expectation 归一到 OPL `artifact_package_lifecycle_shell`，把 operator/workbench 与 observability 拆成 `operator_workbench_drilldown_shell` 和 `observability_repair_projection`，并新增 `opl_family_conflict_blocker_projection` / `opl_runtime_observability_consumption`。这些字段只允许 OPL 读取 MAG refs、receipt、typed blocker、safe action refs 与 counts；禁止 MAG 写 OPL ledger、执行 OPL repair、把 provider completion 解释成 grant-ready、或把 conflict envelope 当成 fallback completion。

2026-05-16 consumer projection follow-up：MAG 现在补齐三组 OPL-led program 可直接消费的 helper。`build_opl_conflict_or_blocker_envelope` 给 OPL family conflict envelope 提供 MAG-owned refs-only payload；`build_controlled_soak_receipt_observability_summary` 把 MAG receipt reconciliation inventory 收成 runtime observability summary；`build_stage_attempt_observability_projection` 把 MAG controlled stage attempt 与 receipt inventory 收成 stage-attempt usage/control-loop projection。三者都挂在 `MedAutoGrantProductEntry` 薄方法下，便于 OPL 或 Codex direct caller 调用；它们不新增 CLI alias、不接入 sidecar generic action、不写 OPL ledger、不实现 retry/dead-letter/control-loop、不包含 memory body 或 grant artifact，也不声明 provider completion、grant readiness、quality readiness、export readiness 或 production soak。

2026-05-16 privatized functional module audit closeout：MAG 侧新增 `mag_consumer_thinning_contract.privatized_functional_module_audit`，并由 sidecar export 投影给 OPL 统一审计。该审计把 runtime registration、task lifecycle、session ledger / attention queue、lifecycle adapter、observability、sidecar/product status、package lifecycle、source intake、人用 workbench / scheduler / daemon 归为 OPL-owned generic primitive consumer；把 grant lifecycle stage、fundability / quality / export verdict、package readiness / submission-ready、grant transition oracle、owner receipt / no-regression evidence、grant strategy memory accept/reject 归为 MAG-owned grant truth / receipt / verdict；把默认 Hermes/Gateway/local-manager runtime owner、domain runtime patch bridge、compatibility aggregate test、legacy flat shell alias 和 repo-owned scheduler/daemon 归为 retire/tombstone。该 closeout 明确保护 grant `lifecycle_stage`、package readiness、submission-ready、fundability、quality、export verdict 与 owner receipt，防止它们被当作通用 lifecycle/readiness/package 面误删。

2026-05-16/17 private functional audit 落地校准：该审计面现在不只给分类，还对每个 audit item 暴露 `code_paths`、`active_callers`、`active_caller_status`、`migration_action`、`retention_reason` 与 `cannot_absorb_reason`。当前代码真实状态是：MAG 仍有本地 `runtime run/resume` journal / attempt ledger、`grant_autonomy_controller` / critique / mainline loop、workspace/source validation、memory receipt writer、package/export helpers、product status/user-loop/sidecar adapter、generic CLI grouped wrappers，以及 optional `hermes_agent` proof lane / upstream `hermes_state.SessionDB` 探测。它们不能被写成“已经全部清空”。迁移动作是把 session ledger、attention queue、stage attempt ledger、generic lifecycle adapter、workspace/source intake shell、artifact/package lifecycle shell、runtime observability、operator workbench、scheduler/daemon 和 generated wrapper owner 上收到 OPL generic primitives / pack compiler；MAG 只保留 grant lifecycle、fundability/quality/export verdict、package authority、memory accept/reject、owner receipt、grant transition oracle、schema/contract、focused tests 和真正无法声明化的 grant authority functions。不能上收的原因也已机器化：OPL 可以承接 transport、ledger、display、SLO、runner、lifecycle 壳和 generated entry surface，但不能解释 funding call、决定 grant readiness、签 owner receipt、写 memory body、批准 submission-ready export 或改写 MAG grant truth。

2026-05-16 thin output guard follow-through：`thin_surface_output_guard` 现在不只禁止 generic runtime / workbench / memory / artifact / observability state，也把 MAG 历史私有功能状态逐项列为 forbidden output class：local runtime journal、local attempt ledger、attention queue、stage attempt ledger、package lifecycle、source intake、operator workbench、scheduler daemon 和 Hermes state-db runtime state。该 guard 让 MAG 即使保留 domain thin adapter 或 explicit proof lane，也不能通过 sidecar / manifest 把这些状态重新输出成 MAG-owned runtime surface。

2026-05-16 focused hosted receipt verification follow-up：MAG 现在可以通过 `product hosted-receipt-verification` / `MedAutoGrantProductEntry.build_focused_hosted_receipt_verification` 读取外部 OPL attempt evidence JSON、MAG owner receipt evidence 和可选 sidecar closeout result，生成 `mag_focused_hosted_receipt_verification`。该 surface 只负责对账 `owner_receipt_ref`、`ledger_ref`、sidecar receipt ref 和 allowed result shape，证明单次 focused hosted attempt 返回 `domain_owner_receipt`、`typed_blocker` 或 `no_regression_evidence` 之一；它不调用 OPL、不写 OPL ledger、不实现 provider/retry/dead-letter，也不声明持续 live reconciliation 或 production soak。

2026-05-16 refs-only handoff closeout：MAG 进一步新增 `product lifecycle-receipt-bundle`、`product memory-receipt-projection`、`product package-lifecycle-handoff` 与 `product continuous-receipt-reconciliation`。这四个 surface 分别把 MAG lifecycle receipt refs、accepted/rejected memory receipt refs、package refs + gap/export verdict refs + manual portal boundary，以及 focused hosted verification + receipt inventory + observability projection 聚合成 body-free / artifact-free / OPL-led shell 可消费的 read projection。它们关闭的是 MAG repo-local projection builder 和 grouped CLI/API 缺口；它们不写 OPL ledger、不实现 OPL memory transport 或 package/artifact lifecycle shell、不执行 generic transition runner、不承诺持续 daemon，也不把 snapshot、provider completion 或 no-regression evidence 写成 grant-ready、quality-ready、export-ready 或 production soak。

2026-05-17 OPL Agent Lab migration guard：MAG 已新增 repo-native `meta` 测试，直接调用 OPL Agent Lab `agent-lab longline --json` 并断言 MAG 出现在 passed suite、`ready_to_reduce_domain_longline_tests=true`、`recommended_repo_test_disposition` 把 controlled grant-stage soak orchestration / receipt reconciliation projection / no-forbidden-write cross-domain regression 迁到 OPL Agent Lab，同时把 fundability scorer / grant owner receipt fixture / proposal artifact authority checks 留在 MAG。本轮完成的是测试 ownership 迁移 guard：framework-level longline orchestration、recovery probe 与 forbidden-write cross-domain regression 由 OPL Agent Lab 承接；MAG 仍保留 domain authority tests 和 grant-owned scorer、receipt fixture、artifact authority checks。该 guard 同步断言 OPL Agent Lab 不允许写 domain truth、memory body、memory accept/reject、quality verdict、fundability verdict 或 export/submission readiness verdict。

主要差距已经不在概念、命名、descriptor、MAG repo 内 receipt writer 或 consumer/thin adapter 功能面。后续计划也不应把 production closure / long soak 放成所有已知工作的前置条件。MAG 当前已经把可复用 workspace/source intake、memory locator/writeback transport、package/export lifecycle shell、generic transition runner、operator workbench、observability/SLO 和 scaffold/template 规则声明为 OPL-owned replacement expectation，并把本仓收窄为 grant authority pack、declarative grant pack 和迁移桥；2026-05-17 后进一步要求把 product status/user-loop/sidecar adapter、grouped CLI/API、projection builder 和 lifecycle adapter 这类仍手写的 thin shell 迁向 OPL generated surface。之后再用真实 grant-stage receipt、focused parity 和 live soak 验收。

当前缺口按执行顺序应读成：

- OPL closeout 已经能观察到 MAG stage closeout packet、owner receipt refs、controlled no-regression evidence refs、lifecycle receipt refs 与 accepted/rejected memory writeback receipt refs；MAG repo-local focused case 也已把 `grant_transition_oracle` fixture、sidecar `stage-attempt/closeout`、owner/no-regression receipt refs，以及 `mag_controlled_soak_receipt_reconciliation_proof` 对账 payload 固定为可测试闭环。本轮新增 `mag_controlled_soak_receipt_reconciliation_inventory` read projection / grouped CLI，并补齐 conflict/blocker envelope、receipt observability summary、stage-attempt observability projection、lifecycle receipt bundle、memory receipt read projection、package lifecycle handoff projection 与 continuous receipt reconciliation snapshot，用同一 refs-only 规则枚举或投影多条 receipt evidence 的 shape、status、typed blocker、no-regression refs、verdict refs、safe action refs、package refs 和 manual portal refs，仍不写 runtime receipt instance、OPL ledger、retry state、repair result、memory body 或 grant artifact。OPL runtime workbench 现在还能把 provider-hosted transition bridge 的 owner receipt refs、no-regression evidence refs 与 typed blocker refs 投影成 operator drilldown。这证明 receipt evidence path 与 MAG ref-only read model 可用，但还没有把真实 grant-stage long-run soak 写成完成。
- Grant strategy memory 已经超过 descriptor / locator 层，进入 consumed-memory、writeback receipt ref proof 和 body-free memory receipt read projection；真实 memory body migration、retrieval/writeback apply 的 workspace-runtime 泛化和跨 workspace policy 仍没有闭合。
- Package/export、artifact lifecycle、restore/retention、operator drilldown、route/decision graph 和 quality/readiness projection 需要由 OPL Framework / App 提供通用壳，MAG 已能回传 authority refs、gap report、receipt bundle 和 export verdict refs。
- 物理 skeleton 迁移、旧 Hermes/Gateway/local-manager active path、`domain_runtime_parts.patch_targets`、旧 flat CLI shell alias 和旧 `tests/test_product_entry.py` 聚合测试已经不再是兼容目标；后续发现 active caller 缺口时直接改到最新 owner surface，旧面只保留 history/provenance 或回归 oracle 语义。

这份计划的核心判断是：MAG 后续不应继续在仓内重复建设通用运行外围；应把可复用的 transport、lifecycle、projection、operator workbench 和 generated wrapper 能力上收到 OPL Framework / pack compiler，MAG 仓保持 grant-domain authority pack、declarative grant pack 和 minimal authority functions。

## 证据读取规则

本文不固定某次 `git status`、OPL CLI 计数或 runtime ledger 数字。维护 MAG 生产状态时，按下面顺序读取 fresh evidence：

1. MAG current truth：`docs/status.md`、核心五件套、`contracts/runtime-program/current-program.json`、product-entry manifest、MAG workspace/runtime receipt。
2. OPL family read model：`opl agents list --json`、`opl stages list --json`、`opl domain-memory list --json`、`opl framework production-closeout --json` 和 OPL runtime/provider receipt。
3. Cross-repo sibling input：MAS/RCA 的理想态、gap plan、status 和 domain receipt surface，只作为模式参考，不把 sibling backlog 写进本文。

读法保持三条约束：

- OPL descriptor/stage/memory resolved 说明 MAG 可被 OPL 发现和投影，不说明 MAG grant-stage production soak 完成。
- OPL provider completion 说明 framework attempt 完成，不产生 fundability-ready、quality-ready 或 export-ready verdict。
- MAG owner receipt、typed blocker、no-regression evidence、memory accept/reject receipt、package/export verdict 和 lifecycle receipt 必须来自 MAG-owned surface 或真实 workspace/runtime root。

当前状态和目标态的权威入口仍是：

- [MAG 理想目标态](../references/med-auto-grant-ideal-state.md)
- [MAG 当前状态](../status.md)
- [MAG 架构](../architecture.md)
- [MAG 不变量](../invariants.md)
- [MAG 决策记录](../decisions.md)
- [`current-program.json`](../../contracts/runtime-program/current-program.json)

## MAG 理想目标态的 owner 边界

MAG 理想态可以压缩成两条边界。

MAG 必须继续持有：

- funding call / funder family / applicant profile 的解释与任务锁定；
- fundability strategy、specific aims、claim-evidence structure 和 reviewer risk；
- proposal authoring、AI-first critique、revision、quality closure 和 issue lineage；
- grant strategy memory 的正文、检索语义、writeback proposal、accept/reject decision 和 receipt；
- local submission-ready package gate、gap report、export verdict 和 package refs；
- domain owner receipt、typed blocker、no-regression evidence 的 domain meaning；
- direct app skill path 与 OPL-hosted path 共享的 route truth、workspace truth、quality gate 和 export gate。

OPL Framework / One Person Lab App 应提供：

- provider-backed runtime、stage attempt ledger、queue、heartbeat、resume、human gate 和 retry/dead-letter；
- generic state-machine runner、transition schema、matrix runner、dispatch receipt 和 transition execution audit；
- workspace/source intake shell、artifact locator、package/export lifecycle shell、restore/retention 和 migration ledger；
- domain memory locator/index、receipt ref projection、freshness、operator grouping 和 writeback transport 壳；
- route/decision graph、quality/readiness projection shell、attention queue、operator drilldown、repair command projection 和 observability/SLO；
- source fingerprint、idempotency、no-forbidden-write proof、receipt audit 和 provider proof ledger；
- App/workbench 的通用展示与 action routing。

这个 owner split 意味着：MAG 后续新增能力时，凡是 grant 专业判断、正文生成、质量 verdict、memory accept/reject 或 export authority，都留在 MAG；凡是跨 MAS/MAG/RCA 可复用的运行外围、receipt transport、lifecycle、workbench、SLO 和 ref-only projection，都优先上收到 OPL。

## 总体差距矩阵

| 维度 | 理想情况 | 当前实际 | 差距 | 完善方向 |
| --- | --- | --- | --- | --- |
| MAG direct path | 单一 app skill / CLI / domain entry 能独立完成 grant authoring、review、package 和 owner receipt | direct capability surface 已落地，product status / user-loop / direct-entry / package submission-ready / quality surfaces 可调用 | 真实 end-to-end grant workspace 的 owner receipt、memory writeback 和 package lifecycle proof 不足 | 先补 workspace/package/memory/lifecycle handoff 与 owner refs，再选真实 grant workspace 跑 stage closeout，留下 owner receipt、quality closure、package refs 和 no-forbidden-write proof |
| OPL-hosted MAG path | OPL 托管 stage attempt，MAG 返回 domain receipt、typed blocker 或 no-regression evidence | OPL 可解析 MAG descriptor/stages/memory，已能从 MAG sidecar closeout 观察 owner receipt refs 与 controlled no-regression evidence refs；MAG consumer/thin adapter 功能面已通过 manifest/sidecar/schema guard 固定为只消费 OPL standard scaffold / generic primitives / functional harness；MAG repo-local focused hosted receipt verification 与 continuous receipt reconciliation snapshot 已落地 | 外部 OPL replacement production consumption、持续 live receipt reconciliation 和真实 grant-stage long-run soak 仍未闭合；MAG 明确不把 OPL harness pass 或 provider completion 写成 grant-ready/export-ready | 用真实 OPL-hosted attempt 生成 owner receipt / typed blocker / no-regression evidence，再扩展到 live reconciliation 和 live soak |
| Stage-led grant control plane | 6 个 grant stage 具备输入、prompt/skill、knowledge、quality gate、handoff、closeout | OPL `stages list` 可解析 MAG 6-stage plane | stage plane 仍偏 descriptor/projection；真实 owner receipt、memory/package/lifecycle handoff 与 provider-hosted activity 证据不足 | 先稳定 stage descriptor 与 OPL transition/package/memory/lifecycle shell，再对 `fundability_strategy`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready` 跑 controlled attempts |
| Grant transition table | MAG 理想上声明 domain transition spec，OPL 只执行通用 runner | `product-entry-manifest.grant_transition_oracle` 已落地 MAG-owned transition table / oracle fixtures，覆盖 call intake、fundability blocker、specific aims、proposal authoring、review repair、quality closure 和 package human-gate 状态；MAG focused proof 已把 `quality_closed_to_package` oracle fixture 通过 sidecar `stage-attempt/closeout` 写成 owner/no-regression receipt refs；OPL 已能只读 ingest 该 oracle 并通过 generic matrix runner 做 oracle smoke；OPL family runtime 现在也能把 `family_transition_matrix_result` hydrate 成 provider-hosted `family_transition/domain_tick` task，并把 transition bridge evidence refs-only 投到 runtime workbench/operator item；`controlled-soak-receipt-reconciliation-inventory` 已可把多条 MAG owner receipt evidence 聚合成 read-only reconciliation inventory | OPL generic runner handoff、retry/dead-letter、receipt 对账、真实 grant-stage long-run soak 仍未闭合；repo-local no-regression closeout case、OPL matrix smoke、transition task bridge、receipt inventory 或 workbench drilldown 不能写成 grant-stage production soak | 先把 oracle/transition result 接到 OPL generic runner 与 workbench shell，确认 MAG 只返回 owner receipt、typed blocker 或 no-regression evidence；随后再跑真实 OPL provider-hosted transition attempt 和 live receipt 对账 |
| Grant strategy memory | stage 检索少量 memory refs，closeout 生成 proposal，MAG owner accept/reject 并写 receipt | OPL memory descriptor resolved；MAG 已有 descriptor、proposal、accept/reject、runtime receipt evidence writer 和 body-free memory receipt read projection | retrieval/writeback apply、memory body migration 和真实 workspace receipts 未形成长线闭环 | 把真实 memory body 保持在 workspace/runtime root；OPL 只上收 locator/index/receipt projection 和 freshness |
| Package/export lifecycle | MAG 持 export gate，OPL/App 展示 package refs、gap report、restore/provenance 和 manual portal boundary | `package submission-ready` 是 MAG-owned export gate；MAG manifest 已把 package/export lifecycle shell 声明为 OPL replacement expectation，MAG 只保留 verdict、gap report、package refs、owner receipt，并已提供 package lifecycle handoff projection | OPL/App 外部 shell 的生产消费和真实 workspace package/lifecycle receipt 泛化仍未闭合 | OPL 提供 package/export shell；MAG 返回 submission-ready verdict、gap report、package refs、manual portal boundary 和 owner receipt |
| Artifact lifecycle | OPL 管 locator/retention/restore ledger，domain artifact mutation 需 MAG receipt | MAG 已有 lifecycle guarded apply proof；OPL closeout 已观察到 lifecycle receipt refs；consumer contract 明确 MAG 不持 generic artifact lifecycle owner；MAG 已能聚合 cleanup/restore/retention lifecycle receipt bundle | cleanup/restore/retention 的真实 workspace coverage 和 App/workbench drilldown 仍不足 | 扩展到真实 grant workspace 的 cleanup/restore/retention guarded receipt，并保持 OPL 只写自有 ledger/locator |
| Quality/readiness projection | App 展示 quality state、issue lineage、closure dossier、next action，但不替 MAG 下 verdict | MAG quality scorecard / closure dossier / diff 已落地 | 通用 quality/readiness drilldown 与 operator action shell 仍需 OPL/App 上收 | OPL 提供 projection shell；MAG 返回 AI critique-backed verdict、issue refs 和 hard blockers |
| Physical skeleton | repo-source 按 `agent/ contracts/ runtime/ docs/` 清晰分层，workspace artifacts 不进 source | MAG 已有 minimum repo-source anchors，OPL 读模型识别为 evidence observed；consumer contract 通过 `consumed_opl_standard_surfaces` 明确 MAG 消费 OPL standard scaffold | 更大范围物理迁移仍需 direct/hosted parity、restore/provenance proof 和 no-forbidden-artifact-blob proof | 按最新 owner surface 迁移；发现旧 import/caller/test 时直接改到新 surface，不保留 path compatibility shell |
| New-agent template readiness | 新 OPL Agent 应能按统一 docs taxonomy、descriptor/stage/action/memory/artifact locator、sidecar/receipt schema 和 no-forbidden-write gate 建仓 | MAG 已具备 `agent/`、`contracts/runtime-program/`、`plugins/mag`、`runtime/`、`schemas/`、canonical docs taxonomy、grant authority pack 和 declarative pack anchors；MAG 当前声明消费 OPL scaffold/checklist，不持有通用模板 owner | 目录仍混有 MAG-specific Python package、grant schemas、historical proof surface 和 artifacts/proof 输出；不能直接复制为通用 scaffold | 抽取 template 文档/contract checklist 到 OPL；MAG 保持 grant-specific 实现。 |
| OPL pack compiler / generated surface | OPL 应从 MAG descriptor、stage graph、action metadata、receipt schema、policy table 和 authority manifest 生成 CLI/product-entry/sidecar/status/workbench/harness | MAG 当前仍有手写 product status/user-loop/sidecar adapter、grouped CLI/API、projection builder、receipt/lifecycle helpers | 这些 thin shell 仍可能被误判为 MAG 必要私有功能；缺 OPL generated surface production consumption | 先把手写 shell 输入抽成声明式 pack，再把 active caller 迁到 OPL generated/replacement；MAG 只保留 fundability/quality/export verdict、package authority、memory accept/reject、owner receipt signer 和 grant helper。 |
| Legacy retirement | 旧 Hermes/Gateway/local-manager active path 只保留 history/proof/provenance | MAG status 已记录 tombstone / physically removed evidence；runtime patch bridge 与旧 product-entry 聚合测试已删除 | OPL closeout 仍把 physical delete 标记为 blocker，但 MAG 不再把旧面作为兼容目标 | 旧模块/接口/测试一旦无 active owner，直接删除或归档；只保留必要 provenance，不新增 alias/facade/compat test |

## OPL Framework 应上收的 MAG 通用外围

下面这些能力来自 MAG 理想态，但不应长期由 MAG 独自维护。它们的抽象对 MAS/RCA 也成立，应该成为 OPL Framework / App 的 family primitives。

| 应上收能力 | OPL owner surface | MAG 保留内容 | 验收信号 |
| --- | --- | --- | --- |
| Workspace/source intake shell | workspace locator、source receipt、profile/call material intake、freshness、repair command | funding call 解释、profile selection、task lock、funder fit | 同一 intake shell 可服务 MAS study、MAG grant、RCA visual source；domain 返回 selected target 和 domain receipt |
| TODO / human gate / wakeup transport | typed queue、human gate token、resume signal、attention queue、dead-letter | 哪些问题构成 grant blocker，哪些只是 objective TODO | OPL action 只路由；MAG 决定 blocker severity 和 authoring impact |
| Grant strategy memory locator/index | memory descriptor、locator、body-free inventory、freshness、operator grouping | memory body、retrieval semantics、writeback proposal、accept/reject | OPL 不显示 memory body、不接收 writeback，只显示 refs/receipts |
| Memory writeback transport | proposal refs、receipt refs、accepted/rejected projection、SLO | 是否接受写回、写回正文、fundability/quality 影响 | MAG workspace/runtime root 有 accepted/rejected receipt；OPL 只读 receipt ref |
| Artifact/package lifecycle shell | artifact locator、package refs、gap report slot、restore/retention ledger、manual portal boundary | submission-ready verdict、export gate、grant package authority | App 显示 refs/gaps/provenance，但不推断 export readiness |
| Route/decision graph | stage route graph renderer、decision history view、handoff graph | fundability decision、aims strategy、revision rationale | OPL 画图，MAG 输出 route nodes/edges/rationale refs |
| State-machine runner / transition matrix | transition schema、matrix runner、tick/retry/dead-letter/human gate、dispatch receipt、transition audit、transition bridge evidence refs-only workbench drilldown | grant transition table、fundability / aims / review / package guards、typed blocker、owner action | OPL 只执行 MAG-declared spec，不产生 fundability-ready、quality-ready 或 export-ready verdict |
| Quality/readiness projection shell | quality panel、issue lineage viewer、closure dossier locator、attention item | AI critique、authoring quality verdict、hard blocker verdict | 无 active AI critique 时 App 只能显示 projection-only |
| Operator observability/SLO | provider proof freshness、attempt age、receipt latency、repair actions | domain success/failure meaning | provider ready 不等于 MAG ready；所有状态轴分开显示 |
| No-forbidden-write / idempotency | source fingerprint、attempt idempotency、forbidden write audit、receipt ledger | workspace mutation permission、artifact write authority | OPL 能证明自己未写 grant truth/artifact/memory body |

这组上收不改变 authority：OPL 提供壳、transport、ledger、projection、UI 和 generated entry surface；MAG 继续持有 domain truth、quality/export verdict、artifact/memory authority、声明式 grant pack 和 minimal authority functions。

## 各仓当前实际状态对 MAG 的影响

### MAG

MAG 当前是 Grant Foundry 的 active domain agent。已成立的部分包括：

- 单一 app skill、CLI、`MedAutoGrantDomainEntry` 和 schema-backed contract；
- 6-stage grant control plane、family action catalog、runtime control/continuity；
- product sidecar export/dispatch、OPL stage runtime registration、standard skeleton descriptor；
- owner receipt contract、controlled domain-memory receipt evidence writer、lifecycle guarded apply proof、grant transition oracle table / oracle fixtures，以及 oracle -> sidecar stage-attempt closeout -> owner/no-regression receipt refs 的 repo-local focused proof；
- physical skeleton minimum anchors、runtime patch bridge 退役、旧 product-entry 聚合测试删除和 no-forbidden-write projection。

MAG 当前不能声明：

- OPL-hosted grant-stage production soak 已完成；
- MAG grant-stage 长时 soak 已闭合；
- grant strategy memory body migration、retrieval/writeback apply 已在真实 workspace/runtime root 泛化完成；
- package/export lifecycle shell 已由 OPL/App 产品化；
- OPL 侧 legacy physical delete blocker 已被观察到，尚未关闭；MAG 侧不因此保留旧兼容面，而是按最新 owner surface 迁移 caller 后直接删除或归档旧面。

### OPL

OPL 当前已经从“descriptor / projection only”推进到更完整的 framework closeout read model：Temporal provider readiness、provider continuous proof、stage attempt ledger、runtime snapshot、domain descriptor aggregation、production closeout gate 都已可读。对 MAG 来说，这证明 OPL 具备托管 MAG 的框架前提，但仍不能替 MAG 产出 grant truth 或 quality/export verdict。

MAG 对 OPL 的依赖重点应转为：

- 真实 OPL-hosted grant-stage attempt 的长时 soak、持续 no-regression evidence 与 receipt 对账；OPL workbench drilldown 只作为 refs-only visibility，不作为 grant ready verdict；
- generic workspace/source intake、memory locator、artifact/package lifecycle、quality/readiness shell 和 App drilldown；
- provider proof cadence、operator SLO 和 repair command projection；
- no-forbidden-write、direct/hosted parity 和 provenance retention 证据。

### MAS

MAS 当前提供了最接近 production owner-chain 的 sibling 样板：它已经有真实 paper-line proof surface、publication-route memory policy、stage knowledge packet、typed closeout routing、provider proof ingestion 和 body-free inventory/grouping/read-model。但 MAS 仍未声明 production-hosted paper automation 闭合，真实 owner apply receipt chain、human gate/resume、更多 memory receipts 和 legacy cleanup 仍在 production evidence gate。

对 MAG 的启发是：

- MAG 的 grant strategy memory 应采用类似 MAS publication-route memory 的 body-free inventory / receipt projection / owner accept-reject 边界；
- 真实 workspace owner receipt 比 descriptor 更重要；MAG 下一步应把已可观察 receipt/no-regression evidence 推进到长时 soak与泛化 memory apply；
- human gate、route decision、artifact mutation 必须回到 domain owner，不由 OPL provider completion 推断。

### RCA

RCA 当前提供了 artifact-heavy domain 的 sibling 样板：direct route 已 landed，OPL-hosted route 是 contract/projection landed；image-first/default visual route、artifact locator、controlled memory apply proof、lifecycle guarded apply proof 和 visual no-regression evidence refs 都已形成。它仍缺 visual-stage long soak、artifact-producing owner receipt 和真实 visual memory body writeback。

对 MAG 的启发是：

- package/export lifecycle shell 应按 RCA artifact gallery/handoff 思路上收到 OPL/App，MAG 只返回 export refs、gap report 和 verdict；
- no-regression evidence 可以先作为 controlled attempt 的有效收口形态，但不能替代 domain owner receipt；
- artifact blob / export package / receipt instance 不进入 repo source 的边界必须持续保持。

## 最短实施顺序

### P0：维护 MAG 侧 gap plan 与 owner 边界

目标：让 MAG 后续 work 不散落在对话或相邻仓 dirty docs 中，并明确过时模块/接口/测试的清理规则。

动作：

1. 保持本文为 MAG active plan，核心 current truth 继续归 `docs/status.md`、核心五件套和 `current-program.json`。
2. 在后续 MAG work 中优先引用 `docs/references/med-auto-grant-ideal-state.md` 和本文，区分 north-star、current truth、active plan 和 fresh evidence。
3. 不在 MAG 文档中把 OPL provider readiness、descriptor aligned 或 receipt packet 写成 production long-run soak 完成。
4. 旧模块、旧接口、旧测试、flat shell alias、facade monkeypatch bridge、聚合测试入口和旧 runtime owner wording 只要已经被最新 owner surface 替代，就直接删除或归档；不得新增兼容 alias、兼容 facade 或兼容测试入口。

验收：

- `docs/active/README*` 和 docs portfolio 能定位本文，并声明 active plan 采用 direct retirement posture；
- `scripts/verify.sh meta` 通过；
- diff 只包含 MAG 文档与文档索引。

### P1：OPL generic primitive absorption design and MAG adapter thinning

目标：把 MAG 已明确不应长期持有的通用外围能力声明为 OPL owner primitive，并把 MAG 侧 adapter 收薄；不等待真实 grant-stage live soak。2026-05-17 后新增要求：能由 OPL pack compiler 生成的 product status/user-loop/sidecar/grouped CLI/API/projection/lifecycle wrapper 不再作为 MAG 长期私有实现。

当前状态：MAG 侧功能面 follow-through 已完成。`mag_consumer_thinning_contract`、`consumed_opl_standard_surfaces`、`functional_harness_consumer_coverage`、`thin_surface_output_guard`、sidecar export、schema 和 focused tests 已经固定 MAG 只消费 OPL standard scaffold / generic primitives / functional harness，不持有 generic scheduler/daemon/queue/attempt ledger/runner/workbench/memory transport/artifact lifecycle，也不把 OPL harness pass 提升成 grant-ready 或 export-ready。

动作：

1. 保持 MAG manifest/sidecar thin adapter 角色：只输出 refs、receipt、typed blocker、verdict refs 和 domain action metadata。
2. 继续把 workspace/source intake shell、memory locator/writeback transport、package/export lifecycle shell、generic transition runner、operator workbench/observability/SLO 和 agent scaffold checklist 作为 OPL replacement expectation。
3. MAG 后续新增 contract 时同步保留 authority boundary 字段：`opl_can_write_domain_truth=false`、`opl_can_write_memory_body=false`、`opl_can_declare_export_ready=false`。
4. 若发现 MAG 新增 generic scheduler、daemon、queue、attempt ledger、generic runner、workbench、memory transport 或 artifact lifecycle owner 角色，视为回归。
5. 将 MAG hand-written thin shell 的输入抽成 declarative grant pack：stage graph、action intent、source/package/memory policies、transition oracle、receipt schema、authority function manifest 和 fixtures；OPL generated surface 可用后迁移 active caller。

验收：

- `product-entry-manifest.mag_consumer_thinning_contract` 和 `product sidecar export.mag_consumer_thinning_contract` 存在，且只声明 refs、receipt、typed blocker、verdict refs 和 domain action metadata，并通过 `thin_surface_output_guard` 禁止 generic runtime / workbench state、grant artifact content 和 memory body；
- `privatized_functional_module_audit` 存在，且把 OPL-owned generic primitive consumer、MAG-owned grant truth / receipt / verdict、retire/tombstone 三类分开，同时把 grant lifecycle stage、package readiness / submission-ready、fundability / quality / export verdict 列入不得退役的 domain authority；
- `consumed_opl_standard_surfaces` 明确 MAG 消费 OPL standard scaffold / generic primitives / functional harness，并保留 grant truth、fundability/quality/export verdict、memory accept/reject、package authority 和 owner receipt；
- `functional_harness_consumer_coverage` 明确覆盖 memory refs-only writeback chain、queue/stage attempt/typed closeout、generic transition runner、restart/dead-letter/repair/human gate 状态链，且 fail-closed 禁止 `OPL harness pass = grant ready/export ready`；
- MAG sidecar/direct entry 不再新增 generic scheduler、daemon、queue、attempt ledger、generic runner、workbench、memory transport、artifact lifecycle 或 generic lifecycle owner；
- App/workbench 展示 owner、freshness、next action 和 repair command，但不越权下 fundability / quality / export verdict。

### P2：Package/export 与 artifact lifecycle shell handoff

目标：把 MAG submission-ready package 和 artifact lifecycle 接到 OPL/App 通用 shell，而不是让 MAG 自己承担通用 gallery、handoff、restore/retention 和 operator navigation。

当前状态：MAG 侧 consumer contract 已把 package/export lifecycle shell 和 generic artifact lifecycle 声明为 OPL-owned replacement expectation，并把 MAG 保留内容限制为 package refs、gap report、submission-ready verdict、manual portal boundary、lifecycle receipt bundle 和 owner receipt。`product package-lifecycle-handoff` 与 `product lifecycle-receipt-bundle` 已提供 refs-only grouped CLI/API。剩余不是 MAG manifest/sidecar/projection builder 功能缺口，而是真实 workspace lifecycle receipt 泛化与 OPL/App 外部 shell 生产消费证据。

动作：

1. MAG 继续持有 `package submission-ready` fail-closed gate、gap report、export verdict 和 owner receipt。
2. OPL/App 提供 package refs、delivery artifact index、gap report slot、restore/provenance、retention、external portal/manual submission boundary 的通用 shell。
3. cleanup/restore/retention guarded apply 在真实 grant workspace 上产出 MAG lifecycle receipt。
4. App action routing 明确指向 OPL ledger 操作、MAG package command 或人工 portal step。
5. MAG repo 不保存真实 export package、receipt instance、private evidence 或 memory body。

验收：

- App/workbench 可以只读看到 package state、gap report、owner、freshness、manual portal boundary 和 MAG lifecycle receipt refs；
- OPL 只能管理 locator/ledger，不能删除或改写 MAG artifact；
- MAG lifecycle receipt 是 artifact mutation 的唯一授权来源。

### P3：Grant strategy memory locator/writeback handoff

目标：让 grant strategy memory 从已可观察 writeback receipt refs 推进到真实 workspace/runtime memory body migration、retrieval apply 与 writeback apply 泛化，同时把通用 locator/index/transport 上收到 OPL。

当前状态：MAG 侧 consumer contract 已把 memory locator/writeback transport 声明为 OPL-owned replacement expectation，并通过 `consumed_opl_standard_surfaces` 保留 MAG 对 memory body、writeback proposal、accept/reject 和 receipt writer 的 authority。`product memory-receipt-projection` 已把 accepted/rejected receipts 收成 body-free refs projection。剩余是真实 workspace/runtime memory body migration、retrieval/writeback apply 和跨 workspace policy 泛化。

动作：

1. 对真实 grant stage closeout 继续生成 writeback proposal，并复用已有 MAG owner accept/reject 和 runtime receipt evidence path。
2. 把 accepted/rejected receipt 从单点 evidence 推进到 workspace/runtime memory body migration 与 retrieval/writeback apply policy。
3. memory body 仅写入 MAG workspace/runtime memory pack，不进入 repo source 或 OPL state。
4. OPL/App 只显示 consumed refs、proposal refs、accept/reject receipt refs、freshness 和 operator grouping。
5. 移除任何只为旧 memory descriptor shape、旧 product-status trace 或旧测试 monkeypatch 存在的 compatibility path。

验收：

- 至少一条 accepted 与一条 rejected receipt 可由 MAG CLI/API 读取，并能通过 `product memory-receipt-projection` 输出 body-free refs projection；
- OPL `domain-memory` read model 继续显示 descriptor/receipt-locator，不显示 memory body；
- `domain-memory list` 对 MAG 不再显示 retrieval/writeback apply 与 memory body migration 为未落地，或明确返回 typed blocker；
- quality/export verdict 不由 memory receipt 自动产生。

### P4：Physical skeleton/template extraction and legacy direct retirement

目标：把 MAG 作为 grant-domain 参考实现中可复用的 skeleton 规则抽到 OPL template/checklist，同时按最新 owner surface 清理旧面，不保留过时兼容接口；把 hand-written thin shell 继续降为迁移桥。

当前状态：MAG 侧 consumer contract 已通过 `standard_agent_scaffold_alignment` 与 `consumed_opl_standard_surfaces` 固定为 OPL standard scaffold 的消费方；MAG 保留 grant-domain source、descriptor、schema、sidecar、projection builder、receipt writer 和 focused tests，不持有通用 scaffold template owner。剩余是 OPL 抽取通用 template/checklist 的外部证据，以及后续发现旧 caller 时按最新 owner surface 继续 direct retirement。

动作：

1. 抽取 OPL-compatible agent 的 docs taxonomy、descriptor/stage/action/memory/artifact locator、sidecar/receipt schema、no-forbidden-write、runtime artifact 不进 source、direct/hosted parity checklist。
2. 抽取 OPL pack compiler 输入清单：domain descriptor、stage graph、action metadata、policy table、receipt schema、authority function manifest、fixtures、no-forbidden-write contract。
3. 以 `agent/ contracts/ runtime/ docs/` 作为 repo-source owner layout，验证 direct app skill path、MAG CLI、OPL-hosted path、restore/provenance proof 和 focused tests。
4. 发现旧 Hermes/Gateway/local-manager 命名、旧 facade patch target、flat CLI shell alias、旧聚合测试、旧 product-status trace 或手写 generated-wrapper 替代面仍被 active caller 使用时，改 caller 到最新 owner surface。
5. caller 迁完后直接删除旧模块/接口/测试，或移入 history/tombstone；不保留 compatibility shim、alias、re-export 或 monkeypatch bridge。
6. 保留必要 provenance 和 regression oracle 语义，但旧名不得重新取得 default runtime、public integration authority 或测试入口地位。

验收：

- OPL `agents list` 继续 `aligned_count=3`、MAG descriptor 无 drift；
- MAG repo 不跟踪真实 workspace artifacts、receipt instances、memory body 或 export packages；
- active path scan 不再发现默认 caller 使用旧 Hermes/Gateway/local-manager、`domain_runtime_parts.patch_targets`、flat shell alias 或旧 `tests/test_product_entry.py` 聚合入口。

### P5：Focused OPL-hosted receipt verification

目标：在功能上收、adapter thinning、memory/package/lifecycle handoff 和 skeleton cleanup 完成后，用 focused hosted attempt 和 continuous read snapshot 验证 MAG owner receipt / typed blocker / no-regression path。

动作：

1. 使用 OPL task-bound provider-backed attempt 触发 MAG sidecar / direct entry，优先覆盖 `fundability_strategy`、`review_and_rebuttal` 与 `package_and_submit_ready`。
2. 对每次 attempt 固定三类结果之一：`domain_receipt`、`typed_blocker`、`no_regression_evidence`。
3. 在 OPL runtime ledger 与 MAG workspace/runtime root 之间对账 receipt ref；MAG 侧使用 `focused-hosted-receipt-verification` 验证单次 hosted attempt evidence 与 MAG owner receipt refs，使用 `controlled-soak-receipt-reconciliation-proof` 生成 repo-local probe payload，使用 `controlled-soak-receipt-reconciliation-inventory` 汇总多条 receipt evidence 的 read-only projection，并用 `continuous-receipt-reconciliation` 把 focused verification、receipt observability 与 stage-attempt observability 收成 read snapshot，确认重复 closeout packet 不制造第二真相。
4. 持续证明 OPL 没有写 grant truth、memory body、quality verdict 或 export package。

验收：

- OPL closeout 中 MAG domain breakdown 出现 owner receipt ref，并能观察 no-regression evidence ref 或明确 typed blocker；
- MAG workspace/runtime root 有对应 receipt evidence，且同一 receipt ref 可通过 `focused-hosted-receipt-verification` 与 OPL attempt evidence 对账，并可进入 `continuous-receipt-reconciliation` read snapshot；
- provider completion 和 MAG ready verdict 在 projection 中保持分轴显示。

### P6：Live soak and production closure

目标：最后再把 focused receipt verification 扩展为真实 grant-stage long-run soak 和 production closure。

动作：

1. 对至少一条真实 grant-stage line 运行长时 soak，输出 domain receipt、no-regression evidence 或明确 typed blocker。
2. 证明 retry/dead-letter、human gate、provider SLO、receipt latency、memory/writeback、package/lifecycle 和 App drilldown 都使用迁移后的 OPL generic primitive。
3. 长时 evidence 只能作为生产验收，不倒置为 P1-P4 功能迁移的前置条件。

验收：

- long-run soak 有 OPL provider receipt、MAG owner receipt / typed blocker / no-regression ref、no-forbidden-write proof 和 App/operator drilldown；
- provider completion 不产生 fundability-ready、quality-ready 或 export-ready verdict；
- production closure 只在真实 grant owner chain、memory/package/lifecycle refs 与 OPL primitive boundaries 都成立后声明。

## 当前不能写成

- 不把 MAG 改成 OPL 内部模块。
- 不把 OPL provider completion 写成 MAG fundability-ready、quality-ready 或 export-ready。
- 不把 grant strategy memory body、private evidence、receipt instance 或 export package 放进 repo source。
- 不在 MAG 仓内实现 generic provider runtime、generic executor registry 或 App workbench。
- 不用非默认 executor 的 proof 替代 Codex CLI 默认执行语义。
- 不在缺少 receipt 对账和真实长时 soak 的情况下声称 production long-run soak 完成。
- 不为过时模块、接口、CLI alias、facade patch target 或测试聚合入口新增兼容层。
- 不把 MAG 当前 repo 物理结构写成完全统一的新 Agent scaffold；它是 grant-domain 参考实现，通用 scaffold 规则应由 OPL 抽象成模板/checklist。

## 下一步推荐顺序

1. 用真实 workspace 把 grant strategy memory accepted/rejected receipts 推进到 memory body migration 与 retrieval/writeback apply 泛化，并让 OPL/App 消费 `memory-receipt-projection` 的 body-free refs。
2. 用真实 workspace 跑 package/export lifecycle 与 cleanup/restore/retention guarded receipts，并让 OPL/App 消费 `package-lifecycle-handoff` 与 `lifecycle-receipt-bundle`。
3. 在 OPL/App 侧补齐 generic primitive replacement 的生产证据：memory locator/writeback transport、package/export lifecycle shell、quality/readiness projection shell、operator observability/SLO 和 scaffold/template checklist。
4. 在 OPL 侧补齐 pack compiler / generated surface，把 MAG 当前手写 product status、sidecar、grouped CLI/API、projection、lifecycle wrapper 的输入迁到 declarative grant pack。
5. 按 latest owner surface 推进 MAG legacy cleanup；旧模块、旧接口、旧测试或 hand-written thin shell 已被替代就直接清理或归档。
6. 选定一个低风险真实 grant-stage line，用已可 ingest / hydrate 的 `grant_transition_oracle` 跑 focused hosted receipt verification、continuous receipt reconciliation 与 live receipt 对账。
7. 最后扩展到 long-run live soak；live soak 是生产验收，不再作为 MAG consumer/thin adapter 功能迁移、上收、清理的前置条件。

完成上述步骤后，MAG 才能从 “OPL-compatible domain authority pack + migration-bridge thin surface consumer follow-through complete” 进入更接近 “production-hosted declarative grant agent” 的状态。
