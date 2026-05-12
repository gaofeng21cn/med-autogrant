from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class OplExecutorAdapterTest(unittest.TestCase):
    def test_run_opl_agent_executor_passes_cwd_and_receipt_request_to_opl(self) -> None:
        from med_autogrant.opl_executor_adapter import run_opl_agent_executor

        request = {
            "executor_kind": "hermes_agent",
            "mode": "agent_loop",
            "prompt": "critique prompt",
            "cwd": "/tmp/mag-workspace",
            "json": True,
            "domain_payload": {"domain_id": "med-autogrant", "route_id": "critique"},
        }
        receipt = {
            "surface_kind": "opl_agent_execution_receipt",
            "executor_kind": "hermes_agent",
            "mode": "agent_loop",
        }

        with tempfile.TemporaryDirectory() as tmp_dir, patch(
            "med_autogrant.opl_executor_adapter.subprocess.run"
        ) as run:

            def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
                self.assertEqual(command[:3], ["python3", "-m", "opl_fake"])
                self.assertEqual(command[3:6], ["executor", "run", "--request"])
                request_path = Path(command[6])
                self.assertEqual(json.loads(request_path.read_text(encoding="utf-8")), request)
                self.assertEqual(kwargs["cwd"], Path(tmp_dir).resolve())
                child_env = kwargs["env"]
                self.assertIsInstance(child_env, dict)
                shim = Path(child_env["OPL_HERMES_AGENT_EXECUTOR_BIN"])
                self.assertTrue(shim.exists())
                return SimpleNamespace(
                    returncode=0,
                    stdout=json.dumps({"agent_execution_receipt": receipt}),
                    stderr="",
                )

            run.side_effect = fake_run

            payload = run_opl_agent_executor(
                request,
                cwd=tmp_dir,
                env={"MED_AUTOGRANT_OPL_COMMAND": "python3 -m opl_fake"},
            )

        self.assertEqual(payload, receipt)


if __name__ == "__main__":
    unittest.main()
