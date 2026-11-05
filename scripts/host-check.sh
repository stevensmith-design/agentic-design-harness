#!/usr/bin/env bash
# Verify the actual explicit instruction chain; no live native activation claim.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="${1:-$(cd "$HERE/.." && pwd)}"
if [ $# -gt 0 ]; then shift; fi
PREFLIGHT="$HERE/harness-preflight.py"; [ -f "$PREFLIGHT" ] || PREFLIGHT="$HERE/dh-preflight.py"
CONTEXT="$HERE/harness-context.py"; [ -f "$CONTEXT" ] || CONTEXT="$HERE/dh-context.py"
python3 "$PREFLIGHT" --root "$ROOT"
python3 "$CONTEXT" --root "$ROOT" "$@"
