# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `ideal_state_gap_plan`
State: `active_plan`
Machine boundary: 本文是人读 gap / completion plan。机器真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、product-entry manifest、workspace/runtime artifact root、receipt、质量报告和导出包。
Date: `2026-05-19`

## 文档读法

- 本文只维护 MAG 当前定位、owner 边界、结构收口状态、测试/证据差距和完善顺序。
- MAG 的 north-star 目标态回到 [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md)。
- dated 过程校准、follow-through、receipt proof 和 closeout 记录归档到 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。
- 差距按目标态判断，不按当前 MAG 代码是否仍可运行判断。通用 runtime、runner、queue、session、journal、workspace/source intake、memory/package transport、workbench、observability、CLI/product-entry/sidecar/status wrapper 必须进入 OPL 上收、generated surface 替换、refs-only 收薄或退役分类。
- 过时模块、接口、测试、fixture、CLI alias、facade、wrapper 和 docs 入口不保留兼容面。local runtime journal、attempt ledger、repo scheduler、Hermes/Gateway/local-manager probe、flat alias、compat aggregate test 等旧面在 active caller 迁出后直接删除、archive 或 tombstone；测试只保留 no-resurrection / negative guard，不维护旧调用路径。

## 当前定位

MAG 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 是一等入口；OPL-hosted path 可以发现、托管、唤醒和投影 MAG，但必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。

OPL Framework / shared family layer 持有通用 provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。MAG 不把这些通用能力继续写成长期私有平台。

当前 product-entry manifest / schema / tests 的 runtime contract 字段为 `opl_provider_runtime_contract`。该字段指向 OPL/configured family provider runtime owner；`codex_cli` 只保留为默认 executor owner / default executor，不再作为 active runtime owner。

## 当前边界

MAG 必须持有：

- funding call 解释、profile/task lock、fundability strategy、specific aims 和 proposal route truth。
- grant stage pack、prompt/skill、policy table、domain transition oracle、quality/review/export gate。
- grant strategy memory body、accept/reject decision、writeback receipt 和 owner boundary。
- submission-ready package、gap report、manual portal boundary、package/export authority 和 owner receipt。
- typed blocker、safe action refs、no-forbidden-write guard 和 MAG domain projection refs。

OPL 必须持有：

- stage attempt lifecycle、queue/wakeup、provider workflow、retry/dead-letter、human gate transport 和 attempt ledger。
- generic transition runner、workspace/source shell、memory/artifact locator、package/export lifecycle shell、observability/SLO 和 App/workbench shell。
- CLI/product-entry/sidecar/status/workbench/harness wrapper 的 generated/hosted surface，除非 MAG 明确保留为 direct domain handler、refs-only adapter、authority function 或迁移桥。

## 当前结构收口状态

当前机器状态：

`mag_functional_structure_gap_count=0`

`classification_gap_count=0`、`followthrough_gaps_open=false`、`claims_opl_replacement_exists=false` 和 `claims_all_bridge_exits_complete=false` 表示 MAG repo 侧已经把当前 surface 收到 handler/ref-only/authority 边界，但外部 OPL generated/hosted caller、真实 App/workbench 消费、全部 bridge exit 和 production long-run soak 仍是证据门。凡仍由 MAG CLI/product-status/sidecar 作为 handler target 或 direct domain entry 的 product/status/user-loop/sidecar/grouped CLI/projection/lifecycle surface，都必须写成 OPL generated/hosted caller 的 domain handler、ref-only adapter 或 minimal authority function。MAG 仍不是纯 knowledge pack；它保留 grant authority functions、domain handler、receipt schema/writer、transition oracle、quality/export verdict、package authority、memory accept/reject 和 focused contract tests。

2026-05-19 production acceptance lane 已把 `production_live_soak_not_claimed_by_conformance` / `domain_ready_not_claimed_by_conformance` 收为 MAG-owned evidence tail，而不是新的结构标准化缺口。稳定机器面为 `contracts/production_acceptance/mag-production-acceptance.json`：structural / physical conformance 记录为 passed，production-like grant receipt chain refs 记录为 present；grant/domain/fundability readiness 仍必须由 MAG owner receipt、typed blocker 或 no-regression evidence refs 裁决。当前 `evidence_tail_status=domain_owned_typed_blocker_with_next_verification_ref`，表示下一步是按 contract 内 command refs 继续验证 owner receipt scaleout，而不是由 OPL/provider/conformance 替 MAG 宣布 grant-ready。

2026-05-19 的 stage cohort-loop refs 已作为结构闭环落地。MAG 当前六个 stage 都声明 `source_scope_refs`、`cohort_query_refs`、OPL queue `trigger_refs`、`monitor_refs` 和 `dashboard_metric_refs`；OPL isolated verification 对当前 MAG main 返回 `stage_count=6`、`closed_loop_ready_count=6`、`blocker_count=0`。这关闭的是 declarative launch/readiness loop gap；外部 OPL generated/hosted caller、真实 App/workbench consumption、grant-stage owner receipt scaleout、direct/hosted parity 和 Temporal soak 仍归 evidence gate。

`opl_provider_runtime_contract` 的落地只关闭 manifest/schema/test 的 owner 语义漂移；它不声明 OPL production/default caller、Temporal long soak、App/workbench consumption 或 live receipt reconciliation 已完成。

1. `generated_surface_bridge_exit`
   `mag_consumer_thinning_contract.generated_surface_handoff.bridge_exit_gate` 固定 OPL generated/hosted wrapper owner，MAG 当前路径只作为 domain handler target 和 grant authority refs。退出证据包括 OPL generated interface compile/scaffold、direct MAG domain handler no-regression、owner receipt / typed blocker refs roundtrip、thin output guard、no-forbidden-write 与 no-active-wrapper scan。

2. `legacy_runtime_session_lifecycle_exit`
   local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge 和 compat aggregate test 都进入 legacy proof / tombstone / regression-oracle 语境；无 active caller 后直接删除或归档，不保留 compatibility alias。

3. `package_memory_lifecycle_refs_only_boundary`
   memory receipt projection、package lifecycle handoff、lifecycle receipt bundle、continuous receipt reconciliation 和 sidecar export 只输出 body-free refs、owner receipt、verdict refs、typed blocker 和 safe action metadata；不输出 memory body、grant artifact/private evidence 或 OPL ledger state。

4. `private_authority_ai_first_guard`
   fundability、quality、export、package、memory、transition oracle、owner receipt 和 grant helper 是 MAG 可保留的 minimal authority surfaces，但不能用函数调用跳过 OPL stage。`function_id` 只保留兼容含义；机器面以 `authority_surface_id`、`work_mode`、`judgment_owner`、`programmatic_role` 和 `mechanical_decision_forbidden` 表达真实边界。fundability / authoring quality / critique / export readiness / memory accept-reject 必须来自 AI-first grant stage artifact；代码只做 schema validator、materializer、receipt signer、guard 和 refs projection。
   当前机器面已把 `fundability_verdict`、`quality_verdict`、`export_verdict`、`package_authority`、`memory_accept_reject`、`owner_receipt_signer` 和 `grant_helper` 的 AI-first taxonomy、`ai_first_guard`、`allowed_return_shapes` 与 `output_boundary` 投影到 `functional_privatization_audit`、product-entry manifest、sidecar export 和 pack compiler input；这只证明 retained authority surface 的 MAG 边界可验，不证明外部 OPL generated caller、真实 App 消费或 production soak 已完成。

5. `contract_source_ref_refresh`
   privatized audit、generated-surface handoff 和 consumer/thinning contract 中的 code path / source_ref 已作为当前 bridge-exit 证据读取；后续若路径漂移，只能进入 source-ref refresh、history/provenance 或 tombstone，不能用漂移路径证明当前状态。
当前 machine-readable handoff 已为每个 generated/bridge surface 的 `current_mag_paths` 投影 `current_mag_path_status`；aggregate `missing_current_mag_path_count=0`、`stale_path_policy=history_or_source_ref_refresh_only`。这只证明 MAG 当前 source refs 存在并可刷新，不声明 OPL replacement exists、bridge exit complete 或 production soak complete。

2026-05-19 的 standard pack 合同校准把根层 `pack_compiler_input` 和 runtime-program/adoption surface 收为 OPL scaffold canonical 形状：`canonical_semantic_pack_root="agent/"`、`canonical_semantic_pack_role="repo_source_declarative_grant_pack"`，并从 active machine required / anchor / source-ref lists 移除 `agent/README.md`。README 仍可作为人读入口与 provenance ref 存在，但不能作为机器 required semantic pack path；OPL scaffold validation 只接受真实 prompt / stage / skill / quality gate / knowledge 文件作为 pack compiler 输入。`contracts/runtime-program/current-program.json` 与 `contracts/runtime-program/opl-family-contract-adoption.json` 若保留 `standard_domain_agent_skeleton.canonical_repo_source_semantic_pack`，必须同时声明它只是 `historical_runtime_program_snapshot_only_not_pack_compiler_input`，不能反向定义 root pack compiler shape。

2026-05-19 的 physical source morphology 调研把 MAG 的源码目标进一步固定：`agent/` 承载 grant semantic pack，`contracts/` 承载 machine contracts / handoff / external evidence request，`src/med_autogrant/**` 长期只保留 grant domain handler、minimal authority function、refs-only adapter、native helper、fixture 或 diagnostic。`product_entry_parts`、`domain_runtime_parts`、sidecar/status/user-loop、runtime registration、lifecycle receipt bundle、memory receipt projection、package lifecycle handoff、observability refs 和 human workbench / scheduler metadata 不能被读成 MAG-owned runtime platform；它们必须继续写成 OPL generated/hosted caller 的 domain target、refs-only adapter、grant authority refs 或 history/tombstone。当前 `mag_functional_structure_gap_count=0` 表示 repo-side handler/ref-only/authority 边界已闭合，不表示物理命名已经完全像新 agent 模板，也不授权恢复 local journal、attempt ledger、scheduler daemon、Hermes/Gateway/local-manager probe 或 compatibility alias。

2026-05-19 fresh `opl agents conformance --family-defaults --json` 返回 MAG structural conformance `passed`，family 汇总为 4/4 structural pass。MAG active exact legacy residue gate 已使用中性 forbidden residue classes，旧 local journal、attempt ledger、repo scheduler、executor probe 和 compat alias 只能作为 history/tombstone/provenance 语境读取。该门槛不声明 external production/default caller、真实 App consumption、grant-stage owner receipt scaleout 或 Temporal long-soak 已完成。

这条目标吸收的是成熟 agent/runtime 项目对职责分层的经验，不引入它们作为依赖。2026-05-19 live check 中，OpenAI Agents SDK 把 Agent 的 instructions/tools/handoffs/guardrails/sessions 与 Runner orchestration 分开；LangGraph 把 graph state 的 checkpoint、thread、store、replay 分开；AutoGen 把 agents、tools/workbench、teams、state/termination 分开；CrewAI 用声明式 agent role/goal/tools 和 crew/process 承载协作。MAG 对应落点是：grant pack、authority function、runtime orchestration、session/checkpoint、workbench/evidence gate 分离；OPL 持有通用 orchestration，MAG 持有 grant judgment。

当前 MAG 的物理源码形态仍有 cleanup tail：`domain_runtime_parts/substrate.py` 聚合 workspace、route、quality、export 与 controller 方法；`domain_entry.py` 维护 service-safe command catalog；`cli.py` 暴露 mainline/status/cockpit/direct-entry/user-loop/product/sidecar/status wrapper；`product_entry_parts/manifest_builder.py`、`manifest.py`、`sidecar.py` 和 `runtime_registration.py` 仍构造 product-entry、status、sidecar、runtime registration、resume/wakeup/lifecycle adapter；`control_plane.py` 与 `owner_receipts.py` 仍处理 runtime-state refs；`grant_autonomy_controller.py` 仍表达 loop/budget/reselection/rollback/quality scheduling。它们当前是 direct domain handler、refs-only adapter、authority refs、regression oracle 或 migration input；不是最终标准 Agent 模板。后续应按 generated caller parity 和 external evidence request pack 逐项收薄、改名、迁出或 tombstone。

6. `external_evidence_request_pack`
   `mag_consumer_thinning_contract.external_evidence_request_pack` 已把剩余外部证据门收成 machine-readable request pack：OPL generated/hosted caller consumption、Codex App workbench refs consumption、production/default caller release/dist consumption、owner receipt / typed blocker roundtrip、continuous no-forbidden-write、direct/hosted parity 和 Temporal provider long-soak receipt reconciliation。该 pack 的状态是 `request_pack_declared_external_evidence_not_claimed`，每个 request 仍是 `requested_not_received`；它只固定 required refs、receipt shapes 和 forbidden payload classes，不实现 OPL runtime / App workbench，也不声明外部证据已完成。

7. `legacy_cleanup_opl_ledger_apply_verified`
   `physical_skeleton_follow_through` 已补齐 replacement parity refs、no-regression evidence refs、tombstone/history refs 和 physically removed active path 的 domain owner handoff receipt refs。2026-05-19 OPL dry-run 读取当前 MAG manifest 后，`opl agents legacy-cleanup apply --domain mag --mode dry-run` 返回 `plan_status=ready`、`lifecycle_apply.status=dry_run_ready`、`safe_action_count=3`、`unsafe_action_count=0`；随后 `--mode apply` 已把 1 条 batch receipt 与 3 条 action receipts 写入 OPL refs-only lifecycle ledger，`--mode verify` 可读回 batch / tombstone / handoff action receipts 和 2 条 domain owner handoff receipt refs。这关闭的是 OPL cleanup ledger blocker；它不声明外部 OPL/App production caller evidence、grant-stage live soak 或 owner receipt scaleout 已完成。
   当前根层 `functional_privatization_audit.mag_consumer_thinning_contract.active_path_scan_state` 已由同一个 `physical_skeleton_follow_through.active_path_scan_no_legacy_default_caller` 注入并返回 `passed`，不再是 `not_available`。这说明 MAG consumer thinning contract 与真实 active-path scan 语义归位；它仍只证明 repo-local legacy default caller 未复活，不替代 production/default caller 或 Temporal soak 证据。

8. `stale_retire_generic_runtime_worktree_closeout`
   2026-05-19 fresh audit 读取了 `main`、`.worktrees/retire-generic-runtime-surfaces` 和 `codex/retire-mag-generic-runtime-surfaces`。该分支 `fd48dc6` 已是当前 `main` 的祖先；旧 worktree 的 dirty cleanup 与当前 `main` 的 `7d877b8 Retire MAG local runtime surfaces` 重叠，最终树相对 `main` 只剩 `io.py` 空行和 `tests/conftest.py` 类型标注差异。重放旧分支会重新引入 `upstream_hermes.py`、`test_local_runtime.py`、`test_upstream_hermes.py`，并反向破坏当前 `stage_control_plane` refs 口径，因此该 lane 的正确动作是清理 stale worktree / branch，而不是合并。

9. `current_private_surface_classification`
   当前 MAG 私有功能面分类按 active source 与 machine audit 读取：runtime registration、task lifecycle、source intake 是 declarative grant pack input；lifecycle adapter、observability、sidecar/product status、package lifecycle、human workbench / scheduler metadata 是 refs-only adapter；fundability / quality / export verdict、package authority、transition oracle、owner receipt、memory accept/reject 和 grant helper 是 MAG minimal authority；旧 Hermes/Gateway/local-manager、local journal / attempt ledger、flat shell alias、compat aggregate test 和 repo-owned scheduler / daemon 是 legacy proof tombstone。该分类不允许把 refs-only adapter 再扩写成 MAG-owned generic runtime。

## Retained Private Authority Surfaces

MAG 只允许保留 grant domain 的 minimal authority surfaces；旧 `function_id` 是兼容字段，不代表由 Python 函数直接裁决：

| Authority surface | Work mode | Judgment owner | 程序角色 |
| --- | --- | --- | --- |
| `fundability_verdict` | AI-first judgment | grant-review / fundability stage artifact 判断 call fit、applicant evidence 和 reviewer risk。 | validator / verdict ref materializer |
| `quality_verdict` | AI-first judgment | AI-authored critique、quality closure dossier 或 reviewer artifact；scorecard 不能单独给出 ready。 | aggregator / guard |
| `export_verdict` | AI-first judgment | package/export stage artifact；artifact existence 或 generic lifecycle completion 不能声明 submission-ready。 | package gate ref validator |
| `memory_accept_reject` | AI-first judgment | grant strategy memory stage 判断 memory 对 fundability / quality 的意义。 | receipt writer / refs projection |
| `package_authority` | Programmatic guard | MAG owner receipt 或 package stage authority。 | materializer / receipt signer |
| `owner_receipt_signer` | Programmatic guard | MAG receipt schema 与 domain provenance。 | receipt signer |
| `grant_helper` | Programmatic guard | deterministic grant metadata、route 和 blocker policy。 | helper implementation / guard |

AI-first 边界统一写法：Codex CLI critique executor 或显式 hosted/proof critique executor 可以产出 AI-authored review artifact；程序只能验证和投影这些 artifact，不用机械 quality score、schema completeness、controller route 或 fixed branch 替代 grant reviewer 判断。

## 当前测试/证据差距

## 当前物理源码形态差距

这部分是 physical morphology hygiene tail，不能被 `mag_functional_structure_gap_count=0` 或 OPL cleanup ledger apply/verify 写成已经完成。

- `product_entry_parts/*`、product status、grant progress / cockpit / direct-entry / user-loop 与 sidecar export 仍是 repo-local wrapper 形态；目标是 OPL generated product/status/workbench/sidecar shell 成为 production/default caller，MAG 只保留 grant handler target、receipt signer、typed blocker、verdict refs 与 safe action metadata。
- `domain_runtime_parts/substrate.py`、`domain_entry.py` 和 grouped CLI command catalog 仍容易被读成 MAG runtime substrate；目标是把 domain runtime 口径降为 route/authority adapter 和 regression oracle，不持有 generic runner、queue、attempt ledger 或 session shell。
- `runtime_registration.py`、`control_plane.py`、lifecycle receipt bundle、memory/package projection 和 owner receipt helper 只允许输出 body-free refs、receipt、typed blocker 或 action metadata；目标是 OPL lifecycle/session/workbench caller 稳定后迁出 generic envelope。
- `grant_autonomy_controller.py` 只能作为 grant route / budget / blocker policy 的 domain controller，不得变成 MAG-owned long-running runtime loop；质量/fundability/export 判断必须来自 AI-first grant stage artifact。

关闭门槛是：external evidence request pack 被 OPL/App/production caller 消费，direct/hosted parity 与 no-forbidden-write 持续成立，MAG owner receipt / typed blocker roundtrip 可重复，active caller 迁移后不保留 compatibility alias。

以下是结构边界正确后的证据门，不能反向重开 MAG repo 侧 active bridge exit：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected grant strategy memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App shell 真实消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- external production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 证据。
- Temporal provider long SLO、repair cadence 和 live receipt reconciliation。

这些 evidence gate 的 repo-local request surface 已落地为 `mag.external_evidence_request_pack.v1`；生产可用 acceptance tail 的 MAG-owned 记录已落地为 `contracts/production_acceptance/mag-production-acceptance.json`。后续关闭或继续阻塞必须来自真实 owner receipt、typed blocker 或 no-regression evidence refs；MAG 仓不生成替代 runtime proof，OPL/provider completion 也不授权 fundability-ready。

Legacy cleanup gate 的 repo-local proof surface 已可被 OPL dry-run / apply / verify 消费，并已写入 OPL refs-only cleanup ledger。后续若涉及物理删除，只能由 MAG owner receipt 证明；OPL 不能替 MAG 删除 grant repo 文件或宣布 grant readiness。

## 完善顺序

1. `consume_external_evidence_request_pack`
   OPL/App/production caller 从 `/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack` 读取 request ids、required refs 和 required receipt shapes，并返回 body-free receipts / typed blockers / no-regression evidence。

2. `external_production_consumption_evidence`
   从 OPL/App/production caller 侧拿到真实消费 MAG declarative pack、domain handler target、owner receipt / typed blocker refs、no-forbidden-write 和 direct/hosted parity 的持续证据。

3. `real_workspace_receipt_scaleout`
   推进真实 grant-stage attempt、memory/package/lifecycle receipt、continuous receipt reconciliation、cleanup/restore/retention 和 provider SLO long soak。

   当前 production acceptance surface 已把该项收为 `domain_owned_typed_blocker_with_next_verification_ref`。下一步按 `contracts/production_acceptance/mag-production-acceptance.json` 中的 `next_verification_command_refs` 继续验证 owner receipt / typed blocker / no-regression evidence，而不是把它计为结构差距。

4. `private_authority_ai_first_guard`
   审计 retained authority surfaces，确保 fundability / quality / export / memory accept-reject 的判断都来自 AI-first stage output，package / receipt / helper 只做 programmatic guard，代码只做 validator、materializer、receipt signer、guard 和 refs projection。

5. `physical_source_morphology_hygiene`
   继续把 active source 中带 runtime / product-entry / sidecar / lifecycle / workbench / scheduler 语义的模块保持在 domain handler、refs-only adapter、minimal authority function 或 history/tombstone 角色；优先治理 `domain_runtime_parts/substrate.py`、`product_entry_parts/*`、`runtime_registration.py`、`control_plane.py`、owner receipt helper、grouped CLI wrapper 和 autonomy controller 的平台化命名。新增代码默认进入 `agent/` pack、`contracts/`、authority function 或 domain handler，不重建本地 runtime/journal/attempt ledger，不新增 compatibility facade。

## 当前不能写成

- 不能写成 OPL provider completion、receipt reconciliation proof 或 no-regression evidence 等于 fundability-ready、quality-ready、export-ready 或 production long-run soak。
- 不能写成 MAG 已经是纯知识文件仓；MAG 仍持有 grant authority functions、domain entry、receipt schema/writer、transition oracle、quality/export verdict、package authority、memory accept/reject 和 focused contract tests。
- 不能把 `mag_functional_structure_gap_count=0` 写成 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 quality scorecard、schema completeness、controller route、package existence 或 mechanical projection 写成 AI-first grant quality / fundability / export verdict。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。
- 不能把 MAG legacy cleanup dry-run / apply / verify ready 写成 external production/default caller、真实 App/workbench consumption、grant readiness 或 production long-run soak 已完成。
- 不能为了兼容保留旧模块、旧接口、旧测试、旧 CLI alias、facade 或 wrapper；active caller 迁走后直接删除或进入 history/tombstone。
