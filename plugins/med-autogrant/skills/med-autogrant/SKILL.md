---
name: mag
description: Use when Codex should operate Med Auto Grant through its grant-authoring domain entry, authority targets, and schema-backed contracts instead of ad-hoc repo scripting.
---

# Med Auto Grant App Skill

机器名与 canonical skill id 使用 `mag`；`med-autogrant` 只作为 repo/source path alias 保留，不作为 Codex-visible app skill id。

当 Codex 需要把 `Med Auto Grant` 作为正式 domain app 来操作，而不是把仓库当成临时脚本集合时，使用这个 app skill。对外第一入口是这个单一 app skill；repo-local `CLI` / `MedAutoGrantDomainEntry` 只保留 grant-native handler 与 authority target，status、user-loop、direct-entry、domain_handler、workbench 等通用 shell 由 OPL/App generated surface 承担。

## 这个 app skill 是什么

- `Med Auto Grant` 面向 Codex 的单一 domain app skill
- 建立在现有 CLI、domain entry、authority target 与 authoring loop 合同之上
- 不替代 `medautogrant` CLI、schema-backed contract，也不替代 repo 内其他自动化入口；这些入口只能作为 MAG authoring runtime 的受控 surface，不能成为绕开 runtime 的替代执行路径

## 核心入口

自动调用 repo-local handler 时使用 clean runner：`<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli ...`。不要用 shell PATH lookup、用户 PATH 上的裸 `medautogrant`，或直接 `uv run --directory` 判断当前模块可用性。

- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli workspace route-report --input <input_path> --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli workspace quality-scorecard --input <input_path> --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli pass revision --input <input_path> --output <output_path> --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli package submission-ready --input <input_path> --output-dir <output_dir> --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli authority memory-proposal --input <input_path> --stage-id <stage_id> --source-ref <source_ref> --lesson-summary "<summary>" --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli authority memory-decision --proposal <proposal_path> --decision accepted|rejected --decision-reason "<reason>" --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli authority source-purity --format json`

OPL generated surface 负责 product manifest、status、user-loop、direct-entry、domain_handler 与 workbench shell。MAG repo-local code 只提供 grant truth、quality/export/package authority、memory accept/reject、owner receipt、grant-native helpers 和 strict source-purity guard readback。当前 MCP projection 是 descriptor-only：`descriptor_only=true`、`public_runtime=false`，不能写成 public MCP runtime 已落地。

默认先由 OPL/App generated status 或 manifest 读取当前 funding call、task intent 和 draft 状态，再回到上述 MAG grant-native handler / authority target。

## OPL Foundry Agent series CLI grammar

MAG 的 repo-local CLI 第一层公共语法使用 OPL Foundry Agent series spine：

- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry status --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry inspect --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry interfaces --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry validate --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry doctor --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry peers --format json`
- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli status --format json`

`grant` 是 `workspace` 的公共 alias，`work` 是 `pass` 的公共 alias；它们只映射到现有 MAG grant-native handler，不新增 runtime owner 或 product shell。

## Domain runtime 护栏

- 用户点名 `MAG` / `Med Auto Grant`，或任务属于基金方向、申请书、立项依据、研究内容、技术路线、修改包、submission-ready package 等 MAG 覆盖范围时，必须通过 OPL/App generated shell 回到 MAG schema-backed authoring contract、domain entry 或 authority target 推进。
- 不得用通用 `documents` / Office skill、直接编辑 `.docx`、ad-hoc 脚本、手写导出包或 prompt-only 文档路径来替代 MAG 的 grant-authoring runtime。
- 任何 grant artifact 写入前，必须先读取 OPL/App generated status 或 MAG workspace route/quality surface，确认 funding call、draft 状态、quality gate、task intent 与 continuation surface。
- 如果某个所需 authoring/export 能力在 MAG surface 中缺失，应回到 repo 层补最小 grant-native handler 或 authority target 并验证，而不是在单个 grant workspace 旁路实现。
- 只有用户明确要求“探索 MAG 之外的替代技术路线”或“只做离线草稿、不进入 MAG runtime”时，才可以使用通用文档工具；回复中必须标明该路线不更新 MAG truth surface。

## 操作约束

- 任何写操作前，先读取当前 workspace、route report 与 quality/package gate
- 把 `domain_entry_contract`、`stage_route_report`、`grant_quality_*`、`owner_receipt` 与 `memory_accept_reject` 当作 MAG repo-local contract surface
- 保持同一指定 funding call 下的 authoring continuity，不写成 opportunistic funder switching
- 不绕开 schema-backed contract 直接手改 runtime state
- 不绕开 MAG authoring runtime 用通用 Office/document 工具、ad-hoc 脚本或 prompt-only 路径完成申请书、修改包、导出包或 submission-ready gate
- 不把 status、user-loop、direct-entry、domain_handler、workbench 等 generated shell 写回 MAG repo-local public/default CLI

## 首先应读的文件

- `README.md`
- `docs/project.md`
- `docs/status.md`

## 典型任务

- 读取当前 grant workspace 的 route report、quality gate 与 package gate
- 通过 OPL/App generated shell 回到 MAG grant-native handler
- 在同一 funding call 下继续 authoring pass 或 authority receipt/memory flow
- 通过结构化命令驱动 critique、revision、submission-ready package 等后续动作
