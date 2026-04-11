#!/usr/bin/env bash
set -euo pipefail

lane="${1:-smoke}"

case "$lane" in
  smoke|fast)
    make test-fast
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
    echo "Usage: scripts/verify.sh [smoke|fast|meta|cli-smoke|full]" >&2
    exit 1
    ;;
esac
