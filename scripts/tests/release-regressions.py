#!/usr/bin/env python3
"""Observed release failures and non-destructive project lifecycle acceptance."""
import hashlib,json,shutil,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(*args):return subprocess.run(list(map(str,args)),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
def inventory(root):return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='.DS_Store'}
class ReleaseTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory(prefix='adh-release-');cls.t=Path(cls.temp.name)
  cls.clean=cls.t/'clean';r=run('bash',ROOT/'scripts/init.sh',cls.clean);assert r.returncode==0,r.stdout
  cls.scoped=cls.t/'existing';cls.scoped.mkdir()
  (cls.scoped/'AGENTS.md').write_text('Existing development harness.\n')
  (cls.scoped/'CLAUDE.md').write_text('@AGENTS.md\n')
  (cls.scoped/'README.md').write_text('Product README\n')
  (cls.scoped/'.agents/rules').mkdir(parents=True)
  (cls.scoped/'.agents/rules/security.md').write_text('Existing security rules\n')
  (cls.scoped/'design').mkdir();(cls.scoped/'design/HARNESS.md').write_text('Existing unrelated design rules\n')
  cls.before=inventory(cls.scoped)
  cls.install=run('bash',ROOT/'scripts/init.sh','--path-scoped',cls.scoped)
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_missing_claude_import_fails(self):
  p=self.clean/'CLAUDE.md';before=p.read_text();p.write_text('# No harness import\n')
  try:self.assertNotEqual(run('bash',ROOT/'scripts/host-check.sh',self.clean).returncode,0)
  finally:p.write_text(before)
 def test_comment_import_does_not_activate(self):
  p=self.clean/'CLAUDE.md';before=p.read_text();p.write_text('<!--\n@AGENTS.md\n-->\n')
  try:self.assertNotEqual(run('bash',ROOT/'scripts/host-check.sh',self.clean).returncode,0)
  finally:p.write_text(before)
 def test_fenced_example_does_not_activate(self):
  p=self.clean/'CLAUDE.md';before=p.read_text();p.write_text('```text\nRead AGENTS.md\n```\n')
  try:self.assertNotEqual(run('bash',ROOT/'scripts/host-check.sh',self.clean).returncode,0)
  finally:p.write_text(before)
 def test_nested_imports_and_actual_integration(self):
  target=self.t/'integrated';target.mkdir()
  (target/'AGENTS.md').write_text('Development harness.\n')
  (target/'CLAUDE.md').write_text('@AGENTS.md\n')
  r=run('bash',ROOT/'scripts/init.sh',target);self.assertEqual(r.returncode,4,r.stdout)
  marker=json.loads((target/'.agentic-design-harness.json').read_text());entry=marker['instruction_file']
  with (target/'AGENTS.md').open('a') as f:f.write('UI and design work reads '+entry+' before work begins.\n')
  # Simulate the explicit integration step by the project owner, not the installer.
  with (target/'CLAUDE.md').open('a') as f:f.write('@'+entry+'\n')
  check=run('bash',target/'scripts/dh-host-check.sh',target);self.assertEqual(check.returncode,0,check.stdout)
  imports=[line[1:] for line in (target/entry).read_text().splitlines() if line.startswith('@')]
  self.assertIn((target/'design/product.md').resolve(),[((target/entry).parent/name).resolve() for name in imports])
  before=inventory(target);again=run('bash',ROOT/'scripts/init.sh',target)
  self.assertEqual(again.returncode,0,again.stdout)
  for name,body in before.items():self.assertEqual((target/name).read_bytes(),body,name)
 def test_path_scoped_budget_uses_harness(self):
  r=run('bash',self.scoped/'scripts/dh-budget.sh')
  self.assertIn('design/agentic-design-harness/HARNESS.md',r.stdout)
  self.assertNotIn('AGENTS.md                       1 lines',r.stdout)
 def test_existing_files_unchanged(self):
  self.assertEqual(self.install.returncode,4,self.install.stdout)
  after=inventory(self.scoped)
  for name,data in self.before.items():self.assertEqual(after[name],data,name)
 def test_distinct_instruction_file_and_report(self):
  marker=json.loads((self.scoped/'.agentic-design-harness.json').read_text())
  self.assertEqual(marker['instruction_file'],'design/agentic-design-harness/HARNESS.md')
  self.assertTrue((self.scoped/marker['instruction_file']).is_file())
  report=self.scoped/'docs/agentic-design-harness/INSTALLATION.md'
  self.assertTrue(report.is_file())
  self.assertIn('existing',report.read_text().lower())
 def test_new_projects_are_independent_complete_copies(self):
  before=inventory(ROOT)
  for name in ['one','two']:
   dest=self.t/name;r=run('python3',ROOT/'scripts/create-project.py','--destination',dest)
   self.assertEqual(r.returncode,0,r.stdout)
   for needed in ['scripts/init.sh','scripts/host-check.sh','scripts/dh-preflight.py','design/brief.md','docs/agentic-design-harness/PROJECT-START.md','.claude/skills/ui-design-system/SKILL.md']:
    self.assertTrue((dest/needed).is_file(),needed)
   (dest/'design/product.md').write_text(name+' brand discovery\n')
  self.assertEqual(before,inventory(ROOT),'source polluted by project creation')
  self.assertNotEqual((self.t/'one/design/product.md').read_bytes(),(self.t/'two/design/product.md').read_bytes())
 def test_installer_refuses_linked_project_rule_file(self):
  target=self.t/'linked';target.mkdir();external=self.t/'external';external.write_text('KEEP\n')
  (target/'AGENTS.md').symlink_to(external)
  r=run('bash',ROOT/'scripts/init.sh',target)
  self.assertEqual(external.read_text(),'KEEP\n')
  self.assertNotEqual(r.returncode,0)
if __name__=='__main__':unittest.main(verbosity=2)
