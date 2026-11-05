# design/

The studio's durable context. Read by design tasks; survives between sessions
and between agents.

**Only `DESIGN.md` and `tokens.json` are a contract.** Normal feature work reads
them and does not edit them. Changing them is its own deliberate task, with the
reason recorded in `knowledge/decisions.md`.

| Path | Status | Holds |
|---|---|---|
| `product.md` | **Tier 1** | the product in one page — loaded every task |
| `cheatsheet.md` | **Tier 1** | the tokens you reach for constantly. **Generated** by `scripts/dh-cheatsheet.sh` — never hand-edited |
| `brief.md` | on demand | greenfield or scattered input reconciled into a bounded design brief |
| `surfaces.md` | on demand | surface jobs, direction sources, required states and reuse — not progress |
| `BRAND.md` | optional | identity, voice, personality, constraints |
| `DESIGN.md` | **contract** | principles and product-specific visual guidance |
| `tokens.json` | **contract** | the semantic values |
| `components.md` | index | name · path · variants · states · lifecycle status |
| `patterns/` | catalogue | approved compositions, each naming the anti-pattern it displaced |
| `knowledge/decisions.md` | memory | what was chosen, and what was rejected |
| `knowledge/preferences.md` | memory | standing taste calls a person has made |
| `knowledge/lessons/` | memory | dated, episodic — what happened and what it taught |
| `knowledge/debt.md` | memory | known-wrong and unfixed |
| `knowledge/upstream-feedback.md` | optional | sanitized, human-reviewed proposals for the source harness; never sent automatically |
| `references/` | examples | approved screens, reference images |

`knowledge/README.md` explains the memory types and the rule for promoting a
lesson into an always-applied rule.

**Load what the task needs.** Only `product.md` and `cheatsheet.md` are read
every time; everything else loads on demand. A file that is never read is not
context, it is furniture — create them when the product needs them.

For a new product, fill `brief.md` before asking the harness to invent missing
context. Before a page, screen, modal or flow step is built or reviewed, give it
a row in `surfaces.md`; the row defines the important states without becoming a
second delivery tracker.

## No design system yet?

Expected on a new product. `cheatsheet.md` will say so explicitly, and a production build creates or extracts the system before implementation. A direction study
uses provisional contracts and study-proof principles; it does not create a production system.
