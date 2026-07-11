# 架构

Owner: `Med Auto Grant`
Purpose: `system_structure_and_owner_boundary`
State: `current`
Machine boundary: 本文是人读架构说明。机器接口归 root contracts、schemas、source、CLI/API behavior、runtime receipts、workspace/artifact roots 与 `contracts/runtime-program/current-program.json`。

## 总体流

`User/Codex -> OPL generated caller or medautogrant CLI -> MedAutoGrantDomainEntry -> MAG domain action/authority function -> workspace artifact or runtime receipt ref`

OPL 负责运行和投影，MAG 负责 grant 判断与交付 authority。两条入口不得形成第二份 route、quality、package 或 receipt truth。

Framework Python helper 由 OPL module workflow 通过 `opl_framework` namespace 托管。MAG 只使用该 namespace，不在 manifest / lock 中声明、安装或锁定 OPL implementation；构建配置只收集 `med_autogrant*`，不把 carrier vendoring 进 MAG wheel。非默认 executor 的 request transport 直接调用 `opl_framework.executor_client.run_agent_execution_request`；临时 request、`opl executor run --request` 子进程、timeout/process cleanup 和 JSON receipt envelope 校验全部归 OPL，MAG 不再持有 adapter 或 command override。

## 声明式 Agent Pack

`agent/` 持有 stages、prompts、skills、knowledge 与 quality gates。`agent/stages/manifest.json`、`contracts/pack_compiler_input.json`、`contracts/action_catalog.json` 和 `contracts/functional_privatization_audit.json` 是 OPL 可消费的机器输入；OPL Pack 将 stage source 投影到 `opl_generated:product_entry_manifest#/family_stage_control_plane/stages`，MAG 不再 tracked 生成后的 stage control plane。

MAG 不再内置私有 standard-pack compiler、source scanner、generated product builder 或 consumer-thinning platform。OPL 通过 canonical conformance scanner读取 pack 与 source boundary。

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
| `grant_native_helper` | 无法声明化的 grant-native prompt、answer validation、direct CLI/domain-handler adapter；generic executor transport 不在本仓 |

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
