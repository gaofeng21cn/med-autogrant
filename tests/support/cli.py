from __future__ import annotations

import json
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import Any

from med_autogrant.cli import main


def public_cli_argv(argv: list[str] | tuple[str, ...]) -> list[str]:
    return list(argv)


def run_cli(*args: str, allow_system_exit: bool = True) -> tuple[int, str, str]:
    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            exit_code = main(public_cli_argv(args))
        except SystemExit as exc:
            if not allow_system_exit:
                raise
            exit_code = int(exc.code)
    return exit_code, stdout.getvalue(), stderr.getvalue()


def run_json_cli(*args: str, allow_system_exit: bool = True) -> dict[str, Any]:
    exit_code, stdout, stderr = run_cli(*args, allow_system_exit=allow_system_exit)
    assert exit_code == 0
    assert stderr == ""
    return json.loads(stdout)
