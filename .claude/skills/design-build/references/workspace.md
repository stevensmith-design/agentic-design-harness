# Choose the project workspace before writing project files

Use an explicit project/output destination when the person supplies one. Work in an existing
application's root for additions, reviews and refinements. Harness maintenance, examples or tests
explicitly requested inside the source harness remain scoped harness work.

Resolve the helpers from the package configuration before acting. It is `docs/harness-package.json`
in a source harness checkout and `docs/agentic-design-harness/harness-package.json` in an installed
project. The context is **installed** when `.agentic-design-harness.json` exists at the root, and
**source** otherwise. Use the commands that configuration lists for the current context; do not
substitute helpers from any other package or location.

**Installed project.** The project root is the workspace. Do not create another project from it.
Its `.agentic-design-harness.json` names the skills path and instruction file. Verify the payload
with `python3 scripts/dh-preflight.py --root .` and check web pages with `scripts/dh-check.sh`.

**Source harness, new page/app/product.** Create a separate project instead of building in the
source checkout. Pick a descriptive name from the brief and announce the resulting path:

    python3 scripts/create-project.py --name <project-name>

For a supplied new destination, use `--destination /absolute/new/project` instead. The helper
preflights the source payload, creates an independent working copy with its own pinned skills,
lock and design context, defaults beside the source checkout, adds a numeric suffix for an existing
name and never overwrites another project. Use the returned `project_root` as the working
directory for subsequent file/build/render tools (creating a folder does not change the caller's
working directory) and the returned `skills_root` for workflow handoffs.

**Source harness, existing application.** Add the harness to that application rather than
creating a project: `bash scripts/init.sh /absolute/path/to/existing-project`. Installation is
additive; it preserves existing files and reports collisions and integration lines to reconcile.
Afterwards the application is an installed project.

A host-managed plugin/cache is not a projects directory: use the host's real project workspace or
an explicit accessible destination. If the host cannot write outside the selected folder, ask for
access or a project location instead of silently building inside the source harness. Keep app
files, assets, proofs, renders and BRAND.md / DESIGN.md / tokens.json in the project. Keep the
pinned skills out of application compilation/test discovery and deployed assets, while retaining
them in project version control. For a scaffolder requiring an empty directory, stage the
application separately and merge its files without replacing the skills or agent contexts.
