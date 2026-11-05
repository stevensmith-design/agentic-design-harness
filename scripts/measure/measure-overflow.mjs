#!/usr/bin/env node
// Rendered narrow-width overflow — does the document exceed the viewport?
//
// The harness previously LABELLED four viewport runs as "narrow-width overflow"
// and ran the padding measurement at each width. The label claimed one thing
// and the evidence recorded another; a page could overflow at 320px and the
// stored evidence would say overflow was measured and passed.
//
// This asks the only question that matters: is scrollWidth wider than the
// viewport, and if so, which elements cross the right edge? Reporting the
// offenders is the point — "the page overflows" sends someone hunting; "these
// three elements are 40px past the edge" does not.
//
// Lives in harness scripts rather than the bundled skills: it is harness plumbing
// for an evidence gap the harness created.
//
// Exit: 0 no overflow · 1 overflow found · 2 could not measure.

import { cdp } from './skill-root.mjs';
const { render, parseCommonArgs, failUnmeasurable } = cdp;

function probe() {
  const doc = document.documentElement;
  const viewport = window.innerWidth;
  const scrollWidth = Math.max(doc.scrollWidth, document.body ? document.body.scrollWidth : 0);

  const offenders = [];
  if (scrollWidth > viewport + 1) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) continue;
      const past = Math.round(r.right - viewport);
      if (past > 1) {
        const cs = getComputedStyle(el);
        // An element clipped by an ancestor does not visibly overflow.
        if (cs.position === 'fixed' && cs.visibility === 'hidden') continue;
        offenders.push({
          tag: el.tagName.toLowerCase(),
          cls: (el.className && typeof el.className === 'string'
                ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.')
                : ''),
          past,
          width: Math.round(r.width),
        });
      }
    }
  }
  // Deepest-first is noisy; report the widest offenders.
  offenders.sort((a, b) => b.past - a.past);
  return { viewport, scrollWidth, offenders: offenders.slice(0, 6),
           total: offenders.length };
}

const opts = parseCommonArgs(process.argv.slice(2));
if (!opts.target) {
  console.error('usage: measure-overflow.mjs <file-or-url> [--width 320]');
  process.exit(2);
}

let result;
try {
  result = await render({
    target: opts.target, probe,
    width: opts.width || 320, height: opts.height || 900, mobile: opts.mobile,
  });
} catch (err) {
  failUnmeasurable(err, 'measure-overflow');
}

const { viewport, scrollWidth, offenders, total } = result;
const over = scrollWidth - viewport;

console.log('');
console.log('  ----------------------------------------');
if (over <= 1) {
  console.log(`  OK document ${scrollWidth}px fits viewport ${viewport}px — no horizontal overflow.`);
  process.exit(0);
}

console.log(`  FAIL document ${scrollWidth}px exceeds viewport ${viewport}px by ${over}px.`);
for (const o of offenders) {
  console.log(`      ${o.tag}${o.cls} — ${o.past}px past the right edge (${o.width}px wide)`);
}
if (total > offenders.length) {
  console.log(`      …and ${total - offenders.length} more`);
}
console.log(`  FAIL ${total} element(s) cross the viewport edge at ${viewport}px.`);
process.exit(1);
