# Approved patterns

Recurring compositions that have been used and are endorsed for reuse — with a
canonical example, and the anti-pattern each one displaced.

**Not generic layout examples.** A pattern earns a place here by having been
built for *this* product and having worked. A three-column feature grid copied
from a template is not a pattern, it is a default.

One file per pattern: `patterns/<slug>.md`.

```markdown
---
name: <pattern name>
status: current | provisional | deprecated
---

**Use when:** the situation it answers.
**Canonical example:** path, and the screen it is on.
**Instead of:** the anti-pattern it displaced, and why that one failed here.
**Do not:** the misuse worth naming.
```

An empty catalogue is the correct state for a new product. Patterns are
harvested from work that happened, never written in advance.
