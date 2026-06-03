from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / 'src'
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from support.cli import run_cli  # noqa: E402


OUTLINE_EXAMPLE_PATH = REPO_ROOT / 'examples' / 'nsfc_workspace_p2b_outline.json'
REVISION_EXAMPLE_PATH = REPO_ROOT / 'examples' / 'nsfc_workspace_p2c_revision.json'
RE_REVIEW_MAJOR_REVISION_EXAMPLE_PATH = REPO_ROOT / 'examples' / 'nsfc_workspace_p3b_re_review_major_revision.json'


def _assert_stage_output_projection(
    test_case: unittest.TestCase,
    *,
    bundle: dict[str, object],
    stage_id: str,
    stage_output_role: str,
) -> None:
    projection = bundle['stage_output_projection']
    test_case.assertIsInstance(projection, dict)
    test_case.assertEqual(projection['surface_kind'], 'mag_stage_output_projection')
    test_case.assertEqual(projection['owner'], 'med-autogrant')
    test_case.assertEqual(projection['stage_id'], stage_id)
    test_case.assertEqual(projection['stage_output_role'], stage_output_role)
    test_case.assertEqual(projection['artifact_classification'], 'grant_stage_output_ref')
    test_case.assertEqual(bundle['manifest']['stage_id'], stage_id)
    test_case.assertEqual(bundle['manifest']['stage_output_role'], stage_output_role)
    test_case.assertEqual(bundle['manifest']['artifact_classification'], 'grant_stage_output_ref')
    test_case.assertEqual(bundle['manifest']['manifest_ref'], projection['manifest_ref'])
    test_case.assertEqual(bundle['manifest']['current_pointer_ref'], projection['current_pointer_ref'])
    test_case.assertEqual(
        bundle['manifest']['owner_receipt_or_typed_blocker_ref'],
        projection['owner_receipt_or_typed_blocker_ref'],
    )
    test_case.assertEqual(projection['current_pointer_ref'], f'current:mag/stages/{stage_id}/{stage_output_role}')
    test_case.assertEqual(
        projection['owner_receipt_or_typed_blocker_ref'],
        f'receipt:mag/grant-stage-controlled-attempt/{stage_id}/owner-receipt-or-typed-blocker',
    )
    opl_consumption = projection['opl_consumption']
    test_case.assertEqual(opl_consumption['role'], 'refs_manifest_receipt_only')
    test_case.assertFalse(opl_consumption['can_read_artifact_body'])
    test_case.assertFalse(opl_consumption['can_write_grant_truth'])
    test_case.assertFalse(opl_consumption['can_infer_fundability'])
    test_case.assertFalse(opl_consumption['can_infer_quality'])
    test_case.assertFalse(opl_consumption['can_infer_export'])
    test_case.assertFalse(opl_consumption['can_infer_submission_ready'])


class ArtifactBundleCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        return run_cli(*args)

    def test_build_artifact_bundle_writes_outline_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / 'outline-bundle.json'

            exit_code, stdout, stderr = self.run_cli(
                'package',
                'artifact-bundle',
                '--input',
                str(OUTLINE_EXAMPLE_PATH),
                '--output',
                str(bundle_path),
                '--format',
                'json',
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, '')
            payload = json.loads(stdout)
            self.assertTrue(payload['ok'])
            self.assertEqual(payload['command'], 'build-artifact-bundle')
            self.assertEqual(payload['grant_run_id'], 'grant-run-nsfc-demo-001-baseline-001')
            self.assertEqual(payload['workspace_id'], 'nsfc-demo-001')
            self.assertEqual(payload['draft_id'], 'draft-outline-v1')
            self.assertEqual(payload['lifecycle_stage'], 'outline')
            self.assertEqual(payload['output_path'], str(bundle_path.resolve()))
            bundle = payload['bundle']
            self.assertEqual(bundle['bundle_version'], 1)
            self.assertEqual(bundle['bundle_kind'], 'artifact_bundle')
            self.assertNotIn('program_id', bundle)
            self.assertNotIn('verification_checkpoint', bundle)
            self.assertEqual(bundle['selection'], {
                'selected_direction_id': 'dir-inflammatory-remodeling',
                'selected_question_id': 'question-immune-fibrosis',
                'active_fit_mapping_id': 'fit-001',
                'active_draft_id': 'draft-outline-v1',
            })
            self.assertEqual(bundle['manifest']['direction_id'], 'dir-inflammatory-remodeling')
            self.assertEqual(bundle['manifest']['question_id'], 'question-immune-fibrosis')
            self.assertEqual(bundle['manifest']['argument_chain_id'], 'arg-001')
            self.assertEqual(bundle['manifest']['fit_mapping_id'], 'fit-001')
            self.assertEqual(bundle['manifest']['draft_id'], 'draft-outline-v1')
            self.assertEqual(bundle['manifest']['draft_version_label'], 'outline-v1')
            self.assertEqual(bundle['manifest']['draft_status'], 'outline')
            _assert_stage_output_projection(
                self,
                bundle=bundle,
                stage_id='specific_aims_and_structure',
                stage_output_role='specific_aims_structure_manifest_ref',
            )
            self.assertEqual(bundle['lineage'], {
                'frozen_question_id': 'question-immune-fibrosis',
                'argument_chain_id': 'arg-001',
                'fit_mapping_id': 'fit-001',
                'draft_id': 'draft-outline-v1',
            })
            self.assertEqual(bundle['bundle_summary'], {'outline_count': 2, 'section_count': 0})
            self.assertEqual(bundle['artifacts']['selected_direction']['direction_id'], 'dir-inflammatory-remodeling')
            self.assertEqual(bundle['artifacts']['selected_question']['question_id'], 'question-immune-fibrosis')
            self.assertEqual(bundle['artifacts']['argument_chain']['argument_chain_id'], 'arg-001')
            self.assertEqual(bundle['artifacts']['fit_mapping']['fit_mapping_id'], 'fit-001')
            self.assertEqual(len(bundle['artifacts']['draft_outline']), 2)
            self.assertEqual(bundle['artifacts']['draft_sections'], [])
            self.assertTrue(bundle_path.exists())
            self.assertEqual(json.loads(bundle_path.read_text(encoding='utf-8')), bundle)

    def test_build_artifact_bundle_writes_revision_bundle_with_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / 'revision-bundle.json'

            exit_code, stdout, stderr = self.run_cli(
                'package',
                'artifact-bundle',
                '--input',
                str(REVISION_EXAMPLE_PATH),
                '--output',
                str(bundle_path),
                '--format',
                'json',
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, '')
            payload = json.loads(stdout)
            bundle = payload['bundle']
            self.assertEqual(bundle['draft_id'], 'draft-v1')
            self.assertEqual(bundle['lifecycle_stage'], 'revision')
            self.assertEqual(bundle['manifest']['draft_version_label'], 'v0.4')
            self.assertEqual(bundle['manifest']['draft_status'], 'revised')
            _assert_stage_output_projection(
                self,
                bundle=bundle,
                stage_id='proposal_authoring',
                stage_output_role='reviewable_grant_artifact_bundle_ref',
            )
            self.assertEqual(bundle['lineage']['frozen_question_id'], 'question-immune-fibrosis')
            self.assertEqual(bundle['bundle_summary'], {'outline_count': 2, 'section_count': 3})
            self.assertNotIn('program_id', bundle)
            self.assertNotIn('checkpoint_status', bundle)
            self.assertEqual(len(bundle['artifacts']['draft_sections']), 3)
            self.assertEqual(bundle['artifacts']['draft_sections'][0]['section_key'], 'basis')
            self.assertIn('炎症巨噬细胞', bundle['artifacts']['draft_sections'][0]['text'])

    def test_build_artifact_bundle_accepts_re_review_revised_output_after_execute_revision_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / 'p3b-revised.json'
            bundle_path = Path(tmp_dir) / 'p3b-revised-bundle.json'

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                'pass',
                'revision',
                '--input',
                str(RE_REVIEW_MAJOR_REVISION_EXAMPLE_PATH),
                '--output',
                str(revised_output),
                '--format',
                'json',
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, '')
            self.assertTrue(json.loads(execute_stdout)['ok'])

            exit_code, stdout, stderr = self.run_cli(
                'package',
                'artifact-bundle',
                '--input',
                str(revised_output),
                '--output',
                str(bundle_path),
                '--format',
                'json',
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, '')
            payload = json.loads(stdout)
            self.assertTrue(payload['ok'])
            bundle = payload['bundle']
            self.assertEqual(bundle['lifecycle_stage'], 'critique')
            self.assertEqual(bundle['manifest']['draft_version_label'], 'v0.5')
            self.assertEqual(bundle['manifest']['draft_status'], 'revised')
            _assert_stage_output_projection(
                self,
                bundle=bundle,
                stage_id='review_and_rebuttal',
                stage_output_role='review_quality_closure_receipt_ref',
            )
            self.assertEqual(bundle['lineage']['draft_id'], 'draft-v1')
            self.assertEqual(len(bundle['artifacts']['draft_sections']), 3)
            self.assertTrue(bundle_path.exists())

    def test_build_artifact_bundle_fails_closed_when_existing_output_has_mismatched_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / 'conflict-bundle.json'
            bundle_path.write_text(
                json.dumps(
                    {
                        'grant_run_id': 'grant-run-other',
                        'workspace_id': 'workspace-other',
                        'draft_id': 'draft-other',
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding='utf-8',
            )

            exit_code, stdout, stderr = self.run_cli(
                'package',
                'artifact-bundle',
                '--input',
                str(REVISION_EXAMPLE_PATH),
                '--output',
                str(bundle_path),
                '--format',
                'json',
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, '')
            payload = json.loads(stdout)
            self.assertFalse(payload['ok'])
            self.assertEqual(payload['command'], 'build-artifact-bundle')
            self.assertIn('bundle output identity 不匹配', payload['error'])
            self.assertEqual(json.loads(bundle_path.read_text(encoding='utf-8'))['grant_run_id'], 'grant-run-other')


if __name__ == '__main__':
    unittest.main()
