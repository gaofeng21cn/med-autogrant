---
name: med-autogrant
description: Use when Codex should operate Med Auto Grant through its grant-authoring domain entry, authority targets, and schema-backed contracts instead of ad-hoc repo scripting.
---

# Med Auto Grant App Skill

OPL canonical agent id 固定为 `mag`。`med-autogrant` 是仓库、Python package、plugin slug 与安装后 skill locator，不是与 `mag` 并存的兼容 alias。

当 Codex 需要操作医学基金申请主线时，使用这个 app skill。OPL/App 负责 generated product/status/user-loop/workbench caller；MAG repo-local `CLI`、`MedAutoGrantDomainEntry` 与 domain handler 只保留 grant-native action target、authority function 和 schema-backed contract。

## 核心入口

调用 repo-local handler 时使用 clean runner：`<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli ...`。不要用 shell PATH 上的裸命令或临时脚本旁路当前 checkout。

- `workspace route-report --input <input_path> --format json`
- `workspace quality-scorecard --input <input_path> --format json`
- `pass revision --input <input_path> --output <output_path> --format json`
- `package submission-ready --input <input_path> --output-dir <output_dir> --format json`
- `authority memory-proposal --input <input_path> --stage-id <stage_id> --source-ref <source_ref> --lesson-summary "<summary>" --format json`
- `authority memory-decision --proposal <proposal_path> --decision accepted|rejected --decision-reason "<reason>" --format json`
- `domain-handler export --input <input_path> --format json`
- `domain-handler dispatch --task <task_path> --format json`

Domain handler dispatch 只允许三项 MAG-owned action：

- `domain-memory/propose`
- `domain-memory/decide`
- `stage-attempt/closeout`

其 export 返回 body-free workspace identity/locator，并携带 action catalog、stage control plane、owner receipt contract、三项 allowed action、八项 minimal authority refs、generated-surface handoff ref，以及 caller/false-authority boundary；不包含 grant、memory、artifact 或 package body，也不是 scheduler、queue、session、status 或 workbench runtime。

## OPL 边界

- OPL/Temporal 持有任务运行驻留、stage attempt lifecycle、queue/wakeup、retry/resume、attempt ledger、generated caller 与 App/workbench shell。
- MAG 持有 grant truth、fundability/quality/export verdict、package authority、memory accept/reject、owner receipt、typed blocker、transition oracle 与 grant-native helper。
- OPL generated surface、provider completion、schema completeness或测试通过都不能声明 grant-ready、submission-ready 或 production-ready。
- 当前 MCP 仍满足 `descriptor_only=true`、`public_runtime=false`；不能写成 public MCP runtime 已落地。

结构 currentness 必须由 OPL canonical scanner 读取，而不是由 MAG 私有 source-purity wrapper 推断：

`<one-person-lab-repo>/bin/opl agents conformance --agent mag=<med-autogrant-repo> --json`

Scanner 通过只证明 standard-agent 结构与 source-behavior gate 对齐，不替代真实 workspace artifact、owner receipt、human gate、quality/export verdict 或 production evidence。

## OPL Foundry Agent CLI grammar

- `foundry status --format json`
- `foundry inspect --format json`
- `foundry interfaces --format json`
- `foundry validate --format json`
- `foundry doctor --format json`
- `foundry peers --format json`
- `status --format json`

`grant` 是 `workspace` 的公共 alias，`work` 是 `pass` 的公共 alias；它们只映射到现有 MAG grant-native handler，不新增 runtime owner 或 product shell。

## 操作约束

- 写 grant artifact 前先读取 workspace route、quality/package gate 与当前 funding call。
- 不用通用 Office/document skill、ad-hoc 脚本或 prompt-only 路径替代 MAG authoring contract。
- 不直接修改 runtime state；所有写入通过 schema-backed handler、authority target 或 package surface。
- 不把 generated status/user-loop/workbench shell重新实现到 MAG repo。
- 能力缺失时补最小 grant-native handler 或 authority target，不恢复旧 wrapper、facade、alias 或私有平台面。

## 首先应读

- `README.md`
- `docs/project.md`
- `docs/status.md`
- `contracts/runtime-program/current-program.json`

## 典型任务

- 读取 route report、quality gate、package gate 与当前 blocker。
- 在同一 funding call 下继续 authoring、critique、revision 或 package flow。
- 提交 memory proposal/decision 或 stage-attempt closeout，并读取 owner receipt / typed blocker refs。
- 通过 OPL generated caller 回到 MAG 的 grant-native handler，而不复制 product/runtime shell。
