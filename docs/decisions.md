# 决策记录

Owner: `Med Auto Grant`
Purpose: `current_decision_log`
State: `current`
Machine boundary: 本文只记录当前仍有效的维护决策。机器真相归 contracts、schemas、source、CLI/API behavior、runtime receipts 与 workspace/artifact outputs。

## D1 标准 OPL Agent 形态

MAG 收敛为 `Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions`。通用 runtime、pack compiler、source scanner、product/status/user-loop/workbench shell 不在 MAG 复制。

## D2 Direct Domain Handler

Repo-local domain handler 保留 export 与 dispatch 两个薄入口。Dispatch action 固定为 memory propose、memory decide、stage closeout；旧 lifecycle receipt、operator readiness、physical morphology、executor/codex bundle action 已退役。

## D3 七项 Authority ID

Fundability、quality、export、package、memory、owner receipt、grant-native helper 分开建模，不用一个笼统 helper 或 merged verdict 代替。`ai_route_policy` 是 declared stage/action scope 的 refs-only projection，不是第八项 authority function，也不拥有 route execution。

## D4 OPL canonical currentness

OPL source-behavior scanner 是结构 currentness owner。MAG 只保留 declarative morphology policy 与 functional audit，不再维护私有 standard-pack/source-purity implementation。

## D5 Direct retirement

旧 module、CLI alias、wrapper、facade、snapshot、compatibility test 无 active caller 后直接删除。需要来龙去脉时使用 history/provenance，不新增 shim、re-export 或别名。

## D6 测试组合

测试覆盖 behavior、authority、identity 与 fail-closed boundary。实现位置、MRO、模块名、wrapper existence、旧快照字段和文档字符串不作为 contract。

## D7 Primary skill carrier

`agent/primary_skill/SKILL.md` 是 canonical rich skill；plugin 路径是 Codex 安装要求的 byte-identical materialized carrier，不是 compatibility mirror，也不持有第二份 MAG truth。

## D8 Live evidence 分层

结构清理可以在没有 production long soak 的情况下完成；但 grant-ready、quality/export ready、submission-ready、owner acceptance 与 production-ready 必须继续 fail closed，直到对应 receipt/human gate/live evidence 到位。

## D9 Framework carrier

MAG 不声明、不安装、不锁定 OPL Framework implementation。OPL module workflow 在 owner checkout 的 `python/opl_framework` 维护 carrier；MAG clean runner 只通过显式 `OPL_FRAMEWORK_ROOT` 将该 namespace加入验证环境。

## D10 Transition runner locator

Transition oracle 中的 `runner_contract_ref` 是 OPL-owned external locator，不要求 MAG 仓内存在同路径文件。MAG 不复制 runner contract，也不重新实现 cycle、rollback、dispatch、replay 或 output orchestration；这些行为由 OPL StageRun owner验证。

## D11 Prompt 保留专业依赖，不规定认知配方

Call/eligibility、证据与 claim、独立复审、package authority 和 human submission gate 的因果顺序继续明确。方向、问题、论证、申请人 fit、章节组织和修订范围由 Codex 在这些依赖内迭代判断；Stage prompt、rubric weight、route label 与历史 checkpoint 字段不能冻结工具顺序、推理顺序、候选数量或 section-by-section 修订策略。

## D12 Standard Agent Interface 归 domain descriptor

MAG workspace locator/topology、runtime domain identity/registration ref、progress alias 与 routing signal只在 `contracts/domain_descriptor.json#/standard_agent_interface` 声明，OPL 通过 current package source 托管消费。`workspace_binding.entry_command_template`、`workspace_binding.manifest_command_template` 与 `runtime.dispatch_command` 已退役，并由 closed-object validation fail closed；OPL 不从 descriptor 恢复 MAG 私有命令模板。

## D13 默认验证只做一次 pytest 收集

默认 `test-fast` 通过一个 marker 选择执行一次 pytest；line-budget 与 smoke case 保留在同一选集中，不再作为前置 pytest lane 重复启动。`test-meta` 只读检查 repository hygiene；任何 `--fix` 只允许通过显式 cleanup/fix 入口触发。

## D14 Stage Review 使用独立上下文

正式 Review 不复用 producer thread。OPL 在同一 StageRun 下创建独立 reviewer/repairer/re-reviewer Attempts，并按 `contracts/stage_quality_cycle_policy.json` 运输 exact refs、hash、rubric 与 lineage。默认最多三轮 repair + re-review；有可消费 artifact 时预算耗尽形成质量债而非 transition blocker。`review_and_rebuttal` 是跨 Stage Grant Meta Review，缺陷回到最早 owning Stage，专业因果顺序继续由 MAG rubric 与 skill 定义。

## D15 最终 package bytes 必须在冻结后独立复审

`package_and_submit_ready` 会在 Grant Meta Review 之后生成或转换四个 canonical package artifacts，并可支撑本地 submission-ready claim，因此不是纯 refs-only handoff。Producer 必须绑定同 generation 的四份 exact refs/hash，且其 package JSON 始终保持 `submission_ready=false`；producer 与 repairer 只能返回 `route_impact.stage_route_recommendation`。`same_stage_repair_required` 在 repair budget 尚存时继续本 Stage 的 assembly/manifest/provenance 修复；若 required finding 的最窄 canonical owner 是另一个 declared Stage，`cross_stage_route_back_before_budget_exhaustion` 允许 reviewer/re-reviewer 提前以 `repair_required + route_back` 终结当前 StageRun，且禁止其他预算耗尽前终局 route。预算耗尽且 exact package bytes 可消费时，它保留 `repair_required` outcome、成为 terminal decisive Attempt并返回 `route_impact.stage_route_decision`，controller 投影 `completed_with_quality_debt`。Reviewer closeout 只提供审阅字段，StageRunController 只能物化 exact-hash-bound `opl_stage_review_receipt`；最终本地 readiness 必须同时消费该 receipt 与 MAG-owned export/owner verdict，OPL 和 reviewer 都不能签 MAG owner receipt。本 Stage repair 只处理 assembly、manifest 和 provenance projection；上游内容、证据、质量闭环、附件 owner 或 export-verdict 缺陷必须 route-back。外部 portal acceptance 继续由下游 human owner 持有。

## D16 Hosted action 与 package lifecycle 归 OPL

MAG public action catalog 固定为 closed `family-action-catalog.v2`，只声明 3 个 `stage_binding` action 和 exact input schema；progress/cockpit 由 OPL generated read model提供。Hosted execution 使用 `opl agents run --domain med-autogrant --action <action_id> --workspace <absolute_path>`。Agent Package 的安装、更新和卸载由 OPL Packages 持有，公共命令分别为 `opl packages install mag`、`opl packages update mag`、`opl packages uninstall mag`；Connect 不再持有 package lifecycle namespace，`medautogrant` 只保留 managed runtime source module locator。

## D17 CLI 声明与执行分离

Command specs 只声明 parser 字段和帮助信息，不承载 callable、method name 或 handler ref。CLI 与 domain entry 使用显式静态 dispatch 调用实际 authority/runtime function；argparse `handler` 注入、`DomainEntryCommandSpec.runtime_method`、`args.handler` 与 `getattr` 动态分派全部退役，避免 command metadata重新成为私有控制面。

## D18 Source transport 归 OPL

通用 HTTPS request、exact URL/origin policy、redirect enforcement、timeout、header validation、decode 与 transport error wrapping 由 `opl_framework.source_transport` 持有。MAG 只声明 NIH/NSFC 三个官方 URL allowlist、funding-specific User-Agent、HTML 解析和 domain provenance；不得恢复 repo-local `urllib` transport、fallback downloader 或第二套网络策略。

## D19 语义 route 与 transition 物化分权

所有 active Stage policy、StageRun profile 和 route advisory 统一声明 `semantic_route_decision_owner=decisive_codex_attempt` 与 `stage_transition_materialization_owner=opl_stage_run_controller`。Primary-only Stage 的 producer、Formal Review 的 terminal reviewer/re-reviewer 可以成为 decisive Attempt；repairer 永不 decisive。Controller 只能校验 decisive Attempt 的 route shape、evidence 与 declared target 后物化 transition，不拥有 grant-semantic approval authority；旧 `semantic_owner`、`route_selection_owner` 和把 `codex_cli` 同时写成语义与 transition owner 的合同已退役。
