#!/usr/bin/env bash
set -euo pipefail

lane="${1:-fast}"

if [[ "$lane" == "cleanup" || "$lane" == "fix" || "$lane" == "hygiene:fix" ]]; then
  scripts/repo-hygiene.sh --fix
  scripts/repo-hygiene.sh
  exit 0
fi

scripts/repo-hygiene.sh

case "$lane" in
  cli-smoke) lane="smoke" ;;
  source-purity:strict) lane="source-purity-strict" ;;
esac

exec make "test-${lane}"
