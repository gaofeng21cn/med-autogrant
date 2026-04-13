from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
README_EN = REPO_ROOT / "README.md"
README_ZH = REPO_ROOT / "README.zh-CN.md"
DOCS_README_EN = REPO_ROOT / "docs" / "README.md"
DOCS_README_ZH = REPO_ROOT / "docs" / "README.zh-CN.md"
CORE_PROJECT = REPO_ROOT / "docs" / "project.md"
CORE_ARCHITECTURE = REPO_ROOT / "docs" / "architecture.md"
CORE_INVARIANTS = REPO_ROOT / "docs" / "invariants.md"
CORE_DECISIONS = REPO_ROOT / "docs" / "decisions.md"
CORE_STATUS = REPO_ROOT / "docs" / "status.md"
DOMAIN_POSITIONING_EN = REPO_ROOT / "docs" / "domain-positioning.md"
DOMAIN_POSITIONING_ZH = REPO_ROOT / "docs" / "domain-positioning.zh-CN.md"
TRUTH_RESET_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md"
)
FAST_CUTOVER_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md"
)
PRODUCT_ENTRY_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md"
)
SCHEMA_BACKED_ENTRY_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md"
)
EXECUTOR_ROUTING_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-author-side-executor-routing-contract-current-truth.md"
)
CRITIQUE_EXECUTOR_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-13-critique-codex-cli-autonomous-executor-current-truth.md"
)
HERMES_NATIVE_CRITIQUE_PROOF_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-13-hermes-native-critique-proof-current-truth.md"
)
PENDING_ROUTE_MATRIX_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md"
)
HOSTED_CONTRACT_BUNDLE_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md"
)
HOSTED_CALLER_CONSUMPTION_PROOF_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-hosted-caller-consumption-proof-current-truth.md"
)
IDEAL_TARGET_PHASE_MAP_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md"
)
P4A_PRODUCT_PROJECTION_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md"
)
P4B_DIRECT_ENTRY_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-p4b-direct-grant-entry-composition-current-truth.md"
)
P4C_USER_LOOP_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md"
)
P4F_SUBMISSION_READY_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-13-p4f-local-submission-ready-package-current-truth.md"
)
IDEAL_TARGET_EXECUTION_PLAN = (
    REPO_ROOT / "docs" / "plans" / "2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md"
)
HERMES_PROGRAM_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md"
)
HERMES_MIGRATION_MAP = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md"
)
RUNTIME_STATE_SESSIONS_DISPLAY = "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@pytest.mark.meta
def test_core_docs_publish_truth_reset_runtime_topology_and_bridge_boundary() -> None:
    for path in (
        README_EN,
        README_ZH,
        DOCS_README_EN,
        DOCS_README_ZH,
        CORE_PROJECT,
        CORE_ARCHITECTURE,
        CORE_STATUS,
    ):
        text = _read(path)
        assert "Hermes-Agent" in text
        assert "CLI" in text
        assert "MCP" in text
        assert "controller" in text

    invariants = _read(CORE_INVARIANTS)
    assert "CLI-first with real upstream Hermes-Agent runtime substrate" in invariants
    assert "domain adapter / entry adapter" in invariants

    decisions = _read(CORE_DECISIONS)
    assert "repo-local runtime" in decisions
    assert "上游 Hermes-Agent 目标" in decisions


@pytest.mark.meta
def test_domain_positioning_public_docs_follow_truth_reset_mainline() -> None:
    for path in (DOMAIN_POSITIONING_EN, DOMAIN_POSITIONING_ZH):
        text = _read(path)
        assert "real upstream Hermes-Agent runtime substrate" in text
        assert "compatibility bridge" in text
        assert "regression oracle" in text or "regression oracle" in text


@pytest.mark.meta
def test_readme_current_maturity_cards_follow_truth_reset_status() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)

    assert "real upstream `Hermes-Agent` runtime substrate" in readme_en
    assert "MedAutoGrantDomainEntry" in readme_en
    assert "actual hosted runtime" in readme_en

    assert "真实上游 `Hermes-Agent` runtime substrate" in readme_zh
    assert "MedAutoGrantDomainEntry" in readme_zh
    assert "submission-ready" in readme_zh


@pytest.mark.meta
def test_core_docs_publish_p4a_direct_product_projection_boundary() -> None:
    for path in (
        README_EN,
        README_ZH,
        DOCS_README_EN,
        DOCS_README_ZH,
        CORE_PROJECT,
        CORE_ARCHITECTURE,
        CORE_STATUS,
    ):
        text = _read(path)
        assert "grant-progress" in text
        assert "grant-cockpit" in text
        assert "grant-direct-entry" in text or "P4.B" in text
        assert "grant-user-loop" in text or "P4.C" in text

    architecture = _read(CORE_ARCHITECTURE)
    assert "controller-owned" in architecture
    assert "supported_commands" in architecture
    assert "grant-progress.schema.json" in architecture
    assert "grant-cockpit.schema.json" in architecture
    assert "grant-direct-entry.schema.json" in architecture
    assert "grant-user-loop.schema.json" in architecture

    status = _read(CORE_STATUS)
    assert "P4.A" in status
    assert "P4.B" in status
    assert "P4.C" in status
    assert "read-only" in status
    assert "schema-backed" in status
    assert "fail-closed" in status


@pytest.mark.meta
def test_repo_tracks_truth_reset_surface_and_historical_migration_map() -> None:
    assert FAST_CUTOVER_CURRENT_TRUTH.exists(), f"Fast cutover current truth 不存在: {FAST_CUTOVER_CURRENT_TRUTH}"
    assert TRUTH_RESET_CURRENT_TRUTH.exists(), f"Truth reset current truth 不存在: {TRUTH_RESET_CURRENT_TRUTH}"
    assert SCHEMA_BACKED_ENTRY_CURRENT_TRUTH.exists(), (
        f"Schema-backed product entry current truth 不存在: {SCHEMA_BACKED_ENTRY_CURRENT_TRUTH}"
    )
    assert EXECUTOR_ROUTING_CURRENT_TRUTH.exists(), f"Executor routing current truth 不存在: {EXECUTOR_ROUTING_CURRENT_TRUTH}"
    assert CRITIQUE_EXECUTOR_CURRENT_TRUTH.exists(), (
        f"Critique executor current truth 不存在: {CRITIQUE_EXECUTOR_CURRENT_TRUTH}"
    )
    assert HERMES_NATIVE_CRITIQUE_PROOF_CURRENT_TRUTH.exists(), (
        f"Hermes-native critique proof current truth 不存在: {HERMES_NATIVE_CRITIQUE_PROOF_CURRENT_TRUTH}"
    )
    assert PENDING_ROUTE_MATRIX_CURRENT_TRUTH.exists(), (
        f"Pending route matrix current truth 不存在: {PENDING_ROUTE_MATRIX_CURRENT_TRUTH}"
    )
    assert HOSTED_CONTRACT_BUNDLE_CURRENT_TRUTH.exists(), (
        f"Hosted contract bundle current truth 不存在: {HOSTED_CONTRACT_BUNDLE_CURRENT_TRUTH}"
    )
    assert HOSTED_CALLER_CONSUMPTION_PROOF_CURRENT_TRUTH.exists(), (
        f"Hosted caller consumption proof current truth 不存在: {HOSTED_CALLER_CONSUMPTION_PROOF_CURRENT_TRUTH}"
    )
    assert IDEAL_TARGET_PHASE_MAP_CURRENT_TRUTH.exists(), (
        f"Ideal target phase map current truth 不存在: {IDEAL_TARGET_PHASE_MAP_CURRENT_TRUTH}"
    )
    assert P4A_PRODUCT_PROJECTION_CURRENT_TRUTH.exists(), (
        f"P4.A product projection current truth 不存在: {P4A_PRODUCT_PROJECTION_CURRENT_TRUTH}"
    )
    assert P4B_DIRECT_ENTRY_CURRENT_TRUTH.exists(), (
        f"P4.B direct entry current truth 不存在: {P4B_DIRECT_ENTRY_CURRENT_TRUTH}"
    )
    assert P4C_USER_LOOP_CURRENT_TRUTH.exists(), (
        f"P4.C grant user loop current truth 不存在: {P4C_USER_LOOP_CURRENT_TRUTH}"
    )
    assert P4F_SUBMISSION_READY_CURRENT_TRUTH.exists(), (
        f"P4.F submission-ready current truth 不存在: {P4F_SUBMISSION_READY_CURRENT_TRUTH}"
    )
    assert IDEAL_TARGET_EXECUTION_PLAN.exists(), f"Ideal target execution plan 不存在: {IDEAL_TARGET_EXECUTION_PLAN}"
    assert HERMES_PROGRAM_TRUTH.exists(), f"Hermes runtime program truth 不存在: {HERMES_PROGRAM_TRUTH}"
    assert HERMES_MIGRATION_MAP.exists(), f"Hermes migration map 不存在: {HERMES_MIGRATION_MAP}"

    fast_cutover = _read(FAST_CUTOVER_CURRENT_TRUTH)
    truth_reset = _read(TRUTH_RESET_CURRENT_TRUTH)
    schema_backed_entry_truth = _read(SCHEMA_BACKED_ENTRY_CURRENT_TRUTH)
    executor_routing_truth = _read(EXECUTOR_ROUTING_CURRENT_TRUTH)
    critique_executor_truth = _read(CRITIQUE_EXECUTOR_CURRENT_TRUTH)
    hermes_native_critique_proof_truth = _read(HERMES_NATIVE_CRITIQUE_PROOF_CURRENT_TRUTH)
    pending_route_matrix_truth = _read(PENDING_ROUTE_MATRIX_CURRENT_TRUTH)
    hosted_contract_bundle_truth = _read(HOSTED_CONTRACT_BUNDLE_CURRENT_TRUTH)
    hosted_caller_consumption_truth = _read(HOSTED_CALLER_CONSUMPTION_PROOF_CURRENT_TRUTH)
    ideal_target_phase_map_truth = _read(IDEAL_TARGET_PHASE_MAP_CURRENT_TRUTH)
    p4a_product_projection_truth = _read(P4A_PRODUCT_PROJECTION_CURRENT_TRUTH)
    p4b_direct_entry_truth = _read(P4B_DIRECT_ENTRY_CURRENT_TRUTH)
    p4c_user_loop_truth = _read(P4C_USER_LOOP_CURRENT_TRUTH)
    p4f_submission_ready_truth = _read(P4F_SUBMISSION_READY_CURRENT_TRUTH)
    ideal_target_execution_plan = _read(IDEAL_TARGET_EXECUTION_PLAN)
    program_truth = _read(HERMES_PROGRAM_TRUTH)
    migration_map = _read(HERMES_MIGRATION_MAP)

    assert "landed / current truth" in fast_cutover
    assert "probe-upstream-hermes" in fast_cutover
    assert "MedAutoGrantDomainEntry" in fast_cutover
    assert "service-safe domain entry" in fast_cutover
    assert PRODUCT_ENTRY_CURRENT_TRUTH.exists(), f"Product entry current truth 不存在: {PRODUCT_ENTRY_CURRENT_TRUTH}"

    product_entry_truth = _read(PRODUCT_ENTRY_CURRENT_TRUTH)
    assert "build-product-entry" in product_entry_truth
    assert "direct" in product_entry_truth
    assert "opl-handoff" in product_entry_truth
    assert "runtime_session_contract" in product_entry_truth
    assert "return_surface_contract" in product_entry_truth
    assert "MedAutoGrantDomainEntry" in product_entry_truth
    assert "executor_routing_contract" in product_entry_truth
    assert "handoff_requirements" in product_entry_truth
    assert "author_side_route_catalog" in product_entry_truth
    assert "domain_entry_contract" in product_entry_truth
    assert "supported_commands" in product_entry_truth
    assert "command_contracts" in product_entry_truth
    assert (
        "direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / frozen"
        in product_entry_truth
    )
    assert "schema-backed" in schema_backed_entry_truth
    assert "executor-routing-contract.schema.json" in schema_backed_entry_truth
    assert "product-entry.schema.json" in schema_backed_entry_truth
    assert "fail-closed" in schema_backed_entry_truth
    assert "author_side_route_catalog" in schema_backed_entry_truth

    assert "critique" in executor_routing_truth
    assert "landed" in executor_routing_truth
    assert "execute-critique-pass" in executor_routing_truth
    assert "execute-revision-pass" in executor_routing_truth
    assert "build-artifact-bundle" in executor_routing_truth
    assert "build-final-package" in executor_routing_truth
    assert "build-hosted-contract-bundle" in executor_routing_truth
    assert "handoff_requirements" in executor_routing_truth
    assert "direction_screening" in executor_routing_truth
    assert "drafting" in executor_routing_truth
    assert "frozen" in executor_routing_truth
    assert "required_summary_fields" in executor_routing_truth
    assert "required_gate_fields" in executor_routing_truth

    assert "execute-critique-pass" in critique_executor_truth
    assert "run_codex_exec" in critique_executor_truth
    assert "Codex CLI autonomous" in critique_executor_truth
    assert "inherit_local_codex_default" in critique_executor_truth
    assert "MED_AUTOGRANT_CODEX_MODEL" in critique_executor_truth
    assert "MED_AUTOGRANT_CODEX_REASONING_EFFORT" in critique_executor_truth
    assert "critique_execution.executor" in critique_executor_truth
    assert "full agent loop" in critique_executor_truth
    assert "executor_kind = hermes_native_proof" in hermes_native_critique_proof_truth
    assert "run_agent.AIAgent.run_conversation" in hermes_native_critique_proof_truth
    assert "~/.hermes/config.yaml" in hermes_native_critique_proof_truth
    assert "MED_AUTOGRANT_HERMES_MODEL" in hermes_native_critique_proof_truth
    assert "tool_start / tool_complete" in hermes_native_critique_proof_truth
    assert "PROVIDER_REASONING_NOT_PROVED_KEEP_DEFAULT" in hermes_native_critique_proof_truth

    assert "direction_screening" in pending_route_matrix_truth
    assert "question_refinement" in pending_route_matrix_truth
    assert "argument_building" in pending_route_matrix_truth
    assert "fit_alignment" in pending_route_matrix_truth
    assert "outline" in pending_route_matrix_truth
    assert "drafting" in pending_route_matrix_truth
    assert "frozen" in pending_route_matrix_truth
    assert "required_summary_fields" in pending_route_matrix_truth
    assert "required_gate_fields" in pending_route_matrix_truth

    assert "hosted contract bundle" in hosted_contract_bundle_truth.lower()
    assert "domain_entry_contract" in hosted_contract_bundle_truth
    assert "schema_contract" in hosted_contract_bundle_truth
    assert "authoring_contract" in hosted_contract_bundle_truth
    assert "hosted-contract-bundle.schema.json" in hosted_contract_bundle_truth
    assert "fail-closed" in hosted_contract_bundle_truth
    assert "OPL" in hosted_contract_bundle_truth
    assert "runtime_substrate_contract" in hosted_contract_bundle_truth
    assert "runtime_state_contract" in hosted_contract_bundle_truth
    assert "operator_contract" in hosted_contract_bundle_truth
    assert "supported_commands" in hosted_contract_bundle_truth
    assert "command_contracts" in hosted_contract_bundle_truth

    assert "hosted caller" in hosted_caller_consumption_truth.lower()
    assert "external caller" in hosted_caller_consumption_truth
    assert "domain_entry_contract" in hosted_caller_consumption_truth
    assert "schema_contract" in hosted_caller_consumption_truth
    assert "authoring_contract" in hosted_caller_consumption_truth
    assert "supported_commands" in hosted_caller_consumption_truth
    assert "command_contracts" in hosted_caller_consumption_truth
    assert "without repo-local helper" in hosted_caller_consumption_truth
    assert "P3" in hosted_caller_consumption_truth
    assert "completed" in hosted_caller_consumption_truth
    assert "critique" in hosted_caller_consumption_truth

    assert "OPL" in ideal_target_phase_map_truth
    assert "理想目标" in ideal_target_phase_map_truth
    assert "phase map" in ideal_target_phase_map_truth.lower()
    assert "User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry" in ideal_target_phase_map_truth
    assert "Hermes-Agent" in ideal_target_phase_map_truth
    assert "MedAutoGrantDomainEntry" in ideal_target_phase_map_truth
    assert "P3" in ideal_target_phase_map_truth
    assert "P4" in ideal_target_phase_map_truth
    assert "P3" in ideal_target_phase_map_truth and "completed" in ideal_target_phase_map_truth
    assert "next" in ideal_target_phase_map_truth.lower()
    assert "P4.A" in ideal_target_phase_map_truth
    assert "P4.B" in ideal_target_phase_map_truth
    assert "P4.C" in ideal_target_phase_map_truth

    assert "grant-progress" in p4a_product_projection_truth
    assert "grant-cockpit" in p4a_product_projection_truth
    assert "controller-owned" in p4a_product_projection_truth
    assert "read-only" in p4a_product_projection_truth
    assert "schema-backed" in p4a_product_projection_truth
    assert "fail-closed" in p4a_product_projection_truth
    assert "grant-progress.schema.json" in p4a_product_projection_truth
    assert "grant-cockpit.schema.json" in p4a_product_projection_truth
    assert "summarize-workspace" in p4a_product_projection_truth
    assert "stage-route-report" in p4a_product_projection_truth
    assert "critique-summary" in p4a_product_projection_truth
    assert "build-product-entry" in p4a_product_projection_truth
    assert "supported_commands" in p4a_product_projection_truth
    assert "没有被写进 `domain_entry_contract.supported_commands`" in p4a_product_projection_truth
    assert "也不进入 hosted contract bundle 的 command catalog" in p4a_product_projection_truth

    assert "grant-direct-entry" in p4b_direct_entry_truth
    assert "grant_direct_entry" in p4b_direct_entry_truth
    assert "build-product-entry" in p4b_direct_entry_truth
    assert "grant-cockpit" in p4b_direct_entry_truth
    assert "grant-progress" in p4b_direct_entry_truth
    assert "grant-direct-entry.schema.json" in p4b_direct_entry_truth
    assert "schema-backed" in p4b_direct_entry_truth
    assert "fail-closed" in p4b_direct_entry_truth
    assert "不进入 `domain_entry_contract.supported_commands`" in p4b_direct_entry_truth or "不进入 hosted contract bundle 的 command catalog" in p4b_direct_entry_truth

    assert "grant-user-loop" in p4c_user_loop_truth
    assert "grant_user_loop" in p4c_user_loop_truth
    assert "mainline-status" in p4c_user_loop_truth
    assert "mainline-phase" in p4c_user_loop_truth
    assert "grant-user-loop.schema.json" in p4c_user_loop_truth
    assert "schema-backed" in p4c_user_loop_truth
    assert "fail-closed" in p4c_user_loop_truth
    assert "不进入 `domain_entry_contract.supported_commands`" in p4c_user_loop_truth or "不进入 hosted contract bundle 的 command catalog" in p4c_user_loop_truth

    assert "build-submission-ready-package" in p4f_submission_ready_truth
    assert "submission-ready-package.schema.json" in p4f_submission_ready_truth
    assert "fail-closed" in p4f_submission_ready_truth
    assert "external submission" in p4f_submission_ready_truth.lower() or "官网提交" in p4f_submission_ready_truth

    assert "# Med Auto Grant OPL-Aligned Target Shape And Hosted Caller Plan" in ideal_target_execution_plan
    assert "Goal:" in ideal_target_execution_plan
    assert "Architecture:" in ideal_target_execution_plan
    assert "Task 1" in ideal_target_execution_plan
    assert "Task 2" in ideal_target_execution_plan
    assert "Task 3" in ideal_target_execution_plan

    assert "还没有**真正完成上游 `Hermes-Agent` 集成" in truth_reset or "还没有" in truth_reset
    assert "repo-local code" in truth_reset
    assert "run-local" in truth_reset
    assert "build-hosted-contract-bundle" in truth_reset

    assert "Hermes-backed runtime substrate" in program_truth
    assert "history" not in program_truth.lower()
    assert "CLI" in program_truth
    assert "MCP" in program_truth
    assert "controller" in program_truth
    assert "Auto-only" in program_truth
    assert "compatibility bridge" in program_truth
    assert "regression oracle" in program_truth
    assert RUNTIME_STATE_SESSIONS_DISPLAY in program_truth
    assert "runtime_substrate_contract" in program_truth
    assert "runtime_state_contract" in program_truth
    assert "operator_contract" in program_truth

    assert "validate-workspace" in migration_map
    assert "summarize-workspace" in migration_map
    assert "next-step" in migration_map
    assert "critique-summary" in migration_map
    assert "stage-route-report" in migration_map
    assert "run-local" in migration_map
    assert "resume-local" in migration_map
    assert "execute-revision-pass" in migration_map
    assert "build-final-package" in migration_map
    assert "build-hosted-contract-bundle" in migration_map
    assert "revised-workspace output identity guard" in migration_map
    assert "artifact-bundle 输入加载" in migration_map
    assert "bundle output identity guard" in migration_map
    assert "final package document assembly" in migration_map
    assert "Hermes substrate" in migration_map
    assert "Grant domain logic" in migration_map
    assert RUNTIME_STATE_SESSIONS_DISPLAY in migration_map
    assert "runtime_substrate_contract" in migration_map
    assert "runtime_state_contract" in migration_map
    assert "operator_contract" in migration_map


@pytest.mark.meta
def test_entry_docs_freeze_product_entry_and_opl_handoff_on_top_of_landed_runtime_substrate() -> None:
    reference = REPO_ROOT / "docs" / "references" / "lightweight_product_entry_and_opl_handoff.md"
    reference_text = _read(reference)

    for path in (README_EN, README_ZH, DOCS_README_EN, DOCS_README_ZH, CORE_PROJECT, CORE_ARCHITECTURE, CORE_STATUS):
        text = _read(path)
        assert "product entry" in text
        assert "OPL" in text

    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)
    docs_readme_en = _read(DOCS_README_EN)
    docs_readme_zh = _read(DOCS_README_ZH)
    architecture = _read(CORE_ARCHITECTURE)
    status = _read(CORE_STATUS)

    assert "build-submission-ready-package" in readme_en
    assert "build-submission-ready-package" in readme_zh
    assert "./specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md" in docs_readme_en
    assert "./specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md" in docs_readme_zh
    assert "submission_ready_package" in architecture
    assert "build-submission-ready-package" in status

    assert "lightweight structured `product entry` shell is now landed" in readme_en
    assert "`build-product-entry`" in readme_en
    assert "richer grant-facing product experience still remains future work" in readme_en
    assert "轻量结构化 `product entry` shell 已经落地" in readme_zh
    assert "`build-product-entry`" in readme_zh
    assert "更完整的 grant-facing 产品体验仍要继续补" in readme_zh

    assert "lightweight grant `product entry` shell" in docs_readme_en
    assert "Product-entry shell" in docs_readme_en
    assert "./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md" in docs_readme_en
    assert "./references/lightweight_product_entry_and_opl_handoff.md" in docs_readme_en
    assert "轻量 grant `product entry` shell" in docs_readme_zh
    assert "产品入口 shell" in docs_readme_zh
    assert "./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md" in docs_readme_zh
    assert "./references/lightweight_product_entry_and_opl_handoff.md" in docs_readme_zh

    assert "User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry" in architecture
    assert "build-product-entry" in architecture
    assert "workspace_id" in architecture
    assert "draft_id" in architecture
    assert "funding_call" in architecture
    assert "schema-backed contract" in architecture
    assert "OPL -> Med Auto Grant" in status
    assert "build-product-entry" in status
    assert "schema-backed" in status

    assert "target_domain_id" in reference_text
    assert "task_intent" in reference_text
    assert "entry_mode" in reference_text
    assert "workspace_locator" in reference_text
    assert "runtime_session_contract" in reference_text
    assert "return_surface_contract" in reference_text
    assert "workspace_id" in reference_text
    assert "draft_id" in reference_text
    assert "funding_call" in reference_text
    assert "runtime substrate 已经真正落在上游 `Hermes-Agent` 上" in reference_text
    assert "build-product-entry" in reference_text


@pytest.mark.meta
def test_docs_and_contracts_index_schema_backed_product_entry_and_routing_contract() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)
    docs_readme_en = _read(DOCS_README_EN)
    docs_readme_zh = _read(DOCS_README_ZH)
    decisions = _read(CORE_DECISIONS)
    current_program = (REPO_ROOT / "contracts" / "runtime-program" / "current-program.json").read_text(encoding="utf-8")
    contracts_readme = (REPO_ROOT / "contracts" / "README.md").read_text(encoding="utf-8")

    assert "schema-backed" in readme_en
    assert "schema-backed" in readme_zh
    assert "./specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md" in docs_readme_en
    assert "./specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md" in docs_readme_zh
    assert "schema-backed" in decisions
    assert "2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md" in current_program
    assert "schema-backed" in contracts_readme


@pytest.mark.meta
def test_docs_publish_schema_backed_p4a_projection_contract_boundary() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)
    docs_readme_en = _read(DOCS_README_EN)
    docs_readme_zh = _read(DOCS_README_ZH)
    project = _read(CORE_PROJECT)
    architecture = _read(CORE_ARCHITECTURE)
    status = _read(CORE_STATUS)
    decisions = _read(CORE_DECISIONS)
    contracts_readme = (REPO_ROOT / "contracts" / "README.md").read_text(encoding="utf-8")

    assert "schema-backed" in readme_en
    assert "schema-backed" in readme_zh
    assert "schema-backed" in docs_readme_en
    assert "schema-backed" in docs_readme_zh
    assert "schema-backed" in project
    assert "schema-backed" in architecture
    assert "schema-backed" in status
    assert "schema-backed" in decisions
    assert "grant-progress.schema.json" in architecture
    assert "grant-cockpit.schema.json" in architecture
    assert "grant-direct-entry.schema.json" in architecture
    assert "grant-user-loop.schema.json" in architecture
    assert "grant-progress.schema.json" in contracts_readme
    assert "grant-cockpit.schema.json" in contracts_readme
    assert "grant-direct-entry.schema.json" in contracts_readme
    assert "grant-user-loop.schema.json" in contracts_readme


@pytest.mark.meta
def test_docs_and_contracts_index_hosted_contract_bundle_contract_catalog_truth() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)
    docs_readme_en = _read(DOCS_README_EN)
    docs_readme_zh = _read(DOCS_README_ZH)
    architecture = _read(CORE_ARCHITECTURE)
    status = _read(CORE_STATUS)
    decisions = _read(CORE_DECISIONS)
    current_program = (REPO_ROOT / "contracts" / "runtime-program" / "current-program.json").read_text(encoding="utf-8")
    contracts_readme = (REPO_ROOT / "contracts" / "README.md").read_text(encoding="utf-8")

    for text in (readme_en, readme_zh, architecture, status, decisions, contracts_readme):
        assert "domain_entry_contract" in text
        assert "schema_contract" in text
        assert "authoring_contract" in text

    assert "./specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md" in docs_readme_en
    assert "./specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md" in docs_readme_zh
    assert "hosted contract bundle" in readme_en.lower()
    assert "托管友好的 handoff contract" in readme_zh
    assert "hosted-contract-bundle.schema.json" in architecture
    assert "hosted_contract_bundle" in status
    assert "2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md" in current_program
    assert "supported_commands" in readme_en
    assert "supported_commands" in readme_zh
    assert "command_contracts" in architecture
    assert "command_contracts" in decisions


@pytest.mark.meta
def test_docs_and_contracts_index_hosted_caller_consumption_proof_truth() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)
    docs_readme_en = _read(DOCS_README_EN)
    docs_readme_zh = _read(DOCS_README_ZH)
    project = _read(CORE_PROJECT)
    status = _read(CORE_STATUS)
    architecture = _read(CORE_ARCHITECTURE)
    current_program = (REPO_ROOT / "contracts" / "runtime-program" / "current-program.json").read_text(encoding="utf-8")

    for text in (readme_en, readme_zh, project, status, architecture):
        assert "external caller" in text or "外部 caller" in text or "hosted caller" in text or "hosted caller" in text.lower()
        assert "domain_entry_contract" in text
        assert "command_contracts" in text

    assert "./specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md" in docs_readme_en
    assert "./specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md" in docs_readme_zh
    assert "2026-04-12-hosted-caller-consumption-proof-current-truth.md" in current_program


@pytest.mark.meta
def test_docs_and_contracts_index_opl_aligned_ideal_target_and_phase_map() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)
    docs_readme_en = _read(DOCS_README_EN)
    docs_readme_zh = _read(DOCS_README_ZH)
    project = _read(CORE_PROJECT)
    status = _read(CORE_STATUS)
    architecture = _read(CORE_ARCHITECTURE)
    current_program = (REPO_ROOT / "contracts" / "runtime-program" / "current-program.json").read_text(encoding="utf-8")

    for text in (readme_en, readme_zh, project, status, architecture):
        assert "ideal target" in text.lower() or "理想目标" in text
        assert "OPL" in text

    assert "./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md" in docs_readme_en
    assert "./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md" in docs_readme_zh
    assert "./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md" in docs_readme_en
    assert "./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md" in docs_readme_zh
    assert "2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md" in current_program
    assert "phase_map" in current_program
    assert "ideal_target" in current_program
    assert '"phase_id": "P3"' in current_program and '"status": "completed"' in current_program
    assert '"phase_id": "P4"' in current_program and '"status": "next"' in current_program
