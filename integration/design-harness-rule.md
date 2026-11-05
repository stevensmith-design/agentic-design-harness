---
name: agentic-design-harness
description: Routes UI and design-system work into the installed Design Harness without making its full instructions always-loaded.
paths: ["public/**", "src/**", "app/**", "design/**", "DESIGN.md", "tokens.json"]
trigger: glob
---

# Design Harness router

Before UI, visual-system, component, layout, or design-review work, read
`design/agentic-design-harness/HARNESS.md`. It owns direction, system creation/extraction, building,
rendering, and fresh-context review for these paths.

The engineering harness remains canonical for repository workflow, security,
testing, and delivery. Where the two overlap, use the stricter requirement and
record an actual policy conflict instead of silently choosing one.
