from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class CodexCliContractTest(unittest.TestCase):
    def test_read_codex_cli_contract_inherits_local_codex_defaults_when_not_overridden(self) -> None:
        from med_autogrant.codex_cli import (
            DEFAULT_CODEX_MODEL,
            DEFAULT_CODEX_REASONING_EFFORT,
            read_codex_cli_contract,
        )

        contract = read_codex_cli_contract({})

        self.assertEqual(contract["command"], ("codex",))
        self.assertIsNone(contract["model"])
        self.assertIsNone(contract["reasoning_effort"])
        self.assertEqual(contract["model_selection"], DEFAULT_CODEX_MODEL)
        self.assertEqual(
            contract["reasoning_selection"],
            DEFAULT_CODEX_REASONING_EFFORT,
        )
        self.assertEqual(contract["sandbox"], "read-only")

    def test_read_codex_cli_contract_keeps_explicit_env_overrides(self) -> None:
        from med_autogrant.codex_cli import read_codex_cli_contract

        contract = read_codex_cli_contract(
            {
                "MED_AUTOGRANT_CODEX_COMMAND": '["/opt/codex","--profile","lab"]',
                "MED_AUTOGRANT_CODEX_MODEL": "gpt-5.4",
                "MED_AUTOGRANT_CODEX_REASONING_EFFORT": "xhigh",
                "MED_AUTOGRANT_CODEX_SANDBOX": "workspace-write",
            }
        )

        self.assertEqual(contract["command"], ("/opt/codex", "--profile", "lab"))
        self.assertEqual(contract["model"], "gpt-5.4")
        self.assertEqual(contract["reasoning_effort"], "xhigh")
        self.assertEqual(contract["model_selection"], "gpt-5.4")
        self.assertEqual(contract["reasoning_selection"], "xhigh")
        self.assertEqual(contract["sandbox"], "workspace-write")


class CodexCliExecCommandTest(unittest.TestCase):
    def test_run_codex_exec_omits_model_and_reasoning_flags_when_inheriting_local_defaults(self) -> None:
        from med_autogrant.codex_cli import run_codex_exec

        recorded: dict[str, object] = {}

        def fake_run(args, **kwargs):
            recorded["args"] = list(args)
            output_path = Path(args[args.index("--output-last-message") + 1])
            output_path.write_text(
                json.dumps({"mentor_critique": {}, "revision_plan": {}}),
                encoding="utf-8",
            )

            class Result:
                returncode = 0
                stdout = ""
                stderr = ""

            return Result()

        with tempfile.TemporaryDirectory() as tmp_dir, patch(
            "med_autogrant.codex_cli.subprocess.run",
            side_effect=fake_run,
        ):
            payload = run_codex_exec("{}", cwd=tmp_dir, env={})

        self.assertEqual(payload, {"mentor_critique": {}, "revision_plan": {}})
        args = recorded["args"]
        self.assertIn("exec", args)
        self.assertNotIn("--model", args)
        self.assertNotIn('model_reasoning_effort="xhigh"', args)

    def test_run_codex_exec_includes_model_and_reasoning_overrides_when_explicitly_configured(self) -> None:
        from med_autogrant.codex_cli import run_codex_exec

        recorded: dict[str, object] = {}

        def fake_run(args, **kwargs):
            recorded["args"] = list(args)
            output_path = Path(args[args.index("--output-last-message") + 1])
            output_path.write_text(
                json.dumps({"mentor_critique": {}, "revision_plan": {}}),
                encoding="utf-8",
            )

            class Result:
                returncode = 0
                stdout = ""
                stderr = ""

            return Result()

        with tempfile.TemporaryDirectory() as tmp_dir, patch(
            "med_autogrant.codex_cli.subprocess.run",
            side_effect=fake_run,
        ):
            payload = run_codex_exec(
                "{}",
                cwd=tmp_dir,
                env={
                    "MED_AUTOGRANT_CODEX_MODEL": "gpt-5.4",
                    "MED_AUTOGRANT_CODEX_REASONING_EFFORT": "xhigh",
                },
            )

        self.assertEqual(payload, {"mentor_critique": {}, "revision_plan": {}})
        args = recorded["args"]
        self.assertEqual(args[args.index("--model") + 1], "gpt-5.4")
        self.assertIn('model_reasoning_effort="xhigh"', args)
