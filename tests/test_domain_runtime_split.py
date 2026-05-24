from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

class RuntimeSplitStructureTest(unittest.TestCase):
    def test_source_modules_do_not_use_star_imports(self) -> None:
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in sorted((SRC_ROOT / "med_autogrant").rglob("*.py"))
            if "import *" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_mag_domain_runtime_is_domain_adapter_not_generic_runtime_owner(self) -> None:
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime

        topology = MagDomainRuntime().describe_topology()

        self.assertEqual(topology["runtime_owner"], "one-person-lab")
        self.assertEqual(topology["runtime_surface_role"], "repo_side_domain_adapter_and_regression_oracle")
        self.assertEqual(topology["domain_surface_owner"], "Med Auto Grant")
        self.assertFalse(topology["can_claim_generic_runtime_owner"])
        self.assertEqual(topology["authoring_truth_owner"], "Med Auto Grant")
        self.assertEqual(topology["quality_gate_owner"], "Med Auto Grant")
        self.assertEqual(topology["export_authority"], "Med Auto Grant")
        self.assertEqual(topology["default_stage_attempt_executor"], "Codex CLI")
        self.assertEqual(topology["optional_proof_executor"], "Hermes-Agent")
        self.assertEqual(topology["optional_proof_executor_boundary"], "explicit opt-in only")

    def test_package_surface_owns_export_methods_under_authoring_mixin(self) -> None:
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime
        from med_autogrant.domain_runtime_parts.authoring_surface import DomainRuntimeAuthoringSurfaceMixin
        from med_autogrant.domain_runtime_parts.package_surface import DomainRuntimePackageSurfaceMixin

        self.assertTrue(issubclass(DomainRuntimeAuthoringSurfaceMixin, DomainRuntimePackageSurfaceMixin))
        self.assertEqual(
            "med_autogrant.domain_runtime_parts.package_surface",
            MagDomainRuntime.build_final_package.__module__,
        )
        self.assertEqual(
            "med_autogrant.domain_runtime_parts.package_surface",
            MagDomainRuntime.build_hosted_contract_bundle.__module__,
        )
        self.assertEqual(
            "med_autogrant.domain_runtime_parts.package_surface",
            MagDomainRuntime.build_submission_ready_package.__module__,
        )

    def test_runtime_substrate_does_not_directly_import_handoff_owners(self) -> None:
        substrate_path = SRC_ROOT / "med_autogrant" / "domain_runtime_parts" / "substrate.py"
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

        self.assertNotIn("from med_autogrant.domain_runtime import", domain_entry_text)

    def test_retired_runtime_facade_is_not_present_in_source(self) -> None:
        self.assertFalse((SRC_ROOT / "med_autogrant" / "domain_runtime.py").exists())

    def test_control_plane_does_not_import_workspace_facade(self) -> None:
        control_plane_text = (SRC_ROOT / "med_autogrant" / "control_plane.py").read_text(encoding="utf-8")

        self.assertNotIn("from med_autogrant.workspace import", control_plane_text)

    def test_runtime_parts_do_not_import_runtime_facade(self) -> None:
        runtime_parts = sorted((SRC_ROOT / "med_autogrant" / "domain_runtime_parts").glob("*.py"))
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in runtime_parts
            if "from med_autogrant.domain_runtime import" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_package_surface_does_not_import_runtime_facade(self) -> None:
        package_surface_text = (
            SRC_ROOT / "med_autogrant" / "domain_runtime_parts" / "package_surface.py"
        ).read_text(encoding="utf-8")

        self.assertIn("class DomainRuntimePackageSurfaceMixin", package_surface_text)
        self.assertNotIn("from med_autogrant.domain_runtime import", package_surface_text)

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
            if "med_autogrant.domain_runtime import" in path.read_text(encoding="utf-8")
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

    def test_workspace_facade_is_the_only_workspace_facade_import_boundary(self) -> None:
        offenders: list[str] = []
        for path in sorted((SRC_ROOT / "med_autogrant").rglob("*.py")):
            if path.name == "workspace.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or node.module != "med_autogrant.workspace":
                    continue
                imported_names = {alias.name for alias in node.names}
                if "*" in imported_names:
                    relative_path = path.relative_to(REPO_ROOT).as_posix()
                    offenders.append(relative_path)

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
