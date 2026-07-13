# 决策记录

Owner: `Med Auto Grant`
Purpose: `current_decision_log`
State: `current`
Machine boundary: 本文只记录当前仍有效的维护决策。机器真相归 contracts、schemas、source、CLI/API behavior、runtime receipts 与 workspace/artifact outputs。

## D1 标准 OPL Agent 形态

MAG 收敛为 `Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions`。通用 runtime、pack compiler、source scanner、product/status/user-loop/workbench shell 不在 MAG 复制。

## D2 Direct Domain Handler

Repo-local domain handler 保留 export 与 dispatch 两个薄入口。Dispatch action 固定为 memory propose、memory decide、stage closeout；旧 lifecycle receipt、operator readiness、physical morphology、executor/codex bundle action 已退役。

## D3 八项 Authority ID

Fundability、quality、export、package、memory、owner receipt、transition oracle、grant-native helper 分开建模，不用一个笼统 helper 或 merged verdict 代替。

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

MAG 不声明、不安装、不锁定 OPL Framework implementation。OPL module workflow 在 checkout 维护 `src/opl_framework` carrier；MAG 只通过该 namespace 消费 Framework helper。

## D10 Transition runner locator

Transition oracle 中的 `runner_contract_ref` 是 OPL-owned external locator，不要求 MAG 仓内存在同路径文件。MAG 不复制 runner contract，也不重新实现 cycle、rollback、dispatch、replay 或 output orchestration；这些行为由 OPL StageRun owner验证。

## D11 Prompt 保留专业依赖，不规定认知配方

Call/eligibility、证据与 claim、独立复审、package authority 和 human submission gate 的因果顺序继续明确。方向、问题、论证、申请人 fit、章节组织和修订范围由 Codex 在这些依赖内迭代判断；Stage prompt、rubric weight、route label 与历史 checkpoint 字段不能冻结工具顺序、推理顺序、候选数量或 section-by-section 修订策略。

## D12 Standard Agent Interface 归 domain descriptor

MAG workspace locator/topology、domain-handler dispatch argv、progress alias 与 routing signal 只在 `contracts/domain_descriptor.json#/standard_agent_interface` 声明，OPL 通过 current package source 托管消费。MAG 不恢复 product status/manifest materializer；这两个 command template 固定为 `null`，generated surface 继续归 OPL。

## D13 默认验证只做一次 pytest 收集

默认 `test-fast` 通过一个 marker 选择执行一次 pytest；line-budget 与 smoke case 保留在同一选集中，不再作为前置 pytest lane 重复启动。`test-meta` 只读检查 repository hygiene；任何 `--fix` 只允许通过显式 cleanup/fix 入口触发。

## D14 Stage Review 使用独立上下文

正式 Review 不复用 producer thread。OPL 在同一 StageRun 下创建独立 reviewer/repairer/re-reviewer Attempts，并按 `contracts/stage_quality_cycle_policy.json` 运输 exact refs、hash、rubric 与 lineage。默认最多三轮 repair + re-review；有可消费 artifact 时预算耗尽形成质量债而非 transition blocker。`review_and_rebuttal` 是跨 Stage Grant Meta Review，缺陷回到最早 owning Stage，专业因果顺序继续由 MAG rubric 与 skill 定义。
