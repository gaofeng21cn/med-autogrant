# Contracts

- `contracts/runtime-program/current-program.json`：当前 repo-tracked 的 Med Auto Grant 主线合同。
- 当前 `product entry` / `executor routing` / `pending handoff` 也已经作为 schema-backed contract 固定在 `schemas/v1/`，并由 `schema-index.json` 统一索引。
- 机器本地 session、log、report、prompt 与其他运行态不再落在仓库根目录，统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 本地 `run-local / resume-local` journal 默认写到 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`。
- `build-hosted-contract-bundle` 会把当前 `current-program` pointer、runtime-state durable surface 与 canonical operator surface 一起导出到 hosted-friendly contract bundle。
