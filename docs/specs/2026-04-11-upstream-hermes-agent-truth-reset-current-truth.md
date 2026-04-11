# Upstream Hermes-Agent Truth Reset Current Truth

## 目的

这份文档用于把 `Med Auto Grant` 当前 runtime 叙事从“仓内已切到 Hermes-backed runtime”纠正回真实状态。

## 当前真实状态

- 当前仓库已经有可运行的本地 `CLI` grant runtime 基线。
- `run-local`、`resume-local`、`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle` 都是 repo-local runtime / export surface。
- `src/med_autogrant/hermes_runtime.py` 当前仍是仓内自写的 local runtime helper / migration scaffold，不等于上游 `Hermes-Agent` runtime。
- 因此，当前仓库**还没有**真正完成上游 `Hermes-Agent` 集成。

## 仍然成立的本地能力

- `NSFCWorkspace` schema-backed validation
- `grant_run_id / workspace_id / draft_id / program_id` 的句柄分离
- critique / revision / re-review linkage
- local run journal / stop reason / stage-action envelope
- local artifact bundle / final package / hosted-friendly contract bundle 导出

这些能力今天都是真实可用的，但 owner 仍在 repo-local code，而不是上游 `Hermes-Agent`。

## 长线目标

- 让上游 `Hermes-Agent` 接手 session / run / resume / interrupt / hosted handoff 这类 runtime substrate 责任。
- 让 `Med Auto Grant` 继续保留 author-side grant semantics、workspace object model、critique / revision / final package / audit / gate truth。

## 历史材料的重分类

下面这些文档继续保留，但应被理解为“本地迁移工件 / 历史误导路径”，而不是当前已落地的上游集成事实：

- `2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md`
- `2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md`

## 下一步允许做什么

1. 冻结“什么才算真正接入上游 `Hermes-Agent`”。
2. 把 current-program pointer、README、核心 docs 与测试口径对齐到这份 truth reset。
3. 在不改写 grant domain semantics 的前提下，逐步把 runtime substrate 责任迁到真实的上游 `Hermes-Agent` pilot。
