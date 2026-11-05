#!/usr/bin/env python3
"""Create a separate project with this pinned design harness; never install globally."""
import argparse,json,re,subprocess,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--name');p.add_argument('--destination',type=Path);a=p.parse_args()
 if (ROOT/'.agentic-design-harness.json').exists():p.error('This is already an installed project. Work in its project root; use source init.sh for another project.')
 if not a.name and not a.destination:p.error('provide --name or --destination')
 if a.destination:
  if not a.destination.is_absolute():p.error('--destination must be absolute')
  dest=a.destination.resolve()
 else:
  name=re.sub(r'[^a-zA-Z0-9_-]+','-',a.name.strip()).strip('-').lower()
  if not name:p.error('project name is empty')
  dest=ROOT.parent/name;n=2
  while dest.exists():dest=ROOT.parent/f'{name}-{n}';n+=1
 if dest==ROOT or ROOT in dest.parents:p.error('project output must be outside the source harness')
 if dest.exists():p.error('destination exists; use init.sh for an existing project')
 # Preflight before creating anything; stale source cannot seed a new project.
 check=subprocess.run([sys.executable,str(ROOT/'scripts/harness-preflight.py'),'--root',str(ROOT)],stdout=subprocess.PIPE,text=True)
 if check.returncode:return check.returncode
 r=subprocess.run(['bash',str(ROOT/'scripts/init.sh'),str(dest)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 if r.returncode:print(r.stdout,file=sys.stderr);return r.returncode
 # Complete independent template copy, excluding generated/private and host history.
 # The installer-created instruction views and context take precedence.
 for f in ROOT.rglob('*'):
  rel=f.relative_to(ROOT)
  if any(part in {'.git','dist','__pycache__','node_modules','.github'} for part in rel.parts) or f.name=='.DS_Store' or f.suffix=='.pyc':continue
  if not f.is_file():continue
  target=dest/rel
  if rel==Path('README.md'):target=dest/'HARNESS-README.md'
  if target.exists():continue
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
 (dest/'README.md').write_text('# '+(a.name or dest.name)+'\n\nIndependent design project with Agentic Design Harness. Start with AGENTS.md and\ndocs/agentic-design-harness/PROJECT-START.md. Product files belong here, not in the reusable source.\n')
 print(json.dumps({'project_root':str(dest),'skills_root':str(dest/'.claude/skills'),'status':'COPIED — use project_root for all subsequent work'},indent=2));return 0
if __name__=='__main__':sys.exit(main())
