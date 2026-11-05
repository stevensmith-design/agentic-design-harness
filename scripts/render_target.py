#!/usr/bin/env python3
"""Resolve what actually gets rendered, and refuse to guess.

`dh measure` passed the ARTIFACT path straight to Chrome. For a directory
artifact — the normal shape for a page with assets — Chrome rendered its
DIRECTORY LISTING and the harness stored the result as a passing measurement.
The recorded evidence read "10 text nodes clean"; the real page has 58. The
rendered lane exists to stop exactly that kind of false green, and it produced
one.

Two rules:

  1. A directory resolves to index.html only when that choice is UNAMBIGUOUS —
     one such file, at the top level. Two candidates is a question for a
     person, not a coin toss.
  2. Anything else is `unmeasurable`. Never a pass: a page nobody rendered is
     not a page that rendered clean.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERABLE = {".html", ".htm"}


def within_scope(entry: Path, artifact: str) -> bool:
    """Is this entrypoint inside the artifact being rendered?

    ENTRYPOINT accepted any readable path, including an absolute one outside
    the repository. A clean sibling file could be measured while the result
    named the artifact under review — measuring one thing and crediting
    another is the same class of defect as rendering a directory listing.
    """
    try:
        entry = entry.resolve()
        scope = (ROOT / artifact).resolve()
    except (OSError, ValueError):
        return False
    if scope.is_file():
        return entry == scope
    return scope in entry.parents


def resolve(artifact: str) -> tuple[str, str]:
    """Return (entrypoint, problem). Exactly one is non-empty."""
    if not artifact:
        return "", "no artifact named"

    p = ROOT / artifact
    if not p.exists():
        return "", f"{artifact} does not exist"

    if p.is_file():
        if p.suffix.lower() not in RENDERABLE:
            return "", (f"{artifact} is not a renderable document "
                        f"({p.suffix or 'no extension'})")
        return str(p.relative_to(ROOT)), ""

    top = sorted(f for f in p.iterdir() if f.is_file() and f.suffix.lower() in RENDERABLE)
    if not top:
        nested = sorted(f for f in p.rglob("*")
                        if f.is_file() and f.suffix.lower() in RENDERABLE)
        if not nested:
            return "", f"{artifact} contains no renderable document"
        return "", (f"{artifact} has no top-level entrypoint; "
                    f"{len(nested)} nested candidate(s). Name one: "
                    f"ENTRYPOINT={nested[0].relative_to(ROOT)}")

    if len(top) == 1:
        return str(top[0].relative_to(ROOT)), ""

    named = [f for f in top if f.stem.lower() == "index"]
    if len(named) == 1:
        return str(named[0].relative_to(ROOT)), ""

    names = ", ".join(f.name for f in top[:4])
    return "", (f"{artifact} has {len(top)} renderable documents ({names}) and no "
                "single index. Which one is the page? Name it: ENTRYPOINT=<path>")


def resolve_override(override: str, artifact: str) -> tuple[str, str]:
    """Validate an explicit ENTRYPOINT: canonicalised, in scope, renderable."""
    p = (ROOT / override) if not Path(override).is_absolute() else Path(override)
    try:
        p = p.resolve()
    except (OSError, ValueError):
        return "", f"ENTRYPOINT={override} cannot be resolved"
    if not p.is_file():
        return "", f"ENTRYPOINT={override} does not exist"
    if p.suffix.lower() not in RENDERABLE:
        return "", f"ENTRYPOINT={override} is not a renderable document"
    if not within_scope(p, artifact):
        return "", (f"ENTRYPOINT={override} is outside the active artifact "
                    f"({artifact}). Evidence is credited to the artifact, so the "
                    "entrypoint must be inside it.")
    try:
        return str(p.relative_to(ROOT)), ""
    except ValueError:
        return "", f"ENTRYPOINT={override} is outside the repository"


def main() -> int:
    import os
    artifact = sys.argv[1] if len(sys.argv) > 1 else ""
    override = os.environ.get("ENTRYPOINT", "").strip()
    if override:
        entry, problem = resolve_override(override, artifact)
        if problem:
            print(f"render target: {problem}", file=sys.stderr)
            return 1
        print(entry)
        return 0
    entry, problem = resolve(artifact)
    if problem:
        print(f"render target: {problem}", file=sys.stderr)
        return 1
    print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
