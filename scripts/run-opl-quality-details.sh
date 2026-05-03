#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"

output_dir="${OPL_QUALITY_DETAILS_DIR:-artifacts/opl-quality-details}"
opl_bin="${OPL_QUALITY_DETAILS_BIN:-/Users/gaofeng/workspace/one-person-lab/bin/opl}"

mkdir -p "${output_dir}"

if [[ -f .sentrux/rules.toml ]]; then
  rules_sidecar="${output_dir}/sentrux-rules.toml"
  cp .sentrux/rules.toml "${rules_sidecar}"
  echo "Writing complete Sentrux rules diagnostic sidecar: ${rules_sidecar}" >&2
fi

if [[ ! -x "${opl_bin}" ]]; then
  echo "OPL quality details unavailable: ${opl_bin} is not executable" >&2
  exit 0
fi

markdown_path="${output_dir}/quality-details.md"
json_path="${output_dir}/quality-details.json"

echo "Writing OPL quality details markdown sidecar: ${markdown_path}" >&2
if ! "${opl_bin}" quality details --root . --format markdown --limit 20 | tee "${markdown_path}"; then
  echo "OPL quality details markdown generation failed; continuing with Sentrux result as authority." >&2
  exit 0
fi

echo "Writing OPL quality details json sidecar: ${json_path}" >&2
if ! "${opl_bin}" quality details --root . --format json >"${json_path}"; then
  echo "OPL quality details json generation failed; continuing with Sentrux result as authority." >&2
  rm -f "${json_path}"
fi
