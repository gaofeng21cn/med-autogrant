---
name: med-autogrant
description: Use when Codex should operate Med Auto Grant through its grant-authoring product entry, user-loop, and schema-backed contracts instead of ad-hoc repo scripting.
---

# Med Auto Grant App Skill

当 Codex 需要把 `Med Auto Grant` 作为正式 domain app 来操作，而不是把仓库当成临时脚本集合时，使用这个 app skill。

## 这个 app skill 是什么

- `Med Auto Grant` 面向 Codex 的单一 domain app skill
- 建立在现有 CLI、domain entry、product entry 与 authoring loop 合同之上
- 不替代 `medautogrant` CLI、schema-backed contract，也不替代 repo 内其他自动化入口

## 核心入口

- `medautogrant product skill-catalog --input <input_path> --format json`
- `medautogrant product frontdesk --input <input_path>`
- `medautogrant product user-loop --input <input_path> --task-intent "<task_intent>"`
- `medautogrant product direct-entry --input <input_path> --task-intent "<task_intent>"`

默认先读取 skill catalog 或打开 frontdesk，再根据当前 funding call、task intent 和 draft 状态进入 user loop 或 direct entry。

## 操作约束

- 任何写操作前，先读取当前 workspace 与 product-entry manifest
- 把 `skill_catalog`、`product_entry_manifest`、`domain_entry_contract`、`task_lifecycle` 当作正式 contract surface
- 保持同一指定 funding call 下的 authoring continuity，不写成 opportunistic funder switching
- 不绕开 schema-backed contract 直接手改 runtime state
- 不把内部 shell 命令写成多个独立用户 skill；它们继续是这个 app skill 的内部 command contract

## 首先应读的文件

- `README.md`
- `docs/project.md`
- `docs/status.md`

## 典型任务

- 读取当前 grant workspace 的 machine-readable skill catalog
- 打开 frontdesk 检查当前 authoring loop、quality gate 与推荐启动路径
- 在同一 funding call 下继续 user loop 或 direct-entry authoring
- 通过结构化命令驱动 critique、revision、submission-ready package 等后续动作
