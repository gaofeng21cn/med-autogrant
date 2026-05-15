# Post-R5A Revised Workspace Validator And Operator Alignment

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-10`

## 目标

在不打开 actual hosted runtime、`P5.A / P5.B`、same-repo `Human-in-the-loop`、`MCP / controller` public formal entry 的前提下，把 post-`R5.A` 本地 runtime hardening 的第一条 concrete delta 冻结成 repo-tracked truth：

- 让 `execute-revision-pass` 已 landed 的 revised workspace outputs 能被当前 validator / checkpoint / route surfaces 诚实接受；
- 让 public docs / operator walkthrough / command matrix 与当前已 landed 的本地 runtime ladder 对齐；
- 让 `grant_run_id / workspace_id / draft_id / program_id` 边界继续不漂移。

## 触发证据

这条 slice 的已关闭 concrete delta 来自 re-review 分支的 revised workspace：

1. `examples/nsfc_workspace_p2c_critique.json`
   - `execute-revision-pass` 输出后的 revised workspace 已能通过：
     - `validate-workspace`
     - `stage-route-report`
     - `summarize-workspace`
     - `critique-summary`
     - `next-step`
2. `examples/nsfc_workspace_p3b_re_review_major_revision.json`
   - `execute-revision-pass` 输出后的 revised workspace 先前会被上述 surfaces 拒绝，因为 validator 把 reviewed revision evidence 错误锚到最新 active draft version；
   - 当前 absorbed baseline 已能通过上述 surfaces，并保留下面固定版本链：
     - `reviewed_revision_plan.post_revision_version_label -> active_revision_plan.pre_revision_version_label -> active_draft.version_label(= active_revision_plan.post_revision_version_label)`

这说明已关闭的 drift 不在 `execute-revision-pass` 本身是否 landed，而在：

- validator 先前保留了“re-review evidence 的 `post_revision_version_label` 必须等于当前 active draft `version_label`”这一较早假设；
- 该假设无法覆盖 `R3.A` landed 之后的 re-review revised workspace output，因此当前 truth 明确要求 generated revised workspace 重新进入 validator / checkpoint / route surfaces。

## Hard Boundary

这份 truth 只收紧当前已 landed 的本地 runtime 合同，不改写以下边界：

- formal entry 仍只有 `CLI`
- `MCP` 仍只是 future protocol layer
- `controller` 仍只是 internal surface
- `build-hosted-contract-bundle` 仍只是 hosted-friendly contract export，不等于 actual hosted runtime
- `execute-revision-pass` 仍只做 section-level deterministic mutation
- `build-final-package` 仍只做本地 final package 组装
- 不进入 remote execution / Web UI / multi-tenant / billing / federation

## Revised Workspace Validation Truth

### A. critique re-review 输入态（执行前）

当 `lifecycle_stage=critique`、当前 active draft 已是 `status=revised`、且当前 active `RevisionPlan.execution_status=planned` 时：

- `MentorCritique.reviewed_revision_plan_id` 继续回答：
  - “这轮批注正在审阅哪一轮上一棒已完成修订证据”
- 被引用的 `RevisionPlan.post_revision_version_label`
  - 必须等于当前 active draft `version_label`

这保持 `P3.B` 已冻结的 re-review critique 输入语义不变。

### B. critique revised output（执行后）

当 `execute-revision-pass` 已对当前 active `RevisionPlan` 完成执行，并产出 revised workspace candidate 时：

- `active RevisionPlan.execution_status`
  - 必须为 `completed`
- active draft
  - `status` 必须为 `revised`
  - `version_label` 必须等于当前 active `RevisionPlan.post_revision_version_label`
- `MentorCritique.reviewed_revision_plan_id`
  - 若存在，继续回答“当前这轮批注原先审阅的是哪一轮上一棒 completed revision evidence”
  - 它不再要求与最新 active draft `version_label` 相等
- 被引用的 reviewed revision evidence
  - 必须继续 `completed`
  - `draft_id` 必须仍与当前 active draft 一致
  - `post_revision_version_label` 必须等于当前 active `RevisionPlan.pre_revision_version_label`

换句话说，re-review 执行后的最小版本链固定为：

`reviewed_revision_plan.post_revision_version_label -> active_revision_plan.pre_revision_version_label -> active_draft.version_label(= active_revision_plan.post_revision_version_label)`

这条链说明：

- `reviewed_revision_plan_id` 继续绑定“上一棒被当前批注审阅的已完成修订证据”；
- `active_revision_plan_id` 继续绑定“当前这一棒刚刚执行完成的修订计划”；
- 两者不互相替代。

## Checkpoint / Route Surface Truth

对满足上面版本链的 revised workspace output：

- `validate-workspace` 必须返回 `ok=true`
- `summarize-workspace` 必须继续回显：
  - `active_revision_plan`
  - `active_critique.reviewed_revision_plan_id`
  - `reviewed_revision_evidence`
- `critique-summary` 必须继续同时回显：
  - 当前 active `revision_plan_id`
  - `reviewed_revision_plan_id`
  - `reviewed_revision_evidence`
- `stage-route-report`
  - 必须继续聚合 `verification_checkpoint / checkpoint_status`
  - 不得因为保留 `reviewed_revision_plan_id` 而失败
- `next-step`
  - 继续沿现有 canonical critique route 产出 machine-readable recommendation
  - 本文不重新定义更高阶 critique synthesis 语义
- `runtime-run`
  - 对这类 revised workspace output 必须基于 route / checkpoint 继续运行
  - 不得退回 `validation_failed`
- `build-artifact-bundle`
  - 对这类 revised workspace output 必须继续可用
  - 输出 `manifest.draft_version_label` 必须与最新 active draft `version_label` 一致

## Canonical Local Operator Walkthrough

post-`R5.A` public/operator-facing 最小 walkthrough 至少要能清楚表达下面这条本地 ladder，而不是只列离散命令：

1. baseline audit surfaces
   - `validate-workspace`
   - `summarize-workspace`
   - `next-step`
   - `critique-summary`
   - `stage-route-report`
2. local runtime entry / recovery
   - `runtime-run`
   - `runtime-resume`
3. local artifact production
   - `build-artifact-bundle`
4. local revision execution
   - `execute-revision-pass`
   - 且 revised workspace output 还能重新进入 validator / route / artifact / runtime surfaces
5. local finalization / hostedization prep
   - `build-final-package`
   - `build-hosted-contract-bundle`

## Required Repo / Control-Surface Sync

closeout 这条 slice 时，至少要同步：

- repo-tracked truth：
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `README.md`
  - `README.zh-CN.md`
  - `docs/README.md`
  - 本文
- local active control plane：
  - `CURRENT_PROGRAM.md`
  - `PROGRAM_ROUTING.md`
  - active `PRD / test-spec / implementation`
  - `LATEST_STATUS.md`
  - `OPEN_ISSUES.md`
  - `ITERATION_LOG.md`

## Required Verification

至少覆盖：

- `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
- `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
- `python3 -m unittest discover -s tests -p 'test_artifact_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_revision_executor.py'`
- `python3 -m unittest discover -s tests -p 'test_final_package.py'`
- `python3 -m unittest discover -s tests -p 'test_hosted_contract_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- 当前 canonical CLI examples
- 至少一条 post-`R3.A` revised workspace walkthrough：
  - `execute-revision-pass` on `examples/nsfc_workspace_p3b_re_review_major_revision.json`
  - `validate-workspace` on revised output
  - `stage-route-report` on revised output
  - `build-artifact-bundle` on revised output
  - `runtime-run` on revised output
- `git diff --check`

## Honest Stop Conditions

若完成这条 slice 后：

- 已没有新的 validator / checkpoint / operator walkthrough concrete delta；
- 剩余事项已经需要 actual hosted runtime、`P5.A / P5.B` 或新的 formal entry；

则必须诚实回到：

- `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
