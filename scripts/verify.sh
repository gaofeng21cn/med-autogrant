#!/usr/bin/env bash
set -euo pipefail

lane="${1:-fast}"

case "$lane" in
  fast)
    make test-fast
    ;;
  full)
    make test-full
    ;;
  *)
    echo "Usage: $0 [fast|full]" >&2
    exit 2
    ;;
esac
