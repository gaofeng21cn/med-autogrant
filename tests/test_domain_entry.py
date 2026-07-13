from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.workspace import WorkspaceStateError


def test_domain_entry_dispatches_declared_runtime_target() -> None:
    runtime = Mock()
    with patch(
        "med_autogrant.domain_entry.grant_quality_scorecard",
        return_value={"ok": True},
    ) as target:
        payload = MedAutoGrantDomainEntry(runtime=runtime).dispatch(
            {"command": "grant-quality-scorecard", "input_path": "/tmp/workspace.json"}
        )

    assert payload == {"command": "grant-quality-scorecard", "ok": True}
    target.assert_called_once_with(runtime, input_path="/tmp/workspace.json")


def test_domain_entry_rejects_missing_required_field() -> None:
    with pytest.raises(WorkspaceStateError, match="缺少必填字段: output_path"):
        MedAutoGrantDomainEntry(runtime=Mock()).dispatch(
            {"command": "build-artifact-bundle", "input_path": "/tmp/workspace.json"}
        )


def test_domain_entry_contract_uses_command_catalog_as_single_source() -> None:
    contract = build_domain_entry_contract()
    commands = {item["command"]: item for item in contract["command_contracts"]}

    assert set(commands) == set(SERVICE_SAFE_DOMAIN_COMMANDS)
    assert all(not hasattr(spec, "runtime_method") for spec in SERVICE_SAFE_DOMAIN_COMMANDS.values())
    assert contract["domain_agent_entry_spec"]["agent_id"] == "mag"
    assert "execute-critique-revision-loop" not in commands
    assert "execute-authoring-mainline-loop" not in commands
    assert {
        "execute-direction-screening-pass",
        "execute-strategy-authoring-pass",
        "execute-question-refinement-pass",
        "execute-argument-building-pass",
        "execute-fit-alignment-pass",
        "execute-outline-pass",
        "execute-drafting-pass",
        "execute-critique-pass",
        "execute-revision-pass",
        "execute-freeze-pass",
    } <= commands.keys()
