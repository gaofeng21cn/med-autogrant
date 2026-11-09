from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
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
