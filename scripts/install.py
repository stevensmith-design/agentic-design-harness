#!/usr/bin/env python3
"""Add the pinned design harness to a project without replacing its existing context."""
import argparse,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
 if (ROOT/'.agentic-design-harness.json').exists():
  print('Use the clean source harness to install into another project; this is a project working copy.',file=sys.stderr);return 2
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--path-scoped',action='store_true');p.add_argument('target',type=Path);a=p.parse_args()
 target=a.target.resolve()
 if target==ROOT or ROOT in target.parents:p.error('refusing to install into the source harness')
 check=subprocess.run([sys.executable,str(ROOT/'scripts/harness-preflight.py'),'--root',str(ROOT)],stdout=subprocess.PIPE,text=True)
 if check.returncode:print(check.stdout);return check.returncode
 target.mkdir(parents=True,exist_ok=True)
 marker=target/'.agentic-design-harness.json'
 old=json.loads(marker.read_text()) if marker.is_file() and not marker.is_symlink() else {}
 scoped=a.path_scoped or old.get('skills_path')=='.agents/skills' or any((target/n).exists() for n in ['.agents','harness.config.yaml','AGENTS.md','CLAUDE.md']) and not old
 skills='.agents/skills' if scoped else '.claude/skills'
 entry=old.get('instruction_file') or ('design/agentic-design-harness/HARNESS.md' if scoped else 'AGENTS.md')
 # Existing project entrypoints always belong to the project.
 if not old and not scoped and (target/'AGENTS.md').exists():entry='AGENTS-agentic-design-harness.md'
 collisions=[];added=[]
 def safe(rel):
  path=target/rel
  if Path(rel).is_absolute() or not path.resolve().is_relative_to(target):raise ValueError('unsafe target: '+rel)
  for item in [path,*path.parents]:
   if item==target:break
   if item.is_symlink():raise ValueError('linked project path: '+rel)
  return path
 def put(rel,data,required=False,mode=None):
  try:
   path=safe(rel)
   if path.exists() or path.is_symlink():
    if required and (not path.is_file() or path.read_bytes()!=data):collisions.append(rel)
    return False
   path.parent.mkdir(parents=True,exist_ok=True)
   with path.open('xb') as f:f.write(data)
   if mode is not None:path.chmod(mode)
   added.append(rel);return True
  except (OSError,ValueError) as e:
   collisions.append(rel+': '+str(e));return False
 def copy(src,dst,required=False):
  f=ROOT/src;return put(dst,f.read_bytes(),required,f.stat().st_mode&0o777)
 for name in sorted(json.loads((ROOT/'docs/skills-lock.json').read_text())['skills']):
  for f in sorted((ROOT/'.claude/skills'/name).rglob('*')):
   if not f.is_file() or f.name=='.DS_Store' or '__pycache__' in f.parts or f.suffix=='.pyc':continue
   rel=str(f.relative_to(ROOT/'.claude/skills'))
   before=len(collisions);copy(str(f.relative_to(ROOT)),skills+'/'+rel,True)
   if len(collisions)>before:
    copy(str(f.relative_to(ROOT)),('.agents' if scoped else '.claude')+'/skill-candidates/agentic-design-harness/'+rel)
 for src,dst in [('check.sh','dh-check.sh'),('budget.sh','dh-budget.sh'),('cheatsheet.sh','dh-cheatsheet.sh'),('harness-preflight.py','dh-preflight.py'),('harness-context.py','dh-context.py'),('host-check.sh','dh-host-check.sh'),('create-project.py','dh-create-project.py'),('render_target.py','render_target.py')]:
  copy('scripts/'+src,'scripts/'+dst,True)
 for f in (ROOT/'scripts/measure').glob('*.mjs'):copy(str(f.relative_to(ROOT)),'scripts/measure/'+f.name,True)
 for name in ['skills-lock.json','harness-package.json','PROJECT-START.md','INTEGRATION.md']:
  copy('docs/'+name,'docs/agentic-design-harness/'+name,True)
 for f in (ROOT/'design').rglob('*'):
  if f.is_file():copy(str(f.relative_to(ROOT)),str(f.relative_to(ROOT)))
 # Generate only a newly installed empty cheat sheet; never replace existing project context.
 if 'design/cheatsheet.md' in added:
  result=subprocess.run(['bash',str(target/'scripts/dh-cheatsheet.sh')],stdout=subprocess.PIPE,text=True)
  if result.returncode:collisions.append('design/cheatsheet.md generation failed')
 # Render instructions once for their actual installed location, including relative imports.
 text=(ROOT/'AGENTS.md').read_text()
 for src,dst in [('scripts/check.sh','scripts/dh-check.sh'),('scripts/create-project.py','scripts/dh-create-project.py'),('docs/PROJECT-START.md','docs/agentic-design-harness/PROJECT-START.md')]:text=text.replace(src,dst)
 text=text.replace('.claude/skills/',skills+'/')
 for name in ['product.md','cheatsheet.md']:
  rel=os.path.relpath(target/'design'/name,(target/entry).parent).replace(os.sep,'/')
  text=text.replace('@design/'+name,'@'+rel)
 put(entry,text.encode(),True)
 router='.agents/rules/agentic-design-harness.md'
 if scoped:
  text=(ROOT/'integration/design-harness-rule.md').read_text().replace('design/HARNESS.md',entry)
  put(router,text.encode(),True)
 else:put('CLAUDE.md',('@'+entry+'\n').encode(),True)
 settings={'name':'agentic-design-harness','version':(ROOT/'VERSION').read_text().strip(),'skills_path':skills,'project_root':'.','instruction_file':entry,'execution_default':'folder-execution'}
 put('.agentic-design-harness.json',(json.dumps(settings,indent=2)+'\n').encode(),True)
 copy('NOTICE','docs/agentic-design-harness/NOTICE',True)
 # No root README, rule file, account setting or project instruction is edited.
 # A report is a new sidecar, including exact proposed human-visible integration lines.
 claude='@'+entry
 codex='UI and design work reads '+entry+' before work begins.'
 report='# Agentic Design Harness — installation\n\nExisting project files are preserved. No global installation or publication.\n\n'
 report+='For Claude, add this actual import to CLAUDE.md (outside code/comments):\n\n    '+claude+'\n\n'
 report+='For hosts reading AGENTS.md, add this routing instruction there:\n\n    '+codex+'\n\n'
 report+='If a development harness generates these files, add the route to its canonical source and regenerate its views.\n\n'
 report+='Confirm with: bash scripts/dh-host-check.sh .\n\n'
 report+='Local skill verification does not certify native activation or hidden host guidance.\n\n'
 if collisions:report+='## Conflicts requiring reconciliation\n\n'+'\n'.join('- '+x for x in collisions)+'\n'
 reportpath='docs/agentic-design-harness/INSTALLATION.md'
 if (target/reportpath).exists() and (target/reportpath).read_text()!=report:
  n=2
  while (target/f'docs/agentic-design-harness/INSTALLATION-{n}.md').exists():n+=1
  reportpath=f'docs/agentic-design-harness/INSTALLATION-{n}.md'
 put(reportpath,report.encode())
 verify=subprocess.run([sys.executable,str(ROOT/'scripts/harness-preflight.py'),'--root',str(target)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 chain=subprocess.run([sys.executable,str(ROOT/'scripts/harness-context.py'),'--root',str(target)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 print(f'Agentic Design Harness → {target}\nAdded {len(added)} files; existing project files kept.')
 if collisions or verify.returncode or chain.returncode:
  print('INSTALLED BUT NOT ACTIVATED — reconcile conflicts and explicit entry routes.')
  print('Integration report: '+reportpath+'\nClaude: '+claude+'\nAGENTS: '+codex)
  for item in collisions[:15]:print('  CONFLICT: '+item)
  if verify.returncode:print(verify.stdout)
  if chain.returncode:print(chain.stdout)
  return 4
 print('INSTALLED — explicit local entry routes verified; live native activation NOT VERIFIED.')
 return 0
if __name__=='__main__':
 try:sys.exit(main())
 except (OSError,ValueError,KeyError) as e:print('INSTALLATION INCOMPLETE: '+str(e),file=sys.stderr);sys.exit(4)
