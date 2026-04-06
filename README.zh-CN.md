<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**`Grant Foundry` 在医学场景下的未来实现 repo scaffold**

`Med Auto Grant` 是 `Grant Foundry` 在医学场景下的首个实现骨架。
它正在被定义为未来 `Grant Ops` 的医学 domain gateway 与 harness，第一阶段 MVP 聚焦医学场景下的 `NSFC` 通用申请骨架。

## 当前定位

- 当前阶段：repo scaffold，不是成熟 runtime
- domain 角色：未来作者侧、proposal-facing 的 `Grant Ops` surface
- 第一阶段 MVP：医学 `NSFC` 通用标书工作流
- 与 `Research Ops` 的关系：高度复用资产，但保持独立边界

## 统一执行方向

`Med Auto Grant` 继承 `OPL` 顶层冻结的执行原则：

- 默认采用 `Agent-first`，而不是 `fixed-code-first`
- 在同一套共享基座上支持两种模式：
  - `Auto`
  - `Human-in-the-loop`

这个系统的目标不是单纯把申请书章节补齐，而是围绕科学问题提纯、论证链构建、导师式批注与修订闭环来组织整个流程。

## 公开文档

- [Domain Positioning](./docs/domain-positioning.zh-CN.md)
- [MVP Scope](./docs/mvp-scope.zh-CN.md)

## 最小 Runtime

仓库现在已经包含一套最小 Python runtime scaffold，用来驱动已冻结的 `NSFCWorkspace` 契约。

快速试跑：

```bash
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_minimal.json
```

当前 CLI 范围：

- 校验冻结后的 `NSFCWorkspace` schema 子集与关键运行时约束
- 汇总当前选中的方向、科学问题、草稿与修订状态
- 根据 `lifecycle_stage`、`gates` 与导师批注 verdict 给出下一步路由建议
- 导出围绕 `60/30/10` 结构的导师批注摘要

## 内部文档

仓库内部设计、计划与开发细节默认仅维护中文，见：

- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md`](./docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
