# 架构

Owner: `Med Auto Grant`
Purpose: `system_structure_and_owner_boundary`
State: `current`
Machine boundary: 本文是人读架构说明。机器接口归 root contracts、schemas、source、CLI/API behavior、runtime receipts、workspace/artifact roots 与 `contracts/runtime-program/current-program.json`。

## 总体流

`User/Codex -> OPL generated caller or medautogrant CLI -> declarative parser + explicit static dispatch -> MAG domain action/authority function -> workspace artifact or runtime receipt ref`

OPL 负责运行和投影，MAG 负责 grant 判断与交付 authority。两条入口不得形成第二份 route、quality、package 或 receipt truth。

`contracts/domain_descriptor.json#/standard_agent_interface` 是 MAG 交给 OPL hosted surface 的唯一差异接口：workspace 只声明 `input_path` locator 与 grant topology；runtime 只声明 domain identity 和 registration ref；progress alias 与显式 routing signal 继续归 MAG。`workspace_binding.entry_command_template`、`workspace_binding.manifest_command_template` 与 `runtime.dispatch_command` 已退出 closed interface，OPL 不从 descriptor 恢复任何 MAG 私有命令模板。OPL 必须通过 package currentness 消费该 descriptor；显式 checkout 只作开发验证 fallback。

Framework Python helper 由 OPL module workflow 通过 `opl_framework` namespace 托管。MAG 只使用该 namespace，不在 manifest / lock 中声明、安装或锁定 OPL implementation；构建配置只收集 `med_autogrant*`，不把 carrier vendoring 进 MAG wheel。所有 executor kind 的 request transport 都调用 `opl_framework.executor_client.run_agent_execution_request`；临时 request、`opl executor run --request`、Codex/其他 executor 子进程、timeout/process cleanup 和 receipt envelope 校验全部归 OPL。MAG 只构造 grant prompt/domain payload，并解析 typed MAG closeout。

Funding source 的通用 HTTPS transport 同样归 OPL：MAG 通过 `opl_framework.source_transport.fetch_text` 使用 fail-closed HTTPS、redirect allowlist、timeout、header 与 decode 语义；MAG 只持有 NIH/NSFC 三个官方 URL 的 exact allowlist、funding-specific User-Agent 和 HTML 解析/领域 provenance，不保留 `urllib` transport 或第二套网络策略。

## 声明式 Agent Pack

`agent/` 持有 stages、prompts、skills、knowledge 与 quality gates。`agent/stages/manifest.json`、`contracts/pack_compiler_input.json`、closed `contracts/action_catalog.json` v2、`contracts/domain_handler_registry.json`、`contracts/source_closure_audit.json` 和 `contracts/functional_privatization_audit.json` 是 OPL 可消费的机器输入；OPL Pack 将 stage source 投影到 `opl_generated:product_entry_manifest#/family_stage_control_plane/stages`，MAG 不再 tracked 生成后的 stage control plane。

MAG 的 public hosted action 只保留 `open_grant_user_loop`、`build_direct_entry`、`build_submission_ready_package`，三者都以 `stage_binding` 指向 canonical stage manifest，并使用 action-specific closed input schema。OPL 统一生成 CLI、MCP、Skill、OpenAI、AI SDK、product entry、status 和 workbench surface；canonical hosted command 是 `opl agents run --domain med-autogrant --action <action_id> --workspace <absolute_path>`。Progress 与 cockpit 是 OPL generated read model，不是 MAG action catalog 中的第二组 read-only action。

MAG 不再内置私有 standard-pack compiler、source scanner、generated product builder 或 consumer-thinning platform。OPL 通过 canonical conformance scanner读取 pack 与 source boundary。

六个 Stage prompt 只保留本 Stage 的目标、好结果、专业依赖、authority/证据边界与 closeout 形状。方向、科学问题、论证与申请人 fit 是同一 grant strategy 内可迭代收敛的专业判断；默认 `execute-strategy-authoring-pass` 在一个 attempt 内用一次 Codex invocation 共同产出 direction/question/argument/fit/outline/draft，再由 deterministic contract projection 物化六个 checkpoint，原子 pass 只用于定点 route-back。receipt 中的 invocation count 只是本次观测 telemetry，不是成功条件或全局调用上限；解析失败、provider/attempt retry、review feedback 与 route-back 仍可触发后续调用。历史 `*_frozen` workspace 字段表示可引用 checkpoint，不规定 Codex 的认知顺序或调用次数。提纲是长文写作的强默认，只有明确人工批准才形成不可静默改写的批准合同。

真实 Codex caller 继续使用 schema-backed closeout packet 和已知 object refs，但不再规定 significance-first 全局写作顺序、固定候选数量或按 rubric 权重遍历的审阅顺序。Critique 必须基于真实 draft 独立完成；revision 后按影响范围复审。Schema 中保留的 profile weight 字段只保证既有 workspace 报告兼容，不作为推理顺序或质量裁决算法。

## Domain Handler

Repo-local CLI 的 command specs 只声明 help、required/optional/exclusive fields；argparse 不注入 callable handler。解析后的 command 由 `dispatch_cli_command` 与 `dispatch_domain_request` 显式静态分支到具体 authority/runtime function，command catalog 中不保存 `runtime_method`，执行路径不使用 `getattr` 或字符串反射。

`domain-handler export` 输出：

- body-free workspace identity 与 locator
- action catalog contract
- declarative stage manifest ref 与 OPL generated stage-plane locator
- owner receipt contract
- 三项 public hosted stage action 与三项 direct-handler allowed dispatch action
- generated surface handoff ref
- 七项 minimal authority function refs
- caller 与 false-authority boundary

它不包含 grant、memory、artifact 或 package body。

`domain-handler dispatch` 只执行：

- `domain-memory/propose`
- `domain-memory/decide`
- `stage-attempt/closeout`

它不提供 status/session/runtime/lifecycle/workbench/closeout bundle 通用壳。

## MAG Authority

| Authority id | 实现边界 |
| --- | --- |
| `fundability_verdict` | funding call 与 proposal fundability 判断 |
| `quality_verdict` | authoring/review quality 判断 |
| `export_verdict` | submission/export fail-closed 判断 |
| `package_authority` | final package body 与 identity authority |
| `memory_accept_reject` | grant strategy memory 提案接受/拒绝 |
| `owner_receipt_signer` | domain owner receipt / typed blocker / no-regression evidence |
| `grant_native_helper` | 无法声明化的 grant-native prompt、typed closeout/answer validation、direct CLI/domain-handler adapter；validation finding 是 Codex input/质量债，不是 stage progression 控制面；任何 executor transport 均不在本仓 |

这七项 ID 必须在 functional audit、pack compiler input、current-program 和 domain handler export 中一致。`ai_route_policy` 只投影 declared stage/action scope；`semantic_route_decision_owner=decisive_codex_attempt` 负责语义 route，`stage_transition_materialization_owner=opl_stage_run_controller` 只校验角色、shape 与 declared target 并物化 transition。

## OPL-owned Surfaces

- Temporal/provider runtime 与 stage attempt lifecycle
- executor request transport、timeout/process cleanup 与 receipt envelope 校验
- fail-closed HTTPS source transport、redirect/allowlist enforcement 与 text decode
- Agent Package / Codex plugin install、update、remove 与 marketplace/symlink lifecycle
- scheduler、queue、retry、resume、dead-letter 与 attempt ledger
- workspace/source intake shell、artifact locator/index 与 lifecycle transport
- generated product/status/user-loop/workbench/CLI/MCP descriptors
- operator projection、observability 与 cross-agent handoff

OPL 可以记录和投影 MAG refs，但不能签发 MAG receipt、生成 verdict、写 grant truth 或绕过 human gate。

## Plugin Lifecycle

MAG 只跟踪 `plugins/med-autogrant/` carrier source 和 `contracts/opl_agent_package_manifest.json` package declaration。公共 lifecycle 由 OPL Packages 持有：`opl packages install mag`、`opl packages update mag`、`opl packages uninstall mag`；`medautogrant` 只是 managed runtime source module locator。MAG 不再提供 installer、marketplace 清理器、用户目录 symlink mutation 或 fallback。

## 数据与状态

开发 checkout 只保存 source、docs、schemas/contracts、descriptor 与 refs。真实 workspace、artifact/package body、receipt instance、cache 和 runtime reports 写入 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

`grant_run_id`、`workspace_id`、`draft_id`、`program_id` 必须分离。OPL stage state 与 MAG workspace lifecycle observation 也必须分离。

## Currentness 与 Readiness

结构 currentness 由 OPL canonical command验证：

```bash
<one-person-lab-repo>/bin/opl agents scaffold --validate <med-autogrant-repo> --json
<one-person-lab-repo>/bin/opl agents interfaces --repo-dir <med-autogrant-repo> --json
<one-person-lab-repo>/bin/opl agents source-closure --agent mag=<med-autogrant-repo> --json
<one-person-lab-repo>/bin/opl agents conformance --agent mag=<med-autogrant-repo> --json
```

必须满足 scaffold passed、interfaces ready、source closure passed、overall structural status passed 与 blockers empty；sensitive effects 只能由逐 symbol exact audit覆盖，unresolved/private generic/unreachable sensitive/audit mismatch 必须为 `0`。

这不证明 live grant progress、owner acceptance、quality/export ready、submission human gate、provider long soak 或 production readiness。对应真相继续归 live progress contract、workspace artifacts 和 owner receipts。

## Stage Review 与 Meta Review

MAG 绑定 `official_high_value_knowledge_deliverable.v1`。每个 AI producer Stage 在同一 StageRun 下使用相互隔离的 producer、reviewer、repairer、re-reviewer Attempts；每个 Attempt 对应新的 Codex thread。同一 thread 内的写后检查只是 `in_thread_refinement`，缺 typed closeout 时的 resume 也只补协议，二者都不能产生 Review receipt。

Formal Review StageRun 的 decisive route owner 是 terminal reviewer/re-reviewer；仅在这种 StageRun 内，producer 与 repairer 始终只能给 route recommendation。`same_stage_repair_required` 在 repair budget 尚存时也只能 recommendation并继续本 Stage 质量循环；若最窄 canonical owner 是另一个 declared Stage，`cross_stage_route_back_before_budget_exhaustion` 允许 reviewer/re-reviewer 提前以 `repair_required + route_back` 成为 terminal decisive Attempt，且这是预算耗尽前唯一允许的终局 `repair_required` route。预算耗尽且 exact artifact 可消费时，它保留 `repair_required` outcome、成为 terminal decisive Attempt并返回 `route_impact.stage_route_decision`，controller 物化 transition 并投影 `completed_with_quality_debt`。Primary-only 的 `review_and_rebuttal` Meta Review 由其 producer 直接输出 `route_impact.stage_route_decision`。OPL 不替代 MAG 的 grant-semantic judgment，也不从 transition materialization 获得领域批准权。

`review_and_rebuttal` 保留稳定 Stage ID，但承担独立 Grant Meta Review：它只消费 exact artifact/hash、Stage Review receipts、call/source/rubric 与必要 lineage，输出整体 verdict 和 defect-owner route-back，不在 Review Stage 内改写 proposal。可消费 artifact 在三轮质量预算耗尽后带质量债推进；债务继续阻止 quality、export、submission 和 ready 声明。

`package_and_submit_ready` 的四份 final bytes 始终先作为 `submission_ready=false` 候选输出。StageRunController 只能物化绑定 exact hashes 的 `opl_stage_review_receipt`；最终本地 submission-ready 投影必须同时消费该 receipt 与 MAG-owned export/owner verdict。Reviewer 与 OPL 都不能签 MAG owner receipt，外部 portal acceptance 继续是独立 human gate。
