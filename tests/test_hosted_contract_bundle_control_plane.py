from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.domain_entry_contract import build_domain_entry_contract  # noqa: E402
from med_autogrant.public_cli import public_cli_argv, public_command_label  # noqa: E402
from med_autogrant import hosted_contract_bundle as hosted_contract_bundle_module  # noqa: E402


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"
AUTHOR_SIDE_ROUTE_IDS = (
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
    "artifact_bundle",
    "final_package",
    "hosted_contract_bundle",
)
SUPPORTED_DOMAIN_ENTRY_COMMANDS = [
    "probe-upstream-hermes",
    "validate-workspace",
    "summarize-workspace",
    "grant-intake-audit",
    "grant-evidence-grounding",
    "grant-quality-scorecard",
    "grant-quality-diff",
    "grant-quality-closure-dossier",
    "discover-funding-opportunities",
    "refresh-funding-opportunities-cache",
    "select-project-profile",
    "initialize-intake-workspace",
    "next-step",
    "critique-summary",
    "stage-route-report",
    "runtime-run",
    "runtime-resume",
    "execute-direction-screening-pass",
    "execute-question-refinement-pass",
    "execute-argument-building-pass",
    "execute-fit-alignment-pass",
    "execute-outline-pass",
    "execute-drafting-pass",
    "build-artifact-bundle",
    "execute-critique-pass",
    "execute-critique-revision-loop",
    "execute-authoring-mainline-loop",
    "execute-grant-autonomy-controller",
    "execute-revision-pass",
    "execute-freeze-pass",
    "build-final-package",
    "build-hosted-contract-bundle",
    "build-submission-ready-package",
]
DOMAIN_ENTRY_COMMAND_CONTRACTS = [
    {"command": "probe-upstream-hermes", "required_fields": [], "optional_fields": []},
    {"command": "validate-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "summarize-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-intake-audit", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-evidence-grounding", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-quality-scorecard", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-quality-closure-dossier", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "grant-quality-diff",
        "required_fields": ["input_path", "previous_input_path"],
        "optional_fields": [],
    },
    {"command": "discover-funding-opportunities", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "refresh-funding-opportunities-cache",
        "required_fields": ["input_path"],
        "optional_fields": ["output_path"],
    },
    {"command": "select-project-profile", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "initialize-intake-workspace",
        "required_fields": ["input_path"],
        "optional_fields": ["output_path", "workspace_root", "initialize_git"],
    },
    {"command": "next-step", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "critique-summary", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "stage-route-report", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "runtime-run", "required_fields": ["input_path"], "optional_fields": ["journal_path"]},
    {"command": "runtime-resume", "required_fields": ["journal_path"], "optional_fields": []},
    {"command": "execute-direction-screening-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-question-refinement-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-argument-building-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-fit-alignment-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-outline-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-drafting-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "build-artifact-bundle", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {
        "command": "execute-critique-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": ["executor_kind"],
    },
    {
        "command": "execute-critique-revision-loop",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["max_rounds", "executor_kind"],
    },
    {
        "command": "execute-authoring-mainline-loop",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["max_cycles", "executor_kind"],
    },
    {
        "command": "execute-grant-autonomy-controller",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["executor_kind"],
    },
    {"command": "execute-revision-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {"command": "execute-freeze-pass", "required_fields": ["input_path", "output_path"], "optional_fields": []},
    {
        "command": "build-final-package",
        "required_fields": ["input_path", "artifact_bundle_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-hosted-contract-bundle",
        "required_fields": ["final_package_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-submission-ready-package",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": [],
    },
]
CANONICAL_EXPORT_SURFACES = [
    "execute-direction-screening-pass",
    "execute-question-refinement-pass",
    "execute-argument-building-pass",
    "execute-fit-alignment-pass",
    "execute-outline-pass",
    "execute-drafting-pass",
    "execute-critique-pass",
    "execute-revision-pass",
    "execute-freeze-pass",
    "build-artifact-bundle",
    "build-final-package",
    "build-hosted-contract-bundle",
    "build-submission-ready-package",
]

PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND = public_command_label("build-product-entry")



class HostedContractBundleControlPlaneResolutionTest(unittest.TestCase):
    def test_resolve_control_plane_current_program_path_prefers_repo_tracked_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo-root"
            current_program_path = repo_root / "contracts" / "runtime-program" / "current-program.json"
            current_program_path.parent.mkdir(parents=True, exist_ok=True)
            current_program_path.write_text(
                json.dumps({"program_id": "local-program"}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            resolved_path = hosted_contract_bundle_module._resolve_control_plane_current_program_path(
                repo_root=repo_root,
            )

            self.assertEqual(resolved_path, current_program_path.resolve())

    def test_resolve_control_plane_current_program_path_ignores_worktree_list_once_contract_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            feature_worktree = Path(tmp_dir) / "feature-worktree"
            feature_worktree.mkdir(parents=True, exist_ok=True)
            current_program_path = feature_worktree / "contracts" / "runtime-program" / "current-program.json"
            current_program_path.parent.mkdir(parents=True, exist_ok=True)
            current_program_path.write_text(
                json.dumps({"program_id": "feature-program"}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            worktree_list_text = "\n".join(
                (
                    f"worktree {feature_worktree}",
                    "HEAD 1111111111111111111111111111111111111111",
                    "branch refs/heads/post-r5a-local-runtime-hardening-20260410-a",
                )
            )

            resolved_path = hosted_contract_bundle_module._resolve_control_plane_current_program_path(
                repo_root=feature_worktree,
                worktree_list_text=worktree_list_text,
            )

            self.assertEqual(resolved_path, current_program_path.resolve())

    def test_resolve_control_plane_current_program_path_fails_closed_without_repo_tracked_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            feature_worktree = Path(tmp_dir) / "feature-worktree"
            feature_worktree.mkdir(parents=True, exist_ok=True)
            with self.assertRaisesRegex(
                hosted_contract_bundle_module.WorkspaceFileError,
                "repo-tracked CURRENT_PROGRAM contract",
            ):
                hosted_contract_bundle_module._resolve_control_plane_current_program_path(
                    repo_root=feature_worktree,
                )

    def test_read_program_id_fails_closed_for_missing_program_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo-root"
            current_program_path = repo_root / "contracts" / "runtime-program" / "current-program.json"
            current_program_path.parent.mkdir(parents=True, exist_ok=True)
            current_program_path.write_text(json.dumps({}, ensure_ascii=False, indent=2), encoding="utf-8")

            with self.assertRaisesRegex(
                hosted_contract_bundle_module.WorkspaceStateError,
                "program_id",
            ):
                hosted_contract_bundle_module._read_program_id(repo_root=repo_root)


if __name__ == "__main__":
    unittest.main()
