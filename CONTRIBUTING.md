# Contributing

Maintain this as a reusable source template. Do not add a real product, brand assets, project memory,
private paths, credentials or generated screenshots here. New products use scripts/create-project.py
and work in their independent copy; existing products use the additive installer.

The eleven skill directories in `.claude/skills/` are this package's bundled design workflows. Edit
them here, then regenerate the lock with `python3 scripts/gen-lock.py` and run the checks below.
Preserve the accepted creative baseline. A project-specific issue is not automatically another
universal aesthetic rule. `docs/harness-package.json` declares the helpers and workspace rules the
workflows resolve; keep it in step with the scripts it names.

For installation/checker changes, first add a fixture demonstrating the failure and a case that must
remain valid. Use Python 3.9+, Node.js 22+, Bash and a local Chromium browser. Run:

    bash scripts/check-skill-sync.sh
    DH_STRICT=1 bash scripts/smoke.sh

Smoke covers real installations, preservation of existing project files, explicit host routes,
relocation, independent copies and deliberately passing/failing rendered floor fixtures. No browser
means not verified, not a release pass. Deterministic tests do not certify live native activation,
truthful model execution or visual quality.

Prepare local public downloads with bash scripts/package.sh. It includes the same tests, docs,
licence, complete skill payload and checksums; it never publishes remotely. Keep dist/ out of source
control. Document the version and actual validation limits in each release.

Before publication, review all prose, inline comments, fixtures, filenames and links for private
client/project context. Use neutral calibration examples and generic paths. Run
`python3 scripts/check-public-content.py <publication-tree-or-archive>` on the actual public tree
and rebuilt downloads. The checker traverses hidden folders, nested archives and archive comments/metadata; it detects known
private labels/lineage and personal checkout paths, not every possible client name or secret.
Regression fixtures construct rejected labels in memory so the tests do not redistribute them.
