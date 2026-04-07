# Med Auto Grant 对象模型 Schema V1

> 当前文档面向内部 schema 冻结，只保留中文版本。

Date: `2026-04-06`

## 目标

冻结 `Med Auto Grant` 第一版对象模型 schema，使后续 runtime、controller、批注闭环与状态机设计都建立在同一套 machine-readable 对象边界之上。

这份冻结不是在做“所有未来对象的一次性大全”，而是在做第一版 `NSFC` 通用 MVP 的最小严格对象集。

## 设计原则

第一版 schema 只冻结满足以下条件的对象：

- 已经在顶层设计与主流程文档里稳定出现
- 会在多个流程阶段反复被引用
- 不应该继续藏在 prompt 文本里
- 适合作为 audit-friendly 的显式结构对象

不满足这些条件的对象先延后，而不是为了追求“完整感”强行塞进去。

## 文件结构

第一版 schema 冻结为：

- `schemas/v1/common.schema.json`
- `schemas/v1/applicant-profile.schema.json`
- `schemas/v1/track-record.schema.json`
- `schemas/v1/active-project-set.schema.json`
- `schemas/v1/preliminary-evidence-pack.schema.json`
- `schemas/v1/funding-opportunity-brief.schema.json`
- `schemas/v1/direction-hypothesis.schema.json`
- `schemas/v1/scientific-question-card.schema.json`
- `schemas/v1/argument-chain.schema.json`
- `schemas/v1/application-draft.schema.json`
- `schemas/v1/mentor-critique.schema.json`
- `schemas/v1/revision-plan.schema.json`
- `schemas/v1/nsfc-workspace.schema.json`
- `schemas/v1/schema-index.json`

其中：

- `nsfc-workspace.schema.json` 是聚合根
- 其他对象都是聚合根下的核心子对象
- `schema-index.json` 是第一版 schema registry

## 为什么是这些对象

### 必须独立成 schema 的对象

- `ApplicantProfile`
  因为整个系统都在回答“这个申请人凭什么做这个问题”。

- `TrackRecord`
  它不是简历文本，而是申请人既有成果与适配度证据的结构化入口。

- `ActiveProjectSet`
  方向收敛与可复用资产判断离不开它。

- `PreliminaryEvidencePack`
  预实验不是草稿附件，而是决定是否允许继续推进的重要 gate 输入。

- `FundingOpportunityBrief`
  即使 MVP 聚焦 `NSFC`，资助机会本身也不该藏在写作模板里。

- `DirectionHypothesis`
  方向候选是主流程早期的核心状态，必须显式可审计。

- `ScientificQuestionCard`
  这是整个系统的中心对象，不独立出来就无法严格区分科学问题与工程任务。

- `ArgumentChain`
  立项依据不是正文段落堆砌，而是一条可审查的链条。

- `ApplicantFitMapping`
  申请人与问题的适配度不能只靠履历散文；它必须是可链接、可验证、可冻结的结构对象。

- `ApplicationDraft`
  草稿必须和被冻结的问题与链条显式绑定。

- `MentorCritique`
  导师批注要能结构化进入修订闭环，而不是停留在自然语言散文。

- `RevisionPlan`
  修订计划是 critique -> revision loop 的执行入口。

### 聚合根为什么是 `NSFCWorkspace`

第一版不是直接把每个对象都当平行资源散放，而是用 `NSFCWorkspace` 作为聚合根。

这样做的原因是：

- 现在聚焦的是一个 `NSFC` 申请工作区，而不是通用对象仓库
- `Auto` / `Human-in-the-loop`、lifecycle stage、gates 都应该挂在同一个 workspace 上
- 方向、问题、链条、草稿、批注、修订之间需要同处一个显式边界

## 当前延后的对象

以下对象暂时不在 V1 冻结：

- `ExecutionTrace`
- `GateStateMachine`
- `SectionLevelEvidenceGraph`
- `CrossCycleDiffArtifact`
- `ReviewerSimulationPack` 作为独立对象

原因不是它们不重要，而是：

- 现在先冻结 grant authoring loop 的核心对象
- 上述对象仍然更像后续 controller / audit / diff 层的派生对象
- 过早冻结会把第一版 schema 范围拉得过大

## 关系结构

第一版最关键的关系是：

- `DirectionHypothesis` -> `ScientificQuestionCard`
- `ScientificQuestionCard` -> `ArgumentChain`
- `ArgumentChain` -> `ApplicantFitMapping`
- `ScientificQuestionCard` -> `ApplicationDraft`
- `ApplicantFitMapping` -> `ApplicationDraft`
- `ApplicationDraft` -> `MentorCritique`
- `MentorCritique` -> `RevisionPlan`

同时，以下输入对象为上游支撑层：

- `ApplicantProfile`
- `TrackRecord`
- `ActiveProjectSet`
- `PreliminaryEvidencePack`
- `FundingOpportunityBrief`

## 执行句柄与对象 ID 边界

`NSFCWorkspace` 作为聚合根，当前同时承载两类不能混写的标识：

- `grant_run_id`
  - 当前 hydrated grant run 的稳定执行句柄
  - 用于 CLI 输出、reports 与恢复入口回显同一次运行
  - 不是 workspace 主键，也不是草稿身份
- `workspace_id`
  - grant workspace 聚合根身份
  - 表示“哪一个工作区对象”而不是“哪一次运行”
- `draft_id`
  - `ApplicationDraft` 身份
  - 即使 `revision` 完成后显式从 `draft -> revised` 切换，也继续沿用同一 `draft_id`
- `program_id`
  - `.omx` 控制面上的长期 mainline 句柄
  - 负责把 reports 与 control surface 路由到同一 active program，而不是指向某一次 runtime run

第一版 schema 的最小合同是：`grant_run_id` 进入 `NSFCWorkspace` 聚合根；runtime 与 CLI 必须稳定回显它，但不因此把 `workspace_id`、`draft_id`、`program_id` 混成同一种 ID。

## current_selection 的阶段相关合同

`NSFCWorkspace.current_selection` 当前不再被解释成“永远已经进入后段”的固定形态，而是阶段相关合同：

- `selected_direction_id`
  - 在 `direction_screening` 起成为显式绑定
- `selected_question_id`
  - 在 `question_refinement` 起成为显式绑定
- `active_fit_mapping_id`
  - 在 `fit_alignment` 起成为显式绑定
- `active_draft_id`
- `active_revision_plan_id`
  - 保留为 downstream identity 槽位，不属于当前 `P2.A` hard gate

这意味着：

- `input_intake` 允许空 `current_selection`
- `direction_screening` 先冻结 direction 绑定
- `question_refinement` 再冻结 direction/question 双绑定
- `fit_alignment` 再冻结 applicant-problem fit mapping
- `outline` 再冻结 draft outline 与 object linking
- `ArgumentChain`、`ApplicationDraft`、`MentorCritique`、`RevisionPlan` 不再作为早段无条件必填

## 第一版 schema 的边界

这次冻结强调的是：

- 对象边界
- 必填字段
- 核心关系
- 聚合根

这次不强调：

- 最优字段命名是否永久不变
- 所有枚举是否已经穷尽未来情况
- runtime 内部如何映射成 Python 类

如果未来要改，也必须在“保持顶层边界不漂移”的前提下做版本化升级。

## 最小验证

本轮配套了一个不依赖第三方库的最小测试：

- `tests/test_schema_registry.py`

它当前验证：

- 核心 schema 文件是否齐全
- 每个 schema 是否能被解析为合法 JSON
- 非 index schema 是否带有最基本的 metadata
- 本地 `$ref` 是否可解析
- 聚合根是否引用全部核心对象

## 下一步

在 V1 schema 冻结后，下一步再推进：

- Python 对象映射层
- gate 状态机
- critique / revision 数据流
- workspace 样例与 round-trip 校验
