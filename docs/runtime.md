# 运行模型与数据边界

本页解释 durable execution 责任、恢复边界与 workspace/source 存储划分。运行合同以 [current-program](../contracts/runtime-program/current-program.json)、[StageRun profile](../contracts/stage_run_kernel_profile.json)、[live progress](../contracts/live_stage_run_progress_evidence.json) 和实际 OPL/provider receipt 为准；workspace/source 边界以 [workspace_lifecycle_policy.json](../contracts/workspace_lifecycle_policy.json) 与 [artifact_locator_contract.json](../contracts/artifact_locator_contract.json) 为准。

## Durable Execution 与状态分层

OPL Framework Runway（`opld` / `@opl/runway`）持有 StageRun、Attempt lifecycle、session、scheduler、queue、wakeup、retry/resume、dead-letter 和 attempt ledger。MAG 提供 single-pass domain handler、authority function、closeout 和 receipt/blocker refs。MAG 不写 OPL current/terminal state，也不将本地 bounded helper 扩为第二个 durable loop。

Decisive Codex Attempt 决定语义 route，OPL controller 校验并物化 transition。Formal Review 的角色、quality budget 和 terminal decision 由 [quality cycle](../contracts/stage_quality_cycle_policy.json) 声明；执行 transport 的异常关闭由 [executor 规格](./specs/critique-executor.md) 解释。

| 持久化层 | 内容与 owner |
| --- | --- |
| 仓库 | source、schemas、contracts、声明式 agent pack、文档与 current-program pointer |
| Grant workspace | `workspace.json`、source、draft、critique、revision、quality 和 package/receipt 结果；MAG 领域 owner |
| 用户 runtime-state | `$OPL_STATE_DIR/domains/med-autogrant/runtime-state/` 的 log、prompt、report、handoff 和本机 evidence |
| OPL/provider | durable execution facts、attempt ledger、queue、恢复与 operator projection |

真实 workspace/artifact/receipt body 不写回开发仓库。运行状态、package 文件存在或 provider completion 不产生 grant/quality/export verdict。恢复后必须核对 workspace、Attempt 与 artifact identity，再消费 owner receipt；用户目录输出也不能单独证明 hosted default caller 或 production long-soak 已闭合。

## Workspace 与 Source 数据边界

真实 funding call、私人 source body、grant body、用户/主题/项目 memory body、artifact/package body 和 receipt instance 不进入 repo source。Repo 只保存可分发的产品知识、schema、locator、policy、descriptor、body-free refs 与 authority implementation。

个人与团队知识正文可以来自既有 Obsidian 等 Markdown 库，项目正文可以留在业务工作目录；没有个人库时，工作区共享知识和项目知识目录直接作为正文主源。来源由已有 Profile/Workspace 控制面绑定，知识身份与 scope 不依赖绝对路径。Framework 按权限和已接受版本直接冻结选中的正文，不要求工作区维护中间全文副本。项目资料、最终正文和分析成果具有自己的生命周期，不随运行缓存清理。

OPL 可以提供 workspace/source intake shell、locator/index 和 lifecycle transport；MAG 保持 source interpretation、grant truth、verdict 与 package authority。当前入口包括 [workspace_lifecycle_policy.json](../contracts/workspace_lifecycle_policy.json)、[artifact_locator_contract.json](../contracts/artifact_locator_contract.json)、[domain_descriptor.json](../contracts/domain_descriptor.json) 与 `domain-handler export`。新增 source helper 必须证明是 grant-native authority 或已有 caller 需要；generic intake/index/lifecycle helper 应上收到 OPL，不在 MAG 再建 wrapper。
