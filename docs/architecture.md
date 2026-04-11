# Med Auto Grant 架构

## 主链路

当前主链路是本地 `CLI-first + host-agent` runtime：

`operator / agent -> CLI -> workspace validation and routing -> critique / export / stage surfaces -> durable artifacts`

## 结构角色

### 1. Public surface

- `README*`
- `docs/README*`
- `docs/domain-positioning*`
- `docs/mvp-scope*`

这层负责对外说明项目定位、范围和当前成熟度。

### 2. Core maintainer docs

- `docs/project.md`
- `docs/status.md`
- `docs/architecture.md`
- `docs/invariants.md`
- `docs/decisions.md`

这层负责 AI / 维护者快速建立上下文。

### 3. Current truth / specs

- `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `docs/specs/2026-04-07-durability-model-clarification.md`
- 各 activation package / current truth 文档

这层负责冻结当前 runtime 与 control-plane 语义，不承担公开首页叙事。

### 4. Local control-plane

- `.runtime-program/context/**`
- `.runtime-program/plans/**`
- `.runtime-program/reports/**`

这层只属于本地 operator control-plane，不是 repo-tracked 产品真相。

## 历史边界

- OMX 已退场。
- `docs/history/omx/` 只保留历史与迁移背景。
