#!/usr/bin/env python3
"""Regenerate docs/skills-lock.json from the bundled skills in .claude/skills.

Per-file SHA-256 plus a per-skill rollup. Run after any intentional skill edit, then re-run
scripts/check-skill-sync.sh and DH_STRICT=1 scripts/smoke.sh. Writes only the lock file.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / '.claude/skills'
LOCK = ROOT / 'docs/skills-lock.json'


def included(path):
    return (path.is_file() and path.name != '.DS_Store' and path.suffix != '.pyc'
            and '__pycache__' not in path.parts)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    skills = {}
    for skill in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        files = sorted((p for p in skill.rglob('*') if included(p)),
                       key=lambda p: str(p.relative_to(SKILLS)))
        hashes = {str(p.relative_to(skill)): sha(p) for p in files}
        listing = ''.join(f'{hashes[str(p.relative_to(skill))]}  {p.relative_to(SKILLS)}\n' for p in files)
        skills[skill.name] = {'fileCount': len(files),
                              'rollup': hashlib.sha256(listing.encode()).hexdigest(),
                              'files': hashes}
    return skills


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='report drift; write nothing')
    args = parser.parse_args()
    skills = build()
    if args.check:
        current = json.loads(LOCK.read_text()).get('skills', {})
        drift = sorted(set(current) ^ set(skills) |
                       {n for n in set(current) & set(skills) if current[n]['files'] != skills[n]['files']})
        print('CLEAN: lock matches bundled skills' if not drift else 'DRIFT: ' + ', '.join(drift))
        return 1 if drift else 0
    lock = {'version': 2,
            'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'provenance': 'SHA-256 snapshot of the bundled Agentic Design Harness workflows',
            'skills': skills}
    LOCK.write_text(json.dumps(lock, indent=2) + '\n')
    print(f'wrote {LOCK.relative_to(ROOT)} ({len(skills)} skills)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
