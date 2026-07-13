---
name: med-autogrant
description: Use when Codex should operate Med Auto Grant through its grant-authoring domain entry, authority targets, and schema-backed contracts instead of ad-hoc repo scripting.
---

# Med Auto Grant App Skill

OPL canonical agent id 与 OPL Agent Package id 都固定为 `mag`，唯一 OCI Package repository 是 `ghcr.io/gaofeng21cn/one-person-lab-packages/mag`。`med-autogrant` 是仓库、Python distribution、plugin slug 与安装后 skill locator，不是与 `mag` 并存的 package identity、OCI package coordinate 或兼容 alias。

Implementation profile 见 `contracts/pack_compiler_input.json#/implementation_profile`：声明 pack 只使用 Markdown/JSON，Python 只作为声明 source root 下的 domain helper；grant authority 由 pack authority contracts 独立声明。它不拥有 generic runtime、CLI、MCP、product-entry、status 或 workbench。

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

MAG 只有一个语义控制面：Codex CLI。任何可读 grant 草稿、fundability
判断、review finding、阴性结果、部分 package 或 diagnostic 都是 progress，
可直接作为下一 declared stage 的输入。retry、review、repair 次数只代表质量
预算；预算用尽时保留最佳 artifact 并以 `completed_with_quality_debt` 推进。
Codex 可以前进、重复当前 stage，或回到 call intake、fundability strategy、
specific aims、proposal authoring、review/package 等任一 declared stage；静态
transition table、schema、normalizer、validator 或 receipt 缺口无权否决该路由。
质量债只关闭 fundable、grant-ready、submission-ready、export-ready、accepted
与 production-ready 声明。只有零可消费 artifact、损坏不可读、权限/安全、
identity/currentness、不可逆 portal/write 操作或明确 owner/human authority 才能硬停。

- OPL/Temporal 持有任务运行驻留、stage attempt lifecycle、queue/wakeup、retry/resume、attempt ledger、generated caller 与 App/workbench shell。
- MAG 持有 grant truth、fundability/quality/export verdict、package authority、memory accept/reject、owner receipt、typed blocker 与 grant-native helper；Codex CLI 独占语义 route 选择。
- OPL generated surface、provider completion、schema completeness或测试通过都不能声明 grant-ready、submission-ready 或 production-ready。
- 当前 MCP 仍满足 `descriptor_only=true`、`public_runtime=false`；不能写成 public MCP runtime 已落地。

结构 currentness 必须由 OPL canonical scanner 读取，而不是由 MAG 私有 source-purity wrapper 推断：

`<one-person-lab-repo>/bin/opl agents conformance --agent mag=<med-autogrant-repo> --json`

Scanner 通过只证明 standard-agent 结构与 source-behavior gate 对齐，不替代真实 workspace artifact、owner receipt、human gate、quality/export verdict 或 production evidence。

## OPL 公开检查面

Foundry membership、status、interfaces、validation、diagnostics 与 peers 由 OPL generated surface 统一投影。使用 `opl foundry agents inspect mag --json`，不要在 MAG repo-local CLI 重建同类 payload 或 alias。

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
