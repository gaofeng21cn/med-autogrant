# 不变量

Owner: `Med Auto Grant`
Purpose: `stable_invariants`
State: `current`
Machine boundary: 本文是人读约束集。可执行约束继续归 contracts、schemas、source、CLI/API behavior、验证脚本、runtime receipts 与 workspace/artifact outputs。

## 身份、入口与运行真相

- `Med Auto Grant` 对外第一身份固定为独立 medical grant domain agent，不写成 `OPL` 内部 workspace 模块。
- `CLI` / `MedAutoGrantDomainEntry` 是 agent entry；`product entry` / `product status` / `direct-entry` / `user-loop` 是单一 app skill 下的内部 command contract / direct-product projection，不提升成公开第一主语。
- formal-entry matrix 当前固定为 `CLI`（默认正式入口）/ `MCP`（future protocol layer）/ `controller`（内部控制面）。不得把 `supported_protocol_layer=MCP` 或 developer control-plane entry 写成当前 public runtime / 产品 controller 已正式支持。
- 当前默认公开 capability contract 固定为 `CLI-first + MedAutoGrantDomainEntry + product-entry/user-loop surfaced local scripts/contracts`；local scripts/contracts 必须是 schema-backed、受控 surface，不得作为绕开 authoring runtime 的 ad-hoc 执行路径。

## Repo Truth 与本地状态

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer；项目级 `.runtime-program/`、`.codex/` 与 `.omx/` 已退役，本机 runtime state 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- repo-tracked current truth 以核心五件套、`contracts/runtime-program/current-program.json`、以及 `docs/specs/README*` 中列出的 active current-truth specs 为准；较早 dated specs、activation package、历史 closeout label 与 baseline 只作为 provenance。
- 当前 owner line 是 `OPL/Temporal hosted autonomous runtime is the default task runtime; MAG stays a grant-domain authority surface with Codex CLI as the default stage executor`。任务启动后的默认运行驻留由 OPL/Temporal 承担；默认 concrete stage executor 是 `codex_cli` / `Codex CLI`；MAG 不实现自己的 daemon、scheduler、attempt loop 或 attempt ledger。`Hermes-Agent`、Gateway、local-manager、旧 host-agent runtime 和非默认 executor/proof backend 只允许作为显式 proof lane、技术参考、history 或 regression oracle，不得进入默认安装依赖、product-entry owner 或 runtime-registration owner。
- `domain_runtime_parts/substrate.py` 与 `domain_entry.py` 只能写成 repo-side domain adapter / entry adapter；旧 `domain_runtime.py` facade 已无 active source，runtime parts 不得通过 facade 读取 monkeypatch target 或重新引入 `domain_runtime_parts.patch_targets` 这类兼容桥。

## OPL 边界与标准 Agent 目标

- `OPL` 是 stage-led、以 Agent executor 为最小执行单位的完整智能体运行框架，可把 MAG 作为外部领域依赖托管；它不承担 grant-domain truth owner、fundability owner、authoring quality owner、submission-ready export authority、concrete authoring executor 或 private Hermes fork。
- OPL runtime framework 持有 stage attempt lifecycle、scheduler、session store、memory locator/index、queue/wakeup/handoff/receipt、retry/dead-letter、operator projection、shared modules/contracts/indexes 和 Temporal-backed provider 编排；OPL-hosted production path 必须以 Temporal readiness 为前提，local provider 只允许作为 dev/CI/offline diagnostic baseline。
- OPL native helper 与高频状态索引只能缓存、探测和投影 MAG 已暴露的 `runtime_control`、`runtime_continuity`、workspace projection、artifact locator 与 explicit wakeup/TODO queue；不得替代 current-program、authoring contract、quality gate、route truth 或 submission-ready export gate。
- 当前 OPL stage-led 对齐 surface 只供 OPL discovery、queue、wakeup、handoff、receipt、retry/dead-letter 和 operator projection 使用；不得授权 OPL 生成 fundability judgment、authoring quality verdict 或 submission-ready export verdict。

## 标准 Agent 目标与 legacy 退役

- MAG 的目标态高于当前实现分布。product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、local journal、attempt ledger、workspace/source intake、package/memory helper 或 product wrapper 只能作为迁移输入；不得因为已有 active caller 或当前能跑就写成长期合理。
- MAG 作为标准 OPL Agent 的长期形态是 `Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions`。通用 transport、ledger、index、lifecycle、runner、workbench、observability、source/package/memory shell 和 generated wrapper 必须上收到 OPL primitive / pack compiler / App shell，或收薄成 refs-only adapter / diagnostic cleanup path。
- 保留在 MAG 的私有程序面必须是无法声明化的 grant authority function：funding call 解释、fundability verdict、specific aims / authoring quality / export verdict、package authority、memory accept/reject、owner receipt signer 或 grant-native helper implementation。缺少接口、active caller、不能上收原因、receipt/blocker/ref 输出边界和 no-forbidden-write 证据时，必须作为功能/结构差距处理。
- Domain memory apply 只能通过 MAG-owned descriptor、writeback proposal、accept/reject decision、runtime receipt evidence writer、operator receipt projection 与 `controlled_domain_memory_apply_proof` 推进。OPL 只能消费 refs / receipt projection，不能写 memory body、fundability verdict、authoring quality verdict 或 submission-ready export verdict。
- MAG owner receipt 与 lifecycle guarded apply 必须保持 ref-only 边界：`owner_receipt_contract` 只允许 OPL 消费 `domain_owner_receipt`、`typed_blocker` 或 `no_regression_evidence` refs；cleanup/restore/retention 若触及 grant artifact、memory body、quality verdict 或 submission-ready export verdict，必须返回 MAG owner receipt requirement 或 typed blocker。
- 开发 checkout 只保存 repo source、docs、schema/contract、locator/index、receipt ref、restore/retention policy 与 authority-function descriptor。真实 workspace state、runtime artifact、receipt instance、submission/export package、临时 build/cache/venv/pycache/pytest cache/install sync 副产物必须写入 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- `runtime/authority_functions/` 的语义只限最小 MAG authority function anchor；它不得变成 runtime artifact root、generic lifecycle engine、session store、scheduler、runner、queue、workbench 或 memory body store。
- OPL 上收通用 workspace/file lifecycle primitive 后，MAG 私有 scheduler/runner/session/workbench 残留只能作为迁移输入、refs-only adapter、diagnostic 或 tombstone；不得继续定义长期结构。
- 旧 local host-agent runtime、旧 `OPL Gateway` wording、默认 Hermes/Gateway/local-manager active path、旧 product-status traces、旧 canonical CLI verifier baseline、兼容聚合面和旧 alias/facade/wrapper 只能作为 history、tombstone、explicit proof history 或 regression oracle；active caller 迁走后不保留 compatibility shim。

## 任务边界与 AI-first Gate

- MAG 当前任务边界固定为“指定基金任务正文 authoring”，不把跨 funder 重选写成默认主线动作。
- “科学完成可待审包”与“形式/客观补件完成”必须分层表达；`package submission-ready` 是本地严格导出 gate，不等于外部基金官网 portal submission 已完成，也不能替代正文科学完成判断。
- AI-first 质量判断必须由 authoring executor / critique executor 产生的 AI-authored artifact 持有；schema、scorecard、closure dossier 与 autonomy controller 只能聚合结构、证据引用、机械状态和队列。缺少 active AI-backed critique 时，不得把质量状态提升为 `near_submission_candidate` 或 `submission_grade_candidate`。
- `pass revision` 只能应用 AI-authored `mutation_payload.replacement_text` / `replacement_core_claim`，不得程序化生成正文 replacement prose 或使用 fallback prose 补齐正文。
- 形式/客观补件默认进入 `TODO + 显式唤醒` 队列；除非直接破坏正文科学成立，否则不得升级为正文 authoring blocker。
- 人工 gate 只覆盖同一基金任务内的作者决策，不跨任务改写 funding 目标。

## 执行句柄与验证审计

- `grant_run_id` 是执行句柄，不替代或污染 `workspace_id`、`draft_id`、`program_id`；所有 CLI 输出必须保持句柄分离并稳定回显。
- 旧五个 canonical CLI surfaces 只作为 regression oracle / historical verifier context 保留；当前验证以 `scripts/verify.sh` 分层 lane、schema / contract / CLI behavior 和生成产物结构为准。
- 测试调用 CLI 时必须使用当前 grouped public command tokens；内部 flat command string 只能作为 payload / schema / dispatch contract 字段存在，不得再作为 public shell alias 调用。
- `stage-route-report` 是唯一 canonical route/checkpoint 聚合面，必须输出 `verification_checkpoint` 与 `checkpoint_status`。
- 最小验证入口是 `scripts/verify.sh`；默认执行 `make test-fast`，保留 `meta`、`cli-smoke`、`full` 分层 lane。
- Python / pytest 验证必须通过 clean runner 路由缓存、bytecode 与 `uv sync` project venv；开发 checkout 不应产生 `.venv`、`__pycache__`、`.pytest_cache` 或 `*.egg-info` 副产物。

## 文档治理

- `AGENTS.md` 只管工作方式，不堆项目事实。
- 项目事实优先收敛到 `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- 理想态差距和开发计划必须按目标态拆分 `功能/结构差距` 与 `测试/证据差距`；现有通用功能面应由 OPL 承担时，即使可运行，也写成功能/结构差距。
- `当前实际` 只能作为迁移起点、风险和证据来源；不得反向约束理想态，不得把现有私有实现包装成长期设计。
- 历史 OMX 资料只从 `docs/history/omx/` 进入。
