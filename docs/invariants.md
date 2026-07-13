# 不变量

Owner: `Med Auto Grant`
Purpose: `stable_invariants`
State: `current`
Machine boundary: 本文是人读约束集。可执行约束归 contracts、schemas、source、CLI/API behavior、验证命令、runtime receipts 与 workspace/artifact outputs。

## 身份与入口

- OPL canonical agent id 与 OPL Agent Package id 都是 `mag`，唯一 OCI Package repository 是 `ghcr.io/gaofeng21cn/one-person-lab-packages/mag`；`med-autogrant` 是 repo、Python distribution 与 plugin/skill carrier locator，`medautogrant` 是 module/CLI locator。载体名不得注册为第二个 package identity 或 OCI package coordinate。
- 正式 repo-local entry 是 `medautogrant` CLI、`MedAutoGrantDomainEntry` 和 direct domain handler。
- `MCP` 仍是 `descriptor_only=true`、`public_runtime=false` 的协议投影，不是当前 public runtime。
- 不恢复 `mag` console script、旧 flat command、wrapper、facade 或 compatibility alias。

## Authority

- MAG 只保留八项 canonical authority ID；ID 集合不得在 audit、pack、current-program 与 handler export 间漂移。
- OPL/provider completion、schema completeness、generated surface、测试或 package 文件存在都不能替代 MAG verdict、receipt 或 human gate。
- Owner receipt class 固定为 `domain_owner_receipt`、`typed_blocker`、`no_regression_evidence`。
- Domain handler dispatch 只允许三项 action；新增 action 必须先证明属于 MAG authority，而非 generic platform shell。
- `agent/stages/manifest.json` 只声明 stage scope；Codex CLI 选择前进、重复、跳过或 route-back 到任一 declared stage。静态 transition table、oracle fixture 或 program guard 不得成为 route authority。
- Stage Pack v2 的 manifest allow-list、action catalog 与 pack input 必须保持 parity。Mutating action 的 `stage_route` 精确覆盖 manifest 中声明该 action 的 Stage，并按 `next_stage_refs` 排序；read-only action 不声明执行 route，观察范围继续由 `allowed_action_refs` 表达。
- Human gate closeout 使用 OPL 标准 `completed_and_wait_owner` + `human_gate_ref`；`typed_blocker_ref` 只用于真实语义或 authority 缺口，不能包装等待人类决定或 portal 操作。
- Workspace route recommendation 同样遵守该语义：人工决定返回 `human_gate_ref`，普通 repair/rollback 返回 `route_back_ref`。

## OPL 边界

- Generic runtime、scheduler、queue、attempt ledger、session、lifecycle transport、generated product shell 与 workbench 归 OPL。
- MAG 不写 OPL stage attempt/current/terminal state，不拥有 Temporal worker，也不把 bounded controller 扩成 durable loop。
- Generated caller 只能回到 MAG action target；不能读取 grant/memory/artifact/package body。

## Source 与状态

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer。
- 开发 checkout 不保存 runtime artifact、receipt instance、workspace body、package body、venv 或 cache。
- `src/` 只允许 domain entry、authority function、refs-only adapter 与 grant-native helper；无 caller 的平台壳直接删除。
- 历史路径只在 `docs/history/**`、明确 provenance 或 negative guard 中出现，不作为兼容承诺。

## 验证

- 默认入口是 `scripts/verify.sh`；`full` 运行完整 repo suite。
- Python/pytest 必须经 clean runner，避免把 cache/venv/bytecode 写回 checkout。
- 结构 source gate 使用 OPL canonical conformance scanner，不再维护 MAG 私有 source-purity wrapper。
- 测试只固定可观察 behavior、authority 和 fail-closed contract，不固定 MRO、`__module__`、源码文件位置、wrapper 存在或文档措辞。

## 证据边界

- Live progress、quality/export、human gate、long soak、owner acceptance 与 production status 必须由对应 live/readback/receipt 证明。
- Production acceptance contract 是 provenance，不是 live closing ref；`domain_owned_closing_ref` 为空时不得写成完成。
- 文档、focused tests、conformance pass 和 refs-only ledger 不能单独支撑 readiness claim。
- 正式 Stage Review 必须来自新的 StageAttempt 和新的 executor session；producer self-check、same-thread resume 或无 exact artifact hash 的记录不能算 Review。
- `review_and_rebuttal` Meta Review 不继承上游生成对话，也不内联修稿；它必须把缺陷路由到最早能关闭根因的 Stage，并在新 generation 后重新审查。
