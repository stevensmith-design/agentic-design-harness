# Surface and state map

The compact design contract for what exists or is deliberately planned. It is
not a roadmap, progress tracker, or second component index.

Add one row when a surface is real enough to design. Read the matching row
before building or reviewing it. If implementation and this map disagree,
report the drift; do not silently rewrite either side during feature work.

| Surface | Entry / path | User job | Direction source | Required states | Reuses |
|---|---|---|---|---|---|
| _(none yet)_ | | | | | |

**Surface** is a page, screen, modal, flow step, document type, or other
composition with a distinct user job—not every route alias.

**Direction source** names the approved direction, established system/shipped
surface, or bounded reference role. “Make it modern” is not a source.

**Required states** names only states that can occur, but does not omit awkward
ones: default · long content · many items · empty · loading · error · success ·
permission/role · disabled · destructive confirmation · offline. A state not
listed and not rendered was not assessed.

**Reuses** names existing components or patterns that should prevent a parallel
implementation. Use `components.md` and `patterns/` as the detailed indexes.
