# 本地交付与 Portal 边界

本页只解释基金交付结果及其验收责任。业务完成语义见[项目定位](../project.md)，入口条件由[action catalog](../../contracts/action_catalog.json)定义。

| 结果 | 验收责任 |
| --- | --- |
| 科学上可评审的正文/待审包 | MAG fundability、authoring quality 与独立 Review evidence |
| 本地 submission-ready package | MAG package/export authority 消费 current review、release integrity 与 owner verdict |
| 外部 portal 已提交 | 独立、明确授权的人工作业和 portal receipt |

形式表单、客观补件与门户操作不取代正文质量判断；影响科学成立性的缺陷返回最早 owning Stage。最终 package Stage 只修 assembly、manifest 和 provenance projection，内容、source、quality closure、上游附件或既有 export verdict 的缺陷按 owner route-back。

## 四文件候选与验收

`package_and_submit_ready` 的同一 generation 包含 `artifact-bundle.json`、`final-package.json`、`hosted-contract-bundle.json` 和 `submission-ready-package.json`。Producer/helper 始终产生 `submission_ready=false` 候选，不能凭文件存在或机械完整性声称 ready。

[epistemic review profile](../../contracts/epistemic_review_scope_profile.json)声明 content、methodology、reference、display、export 和 package 的依赖。只复审缺少 current evidence 或依赖发生变化的 scope；layout/wrapper/metadata 变化不自动失效无关科学内容。Exact hashes 用于 transport identity 和独立 release integrity，不能代替语义判断。

OPL StageRunController 物化 identity-bound `opl_stage_review_receipt`。任何本地 readiness 投影还须同时消费 current scoped evidence、绑定所审 artifact 的 Review、匹配当前四文件 bytes 的 release integrity 和 MAG-owned export/owner verdict。Reviewer 与 OPL 都不能签 MAG owner receipt。没有可读结果时只能返回诊断；质量债、failed review 或机械完整性均不能越过 export gate。

## 人工作业

`submission_ready_export_gate` 与外部 portal submission 是不同授权。人工 portal 操作使用 `completed_and_wait_owner` 和 owner-issued `human_gate_ref`；不能编码成普通 typed blocker，也不能从本地 package 推导 portal 已接受。

机器 owner 为 [owner receipt contract](../../contracts/owner_receipt_contract.json)、[package knowledge](../../agent/knowledge/package_authority.md)、[export quality gate](../../agent/quality_gates/export_and_package.md)及 package/export 源码。Artifact body 留在 workspace/delivery root；OPL 只持有 locator、lifecycle transport 和 refs projection。
