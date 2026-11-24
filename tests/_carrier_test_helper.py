#!/usr/bin/env python3
"""Materialize or verify MAG's native plugin carrier from canonical repo sources."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CARRIER_PROJECTION_REL = "contracts/carrier_projection.json"
OWNER_MANIFEST_REL = "contracts/opl_agent_package_manifest.json"
EXPECTED_TRACKED_CARRIER_FILES = frozenset(
    {
        "plugins/med-autogrant/.codex-plugin/plugin.json",
        "plugins/med-autogrant/app-contribution-adapter.json",
        "plugins/med-autogrant/assets/icon.png",
        "plugins/med-autogrant/assets/icon.svg",
        "plugins/med-autogrant/opl-package.json",
        "plugins/med-autogrant/plugin.json",
        "plugins/med-autogrant/skills/med-autogrant/SKILL.md",
        "plugins/med-autogrant/skills/med-autogrant/agents/openai.yaml",
    }
)
PROJECTED_DESCRIPTOR_FIELDS = (
    "surface_kind",
    "kind",
    "agent_id",
    "package_id",
    "domain_id",
    "display_name",
    "presentation",
    "publisher",
    "version",
    "source",
    "carrier_source_role",
    "schema_ref",
    "domain_descriptor_ref",
    "task_provider_ref",
    "action_catalog_ref",
    "view_refs",
    "entrypoints",
    "capability_dependencies",
    "app_contributions",
)
PROJECTED_CODEX_SURFACE_FIELDS = (
    "plugin_id",
    "plugin_source_path",
    "configured_codex_plugin_carrier",
    "required_skill_ids",
    "app_contribution_abi",
    "app_contribution_adapter",
)


def resolve_opl_bin(*, required: bool = True) -> str | None:
    env_bin = os.environ.get("OPL_BIN", "").strip()
    if env_bin:
        return env_bin
    fw_root = os.environ.get("OPL_FRAMEWORK_ROOT", "").strip()
    if fw_root:
        candidate = Path(fw_root) / "bin" / "opl"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    sibling = ROOT.parent / "one-person-lab" / "bin" / "opl"
    if sibling.is_file() and os.access(sibling, os.X_OK):
        return str(sibling)
    found = shutil.which("opl")
    if found:
        return found
    if required:
        raise SystemExit("OPL CLI is unavailable; set OPL_BIN or OPL_FRAMEWORK_ROOT.")
    return None


def _git_ls_files(repo_root: Path, pathspec: str | None = None) -> list[str]:
    cmd = ["git", "-C", str(repo_root), "ls-files", "-z"]
    if pathspec is not None:
        cmd.extend(["--", pathspec])
    completed = subprocess.run(cmd, check=True, capture_output=True)
    return [entry.decode("utf-8") for entry in completed.stdout.split(b"\x00") if entry]


def _forbidden_mirror_targets(config: dict[str, Any]) -> tuple[tuple[str, ...], frozenset[str]]:
    carrier_root = str(config["carrier_root"]).strip("/")
    prefixes: set[str] = {f"{carrier_root}/src/", f"{carrier_root}/assets/branding/"}
    exact_files: set[str] = set()
    for root in config.get("resource_roots", []):
        rel = str(root).strip("/")
        if rel:
            prefixes.add(f"{carrier_root}/{rel}/")
    for extra in config.get("extra_files", []):
        rel = str(extra).strip("/")
        if rel:
            exact_files.add(f"{carrier_root}/{rel}")
    return tuple(sorted(prefixes)), frozenset(exact_files)


def _check_tracked_carrier_shell(
    repo_root: Path,
    config: dict[str, Any],
) -> tuple[list[str], list[str]]:
    carrier_root = str(config["carrier_root"]).strip("/")
    tracked = sorted(_git_ls_files(repo_root, carrier_root))
    errors: list[str] = []
    forbidden_prefixes, forbidden_exact = _forbidden_mirror_targets(config)

    for rel in tracked:
        if rel in forbidden_exact or any(rel.startswith(prefix) for prefix in forbidden_prefixes):
            errors.append(f"mirror artifact must not be tracked in Git: {rel}")
        elif rel.endswith(".py"):
            errors.append(f"Python source must not be tracked under carrier root: {rel}")

    tracked_set = set(tracked)
    missing_expected = sorted(EXPECTED_TRACKED_CARRIER_FILES - tracked_set)
    for rel in missing_expected:
        errors.append(f"required thin carrier file is not tracked in Git: {rel}")
    unexpected_tracked = sorted(tracked_set - EXPECTED_TRACKED_CARRIER_FILES)
    for rel in unexpected_tracked:
        if not any(rel in err for err in errors):
            errors.append(f"unexpected file tracked under thin carrier root: {rel}")

    for rel in sorted(EXPECTED_TRACKED_CARRIER_FILES):
        if not (repo_root / rel).is_file():
            errors.append(f"tracked thin carrier file is missing on disk: {rel}")

    return tracked, errors


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check_metadata_and_alias_parity(repo_root: Path) -> list[str]:
    errors: list[str] = []
    owner_manifest_path = repo_root / OWNER_MANIFEST_REL
    root_descriptor_path = repo_root / "opl-package.json"
    carrier_root = repo_root / "plugins" / "med-autogrant"
    carrier_descriptor_path = carrier_root / "opl-package.json"
    codex_manifest_path = carrier_root / ".codex-plugin" / "plugin.json"
    portable_manifest_path = carrier_root / "plugin.json"
    primary_skill_path = repo_root / "agent" / "primary_skill" / "SKILL.md"
    carrier_skill_path = carrier_root / "skills" / "med-autogrant" / "SKILL.md"
    owner_adapter_path = repo_root / "app-contribution-adapter.json"
    carrier_adapter_path = carrier_root / "app-contribution-adapter.json"

    if root_descriptor_path.read_bytes() != owner_manifest_path.read_bytes():
        errors.append("opl-package.json is out of sync with contracts/opl_agent_package_manifest.json")
    if carrier_skill_path.read_bytes() != primary_skill_path.read_bytes():
        errors.append(
            "plugins/med-autogrant/skills/med-autogrant/SKILL.md is out of sync with agent/primary_skill/SKILL.md"
        )
    if carrier_adapter_path.read_bytes() != owner_adapter_path.read_bytes():
        errors.append(
            "plugins/med-autogrant/app-contribution-adapter.json is out of sync with app-contribution-adapter.json"
        )

    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    lock_data = tomllib.loads((repo_root / "uv.lock").read_text(encoding="utf-8"))
    owner_manifest = _read_json(owner_manifest_path)
    carrier_descriptor = _read_json(carrier_descriptor_path)
    codex_manifest = _read_json(codex_manifest_path)
    portable_manifest = _read_json(portable_manifest_path)
    init_text = (repo_root / "src" / "med_autogrant" / "__init__.py").read_text(encoding="utf-8")

    project_name = pyproject["project"]["name"]
    expected_version = pyproject["project"]["version"]
    locked_version = next(
        (pkg.get("version") for pkg in lock_data.get("package", []) if pkg.get("name") == project_name),
        None,
    )
    init_match = re.search(r'^__version__\s*=\s*"([^"]+)"', init_text, re.MULTILINE)
    init_version = init_match.group(1) if init_match else None

    version_sources = {
        "src/med_autogrant/__init__.py": init_version,
        "uv.lock": locked_version,
        OWNER_MANIFEST_REL: owner_manifest.get("version"),
        "plugins/med-autogrant/opl-package.json": carrier_descriptor.get("version"),
        "plugins/med-autogrant/.codex-plugin/plugin.json": codex_manifest.get("version"),
        "plugins/med-autogrant/plugin.json": portable_manifest.get("version"),
    }
    for source_name, observed in version_sources.items():
        if observed != expected_version:
            errors.append(
                f"version mismatch in {source_name}: {observed!r} != pyproject.toml {expected_version!r}"
            )

    for field in PROJECTED_DESCRIPTOR_FIELDS:
        if carrier_descriptor.get(field) != owner_manifest.get(field):
            errors.append(f"plugins/med-autogrant/opl-package.json mismatch for field: {field}")

    owner_surface = owner_manifest.get("codex_surface", {})
    carrier_surface = carrier_descriptor.get("codex_surface", {})
    for field in PROJECTED_CODEX_SURFACE_FIELDS:
        if carrier_surface.get(field) != owner_surface.get(field):
            errors.append(
                f"plugins/med-autogrant/opl-package.json mismatch for codex_surface.{field}"
            )

    expected_requires = [
        {
            "package_id": dep["package_id"],
            "presence": "required" if dep.get("required") else "optional",
        }
        for dep in owner_manifest.get("capability_dependencies", [])
    ]
    if carrier_descriptor.get("requires") != expected_requires:
        errors.append("plugins/med-autogrant/opl-package.json requires does not match capability_dependencies")

    if portable_manifest.get("name") != codex_manifest.get("name"):
        errors.append("plugins/med-autogrant/plugin.json name does not match .codex-plugin/plugin.json")
    portable_interface = portable_manifest.get("extensions", {}).get("com.openai", {}).get("interface")
    codex_interface = codex_manifest.get("interface")
    if portable_interface != codex_interface:
        errors.append("plugins/med-autogrant/plugin.json openai interface does not match .codex-plugin/plugin.json")
    for icon_field in ("logo", "composerIcon"):
        icon_value = codex_interface.get(icon_field) if isinstance(codex_interface, dict) else None
        if icon_value != "./assets/icon.png":
            errors.append(
                f"plugins/med-autogrant/.codex-plugin/plugin.json interface.{icon_field} "
                f"must be './assets/icon.png' (got {icon_value!r})"
            )
        elif not (carrier_root / icon_value.removeprefix("./")).is_file():
            errors.append(f"carrier icon file missing: {icon_value}")

    return errors


def stage_repo_for_carrier_projection(source_root: Path, dest_repo: Path) -> Path:
    staged = dest_repo.resolve()
    staged.mkdir(parents=True, exist_ok=True)
    for rel in _git_ls_files(source_root):
        src_file = source_root / rel
        if not src_file.is_file() or src_file.is_symlink():
            continue
        dst_file = staged / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)
    subprocess.run(["git", "-C", str(staged), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(staged), "add", "-A"], check=True)
    return staged


def materialize_carrier_in_temp(
    source_root: Path,
    temp_root: Path,
    *,
    opl_bin: str | None = None,
) -> tuple[Path, dict[str, Any]]:
    resolved_bin = opl_bin or resolve_opl_bin(required=True)
    assert resolved_bin is not None
    staged_repo = stage_repo_for_carrier_projection(source_root, temp_root / "repo")
    config = _read_json(source_root / CARRIER_PROJECTION_REL)
    carrier_root_rel = str(config["carrier_root"]).strip("/")

    projected = subprocess.run(
        [resolved_bin, "pack", "project-carrier", "--repo", str(staged_repo), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if projected.returncode != 0:
        detail = projected.stderr.strip() or projected.stdout.strip()
        raise RuntimeError(f"opl pack project-carrier failed (exit {projected.returncode}): {detail}")

    verified = subprocess.run(
        [resolved_bin, "pack", "project-carrier", "--repo", str(staged_repo), "--json", "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if verified.returncode != 0:
        detail = verified.stderr.strip() or verified.stdout.strip()
        raise RuntimeError(f"opl pack project-carrier --check failed (exit {verified.returncode}): {detail}")

    report = json.loads(verified.stdout) if verified.stdout.strip() else {}
    return staged_repo / carrier_root_rel, report


def _check_staged_materialization(
    repo_root: Path,
    tracked_carrier_files: list[str],
    opl_bin: str,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="mag-carrier-check-") as tmp_dir:
        staged_root = Path(tmp_dir)
        try:
            _staged_carrier_dir, report = materialize_carrier_in_temp(
                repo_root,
                staged_root,
                opl_bin=opl_bin,
            )
        except RuntimeError as exc:
            return [str(exc)], {"status": "failed"}

        staged_repo = (staged_root / "repo").resolve()
        for rel in tracked_carrier_files:
            repo_file = repo_root / rel
            staged_file = staged_repo / rel
            if not staged_file.is_file():
                errors.append(f"tracked carrier file missing after staged projection: {rel}")
            elif repo_file.read_bytes() != staged_file.read_bytes():
                errors.append(f"tracked carrier file differs from staged projection output: {rel}")

        projection_summary = report.get("pack_carrier_projection", {})
        return errors, {
            "status": "passed" if not errors else "failed",
            "projected_file_count": projection_summary.get("projected_file_count"),
            "unchanged_count": projection_summary.get("unchanged_count"),
        }


def run_check(repo_root: Path = ROOT) -> tuple[int, dict[str, Any]]:
    config = _read_json(repo_root / CARRIER_PROJECTION_REL)
    tracked_carrier_files, shell_errors = _check_tracked_carrier_shell(repo_root, config)
    parity_errors = _check_metadata_and_alias_parity(repo_root)
    errors = [*shell_errors, *parity_errors]

    opl_bin = resolve_opl_bin(required=False)
    staged_report: dict[str, Any]
    if opl_bin is not None:
        staged_errors, staged_report = _check_staged_materialization(
            repo_root,
            tracked_carrier_files,
            opl_bin,
        )
        errors.extend(staged_errors)
    else:
        staged_report = {"status": "skipped", "reason": "opl_cli_unavailable"}

    payload = {
        "mode": "check",
        "status": "passed" if not errors else "failed",
        "carrier_root": config["carrier_root"],
        "tracked_carrier_file_count": len(tracked_carrier_files),
        "tracked_carrier_files": tracked_carrier_files,
        "staged_materialization": staged_report,
        "errors": errors,
    }
    return (0 if not errors else 1), payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        code, payload = run_check(ROOT)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return code

    opl_bin = resolve_opl_bin(required=True)
    assert opl_bin is not None
    cmd = [opl_bin, "pack", "project-carrier", "--repo", str(ROOT), "--json"]
    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
