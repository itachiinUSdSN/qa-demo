#!/usr/bin/env bash
# The load agent's only way to run k6: one virtual user, one iteration, against staging.
set -euo pipefail
case "${1:-}" in tests/load/*.js) ;; *) echo "usage: k6-smoke.sh tests/load/<name>.js" >&2; exit 2;; esac
BASE_URL="$STAGING_API_URL" exec k6 run --vus 1 --iterations 1 "$1"
