# 不变量

## Runtime 与 formal-entry

- `Med Auto Grant` 对外第一身份固定为独立 medical grant domain agent，不写成 `OPL` 内部 workspace 模块。
- `CLI` / `MedAutoGrantDomainEntry` 固定为 agent entry；`product entry/frontdesk/direct-entry/user-loop` 固定为 lightweight direct entry / projection。
- `gateway / harness` 继续保留为内部架构分层术语，不作为对外第一身份。
- formal-entry matrix 当前固定为：默认正式入口 `CLI`、支持协议层 `MCP`（future layer）、内部控制面 `controller`。
- 不得把 `supported_protocol_layer=MCP` 解释成“当前 public runtime 已正式支持 MCP”。
- 不得把 developer control-plane entry 的存在解释成“产品 controller 已正式支持”。
- 当前默认公开 capability contract 固定为 `CLI-first + MedAutoGrantDomainEntry + product-entry/user-loop surfaced local scripts/contracts`；local scripts/contracts 必须是 schema-backed、由 product-entry / user-loop / direct-entry surface 暴露的受控 contract，不得作为绕开 authoring runtime 的 ad-hoc 执行路径。
- 历史 local host-agent runtime 材料只允许作为归档追溯材料，不得继续写成当前产品 runtime。
- 当前 `hermes_runtime.py` 与 `domain_entry.py` 只允许被写成 repo-side domain adapter / entry adapter，不得再被误写成 runtime substrate owner。

## Control-plane 与 repo-tracked truth

- `contracts/runtime-program/current-program.json` 是 repo-tracked 的 current-program pointer。
- 项目级 `.runtime-program/` 已退役；机器本地 runtime state 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 项目级 `.codex/` 与 `.omx/` 已退役，不再作为仓库本地状态入口。
- 如需保留历史 session、prompt、log 或 hook 状态，应迁入用户级 `~/.codex/` 归档。
- repo-tracked current truth 以 `docs/specs/*current-truth.md` 与相关 activation package 为准。
- 当前 owner line 固定为“CLI/domain-entry stable capability surface with Codex-default execution and optional hosted backend lanes”。
- 历史 closeout label 与 baseline 只保留在归档 current-truth 材料中；核心五件套不再把它们写成当前 owner line。
- 在没有新的 repo-tracked tranche truth 前，不得把旧 host-agent runtime closeout 材料重新写回“还有默认续推中的 active delta”。

## 目标优先级

- `OPL` 当前固定只承担 family-level session/runtime/projection 与 shared modules/contracts/indexes，不承担本仓 domain truth owner 身份。
- `OPL Runtime Manager` 当前固定为 OPL 侧 thin adapter/projection layer over external `Hermes-Agent` substrate；它不得成为 MAG grant-domain truth owner、scheduler kernel、session store、memory store、concrete authoring executor 或 private Hermes fork。
- OPL native helper 与高频状态索引只能缓存、探测和投影 MAG 已暴露的 `runtime_control`、`runtime_continuity`、workspace projection、artifact locator 与 explicit wakeup/TODO queue；不得替代 `contracts/runtime-program/current-program.json`、authoring contract、quality gate、route truth 或 submission-ready export gate。
- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态，而不是继续深磨已放弃的旧本地宿主路线。
- 当前 `CLI-first + host-agent runtime` 是历史 repo-verified baseline，但它只允许留在归档追溯材料中，不应再被误写为长期终态。
- 当 hosted/proof backend 相关材料存在时，不得把 repo-side adapter 重写成默认 runtime owner，也不得把这些 lane 误写成唯一公开 capability contract。
- 当前 landed substrate、兼容桥与 future scope 必须在 `docs/status.md` 与 `docs/README*` 中显式拆开。

## 任务边界与 gate 语义

- MAG 当前任务边界固定为“指定基金任务正文 authoring”，不把跨 funder 重选写成默认主线动作。
- “科学完成可待审包”与“形式/客观补件完成”必须分层表达，禁止合并成单一完成态。
- AI-first 质量判断必须由 authoring executor / critique executor 产生的 AI-authored artifact 持有；schema、scorecard、closure dossier 与 autonomy controller 只能聚合结构、证据引用、机械状态和队列。缺少 active AI-backed critique 时，不得把质量状态提升为 `near_submission_candidate` 或 `submission_grade_candidate`。
- `pass revision` 只能应用 AI-authored `mutation_payload.replacement_text` / `replacement_core_claim`，不得程序化生成正文 replacement prose 或使用 fallback prose 补齐正文。
- 形式/客观补件默认进入 `TODO + 显式唤醒` 队列；除非直接破坏正文科学成立，否则不得升级为正文 authoring blocker。
- 人工 gate 只覆盖同一基金任务内的作者决策，不跨任务改写 funding 目标。

## 执行句柄边界

- `grant_run_id` 是执行句柄，不替代或污染 `workspace_id`、`draft_id`、`program_id`。
- 所有 CLI 输出必须保持句柄分离并稳定回显。

## 验证与审计

- 旧五个 canonical CLI surfaces 仍是 verifier/audit baseline。
- `stage-route-report` 是唯一 canonical route/checkpoint 聚合面，必须输出 `verification_checkpoint` 与 `checkpoint_status`。
- 最小验证入口是 `scripts/verify.sh`；默认执行 `make test-fast`，保留 `meta`、`cli-smoke`、`full` 分层 lane。

## 文档治理

- `AGENTS.md` 只管工作方式，不堆项目事实。
- 项目事实优先收敛到 `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- 历史 OMX 资料只从 `docs/history/omx/` 进入。
