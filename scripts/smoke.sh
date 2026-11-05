#!/usr/bin/env bash
# Validate the harness's real wiring plus the retained failing floor fixtures.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SK="$ROOT/.claude/skills"
GRN=$'\033[0;32m'; RED=$'\033[0;31m'; YEL=$'\033[1;33m'; BLD=$'\033[1m'; RST=$'\033[0m'
FAIL=0; NV=0
ok(){ echo "  ✔ $1"; }
no(){ echo "  ✘ $1"; FAIL=$((FAIL+1)); }
nv(){ echo "  ? $1 — NOT VERIFIED"; NV=$((NV+1)); }
echo "Agentic Design Harness · smoke"
for check in check-skill-sync host-check budget; do
 if bash "$ROOT/scripts/$check.sh"; then ok "$check"; else no "$check"; fi
done
if python3 "$ROOT/scripts/tests/wiring.py"; then ok "installation and workspace integration"; else no "installation and workspace integration"; fi
if python3 "$ROOT/scripts/tests/release-regressions.py"; then ok "release regressions and non-destructive lifecycle"; else no "release regressions"; fi
if python3 "$ROOT/scripts/tests/contracts.py"; then ok "bundled workflow contracts"; else no "bundled workflow contracts"; fi
if python3 "$ROOT/scripts/tests/content-audit/run.py"; then ok "public content/privacy fixtures"; else no "public content/privacy fixtures"; fi
# 20 · the floor has been observed failing — one fixture per check
#
# This used to assert only that scripts/check.sh was executable. A check nobody
# has watched fail is a check with no evidence behind it, and this one hides
# four rendered measurements and a text scan behind a single exit code.
#
# Writing these fixtures found the text scan failing CORRECT work: the token
# filter was line-oriented, so a `:root{--a:#111;--b:#fff}` written on one line
# reported every token it declared as a raw colour leak. floor-tokens-oneline
# is that case, kept passing.
#
# Each rigged fixture is the clean one with a single defect, so a red line names
# one check. The assertion is the LINE, not the exit code: one exit code cannot
# say which of five checks spoke.
[ -x "$ROOT/scripts/check.sh" ] && ok "floor check is executable" || no "scripts/check.sh not executable"
grep -q "mainCount === 1" "$ROOT/scripts/measure/structure.mjs" \
  || no "structure floor no longer requires exactly one semantic main"
! grep -q "landmarks.length === 4" "$ROOT/scripts/measure/structure.mjs" \
  || no "structure floor still requires footer/header/nav on every screen"
grep -q "below 24px without spacing exception" "$ROOT/scripts/measure/structure.mjs" \
  || no "target-size floor is not calibrated to WCAG 2.2 AA"
grep -q "preferred 44px" "$ROOT/scripts/measure/structure.mjs" \
  || no "44px touch guidance is no longer reported as advisory"

FIX="$ROOT/scripts/fixtures"
floor_out(){ ( cd "$ROOT" && bash "$ROOT/scripts/check.sh" "$FIX/$1.html" 2>&1 ); }

# Probe the shared renderer once before asking check.sh to perform all seven
# rendered measurements. Without this, an unavailable browser consumed seven
# identical 10-second timeouts before the suite could say what it already knew.
_probe=$(node "$SK/ui-design-review/scripts/measure-contrast.mjs" "$FIX/floor-clean.html" --width 1280 2>&1)
if ! grep -qE '✔|✘|no text nodes matched' <<<"$_probe"; then
  RENDERS=0
  # Carry the renderer's OWN reason through, rather than naming a cause. This
  # branch fires for ANY unmeasurable render — a missing browser, a browser that
  # will not launch, a CDP timeout, a crashed probe — and the first version said
  # "no headless Chrome", which sends someone to install a browser they already
  # have. check.sh prints the reason; the suite quotes it instead of guessing.
  RENDER_WHY=$(grep -oE '(measure-[a-z]+|structure): .*' <<<"$_probe" | head -1)
  [ -n "$RENDER_WHY" ] || RENDER_WHY=$(sed 's/^[[:space:]]*//' <<<"$_probe" | grep -e . | head -1)
  [ -n "$RENDER_WHY" ] || RENDER_WHY="scripts/check.sh reported no reason"
  nv "the floor's four rendered checks — renderer unavailable: $RENDER_WHY"
else
  RENDERS=1
  _clean=$(floor_out floor-clean); _clean_rc=$?
  [ "$_clean_rc" -eq 0 ] && ok "the floor passes a clean fixture" \
    || no "the floor FAILS scripts/fixtures/floor-clean.html — it rejects work it should admit"
fi

# fixture · the line that must appear · whether it needs a renderer
floor_case(){
  local fixture="$1" pattern="$2" needs_render="$3" label="$4"
  if [ "$needs_render" = "1" ] && [ "$RENDERS" != "1" ]; then
    nv "floor: $label (renderer unavailable)"; return
  fi
  if [ "$needs_render" = "1" ]; then
    case_out=$(floor_out "$fixture")
  else
    case_out=$(cd "$ROOT" && bash "$ROOT/scripts/check.sh" --static-only "$FIX/$fixture.html" 2>&1)
  fi
  if grep -qE "$pattern" <<<"$case_out"; then ok "floor: $label"
  else no "floor: $label — scripts/fixtures/$fixture.html did not produce it"; fi
}

floor_case floor-contrast       '✘.*contrast'                  1 "contrast rejects text below the ratio"
floor_case floor-overflow       '✘.*overflow @320'             1 "overflow rejects a block wider than the viewport"
floor_case floor-padding        '✘.*padding drifts'            1 "padding rejects a container that loses it at render"
floor_case floor-structure      '✘.*exactly one h1'            1 "structure rejects a second h1"
floor_case floor-raw-colour     '✘.*raw colour outside'        0 "tokens reject a literal colour below :root"
floor_case floor-tokens-oneline '✔.*no raw colour below'       0 "tokens accept a :root block written on one line"

echo
if [ "$FAIL" -ne 0 ]; then
  echo "${RED}${BLD}✘ $FAIL problem(s).${RST}"; exit 1
fi
if [ "$NV" -ne 0 ]; then
  if [ -n "${DH_STRICT:-}${CI:-}" ]; then
    echo "${RED}${BLD}✘ $NV check(s) NOT VERIFIED.${RST} Strict mode does not accept an unmeasured check."
    exit 1
  fi
  echo "${YEL}${BLD}? smoke ran, $NV check(s) NOT VERIFIED.${RST} The reason each one could"
  echo "  not run is printed above — read it before assuming a browser is missing. Do not"
  echo "  report the floor as proven until they have run; DH_STRICT=1 makes this a failure."
  exit 0
fi
echo "${GRN}${BLD}✔ smoke clean.${RST}"; exit 0
