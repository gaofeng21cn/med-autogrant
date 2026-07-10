from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
from support.hosted_contract_bundle import (  # noqa: E402
    assert_hosted_contract_bundle_cli_failure,
    build_final_package,
    run_hosted_contract_bundle_cli,
)


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
DELETE = object()


def mutate(document: dict[str, object], path: tuple[str, ...], value: object) -> None:
    target = document
    for key in path[:-1]:
        target = target[key]
    if value is DELETE:
        target.pop(path[-1])
    else:
        target[path[-1]] = value


class HostedContractBundleCheckpointCasesTest(unittest.TestCase):
    def test_all_missing_invalid_and_status_mutations_fail_closed(self) -> None:
        freeze_required = (
            "draft_version_label", "draft_status", "active_revision_plan_id",
            "critique_id", "checkpoint_status", "presubmission_frozen",
        )
        lineage_required = (
            "frozen_question_id", "selected_direction_id", "selected_question_id",
            "active_fit_mapping_id", "draft_id", "revision_plan_id",
        )
        cases: list[tuple[str, tuple[str, ...], object]] = []
        cases.extend((f"missing-freeze-{field}", ("freeze_manifest", field), DELETE) for field in freeze_required)
        cases.extend((f"missing-lineage-{field}", ("lineage", field), DELETE) for field in lineage_required)
        cases.extend(
            (
                ("missing-checkpoint-verification", ("checkpoint_summary", "verification_checkpoint"), DELETE),
                ("missing-checkpoint-status", ("checkpoint_summary", "checkpoint_status"), DELETE),
                ("invalid-freeze-version", ("freeze_manifest", "draft_version_label"), ""),
                ("invalid-freeze-plan", ("freeze_manifest", "active_revision_plan_id"), []),
                ("invalid-freeze-critique", ("freeze_manifest", "critique_id"), ""),
                ("invalid-freeze-flag", ("freeze_manifest", "presubmission_frozen"), "false"),
                ("invalid-draft-status", ("freeze_manifest", "draft_status"), "draft"),
                ("invalid-freeze-status", ("freeze_manifest", "checkpoint_status"), "forward_progress"),
                ("invalid-summary-status", ("checkpoint_summary", "checkpoint_status"), "forward_progress"),
                ("missing-verification-status", ("checkpoint_summary", "verification_checkpoint", "checkpoint_status"), DELETE),
                ("mismatched-verification-status", ("checkpoint_summary", "verification_checkpoint", "checkpoint_status"), "freeze_ready"),
                ("mismatched-freeze-status", ("freeze_manifest", "checkpoint_status"), "freeze_ready"),
            )
        )
        for field in lineage_required:
            cases.append((f"invalid-lineage-{field}", ("lineage", field), [] if field in {"active_fit_mapping_id", "revision_plan_id"} else ""))

        for name, path, value in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp_dir:
                final_path = Path(tmp_dir) / "final.json"
                output_path = Path(tmp_dir) / "hosted.json"
                build_final_package(self, FROZEN_EXAMPLE_PATH, final_path)
                final_package = json.loads(final_path.read_text(encoding="utf-8"))
                mutate(final_package, path, value)
                final_path.write_text(json.dumps(final_package, ensure_ascii=False), encoding="utf-8")

                assert_hosted_contract_bundle_cli_failure(
                    self,
                    run_hosted_contract_bundle_cli(final_path, output_path),
                    output_path,
                )


if __name__ == "__main__":
    unittest.main()
