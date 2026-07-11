from __future__ import annotations

import json
import sys
from functools import partial
from pathlib import Path

from med_autogrant.domain_executor_client import run_domain_executor
from opl_framework.executor_client import run_agent_execution_request


def test_domain_executor_consumes_canonical_opl_receipt(tmp_path: Path) -> None:
    input_path = tmp_path / "workspace.json"
    input_path.write_text("{}\n", encoding="utf-8")
    fake_opl = tmp_path / "fake_opl.py"
    fake_opl.write_text(
        """import json, pathlib, sys
request_path = pathlib.Path(sys.argv[sys.argv.index('--request') + 1])
request = json.loads(request_path.read_text(encoding='utf-8'))
route_id = request['domain_payload']['route_id']
receipt = {
  'surface_kind': 'opl_agent_execution_receipt',
  'executor_kind': request['executor_kind'],
  'mode': request['mode'],
  'session_id': 'codex-domain-client-1',
  'exit_code': 0,
  'non_equivalence_notice': 'codex_cli_first_class_default',
  'proof': {'default_executor': True},
  'closeout_packet': {
    'surface_kind': request['domain_payload']['closeout_surface_kind'],
    'route_id': route_id,
    'domain_output_kind': request['domain_payload']['domain_output_kind'],
    'domain_output': {'result': 'ok'}
  }
}
print(json.dumps({'agent_execution_receipt': receipt}))
""",
        encoding="utf-8",
    )
    runner = partial(
        run_agent_execution_request,
        opl_command=[sys.executable, str(fake_opl)],
    )

    domain_output, executor = run_domain_executor(
        prompt="Return the typed MAG closeout.",
        input_path=input_path,
        executor_kind="codex_cli",
        route_id="direction_screening",
        closeout_surface_kind="domain_stage_closeout_packet",
        domain_output_kind="mag_authoring_output",
        executor_runner=runner,
    )

    assert domain_output == {"result": "ok"}
    assert executor["kind"] == "codex_cli"
    assert executor["adapter_owner"] == "one-person-lab"
    assert executor["session_id"] == "codex-domain-client-1"
