# 架构与责任边界

本文解释当前组件关系；强约束见[不变量](./invariants.md)，设计理由见[决策](./decisions.md)，运行证据见[状态](./status.md)。机器事实来自 contracts、源码和实际调用回执。

```text
User -> primary Skill / OPL-generated action
     -> OPL StageRun / executor transport
     -> MAG stage semantics and authority target
     -> grant workspace artifact + domain receipt refs
     -> OPL-generated status / App view
```

## 源码分层

| 位置 | 唯一职责 |
| --- | --- |
| `agent/` | Stage、prompt、professional skill、quality gate 与知识边界的声明式语义源 |
| `contracts/`、`schemas/` | Package、action、workspace、artifact、memory、review 和 receipt 的机器接口 |
| `src/med_autogrant/` | direct domain entry、authority function、refs adapter 与 grant-native helper |
| `runtime/` | runtime-facing descriptor/declaration；不保存运行输出或执行通用 scheduler |
| `plugins/med-autogrant/` | Codex 原生安装所需的 carrier source；[canonical Skill 投影](./references/primary-skill-plugin-carrier-boundary.md) |

[pack compiler input](../contracts/pack_compiler_input.json) 与 [source closure audit](../contracts/source_closure_audit.json) 声明实际 pack/source 分类。Framework 从 Stage manifest 和 action catalog 生成入口和 read model；MAG 不保存第二份 generated stage control plane。

## Package、Carrier 与 Executor

MAG owner 定义 Package identity、capability/dependency intent、grant task 和 typed views。配置的 Codex carrier 与 GHCR publication locator 在 [Package manifest](../contracts/opl_agent_package_manifest.json)；安装字节、完整 runtime health 与 publication currentness 由实际 carrier/owner 回读。

`mas-scholar-skills` 是 required dependency。普通组合按 identity presence/callability 判断；缺失只阻断 MAG。manifest 仍携带 `version_requirement` 与 `capability_abi` 等 provider 描述字段，其存在不是跨包版本求解或已安装状态的证明。具体调用要求由 [Scholar binding](../contracts/scholar_skill_binding_contract.json) 持有。

Framework 聚合 `opl packages install|update|uninstall mag` 动作和 carrier readback，App 消费该投影。MAG owner 独立推进本包 publication；本仓不维护用户 marketplace/symlink installer。Package 组合与 MAG submission artifact 的 exact-byte integrity 是不同边界，后者仍须独立验证。

跨仓平台实现和迁移由 [App 文档](https://github.com/gaofeng21cn/one-person-lab-app/tree/main/docs)与 [Framework 文档](https://github.com/gaofeng21cn/one-person-lab/tree/main/docs)各自持有，本仓不复制其他仓的兼容清单、阶段状态或删除授权。

## 调用与执行

[domain descriptor](../contracts/domain_descriptor.json) 声明 workspace locator/topology、runtime identity/registration、progress alias 和 routing signal。Hosted actions 来自 closed [action catalog](../contracts/action_catalog.json) 的 `stage_binding` 与 exact input schemas；用户面详见[产品入口](./product/README.md)。

Repo-local CLI 由声明式 parser metadata 与显式静态 dispatch 组成，最终调用同一 MAG authority target。`domain-handler export` 只输出 workspace identity/locator、action/Stage/handoff 与 authority/receipt refs；`domain-handler dispatch` 的允许动作由 [current-program](../contracts/runtime-program/current-program.json) 和 [handler contract](../src/med_autogrant/product_entry_parts/domain_handler_contract.py)持有，当前为 memory propose、memory decide 和 Stage closeout。

MAG 只构造 grant prompt/domain payload 并解析 typed closeout。所有 executor request 经 `opl_framework.executor_client.run_agent_execution_request`；临时请求文件、subprocess、timeout/cleanup 和 canonical receipt envelope 由 OPL 持有。MAG 构建只收集 `med_autogrant*`，验证环境经 clean runner 定位 Framework helpers。Funding source 也调用 `opl_framework.source_transport.fetch_text`；MAG 持有 NIH/NSFC 官方 URL allowlist、User-Agent、HTML 解析与领域 provenance。

## 领域 Authority

[pack compiler input](../contracts/pack_compiler_input.json) 定义 fundability、quality、export、package、memory accept/reject、owner receipt 与 grant-native helper 七项 authority。它们在 handler export 与审计合同间必须一致。OPL 可以运输、索引、恢复和投影 refs，不能写 grant/memory/package body、签 MAG owner receipt 或生成领域 verdict。

Decisive Codex Attempt 选择语义 route；OPL StageRun controller 校验角色、shape、evidence 与 declared target 后物化 transition。`ai_route_policy` 是声明式 route context，不是额外 authority。默认联合 authoring 与原子 route-back 见 [authoring](./specs/authoring.md)；独立评审和质量债见[质量边界](./specs/quality.md)。

## 数据与持久化

Workspace 持有真实申请材料、正文、版本和结果；运行面持有 Attempt/queue/receipt 等执行事实。`grant_run_id`、`workspace_id`、`draft_id` 与 `program_id` 不互相替代。详细存储位置见[数据边界](./source/README.md)，durable runtime 责任见[运行模型](./runtime/README.md)，最终 package/portal 责任见[交付](./delivery/README.md)。
