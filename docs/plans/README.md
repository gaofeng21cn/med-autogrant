# Active Plans

This directory is reserved for active or explicitly future planning work that has not yet been absorbed into the core docs, contract surfaces, or historical archive.

The active plan lane now uses direct retirement as its cleanup posture: obsolete modules, interfaces, CLI shell aliases, facade patch bridges, and aggregate compatibility tests are not kept as compatibility surfaces once core docs, contracts, source, or tests have replaced them. If an active caller still exists, move it to the latest owner surface, then delete or archive the old surface.

Current active plan:

- [MAG ideal-state gap and completion plan](./mag-ideal-state-cross-repo-gap-plan.zh-CN.md): focuses on production live soak, no-regression evidence, memory-apply generalization, OPL generic primitive absorption, and legacy direct retirement.

Completed one-time planning artifacts now live under:

- [Historical plans](../history/plans/README.md)

Current project truth and maintainer guidance live in:

- [Docs Guide](../README.md)
- [Project](../project.md)
- [Status](../status.md)
- [Architecture](../architecture.md)
- [Invariants](../invariants.md)
- [Decisions](../decisions.md)
- [`current-program.json`](../../contracts/runtime-program/current-program.json)
