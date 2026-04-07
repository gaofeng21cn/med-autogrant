<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**面向申请人侧 `NSFC` 风格申请的医学基金主线（开发中）**

> 当前状态：仓库已进入 `P2 / NSFC Authoring Mainline Freeze`，当前 active tranche 为 `P2.A / Intake-Direction-Question Mainline`；它仍不是可直接替代人工判断的成熟基金写作系统，也不是 submission-ready 的自动驾驶产品。

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>面向谁</strong><br/>
      需要准备基金申请的医学研究者、临床团队、青年教师与 PI
    </td>
    <td width="33%" valign="top">
      <strong>它是什么</strong><br/>
      共享 <code>Unified Harness Engineering Substrate</code> 之上，面向申请人侧、proposal-facing 的医学 <code>Grant Ops</code> <code>Domain Harness OS</code> 方向/系统
    </td>
    <td width="33%" valign="top">
      <strong>当前成熟度</strong><br/>
      已有最小 runtime baseline，当前 active tranche 已切到 <code>P2.A / Intake-Direction-Question Mainline</code>
    </td>
  </tr>
</table>

## 一句话理解

如果你的目标是把申请人履历、既有成果、在研项目、预实验结果和候选方向，收敛成一条更像样的 `NSFC` 风格基金申请主线，`Med Auto Grant` 正在被构建成共享 `Unified Harness Engineering Substrate` 之上的医学 `Grant Ops` `Domain Harness OS`，用于承载可治理、可审计、可持续修订的主线流程。

## Runtime 形态（当前与未来）

- 当前默认本地执行形态：`Codex-default host-agent runtime`。
- 当前仓库最小 baseline 以该 host-agent 形态为默认落地与验证对象。
- 未来兼容形态：如果核心 domain contract 不变，可迁移到同一 substrate 上的 managed web runtime。

## 它主要想帮你解决什么问题

- 判断一个方向到底是不是“真正的科学问题”，而不是工程任务或泛泛的临床需求。
- 把申请人画像、代表作、在研项目和预实验，组织进同一个可审计的基金工作区。
- 在花大力气写全文之前，先把“必要性与科学价值”这条主线磨清楚。
- 让“为什么是这个申请人来做这个问题”成为显式判断，而不是简历堆砌。
- 用“导师式批注 + 结构化修订”替代一次性文本生成。

## 现在已经能做什么

仓库已经有一套围绕冻结 `NSFCWorkspace` 契约的最小可运行底座，默认运行在当前 `Codex-default host-agent runtime` 形态上。

当前 runtime 已经可以：

- 校验 `input_intake`、`direction_screening`、`question_refinement` 三段结构化 `NSFC` workspace
- 在 CLI 输出中统一携带稳定的 `grant_run_id`，作为当前 hydrated grant run 的正式执行句柄
- 汇总 intake artifact，以及 direction / question 的显式 `current_selection` 绑定
- 根据 `lifecycle_stage` 与 gates 给出 `input_intake -> direction_screening -> question_refinement -> argument_building` 的下一步建议
- 把早段 route 聚合成单个 machine-readable `stage-route-report`
- 在存在后段 workspace 时，继续保留结构化 `critique-summary` 与 later-stage baseline 检查

## 现在还没有完成什么

下面这些能力仍处于规划或开发中：

- 从 argument building 到稳定 draft 的完整 authoring loop
- `revision` 阶段内部更细粒度的草稿版本切换建模
- human-in-the-loop gate 与 submission-grade 交付面
- 超出首个 `NSFC` 通用骨架之外的更多基金 family 扩展

## 最快开始方式：通过你的 Agent

对大多数医学用户来说，最快的入口不是先学习底层命令，而是先把你的申请材料和目标交给自己的 Agent，再让它调用 `Med Auto Grant`。

通常可以这样开始：

1. 准备申请人材料、代表性成果、在研项目、预实验结果和目标基金要求。
2. 让 Agent 先把这些材料整理成结构化、可审计的 grant workspace。
3. 再让 Agent 用 `Med Auto Grant` 去推进科学问题提纯、必要性链条收紧、导师式批注和修订。

你可以直接把下面这段话发给 Agent：

> 请先读取这个工作区里的申请人材料、既有成果、在研项目、预实验结果和目标基金要求，并把它们整理成结构化、可审计的 grant workspace。然后使用 Med Auto Grant 作为医学 Grant Ops 主线来推进这份 NSFC 风格申请。请优先判断科学问题是否成立、必要性与科学价值是否足够、申请人与问题是否真正适配，再进入草稿扩写。如果当前方向偏弱，请及时止损、改题或指出缺失证据，而不是机械地把一条弱路线写到底。

## 公开文档

- [文档索引](./docs/README.zh-CN.md)
- [Domain Positioning](./docs/domain-positioning.zh-CN.md)
- [MVP Scope](./docs/mvp-scope.zh-CN.md)

<details>
<summary><strong>技术与 Agent 说明</strong></summary>

### 最小 Runtime 命令

```bash
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_minimal.json
```

### 当前技术范围

- 基于 schema 的 `NSFCWorkspace` 校验
- runtime / CLI 表面上显式区分 `grant_run_id`、`workspace_id` 与 `draft_id`
- critique、revision、frozen 等后段 route 的运行时一致性检查
- machine-readable 的批注与 route artifact
- 覆盖 runtime 与 control-surface 不变量的测试

### 内部文档

- [`docs/domain-harness-os-positioning.md`](./docs/domain-harness-os-positioning.md)
- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`](./docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
- [`docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md`](./docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)

### 本地运行状态

本地 operator 与 runtime 状态属于机器私有内容，不属于公开 GitHub 源码表面。

</details>
