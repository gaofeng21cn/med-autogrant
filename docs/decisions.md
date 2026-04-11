# 决策记录

## 2026-04-11：统一文档骨架

- 建立核心五件套：`project/architecture/invariants/decisions/status`。
- `docs/README*` 以核心骨架为首读入口，其次是 `specs/`、`plans/`、`history/`。

## 2026-04-11：移除 OMX-era 外部验证入口

- `omx-project-installer` 相关的外部 verifier 不再出现在 repo-tracked current truth 的验证表述中。
- 如需追溯历史来源，仅在历史说明或本文件记录，不再作为当前验证或 hard gate 入口。
