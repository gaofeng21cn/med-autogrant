# 文档索引

[English](./README.md) | **中文**

这里是 `Med Auto Grant` 的双语文档索引，也是默认的对外公开入口。
内容与项目真相一致：该仓库在共享 `Unified Harness Engineering Substrate` 上承载面向医学 `Grant Ops` 的领域承载操作系统（Domain Harness OS），当前处于 baseline freeze（基线冻结）/runtime hardening（运行时强化）阶段。

## 统一文档治理

- 所有对外文档都必须同时提供英文 `.md` 与中文 `.zh-CN.md`，并保持同步更新。
- 内部设计、规划与备忘文档默认使用中文，除非明确提升到公开面后再补充英文。
- 术语可以保留英文，但要避免无意义的中英混写，保证语言连贯。
- `docs/README*` 的结构与措辞应保持一致，帮助快速区分双语公开面与内部参考文档。
- 更多细节请参考 [文档治理规则](documentation-governance.md)。

## 默认对外双语公开面

- [仓库首页](../README.zh-CN.md)
- [领域定位](./domain-positioning.zh-CN.md)
- [MVP 范围](./mvp-scope.zh-CN.md)

这一索引与仓库首页一起构成默认的双语公开面。

## 仓库跟踪的内部设计与规划文档

以下文档主要是内部设计参考，默认以中文维护。

- [Domain Harness OS 定位映射](./domain-harness-os-positioning.md)
- [顶层设计](./specs/2026-04-06-med-auto-grant-top-level-design.md)
- [NSFC 主流程与导师批注闭环](./specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [对象模型 Schema V1](./specs/2026-04-06-object-model-schema-v1.md)
- [主线与 OMX Bridge](./specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
- [最小 Scaffold 计划](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [文档治理规则](documentation-governance.md)

## 建议阅读顺序

1. 先看 [领域定位](./domain-positioning.zh-CN.md)。
2. 再看 [MVP 范围](./mvp-scope.zh-CN.md)。
3. 只有在需要架构、Schema 或执行细节时，再阅读内部设计文档。

## 状态说明

`Med Auto Grant` 仍在积极开发中，已有最小 runtime baseline。
当前成熟度保持在 `baseline freeze / runtime hardening`，完整的基金申请 authoring runtime 尚未完成。

## 文档边界

- `README*` 与 `docs/README*`：默认的双语对外公开面。
- `docs/domain-harness-os-positioning.md`、`docs/specs/**` 与 `docs/plans/**`：默认的内部技术/设计文档。
- 对外公开文档必须同步提供英文与中文镜像。
- 内部技术、规划与备忘文档默认使用中文。
- 避免无意义的中英混写；英文只保留给固定术语、路径、命令与代码标识符。
