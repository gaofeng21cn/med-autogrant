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
  fast)
    make test-fast
    ;;
  smoke|cli-smoke)
    make test-line-budget
    make test-cli-smoke
    ;;
  family)
    make test-line-budget
    make test-family
    ;;
  meta)
    make test-meta
    ;;
  regression)
    make test-regression
    ;;
  proof)
    make test-proof
    ;;
  structure)
    make test-structure
    ;;
  full)
    make test-full
    ;;
  *)
    echo "Unknown lane: $lane" >&2
    echo "Usage: $0 [fast|smoke|cli-smoke|family|meta|regression|proof|structure|full|cleanup]" >&2
    exit 2
    ;;
esac
