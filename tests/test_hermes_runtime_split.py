from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class HermesRuntimeSplitStructureTest(unittest.TestCase):
    def test_source_modules_do_not_use_star_imports(self) -> None:
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in sorted((SRC_ROOT / "med_autogrant").rglob("*.py"))
            if "import *" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_runtime_substrate_lives_below_runtime_parts(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        self.assertEqual(
            "med_autogrant.hermes_runtime_parts.substrate",
            HermesRuntimeSubstrate.__module__,
        )

    def test_facade_re_exports_split_runtime_helpers(self) -> None:
        from med_autogrant import hermes_runtime
        from med_autogrant.hermes_runtime_parts import runtime_ops

        self.assertIs(
            hermes_runtime._build_autonomy_quality_evaluator_output,
            runtime_ops.build_autonomy_quality_evaluator_output,
        )

    def test_runtime_facade_keeps_handoff_monkeypatch_targets(self) -> None:
        from med_autogrant import hermes_runtime
        from med_autogrant.hermes_runtime_parts import handoff_surfaces

        self.assertIs(
            hermes_runtime.build_artifact_bundle_document,
            handoff_surfaces.build_artifact_bundle_document,
        )
        self.assertIs(
            hermes_runtime._guard_critique_output_identity,
            handoff_surfaces._guard_critique_output_identity,
        )

    def test_runtime_substrate_does_not_directly_import_handoff_owners(self) -> None:
        substrate_path = SRC_ROOT / "med_autogrant" / "hermes_runtime_parts" / "substrate.py"
        tree = ast.parse(substrate_path.read_text(encoding="utf-8"))
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and isinstance(node.module, str)
        }

        self.assertFalse(
            {
                "med_autogrant.authoring_executor",
                "med_autogrant.artifact_bundle",
                "med_autogrant.critique_executor",
                "med_autogrant.revision_executor",
            }
            & imported_modules
        )

    def test_domain_entry_does_not_import_runtime_facade(self) -> None:
        domain_entry_text = (SRC_ROOT / "med_autogrant" / "domain_entry.py").read_text(encoding="utf-8")

        self.assertNotIn("from med_autogrant.hermes_runtime import", domain_entry_text)
        self.assertNotIn("from med_autogrant import hermes_runtime", domain_entry_text)

    def test_control_plane_does_not_import_workspace_facade(self) -> None:
        control_plane_text = (SRC_ROOT / "med_autogrant" / "control_plane.py").read_text(encoding="utf-8")

        self.assertNotIn("from med_autogrant.workspace import", control_plane_text)

    def test_runtime_parts_do_not_import_runtime_facade(self) -> None:
        runtime_parts = sorted((SRC_ROOT / "med_autogrant" / "hermes_runtime_parts").glob("*.py"))
        forbidden_fragments = (
            "from med_autogrant.hermes_runtime import",
            "from med_autogrant import hermes_runtime",
        )
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in runtime_parts
            if any(fragment in path.read_text(encoding="utf-8") for fragment in forbidden_fragments)
        ]

        self.assertEqual([], offenders)

    def test_package_builders_do_not_import_runtime_facade(self) -> None:
        package_builders = [
            SRC_ROOT / "med_autogrant" / "artifact_bundle.py",
            SRC_ROOT / "med_autogrant" / "final_package.py",
            SRC_ROOT / "med_autogrant" / "hosted_contract_bundle.py",
            SRC_ROOT / "med_autogrant" / "revision_executor.py",
        ]

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in package_builders
            if "med_autogrant.hermes_runtime import" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_workspace_parts_do_not_import_workspace_facade(self) -> None:
        workspace_parts = [
            SRC_ROOT / "med_autogrant" / "workspace_parts.py",
            SRC_ROOT / "med_autogrant" / "workspace_projection_parts.py",
        ]

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in workspace_parts
            if "med_autogrant.workspace import" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
