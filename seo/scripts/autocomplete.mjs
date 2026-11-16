#!/usr/bin/env node
/**
 * Expand seed keywords with live Google Autocomplete suggestions.
 *
 *   node autocomplete.mjs --gl in --hl en "ai chatbot for" "whatsapp automation"
 *   node autocomplete.mjs --gl us --deep "crm for real estate"   # also a-z and question prefixes
 *
 * Prints JSON: { seed: [suggestions...] }. Uses Google's public suggest endpoint,
 * the same one the search box uses. Keep runs small; it is a research aid, not a crawler.
 */
const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  if (i === -1) return fallback;
  const value = args[i + 1];
  args.splice(i, 2);
  return value;
};
const gl = opt("gl", "us");
const hl = opt("hl", "en");
const deepIndex = args.indexOf("--deep");
const deep = deepIndex !== -1;
if (deep) args.splice(deepIndex, 1);
const seeds = args;

if (seeds.length === 0) {
  console.error('Usage: node autocomplete.mjs [--gl in] [--hl en] [--deep] "seed one" "seed two"');
  process.exit(1);
}

const QUESTION_PREFIXES = ["how", "what", "why", "best", "is", "can", "cost of", "vs"];
const LETTERS = "abcdefghijklmnopqrstuvwxyz".split("");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function suggest(query) {
  const url = `https://suggestqueries.google.com/complete/search?client=firefox&hl=${hl}&gl=${gl}&q=${encodeURIComponent(query)}`;
  const res = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 keyword-research" } });
  if (!res.ok) return [];
  const data = JSON.parse(await res.text());
  return Array.isArray(data?.[1]) ? data[1] : [];
}

const out = {};
for (const seed of seeds) {
  const queries = [seed];
  if (deep) {
    queries.push(...LETTERS.map((l) => `${seed} ${l}`));
    queries.push(...QUESTION_PREFIXES.map((p) => `${p} ${seed}`));
  }
  const found = new Set();
  for (const q of queries) {
    for (const s of await suggest(q)) found.add(s);
    await sleep(150);
  }
  out[seed] = [...found];
}
console.log(JSON.stringify({ gl, hl, fetchedAt: new Date().toISOString(), results: out }, null, 2));
