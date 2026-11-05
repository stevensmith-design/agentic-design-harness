#!/usr/bin/env python3
"""Protect host wiring against the two observed workflow regressions."""
from pathlib import Path
import sys
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
s=(ROOT/'AGENTS.md').read_text();errors=[]
for phrase in ['folder-execution','keep original references directly available','study-proof','STUDY — DECISION REQUIRED','DRAFT — REVIEW REQUIRED','/ui-design-system','one bounded repair','separate sibling project']:
 if phrase.lower() not in s.lower():errors.append('missing harness contract: '+phrase)
for phrase in ['never the originals','only abstract findings','invoke skills by name.','contract-only builders']:
 if phrase.lower() in s.lower():errors.append('retired routing restored: '+phrase)
# Inspect the current cross-skill instructions without imposing a Code-only CLAUDE template.
checks={
 'direction-study':['args: "study-proof"','every rendered proof','no positive recommendation','originals remain directly viewable'],
 'ui-design-principles':['## Study-proof mode','An index-only read does not complete this skill'],
 'distinctiveness-review':['## Direction-study handoff','## 1 · Look before machine evidence'],
 'design-build':['references/skill-invocation.md','### 5 · Render','### 6 · Delegate'],
 'design-review':['references/skill-invocation.md','Reference resonance and similarity']}
for name,phrases in checks.items():
 text=' '.join((ROOT/'.claude/skills'/name/'SKILL.md').read_text().split()).lower()
 for phrase in phrases:
  if phrase.lower() not in text:errors.append(name+': missing '+phrase)
for error in errors:print('FAIL',error)
if not errors:print('PASS — bundled workflow handoffs and reference/folder execution contracts')
sys.exit(bool(errors))
