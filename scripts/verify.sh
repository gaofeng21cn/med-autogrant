#!/usr/bin/env bash
set -euo pipefail

lane="${1:-fast}"

case "$lane" in
  fast|smoke)
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
    echo "Usage: $0 [fast|meta|cli-smoke|full]" >&2
    exit 2
    ;;
esac
