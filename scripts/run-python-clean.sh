#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
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

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-${tmp_root}/pycache}"
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
if [[ -n "${MAG_CLEAN_RUNNER_UV_EXTRA:-}" ]]; then
  sync_args+=(--extra "${MAG_CLEAN_RUNNER_UV_EXTRA}")
fi

if [[ "${MAG_CLEAN_RUNNER_SKIP_SYNC:-0}" != "1" && "${UV_NO_SYNC:-0}" != "1" ]]; then
  "${sync_args[@]}"
fi
export MAG_CLEAN_RUNNER_SKIP_SYNC=1

venv_python="${repo_root}/.venv/bin/python"
if [[ ! -x "${venv_python}" ]]; then
  echo "run-python-clean.sh: missing venv Python after dependency sync: ${venv_python}" >&2
  exit 1
fi

exec "${venv_python}" "$@"
