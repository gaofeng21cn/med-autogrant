# 文档导航与维护

本页负责导航、文档分工与生命周期。文档解释当前代码和合同，不作为 runtime、测试或脚本的语义接口。

## 按问题阅读

| 问题 | 唯一人读入口 |
| --- | --- |
| MAG 服务谁、做到哪里 | [项目定位](./project.md)；[首页](../README.zh-CN.md)负责安装和开始使用 |
| 仓内已实现什么、哪些运行结论尚不能声明 | [当前状态](./status.md) |
| 哪个组件或仓库负责什么 | [架构](./architecture.md) |
| 哪些约束不能被破坏 | [不变量](./invariants.md) |
| 为什么采用这些设计 | [决策](./decisions.md) |
| 还缺什么真实外部证据、由谁关闭 | [外部证据](./active/mag-ideal-state-cross-repo-gap-plan.md) |
| 用户 action 与内部 target 如何区分 | [产品入口](./product/README.md) |
| durable runtime 与本机状态如何分开 | [运行模型](./runtime/README.md) |
| 工作区数据放在哪里 | [数据边界](./source/README.md) |
| 本地 package 到人工 portal 的交付边界 | [交付](./delivery/README.md) |
| authoring、review 与 executor 如何工作 | [技术规格](./specs/README.md) |
| memory 与 Skill carrier 的专项说明 | [参考](./references/README.md) |
| 机器字段与定位符 | [contracts](../contracts/README.md) |

## 生命周期

每个主题只有一个当前正文 owner。新增或修改文档前先定位读者、用途、源码/合同和现有 owner；只有独立的读者任务或稳定技术边界才新增页面。上层页面概括子主题并链接详细 owner，不复制 action 清单、阶段状态或验收表。中英文首页保持相同使用边界。

实现或合同变化时，同一次修改更新 owner 正文及全部入链。状态页仅保留当前实现摘要；未闭合证据由 active 页唯一维护，证据到达时先更新真实 owner surface，再收敛对应文档。设计记录只保留仍影响后续选择的理由，不追加已完成工作清单。

删除或合并页面前逐节检查仍有效的条件、角色、失败语义、权限和未闭合证据，把独有内容移交当前 owner，并修复文档、合同、源码和测试的引用。已替代方案、结束计划、旧接口/模块/测试的说明直接退出当前文档；历史从 Git 读取，不保留兼容页、tombstone 或重复 archive 正文。实际源码仍支持的接口必须如实说明；退役实现需由其代码 owner 处理真实 caller，不能仅靠删文档宣告完成。

文档语义由维护者结合合同、源码、调用者和验证结果判断。机器检查仅验证 schema/格式、链接与资源存在性、可执行示例、载体完整性和安全边界；关键词、固定章节、长度或测试计数不能证明内容正确。

## 验证

`scripts/verify.sh` 是公开 wrapper，[Makefile](../Makefile)持有 lane 组合。Python/pytest 经 clean runner 将 cache/bytecode 放在 checkout 外；需要 Framework helpers 时使用显式 `OPL_FRAMEWORK_ROOT` 或已安装的 `opl` launcher。

```bash
./scripts/verify.sh
./scripts/verify.sh structure
./scripts/verify.sh full
```

默认 fast lane 单次收集非 meta、非 regression 测试；`smoke` 检查 CLI，`regression` 检查较重行为，`meta` 检查仓库与 descriptor。`cleanup` 是显式清理动作，普通检查不会删除 ignored 文件。文档改动先做链接/资源与 `git diff --check`；改变 agent 可消费语义时运行对应 descriptor 和行为验证。需要结构 currentness 时再从 Framework 执行 `agents check`、`interfaces`、`source-closure` 或 `conformance`；这些结果不替代真实领域和生产验收。
