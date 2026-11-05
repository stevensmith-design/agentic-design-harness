# knowledge/

Four kinds of memory, kept apart because they answer different questions and
decay at different rates. Collapsing them is how a harness ends up applying a
one-off incident as a permanent rule.

| File | Memory type | Answers | Changes when |
|---|---|---|---|
| `../DESIGN.md`, `../tokens.json`, `../components.md`, `../patterns/` | **semantic** | what is true of the product *now* | the product changes |
| `decisions.md` | semantic | what we chose, and what we rejected | a decision is made |
| `preferences.md` | semantic | what a person wants, regardless of reason | a person says so |
| `lessons/` | **episodic** | what happened on a date and what it taught · work a person rejected, with their reason | something goes wrong, or a person rejects something |
| `debt.md` | semantic | what we know is wrong and have not fixed | debt is taken on or paid |
| `../../AGENTS.md` | **procedural** | how agents must work here | a lesson is promoted (see below) |

Working memory — the current task's state — is the session. It is not written
here.

`upstream-feedback.md` is deliberately outside those memory types. It is an
optional, sanitized proposal queue for a lesson a person confirms belongs in
the source harness or its bundled workflows, not a new product fact or rule. A cleared local
draft still requires separate explicit authorization before it is transmitted.

## Lessons and judged examples

One file per lesson: `lessons/YYYY-MM-DD-slug.md`. Two things land here, and the
second is the one a design harness cannot do without.

**A mistake** — something went wrong and taught something.

**A judged example** — work a person rejected, *with the reason they gave*. This
is the half most design harnesses never collect, because `preferences.md` will
accept a taste call with no justification and `patterns/` only ever records what
was approved. Neither leaves a rejection anywhere. A domain whose standard is
judgement, storing only its approvals, is storing adjectives.

Write the reason in the person's words, not a tidied paraphrase: *"the hover
makes it look disabled"* teaches the next screen something; *"felt off"* does
not. A screenshot path belongs in the file where one exists — an example nobody
can look at is an assertion.

Enough of them that say the same thing is a rule candidate, and that is how the
ladder below starts moving in a domain with nothing mechanical to measure.

```markdown
---
date: YYYY-MM-DD
tags: [contrast, responsive, ...]
rule_candidate: false      # true once it has recurred
rule_ref:                  # set when promoted, e.g. R_2026_09_15_render_at_320
---

**What happened.** The observable thing.
**Why.** The cause, if known. "Not known" is a legitimate answer.
**What to do differently.** One sentence, actionable.
**Recurrence.** Dates this has now happened. One date is an anecdote.
```

## Promotion — a lesson becoming a rule

A lesson is episodic: it describes one day. A rule in `AGENTS.md` applies to
**every** task forever, and every rule there is paid for on every future task.

**Three conditions, all required:**

1. **It recurred.** The same lesson has happened on two or more separate tasks,
   and the dates are listed under Recurrence. One occurrence is an anecdote.
2. **No more mechanical owner can hold it.** Work down this ladder and stop at
   the first rung that can carry the lesson — a rule is the bottom rung, not the
   default one:

   | Rung | Where it lives | What it costs |
   |---|---|---|
   | **a fixture** | `scripts/fixtures/` + a case in `scripts/smoke.sh` | nothing per task — it runs when the suite runs |
   | **a check** | `scripts/check.sh` | one measurement, on the artifacts checked |
   | **the system** | `DESIGN.md`, `tokens.json`, `components.md`, `patterns/` | read on demand, by the tasks it applies to |
   | **a rule** | `AGENTS.md` § Rules in force | every task, forever, whether or not it applies |

   A lesson a fixture can hold has been held: the fixture fails the moment the
   lesson is forgotten, which is more than a sentence in a rulebook can claim.
3. **A person accepted the promotion.** Not the agent. Ask; do not self-promote.

When all three hold: add the rule to `AGENTS.md` § Rules in force with an
`R_<date>_<slug>` id, and set `rule_ref` in the lesson. The lesson stays — it is
the evidence.

**Why the bar is high.** An always-applied rule costs context on every task
forever. A harness that promotes on first occurrence accretes rules until the
guidance outweighs the work — which is the documented failure of the previous
version of this harness.
