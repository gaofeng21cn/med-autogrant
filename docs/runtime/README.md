# 运行模型

本页解释 durable execution 的责任和恢复边界。运行合同以 [current-program](../../contracts/runtime-program/current-program.json)、[StageRun profile](../../contracts/stage_run_kernel_profile.json)、[live progress](../../contracts/live_stage_run_progress_evidence.json)和实际 OPL/provider receipt 为准。

OPL/Temporal 持有 StageRun、Attempt lifecycle、session、scheduler、queue、wakeup、retry/resume、dead-letter 和 attempt ledger。MAG 提供 single-pass domain handler、authority function、closeout 和 receipt/blocker refs。MAG 不写 OPL current/terminal state，也不将本地 bounded helper 扩为第二个 durable loop。

Decisive Codex Attempt 决定语义 route，OPL controller 校验并物化 transition。Formal Review 的角色、quality budget 和 terminal decision 由 [quality cycle](../../contracts/stage_quality_cycle_policy.json)声明；执行 transport 的异常关闭由 [executor 规格](../specs/critique-executor.md)解释。

| 持久化层 | 内容与 owner |
| --- | --- |
| 仓库 | source、schemas、contracts、声明式 agent pack、文档与 current-program pointer |
| Grant workspace | `workspace.json`、source、draft、critique、revision、quality 和 package/receipt 结果；MAG 领域 owner |
| 用户 runtime-state | `$CODEX_HOME/projects/med-autogrant/runtime-state/` 的 log、prompt、report、handoff 和本机 evidence |
| OPL/provider | durable execution facts、attempt ledger、queue、恢复与 operator projection |

真实 workspace/artifact/receipt body 不写回开发仓库。运行状态、package 文件存在或 provider completion 不产生 grant/quality/export verdict。恢复后必须核对 workspace、Attempt 与 artifact identity，再消费 owner receipt；用户目录输出也不能单独证明 hosted default caller 或 production long-soak 已闭合。具体 source 存储规则见[数据边界](../source/README.md)。
