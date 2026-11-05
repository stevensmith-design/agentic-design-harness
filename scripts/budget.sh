#!/usr/bin/env bash
# Measure the actual installed design module, preserving the engineering harness's own budget.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
CONTEXT="$HERE/harness-context.py"; [ -f "$CONTEXT" ] || CONTEXT="$HERE/dh-context.py"
python3 "$CONTEXT" --root "$ROOT" --budget
