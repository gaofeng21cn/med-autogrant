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
- Current owner line：`post-R5A local runtime closeout / honest stop`
- Current truthful closeout：`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
- repo-tracked current truth 入口：
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
  - `docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`

## 当前优先事项

1. 保持当前 repo-verified local runtime baseline、artifact/export surface 与 canonical CLI examples 持续全绿。
2. 任何 further productization 先冻结新 tranche truth，不把未冻结 reality 写成当前已存在主线。
3. 保持 `.runtime-program/**` 只是本地 control-plane，而不是 repo-tracked 产品主线。

## 默认验证

- 默认最小验证：`scripts/verify.sh`（`make test-fast`）。
- meta 验证：`scripts/verify.sh meta`。
- CLI smoke：`scripts/verify.sh cli-smoke`。
- full 验证：`scripts/verify.sh full`。
