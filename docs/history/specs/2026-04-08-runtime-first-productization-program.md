# Runtime-First Productization Program

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_runtime_first_productization_program_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-08 runtime-first productization program 与 R1-R5 execution priority 的形成过程。当前 runtime owner 是 OPL/Temporal，MAG 保留 grant domain authority surfaces；local runtime、journal、attempt ledger、host-agent、Gateway 与 hostedization wording 均按 provenance 阅读。当前执行顺序、runtime owner、product-entry、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

Date: `2026-04-08`

## Purpose

这份文档冻结 `Med Auto Grant` 当前的执行优先级：

- 先把 `CLI-first + host-agent` 的本地产品 runtime 做成熟
- 再把最终交付面做成 submission-facing 的本地导出面
- 最后才做 hostedization prep

它不是在改写项目的长期 north star，也不是在替代 `P1 -> P5` 的 domain maturity order。

更准确地说：

- `P1 -> P5` 仍然回答“Grant Ops domain 本身成熟到哪里”
- `R1 -> R5` 回答“当前执行优先级应该先把哪条产品 runtime 主线做出来”

## Why This Program Exists

当前仓内已经有：

- `NSFC` 通用 authoring loop 的对象与 route 边界
- critique / revision / re-review / rollback 的 machine-readable contract
- verification / checkpoint 的 CLI baseline 与 durable report surface

但这些能力还没有被收束成一个真正连续运行的本地产品 runtime。

因此，当前最优先的不是继续做第二 family、federation、或托管平台外壳，而是先把下面这条产品主线真正跑起来：

`输入接入 -> 方向收敛 -> 科学问题提纯 -> 论证链 -> 适配度 -> 提纲 -> 草稿 -> 批注 -> 修订 -> 冻结 -> 导出`

## Relationship To Existing P1-P5 Order

`P1 -> P5` 仍保持原有语义：

1. `P1 / Reality Convergence And NSFC Baseline Freeze`
2. `P2 / NSFC Authoring Mainline Freeze`
3. `P3 / Mentor Critique And Revision Loop Hardening`
4. `P4 / Verification Surface And HITL Layering Preparation`
5. `P5 / Grant Ops Gateway Expansion And Federation`

当前 `runtime-first productization` 不替换这条顺序，只改变执行优先级：

- 先消化 `P1 -> P4` 已冻结能力，把它们收束成成熟本地 runtime
- `P5.A / P5.B` 当前转为 deferred future expansion
- hostedization prep 只有在本地 runtime 已经像一个真正产品那样工作时才允许进入

## Pre-Frozen Boundary Map

当前 `R1 -> R5` 的 future activation boundary 已一次性冻结在：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`

这份边界图当前承认：

- `R1.B / Stage Action Executor Envelope` 与 `R2.A / Artifact Bundle Production Surface` 已从 pre-frozen package 进入 absorbed current truth
- `R3.A / R4.A / R5.A` 已在 frozen object boundary 内完成实现并一起 absorbed 到 `main`
- latest absorbed runtime slice 已是 `R5.A / Hosted-Friendly Session Boundary`
- `R3.A` 的 machine-applicable implementation contract 已冻结并成为 absorbed runtime truth 的一部分：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`
- 已 absorbed 的 post-`R5.A` local runtime hardening 继续锁定：
  1. revised workspace validator / checkpoint regression
  2. runtime-first truth / operator walkthrough 与 landed 本地 runtime ladder 的一致性
  3. final-package / hosted-contract fail-closed closeout
- 当前 truthful continuation 已收口为 `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`：
  1. 当前 repo 内已没有新的 concrete、本地、可 repo-track 的 runtime delta 可以默认继续
  2. 若要继续推进，必须先冻结新的 tranche truth
  3. 不得把 closeout后的本地 runtime 误写成 actual hosted runtime、`P5` expansion 或 submission-grade autopilot reality
- 当前 owner line 已切换为 `post-R5A local runtime closeout / honest stop`

当前 realized activation packages：

- `R3.A`：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-r3a-critique-revision-executor-surface-activation-package.md`
- `R4.A`：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`
- `R5.A`：
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md`

也就是说，边界图仍然是 runtime boundary contract，但它现在记录的是“已 absorbed through `R5.A` 的对象边界 + absorbed post-`R5.A` closeout + freeze-before-continue rule”，而不是 `R3.A / R4.A / R5.A` 的待实现队列。

## Program Ladder

### R1 / Autonomous Main Loop

目标：

- 把现有 `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report` 五个 CLI surfaces 收束成一个连续的本地主循环
- 让系统能围绕同一 `grant_run_id`、同一 workspace、同一 draft lineage 持续推进，而不是靠人工逐条调用命令拼出来
- 让停机、回退、冻结、恢复都变成 runtime 行为，而不是只存在于控制面叙述里

当前推荐冻结的 runtime entry：

- `CLI-first`
- 新的本地主循环 entry 可以由 `runtime-run` 类命令承载，但必须保持旧五个 CLI surfaces 继续作为 verifier / audit surfaces

验收重点：

- 至少一个本地主循环入口能够从 workspace 输入连续跑到真实 stop reason
- stop reason 必须 machine-readable
- recovery 必须不依赖旧 pane / 聊天上下文

### R2 / Artifact Production Surface

目标：

- 把“方向、问题、论证链、适配度、提纲、草稿”从逻辑状态变成稳定 artifact bundle
- 让本地 runtime 不只是会判断下一步，还会稳定产出用户真正会用的申请材料包
- 当前 absorbed surface 已包括：`build-artifact-bundle`

验收重点：

- 产物必须有 manifest / lineage / version
- artifact bundle 必须与当前 frozen question、argument chain、fit mapping、draft lineage 一致
- 不允许在写作阶段偷偷换题

### R3 / Critique Revision Autoloop

目标：

- 把“导师批注 -> 修订计划 -> 执行修订 -> 复审 -> 必要时回退”变成真正连续的 autoloop
- 让系统不仅能给批注，还能围绕批注持续修改，直到进入下一真实 stop condition

验收重点：

- critique、revision、re-review 之间必须保持 evidence trace
- forced rollback 必须是 runtime 真行为
- 局部润色与结构性返工必须可区分

### R4 / Finalization And Export Surface

目标：

- 把最终冻结版本、导出包、checkpoint summary 与 submission-facing 本地交付面做出来
- 让系统从“能出草稿”提升到“能形成可审阅的完整申请包”

验收重点：

- final package 必须有冻结版本身份
- 章节完整性、证据挂接、lineage 与 final checkpoint 必须一致
- export surface 必须是结构化 package，不是自由文本说明

### R5 / Hostedization Prep

目标：

- 在本地 runtime 成熟后，再拆 host/runtime boundary，为后续托管化准备
- 只做 contract、state、session、artifact、audit surface 的 hosted-friendly 抽象

验收重点：

- 不改写 domain contract
- 不提前伪装成已完成 hosted runtime
- hostedization prep 只在 `R1 -> R4` 成熟后打开

## Deferred Scope

在当前 program 内，以下内容全部后置：

- `P5.A / Second Grant Family Onboarding`
- `P5.B / Federation Contract Freeze`
- second-family source packet 扩张
- `Grant Foundry` admission / federation package
- same-repo `Human-in-the-loop`
- `MCP / controller` public formal entry
- web runtime / hosted runtime 正式落地

## Promotion Invariants

- formal entry 继续固定为 `CLI-first`
- `grant_run_id / workspace_id / draft_id / program_id` 边界不变
- 旧五个 CLI surfaces 继续作为 verifier / audit surfaces
- critique / revision / rollback / checkpoint 的 absorbed contracts 不得回退
- 本地 runtime 成熟化优先于 second-family / federation 扩张
- hostedization 只能发生在本地 runtime 成熟之后

## OMX Autonomy Rules For This Program

> 历史说明：本节保留 OMX 时代的连续执行约束，作为审计与迁移背景；当前活跃入口已迁回根 `AGENTS.md`、`docs/README*` 与 `docs/history/omx/README*`。

在这条 program 里，`OMX` 不是被允许“想到什么就做什么”，而是被允许：

1. 先在 `R1 -> R5` 中定位当前 stage
2. 如果发现新的、具体的、可测试的 runtime 缺口：
   - 先把缺口冻结进 active `PRD / test-spec / implementation`
   - 必要时新增 repo-tracked 内部 spec
   - 再实现、验证、closeout、absorb
3. 在同一 stage 内连续拆分多个 bounded sub-slices，只要每个 sub-slice 都先 freeze 再 implement

补充规则：

- 如果下一 honest delta 实际属于更后面的 stage，`OMX` 可以直接重分类到对应的 pre-frozen package，而不是强行编造当前 stage 的中间 tranche
- 在 `R1.A` 之后，如果下一能力已经属于 artifact / revision / export / hosted-friendly boundary，就应分别进入 `R2.A / R3.A / R4.A / R5.A`

禁止：

- 直接跳到 hostedization
- 越过 `R1 -> R4` 去做 second-family / federation
- 在没有 frozen slice contract 的情况下硬写 runtime 行为

## Honest Stop Conditions

以下情况必须诚实停车，而不是硬跑：

- 当前 stage 没有新的 concrete runtime delta
- 下一步需要新的 formal entry、平台 runtime、外部凭据、或仓外 readiness
- 当前想做的动作其实属于 `P5` expansion，而不是 runtime-first productization
- 无法把新增能力写成可验证 slice
