#!/usr/bin/env bash
set -euo pipefail

readonly DEFAULT_REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

REPO_ROOT="${DEFAULT_REPO_ROOT}"
INSTALL_HOME="${HOME}"
SKIP_TOOLS=0

fail() {
  printf "med-autogrant codex installer error: %s\n" "$1" >&2
  exit 1
}

usage() {
  cat >&2 <<'EOF'
Usage: install-codex-plugin.sh [--repo-root /abs/path/to/repo] [--home /abs/path/to/home] [--skip-tools]
EOF
}

parse_args() {
  while (($#)); do
    case "$1" in
      --repo-root)
        [[ $# -ge 2 ]] || fail "--repo-root requires a value"
        REPO_ROOT="$2"
        shift 2
        ;;
      --home)
        [[ $# -ge 2 ]] || fail "--home requires a value"
        INSTALL_HOME="$2"
        shift 2
        ;;
      --skip-tools)
        SKIP_TOOLS=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        fail "unknown argument: $1"
        ;;
    esac
  done
}

check_dependencies() {
  local cmd
  for cmd in bash python3; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
      fail "required command not found: ${cmd}"
    fi
  done
}

install_python_tools() {
  mkdir -p "${INSTALL_HOME}/.local/bin"
  write_clean_runner_entrypoint medautogrant med_autogrant.cli
}

write_clean_runner_entrypoint() {
  local name="$1"
  local module="$2"
  local script_path="${INSTALL_HOME}/.local/bin/${name}"
  rm -f "${script_path}.uv-entrypoint"
  rm -f "${script_path}"
  cat >"${script_path}" <<EOF
#!/usr/bin/env bash
set -euo pipefail
# med-autogrant clean runner wrapper: avoid repo-local virtualenv, bytecode, and editable metadata.
exec "${REPO_ROOT}/scripts/run-python-clean.sh" -m "${module}" "\$@"
EOF
  chmod +x "${script_path}"
}

install_codex_paths() {
  HOME="${INSTALL_HOME}" PYTHONPATH="${REPO_ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}" python3 -m med_autogrant.codex_plugin_installer \
    --repo-root "${REPO_ROOT}" \
    --home "${INSTALL_HOME}"
}

main() {
  parse_args "$@"
  check_dependencies

  if [[ "${SKIP_TOOLS}" -eq 0 ]]; then
    install_python_tools
  fi

  install_codex_paths

  if [[ "${SKIP_TOOLS}" -eq 1 ]]; then
    printf "checked MedAutoGrant tracked Codex plugin source and retired repo-local marketplace metadata (skip-tools)\n" >&2
  else
    printf "installed MedAutoGrant CLI tools into %s and checked tracked Codex plugin source\n" "${INSTALL_HOME}" >&2
    printf "Codex marketplace registration is owned by the OPL wrapper, not this domain repo\n" >&2
  fi
}

main "$@"
