# 不变量

Owner: `Med Auto Grant`
Purpose: `stable_invariants`
State: `current`
Machine boundary: 本文是人读约束集。可执行约束归 contracts、schemas、source、CLI/API behavior、验证命令、runtime receipts 与 workspace/artifact outputs。

## 身份与入口

- OPL canonical agent id 与 OPL Agent Package id 都是 `mag`，kind 固定为 `agent`；唯一
  OCI Package repository 是 `ghcr.io/gaofeng21cn/one-person-lab-packages/mag`，MAG
  owner 只推进自己的 `latest-stable`。`med-autogrant` 是 repo、Python distribution 与
  plugin/skill carrier locator，`medautogrant` 是 module/CLI locator。载体名不得注册为
  第二个 package identity 或 OCI package coordinate。
- 正式 repo-local entry 是 `medautogrant` CLI、`MedAutoGrantDomainEntry` 和 direct domain handler。
- CLI command metadata 只声明 parser 字段；执行必须走显式静态 dispatch，不得向 argparse 注入 callable handler，不得在 command spec保存 runtime method，也不得使用 `getattr`/字符串反射执行命令。
- `MCP` 仍是 `descriptor_only=true`、`public_runtime=false` 的协议投影，不是当前 public runtime。
- 不恢复 `mag` console script、旧 flat command、wrapper、facade 或 compatibility alias。

## Authority

- MAG 只保留七项 canonical authority ID；`ai_route_policy` 不是 authority function。ID 集合不得在 audit、pack、current-program 与 handler export 间漂移。
- OPL/provider completion、schema completeness、generated surface、测试或 package 文件存在都不能替代 MAG verdict、receipt 或 human gate。
- Owner receipt class 固定为 `domain_owner_receipt`、`typed_blocker`、`no_regression_evidence`。
- Domain handler dispatch 只允许三项 action；新增 action 必须先证明属于 MAG authority，而非 generic platform shell。
- `agent/stages/manifest.json` 只声明 stage scope。`semantic_route_decision_owner=decisive_codex_attempt` 选择前进、重复、跳过或 route-back 到任一 declared stage；`stage_transition_materialization_owner=opl_stage_run_controller` 只校验并物化 transition。静态 transition table、oracle fixture、program guard 或 controller 不得成为 grant-semantic route authority。
- Stage Pack v2 的 manifest allow-list、closed action catalog 与 pack input 必须保持 parity。每个 public hosted action 必须使用 exact `stage_binding`，其 `stage_route` 精确覆盖 manifest 中声明该 action 的 Stage，并按 `next_stage_refs` 排序；progress/cockpit 观察面归 OPL generated read model，不得作为 MAG read-only action 回流 Stage allow-list。
- Human gate closeout 使用 OPL 标准 `completed_and_wait_owner` + `human_gate_ref`；`typed_blocker_ref` 只用于真实语义或 authority 缺口，不能包装等待人类决定或 portal 操作。
- Workspace route recommendation 同样遵守该语义：人工决定返回 `human_gate_ref`，普通 repair/rollback 返回 `route_back_ref`。

## OPL 边界

- Generic runtime、scheduler、queue、attempt ledger、session、lifecycle transport、generated product shell 与 workbench 归 OPL。
- Standard Agent interface 不得恢复 `entry_command_template`、`manifest_command_template` 或 `runtime.dispatch_command`；hosted execution 统一由 OPL 从 action catalog v2生成。
- MAG owner 持有 executor-neutral Package identity、capability/dependency intent、grant
  business task 与 typed views；App、Framework、carrier 与 executor 不得复制这些
  authority。
- Required/optional Package 依赖只以 identity presence 与 callability 判断。普通
  composition/readiness 不得要求版本范围、ABI、lock、payload、digest、atomic closure、
  shared Release Set 或跨 Package 版本求解。
- 公共 install/update/uninstall 入口固定为 `opl packages ...` 聚合动作，不得回退到
  `opl connect ... --module medautogrant`；动作实现委托实际 carrier，Framework 不保存
  第二份 currentness 或完整 installed truth。
- Codex Plugin 只投影 Plugin/config/cache。完整 MAG runtime 必须由所有实际 carrier 的
  fresh readback共同证明；切换 executor 不得重装 Package 或丢失偏好、grant task、
  dependency 和 typed view。
- 通用 source fetch 必须调用 OPL fail-closed HTTPS transport；MAG 只持有 exact official URL allowlist和领域解析语义，不得恢复私有 `urllib` transport、宽泛 origin放行或 fallback downloader。
- MAG 不写 OPL stage attempt/current/terminal state，不拥有 Temporal worker，也不把 bounded controller 扩成 durable loop。
- Generated caller 只能回到 MAG action target；不能读取 grant/memory/artifact/package body。

## Source 与状态

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer。
- 开发 checkout 不保存 runtime artifact、receipt instance、workspace body、package body、venv 或 cache。
- `src/` 只允许 domain entry、authority function、refs-only adapter 与 grant-native helper；无 caller 的平台壳直接删除。
- 历史路径只在 `docs/history/**`、明确 provenance 或 negative guard 中出现，不作为兼容承诺。
- Exact ref/digest 只约束单次 OPL release artifact 或 MAG submission artifact integrity，
  不成为日常 Package composition/readiness 门。

## 验证

- 默认入口是 `scripts/verify.sh`；`full` 运行完整 repo suite。
- Python/pytest 必须经 clean runner，避免把 cache/venv/bytecode 写回 checkout。
- 结构 source gate 使用 OPL canonical conformance scanner，不再维护 MAG 私有 source-purity wrapper。
- 测试只固定可观察 behavior、authority 和 fail-closed contract，不固定 MRO、`__module__`、源码文件位置、wrapper 存在或文档措辞。

## 证据边界

- Live progress、quality/export、human gate、long soak、owner acceptance 与 production status 必须由对应 live/readback/receipt 证明。
- Production acceptance contract 是 provenance，不是 live closing ref；`domain_owned_closing_ref` 为空时不得写成完成。
- 文档、focused tests、conformance pass 和 refs-only ledger 不能单独支撑 readiness claim。
- 正式 Stage Review 必须来自新的 StageAttempt 和新的 executor session；producer self-check、same-thread resume 或无 exact artifact identity/hash locator 的记录不能算 Review。Hash 不构成 content authority，也不能单独判定 epistemic evidence stale。
- `review_and_rebuttal` Meta Review 不继承上游生成对话，也不内联修稿；它必须把缺陷路由到最早能关闭根因的 Stage，并在新 generation 后重新审查。
- `package_and_submit_ready` 必须把四个 canonical package artifacts 的 exact refs/hash 交给 fresh Reviewer 作为 identity/release-integrity input，并按 `contracts/epistemic_review_scope_profile.json` 只复审 stale dependency scopes；producer/helper 结果固定为 `submission_ready=false` 候选，不能投影 terminal `submission_ready`。Governance metadata、layout 或 package-only delta 不得自动失效 content/methodology/reference evidence。本 Stage 只修 assembly、manifest 与 provenance projection，其余缺陷 route-back，外部 portal acceptance 保持 human-owned。
- StageRunController 只能物化绑定所审 scope artifact identity 的 `opl_stage_review_receipt`；无关 package hash 单独变化不失效该 receipt，但其所审 artifact identity 变化必须失效。任何本地 submission-ready 投影仍须同时消费 current scoped evidence、匹配当前 package hashes 的独立 exact-byte release integrity 与 MAG-owned export/owner verdict；reviewer 与 OPL 均不得签 MAG owner receipt 或授权 export/submission readiness。
- Reviewer 与 re-reviewer Attempt 只通过 `route_impact.stage_quality_cycle.outcome` 返回 `pass|repair_required|quality_debt|blocked|human_gate`。Attempt 不得输出 receipt `verdict`；StageRunController 将前三者同名映射，并将 `blocked|human_gate` 映射为 receipt `hard_stop`。
- Formal Review StageRun 中只有 terminal reviewer/re-reviewer 能输出 `route_impact.stage_route_decision`；在这种 StageRun 内 producer、repairer 始终只能输出 `stage_route_recommendation`，但 primary-only StageRun 的 producer可以成为 decisive Attempt。`same_stage_repair_required` 且 budget 尚存时，reviewer/re-reviewer 也只 recommendation并继续本 Stage；仅当最窄 canonical owner 是另一个 declared Stage 时，`cross_stage_route_back_before_budget_exhaustion` 才允许它提前输出 `repair_required + stage_route_decision(decision_kind=route_back)`，其他预算耗尽前终局 route 一律禁止。预算耗尽且 exact artifact 可消费时，`repair_required` reviewer/re-reviewer 是 terminal decisive Attempt；hard boundary 或零可消费 artifact 不输出 route。Attempt 不直接物化 transition 或 Review receipt，旧 route closeout 字段不得使用。
