# Contracts

- `contracts/runtime-program/current-program.json`：当前 repo-tracked 的 Med Auto Grant 主线合同。
- 机器本地 session、log、report、prompt 与其他运行态不再落在仓库根目录，统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 本地 `run-local / resume-local` journal 默认写到 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`。
