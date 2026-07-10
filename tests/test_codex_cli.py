from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


from med_autogrant.codex_cli import read_codex_cli_contract, run_codex_exec  # noqa: E402


class CodexCliTest(unittest.TestCase):
    def test_contract_defaults_and_overrides(self) -> None:
        cases = (
            ({}, ("codex",), None, None, "read-only"),
            (
                {
                    "MED_AUTOGRANT_CODEX_COMMAND": '["/opt/codex","--profile","lab"]',
                    "MED_AUTOGRANT_CODEX_MODEL": "gpt-5.4",
                    "MED_AUTOGRANT_CODEX_REASONING_EFFORT": "xhigh",
                    "MED_AUTOGRANT_CODEX_SANDBOX": "workspace-write",
                },
                ("/opt/codex", "--profile", "lab"),
                "gpt-5.4",
                "xhigh",
                "workspace-write",
            ),
        )
        for env, command, model, effort, sandbox in cases:
            with self.subTest(overridden=bool(env)):
                contract = read_codex_cli_contract(env)
                self.assertEqual(contract["command"], command)
                self.assertEqual(contract["model"], model)
                self.assertEqual(contract["reasoning_effort"], effort)
                self.assertEqual(contract["model_selection"], model or "inherit_local_codex_default")
                self.assertEqual(contract["reasoning_selection"], effort or "inherit_local_codex_default")
                self.assertEqual(contract["sandbox"], sandbox)

    def test_exec_argv_defaults_and_overrides(self) -> None:
        cases = (
            ({}, None, None),
            (
                {
                    "MED_AUTOGRANT_CODEX_MODEL": "gpt-5.4",
                    "MED_AUTOGRANT_CODEX_REASONING_EFFORT": "xhigh",
                },
                "gpt-5.4",
                'model_reasoning_effort="xhigh"',
            ),
        )
        for env, model, effort_flag in cases:
            recorded: list[str] = []

            def fake_run(args, **_kwargs):
                recorded.extend(args)
                Path(args[args.index("--output-last-message") + 1]).write_text(
                    json.dumps({"mentor_critique": {}, "revision_plan": {}}),
                    encoding="utf-8",
                )
                return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

            with self.subTest(overridden=bool(env)), tempfile.TemporaryDirectory() as tmp_dir, patch(
                "med_autogrant.codex_cli.subprocess.run", side_effect=fake_run
            ):
                run_codex_exec("{}", cwd=tmp_dir, env=env)

            self.assertEqual("--model" in recorded, model is not None)
            if model is not None:
                self.assertEqual(recorded[recorded.index("--model") + 1], model)
                self.assertIn(effort_flag, recorded)
            else:
                self.assertFalse(any(arg.startswith("model_reasoning_effort=") for arg in recorded))
