# Post-R5A 本地 Runtime Hardening Brief

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_post_r5a_local_runtime_hardening_brief_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-09 post-R5A local runtime hardening owner line 与 honest-stop 前置判断。当前 default task runtime owner 是 OPL/Temporal，MAG 不持有 daemon、scheduler、attempt loop 或 attempt ledger；post-R5A local runtime、journal、host-agent、Gateway 与 hostedization wording 只作 provenance。当前 runtime owner、stage executor、package/export authority 与机器行为以核心五件套、active gap plan、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

日期锚点：`2026-04-09`

## 文档目的

这份 brief 冻结 `R5.A / Hosted-Friendly Session Boundary` 已本地落地之后，下一条最诚实的 `OMX` owner line。

它只回答一个问题：

- 当前预冻结的本地 `R1 -> R5` runtime ladder 已经吸收后，在不打开 `P5` 的前提下，下一条 truthful OMX 线应该是什么？

这份文档**不是**：

- “actual hosted runtime 已进入当前 scope”的声明；
- “下一步就该直接打开 `P5.A / P5.B`”的声明；
- formal-entry matrix 的改写；
- `R1 -> R5` runtime-first boundary map 的改写。

## 当前诚实位置

截至当前 absorbed baseline：

- `runtime-run`
- `runtime-resume`
- `build-artifact-bundle`
- `execute-revision-pass`
- `build-final-package`
- `build-hosted-contract-bundle`

都已经作为本地 `CLI-first` runtime surface 落地。

这意味着，旧问题已经不是：

- “怎么从 `R1.B` 走到后面的 runtime ladder？”

当前真正的问题是：

- “在不假装已经进入 actual hosted runtime 或 `P5` 的前提下，怎样让已经 landed 的本地 runtime 保持诚实、可用、且口径一致？”

## 建议新线

当前建议的 `OMX` owner line 是：

- `post-R5A local runtime hardening`

这条线仍然**严格停留在**已经 landed 的本地 runtime productization 范围内。

它：

- 不打开新的 `R6`
- 不打开 `P5`

## 目标

围绕 `R5.A` 之后的本地 runtime，沿三条轴继续收紧：

1. 去掉 validator / checkpoint surface 与新 landed 的 revision / final / export surface 之间的 repo-tracked truth drift；
2. 把 `README` / `docs` / command matrix / operator 理解，对齐到真实已 landed 的本地 runtime ladder；
3. 让当前本地 runtime 真正维持为一个诚实的本地 `CLI-first + host-agent` 产品 baseline，而不是把它提前吹成 submission-grade autopilot 或 actual hosted runtime。

## In Scope

### 1. revised workspace validator truth tightening

当前第一优先级 follow-up 是已知的 post-`R3.A` 漂移：

- `validate-workspace` 与相关 checkpoint / route surfaces 仍带着早于 landed revision / final / export path 的旧假设。

因此这条线可以做：

- 收紧 `execute-revision-pass` 输出之后 revised workspace 的 validator 语义；
- 让 `stage-route-report`、`verification_checkpoint`、`checkpoint_status` 与 landed local-runtime outputs 对齐；
- 补或收紧回归测试，使 revised / final / export outputs 都落在同一 durable truth 下被验证。

### 2. 本地 operator / public-surface 对齐

这条线也可以做：

- 更新 `README*`、`docs/README*` 与紧邻的内部文档，不再把当前项目写成还停留在 `R1.B`；
- 把已 landed 命令面整理成更清楚的本地 operator path；
- 保持对外措辞诚实地区分“已经 landed 的本地能力”和“仍属 future scope 的部分”。

### 3. canonical end-to-end local walkthrough

如果有需要，这条线还可以补或收紧一条 canonical 本地 walkthrough，覆盖：

- workspace validation / summaries
- local runtime entry and resume
- artifact bundle production
- revision execution
- final package production
- hosted-contract bundle export

目的不是新增产品模式。
目的只是让已经 landed 的本地产品 runtime 更容易被验证与诚实操作。

## Hard Boundaries

这条线不得越过：

- actual hosted runtime
- remote execution
- Web UI
- multi-tenant platform
- credits / billing
- `P5.A / Second Grant Family Onboarding`
- `P5.B / Federation Contract Freeze`
- same-repo `Human-in-the-loop`
- `MCP / controller` public formal entry

## Required Truth Sources

执行前，旧 `OMX` handoff 快照当时要求读取：

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/history/specs/2026-04-08-runtime-first-productization-program.md`
- `docs/history/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`
- `docs/history/specs/README.md` 中的 runtime-first R1-R5 compression record；原 R1-R5 boundary / activation package 长正文已删除，精确正文只从 git history 读取
- 本文 `docs/history/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`
- `.runtime-program/context/CURRENT_PROGRAM.md`
- `.runtime-program/reports/med-autogrant-mainline/LATEST_STATUS.md`
- `.runtime-program/reports/med-autogrant-mainline/OPEN_ISSUES.md`
- `.runtime-program/reports/med-autogrant-mainline/ITERATION_LOG.md`

## Required Verification

每轮有意义 closeout 至少重跑：

- `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
- `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
- `python3 -m unittest discover -s tests -p 'test_artifact_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_revision_executor.py'`
- `python3 -m unittest discover -s tests -p 'test_final_package.py'`
- `python3 -m unittest discover -s tests -p 'test_hosted_contract_bundle.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- 当前 canonical CLI examples
- `git diff --check`

## Honest Stop Conditions

满足任一情况就应停车：

1. post-`R5.A` 已没有新的 concrete 本地 runtime delta 可继续收紧；
2. 下一步已经需要 actual hosted runtime 语义，而不只是 hostedization prep；
3. 下一步已经需要 `P5.A / P5.B`、same-repo HITL 或新的 formal entry；
4. 继续推进只能靠启发式补丁或 story-first 漂移。

## 推荐停车结论

这条线的理想停车结论是：

- `POST_R5A_LOCAL_RUNTIME_HARDENING_CLOSED_AND_ABSORBED`
  或
- `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
