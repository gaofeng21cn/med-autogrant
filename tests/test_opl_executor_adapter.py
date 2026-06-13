from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import med_autogrant.opl_hermes_executor_helper as hermes_helper


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

    def test_opl_hermes_executor_helper_accepts_opl_owned_critique_receipt(self) -> None:
        result = {
            "agent_execution_receipt": {
                "receipt_owner": "one-person-lab",
                "mag_executor_owner": False,
                "executor_kind": "hermes_agent",
            },
            "contract": {"adapter": "hermes_agent"},
            "payload": {
                "mentor_critique": {"verdict": "major_revision"},
                "revision_plan": {"plan_id": "revision-plan"},
            },
        }

        with tempfile.TemporaryDirectory() as tmp_dir, patch.object(
            hermes_helper,
            "run_hermes_agent_exec",
            return_value=result,
        ) as run_hermes:
            receipt = hermes_helper.run_mag_hermes_executor_request(
                {
                    "executor_kind": "hermes_agent",
                    "prompt": "critique prompt",
                    "cwd": tmp_dir,
                    "domain_payload": {"route_id": "critique"},
                }
            )

        run_hermes.assert_called_once_with("critique prompt", cwd=Path(tmp_dir).resolve())
        self.assertEqual(receipt["executor_contract"], {"adapter": "hermes_agent"})
        self.assertEqual(receipt["closeout_packet"]["surface_kind"], "mag_critique_closeout_packet")
        self.assertEqual(
            receipt["closeout_packet"]["mentor_critique"],
            {"verdict": "major_revision"},
        )


if __name__ == "__main__":
    unittest.main()
