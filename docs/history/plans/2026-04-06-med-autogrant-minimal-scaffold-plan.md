# Med Auto Grant 最小 Scaffold 实施计划

Owner: `Med Auto Grant`
Purpose: `historical_minimal_scaffold_plan_provenance`
State: `history`
Machine boundary: 本文是人读历史计划，保留 2026-04-06 最小 scaffold 搭建过程。当前仓库入口、docs taxonomy、runtime owner、标准 OPL Agent 目标态与机器行为以核心五件套、active gap plan、docs portfolio、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准；本文不作为当前 scaffold backlog、controller/runtime plan 或兼容承诺。

> 当前文档面向内部执行，只保留中文版本。
> Historical / completed scaffold plan：该计划对应的仓库搭建阶段已完成，当前仅保留为历史 provenance，不代表当前主线目标。

Date: `2026-04-06`

## 目标

先把 `med-autogrant` 独立仓库开起来，以文档先行方式冻结命名、边界、公开定位和第一阶段 MVP 范围，为后续 schema 与 runtime 开发留出清晰入口。

## 本轮任务

- [x] 创建独立仓库目录并初始化 git
- [x] 建立基础目录：`docs/`、`src/`、`tests/`、`examples/`、`schemas/`
- [x] 建立 repo 级 `AGENTS.md`
- [x] 建立顶层双语 `README`
- [x] 建立最小双语公开文档：
  - [x] `docs/domain-positioning.*`
  - [x] `docs/mvp-scope.*`
- [x] 建立中文内部设计文档
- [x] 建立中文内部计划文档
- [x] 增加基础 `.gitignore`

## 本轮不做

- [x] 不引入运行时依赖
- [x] 不实现 agent controller
- [x] 不实现 schema
- [x] 不实现测试框架
- [x] 不实现 CLI 或 web app

## 验证

本轮验证以结构和文档存在性为主：

- 仓库目录已初始化
- 公开双语文档已成对出现
- 内部文档已按中文单语落地
- 基础目录可被 git 跟踪

## 下一步

- 冻结 MVP 对象模型 schema
- 冻结第一条 `NSFC` 申请主流程
- 设计第一版 critique / revision loop
- 决定首个 runtime 与 controller 组织方式

以上“下一步”已经属于历史阶段后续动作，现已被 repo-tracked current-truth 文档吸收，不再代表当前 active mainline 的最近目标。
