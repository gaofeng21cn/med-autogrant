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

## D9 Dependency pin

MAG 继续消费 release cohort 指定的 `opl-harness-shared` commit。OPL conformance 使用当前 OPL main 运行，但不得把 consumer dependency pin追到 OPL dev HEAD。

## D10 Transition runner locator

Transition oracle 中的 `runner_contract_ref` 是 OPL-owned external locator，不要求 MAG 仓内存在同路径文件。MAG 不复制 runner contract，也不重新实现 cycle、rollback、dispatch、replay 或 output orchestration；这些行为由 OPL StageRun owner验证。
