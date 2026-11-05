#!/usr/bin/env python3
"""Verify/discover this harness's local skill payload; never certify live activation."""
import argparse,hashlib,json,sys
from pathlib import Path

def inspect(root):
 root=root.resolve();marker=root/'.agentic-design-harness.json'
 config=json.loads(marker.read_text()) if marker.exists() else {}
 rel=config.get('skills_path','.claude/skills')
 if rel not in ('.claude/skills','.agents/skills'):raise ValueError('unsupported local skills_path')
 lock_path=root/('docs/agentic-design-harness/skills-lock.json' if marker.exists() else 'docs/skills-lock.json')
 lock=json.loads(lock_path.read_text());skills=root/rel
 expected={f'{name}/{p}':sha for name,record in lock['skills'].items() for p,sha in record['files'].items()}
 actual={str(p.relative_to(skills)):hashlib.sha256(p.read_bytes()).hexdigest() for p in skills.rglob('*') if p.is_file() and p.suffix!='.pyc' and '__pycache__' not in p.parts and p.name!='.DS_Store'}
 errors=[]
 if not skills.resolve().is_relative_to(root):errors.append('skill tree resolves outside this project')
 for path in expected:
  item=skills/path
  if item.is_symlink() or not item.resolve().is_relative_to(root):errors.append('external or linked pinned file: '+path)
 # Unrelated project skills may coexist, but the pinned eleven must match exactly.
 owned=set(lock['skills'])
 for path,sha in expected.items():
  if actual.get(path)!=sha:errors.append('missing or changed: '+str(Path(rel)/path))
 for path in actual.keys()-expected.keys():
  if path.split('/')[0] in owned:errors.append('unexpected in pinned skill: '+path)
 if len(owned)!=11:errors.append('expected eleven pinned design workflows')
 if errors:raise ValueError('\n'.join(errors[:30]))
 return {'root':str(root),'skills_path':rel,'skills':{name:str(skills/name/'SKILL.md') for name in sorted(owned)},'payload':'CLEAN','native_activation':'NOT VERIFIED','host_isolation':'NOT VERIFIED'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--skill-path',action='store_true');p.add_argument('--json',action='store_true');a=p.parse_args()
 try:r=inspect(a.root)
 except (OSError,ValueError,KeyError) as e:print('INVALID LOCAL HARNESS: '+str(e),file=sys.stderr);return 1
 if a.skill_path:print(r['skills_path'])
 elif a.json:print(json.dumps(r,indent=2))
 else:
  print('CLEAN: eleven pinned local workflows — '+r['skills_path'])
  for name,path in r['skills'].items():print('  '+name+': '+path)
  print('Filesystem verification only; native activation and host isolation are NOT VERIFIED.')
 return 0
if __name__=='__main__':sys.exit(main())
