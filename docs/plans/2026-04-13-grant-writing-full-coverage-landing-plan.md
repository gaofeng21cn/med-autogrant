# Grant Writing Full Coverage Landing Plan

> Historical completed plan. The full `direction_screening -> frozen` authoring route is already landed. Current truth now lives in `docs/decisions.md`, `docs/project.md`, and `contracts/runtime-program/current-program.json`.

## 历史目标

把当前只在合同层冻结的前半程 authoring 路线，补齐为可执行、可验证、可审计的 landed executor surface，使 `Med Auto Grant` 能从 `input_intake` 之后一路推进到 `frozen`，覆盖人工国自然写作流程中的主线收敛、问题提纯、立项依据、适配度、提纲、正文起草与送审前冻结。

## 历史范围

- landed 下列 authoring route：
  - `direction_screening`
  - `question_refinement`
  - `argument_building`
  - `fit_alignment`
  - `outline`
  - `drafting`
  - `frozen`
- 保持现有 landed route 继续可用：
  - `critique`
  - `revision`
  - `artifact_bundle`
  - `final_package`
  - `hosted_contract_bundle`
- 同步更新：
  - `executor_routing_contract`
  - `domain_entry_contract`
  - `grant-direct-entry`
  - `grant-user-loop`
  - 核心骨架与 current truth
  - 相关测试与验证入口

## 历史非目标

- 不把 `MCP` 写成已公开 formal entry。
- 不把当前仓库写成 mature Web UI 或 hosted runtime。
- 不引入新的 repo-local runtime owner 叙事。
- 不为了“全覆盖”引入不可验证的兜底或启发式后处理。

## 当时的设计原则

### 1. 继续沿现有 stage 梯子落地

不新增一条平行 authoring 流程，也不把人工流程拆成另一套 stage。
人工流程中的：

- 方向延续性与热点筛选
- 具体临床问题锚定
- 创新框架与立项依据收敛
- 申请人适配度论证
- 提纲、正文、进度与冻结

全部映射进现有：

- `direction_screening`
- `question_refinement`
- `argument_building`
- `fit_alignment`
- `outline`
- `drafting`
- `critique`
- `revision`
- `frozen`

### 2. controller-first / workspace-first

借鉴 `Med Auto Science` 的做法，先让 workspace 上的结构化对象与稳定 command surface 落地，再让 product projection / user loop 去消费这些真相；不反过来先堆 UI。

### 3. honest route catalog

一旦 route 已 landed，就必须：

- 出现在 `author_side_route_catalog`
- 带明确 `execution_surface.command`
- 能被 `MedAutoGrantDomainEntry`
- CLI
- `grant-user-loop`
- hosted contract bundle

同时看见。

### 4. 明确下游失效与重建边界

前半程 route 一旦改写上游对象，必须清空不再可信的下游对象，避免伪稳定：

- 方向重筛后清空问题/论证/适配/草稿/批注/修订
- 问题重塑后清空论证/适配/草稿/批注/修订
- 立项依据重建后清空适配/草稿/批注/修订
- 适配度重建后清空草稿/批注/修订
- drafting 重跑后清空批注/修订

## 当时的实施分块

### A. 文档与 current truth

- 新增一份 full-coverage current truth，明确全量 authoring route 已 landed。
- 更新 `README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`。
- 更新 `contracts/runtime-program/current-program.json` 的 active tranche 与 truth surface。

### B. executor landing

- 新增前半程 executor 实现：
  - `execute-direction-screening-pass`
  - `execute-question-refinement-pass`
  - `execute-argument-building-pass`
  - `execute-fit-alignment-pass`
  - `execute-outline-pass`
  - `execute-drafting-pass`
  - `execute-freeze-pass`
- 保持现有 `execute-critique-pass`、`execute-revision-pass` 不漂移。

### C. route contract / product surface 同步

- 更新 `hermes_runtime.py` 内：
  - `SUPPORTED_DOMAIN_ENTRY_COMMANDS`
  - `DOMAIN_ENTRY_COMMAND_CONTRACTS`
  - `AUTHOR_SIDE_ROUTE_IDS`
  - `_build_author_side_route_contract`
  - `_build_executor_routing_contract`
- 更新 `product_entry.py` 内：
  - `grant_direct_entry`
  - `grant_user_loop`
  - landed route 命令串生成

### D. 测试与验证

- 更新 `tests/test_domain_entry.py`
- 更新 `tests/test_product_entry.py`
- 更新 `tests/test_hermes_runtime.py`
- 更新 `tests/test_hermes_runtime_truth.py`
- 更新 `tests/test_stage_router.py`
- 必要时补充 executor 级测试

## 当时的验证策略

- 最小验证：`scripts/verify.sh`
- 重点回归：
  - 前半程 landed route command 可调用
  - `grant-user-loop.next_action` 对前半程返回 landed command
  - hosted contract bundle 导出新的 command catalog
  - current truth / status / README 与测试一致

## 当时的吸收策略

在独立 worktree 完成实现与验证后：

1. 切回主 checkout
2. 吸收分支到 `main`
3. 清理 worktree 与临时分支

避免长时间留下并行 lane，降低和其他对话冲突的概率。
