# Med Auto Grant 关键决策

## 2026-04-11

### 决策：采用核心五件套文档骨架

- `docs/project.md`
- `docs/architecture.md`
- `docs/invariants.md`
- `docs/decisions.md`
- `docs/status.md`

原因：让 AI 和维护者能快速建立项目上下文，不再在 README、specs 与历史计划之间来回跳转。

### 决策：`AGENTS.md` 只保留工作方式

原因：项目事实会变化，工作方式应更稳定；两者混写会形成重复真相源。

### 决策：OMX 只保留历史入口

原因：OMX 已退场。与 OMX 相关的当前验证和运行描述应从 active docs 中移除，只保留历史背景。

### 决策：统一最小验证入口

原因：新增 `scripts/verify.sh`，让 AI、维护者和自动化都有固定的最小验证调用面。
