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

requested_uv_project_environment="${UV_PROJECT_ENVIRONMENT:-}"
if path_is_inside_checkout "${requested_uv_project_environment}"; then
  unset UV_PROJECT_ENVIRONMENT
fi

if path_is_inside_checkout "${PYTHONPYCACHEPREFIX:-}"; then
  unset PYTHONPYCACHEPREFIX
fi

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-${tmp_root}/pycache}"
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-${tmp_root}/venv}"

resolve_launcher_path() {
  local path="${1}"
  local link_target
  local parent

  if [[ "${path}" != */* ]]; then
    path="$(command -v "${path}" 2>/dev/null)" || return 1
  fi
  while [[ -L "${path}" ]]; do
    parent="$(cd "$(dirname "${path}")" >/dev/null 2>&1 && pwd -P)" || return 1
    link_target="$(readlink "${path}")" || return 1
    if [[ "${link_target}" == /* ]]; then
      path="${link_target}"
    else
      path="${parent}/${link_target}"
    fi
  done
  parent="$(cd "$(dirname "${path}")" >/dev/null 2>&1 && pwd -P)" || return 1
  printf '%s/%s\n' "${parent}" "$(basename "${path}")"
}

opl_client_src=""
if [[ -n "${OPL_PYTHON_CLIENT_DIR:-}" ]]; then
  if [[ -f "${OPL_PYTHON_CLIENT_DIR}/src/opl_client/__init__.py" ]]; then
    opl_client_src="$(cd "${OPL_PYTHON_CLIENT_DIR}/src" >/dev/null 2>&1 && pwd -P)"
  elif [[ -f "${OPL_PYTHON_CLIENT_DIR}/opl_client/__init__.py" ]]; then
    opl_client_src="$(cd "${OPL_PYTHON_CLIENT_DIR}" >/dev/null 2>&1 && pwd -P)"
  else
    echo "run-python-clean.sh: invalid OPL_PYTHON_CLIENT_DIR: ${OPL_PYTHON_CLIENT_DIR}" >&2
    exit 1
  fi
fi

if [[ -z "${opl_client_src}" ]]; then
  framework_root="${OPL_FRAMEWORK_ROOT:-${OPL_OWNER_REPO_ROOT:-}}"
  if [[ -z "${framework_root}" ]]; then
    opl_launcher="${OPL_BIN:-}"
    if [[ -z "${opl_launcher}" ]]; then
      opl_launcher="$(command -v opl 2>/dev/null || true)"
    fi
    if [[ -n "${opl_launcher}" ]]; then
      resolved_launcher="$(resolve_launcher_path "${opl_launcher}")" || true
      if [[ -n "${resolved_launcher:-}" ]]; then
        framework_root="$(cd "$(dirname "${resolved_launcher}")/.." >/dev/null 2>&1 && pwd -P)"
      fi
    fi
  fi
  if [[ -n "${framework_root}" && -f "${framework_root}/sdks/python-client/src/opl_client/__init__.py" ]]; then
    opl_client_src="$(cd "${framework_root}/sdks/python-client/src" >/dev/null 2>&1 && pwd -P)"
  elif [[ -f "${repo_root}/../one-person-lab/sdks/python-client/src/opl_client/__init__.py" ]]; then
    opl_client_src="$(cd "${repo_root}/../one-person-lab/sdks/python-client/src" >/dev/null 2>&1 && pwd -P)"
  elif [[ -f "${repo_root}/../.worktrees/opl-v2/sdks/python-client/src/opl_client/__init__.py" ]]; then
    opl_client_src="$(cd "${repo_root}/../.worktrees/opl-v2/sdks/python-client/src" >/dev/null 2>&1 && pwd -P)"
  fi
fi

if [[ -z "${opl_client_src}" ]]; then
  if python3 -c "import opl_client" >/dev/null 2>&1; then
    export PYTHONPATH="${repo_root}/src${PYTHONPATH:+:${PYTHONPATH}}"
  else
    echo "run-python-clean.sh: cannot locate opl_client SDK; set OPL_PYTHON_CLIENT_DIR or OPL_BIN" >&2
    exit 1
  fi
else
  export PYTHONPATH="${opl_client_src}:${repo_root}/src${PYTHONPATH:+:${PYTHONPATH}}"
fi
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
if [[ ! -x "${venv_python}" && "${MAG_CLEAN_RUNNER_SKIP_SYNC:-0}" == "1" \
  && -x "${requested_uv_project_environment}/bin/python" ]]; then
  # A caller may deliberately reuse its already-active test environment while
  # skipping sync; retain that explicit interpreter without making it the
  # default cache or sync location.
  venv_python="${requested_uv_project_environment}/bin/python"
fi
if [[ ! -x "${venv_python}" ]]; then
  echo "run-python-clean.sh: missing venv Python after dependency sync: ${venv_python}" >&2
  exit 1
fi

exec "${venv_python}" "$@"
