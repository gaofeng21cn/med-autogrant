# 当前状态

Date: `2026-04-11`

## 当前角色

- 仓库角色：医学 `Grant Ops` 的 author-side / proposal-facing `Domain Harness OS` 方向。
- 当前执行口径：`CLI-first + host-agent runtime`。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。

## 主线与阶段

- Current phase：`Runtime Productization Program`
- Active tranche：`R5 / Hostedization Prep`
- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Current owner line：`post-R5A local runtime hardening`
- repo-tracked current truth 入口：
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`

## 当前优先事项

1. 收紧 local runtime 与 artifact/export surface 的 fail-closed 语义。
2. 继续把 current truth、activation package 与 README/docs 入口对齐。
3. 保持 `.runtime-program/**` 只是本地 control-plane，而不是 repo-tracked 产品主线。

## 默认验证

- 默认最小验证：`scripts/verify.sh`（`make test-fast`）。
- meta 验证：`scripts/verify.sh meta`。
- CLI smoke：`scripts/verify.sh cli-smoke`。
- full 验证：`scripts/verify.sh full`。
