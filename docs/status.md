# 当前状态

Date: `2026-04-23`

## 当前角色

- 仓库角色：`Med Auto Grant` 是独立 medical grant domain agent，负责 author-side grant truth、route、review gate 与 package export；`OPL` 只保留 family-level session/runtime/projection 与 shared modules/contracts/indexes。
- 当前执行口径：repo-tracked 默认 capability contract 收口为 `CLI`、`MedAutoGrantDomainEntry`、本地脚本、product-entry/projection commands 与 schema-backed contract；默认正文执行继续继承本机 `Codex` 配置；`Hermes-Agent` 相关路径只保留在显式 hosted/proof lane 与技术参考层。
- 当前 agent entry：`CLI` / `MedAutoGrantDomainEntry` 可被 `Codex`、`OPL` 和其他通用 agent 直接调用。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。

## 当前入口

- 用户路径收口为 `product frontdesk` -> `product user-loop` -> `workspace progress / workspace cockpit` -> `product direct-entry` -> landed `pass` / `package` commands。
- pre-workspace 入口现在增加 `discover-funding-opportunities` -> `select-project-profile` -> `initialize-intake-workspace`，用于先发现候选池，再选 funding/profile，最后落到 `input_intake` workspace。
- 质量治理入口现在包括 `workspace quality-scorecard`、`workspace quality-closure-dossier` 与 `workspace quality-diff`，用于当前版本质量评估、closure package 收口与版本间问题关闭比较。
- 长时间自治入口现在包括 `pass autonomy-controller`（internal command: `execute-grant-autonomy-controller`），用于在预算、轮次、blocker 队列和 evidence gap 队列约束下调度既有主线。
- `product build-entry` 与 lightweight `product entry` shell 继续作为 machine-readable domain/API catalog 的构建层。
- `product frontdesk` 是 controller-owned direct frontdoor contract，读取当前 user loop、projection 与 route truth，并通过 `product-frontdesk.schema.json` generation-time fail-closed 校验。
- `product-entry-manifest` 现已导出 `runtime_control` surface，固定 session/runtime/domain/executor owner、restore point、progress/artifact/approval control surface 与 direct-entry locator，作为 OPL 可归一化消费的 runtime control reference truth。
- `product direct-entry` 组合 `workspace progress`、`workspace cockpit` 与 direct / `opl-handoff` entry mode，是 controller-owned product contract。
- `mainline status` 负责 current line / current focus / completed records / remaining gaps；`mainline phase` 继续保留为维护者参考记录查询。

## 当前执行线

- 当前公开执行线：`direct MAG agent entry / OPL federation handoff -> product frontdesk -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`
- 当前 pre-workspace intake 线：`selection_input materials -> select-project-profile -> initialize-intake-workspace -> input_intake workspace`
- 当前 funding discovery 线：`discovery_input materials -> discover-funding-opportunities -> funding_opportunity_pool`
- 当前 funding discovery 已支持 `official_live`，会记录 source receipts，便于后续 profile 选择和材料 provenance 回溯。
- 当前 `official_live` 官方入口：
  NIH Parent Announcements + NSFC 项目指南列表 + NSFC 医学科学部指南页。
- 当前 funding sync 已支持 `refresh-funding-opportunities-cache` 与 `official_cached`；默认 cache 落点是 `$CODEX_HOME/projects/med-autogrant/runtime-state/funding-landscape/cache/latest.json`。
- 当前 funding sync 会同时生成 `latest.diff.json`，并对消失条目标记 `withdrawn_or_not_listed`。
- 当前公开用户回路：`product frontdesk -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`
- 当前公开 CLI 入口面：`product build-entry`、`product manifest`、`product frontdesk` 与 `package submission-ready`
- 当前稳定可调用面：`CLI` / `MedAutoGrantDomainEntry`、本地脚本、`product build-entry` / `product manifest` / `product frontdesk` / `product direct-entry` / `product user-loop`，以及对应 schema-backed contract
- 当前 `product skill-catalog` 已收口为单一 `Med Auto Grant` app skill；`frontdesk`、`direct-entry`、`user-loop` 等继续作为这个 app skill 的内部 command contract 暴露给 `Codex` / `OPL`。
- 当前主任务完成语义：以正文科学性与 authoring quality 为主，不把单一导出命令当作主任务完成替代。
- 当前 `package submission-ready` 语义：继续作为更严格的本地提交包导出面；它是高标准交付导出能力，不是 authoring 主任务的唯一完成条件。
- 当前形式审查/客观补件语义：默认进入 `TODO` 与显式唤醒链路；仅在直接破坏科学论证成立性时升级为正文 authoring blocker。
- 当前 funder 锁定语义：已锁定 funder/family 的任务线维持同一 funder 闭环推进，不写成 opportunistic 跨 funder 切换。
- 当前新增自治入口：`pass critique-loop`（internal command: `execute-critique-revision-loop`）
- 当前新增全链路自治入口：`pass mainline-loop`（internal command: `execute-authoring-mainline-loop`）
- 当前新增长期 controller 入口：`pass autonomy-controller`（internal command: `execute-grant-autonomy-controller`）
- 当前新增质量治理入口：`workspace quality-scorecard`、`workspace quality-closure-dossier` 与 `workspace quality-diff`
- 当前质量治理已补齐 `issue lineage` 合同：同一问题在 revision 后即使摘要改写，`quality diff` 也会优先按 lineage 跟踪关闭进度，而不是把它误记成“旧问题关闭 + 新问题打开”。
- 当前质量治理已补齐 `closure dossier` 合同：同一轮 quality evaluation 会把 open issue lineage、evidence supply queue 与 queue-only reselection gap 收口成 formal closure package，供 controller / human operator 直接消费。
- 当前 `pass critique-loop` 与 `pass mainline-loop` 的 loop report 已正式携带 `grant_quality_scorecard` 与 `grant_quality_closure_dossier`，每轮质量状态、closure package 与 stop/continue 依据不再只停留在 route reason。
- 当前 autonomy controller 已支持从 prior `controller_report` 恢复：`start.mode=controller_report` 会继续沿用已有 workspace、blocker/evidence gap 队列、action trace、reselection/rollback 决策与 tranche history，并通过 `controller_checkpoint` 输出下一次 resume 的稳定锚点。
- 当前 autonomy controller 已升级为 dossier-driven planning：`grant-autonomy-controller-report` 现在正式输出 `latest_quality_closure_dossier`、`closure_package_queue`、`active_closure_package`，并把 active package / quality summary 写入 tranche history 与 decision basis，作为 stop / continue / fail-closed 的正式治理依据。
- 当前 funder family 抽象：`grant_family_registry.py` 持有 common grant grammar、review grammar、template strategy 与 family compatibility hooks；NSFC / NIH R21 / Wellcome Discovery 已作为 admitted family preset 进入 registry，同时保留 Wellcome discovery placeholder 作为 future family scaffold。
- 当前 family grammar 已补齐 `grant_governance_adapter.py`：family-specific governance policy 现在会显式影响 controller plan hydration 与 closure package ordering，不再散落在 controller 私有 helper 中。
- 当前 controller-owned projection：`workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`
- 当前 repo 级投影：`mainline status` 输出 current line / current focus；`mainline phase` 只承担维护者参考记录。
- `pass critique --executor hermes_native_proof` 继续作为显式 proof lane；默认执行器继续保持 `Codex CLI`，默认模式是 `autonomous`

## 参考入口

- 当前技术记录：`docs/specs/` 与 `contracts/runtime-program/current-program.json`
- 追溯记录：`docs/references/` 与 `docs/history/`
- 当前规范与边界：`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`
- 维护者验证与文档治理：`docs/references/series-doc-governance-checklist.md`
