# 当前状态

Date: `2026-05-11`

## 当前角色

- 仓库角色：`Med Auto Grant` 是独立 medical grant domain agent，负责 author-side grant truth、route、review gate 与 package export；`OPL` 只保留 family-level session/runtime/projection 与 shared modules/contracts/indexes。
- OPL 关系：MAG 可以作为 OPL Codex-first、stage-led 完整智能体运行框架上的 admitted domain agent 被托管、唤醒和投影，但不是 OPL 内部模块。OPL 负责 stage attempt 生命周期、queue/wakeup、handoff、receipt、approval/retry/dead-letter、operator projection、shared modules/contracts/indexes 与外部 provider 编排；MAG 继续持有 grant stage pack、prompt/skill、route truth、quality gate 和 submission-ready export authority。
- OPL framework 总入口：涉及 stage-led framework、Codex CLI 最小执行单元、外部 provider、OPL-hosted path、旧 Hermes/Gateway/local-runtime surface 退役的跨仓问题，先读 `/Users/gaofeng/workspace/one-person-lab/docs/references/runtime-substrate/opl-stage-led-agent-framework-roadmap.zh-CN.md`；MAG 本仓只维护 grant-domain truth、descriptor/projection 和 direct skill 等价。
- Standard domain-agent skeleton 目标：MAG 后续应按 OPL 统一 `agent/`、`contracts/`、`runtime/`、`docs/` repo-source 边界映射现有 grant stages、prompt/skill、knowledge/context、quality gate、sidecar、receipt schema、projection builder 和 package/export locator contract。当前先以 manifest/adapter 对齐，不要求立即物理移动目录；真实申请书、receipt 实例、中间产物和导出包属于 workspace / runtime artifact root，不属于开发仓源码目录。OPL 可上收 lifecycle/artifact/retention/restore 等 framework primitive，但不得持有 MAG grant truth、fundability judgment 或 submission-ready export verdict。
- 当前执行口径：repo-tracked 默认 capability contract 收口为单一 `Med Auto Grant` app skill、`CLI`、`MedAutoGrantDomainEntry`、本地脚本、product-entry/projection commands 与 schema-backed contract；其中 `product entry/product status/direct-entry/user-loop` 是 app skill 下的内部 command contract 和 direct-product projection。默认正文执行固定继承本机 `Codex CLI` / `codex_cli` 配置；在 OPL 托管语境中，`Codex CLI` 是 stage attempt 的最小执行单元。`Hermes-Agent` 相关路径只保留在显式 hosted/proof lane 与技术参考层，默认安装不拉取 `hermes-agent`。
- OPL 运行框架口径：OPL 是完整智能体运行框架，不是只索引 MAG projection 的薄 sidecar。它可以把 MAG 的 task registration、runtime_control、runtime_continuity、workspace projection、artifact locator 与 explicit wakeup/TODO queue 接到 stage-led runtime、状态索引、doctor/repair/resume 和外部 provider 编排面；这些能力不持有 author-side truth、quality gate、submission-ready export gate 或 concrete executor。旧 `OPL Runtime Manager`、Temporal、Hermes-first、Gateway/local-runtime 说法只保留为历史追溯或 provider-specific 实现记录。
- 当前 agent entry：`CLI` / `MedAutoGrantDomainEntry` 可被 `Codex`、`OPL` 和其他通用 agent 直接调用，或者先通过单一 app skill 读取 machine-readable surface。
- Codex App direct skill 调用与 OPL 托管调用都必须回到同一套 MAG-owned route truth、workspace truth、quality surfaces 和 export gate。
- Stage-led OPL 对齐当前状态：MAG 已通过 `family_action_catalog`、`family_stage_control_plane`、`runtime_control`、`runtime_continuity`、`product sidecar export/dispatch`、`opl_stage_runtime_registration` 和 `domain_agent_skeleton_mapping` 暴露 OPL 可发现/可排队/可投影 surface。OPL 只能消费这些 MAG-owned descriptor / projection / refs，不能替代 MAG 做 fundability strategy、specific aims、proposal authoring、critique/revision、quality gate 或 submission-ready export 判断。当前还不能把 MAG stage attempt 写成已完成 production long-run soak；OPL 侧 Temporal provider code、Codex runner repo/test harness、human-gate signal ledger 和 Aion stage-attempt visibility 已落地，但 MAG provider-hosted controlled grant stage soak、真实 workspace/runtime receipt instance 和真实 memory writeback apply 仍待完成。
- 2026-05-11 OPL family index 校准：OPL `agents list` 与 `stages list` 当前能把 MAG 识别为 aligned standard domain-agent skeleton 和 6-stage family stage plane；OPL `domain-memory list` 当前能把 MAS/MAG/RCA 解析为 `resolved_memory_descriptor_count=3`、`missing_memory_descriptor_count=0`。MAG 本仓也已经把 grant strategy memory 推进到 migration plan、seed fixture、writeback proposal generator、accept/reject command、receipt locator、controlled consumed-memory proof、writeback receipt proof 与 operator receipt projection，并在 product-entry manifest 顶层暴露标准 `domain_memory_descriptor` / `family_domain_memory_ref.v1` adapter。该 adapter 只解决 OPL family memory index 的标准解析入口；MAG 继续持有 memory store、accept/reject、fundability/authoring quality 和 submission-ready export authority。
- 旧面退役校准：默认公开能力已收口到单一 app skill、CLI、MedAutoGrantDomainEntry、product-entry/projection commands 与 schema-backed contract；旧 local host-agent runtime、旧 `OPL Gateway` wording、较早 Hermes-first specs、旧五个 canonical CLI verifier baseline 和旧 product-status traces 只保留为 provenance / regression oracle。旧 `tests/test_product_entry.py` 兼容聚合面已删除，product-entry regression cases 直接由 `tests/product_entry_cases/` 收集。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。
- 文档组合状态：2026-05-11 文档治理后，公开/核心入口继续以 single app skill、`CLI` / `MCP` / `controller` stable surface、OPL Codex-first stage-led framework 边界、Codex CLI 最小执行单元和本地 `submission-ready` 非外部 portal submission 为准；旧 specs 保留原路径作为 provenance，通过 `docs/history/specs/` 进入。

## 当前入口

- 用户路径收口为单一 app skill 下的 `product status` -> `product user-loop` -> `workspace progress / workspace cockpit` -> `product direct-entry` -> landed `pass` / `package` commands。
- pre-workspace 入口现在增加 `discover-funding-opportunities` -> `select-project-profile` -> `initialize-intake-workspace`，用于先发现候选池，再选 funding/profile，最后落到带 `workspace.json` canonical document 与 workspace-local Git boundary 的目录型 `input_intake` workspace。
- 质量治理入口现在包括 `workspace quality-scorecard`、`workspace quality-closure-dossier` 与 `workspace quality-diff`，用于当前版本质量评估、closure package 收口与版本间问题关闭比较。
- 长时间自治入口现在包括 `pass autonomy-controller`（internal command: `execute-grant-autonomy-controller`），用于在预算、轮次、blocker 队列和 evidence gap 队列约束下调度既有主线。
- `product build-entry` 与 lightweight `product entry` shell 继续作为 machine-readable domain/API catalog 的构建层。
- `product status` 是 controller-owned direct product entry contract，读取当前 user loop、projection 与 route truth，并通过 `product-status.schema.json` generation-time fail-closed 校验；它属于 app skill 的内部 command contract。
- `product-entry-manifest` 现已导出 `runtime_control` surface，固定 session/runtime/domain/executor owner、restore point、progress/artifact/approval control surface、direct-entry locator 与 `semantic_closure`，作为 integration/reference truth 供 OPL 或 hosted caller 归一化消费。
- `MAG` 已声明 `OPL` family contract adoption：`contracts/runtime-program/opl-family-contract-adoption.json` 与 `docs/references/opl_family_contract_adoption.md` 把 runtime attempt、grant quality projection、incident learning 与 product operator projection 映射回 MAG-owned surfaces；`OPL` 只消费投影，不持有 grant truth、fundability judgment 或 submission-ready export gate。
- 同一 adoption contract 现在包含 `stage_control_projection`，且 `product-entry-manifest` 会导出 `family_stage_control_plane`：它把 `call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready` 映射回 MAG 已有 intake、screening、question/argument/fit/outline、drafting、critique/revision、freeze 与 `package submission-ready` surface。每个 stage descriptor 固定 stage goal、owner、skills、allowed action refs、handoff、source refs、freshness 与 authority boundary，并在构建时校验 `allowed_action_refs` 对齐 `family_action_catalog`，供 OPL 真实 discovery smoke 消费。这只是 OPL family Stage Control Plane 的 descriptor/projection，不改写 MAG route truth、fundability judgment 或 submission-ready export gate。
- 当前 OPL family shared release pin 已对齐到 `2b08c7efd8acd80355e870087d4ce5be7b45d4d1`；`pyproject.toml` 与 `uv.lock` 共同持有这条 Python shared package pin。
- `product-entry-manifest` 现已导出 MAG-owned `family_action_catalog`，并从同一份 action definition 投影 CLI、product-entry、skill metadata 与 MCP-compatible descriptor；当前 MCP 明确为 `descriptor_only=true`、`public_runtime=false`，不声明 public MCP runtime 已落地。
- `runtime_control` 与 skill catalog 的 `runtime_continuity` 也是 OPL stage-led runtime framework 的 MAG 侧注册/投影输入；任何上层索引都必须回指这些 repo-tracked surface，不能在 OPL 侧复制 authoring truth。
- `product sidecar export` / `product sidecar dispatch` 现在提供 MAG product sidecar adapter：export 把 `runtime_control`、`runtime_continuity`、TODO/explicit wakeup、autonomy-controller 与 user-loop attention queue 映射为 OPL typed family queue 可消费的 projection；dispatch 只接受 `status/read`、`user-loop/wakeup`、`autonomy-controller/dry-run`、`autonomy-controller/guarded-run`、`notification/receipt` 这组 MAG-owned guarded actions。Hermes proof executor 不成为默认 authoring executor。
- `product direct-entry` 组合 `workspace progress`、`workspace cockpit` 与 direct / `opl-handoff` entry mode，是 controller-owned product contract。
- `mainline status` 负责 current line / current focus / completed records / remaining gaps；`mainline phase` 继续保留为维护者参考记录查询。

## 当前执行线

- 当前公开执行线：`single Med Auto Grant app skill / direct MAG agent entry -> internal product status -> internal product user-loop -> workspace progress / workspace cockpit -> internal product direct-entry -> pass / package commands`
- 当前 pre-workspace intake 线：`selection_input materials -> select-project-profile -> initialize-intake-workspace -> input_intake workspace directory / workspace.json`
- 当前 funding discovery 线：`discovery_input materials -> discover-funding-opportunities -> funding_opportunity_pool`
- 当前 funding discovery 已支持 `official_live`，会记录 source receipts，便于后续 profile 选择和材料 provenance 回溯。
- 当前 `official_live` 官方入口：
  NIH Parent Announcements + NSFC 项目指南列表 + NSFC 医学科学部指南页。
- 当前 funding sync 已支持 `refresh-funding-opportunities-cache` 与 `official_cached`；默认 cache 落点是 `$CODEX_HOME/projects/med-autogrant/runtime-state/funding-landscape/cache/latest.json`。
- 当前 funding sync 会同时生成 `latest.diff.json`，并对消失条目标记 `withdrawn_or_not_listed`。
- 当前用户回路：`single Med Auto Grant app skill -> product status -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`
- 当前 CLI 入口面：`product build-entry`、`product manifest`、`product status` 与 `package submission-ready`；这些都属于 app skill 下的内部命令面
- 当前稳定可调用面：`CLI` / `MedAutoGrantDomainEntry`、本地脚本、`product build-entry` / `product manifest` / `product status` / `product direct-entry` / `product user-loop`，以及对应 schema-backed contract；它们都挂在单一 `Med Auto Grant` app skill 之下。
- 当前 `product skill-catalog` 已收口为单一 `Med Auto Grant` app skill；`product status`、`direct-entry`、`user-loop` 等继续作为这个 app skill 的内部 command contract 暴露给 `Codex` / `OPL`。
- 同一 skill descriptor 的 `domain_projection` 现已带 `runtime_continuity` envelope，复用 `session_continuity`、`progress_projection`、`artifact_inventory`、`runtime_control.semantic_closure` 真相面，把 authoring continuity、funding call lock、quality closure surface 与 submission-ready gate 语义一起供 `Codex` / `OPL` 直接消费。
- 同一 `domain_projection` 现已暴露 `opl_stage_runtime_registration` v1：该字段是 OPL stage-led runtime framework 的 MAG 侧 registration/projection envelope。OPL 可以索引 MAG 的 runtime_control、runtime_continuity、artifact inventory、authoring-loop wakeup 与 runtime health 输入；其中高频 workspace/session/artifact/TODO/runtime-health 索引可由 OPL Rust native helper 消费，并由 `native_helper_consumption.proof_surface` 固定 coverage、只读写入边界与 MAG-owned gate 边界，但不得复制 grant truth 或绕过 submission-ready export gate。
- 同一 `opl_stage_runtime_registration` 现已携带 `family_lifecycle_adapter`：它把现有 `runtime_control`、`session_continuity`、`grant-progress/user-loop` 与 `artifact_inventory` 映射成 OPL family persistence、lifecycle、owner-route discovery 与 adoption projection；这只是薄 adapter，不重塑 runtime，不引入 SQLite 深迁移。
- 同一 manifest 现已携带标准 `domain_agent_skeleton_mapping`、`artifact_locator_contract` 与 `controlled_stage_attempt_projection`：repo-source 边界为 `agent/contracts/runtime/docs`，runtime 只声明 sidecar、projection builder、lifecycle adapter、受控 stage-attempt proof refs 与 OPL-hosted controlled grant stage attempt proof refs；真实 grant artifacts 与 receipt 实例必须在 workspace 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/artifacts/<grant_run_id>/` / `receipts/`，OPL 只消费 descriptor、locator、source refs 与 receipt refs，不持有 fundability 或 submission-ready export verdict。
- 同一 manifest 现已把 domain memory 从 descriptor/locator 推进到可验收的 controlled proof contract，并额外暴露 OPL 可解析的顶层 `domain_memory_descriptor`：`domain_memory_descriptor_locator` 内含 migration plan、seed fixture ref、writeback proposal generator、MAG accept/reject command、receipt locator、controlled consumed-memory proof、writeback receipt proof 与 operator receipt projection；`contracts/runtime-program/domain-memory-seed-fixture.json` 只定义模板和禁止项，不包含真实 memory entry、workspace private evidence、grant artifact 或 receipt instance。direct skill 与 OPL-hosted path 使用同一 descriptor、sidecar 和 quality refs，OPL 只消费 consumed-memory refs、receipt/operator projection，不写 memory body、fundability 或 submission-ready verdict。
- OPL family memory 标准化的下一步是让真实 workspace/runtime stage attempt 按该 proof contract 产出 receipt 实例；真实 memory body、accept/reject decision 和 receipt instance 仍属于 MAG workspace/runtime artifact root。
- 当前主任务完成语义：以正文科学性与 authoring quality 为主，不把单一导出命令当作主任务完成替代。
- 当前 `package submission-ready` 语义：继续作为更严格的本地提交包导出面；它是高标准交付导出能力，不是 authoring 主任务的唯一完成条件。
- 当前形式审查/客观补件语义：默认进入 `TODO` 与显式唤醒链路；仅在直接破坏科学论证成立性时升级为正文 authoring blocker。
- 当前 funder 锁定语义：已锁定 funder/family 的任务线维持同一 funder 闭环推进，不写成 opportunistic 跨 funder 切换。
- 当前新增自治入口：`pass critique-loop`（internal command: `execute-critique-revision-loop`）
- 当前新增全链路自治入口：`pass mainline-loop`（internal command: `execute-authoring-mainline-loop`）
- 当前新增长期 controller 入口：`pass autonomy-controller`（internal command: `execute-grant-autonomy-controller`）
- 当前新增质量治理入口：`workspace quality-scorecard`、`workspace quality-closure-dossier` 与 `workspace quality-diff`
- 当前 AI-first 质量边界：`grant_quality_scorecard` / `grant_quality_closure_dossier` 只是 AI critique-backed aggregator。结构字段完整性、证据链接和分数只能作为 completeness signal；没有当前 active AI critique 或 AI-authored quality assessment 时，scorecard 必须标记 `assessment_owner=projection_only`、`ai_reviewer_required=true`，不得产生 `near_submission_candidate` / `submission_grade_candidate`。
- 当前质量治理已补齐 `issue lineage` 合同：同一问题在 revision 后即使摘要改写，`quality diff` 也会优先按 lineage 跟踪关闭进度，而不是把它误记成“旧问题关闭 + 新问题打开”。
- 当前质量治理已补齐 `closure dossier` 合同：同一轮 quality evaluation 会把 open issue lineage、evidence supply queue 与 queue-only reselection gap 收口成 formal closure package，供 controller / human operator 直接消费。
- 当前 `pass critique-loop` 与 `pass mainline-loop` 的 loop report 已正式携带 `grant_quality_scorecard` 与 `grant_quality_closure_dossier`，每轮质量状态、closure package 与 stop/continue 依据不再只停留在 route reason。
- 当前 autonomy controller 已支持从 prior `controller_report` 恢复：`start.mode=controller_report` 会继续沿用已有 workspace、blocker/evidence gap 队列、action trace、reselection/rollback 决策与 tranche history，并通过 `controller_checkpoint` 输出下一次 resume 的稳定锚点。
- 当前 autonomy controller 已升级为 dossier-driven planning：`grant-autonomy-controller-report` 现在正式输出 `latest_quality_closure_dossier`、`closure_package_queue`、`active_closure_package`，并把 active package / quality summary 写入 tranche history 与 decision basis，作为 stop / continue / fail-closed 的正式治理依据。
- 当前 funder family 抽象：`grant_family_registry.py` 持有 common grant grammar、review grammar、template strategy 与 family compatibility hooks；NSFC / NIH R21 / Wellcome Discovery 已作为 admitted family preset 进入 registry，同时保留 Wellcome discovery placeholder 作为 future family scaffold。
- 当前 family grammar 已补齐 `grant_governance_adapter.py`：family-specific governance policy 现在会显式影响 controller plan hydration 与 closure package ordering，不再散落在 controller 私有 helper 中。
- 当前 controller-owned projection：`workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`
- 当前 repo 级投影：`mainline status` 输出 current line / current focus；`mainline phase` 只承担维护者参考记录。
- `pass critique --executor hermes_agent` 继续作为显式 optional proof lane；它只证明选定外部 executor 能在 MAG-owned route/quality/export contract 下工作，不等于默认 runtime、默认 authoring executor、MAG grant truth owner 或 OPL stage-led runtime owner。默认执行器固定为 `codex_cli` / `Codex CLI`，默认模式是 `autonomous`。
- MAG 侧当前目标是 product sidecar adapter，而不是常驻 sidecar daemon：`product sidecar export` / `dispatch` 是 CLI/product-entry 结构化 surface，供 OPL typed queue 与 OPL family runtime provider 唤醒；默认正文 executor 仍由 Codex/domain-selected route 承担。

## 当前目录治理

- repo-tracked 主线不再保留项目级 `.codex/`、`.omx/`、`.runtime-program/`、`.agent-contract-baseline.json` 或 `runtime-state/`；本机 session、prompt、log、report 与 hook 状态统一属于 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 当前测试 lane 已收口为平衡默认：`scripts/verify.sh` 默认运行一次 line-budget、最小 `smoke` 入口健康检查和不需要 optional proof dependency 的非重型 fast core；矩阵型、runtime/session、hosted/export 与 product-entry 覆盖进入显式 `regression` lane；Hermes hosted/proof 进入显式 `proof` lane 并使用 `proof` extra。`tests/product_entry_cases/` 现在是直接收集的 product-entry regression case 边界，旧 `tests/test_product_entry.py` 兼容聚合面已删除。测试口径只固定 machine-readable contract、schema、CLI/API、generated artifact 结构与污染 guard；`README*`、`docs/**`、Markdown 渲染标题和 skill 正文文案不作为稳定断言面。
- `tests/test_repository_hygiene.py` 作为 meta 验证的一部分，阻断 tracked `dist/`、`build/`、`out/`、`__pycache__`、`*.egg-info`、`.DS_Store`、项目级本地状态目录，以及除 `.agents/plugins/marketplace.json` 外的 `.agents/` 内容。
- 同一 hygiene 测试同时固定 tracked source/test line budget，新增或增长的超长源码应先拆分到清晰子模块，而不是扩大单文件基线。

## 参考入口

- 当前技术记录：`docs/specs/` 与 `contracts/runtime-program/current-program.json`
- AI-first 质量边界记录：`docs/specs/2026-04-27-ai-first-quality-boundary-current-truth.md`
- 追溯记录：`docs/references/` 与 `docs/history/`
- 当前规范与边界：`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`
- 维护者验证与文档治理：`docs/references/series-doc-governance-checklist.md`
