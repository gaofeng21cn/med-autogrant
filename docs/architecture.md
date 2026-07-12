# 架构

Owner: `Med Auto Grant`
Purpose: `system_structure_and_owner_boundary`
State: `current`
Machine boundary: 本文是人读架构说明。机器接口归 root contracts、schemas、source、CLI/API behavior、runtime receipts、workspace/artifact roots 与 `contracts/runtime-program/current-program.json`。

## 总体流

`User/Codex -> OPL generated caller or medautogrant CLI -> MedAutoGrantDomainEntry -> MAG domain action/authority function -> workspace artifact or runtime receipt ref`

OPL 负责运行和投影，MAG 负责 grant 判断与交付 authority。两条入口不得形成第二份 route、quality、package 或 receipt truth。

`contracts/domain_descriptor.json#/standard_agent_interface` 是 MAG 交给 OPL hosted surface 的唯一接口声明：workspace 只声明 `input_path` locator 与 grant topology；runtime 只声明 direct domain-handler argv 和 registration ref；progress alias 与 Atlas routing signal 继续归 MAG。product status/manifest command 明确为 `null`，因为它们由 OPL generated surface 承担，不在 MAG 恢复私有 materializer。OPL 必须通过 package currentness 消费该 descriptor；显式 checkout 只作开发验证 fallback。

Framework Python helper 由 OPL module workflow 通过 `opl_framework` namespace 托管。MAG 只使用该 namespace，不在 manifest / lock 中声明、安装或锁定 OPL implementation；构建配置只收集 `med_autogrant*`，不把 carrier vendoring 进 MAG wheel。所有 executor kind 的 request transport 都调用 `opl_framework.executor_client.run_agent_execution_request`；临时 request、`opl executor run --request`、Codex/其他 executor 子进程、timeout/process cleanup 和 receipt envelope 校验全部归 OPL。MAG 只构造 grant prompt/domain payload，并解析 typed MAG closeout。

## 声明式 Agent Pack

`agent/` 持有 stages、prompts、skills、knowledge 与 quality gates。`agent/stages/manifest.json`、`contracts/pack_compiler_input.json`、`contracts/action_catalog.json` 和 `contracts/functional_privatization_audit.json` 是 OPL 可消费的机器输入；OPL Pack 将 stage source 投影到 `opl_generated:product_entry_manifest#/family_stage_control_plane/stages`，MAG 不再 tracked 生成后的 stage control plane。

MAG 不再内置私有 standard-pack compiler、source scanner、generated product builder 或 consumer-thinning platform。OPL 通过 canonical conformance scanner读取 pack 与 source boundary。

六个 Stage prompt 只保留本 Stage 的目标、好结果、专业依赖、authority/证据边界与 closeout 形状。方向、科学问题、论证与申请人 fit 是同一 grant strategy 内可迭代收敛的专业判断；默认 `execute-strategy-authoring-pass` 在一个 attempt 内用一次 Codex invocation 共同产出 direction/question/argument/fit/outline/draft，再由 deterministic contract projection 物化六个 checkpoint，原子 pass 只用于定点 route-back。receipt 中的 invocation count 只是本次观测 telemetry，不是成功条件或全局调用上限；解析失败、provider/attempt retry、review feedback 与 route-back 仍可触发后续调用。历史 `*_frozen` workspace 字段表示可引用 checkpoint，不规定 Codex 的认知顺序或调用次数。提纲是长文写作的强默认，只有明确人工批准才形成不可静默改写的批准合同。

真实 Codex caller 继续使用 schema-backed closeout packet 和已知 object refs，但不再规定 significance-first 全局写作顺序、固定候选数量或按 rubric 权重遍历的审阅顺序。Critique 必须基于真实 draft 独立完成；revision 后按影响范围复审。Schema 中保留的 profile weight 字段只保证既有 workspace 报告兼容，不作为推理顺序或质量裁决算法。

## Domain Handler

`domain-handler export` 输出：

- body-free workspace identity 与 locator
- action catalog contract
- declarative stage manifest ref 与 OPL generated stage-plane locator
- owner receipt contract
- 三项 allowed action
- generated surface handoff ref
- 八项 minimal authority function refs
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
| `grant_transition_oracle` | grant stage transition recommendation |
| `grant_native_helper` | 无法声明化的 grant-native prompt、typed closeout/answer validation、direct CLI/domain-handler adapter；任何 executor transport 均不在本仓 |

这八项 ID 必须在 functional audit、pack compiler input、current-program 和 domain handler export 中一致。

`grant_transition_oracle` 返回的 `runner_contract_ref` 指向 OPL-owned
`contracts/opl-framework/family-transition-runner-contract.json`。这是跨仓 owner locator，
不是 MAG 应复制或本地解析的 contract；MAG 只生成 grant-native transition recommendation，
OPL StageRun 持有 cycle、rollback、dispatch、replay 与 output orchestration。

## OPL-owned Surfaces

- Temporal/provider runtime 与 stage attempt lifecycle
- executor request transport、timeout/process cleanup 与 receipt envelope 校验
- Agent Package / Codex plugin install、update、remove 与 marketplace/symlink lifecycle
- scheduler、queue、retry、resume、dead-letter 与 attempt ledger
- workspace/source intake shell、artifact locator/index 与 lifecycle transport
- generated product/status/user-loop/workbench/CLI/MCP descriptors
- operator projection、observability 与 cross-agent handoff

OPL 可以记录和投影 MAG refs，但不能签发 MAG receipt、生成 verdict、写 grant truth 或绕过 human gate。

## Plugin Lifecycle

MAG 只跟踪 `plugins/med-autogrant/` carrier source 和 `contracts/opl_agent_package_manifest.json` package declaration。安装、更新和移除分别通过 `opl connect install/update/remove --module medautogrant` 完成；本仓不再提供 installer、marketplace 清理器、用户目录 symlink mutation 或 fallback。

## 数据与状态

开发 checkout 只保存 source、docs、schemas/contracts、descriptor 与 refs。真实 workspace、artifact/package body、receipt instance、cache 和 runtime reports 写入 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

`grant_run_id`、`workspace_id`、`draft_id`、`program_id` 必须分离。OPL stage state 与 MAG workspace lifecycle observation 也必须分离。

## Currentness 与 Readiness

结构 currentness 由 OPL canonical command验证：

`<one-person-lab-repo>/bin/opl agents conformance --agent mag=<med-autogrant-repo> --json`

必须满足 overall structural status passed、source `matched_source_behavior_count=0`、blockers empty；allowed matches 只能是逐文件 authority/adapter 覆盖。

这不证明 live grant progress、owner acceptance、quality/export ready、submission human gate、provider long soak 或 production readiness。对应真相继续归 live progress contract、workspace artifacts 和 owner receipts。
