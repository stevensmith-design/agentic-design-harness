#!/usr/bin/env python3
"""Check explicit project instruction routes or budget the actual design context.

This is a static local contract check, not a simulation of a live host.
"""
import argparse,json,re,sys
from pathlib import Path

def config(root):
 p=root/'.agentic-design-harness.json'
 return json.loads(p.read_text()) if p.exists() else {}
def instruction(root):
 c=config(root)
 name=c.get('instruction_file')
 if not name:
  if (root/'design/HARNESS.md').exists():name='design/HARNESS.md'
  elif (root/'AGENTS-design-harness.md').exists():name='AGENTS-design-harness.md'
  else:name='AGENTS.md'
 p=(root/name).resolve()
 if not p.is_relative_to(root):raise ValueError('instruction path escapes project')
 if not p.is_file():raise ValueError('missing instruction file: '+name)
 return p

def plain_blocks(text):
 text=re.sub(r'<!--.*?-->','',text,flags=re.S)
 text=re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$','',text)
 return text

def prose(text):
 return re.sub(r'`[^`\n]*`','',plain_blocks(text))

def check(root,host):
 target=instruction(root);seen=set()
 def follow(p,depth=0):
  p=p.resolve()
  if not p.is_relative_to(root):raise ValueError('external import not verified: '+str(p))
  if not p.is_file():raise ValueError('unresolved import: '+str(p.relative_to(root)))
  if p in seen:return
  if depth>4:raise ValueError('import depth exceeds four hops')
  seen.add(p);raw=p.read_text();text=prose(raw)
  for name in re.findall(r'(?<![\w])@((?:\\ |[A-Za-z0-9_./-])+)',text):
   follow(p.parent/name.replace('\\ ',' '),depth+1)
  # Manual routing is checked separately from Claude's actual @ import syntax.
  # Only an explicit reading directive counts; code examples/comments do not.
  for line in plain_blocks(raw).splitlines():
   if not re.search(r'\b(read|reads|follow|consult|load)\b',line,re.I):continue
   if line.lstrip().startswith(('```','~~~')):continue
   for candidate in [target,root/'.agents/rules/agentic-design-harness.md']:
    rel=str(candidate.relative_to(root))
    if rel in line and candidate!=p:follow(candidate,depth+1)
  return seen
 entry=root/('CLAUDE.md' if host=='claude' else 'AGENTS.md')
 follow(entry)
 if target not in seen:raise ValueError(host+' entry does not route to '+str(target.relative_to(root)))
 # Context imports inside the actual harness must resolve from that file, not project cwd.
 for name in ['product.md','cheatsheet.md']:
  if (root/'design'/name).resolve() not in seen:
   raise ValueError('design context is unreachable: design/'+name)
 print('PASS — '+host+' explicit local instruction chain resolves; native activation NOT VERIFIED')

def budget(root):
 entry=instruction(root);total=0
 print('Design context budget (the design module, not the engineering harness)')
 for p in [entry,root/'design/product.md',root/'design/cheatsheet.md']:
  text=p.read_text();n=sum(bool(line.strip()) and line.strip() not in ('<!--','-->') for line in text.splitlines())
  if p.name=='product.md' and '<PRODUCT>' in text:n=21
  if p.name=='cheatsheet.md' and not re.search(r'^- `',text,re.M):n=46
  print(f'  {str(p.relative_to(root))}: {n} lines');total+=n
 print(f'  total: {total}/200; headroom: {200-total}')
 if total>160:raise ValueError('design context needs at least 40 lines of headroom')
 print('PASS — design context within budget')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--host',choices=['claude','codex','both'],default='both');p.add_argument('--budget',action='store_true');a=p.parse_args()
 try:
  root=a.root.resolve()
  if a.budget:budget(root)
  else:
   for host in (['claude','codex'] if a.host=='both' else [a.host]):check(root,host)
 except (ValueError,OSError,KeyError) as e:print('NOT VERIFIED: '+str(e),file=sys.stderr);return 1
 return 0
if __name__=='__main__':sys.exit(main())
