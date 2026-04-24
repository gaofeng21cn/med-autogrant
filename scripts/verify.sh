#!/usr/bin/env bash
set -euo pipefail

lane="${1:-fast}"

python scripts/line_budget.py

case "$lane" in
  fast|smoke)
    make test-line-budget
    make test-fast
    ;;
  family)
    make test-line-budget
    make test-family
    ;;
  meta)
    make test-meta
    ;;
  cli-smoke)
    make test-cli-smoke
    ;;
  full)
    make test-full
    ;;
  *)
    echo "Unknown lane: $lane" >&2
    echo "Usage: $0 [fast|family|meta|cli-smoke|full]" >&2
    exit 2
    ;;
esac
