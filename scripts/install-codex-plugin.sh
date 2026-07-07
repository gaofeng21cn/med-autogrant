#!/usr/bin/env bash
set -euo pipefail

readonly DEFAULT_REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

REPO_ROOT="${DEFAULT_REPO_ROOT}"
INSTALL_HOME="${HOME}"

fail() {
  printf "med-autogrant codex installer error: %s\n" "$1" >&2
  exit 1
}

usage() {
  cat >&2 <<'EOF'
Usage: install-codex-plugin.sh [--repo-root /abs/path/to/repo] [--home /abs/path/to/home]
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
  if ! command -v python3 >/dev/null 2>&1; then
    fail "required command not found: python3"
  fi
}

install_codex_paths() {
  HOME="${INSTALL_HOME}" PYTHONPATH="${REPO_ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}" python3 -m med_autogrant.codex_plugin_installer \
    --repo-root "${REPO_ROOT}" \
    --home "${INSTALL_HOME}"
}

main() {
  parse_args "$@"
  check_dependencies

  install_codex_paths

  printf "checked MedAutoGrant tracked Codex plugin source and retired repo-local marketplace metadata\n" >&2
  printf "CLI installation is owned by Python packaging project.scripts, not this domain installer\n" >&2
  printf "Codex marketplace registration is owned by the OPL wrapper, not this domain repo\n" >&2
}

main "$@"
