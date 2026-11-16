# Search Console page scripts (Chrome DevTools MCP)

Search Console is a single-page app: several `[role=main]` panels exist and only one is visible. These functions read the visible panel. Run them with `mcp__chrome-devtools__evaluate_script` (paste as `function`, or save to a file and pass `sourcePath`). Selectors can change; if one returns nothing, take a snapshot and adapt.

## Read the visible report as text

```javascript
async () => {
  await new Promise((r) => setTimeout(r, 2500));
  const main = [...document.querySelectorAll('[role=main]')].find((m) => m.offsetParent);
  return main ? main.innerText.slice(0, 8000) : document.body.innerText.slice(0, 8000);
}
```

## Table rows, with rows-per-page raised to 100

Works on Page indexing drilldowns, the indexed-pages list and Performance tables.

```javascript
async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const vis = () => [...document.querySelectorAll('[role=main]')].find((m) => m.offsetParent);
  let m;
  for (let i = 0; i < 40; i++) { m = vis(); if (m && m.querySelector('tr')) break; await sleep(300); }
  const lb = [...m.querySelectorAll('[aria-label="Number of rows per page"]')].find((x) => x.offsetParent);
  if (lb) {
    lb.click(); await sleep(500);
    const opt = [...document.querySelectorAll('[role=option]')].filter((o) => o.offsetParent && o.textContent.trim() === '100').pop();
    if (opt) { opt.click(); await sleep(2500); }
  }
  m = vis();
  return [...m.querySelectorAll('tr')].map((r) => r.innerText.replace(/\s+/g, ' ').trim()).filter(Boolean);
}
```

## Open one "Why pages aren't indexed" reason

On `.../search-console/index?resource_id=...`; change the prefix to the reason you want, then run the table script above.

```javascript
() => {
  const m = [...document.querySelectorAll('[role=main]')].find((x) => x.offsetParent);
  const row = [...m.querySelectorAll('tr')].find((r) => r.innerText.startsWith('Crawled - currently not indexed'));
  row?.click();
  return !!row;
}
```

## Performance: switch to the Pages tab

```javascript
async () => {
  const m = [...document.querySelectorAll('[role=main]')].find((x) => x.offsetParent);
  [...m.querySelectorAll('[role=tab]')].find((t) => t.textContent.trim() === 'Pages')?.click();
  await new Promise((r) => setTimeout(r, 2500));
  return 'ok';
}
```

## Request indexing for one URL

URL Inspection has no deep link. First `fill` the "Inspect any URL" combobox (take a snapshot for its uid) with the full URL and `press_key` Enter, then run:

```javascript
async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  await sleep(1500);
  const dialogs = () => [...document.querySelectorAll('[role=dialog],[role=alertdialog]')].filter((x) => x.offsetParent && !/About Search Console/.test(x.innerText));
  let btn;
  for (let i = 0; i < 90; i++) {
    btn = [...document.querySelectorAll('[role=button],button')].find((b) => b.offsetParent && /^\s*request indexing\s*$/i.test(b.innerText));
    if (btn) break;
    await sleep(500);
  }
  const main = [...document.querySelectorAll('[role=main]')].filter((m) => m.offsetParent).map((m) => m.innerText).join('\n');
  const status = main.split('\n').filter((l) => /^URL is|^Page is/i.test(l)).slice(0, 2).join(' | ');
  if (!btn) return 'NO BUTTON: ' + status;
  btn.click();
  for (let i = 0; i < 150; i++) {
    const d = dialogs().map((x) => x.innerText).join(' ').replace(/\s+/g, ' ');
    if (/requested|quota|exceeded|problem|error|try again/i.test(d)) {
      dialogs().flatMap((x) => [...x.querySelectorAll('[role=button],button')]).find((b) => /dismiss|got it|ok/i.test(b.innerText))?.click();
      return status + ' => ' + d.slice(0, 160);
    }
    await sleep(1000);
  }
  return status + ' => timeout';
}
```

A "quota exceeded" message means stop for today. If a visible reCAPTCHA challenge appears, ask the user to complete it.

## Validate fix on an issue group

Open the reason's drilldown page, then:

```javascript
async () => {
  const m = [...document.querySelectorAll('[role=main]')].find((x) => x.offsetParent);
  const b = [...m.querySelectorAll('[role=button],button')].find((x) => /validate fix/i.test(x.innerText));
  if (!b) return 'no Validate button (already validating, or not available for this reason)';
  b.click();
  await new Promise((r) => setTimeout(r, 5000));
  return [...document.querySelectorAll('[role=main]')].find((x) => x.offsetParent).innerText.slice(0, 300);
}
```

## Submit a sitemap

On the Sitemaps page, `fill` the "Enter sitemap URL" textbox with `sitemap.xml` and click SUBMIT (snapshot for the uids). Expect "Sitemap submitted successfully".
