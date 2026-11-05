// Heading order, semantic main and target size — rendered, not parsed.
// WCAG 2.2 SC 2.5.8 uses a 24 CSS px minimum with spacing and inline-target
// exceptions. A 44px touch target remains useful guidance, but is not the AA
// blocking threshold.
import { cdp } from './skill-root.mjs';
const { render } = cdp;

function probe() {
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')]
    .map(h => ({ level: +h.tagName[1], text: h.textContent.trim().slice(0, 40) }));
  const skips = [];
  for (let i = 1; i < hs.length; i++) {
    if (hs[i].level > hs[i - 1].level + 1) skips.push(`h${hs[i-1].level} → h${hs[i].level} ("${hs[i].text}")`);
  }

  const landmarks = ['header', 'nav', 'main', 'footer'].filter(tag => {
    const role = tag === 'header' ? 'banner' : tag === 'footer' ? 'contentinfo' : tag;
    return document.querySelector(tag) || document.querySelector(`[role="${role}"]`);
  });
  const mainCount = document.querySelectorAll('main,[role="main"]').length;

  const targets = [...document.querySelectorAll('a,button,input,select,textarea,[role="button"]')]
    .map(el => ({ el, cs: getComputedStyle(el), rect: el.getBoundingClientRect() }))
    .filter(({ cs, rect }) => cs.display !== 'none' && cs.visibility !== 'hidden' && rect.width > 0 && rect.height > 0);

  const label = ({ el, rect }) => {
    const cls = typeof el.className === 'string' && el.className.trim() ? `.${el.className.trim().split(/\s+/)[0]}` : '';
    return `${el.tagName.toLowerCase()}${cls} ${Math.round(rect.width)}×${Math.round(rect.height)}px`;
  };
  const center = rect => ({ x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 });

  const undersized = targets.filter((target, index) => {
    const { el, cs, rect } = target;
    if (rect.width >= 24 && rect.height >= 24) return false;
    if (el.tagName === 'A' && cs.display === 'inline') return false; // inline-target exception
    const a = center(rect);
    const hasClearSpacing = targets.every((other, otherIndex) => {
      if (index === otherIndex) return true;
      const b = center(other.rect);
      return Math.hypot(a.x - b.x, a.y - b.y) >= 24;
    });
    return !hasClearSpacing;
  });

  const belowPreferred = targets.filter(({ rect }) => rect.width < 44 || rect.height < 44);
  return {
    h1: document.querySelectorAll('h1').length,
    skips,
    landmarks,
    mainCount,
    undersized: [...new Set(undersized.map(label))].slice(0, 5),
    belowPreferred: belowPreferred.length,
  };
}

const target = process.argv[2];
const result = await render({ target, probe, width: 1280, height: 900 });
const G = '\x1b[0;32m', R = '\x1b[0;31m', Y = '\x1b[1;33m', X = '\x1b[0m';
const line = (ok, message) => console.log(`${ok ? G + '✔' : R + '✘'}${X} ${message}`);
line(result.h1 === 1, `exactly one h1 (found ${result.h1})`);
line(result.skips.length === 0, result.skips.length ? `heading levels skip: ${result.skips.join(', ')}` : 'no skipped heading levels');
line(result.mainCount === 1, `exactly one semantic main (found ${result.mainCount})`);
line(result.undersized.length === 0,
  result.undersized.length ? `targets below 24px without spacing exception: ${result.undersized.join(', ')}` : 'targets meet WCAG 2.2 AA 24px size or an allowed exception');
console.log(`${Y}•${X} landmarks present: ${result.landmarks.join(', ') || 'none'} (header, nav and footer are page-dependent)`);
console.log(`${Y}•${X} ${result.belowPreferred} interactive target(s) below the preferred 44px touch size (advisory)`);
