#!/bin/bash
# package — build the redistributable Agentic Design Harness archives.
#
# Packaging only. It does not manage, install or verify the harness beyond the
# checks that already exist; it runs those, stages what ships, and writes the
# archives plus their checksums and a manifest.
#
# Usage: scripts/package.sh [version]     (default: 2.0.0)
# Exit:  0 packaged · 1 a precondition or a packaging check failed

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="${1:-$(cat "$ROOT/VERSION")}"
NAME="agentic-design-harness-v${VERSION}"
DIST="$ROOT/dist"
STAGE="$DIST/.stage/$NAME"

GRN='\033[0;32m'; RED='\033[0;31m'; CYN='\033[0;36m'; BLD='\033[1m'; RST='\033[0m'
FAIL=0
ok()   { echo -e "  ${GRN}✔${RST} $1"; }
bad()  { echo -e "  ${RED}✘${RST} $1"; FAIL=1; }
step() { echo; echo -e "${CYN}$1${RST}"; }

# ── 1 · required files ───────────────────────────────────────────────────────
step "1 · Source tree"
REQUIRED=(
  AGENTS.md CLAUDE.md README.md LICENSE NOTICE CONTRIBUTING.md SECURITY.md CHANGELOG.md
  VERSION docs/skills-lock.json docs/harness-package.json integration/design-harness-rule.md
  scripts/harness-preflight.py scripts/harness-context.py scripts/install.py scripts/create-project.py scripts/measure/skill-root.mjs
  docs/PROJECT-START.md scripts/tests/release-regressions.py
  scripts/check-public-content.py scripts/tests/content-audit/run.py
  scripts/tests/wiring.py scripts/tests/contracts.py
  scripts/init.sh scripts/check.sh scripts/smoke.sh scripts/host-check.sh
  scripts/check-skill-sync.sh scripts/gen-lock.py
  scripts/budget.sh scripts/cheatsheet.sh
  design/product.md design/cheatsheet.md design/components.md
)
for f in "${REQUIRED[@]}"; do
  [ -f "$ROOT/$f" ] || bad "missing required file: $f"
done
[ "$FAIL" -eq 0 ] && ok "${#REQUIRED[@]} required files present"

SKILLS=(brand-to-system design-build design-refine design-review direction-study
        distinctiveness-review ia-review starter-directions ui-design-principles
        ui-design-review ui-design-system)
for s in "${SKILLS[@]}"; do
  [ -f "$ROOT/.claude/skills/$s/SKILL.md" ] || bad "missing skill: $s"
done
[ "$FAIL" -eq 0 ] && ok "all ${#SKILLS[@]} skills present"

if grep -RIlE 'SPDX-License-Identifier: Apache-2.0|modern-screenshot\.umd|name:[[:space:]]*(hallmark|impeccable)' "$ROOT/.claude/skills" >/dev/null 2>&1; then
  bad "retired third-party payload detected in bundled skills"
else
  ok "bundled skills contain no retired third-party payload"
fi

[ "$FAIL" -eq 0 ] || { echo; echo -e "${RED}${BLD}✘ source tree incomplete.${RST}"; exit 1; }

# ── 2 · existing checks ──────────────────────────────────────────────────────
step "2 · Harness checks"
if DH_STRICT=1 bash "$ROOT/scripts/smoke.sh"; then ok "strict smoke, load chain, payload, budget and integration"; else bad "strict smoke failed"; fi
[ "$FAIL" -eq 0 ] || { echo; echo -e "${RED}${BLD}✘ checks failed; not packaging.${RST}"; exit 1; }

# ── 3 · stage ────────────────────────────────────────────────────────────────
step "3 · Staging"
rm -rf "$DIST/.stage"
mkdir -p "$STAGE"

# Copied wholesale, minus the exclusions applied below.
for item in AGENTS.md CLAUDE.md README.md LICENSE NOTICE VERSION CONTRIBUTING.md SECURITY.md CHANGELOG.md .gitignore .github \
            docs scripts design integration .claude; do
  cp -R "$ROOT/$item" "$STAGE/"
done

# Exclusions: development and machine-specific material.
find "$STAGE" \( -name '.DS_Store' -o -name '__pycache__' -o -name '*.pyc' \
                 -o -name 'node_modules' -o -name '*.log' -o -name '.git' \
                 -o -name '*.dh-tmp.*' -o -name '*~' -o -name '*.swp' \) \
     -exec rm -rf {} + 2>/dev/null
rm -rf "$STAGE/dist"

# The scaffold ships empty: a cheat sheet with no system to summarise, and no
# product-specific brand, tokens, references, decisions or patterns.
mkdir -p "$STAGE/design/references" "$STAGE/design/patterns" "$STAGE/design/knowledge"
if [ -f "$ROOT/design/cheatsheet.md" ] && ! grep -q "No design system yet" "$STAGE/design/cheatsheet.md" 2>/dev/null; then
  bad "design/cheatsheet.md is not the empty scaffold — it carries a real system"
fi
for leak in design/DESIGN.md design/tokens.json design/BRAND.md; do
  [ -e "$STAGE/$leak" ] && bad "product-specific file would ship: $leak"
done
ok "staged $(find "$STAGE" -type f | wc -l | tr -d ' ') files"

# ── 4 · no absolute paths from this machine ──────────────────────────────────
step "4 · Machine-specific paths"
# Built at runtime so this script's own source does not match the pattern it
# searches for — otherwise packaging fails on its own grep argument.
HOMEPAT="$HOME"
USERPAT="/U""sers/"
LEAKS=$(grep -rIl -e "$HOMEPAT" -e "$USERPAT" "$STAGE" 2>/dev/null || true)
if [ -n "$LEAKS" ]; then
  bad "absolute paths from this computer appear in:"
  echo "$LEAKS" | sed "s|$STAGE|  ·|"
else
  ok "no source-machine absolute paths in textual release files"
fi

[ "$FAIL" -eq 0 ] || { echo; echo -e "${RED}${BLD}✘ staging failed.${RST}"; exit 1; }

python3 "$ROOT/scripts/check-public-content.py" "$STAGE" || { bad "public content audit failed"; exit 1; }

# ── 5 · archives ─────────────────────────────────────────────────────────────
step "5 · Archives"
cd "$DIST/.stage" || exit 1
# Deterministic-ish ordering; COPYFILE_DISABLE stops macOS tar writing ._ files.
MANIFEST="$DIST/$NAME.manifest.txt"
find "$NAME" -type f | LC_ALL=C sort > "$MANIFEST"

# Anonymous ownership avoids publishing the build machine's account identity.
python3 - "$STAGE" "$NAME" "$DIST/$NAME.tar.gz" <<'TAR'
from pathlib import Path
import sys,tarfile
def anonymous(info):
    info.uid=info.gid=0
    info.uname=info.gname=''
    for key in ['uid','gid','uname','gname']:info.pax_headers.pop(key,None)
    return info
with tarfile.open(sys.argv[3],'w:gz') as archive:
    archive.add(Path(sys.argv[1]),arcname=sys.argv[2],filter=anonymous)
TAR
rm -f "$DIST/$NAME.zip"
zip -qr "$DIST/$NAME.zip" "$NAME" -x '*.DS_Store'
cd "$ROOT" || exit 1
ok "$(basename "$DIST/$NAME.tar.gz") · $(du -h "$DIST/$NAME.tar.gz" | cut -f1 | tr -d ' ')"
ok "$(basename "$DIST/$NAME.zip") · $(du -h "$DIST/$NAME.zip" | cut -f1 | tr -d ' ')"

# ── 6 · the two archives must carry the same manifest ────────────────────────
step "6 · Manifest parity"
T_LIST=$(tar -tzf "$DIST/$NAME.tar.gz" | grep -v '/$' | LC_ALL=C sort)
Z_LIST=$(unzip -Z1 "$DIST/$NAME.zip" | grep -v '/$' | LC_ALL=C sort)
if [ "$T_LIST" = "$Z_LIST" ]; then
  ok "tar and zip carry the same $(echo "$T_LIST" | wc -l | tr -d ' ') files"
else
  bad "archive manifests differ:"; diff <(echo "$T_LIST") <(echo "$Z_LIST") | head -20
fi
if [ "$T_LIST" = "$(cat "$MANIFEST")" ]; then ok "archives match the staged manifest"
else bad "archives do not match the staged manifest"; fi

# ── 7 · checksums ────────────────────────────────────────────────────────────
step "7 · Checksums"
cd "$DIST" || exit 1
: > SHA256SUMS
for f in "$NAME.tar.gz" "$NAME.zip"; do
  if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$f" >> SHA256SUMS
  else sha256sum "$f" >> SHA256SUMS; fi
done
cd "$ROOT" || exit 1
ok "dist/SHA256SUMS"
sed 's|^|    |' "$DIST/SHA256SUMS"

python3 "$ROOT/scripts/check-public-content.py" "$DIST/$NAME.zip" "$DIST/$NAME.tar.gz" || { bad "archive content audit failed"; exit 1; }

rm -rf "$DIST/.stage"

echo
if [ "$FAIL" -eq 0 ]; then
  echo -e "${GRN}${BLD}✔ packaged $NAME.${RST}"
  exit 0
fi
echo -e "${RED}${BLD}✘ packaging completed with problems.${RST}"
exit 1
