#!/usr/bin/env python3
"""Pin cross-skill integration instructions; this is a static guard, not a model eval.

Checks this package's own entry instructions and bundled skills. Works in a source harness checkout
and in an installed project (skills under .claude/skills or .agents/skills).
"""
from pathlib import Path
import json
import sys

here = Path(__file__).resolve()
root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else here.parents[4]
skills_dir = here.parents[2] if len(sys.argv) <= 1 else None
marker = root / '.agentic-design-harness.json'
settings = json.loads(marker.read_text()) if marker.is_file() else {}
if skills_dir is None:
    rel = settings.get('skills_path', '.claude/skills')
    skills_dir = root / rel
entry = root / settings.get('instruction_file', 'AGENTS.md')

requirements = {
    entry: ['folder-execution', 'Never claim native invocation from a file read',
            'design-build/references/skill-invocation.md', '/direction-study', '/design-review'],
    skills_dir / 'direction-study/SKILL.md': ['invoke packaged `/ui-design-principles`', 'args: "study-proof"',
        'relevant detailed `rules.md` sections', 'invoke packaged `/distinctiveness-review`',
        'every rendered proof', 'no positive recommendation', 'IA conditional',
        'rejecting every direction and requesting a rerun', 'this package supplies no plugin'],
    skills_dir / 'ui-design-principles/SKILL.md': ['## Study-proof mode', 'instead of production Steps 1 and 1.5',
        'IA Mode 3 is conditional', 'An index-only read does not complete this skill'],
    skills_dir / 'distinctiveness-review/SKILL.md': ['## Direction-study handoff', '## 1 · Look before machine evidence',
        'After that first-pass judgement', 'blocks positive recommendation'],
    skills_dir / 'design-build/SKILL.md': ['references/skill-invocation.md'],
    skills_dir / 'design-review/SKILL.md': ['references/skill-invocation.md'],
    skills_dir / 'design-build/references/workspace.md': ['harness-package.json',
        'Do not create another project from it', 'scripts/create-project.py --name', 'scripts/init.sh'],
}
failures = []
for path, phrases in requirements.items():
    if not path.is_file():
        failures.append(f'{path}: missing')
        continue
    text = ' '.join(path.read_text().split()).lower()
    for phrase in phrases:
        if ' '.join(phrase.split()).lower() not in text:
            failures.append(f'{path.name}: missing integration: {phrase}')
for failure in failures:
    print('FAIL', failure)
raise SystemExit(bool(failures))
