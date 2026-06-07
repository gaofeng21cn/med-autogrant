# MAG product entry parts package-root facade retirement closeout

Owner: `Med Auto Grant`
Purpose: `product_entry_parts_init_facade_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读退役记录。当前机器真相继续归 `src/med_autogrant/product_entry.py`、`src/med_autogrant/product_entry_parts/*` concrete owner modules、tests、CLI/API behavior、runtime receipts 和 `contracts/runtime-program/current-program.json`。

## Closeout

本 lane 退役 `src/med_autogrant/product_entry_parts/__init__.py` 的 package-root lazy `MedAutoGrantProductEntry` re-export facade。

当前 public product-entry class 只从 canonical module 读取：

- `med_autogrant.product_entry.MedAutoGrantProductEntry`

`product_entry_parts/` 是 implementation parts package。包根只保留 marker，不再通过 `__getattr__`、`__all__` 或 package-root import 暴露 `MedAutoGrantProductEntry`。需要使用具体实现 helper 时，调用方应导入对应 concrete owner module；需要 public entry class 时，调用方应导入 `med_autogrant.product_entry`。

## Retired Surface

- `from med_autogrant.product_entry_parts import MedAutoGrantProductEntry`
- `product_entry_parts.__getattr__("MedAutoGrantProductEntry")`
- `product_entry_parts.__all__ = ["MedAutoGrantProductEntry"]`

## Verification

- `rtk ./scripts/run-pytest-clean.sh -q tests/test_opl_standard_pack.py::test_product_entry_canonical_module_keeps_public_export tests/product_entry_cases/test_dependency_structure.py::ProductEntryPartsStructureTest::test_product_entry_parts_package_root_is_marker_only tests/product_entry_cases/test_family_stage_control_plane.py tests/product_entry_cases/test_authority_surface_boundaries.py`
- `rtk ./scripts/verify.sh`
- `rtk git diff --check`
- conflict-marker scan over touched files.

## Out Of Scope

This closeout does not change product-entry manifest semantics, stage control plane semantics, authority surface taxonomy, CLI/API behavior, runtime receipts, grant truth, package/export authority, OPL default-caller status, App projection, domain readiness or production readiness.
