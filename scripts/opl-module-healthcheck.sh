#!/usr/bin/env bash
set -euo pipefail

export PATH="${HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:${PATH}"

command -v python3 >/dev/null 2>&1
command -v uv >/dev/null 2>&1

make test-cli-smoke
