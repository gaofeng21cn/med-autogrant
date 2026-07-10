from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]
from support.cli import run_cli  # noqa: E402


EXAMPLES = REPO_ROOT / "examples"
NSFC_INPUT = EXAMPLES / "profile_selection_input_nsfc_general.json"


class ProjectProfileSelectionCliTest(unittest.TestCase):
    def json_cli(self, *args: str) -> dict[str, object]:
        exit_code, stdout, stderr = run_cli(*args, allow_system_exit=False)
        self.assertEqual((exit_code, stderr), (0, ""))
        return json.loads(stdout)

    def test_select_profile_covers_three_funders(self) -> None:
        cases = (
            ("profile_selection_input_nsfc_general.json", "nsfc_general_medical_v1", "nsfc-2026-general"),
            ("profile_selection_input_nih_r21.json", "nih_r21_translational_v1", "nih-r21-2026-nhlbi"),
            ("profile_selection_input_wellcome_discovery.json", "wellcome_discovery_v1", "wellcome-discovery-2026"),
        )
        for filename, preset_id, brief_id in cases:
            with self.subTest(funder=filename):
                payload = self.json_cli(
                    "workspace", "select-profile", "--input", str(EXAMPLES / filename), "--format", "json"
                )["project_profile_selection"]
                self.assertEqual(payload["recommended_project_profile"]["preset_id"], preset_id)
                self.assertEqual(payload["recommended_funding_opportunity"]["brief_id"], brief_id)
                self.assertEqual(payload["selection_summary"]["evaluated_profile_preset_count"], 3)

    def test_initialize_intake_materializes_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "workspace.json"
            payload = self.json_cli(
                "workspace", "initialize-intake", "--input", str(NSFC_INPUT),
                "--output", str(output_path), "--format", "json",
            )

            self.assertTrue(output_path.is_file())
            self.assertEqual(payload["initialized_workspace"]["lifecycle_stage"], "input_intake")
            self.assertEqual(payload["initialized_workspace"]["project_profile"]["preset_id"], "nsfc_general_medical_v1")

    def test_initialize_intake_directory_git_and_no_git_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            for no_git in (False, True):
                with self.subTest(no_git=no_git):
                    workspace_root = Path(tmp_dir) / ("without-git" if no_git else "with-git")
                    argv = [
                        "workspace", "initialize-intake", "--input", str(NSFC_INPUT),
                        "--workspace-root", str(workspace_root),
                    ]
                    if no_git:
                        argv.append("--no-git")
                    argv.extend(("--format", "json"))
                    payload = self.json_cli(*argv)

                    self.assertTrue((workspace_root / "workspace.json").is_file())
                    self.assertEqual((workspace_root / ".git").exists(), not no_git)
                    self.assertEqual(payload["workspace_git"]["enabled"], not no_git)
                    if not no_git:
                        runtime_probe = workspace_root / "runtime" / "probe.json"
                        runtime_probe.parent.mkdir(parents=True, exist_ok=True)
                        runtime_probe.write_text("{}", encoding="utf-8")
                        ignored = subprocess.run(
                            ["git", "check-ignore", str(runtime_probe.relative_to(workspace_root))],
                            cwd=workspace_root,
                            capture_output=True,
                            text=True,
                        )
                        self.assertEqual(ignored.returncode, 0)
                        validated = self.json_cli(
                            "workspace", "validate", "--input", str(workspace_root), "--format", "json"
                        )
                        self.assertTrue(validated["ok"])
