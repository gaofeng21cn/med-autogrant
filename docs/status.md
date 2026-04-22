# 当前状态

Date: `2026-04-22`

## 当前角色

- 仓库角色：`Med Auto Grant` 是独立 medical grant domain agent，负责 author-side grant truth、route、review gate 与 package export；`OPL` 只保留 family-level session/runtime/projection 与 shared modules/contracts/indexes。
- 当前执行口径：`Hermes-Agent` 作为外部 runtime substrate owner 持有长期在线与 proof 语义；repo-side grant adapter 继续持有 direct entry、route contract 与导出边界。
- 当前 agent entry：`CLI` / `MedAutoGrantDomainEntry` 可被 `Codex`、`OPL` 和其他通用 agent 直接调用。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。

## 当前入口

- 用户路径收口为 `product frontdesk` -> `product user-loop` -> `workspace progress / workspace cockpit` -> `product direct-entry` -> landed `pass` / `package` commands。
- pre-workspace 入口现在增加 `discover-funding-opportunities` -> `select-project-profile` -> `initialize-intake-workspace`，用于先发现候选池，再选 funding/profile，最后落到 `input_intake` workspace。
- 质量治理入口现在包括 `workspace quality-scorecard` 与 `workspace quality-diff`，用于当前版本质量评估与版本间问题关闭比较。
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
- 当前新增自治入口：`pass critique-loop`（internal command: `execute-critique-revision-loop`）
- 当前新增全链路自治入口：`pass mainline-loop`（internal command: `execute-authoring-mainline-loop`）
- 当前新增长期 controller 入口：`pass autonomy-controller`（internal command: `execute-grant-autonomy-controller`）
- 当前新增质量治理入口：`workspace quality-scorecard` 与 `workspace quality-diff`
- 当前 funder family 抽象：`grant_family_registry.py` 持有 common grant grammar、review grammar、template strategy 与 family compatibility hooks；NSFC / NIH R21 已在 registry 中，Wellcome discovery 为正式 placeholder。
- 当前 controller-owned projection：`workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`
- 当前 repo 级投影：`mainline status` 输出 current line / current focus；`mainline phase` 只承担维护者参考记录。
- `pass critique --executor hermes_native_proof` 继续作为显式 proof lane；默认执行器继续保持 `Codex CLI`，默认模式是 `autonomous`

## 参考入口

- 当前技术记录：`docs/specs/` 与 `contracts/runtime-program/current-program.json`
- 追溯记录：`docs/references/` 与 `docs/history/`
- 当前规范与边界：`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`
- 维护者验证与文档治理：`docs/references/series-doc-governance-checklist.md`
