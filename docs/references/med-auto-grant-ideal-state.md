# Med Auto Grant 理想目标态

Owner: `Med Auto Grant`
Purpose: `north_star_reference`
State: `north_star_reference`
Machine boundary: 本文描述目标形态。当前机器状态归 contracts、schemas、source、workspace artifacts、receipts 与 `contracts/runtime-program/current-program.json`。

## 目标

`Med Auto Grant` 是生产级医学基金申请 domain agent。用户通过单一 `Med Auto Grant` app skill 调用它；OPL Framework 可以发现、托管、恢复和投影同一个 MAG Package。

MAG 的核心价值是 funding-call 解释、fundability strategy、specific aims、正文写作、独立 review/revision、quality closure、submission-ready local package、grant strategy memory 和 owner receipt。

```text
Declarative Grant Pack
  + OPL generated/hosted surfaces
  + minimal MAG authority functions
```

物理源码与这条分层一致：

- `agent/`：Stage、prompt、skill、knowledge 与 quality gate。
- `contracts/` 和 `schemas/`：action、artifact、memory、receipt、handoff 与 package interface。
- `src/med_autogrant/`：domain handler、authority functions、refs-only adapter 与 grant-native validation。

## Owner 分工

| Owner | 职责 |
| --- | --- |
| MAG | grant truth、fundability/quality/export verdict、package authority、memory accept/reject、typed blocker 与 owner receipt |
| OPL | StageRun、Attempt lifecycle、executor transport、queue/retry/resume、generated callers、operator projection 与 artifact lifecycle shell |
| Human | funding-call 决策、protected credentials、签字认证与外部 portal submission |
| Grant workspace | 用户材料、draft、critique、revision、quality report、receipts、memory writeback 与本地 package |

OPL 运输和投影 MAG refs；grant body、memory body、verdict 与 owner receipt 的写入仍由 MAG authority surface 完成。

## Stage Model

| Stage | 领域责任 | 主要输出 |
| --- | --- | --- |
| `call_and_candidate_intake` | funding call、资格、profile 与材料边界 | call/profile lock、source gap、candidate ref |
| `fundability_strategy` | 可资助性、竞争位置、风险与 reviewer fit | strategy artifact、fundability verdict/ref |
| `specific_aims_and_structure` | 科学问题、aims、创新点与论证结构 | aims outline、argument map、section skeleton |
| `proposal_authoring` | 正文、claim-evidence、方法和申请人适配 | draft artifact、progress refs |
| `review_and_rebuttal` | 独立诊断、缺陷归属与 route-back | critique、closure dossier、revision route |
| `package_and_submit_ready` | artifact assembly、本地 export gate 与 portal handoff | final package、gap report、export receipt |

Decisive Codex Attempt 选择语义 route，OPL StageRun controller 校验并物化 transition。MAG 的 professional skill 和 quality gate 定义基金专业依赖与 verdict 标准。

## Memory 与证据

Grant strategy memory 保存可复用的策略经验，并始终服从当前 funding call 与 source refs。OPL 持有 locator、consumed refs、proposal refs 和 receipt refs；MAG 持有 memory body 与 accept/reject decision。

每个真实 grant run 绑定明确 workspace、StageRun/Attempt identity 和 artifact refs。Quality、export、human gate 与 production 状态由各自 owner receipt 或 typed blocker 表达。

## 用户工作台

MAG 工作台围绕申请任务组织：

- `Status`：当前 funding call、Stage、owner、blocker 与 next action。
- `Workspace`：材料、profile、draft、evidence gaps 与待办。
- `Quality`：review findings、issue lineage、scorecard 与 closure state。
- `Artifacts`：draft、review packet、revision packet、final package 与 export receipts。
- `Memory`：consumed strategy refs、writeback proposal 与 accept/reject receipt。
- `Attention`：人工决定、补件、重新评审与 provider wait。

## 验收

- Direct MAG path 与 OPL-hosted path 返回同一 MAG owner surfaces。
- OPL standard conformance、source closure 和 generated interface readback 通过。
- 真实 workspace 产生 identity-bound owner receipts、quality movement、package/export receipt、memory receipt 或 typed blocker。
- Sustained App/operator consumption 与 provider long-soak 有 fresh evidence。
- 外部 portal submitted 状态由独立的人工作业回执确认。

当前尚缺的 owner evidence 见 [MAG 外部 Owner Evidence](../active/mag-ideal-state-cross-repo-gap-plan.md)。
