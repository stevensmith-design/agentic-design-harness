#!/usr/bin/env bash
# ADDITIVE ONLY. Preserve project files; report collisions and incomplete integration.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/scripts/install.py" "$@"
