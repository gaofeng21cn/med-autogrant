# Med Auto Grant OPL-Aligned Target Shape And Hosted Caller Plan

Owner: `Med Auto Grant`
Purpose: `historical_opl_aligned_hosted_caller_plan_provenance`
State: `history`
Machine boundary: 本文是人读历史计划，保留 2026-04-12 OPL-aligned target shape、hosted caller proof 和旧 Hermes/Gateway 迁移计划。当前 OPL/Temporal stage-led runtime owner、MAG grant authority、hosted caller evidence、product-entry handoff 与机器行为以核心五件套、active gap plan、history specs lifecycle map、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准；本文不声明 Hermes 默认 owner、OPL Gateway ready 或 active hosted runtime backlog。

> Historical completed plan. `P3 hosted caller / OPL consumption proof` is already completed. Current mainline truth now lives in `docs/project.md`, `docs/decisions.md`, and `contracts/runtime-program/current-program.json`.

**Historical goal:** Prove the then-next honest `P3` phase without inventing new repo-local hosted helpers: external hosted callers and future `OPL Gateway` must consume the already frozen `domain_entry_contract`, `schema_contract`, and `authoring_contract`.

**Historical architecture:** Keep `Hermes-Agent` as substrate owner, keep `Med Auto Grant` as authoring-truth owner, and make the next phase a caller-consumption proof rather than another local runtime rewrite. Reuse `build-product-entry`, `build-hosted-contract-bundle`, and `MedAutoGrantDomainEntry` as the only contract sources.

**Historical tech stack:** Python CLI, repo-tracked markdown current truth, JSON contracts, pytest meta tests

---

### Historical Task 1: Freeze The P3 Proof Boundary

**Files:**
- Modify: `docs/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md`
- Modify: `docs/status.md`
- Test: `tests/test_hermes_runtime_truth.py`

- [ ] **Step 1: Write the failing test**

```python
def test_docs_and_contracts_index_opl_aligned_ideal_target_and_phase_map() -> None:
    assert "./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md" in docs_readme_en
    assert "phase_map" in current_program
    assert "ideal_target" in current_program
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_hermes_runtime_truth.py tests/test_program_control_surfaces.py -q`
Expected: FAIL because the ideal-target current truth and `current-program` phase map are missing.

- [ ] **Step 3: Write minimal implementation**

```md
- `P1` completed
- `P2` completed
- `P3` next
- `P4` future
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_hermes_runtime_truth.py tests/test_program_control_surfaces.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md docs/status.md tests/test_hermes_runtime_truth.py tests/test_program_control_surfaces.py
git commit -m "Freeze OPL-aligned ideal target and phase map"
```

### Historical Task 2: Add Hosted Caller Consumption Truth

**Files:**
- Modify: `docs/architecture.md`
- Modify: `docs/project.md`
- Modify: `docs/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md`
- Test: `tests/test_hermes_runtime_truth.py`

- [ ] **Step 1: Write the failing test**

```python
assert "hosted caller / OPL consumption proof" in ideal_target_phase_map_truth
assert "domain_entry_contract" in hosted_contract_bundle_truth
assert "schema_contract" in hosted_contract_bundle_truth
assert "authoring_contract" in hosted_contract_bundle_truth
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_hermes_runtime_truth.py -q`
Expected: FAIL because P3 consumption proof boundary is not frozen clearly enough.

- [ ] **Step 3: Write minimal implementation**

```md
- next phase: prove external hosted caller / `OPL Gateway` consumes frozen contracts
- do not add new repo-local hosted helper
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_hermes_runtime_truth.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/architecture.md docs/project.md docs/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md tests/test_hermes_runtime_truth.py
git commit -m "Freeze hosted caller proof boundary"
```

### Historical Task 3: Prepare The Next Honest Proof Lane

**Files:**
- Modify: `docs/plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md`
- Modify: `docs/README.md`
- Modify: `docs/README.md`
- Test: `tests/test_hermes_runtime_truth.py`

- [ ] **Step 1: Write the failing test**

```python
assert "./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md" in docs_readme_en
assert "Task 1" in ideal_target_execution_plan
assert "Task 2" in ideal_target_execution_plan
assert "Task 3" in ideal_target_execution_plan
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_hermes_runtime_truth.py -q`
Expected: FAIL because the execution plan is not indexed or not written yet.

- [ ] **Step 3: Write minimal implementation**

```md
### Task 1: Freeze The P3 Proof Boundary
### Task 2: Add Hosted Caller Consumption Truth
### Task 3: Prepare The Next Honest Proof Lane
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_hermes_runtime_truth.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md docs/README.md docs/README.md tests/test_hermes_runtime_truth.py
git commit -m "Add OPL-aligned hosted caller execution plan"
```
