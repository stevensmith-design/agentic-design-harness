// Resolve the installed tree once. Never silently fall through to a global copy.
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = new URL('../../', import.meta.url);
const marker = new URL('.agentic-design-harness.json', root);
export const skillRoot = fs.existsSync(marker)
  ? JSON.parse(fs.readFileSync(marker, 'utf8')).skills_path : '.claude/skills';
if (!['.claude/skills', '.agents/skills'].includes(skillRoot)) throw new Error('Invalid harness skill path');
const moduleURL = new URL(`${skillRoot}/ui-design-review/scripts/cdp.mjs`, root);
if (!fs.existsSync(fileURLToPath(moduleURL))) throw new Error('Pinned local renderer missing; run harness preflight');
export const cdp = await import(moduleURL);
