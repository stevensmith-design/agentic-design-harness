#!/bin/bash
# cheatsheet — regenerate design/cheatsheet.md from tokens.json.
#
# The cheat sheet is Tier 1, so it is read constantly and must never disagree
# with the tokens. Generated, never hand-edited.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
T="$ROOT/design/tokens.json"
OUT="$ROOT/design/cheatsheet.md"
# The generated text must name THIS script, whatever it was installed as
# (init renames it dh-cheatsheet.sh). Derived from argv[0] so the source copy
# and the installed copy cannot drift apart.
SELF="scripts/$(basename "$0")"
# No tokens? RESET the cheat sheet. Leaving the previous contents in place
# means Tier 1 — read on every task — carries values from a product that is not
# this one. That is how a fresh install inherits another product's palette.
if [ ! -f "$T" ]; then
  cat > "$OUT" <<EMPTY
# Design system — cheat sheet

<!-- Tier 1: loaded on every task. GENERATED from design/tokens.json by
     $SELF — do not hand-edit. -->

## No design system yet

This product has no \`design/tokens.json\`, so there is nothing to summarise.

**Production establishes or consumes the system** — \`ui-design-system\` Create / Extract /
Reconcile as appropriate. A direction study uses provisional contracts instead. Read the
installed harness instructions for the current phase.

Then run \`$SELF\` to fill this file.
EMPTY
  echo "no design/tokens.json — cheat sheet reset to the empty state."
  exit 0
fi
python3 - "$T" "$OUT" "$SELF" <<'PY'
import json, sys
tok, out, self_cmd = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(tok))
def flat(o, p=''):
    r = []
    if isinstance(o, dict):
        if 'value' in o and not isinstance(o['value'], dict): return [(p, o['value'])]
        for k, v in o.items():
            if k.startswith('$'): continue
            r += flat(v, f'{p}.{k}' if p else k)
    else: r.append((p, o))
    return r
vals = flat(d)
def group(pre): return [(k.split('.', 1)[-1], v) for k, v in vals if k.startswith(pre)]
L = ['# Design system — cheat sheet', '',
     '<!-- Tier 1: loaded on every task. GENERATED from tokens.json by',
     f'     {self_cmd} — do not hand-edit. Full rules in DESIGN.md. -->', '']
for title, pre in [('Colour', 'color'), ('Space', 'space'), ('Type', 'type'), ('Radius', 'radius')]:
    g = group(pre)
    if not g: continue
    L += [f'## {title}', '']
    L += [f'- `{k}` `{v}`' for k, v in g[:14]]
    if len(g) > 14: L.append(f'- …{len(g)-14} more in `tokens.json`')
    L.append('')
L += ['## Rules broken most often', '',
      '_(the two or three prose rules from DESIGN.md that actually get violated —',
      'listed here because a rule nobody loads is a rule nobody follows)_', '']
open(out, 'w').write('\n'.join(L))
print(f'wrote {out} — {len(vals)} tokens read')
PY
