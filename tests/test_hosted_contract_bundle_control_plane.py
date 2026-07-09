from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant import hosted_contract_bundle as hosted_contract_bundle_module  # noqa: E402


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
