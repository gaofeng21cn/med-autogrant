---
name: mag
description: Use when Codex should operate Med Auto Grant through its grant-authoring product entry, user-loop, and schema-backed contracts instead of ad-hoc repo scripting.
---

# MAG App Skill

当 Codex 需要把 `Med Auto Grant` 作为正式 domain app 来操作，而不是把仓库当成临时脚本集合时，使用这个 app skill。对外第一入口是这个单一 app skill；`CLI` / `MedAutoGrantDomainEntry`、`status`、`user-loop`、`direct-entry` 等都属于它下面的内部 command contract。

## 这个 app skill 是什么

- `Med Auto Grant` 面向 Codex 的单一 domain app skill
- 建立在现有 CLI、domain entry、product entry 与 authoring loop 合同之上
- 不替代 `medautogrant` CLI、schema-backed contract，也不替代 repo 内其他自动化入口；这些入口只能作为 MAG authoring runtime 的受控 surface，不能成为绕开 runtime 的替代执行路径

## 核心入口

自动调用时使用 repo-local launcher：`uv run --directory <med-autogrant-repo> medautogrant ...`。不要用 shell PATH lookup 或用户 PATH 上的裸 `medautogrant` 判断当前模块可用性。

- `uv run --directory <med-autogrant-repo> medautogrant product skill-catalog --input <input_path> --format json`
- `uv run --directory <med-autogrant-repo> medautogrant product status --input <input_path>`
- `uv run --directory <med-autogrant-repo> medautogrant product user-loop --input <input_path> --task-intent "<task_intent>"`
- `uv run --directory <med-autogrant-repo> medautogrant product direct-entry --input <input_path> --task-intent "<task_intent>"`

`product manifest` 暴露 MAG-owned `family_action_catalog`；CLI、product-entry、skill metadata 与 MCP-compatible descriptor 从同一份 action definition 派生。当前 MCP projection 是 descriptor-only：`descriptor_only=true`、`public_runtime=false`，不能写成 public MCP runtime 已落地。

默认先读取 skill catalog 或打开 status，再根据当前 funding call、task intent 和 draft 状态进入 user loop 或 direct entry。

## Domain runtime 护栏

- 用户点名 `MAG` / `Med Auto Grant`，或任务属于基金方向、申请书、立项依据、研究内容、技术路线、修改包、submission-ready package 等 MAG 覆盖范围时，必须通过 MAG product-entry、user-loop、direct-entry 或 schema-backed authoring contract 推进。
- 不得用通用 `documents` / Office skill、直接编辑 `.docx`、ad-hoc 脚本、手写导出包或 prompt-only 文档路径来替代 MAG 的 grant-authoring runtime。
- 任何 grant artifact 写入前，必须先读取 skill catalog / status / product-entry manifest，确认 funding call、draft 状态、quality gate、task intent 与 continuation surface。
- 如果某个所需 authoring/export 能力在 MAG surface 中缺失，应回到 repo 层补最小 callable/product-entry surface 并验证，而不是在单个 grant workspace 旁路实现。
- 只有用户明确要求“探索 MAG 之外的替代技术路线”或“只做离线草稿、不进入 MAG runtime”时，才可以使用通用文档工具；回复中必须标明该路线不更新 MAG truth surface。

## 操作约束

- 任何写操作前，先读取当前 workspace 与 product-entry manifest
- 把 `skill_catalog`、`product_entry_manifest`、`domain_entry_contract`、`task_lifecycle` 当作正式 contract surface
- 保持同一指定 funding call 下的 authoring continuity，不写成 opportunistic funder switching
- 不绕开 schema-backed contract 直接手改 runtime state
- 不绕开 MAG authoring runtime 用通用 Office/document 工具、ad-hoc 脚本或 prompt-only 路径完成申请书、修改包、导出包或 submission-ready gate
- 不把内部 shell 命令写成多个独立用户 skill；它们继续是这个 app skill 的内部 command contract 和 direct-product projection

## 首先应读的文件

- `README.md`
- `docs/project.md`
- `docs/status.md`

## 典型任务

- 读取当前 grant workspace 的 machine-readable skill catalog
- 打开 status 检查当前 authoring loop、quality gate 与推荐启动路径
- 在同一 funding call 下继续 user loop 或 direct-entry authoring
- 通过结构化命令驱动 critique、revision、submission-ready package 等后续动作
