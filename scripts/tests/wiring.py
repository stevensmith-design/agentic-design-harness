#!/usr/bin/env python3
"""Integration checks for real installation, relocation and local skill identity."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(*args,cwd=None):
 return subprocess.run(list(map(str,args)),cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
def require(ok,message):
 if not ok:raise AssertionError(message)
print('Harness wiring integration')
with tempfile.TemporaryDirectory(prefix='adh-wiring-') as tmp:
 t=Path(tmp)
 clean=t/'new project';r=run('bash',ROOT/'scripts/init.sh',clean);require(r.returncode==0,r.stdout)
 require((clean/'.agentic-design-harness.json').exists(),'missing installed workspace identity')
 require((clean/'docs/agentic-design-harness/skills-lock.json').exists(),'installed payload has no lock')
 r=run('python3',ROOT/'scripts/harness-preflight.py','--root',clean);require(r.returncode==0,r.stdout)
 r=run('bash',ROOT/'scripts/init.sh',clean);require(r.returncode==0,'repeat clean install failed: '+r.stdout)
 moved=t/'moved project';clean.rename(moved)
 r=run('python3',ROOT/'scripts/harness-preflight.py','--root',moved);require(r.returncode==0,r.stdout)
 scoped=t/'existing project';(scoped/'.agents/skills').mkdir(parents=True)
 for name,body in [('AGENTS.md','PROJECT INSTRUCTIONS\n'),('CLAUDE.md','@AGENTS.md\n'),('README.md','PROJECT README\n'),('harness.config.yaml','harness: 1\n')]:
  (scoped/name).write_text(body)
 before={p.name:p.read_bytes() for p in scoped.iterdir() if p.is_file()}
 r=run('bash',ROOT/'scripts/init.sh',scoped);require(r.returncode==4,r.stdout)
 for name,data in before.items():require((scoped/name).read_bytes()==data,'existing '+name+' changed')
 r=run('python3',ROOT/'scripts/harness-preflight.py','--root',scoped);require(r.returncode==0,r.stdout)
 # A real Node import must resolve the .agents renderer, not just pass a text scan.
 r=run('node','--input-type=module','-e',"import { skillRoot } from './scripts/measure/skill-root.mjs'; await import(new URL('../../'+skillRoot+'/ui-design-review/scripts/cdp.mjs',new URL('./scripts/measure/skill-root.mjs',import.meta.url))); console.log(skillRoot)",cwd=scoped)
 require(r.returncode==0 and '.agents/skills' in r.stdout,r.stdout)
 r=run('bash',scoped/'scripts/dh-check.sh','--static-only',ROOT/'scripts/fixtures/floor-tokens-oneline.html');require(r.returncode==0,r.stdout)
 (scoped/'.agents/skills/design-build/SKILL.md').write_text('wrong same-named skill')
 r=run('python3',ROOT/'scripts/harness-preflight.py','--root',scoped);require(r.returncode!=0,'corrupt payload accepted')
 r=run('bash',ROOT/'scripts/init.sh',scoped);require(r.returncode==4,'collision claimed activated')
 require((scoped/'.agents/skills/design-build/SKILL.md').read_text()=='wrong same-named skill','collision overwritten')
 require((scoped/'.agents/skill-candidates/agentic-design-harness/design-build/SKILL.md').exists(),'collision has no candidate')
 dest=t/'separate project'
 r=run('python3',ROOT/'scripts/create-project.py','--destination',dest);require(r.returncode==0,r.stdout)
 require((dest/'.agentic-design-harness.json').exists(),'bootstrap did not install ongoing harness')
 r=run('python3',ROOT/'scripts/create-project.py','--destination',dest);require(r.returncode!=0,'bootstrap overwrote existing project')
 r=run('python3',ROOT/'scripts/create-project.py','--destination',ROOT/'accidental-app');require(r.returncode!=0,'bootstrap allowed output inside harness')
 # Default sibling output + name collisions, using a relocatable full source copy.
 checkout=t/'harness-copy';shutil.copytree(ROOT,checkout,ignore=shutil.ignore_patterns('dist','__pycache__'))
 r=run('python3',checkout/'scripts/create-project.py','--name','workshop');require(r.returncode==0,r.stdout)
 require((t/'workshop/.agentic-design-harness.json').exists(),'new project did not default beside harness')
 r=run('python3',checkout/'scripts/create-project.py','--name','workshop');require(r.returncode==0,r.stdout)
 require((t/'workshop-2/.agentic-design-harness.json').exists(),'name collision was not handled safely')
 r=run('python3',dest/'scripts/dh-create-project.py','--name','nested');require(r.returncode!=0,'installed project spawned another by default')
print('PASS — clean install, path-scoped preservation, relocation, renderer identity, drift/collision rejection and separate-project bootstrap')
