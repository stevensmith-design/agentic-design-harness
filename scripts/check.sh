#!/bin/bash
# check — the rendered floor, in one command.
#
# Not a gate programme. Five objective things that are cheap to measure and
# expensive to ship wrong: contrast, overflow at the narrow widths, declared
# padding surviving render, token integrity, and heading/landmark structure.
#
# Everything else about a design is a judgement, and judgements belong to the
# review skills, not to this file.
#
# WEB ONLY. Every check here renders HTML in a headless browser or reads a
# <style> block. A native mobile screen, a PDF, a Figma frame or an exported
# image has no floor result from this script at all — which is *not verified*,
# never a pass, and never a reason to call the floor green for that artifact.
#
# Usage: scripts/check.sh [--static-only] <file.html> [more.html ...]
# Exit:  0 all clear · 1 a floor check failed · 3 not verified (something
#        could not be measured) · 2 bad usage

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SKILLS_PATH=$(python3 "$ROOT/scripts/dh-preflight.py" --root "$ROOT" --skill-path 2>/dev/null) ||
  SKILLS_PATH=$(python3 "$ROOT/scripts/harness-preflight.py" --root "$ROOT" --skill-path) || exit 3
SKILLS_ROOT="$ROOT/$SKILLS_PATH"
RED=$'\033[0;31m'; GRN=$'\033[0;32m'; YEL=$'\033[1;33m'; BLD=$'\033[1m'; RST=$'\033[0m'

STATIC_ONLY=0
if [ "${1:-}" = "--static-only" ]; then STATIC_ONLY=1; shift; fi
[ $# -ge 1 ] || { echo "usage: scripts/check.sh [--static-only] <file.html>"; exit 2; }
FAIL=0
UNMEASURED=0

for TARGET in "$@"; do
  [ -f "$TARGET" ] || { echo "${RED}✘${RST} no such file: $TARGET"; exit 2; }
  echo "${BLD}rendered floor${RST}  ·  $TARGET"

  if [ "$STATIC_ONLY" = 0 ]; then
  # 1 · contrast, composited — the bundled ui-design-review primitive
  out=$(node "$SKILLS_ROOT/ui-design-review/scripts/measure-contrast.mjs" "$TARGET" --width 1280 2>&1)
  if grep -q "✔" <<<"$out"; then
    echo "  ${GRN}✔${RST} contrast $(grep -o '[0-9]* text node.*' <<<"$out" | head -1)"
  elif grep -q "no text nodes matched" <<<"$out"; then
    echo "  ${YEL}?${RST} contrast UNMEASURABLE — no text nodes matched (selector-based)"
    UNMEASURED=1
  elif ! grep -q "✘" <<<"$out"; then
    echo "  ${YEL}?${RST} contrast UNMEASURABLE — the renderer produced no verdict"
    sed 's/^/      /' <<<"$out" | head -3
    UNMEASURED=1
  else
    echo "  ${RED}✘${RST} contrast"; sed 's/^/      /' <<<"$out" | grep -E "✘|needs" | head -8
    FAIL=1
  fi

  # 2 · overflow at the widths a phone actually uses
  for w in 320 375 414 768; do
    out=$(node "$ROOT/scripts/measure/measure-overflow.mjs" "$TARGET" --width "$w" 2>&1)
    if grep -q "OK document" <<<"$out"; then
      echo "  ${GRN}✔${RST} no overflow @${w}"
    elif grep -q "FAIL document" <<<"$out"; then
      echo "  ${RED}✘${RST} overflow @${w}"
      grep -E "FAIL document|past the right edge" <<<"$out" | sed 's/^/     /' | head -5
      FAIL=1
    else
      echo "  ${YEL}?${RST} overflow @${w} UNMEASURABLE — the renderer returned no verdict"
      sed 's/^/      /' <<<"$out" | head -3
      UNMEASURED=1
    fi
  done

  # 3 · declared padding survives render
  out=$(node "$SKILLS_ROOT/ui-design-review/scripts/measure-padding.mjs" "$TARGET" --width 1280 2>&1)
  if grep -qE "✔|OK" <<<"$out"; then echo "  ${GRN}✔${RST} declared padding survives render"
  elif grep -qE "✘|FAIL" <<<"$out"; then echo "  ${RED}✘${RST} padding drifts at render"; FAIL=1
  else echo "  ${YEL}?${RST} padding UNMEASURABLE — no measurable container"; UNMEASURED=1; fi
  fi

  # 4 · token integrity — no raw colour below :root
  # Strip CSS comments FIRST. A theme stamp in a comment is not a declaration,
  # and a presence check that counts comments reports defects that aren't there.
  # (This exact bug has been shipped repeatedly across this project's tooling.)
  #
  # Then remove the custom-property DECLARATIONS, not the lines they sit on.
  # The line-oriented filter this replaces dropped a line only when it BEGAN
  # with `--name:`, so a `:root{--a:#111;--b:#fff}` written on one line — which
  # is what a minifier and plenty of hand-written files produce — reported every
  # token it declared as a raw colour leak. The floor failed correct work, which
  # is the more expensive direction for a floor to be wrong in.
  # scripts/fixtures/floor-tokens-oneline.html is that case, kept passing.
  raw=$(sed -n '/<style/,/<\/style>/p' "$TARGET" \
        | perl -0777 -pe 's{/\*.*?\*/}{}gs' \
        | perl -0777 -pe 's/--[A-Za-z0-9_-]+\s*:[^;}]*//g' \
        | grep -oE '(#[0-9a-fA-F]{3,8}\b|\brgba?\([^)]*\)|\boklch\([^)]*\))' \
        | grep -vE '^rgba?\(0, ?0, ?0, ?0\)$' | sort -u)
  if [ -z "$raw" ]; then echo "  ${GRN}✔${RST} no raw colour below :root"
  else
    echo "  ${RED}✘${RST} raw colour outside the token layer:"
    sed 's/^/        /' <<<"$raw" | head -6; FAIL=1
  fi

  if [ "$STATIC_ONLY" = 0 ]; then
  # 5 · structure: one h1, landmarks, no skipped levels
  # A crashed measurement must say so. Swallowing the error and printing
  # nothing let a broken renderer pass as clean — silence read as success.
  if out=$(node "$ROOT/scripts/measure/structure.mjs" "$TARGET" 2>&1); then
    echo "$out" | sed 's/^/  /'
    grep -q "✘" <<<"$out" && FAIL=1
  else
    echo "  ${YEL}?${RST} structure UNMEASURABLE — the measurement did not complete"
    sed 's/^/      /' <<<"$out" | head -4
    UNMEASURED=1
  fi
  fi
  echo
done

if [ "$FAIL" -ne 0 ]; then
  echo "${RED}${BLD}✘ the floor is broken above.${RST} Repair, then re-run on the changed areas."
  exit 1
fi
if [ "$UNMEASURED" -ne 0 ]; then
  echo "${YEL}${BLD}? the floor is NOT verified.${RST} Something above could not be measured."
  echo "  An unmeasured check is not a passing one. Fix the renderer, or say plainly"
  echo "  in your report which checks were not run — never infer and report as looked at."
  exit 3
fi
echo "${GRN}${BLD}✔ floor holds.${RST} Judgement is the review skills' job, not this script's."
exit 0
