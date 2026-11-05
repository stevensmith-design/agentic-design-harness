#!/usr/bin/env bash
# Verify the bundled skills against this package's own lock. Local only; no other checkout is used.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/scripts/gen-lock.py" --check
python3 "$ROOT/scripts/harness-preflight.py" --root "$ROOT"
