# <PRODUCT> — Agentic Design Harness

@design/product.md
@design/cheatsheet.md

Read both before design work even if the host does not expand `@` imports. These plus this
file are Tier 1; everything else loads on demand. **Context**: these files · **Skills**:
`.claude/skills/` · **Orchestration**: study/build/review · **Evaluation**: floor + lenses ·
**Knowledge**: `design/knowledge/`.

## Workspace and execution

When this source harness is opened for a new product, run `scripts/create-project.py --name
<project-name>`: work in the returned separate sibling project, with its own working copy of the harness, pinned skills and context.
For new-product discovery, read `docs/PROJECT-START.md` in that project before choosing a direction.
An installed project has `.agentic-design-harness.json`: work there. Existing applications and
explicit destinations take precedence. Harness maintenance stays in this checkout.

Before choosing a design approach, run `python3 scripts/dh-preflight.py --root .` in an installed
project, or `python3 scripts/harness-preflight.py --root .` in this source checkout. It resolves the
local skill tree and checks its lock. Read its `design-build/references/skill-invocation.md`.
Use verified native activation when available; otherwise use **folder-execution**: select the local
SKILL.md and actually execute its procedure. `/name` below means that same verified workflow.
Reading is loaded; doing the steps is executed; finishing required scope is completed. Never
claim native invocation from a file read, or substitute a same-named global/external design skill.
Pass the same verified root to supporting reviewers. Filesystem checks cannot certify live host
activation or isolation; report missing capabilities and incomplete reviews honestly.

## Direction, systems and routing

Apply the brief, approved references, brand, systems and shipped components consistently. Direction
precedence: approved direction › system/shipped surfaces › role-assigned references › opt-in starters.
Supplied direction is never translated into a starter. Reuse before inventing another component.
Read the matching `design/surfaces.md` row; capture material context in `design/brief.md` as needed.
Ask material unresolved questions together; reuse answers and explicitly delegated professional
judgement. Record assumptions; never invent brand facts or customer evidence.

| Request | Execute |
|---|---|
| Concepts, alternatives, supplied references or help choosing | `/direction-study`; keep original references directly available to designer and builders. Ask about faithful style, loose inspiration or compatible mixing; reuse stated preferences and resolve material conflicts/imagery. Reference-led is the normal reference route; reference-directed requires an explicit close-recreation request |
| New page/screen/app or substantial rebuild after selection | `/design-build`: direction → system → implementation → render → delegated review; `/ui-design-principles` during decisions |
| Material UI, navigation or system review | `/design-review`: isolated lenses, bounded repair, fresh finish review. Focused by default; whole-product scope when warranted |
| Refinement | Read system, patterns and surface first, then `/design-refine`; read-only unless edits are authorized or unlocked by the review orchestrator |
| Brand/style guidelines or system work | `/ui-design-system` Create / Extract / Reconcile / Audit–Drift as appropriate. Compatible machine-readable brand → `/brand-to-system`; prose or absent brand → system Create |
| No visual direction | Brief-originated exploration, or opt-in `/starter-directions` when requested or direction genuinely absent and delegated; never preload its catalogue in reference-led work |

A brand is not a design system. Before production, create/extract/reconcile a system when needed;
otherwise consume it. `BRAND.md` binds identity; `DESIGN.md` and `tokens.json` bind implementation.
Feature work reads contracts and does not rewrite them; contract changes are their own task and
record their reason. Report conflicts with accessibility or strong practice. Spend the expressive
range an approved system licenses. Load full systems, components, patterns, references and detailed
rule sections only when relevant; keep a compact `design/cheatsheet.md` for ongoing work.

## Exploration and review

Studies use provisional contracts and study-proof principles, not production system creation.
Extract a provisional visual guide per source alongside the originals: colour roles/coverage, type,
layout, components and imagery. Contrasting examples may be alternatives; mix only compatible ideas
with clear roles. Preserve style while adapting content; expose constraint-driven departures.
Keep references visible; visual techniques may earn their place. Contrast, usability, legibility
and reduced-motion requirements still apply. For standalone web studies, save local HTML/CSS proofs,
an index and desktop/mobile screenshots in the project; native/existing-app/requested design files
keep their format. No design canvas, hosted artifact or publication unless requested.
Initial previews may pause at **STUDY PREVIEW — FEEDBACK REQUIRED** after builder fidelity and
legibility inspection; study-proof design guidance still applies. Full reviews remain pending.
Render and look, then run independent distinctiveness and reference-resonance reviews before
recommending. Genericness, reference influence and mechanical correctness are separate judgements.
Unreviewed or confirmed generic proofs cannot receive positive recommendations. Preserve versions
and findings when exploring further; `/direction-study` stops at **STUDY — DECISION REQUIRED**.

Production build delegates `/design-review` to a fresh context. Its required separate lenses are
`/distinctiveness-review`, `/ui-design-review`, and locked read-only `/design-refine`; add
`/ia-review` when structure is material, plus source similarity for reference work. Keep disagreement.
Review owns one bounded repair through fresh unlocked `/design-refine`, then rerenders, reruns the
complete floor against matching source evidence and obtains a fresh finish review. Existing debt
is separate; it blocks only where introduced/worsened, owned by scope, safety relevant or required.
Missing render/lens, stale evidence or unresolved material findings forbid readiness. The build
reports **DRAFT — REVIEW REQUIRED** when independent review is unavailable; only `/design-review`
may report `REVIEWED`, `READY WITH PROPOSALS` or `READY`. Never upgrade its verdict.
Review timeboxes are 8/15/30 minutes; report unassessed scope. Three attempts at a stubborn issue,
then stop. Small CSS/copy/administrative changes do not automatically trigger full review.

## Floor and memory

`scripts/dh-check.sh <file.html>` (source checkout: `scripts/check.sh`) measures web contrast,
overflow, padding, tokens, headings, semantic main and targets. It is web-only; unavailable checks
are **not verified**, never passes. Inspect actual renders and applicable states; scanners cannot
prove craft or readiness. A native screen, PDF, Figma file or image needs its appropriate checks.

Decisions → `design/knowledge/decisions.md`; taste → `preferences.md`; rejected work and why or a
mistake → judged example in `lessons/`; reusable composition → `design/patterns/`; component →
`design/components.md`; unfixed issue → `debt.md`. Routine work records nothing. Promote a lesson
into an always-applied rule only after recurrence across tasks, no better mechanical owner, and a
person's acceptance. Never self-promote. Upstream proposals stay local until a person sends them.

## Rules in force

_(No promoted lessons yet.)_
