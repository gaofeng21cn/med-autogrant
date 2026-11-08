from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from med_autogrant.control_plane import (
    read_current_program_contract as _read_current_program_contract_from_contract,
    read_program_id as _read_program_id_from_contract,
    runtime_state_display_path,
)
from med_autogrant.domain_entry_contract import (
    SERVICE_SAFE_ENTRY_ADAPTER,
    SERVICE_SAFE_ENTRY_SURFACE_KIND,
    build_domain_entry_contract,
)
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace_types import WorkspaceStateError
from opl_framework.schema_validation import SchemaSubsetValidator

from .shared import (
    AUTHOR_SIDE_ROUTE_IDS,
    CURRENT_PROGRAM_RELATIVE_PATH,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
    EXECUTOR_ROUTE_OWNER,
    EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE,
    EXECUTOR_ROUTING_CONTRACT_VERSION,
    HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE,
    HOSTED_CONTRACT_SCHEMA_FILES,
    SCHEMA_INDEX_RELATIVE_PATH,
)
from .contract_leaves.route_contracts import (
    AUTHOR_SIDE_ROUTE_COMMANDS,
    build_author_side_route_command,
    build_author_side_route_contract,
    build_executor_routing_contract,
    build_service_safe_domain_surface,
    build_stage_route_contract,
    require_known_route_id,
    require_nonempty_route_id,
    validate_executor_routing_contract,
)
from .contract_leaves.runtime_contracts import (
    build_hosted_authoring_contract,
    build_operator_contract,
    build_runtime_state_contract,
    build_runtime_substrate_contract,
    build_schema_contract,
    directory_display_path,
    read_current_program_contract,
    read_program_id,
    require_nonempty_string,
    validate_hosted_contract_bundle,
)
from .contract_leaves.schema_validation import (
    validate_contract_schema,
    validate_schema_payload,
)
from .contract_leaves.scholar_binding import (
    SCHOLAR_SKILL_BINDING_CONTRACT_RELATIVE_PATH,
    SCHOLAR_SKILL_REQUIRED_BLOCK_FIELDS,
    SCHOLAR_SKILL_REQUIRED_NON_USABLE_OBSERVATIONS,
    build_direct_scholar_skill_prompt_lines,
    read_scholar_skill_binding_contract,
    scholar_skill_ids_for_direct_route,
)
