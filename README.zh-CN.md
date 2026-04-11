<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**面向申请人侧 `NSFC` 风格申请的医学基金主线（开发中）**

> 当前状态：仓库当前执行 `Runtime Productization Program`；预冻结的本地 `R1 -> R5` runtime ladder 已吸收到 `R5.A / Hosted-Friendly Session Boundary`。当前已具备本地 `CLI-first + host-agent` runtime baseline，但仍不是 actual hosted runtime，也不是 submission-ready 的自动驾驶产品。

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
      本地 <code>R1 -> R5</code> runtime ladder 已吸收至 <code>R5.A</code>，当前保持 <code>baseline freeze / runtime hardening</code>
    </td>
  </tr>
</table>

## 一句话理解

如果你的目标是把申请人履历、既有成果、在研项目、预实验结果和候选方向，收敛成一条更像样的 `NSFC` 风格基金申请主线，`Med Auto Grant` 正在被构建成共享 `Unified Harness Engineering Substrate` 之上的医学 `Grant Ops` `Domain Harness OS`，用于承载可治理、可审计、可持续修订、并能显式回看上一轮修订证据的主线流程。

## Runtime 形态（当前与未来）

- 当前默认本地执行形态：`Codex-default host-agent runtime`。
- 当前仓库最小 baseline 以该 host-agent 形态为默认落地与验证对象。
- 其 formal-entry matrix 已固定为：默认正式入口 `CLI`、支持协议层 `MCP`（当前保留为 future layer，尚未 repo-verified）、内部控制面 `controller`。
- 当前仓库主线按 `Auto-only` 理解；未来如果要做 `Human-in-the-loop` 产品，应作为兼容 sibling 或 upper-layer product 复用同一 substrate，而不是把当前仓改成同仓双模。
- 未来兼容形态：如果核心 domain contract 不变，可迁移到同一 substrate 上的 managed web runtime。

## 执行句柄与持久表面

- `grant_run_id`：单次 hydrated grant run 的正式执行句柄
- `workspace_id`：当前 `NSFCWorkspace` 的持久聚合根身份
- `draft_id`：跨 critique / revision 延续的草稿身份，而不是每次 run 重新生成的 ID
- `program_id`：当前 Med Auto Grant active mainline 的 control-plane / report-routing 指针
- 当前 repo-verified 的 durable report / audit surface：`summarize-workspace`、`critique-summary`、`stage-route-report`
- 当前 repo-verified 的本地 runtime entry 还包括 `run-local`、`resume-local`、`build-artifact-bundle`、`execute-revision-pass`、`build-final-package` 与 `build-hosted-contract-bundle`；它们分别负责本地主循环与恢复、artifact bundle 生产、section-level deterministic revision pass、本地 final package 导出，以及 hosted-friendly contract bundle 导出
- `stage-route-report` 当前还是 machine-readable 的 verification / checkpoint 聚合面，并会输出 `verification_checkpoint` 与 `checkpoint_status`
- repo-tracked review truth 与 local durable handoff surfaces 必须分开：前者负责解释 runtime contract，后者负责机器私有的恢复状态

## 它主要想帮你解决什么问题

- 判断一个方向到底是不是“真正的科学问题”，而不是工程任务或泛泛的临床需求。
- 把申请人画像、代表作、在研项目和预实验，组织进同一个可审计的基金工作区。
- 在花大力气写全文之前，先把“必要性与科学价值”这条主线磨清楚。
- 让“为什么是这个申请人来做这个问题”成为显式判断，而不是简历堆砌。
- 用“草稿扩写 + 导师式批注 + 结构化修订 + re-review 证据绑定”替代一次性文本生成。

## 现在已经能做什么

仓库已经有一套围绕冻结 `NSFCWorkspace` 契约的最小可运行底座，默认运行在当前 `Codex-default host-agent runtime` 形态上。

当前 runtime 已经可以：

- 校验已 absorbed 的 `drafting -> critique -> revision` 主线，并保留 `major_reframe / major_revision / minor_revision / ready_for_submission` 的导师 verdict 分叉
- 在 CLI 输出中统一携带稳定的 `grant_run_id`，作为当前 hydrated grant run 的正式执行句柄
- 汇总 direction / question / fit mapping / draft / revision plan 的显式 `current_selection` 绑定
- 通过 `MentorCritique.reviewed_revision_plan_id` 把 re-review 批注显式绑定到上一轮 completed revision evidence
- 根据 `lifecycle_stage`、gates 与 verdict 给出 `major_reframe -> question_refinement`、`major_revision / minor_revision -> revision`、`ready_for_submission -> frozen`，以及 `revision(completed) -> critique -> revision` 的下一步建议
- 把当前 authoring route 聚合成单个 machine-readable `stage-route-report`
- 通过 `verification_checkpoint / checkpoint_status` 把当前 verification、forced rollback 与 frozen gate 语义收进同一个 checkpoint surface
- 输出带有 verdict、当前 `RevisionPlan.execution_status`、reviewed revision evidence、rollback / frozen gate 状态、版本标签和比较证据的 `critique-summary / stage-route-report` 审计面
- 通过 `run-local` 运行一次本地主循环、派生 machine-readable `stop_reason`、在 `stage_action_required` 分支上生成 machine-readable `stage_action_envelope`、写入 durable run journal，并通过 `resume-local` 从该 journal 恢复
- 通过 `build-artifact-bundle` 把当前已选方向、问题、论证链、适配度、提纲与草稿章节打包成 local `artifact_bundle`，并保留 manifest、lineage、version 与 `grant_run_id / workspace_id / draft_id` 身份一致性
- 通过 `execute-revision-pass` 对冻结在 `RevisionPlan` 中的 section-level deterministic mutation 执行本地 revision pass，并保持 draft lineage、rollback gate 与 checkpoint 语义不漂移
- 通过 `build-final-package` 把 freeze-ready / submission-frozen 的 workspace 与 artifact bundle 收成 machine-readable 本地 `final_package`
- 通过 `build-hosted-contract-bundle` 从当前 `final_package` 导出 hosted-friendly 的 session / state / artifact / audit contract bundle，作为托管化 prep 的本地合同产物

## 现在还没有完成什么

下面这些能力仍处于后续 hardening 或 future scope：

- 当前本地 runtime 仍需继续做 submission-grade hardening 与更高判断密度的 authoring runtime 收束，但 canonical 本地 walkthrough 与 revised/final/hosted 输出一致性 truth 已冻结
- actual hosted runtime、remote execution、Web UI 与 multi-tenant 托管化
- 未来 `Human-in-the-loop` sibling 或 upper-layer product 相关表面
- submission-grade 自动驾驶质量与更强的端到端 authoring/runtime 稳定性
- 超出首个 `NSFC` 通用骨架之外的更多基金 family 扩展，以及 `P5` federation

## 最快开始方式：通过你的 Agent

对大多数医学用户来说，最快的入口不是先学习底层命令，而是先把你的申请材料和目标交给自己的 Agent，再让它调用 `Med Auto Grant`。

通常可以这样开始：

1. 准备申请人材料、代表性成果、在研项目、预实验结果和目标基金要求。
2. 让 Agent 先把这些材料整理成结构化、可审计的 grant workspace。
3. 再让 Agent 用 `Med Auto Grant` 去推进科学问题提纯、必要性链条收紧、草稿扩写、导师式批注、修订与 re-review 证据绑定。

你可以直接把下面这段话发给 Agent：

> 请先读取这个工作区里的申请人材料、既有成果、在研项目、预实验结果和目标基金要求，并把它们整理成结构化、可审计的 grant workspace。然后使用 Med Auto Grant 作为医学 Grant Ops 主线来推进这份 NSFC 风格申请。请优先判断科学问题是否成立、必要性与科学价值是否足够、申请人与问题是否真正适配、草稿是否忠实继承已冻结问题、上一轮修订证据是否被当前批注显式承接，再进入 submission-facing 的更后段动作。如果当前方向偏弱，请及时止损、改题或指出缺失证据，而不是机械地把一条弱路线写到底。

## 公开文档

- [文档索引](./docs/README.zh-CN.md)
- [Domain Positioning](./docs/domain-positioning.zh-CN.md)
- [MVP Scope](./docs/mvp-scope.zh-CN.md)

## 开发验证

```bash
uv sync --frozen
make test-full
```

本地测试分层入口：

- `make test-fast`：默认开发切片
- `make test-meta`：program control 与 repository hygiene 检查
- `make test-cli-smoke`：CLI 校验与本地 runtime smoke
- `make test-full`：clean-clone 基线使用的完整验证入口

<details>
<summary><strong>技术与 Agent 说明</strong></summary>

### 最小 Runtime 命令

```bash
TMPDIR="$(mktemp -d)"

# 当前 canonical post-R5A 本地 walkthrough（真相来源：
# docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md）

# 1. 对 critique workspace 做 baseline 审计
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_critique.json --format json

# 2. 执行 deterministic local revision pass
PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json --output "$TMPDIR/r3a-p2c-revised.json" --format json

# 3. 对 generated revised workspace 做 fresh validator / summary / route / checkpoint
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant next-step --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input "$TMPDIR/r3a-p2c-revised.json" --format json

# 4. re-review revised output 也必须留在同一条本地 ladder 上
PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p3b_re_review_major_revision.json --output "$TMPDIR/r3a-p3b-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input "$TMPDIR/r3a-p3b-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input "$TMPDIR/r3a-p3b-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant next-step --input "$TMPDIR/r3a-p3b-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input "$TMPDIR/r3a-p3b-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input "$TMPDIR/r3a-p3b-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input "$TMPDIR/r3a-p3b-revised.json" --output "$TMPDIR/r3a-p3b-revised-bundle.json" --format json
PYTHONPATH=src python3 -m med_autogrant run-local --input "$TMPDIR/r3a-p3b-revised.json" --journal "$TMPDIR/r3a-p3b-revised-run.json" --format json

# 5. 本地 runtime 入口 / 恢复继续保持 CLI-first
PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p2c_revision.json --journal "$TMPDIR/r1a-revision.json" --format json
PYTHONPATH=src python3 -m med_autogrant resume-local --journal "$TMPDIR/r1a-revision.json" --format json

# 6. 本地 final / hosted-contract 产物链
PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output "$TMPDIR/r5a-bundle.json" --format json
PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle "$TMPDIR/r5a-bundle.json" --output "$TMPDIR/r5a-final-package.json" --format json
PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle --final-package "$TMPDIR/r5a-final-package.json" --output "$TMPDIR/r5a-hosted-contract.json" --format json
```

### 当前技术范围

- 基于 schema 的 `NSFCWorkspace` 校验
- runtime / CLI 表面上显式区分 `grant_run_id`、`workspace_id` 与 `draft_id`
- `major_reframe / major_revision / minor_revision / ready_for_submission` 的 machine-readable verdict contract
- 通过 `active_revision_plan_id`、`reviewed_revision_plan_id` 与 `reviewed_revision_evidence` 冻结 machine-readable re-review linkage
- 通过 `forced_rollback_stage`、`forced_rollback_reason` 与 `presubmission_frozen` 冻结 machine-readable rollback / gate contract
- machine-readable 的批注、verdict 与 route artifact
- machine-readable 的本地 runtime stop reason、stage-action envelope 与 durable run-journal recovery
- 带有 manifest、lineage、version 与 bundle summary 的 machine-readable 本地 artifact bundle 生产
- section-level deterministic 本地 revision executor
- machine-readable 的本地 final package
- hosted-friendly session / state / artifact / audit contract bundle 导出
- 覆盖 runtime 与 control-surface 不变量的测试

### 内部文档

- 当前 canonical post-R5A walkthrough truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
- [`docs/domain-harness-os-positioning.md`](./docs/domain-harness-os-positioning.md)
- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`](./docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md)
- [`docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`](./docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md)
- [`docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`](./docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md)
- [`docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`](./docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md)
- [`docs/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`](./docs/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md)
- [`docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md`](./docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md)
- [`docs/history/omx/README.zh-CN.md`](./docs/history/omx/README.zh-CN.md)

### 本地运行状态

本地 operator 与 runtime 状态属于机器私有内容，不属于公开 GitHub 源码表面。
</details>
