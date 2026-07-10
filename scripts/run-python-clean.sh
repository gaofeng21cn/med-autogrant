#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

cleanup_tmp_root=0
if [[ -n "${MAG_CLEAN_RUNNER_TMP_ROOT:-}" ]]; then
  tmp_root="${MAG_CLEAN_RUNNER_TMP_ROOT}"
else
  tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/mag-python-run.XXXXXX")"
  cleanup_tmp_root=1
fi

cleanup() {
  if [[ "${cleanup_tmp_root}" == "1" ]]; then
    rm -rf "${tmp_root}"
  fi
}
trap cleanup EXIT

mkdir -p "${tmp_root}"

resolve_for_boundary_check() {
  local raw_path="${1}"
  local path
  local parent
  local base

  if [[ -z "${raw_path}" ]]; then
    return 1
  fi

  case "${raw_path}" in
    "~")
      path="${HOME}"
      ;;
    "~/"*)
      path="${HOME}/${raw_path#~/}"
      ;;
    /*)
      path="${raw_path}"
      ;;
    *)
      path="${repo_root}/${raw_path}"
      ;;
  esac

  if [[ -d "${path}" ]]; then
    (cd "${path}" >/dev/null 2>&1 && pwd -P)
    return
  fi

  parent="$(dirname "${path}")"
  base="$(basename "${path}")"
  if [[ -d "${parent}" ]]; then
    printf '%s/%s\n' "$(cd "${parent}" >/dev/null 2>&1 && pwd -P)" "${base}"
    return
  fi

  return 1
}

path_is_inside_checkout() {
  local raw_path="${1}"
  local resolved

  resolved="$(resolve_for_boundary_check "${raw_path}")" || return 1
  [[ "${resolved}" == "${repo_root}" || "${resolved}" == "${repo_root}/"* ]]
}

if path_is_inside_checkout "${UV_PROJECT_ENVIRONMENT:-}"; then
  unset UV_PROJECT_ENVIRONMENT
fi

if path_is_inside_checkout "${PYTHONPYCACHEPREFIX:-}"; then
  unset PYTHONPYCACHEPREFIX
fi

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-${tmp_root}/pycache}"
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-${tmp_root}/venv}"
export PYTHONPATH="${repo_root}/src${PYTHONPATH:+:${PYTHONPATH}}"
export PYTEST_ADDOPTS="${PYTEST_ADDOPTS:-} -p no:cacheprovider -o cache_dir=${tmp_root}/pytest-cache"

entrypoint_bin="${tmp_root}/bin"
mkdir -p "${entrypoint_bin}"

cat >"${entrypoint_bin}/medautogrant" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "${repo_root}/scripts/run-python-clean.sh" -m med_autogrant.cli "\$@"
EOF
chmod +x "${entrypoint_bin}/medautogrant"
export PATH="${entrypoint_bin}:${PATH}"

sync_args=(uv sync --frozen --group dev --no-install-project --inexact)

if [[ "${MAG_CLEAN_RUNNER_SKIP_SYNC:-0}" != "1" && "${UV_NO_SYNC:-0}" != "1" ]]; then
  "${sync_args[@]}"
fi
export MAG_CLEAN_RUNNER_SKIP_SYNC=1

venv_python="${UV_PROJECT_ENVIRONMENT}/bin/python"
if [[ ! -x "${venv_python}" ]]; then
  echo "run-python-clean.sh: missing venv Python after dependency sync: ${venv_python}" >&2
  exit 1
fi

exec "${venv_python}" "$@"
