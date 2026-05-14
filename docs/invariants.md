# 不变量

## Runtime 与 formal-entry

- `Med Auto Grant` 对外第一身份固定为独立 medical grant domain agent，不写成 `OPL` 内部 workspace 模块。
- `CLI` / `MedAutoGrantDomainEntry` 固定为 agent entry；`product entry/product status/direct-entry/user-loop` 固定为单一 app skill 下的内部 command contract / direct-product projection，不得被提升成公开第一主语。
- stage-led framework / domain harness 继续保留为内部架构分层术语，不作为对外第一身份。
- formal-entry matrix 当前固定为：默认正式入口 `CLI`、支持协议层 `MCP`（future layer）、内部控制面 `controller`。
- 不得把 `supported_protocol_layer=MCP` 解释成“当前 public runtime 已正式支持 MCP”。
- 不得把 developer control-plane entry 的存在解释成“产品 controller 已正式支持”。
- 当前默认公开 capability contract 固定为 `CLI-first + MedAutoGrantDomainEntry + product-entry/user-loop surfaced local scripts/contracts`；local scripts/contracts 必须是 schema-backed、由 product-entry / user-loop / direct-entry surface 暴露的受控 contract，不得作为绕开 authoring runtime 的 ad-hoc 执行路径。
- 历史 local host-agent runtime 材料只允许作为归档追溯材料，不得继续写成当前产品 runtime。
- 当前 `domain_runtime.py` 与 `domain_entry.py` 只允许被写成 repo-side domain adapter / entry adapter，不得再被误写成 runtime substrate owner。
- `domain_runtime.py` 只保留薄 facade / public import surface；runtime parts 不得通过 `med_autogrant.domain_runtime` facade 读取 monkeypatch target，也不得重新引入 `domain_runtime_parts.patch_targets` 这类兼容桥。测试应 patch 真实 owner module 或显式注入对象。

## Control-plane 与 repo-tracked truth

- `contracts/runtime-program/current-program.json` 是 repo-tracked 的 current-program pointer。
- 项目级 `.runtime-program/` 已退役；机器本地 runtime state 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 项目级 `.codex/` 与 `.omx/` 已退役，不再作为仓库本地状态入口。
- 如需保留历史 session、prompt、log 或 hook 状态，应迁入用户级 `~/.codex/` 归档。
- repo-tracked current truth 以核心五件套、`contracts/runtime-program/current-program.json`、以及 `docs/specs/README*` 中列出的 active current-truth specs 为准；较早 dated specs 与 activation package 只作为历史 provenance。
- 当前 owner line 固定为“CLI/domain-entry stable capability surface with Codex-default execution and optional hosted backend lanes”。
- 默认最小执行单元固定为 `codex_cli` / `Codex CLI`；`Hermes-Agent` 只允许作为显式 hosted/proof lane 或技术参考依赖出现，不得进入默认安装依赖或默认 product-entry/runtime-registration owner。
- 历史 closeout label 与 baseline 只保留在归档 current-truth 材料中；核心五件套不再把它们写成当前 owner line。
- 在没有新的 repo-tracked tranche truth 前，不得把旧 host-agent runtime closeout 材料重新写回“还有默认续推中的 active delta”。

## 目标优先级

- `OPL` 当前固定为 stage-led、以 Agent executor 为最小执行单位的完整智能体运行框架，可把 MAG 作为外部领域依赖托管；它不承担本仓 domain truth owner 身份。
- OPL runtime framework 可以持有 stage attempt lifecycle、scheduler、session store、memory store、queue/wakeup/handoff/receipt、retry/dead-letter、operator projection、shared modules/contracts/indexes 和 Temporal-backed provider 编排；它不得成为 MAG grant-domain truth owner、fundability owner、authoring quality owner、submission-ready export authority、concrete authoring executor 或 private Hermes fork。OPL-hosted production path 必须以 Temporal readiness 为前提；local provider 只允许作为 dev/CI/offline diagnostic baseline。
- OPL native helper 与高频状态索引只能缓存、探测和投影 MAG 已暴露的 `runtime_control`、`runtime_continuity`、workspace projection、artifact locator 与 explicit wakeup/TODO queue；不得替代 `contracts/runtime-program/current-program.json`、authoring contract、quality gate、route truth 或 submission-ready export gate。
- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态，而不是继续深磨已放弃的旧本地宿主路线。
- 当前 `CLI-first + host-agent runtime` 是历史 repo-verified baseline，但它只允许留在归档追溯材料中，不应再被误写为长期终态。
- 当 hosted/proof backend 相关材料存在时，不得把 repo-side adapter 重写成默认 runtime owner，也不得把这些 lane 误写成唯一公开 capability contract。
- 当前 landed substrate、兼容桥与 future scope 必须在 `docs/status.md` 与 `docs/README*` 中显式拆开。
- 当前 OPL stage-led 对齐已经落到 MAG-owned `family_action_catalog`、`family_stage_control_plane`、runtime_control / runtime_continuity projection 与 product sidecar adapter；这些 surface 只供 OPL discovery、queue、wakeup、handoff、receipt、retry/dead-letter 和 operator projection 使用，不授权 OPL 生成 fundability judgment、authoring quality verdict 或 submission-ready export verdict。
- Domain memory apply 只能通过 MAG-owned descriptor、writeback proposal、accept/reject decision、runtime receipt evidence writer、operator receipt projection 与 `controlled_domain_memory_apply_proof` 推进；repo 只保存 contract、schema、locator、seed fixture、receipt evidence writer contract 和 repo-source layout audit，不保存真实 memory entry、grant artifact、workspace private evidence 或 receipt instance。OPL 只能消费 refs / receipt projection，不能写 memory body、fundability verdict、authoring quality verdict 或 submission-ready export verdict。
- MAG owner receipt 与 lifecycle guarded apply 必须保持 ref-only 边界：`owner_receipt_contract` 只允许 OPL 消费 `domain_owner_receipt`、`typed_blocker` 或 `no_regression_evidence` refs；`lifecycle_guarded_apply_proof` 只允许 OPL apply 自有 ledger/locator，cleanup/restore/retention 若触及 grant artifact、memory body、quality verdict 或 submission-ready export verdict，必须返回 MAG owner receipt requirement 或 typed blocker。
- 旧 local host-agent runtime、旧 `OPL Gateway` wording、默认 Hermes/Gateway/local-manager active path、旧 product-status traces 和旧五个 canonical CLI verifier baseline 只能作为历史 provenance、explicit proof history 或 regression oracle 保留；它们不得回到默认 product/runtime owner。旧 `tests/test_product_entry.py` 兼容聚合面已删除。

## 任务边界与 gate 语义

- MAG 当前任务边界固定为“指定基金任务正文 authoring”，不把跨 funder 重选写成默认主线动作。
- “科学完成可待审包”与“形式/客观补件完成”必须分层表达，禁止合并成单一完成态。
- `package submission-ready` 是本地严格导出 gate，不等于外部基金官网 portal submission 已完成，也不能替代正文科学完成判断。
- AI-first 质量判断必须由 authoring executor / critique executor 产生的 AI-authored artifact 持有；schema、scorecard、closure dossier 与 autonomy controller 只能聚合结构、证据引用、机械状态和队列。缺少 active AI-backed critique 时，不得把质量状态提升为 `near_submission_candidate` 或 `submission_grade_candidate`。
- `pass revision` 只能应用 AI-authored `mutation_payload.replacement_text` / `replacement_core_claim`，不得程序化生成正文 replacement prose 或使用 fallback prose 补齐正文。
- 形式/客观补件默认进入 `TODO + 显式唤醒` 队列；除非直接破坏正文科学成立，否则不得升级为正文 authoring blocker。
- 人工 gate 只覆盖同一基金任务内的作者决策，不跨任务改写 funding 目标。

## 执行句柄边界

- `grant_run_id` 是执行句柄，不替代或污染 `workspace_id`、`draft_id`、`program_id`。
- 所有 CLI 输出必须保持句柄分离并稳定回显。

## 验证与审计

- 旧五个 canonical CLI surfaces 只作为 regression oracle / historical verifier context 保留；当前验证以 `scripts/verify.sh` 分层 lane、schema / contract / CLI behavior 和生成产物结构为准。
- 测试调用 CLI 时必须使用当前 grouped public command tokens；内部 flat command string 只能作为 payload / schema / dispatch contract 字段存在，不得再作为 public shell alias 调用。
- `stage-route-report` 是唯一 canonical route/checkpoint 聚合面，必须输出 `verification_checkpoint` 与 `checkpoint_status`。
- 最小验证入口是 `scripts/verify.sh`；默认执行 `make test-fast`，保留 `meta`、`cli-smoke`、`full` 分层 lane。

## 文档治理

- `AGENTS.md` 只管工作方式，不堆项目事实。
- 项目事实优先收敛到 `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- 历史 OMX 资料只从 `docs/history/omx/` 进入。
