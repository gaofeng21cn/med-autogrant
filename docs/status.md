# 当前状态

本文只概括仓库实现及其证据边界。版本以 [pyproject.toml](../pyproject.toml) 和 [Package manifest](../contracts/opl_agent_package_manifest.json) 为准，发布与安装须另行回读其 owner。

## 仓内实现

[current-program](../contracts/runtime-program/current-program.json) 当前记录 `structural_cleanup_closed` 和 `external_owner_evidence_gated`：MAG 提供声明式 Grant Pack、direct domain handler 和领域 authority，通用运行与产品投影归 OPL。

| 实现面 | 当前代码或合同 |
| --- | --- |
| 用户入口 | [action catalog](../contracts/action_catalog.json) 的三个 Stage-bound action；[产品入口](./product/README.md)解释调用边界 |
| 阶段语义 | [六阶段 manifest](../agent/stages/manifest.json)、对应 prompt/policy、[quality cycle](../contracts/stage_quality_cycle_policy.json) |
| 直接 authority target | `medautogrant`、`MedAutoGrantDomainEntry` 和 [domain handler contract](../src/med_autogrant/product_entry_parts/domain_handler_contract.py)；不作为 Skill 的默认用户入口 |
| 通用 transport | [executor client](../src/med_autogrant/domain_executor_client.py) 与 funding source 调用 OPL Python helpers |
| Package dependency | `mas-scholar-skills` 为 required dependency；manifest 声明不能代替 provider 实际 presence/callability |
| 结构证据 | [conformance profile](../contracts/standard_agent_conformance_profile.json)、[source closure audit](../contracts/source_closure_audit.json)，需 fresh scanner 才能判断当前检查结果 |

仓内仍有 `hermes_agent` 的显式 critique executor 分支和行为测试；默认 executor 为 `codex_cli`。这仅说明当前 MAG 源码接受的请求类型，不证明任何外部 executor 已安装或可用。详见 [executor 边界](./specs/critique-executor.md)。

## 未闭合证据

[production acceptance](../contracts/production_acceptance/mag-production-acceptance.json) 与 [live progress](../contracts/live_stage_run_progress_evidence.json) 仍保留外部 owner evidence 缺口；完整清单、责任人与关闭条件只在[外部证据](./active/mag-ideal-state-cross-repo-gap-plan.md)维护。

因此不能由仓内结构清理、测试或源包版本推导 live grant、quality、export、submission、owner acceptance 或 production readiness。独立 Package publication、完整 runtime installed state、sustained App/default-caller consumption 和 provider long-soak 都须各自 owner 的实时回读。

验证命令见[文档索引](./README.md#验证)。完成记录和版本变化由 Git 保存；不向本页追加发行日志或历史测试计数。
