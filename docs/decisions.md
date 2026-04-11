# 决策记录

## 2026-04-11：统一文档骨架

- 采用核心五件套：`project/architecture/invariants/decisions/status`。
- `docs/README*` 以核心骨架为首读入口，其次是 `specs/`、`plans/`、`history/`。

## 2026-04-11：AGENTS 仅保留工作方式

- `AGENTS.md` 不再承载项目事实与阶段判断，统一回收至核心骨架与 specs。

## 2026-04-11：OMX 仅保留历史入口

- OMX 相关内容只作为历史入口保留在 `docs/history/omx/**`，不再作为活跃执行入口。

## 2026-04-11：移除 OMX-era 外部验证入口

- `omx-project-installer` 相关的外部 verifier 不再出现在 repo-tracked current truth 的验证表述中。
- 如需追溯历史来源，仅在历史说明或本文件记录，不再作为当前验证或 hard gate 入口。

## 2026-04-11：统一最小验证入口

- `scripts/verify.sh` 作为默认最小验证入口，保持分层 lane 与 `Makefile` 一致。
