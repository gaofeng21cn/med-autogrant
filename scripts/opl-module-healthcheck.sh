#!/usr/bin/env bash
set -euo pipefail

python scripts/line_budget.py
make test-cli-smoke
