# Upstream design-harness feedback

Local candidates for improving the source Design Harness and its bundled workflows.
This is not a publishing queue: nothing here may be sent, posted, or used to
change another repository without a separate explicit instruction.

Add a candidate only after a local lesson has recurred across separate tasks, a
person confirms it is about the harness rather than this product, and the local
problem is already fixed or tracked. One product-specific preference does not
belong here.

Before writing, reduce the evidence to a synthetic example. Do not open private
material to redact it. Remove names, personal data, secrets, customer or client
content, internal URLs and paths, repository or branch names, proprietary
assets, and unreleased product detail. If the lesson cannot survive that
reduction, report that it cannot safely travel upstream.

Use this shape:

```markdown
## YYYY-MM-DD · <finding>

Source: <confirmed harness file or bundled workflow, or unresolved>
Evidence: <recurrence count and dates; no product identifiers>
Observed failure: <what the harness allowed or failed to reveal>
Why it generalises: <why unrelated products could encounter it>
Synthetic reproduction: <invented inputs only>
Proposed owner: <skill, fixture, check, system, or documentation>
Smallest change: <proposal, including what must remain unchanged>
Verification: <one failure case and one clean case where deterministic>
Disclosure review: pending | cleared by a person on YYYY-MM-DD
```

`cleared` means the local draft was reviewed for disclosure. It is not
authorization to transmit it.
