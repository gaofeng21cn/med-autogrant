#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"

strict=false
case "${1:-}" in
  ""|"--advisory")
    strict=false
    ;;
  "--strict")
    strict=true
    ;;
  *)
    echo "Usage: $0 [--advisory|--strict]" >&2
    exit 2
    ;;
esac

status=0

./scripts/run-opl-quality-details.sh

if [[ -f .sentrux/baseline.json ]]; then
  if ! sentrux gate .; then
    echo "Sentrux failed; generating OPL quality details and complete .sentrux/rules.toml sidecar before reporting failure." >&2
    ./scripts/run-opl-quality-details.sh
    echo "::warning::Sentrux reported structural regression. Review OPL quality details and the complete Sentrux rules sidecar before accepting this change."
    status=1
  fi
else
  echo "::notice::No .sentrux/baseline.json found; saving advisory baseline for this run."
  sentrux gate --save .
fi

if [[ -f .sentrux/rules.toml ]]; then
  if ! sentrux check .; then
    echo "Sentrux failed; generating OPL quality details and complete .sentrux/rules.toml sidecar before reporting failure." >&2
    ./scripts/run-opl-quality-details.sh
    echo "::warning::Sentrux rules reported violations. Review OPL quality details and the complete Sentrux rules sidecar before accepting this change."
    status=1
  fi
else
  echo "::notice::No .sentrux/rules.toml found; skipping rules check."
fi

if [[ "${status}" -ne 0 && "${strict}" == "true" ]]; then
  exit "${status}"
fi
