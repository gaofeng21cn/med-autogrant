# Contracts

- `contracts/runtime-program/current-program.json`：当前 repo-tracked 的 Med Auto Grant 主线合同。
- 当前 `product entry` / `executor routing` / `pending handoff` / `grant-progress` / `grant-cockpit` 也已经作为 schema-backed contract 固定在 `schemas/v1/`，并由 `schema-index.json` 统一索引；其中 `grant-progress.schema.json` 与 `grant-cockpit.schema.json` 会把 direct-product projection 收口成 generation-time fail-closed contract。
- 机器本地 session、log、report、prompt 与其他运行态不再落在仓库根目录，统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 本地 `run-local / resume-local` journal 默认写到 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`。
- `build-hosted-contract-bundle` 会把当前 `current-program` pointer、runtime-state durable surface 与 canonical operator surface 一起导出到 hosted-friendly contract bundle，并额外显式携带 `domain_entry_contract`、`schema_contract`、`authoring_contract`。
- 共享 `domain_entry_contract` 当前还会固定 `supported_commands` 与 `command_contracts`，供 external caller 直接消费。
- `schemas/v1/hosted-contract-bundle.schema.json` 现在定义整份 hosted contract bundle 的 fail-closed 结构。
- `contracts/runtime-program/current-program.json` 现在还额外固定了 `ideal_target` 与 `phase_map`，用于说明 `OPL` / `Hermes-Agent` / `Med Auto Grant` 的理想分工，以及当前已经完成到哪个阶段。
