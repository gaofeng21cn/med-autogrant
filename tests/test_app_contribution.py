from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from med_autogrant.app_contribution import NOTE_ACTION, current_review_feedback, read_contribution, record_review
from med_autogrant.critique_executor import _build_critique_context, _build_critique_prompt
from med_autogrant.domain_entry import dispatch_domain_request
from med_autogrant.workspace_projection_parts import _build_workspace_state
from med_autogrant.workspace_types import WorkspaceStateError

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    shutil.copyfile(ROOT / 'examples/nsfc_workspace_p2c_drafting.json', tmp_path / 'workspace.json')
    return tmp_path


def note_input(root: Path, request_id: str = 'review-1') -> dict:
    item = read_contribution(root, {}, 'route')['data']['items'][0]
    return {**item['actions'][0]['input'], 'request_id': request_id, 'note': '请比较两组预实验，并明确主要终点。'}


def record(root: Path, value: dict) -> dict:
    return dispatch_domain_request({'command': 'record-review-feedback', 'input_path': root / value['workspace_file'],
                                   **{k: v for k, v in value.items() if k != 'workspace_file'}})


def test_owner_projection_feedback_reopen_and_critique_consumption(workspace: Path) -> None:
    source = workspace / 'workspace.json'
    original = source.read_bytes()
    projection = read_contribution(workspace, {}, 'route')
    item = projection['data']['items'][0]
    assert item['workspace_id'] == 'nsfc-demo-001'
    assert item['active_draft']['draft_id'] == item['active_draft_id']
    assert item['mentor_critiques'] == json.loads(original).get('mentor_critiques', [])
    saved = record(workspace, note_input(workspace))
    assert saved['status'] == 'recorded'
    assert saved['continuation']['stage_execution_started'] is False
    assert source.read_bytes() == original
    reread = dispatch_domain_request({'command': 'read-review-feedback', 'input_path': source})
    assert reread['review_notes'][0]['artifact_ref'] == saved['artifact_ref']
    assert reread['review_notes'][0]['matches_current_revision'] is True
    document = json.loads(original)
    context = _build_critique_context(document=document, state=_build_workspace_state(document))
    prompt = _build_critique_prompt(context=context, input_path=source)
    assert note_input(workspace)['note'] in prompt
    assert saved['artifact_ref'] in prompt
    assert 'They do not approve quality or export' in prompt
    assert read_contribution(workspace, {}, 'quality')['data']['items'][0]['review_notes'][0]['request_id'] == 'review-1'


def test_stale_revision_and_duplicate_inputs(workspace: Path) -> None:
    value = note_input(workspace)
    saved = record(workspace, value)
    assert record(workspace, value)['artifact_ref'] == saved['artifact_ref']
    with pytest.raises(WorkspaceStateError, match='不同输入'):
        record(workspace, {**value, 'note': 'different'})
    source = workspace / 'workspace.json'
    document = json.loads(source.read_text())
    document['application_drafts'][0]['version_label'] = 'new-draft'
    source.write_text(json.dumps(document))
    assert record(workspace, value)['matches_current_revision'] is False
    with pytest.raises(WorkspaceStateError, match='已变化'):
        record(workspace, {**value, 'request_id': 'review-2'})
    assert current_review_feedback(source, document) == []
    assert read_contribution(workspace, {}, 'route')['data']['items'][0]['review_notes'][0]['matches_current_revision'] is False


def test_concurrent_duplicate_feedback_is_one_owner_record(workspace: Path) -> None:
    value = note_input(workspace)
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(lambda _: record(workspace, value), range(3)))
    assert len({item['artifact_ref'] for item in results}) == 1
    assert len(list((workspace / 'runtime/review-feedback').glob('*.json'))) == 1


def test_wrong_identity_path_escape_and_runtime_symlink_rejected(workspace: Path, tmp_path_factory) -> None:
    value = note_input(workspace)
    with pytest.raises(WorkspaceStateError, match='不一致'):
        record(workspace, {**value, 'workspace_id': 'other'})
    with pytest.raises(WorkspaceStateError, match='不一致'):
        read_contribution(workspace, {'work_item_identity': {'domain_work_item_id': 'other'}}, 'route')
    with pytest.raises(WorkspaceStateError, match='不属于'):
        read_contribution(workspace, {'work_item_identity': {'agent_id': 'mas'}}, 'route')
    outside = tmp_path_factory.mktemp('outside')
    shutil.copyfile(workspace / 'workspace.json', outside / 'workspace.json')
    with pytest.raises(WorkspaceStateError, match='已登记'):
        read_contribution(workspace, {'workspace_file': str(outside / 'workspace.json')}, 'route')
    (workspace / 'runtime').symlink_to(outside)
    with pytest.raises(WorkspaceStateError, match='申请目录'):
        record(workspace, value)


def test_source_and_carrier_commands_share_owner_and_no_ui_cli(workspace: Path) -> None:
    env = {**os.environ, 'OPL_PROFILE_WORKSPACE': str(workspace), 'PYTHONDONTWRITEBYTECODE': '1'}
    for package_root in (ROOT, ROOT / 'plugins/med-autogrant'):
        read = subprocess.run([sys.executable, 'runtime/app_contribution.py', 'route'], cwd=package_root,
                              input='{}', text=True, capture_output=True, env=env, check=True)
        item = json.loads(read.stdout)['data']['items'][0]
        value = {**item['actions'][0]['input'], 'request_id': 'same-source-carrier', 'note': '对比候选'}
        executed = subprocess.run([sys.executable, 'runtime/app_contribution.py', 'note'], cwd=package_root,
                                 input=json.dumps(value), text=True, capture_output=True, env=env, check=True)
        assert json.loads(executed.stdout)['result']['status'] == 'recorded'
    result = subprocess.run([sys.executable, '-m', 'med_autogrant.cli', 'workspace', 'review-feedback',
                             '--input', str(workspace), '--json'], text=True, capture_output=True, env=env, check=True)
    assert json.loads(result.stdout)['review_notes'][0]['note'] == '对比候选'
    invalid = subprocess.run([sys.executable, 'runtime/app_contribution.py', 'note'], cwd=ROOT,
                             input=json.dumps({**value, 'workspace_id': 'bad'}), text=True, capture_output=True, env=env, check=True)
    assert json.loads(invalid.stdout)['ok'] is False
    assert json.loads(invalid.stdout)['ref'] == NOTE_ACTION


def test_handoff_context_binds_supplied_identity_and_exact_source_and_note(workspace: Path) -> None:
    identity = {"agent_id": "mag", "domain_id": "med-autogrant", "work_item_id": "nsfc-demo-001",
                "domain_work_item_id": "nsfc-demo-001", "work_item_scope_id": "scope-mag-demo",
                "identity_state": "resolved"}
    saved = record(workspace, note_input(workspace))
    item = read_contribution(workspace, {"work_item_identity": identity}, "route")["data"]["items"][0]
    assert item["read_input"]["work_item_identity"] == identity
    assert item["review_context"]["work_item_identity"] == identity
    assert item["review_context"]["artifact_refs"] == ["workspace.json"]
    context = item["review_notes"][0]["review_context"]
    assert context["work_item_identity"] == identity
    assert context["artifact_refs"] == ["workspace.json", "runtime/review-feedback/review-1.json"]
    assert context["artifact_hashes"] == [
        "sha256:" + hashlib.sha256((workspace / ref).read_bytes()).hexdigest()
        for ref in context["artifact_refs"]]
    assert saved["artifact_ref"] == str(workspace / context["artifact_refs"][1])
    assert "work_item_identity" not in saved["review_context"]
    assert "review_context" not in read_contribution(workspace, {}, "route")["data"]["items"][0]


def test_critique_feedback_keeps_the_already_read_candidate_during_source_switch(workspace: Path) -> None:
    from med_autogrant import app_contribution as owner

    source = workspace / "workspace.json"
    original = json.loads(source.read_text())
    first = record(workspace, note_input(workspace))
    old_snapshot = owner._snapshot
    switched = False

    def switch_after_snapshot(path: Path):
        nonlocal switched
        snapshot = old_snapshot(path)
        if path == source and not switched:
            switched = True
            newer = json.loads(source.read_text())
            newer["application_drafts"][0]["version_label"] = "new-candidate"
            source.write_text(json.dumps(newer))
            record(workspace, {**note_input(workspace, "new-note"), "note": "仅对新版本的意见"})
        return snapshot

    with patch.object(owner, "_snapshot", side_effect=switch_after_snapshot):
        feedback = current_review_feedback(source, original)
    assert [note["artifact_ref"] for note in feedback] == [first["artifact_ref"]]
    assert all(note["note"] != "仅对新版本的意见" for note in feedback)


def test_recorded_feedback_continues_same_grant_through_actual_critique_cli(workspace: Path, capsys) -> None:
    from med_autogrant.cli import main
    from med_autogrant.critique_executor import build_critique_execution_document
    from test_critique_executor import CRITIQUE_PACKET_PATH, _closeout_packet, _codex_receipt

    source = workspace / "workspace.json"
    original = json.loads(source.read_text())
    value = note_input(workspace)
    assert main(["workspace", "record-review", "--input", str(source),
                 "--workspace-id", value["workspace_id"], "--grant-run-id", value["grant_run_id"],
                 "--revision", value["revision"], "--request-id", value["request_id"],
                 "--note", value["note"], "--json"]) == 0
    recorded = json.loads(capsys.readouterr().out)
    assert main(["workspace", "review-feedback", "--input", str(source), "--json"]) == 0
    readback = json.loads(capsys.readouterr().out)
    assert readback["review_notes"][0]["artifact_ref"] == recorded["artifact_ref"]

    observed = []

    def fixture_executor(request: dict, *, timeout_seconds: float) -> dict:
        observed.append(request)
        receipt = _codex_receipt(_closeout_packet(CRITIQUE_PACKET_PATH))
        receipt["cwd"] = request["cwd"]
        return receipt

    def critique_with_fixture(**kwargs):
        return build_critique_execution_document(**kwargs, executor_runner=fixture_executor)

    output = workspace / "reviewed-workspace.json"
    with patch("med_autogrant.domain_runtime_parts.handoff_surfaces.build_critique_execution_document",
               side_effect=critique_with_fixture):
        assert main(["pass", "critique", "--input", str(source), "--output", str(output), "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    persisted = json.loads(output.read_text())
    assert len(observed) == 1
    assert value["note"] in observed[0]["prompt"]
    assert recorded["artifact_ref"] in observed[0]["prompt"]
    assert observed[0]["domain_payload"]["input_path"] == str(source)
    for field in ("grant_run_id", "workspace_id"):
        assert result[field] == persisted[field] == original[field]
    assert result["draft_id"] == original["current_selection"]["active_draft_id"]
    assert result["critique_execution"]["critique_id"] == persisted["mentor_critiques"][-1]["critique_id"]
    assert persisted["current_selection"]["active_revision_plan_id"] == result["critique_execution"]["active_revision_plan_id"]
    assert len(persisted["mentor_critiques"]) == len(original.get("mentor_critiques", [])) + 1
    assert persisted["gates"]["presubmission_frozen"] is False
    assert json.loads(source.read_text()) == original
