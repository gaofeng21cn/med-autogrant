from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

OLD_RUNTIME_TOKEN = "hermes" + "_runtime"
OLD_RUNTIME_IMPORT = f"from med_autogrant import {OLD_RUNTIME_TOKEN}"
OLD_RUNTIME_MODULE_IMPORT = f"from med_autogrant.{OLD_RUNTIME_TOKEN} import"
OLD_RUNTIME_PARTS = f"{OLD_RUNTIME_TOKEN}_parts"
OLD_RUNTIME_MODULE = f"med_autogrant.{OLD_RUNTIME_TOKEN}"


class RuntimeSplitStructureTest(unittest.TestCase):
    def test_source_modules_do_not_use_star_imports(self) -> None:
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in sorted((SRC_ROOT / "med_autogrant").rglob("*.py"))
            if "import *" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_mag_domain_runtime_is_domain_adapter_not_generic_runtime_owner(self) -> None:
        from med_autogrant.domain_runtime import MagDomainRuntime

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
        from med_autogrant.domain_runtime import MagDomainRuntime
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
        self.assertNotIn(OLD_RUNTIME_IMPORT, domain_entry_text)

    def test_control_plane_does_not_import_workspace_facade(self) -> None:
        control_plane_text = (SRC_ROOT / "med_autogrant" / "control_plane.py").read_text(encoding="utf-8")

        self.assertNotIn("from med_autogrant.workspace import", control_plane_text)

    def test_retired_runtime_module_paths_are_not_present_in_source(self) -> None:
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in sorted((SRC_ROOT / "med_autogrant").rglob("*.py"))
            if OLD_RUNTIME_TOKEN in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_runtime_patch_target_bridge_is_retired(self) -> None:
        self.assertFalse((SRC_ROOT / "med_autogrant" / "domain_runtime_parts" / "patch_targets.py").exists())

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in sorted((SRC_ROOT / "med_autogrant" / "domain_runtime_parts").glob("*.py"))
            if "resolve_runtime_patch_target" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_runtime_parts_do_not_import_runtime_facade(self) -> None:
        runtime_parts = sorted((SRC_ROOT / "med_autogrant" / "domain_runtime_parts").glob("*.py"))
        forbidden_fragments = (
            "from med_autogrant.domain_runtime import",
            OLD_RUNTIME_IMPORT,
            OLD_RUNTIME_MODULE_IMPORT,
        )
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in runtime_parts
            if any(fragment in path.read_text(encoding="utf-8") for fragment in forbidden_fragments)
        ]

        self.assertEqual([], offenders)

    def test_package_surface_does_not_import_runtime_facade(self) -> None:
        package_surface_text = (
            SRC_ROOT / "med_autogrant" / "domain_runtime_parts" / "package_surface.py"
        ).read_text(encoding="utf-8")

        self.assertIn("class DomainRuntimePackageSurfaceMixin", package_surface_text)
        self.assertNotIn("from med_autogrant.domain_runtime import", package_surface_text)
        self.assertNotIn(OLD_RUNTIME_IMPORT, package_surface_text)
        self.assertNotIn(OLD_RUNTIME_PARTS, package_surface_text)

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

    def test_workspace_facade_imports_only_public_workspace_surfaces(self) -> None:
        offenders: list[str] = []
        forbidden_names = {
            "WorkspaceError",
            "WorkspaceFileError",
            "WorkspaceStateError",
            "_SchemaSubsetValidator",
            "_build_workspace_state",
            "_collect_known_ids",
            "_require_workspace_context",
            "validate_workspace_document",
        }
        for path in sorted((SRC_ROOT / "med_autogrant").rglob("*.py")):
            if path.name == "workspace.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or node.module != "med_autogrant.workspace":
                    continue
                imported_names = {alias.name for alias in node.names}
                forbidden_imports = sorted(imported_names & forbidden_names)
                if forbidden_imports:
                    relative_path = path.relative_to(REPO_ROOT).as_posix()
                    offenders.append(f"{relative_path}: {', '.join(forbidden_imports)}")

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
