// Original background music for a video, fitted to its story. Eravue owns it (synthesised from scratch, no samples),
// so it is cleared for organic posts AND ads. One command from plan to a ducked bed:
//
//   pnpm compose <slug> --init            write music/compositions/<slug>.plan.json (edit the moments, then run again)
//   pnpm compose <slug>                   fit + synthesise + register + build public/<slug>/bed.wav (ducked under the voice)
//   pnpm compose <slug> --no-bed          only the track (e.g. before the voice exists)
//
// The plan (music/compositions/<slug>.plan.json) names story MOMENTS, not bars:
//   { "engine": "lofi", "mood": "night", "title": "...",
//     "moments": { "drop": "r1", "lift": "w1:what", "breakdown": "t1", "back": "t2:customer", "outro": "c1", "final": 66.1 },
//     "length"?: 68.2, "bpm"?: [72, 96] }
// A moment is a beat id ("r1"), beat:word ("t2:customer", same matching as cue()), or seconds. Only "drop" is required.
//   drop = drums come in · lift = the arp joins (the build / reveal) · breakdown = drums out (the reflective line)
//   back = drums return · outro = thins out under the CTA · final = the last chord (default: end of voice)
// compose.mjs searches tempo + offset so bar lines land on those times (drop exact, the rest within ~0.1 s or on
// a half bar), writes the full arrangement to music/compositions/<slug>.json, renders it with scripts/compose-lofi.py
// to E:/video-edits/eravue-motion/music/<slug>-original.wav, registers it in music/beds.json + music/LICENSES.md and
// runs music-bed.mjs. Moods: night (lo-fi, late, reflective), warm (calm, friendly), bright (upbeat, optimistic),
// tense (problem / stakes). A handmade <slug>.json with no plan is rendered as is; "engine": "paper" (marimba,
// per-section tempo, absolute times; see scripts/compose-paper.py) is passed through the same way.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { ROOT, paths, readJson, rel } from "./paths.mjs";

const RS = process.env.REELSTUDIO_DIR ?? "D:/projects/SOCIAL MEDIA/short-form-quick-edits";
const PY = process.env.ERAVUE_PYTHON ?? path.join(RS, ".venv/Scripts/python.exe");
const MUSIC_DIR = process.env.ERAVUE_MUSIC_DIR ?? "E:/video-edits/eravue-motion/music";
const args = process.argv.slice(2);
const slug = args.find((a) => !a.startsWith("--"));
const p = paths(slug);
const compDir = path.join(ROOT, "music/compositions");
const planFile = path.join(compDir, `${slug}.plan.json`);
const specFile = path.join(compDir, `${slug}.json`);
const timing = fs.existsSync(p.timing) ? readJson(p.timing) : null;
const write = (f, o) => fs.writeFileSync(f, JSON.stringify(o, null, 2) + "\n");

const MOODS = {
  night: { swing: 0.07, chords: [["F2", "F3 A3 C4 E4"], ["E2", "E3 G3 B3 D4"], ["D2", "F3 A3 C4 E4"], ["C2", "E3 G3 B3 D4"]], final: ["F2", "F3 A3 C4 E4 G4"] },
  warm: { swing: 0.06, chords: [["C2", "G3 B3 E4 G4"], ["A2", "C4 E4 G4 A4"], ["F2", "A3 C4 E4 G4"], ["G2", "B3 D4 E4 G4"]], final: ["C2", "G3 B3 D4 E4 G4"] },
  bright: { swing: 0.04, chords: [["D2", "F#3 A3 C#4 E4"], ["B1", "D4 F#4 A4 B4"], ["G2", "B3 D4 F#4 A4"], ["A2", "C#4 E4 G4 B4"]], final: ["D2", "F#3 A3 C#4 E4 A4"] },
  tense: { swing: 0.05, chords: [["A2", "C4 E4 G4 A4"], ["F2", "A3 C4 E4 G4"], ["D2", "F3 A3 C4 E4"], ["E2", "G#3 B3 D4 E4"]], final: ["A2", "C4 E4 G4 B4"] },
};
const chord = ([bass, notes]) => ({ bass, notes: notes.split(" ") });

// ---------- --init: a starting plan from the script's beats ----------
if (args.includes("--init")) {
  if (fs.existsSync(planFile)) throw new Error(`${rel(planFile)} exists; edit it instead`);
  if (!timing) throw new Error(`No ${rel(p.timing)} yet (run vo:sync / vo:align first)`);
  const ids = timing.beats.map((b) => b.id);
  const at = (f) => ids[Math.min(ids.length - 1, Math.max(1, Math.round(ids.length * f)))];
  write(planFile, {
    engine: "lofi",
    mood: "night",
    title: `${slug} (Eravue original)`,
    moments: { drop: at(0.15), lift: at(0.45), breakdown: at(0.7), back: at(0.78), outro: ids[ids.length - 1] },
    why: "EDIT ME: say which line each moment lands on and why (drop = the first payoff, breakdown = the reflective line, outro = under the CTA).",
    beats: Object.fromEntries(timing.beats.map((b) => [b.id, `${b.start.toFixed(2)} s  ${b.words.slice(0, 6).map((w) => w.w).join(" ")}`])),
  });
  console.log(`wrote ${rel(planFile)}: guessed moments from the beat list. Set them to the real story moments, then: pnpm compose ${slug}`);
  process.exit(0);
}

// ---------- moments -> seconds ----------
const norm = (s) => s.toLowerCase().replace(/[’']/g, "").replace(/[^a-z0-9]+/g, "");
const toSec = (m) => {
  if (typeof m === "number") return m;
  if (!timing) throw new Error("moments need timing.json (or use seconds)");
  const [id, word] = String(m).split(":");
  const b = timing.beats.find((x) => x.id === id);
  if (!b) throw new Error(`moment "${m}": no beat ${id}`);
  if (!word) return b.start;
  const hit = b.words.find((w) => w.w === norm(word) || w.w.startsWith(norm(word)));
  if (!hit) throw new Error(`moment "${m}": no word "${word}" in ${id}`);
  return hit.t;
};

// ---------- fit tempo + offset ----------
function fit(plan) {
  const mo = Object.fromEntries(Object.entries(plan.moments).map(([k, v]) => [k, toSec(v)]));
  if (mo.drop === undefined) throw new Error("plan.moments.drop is required");
  const [lo, hi] = plan.bpm ?? [72, 96];
  const others = ["lift", "breakdown", "back", "outro", "final"].filter((k) => mo[k] !== undefined);
  let best = null;
  for (let bpm = lo; bpm <= hi + 1e-9; bpm += 0.25) {
    const bar = 240 / bpm;
    for (const introBars of [2, 3, 4, 5, 6]) {
      const offset = mo.drop - introBars * bar;
      if (offset < 0 || offset > 1.2) continue;
      let score = 0;
      const bars = { drop: introBars };
      for (const k of others) {
        const x = (mo[k] - offset) / bar;
        const whole = Math.round(x);
        const half = Math.round(x * 2) / 2;
        const eW = Math.abs(x - whole) * bar;
        const eH = Math.abs(x - half) * bar + 0.04; // a half bar costs a little
        const useHalf = eH < eW && k !== "final";
        bars[k] = useHalf ? half : whole;
        score += (useHalf ? eH : eW) ** 2;
      }
      score += Math.abs(bpm - 82) * 0.0004 + offset * 0.002; // prefer a relaxed tempo and a short lead-in
      if (!best || score < best.score) best = { bpm, offset, bars, score, mo };
    }
  }
  if (!best) throw new Error(`no tempo in ${lo}-${hi} BPM gives a 2-6 bar intro before the drop at ${mo.drop.toFixed(2)} s; move the drop or widen "bpm"`);
  return best;
}

function arrange(plan, f) {
  const mood = MOODS[plan.mood ?? "night"];
  if (!mood) throw new Error(`Unknown mood "${plan.mood}". Moods: ${Object.keys(MOODS).join(", ")}`);
  const bar = 240 / f.bpm;
  const length = plan.length ?? (timing ? timing.duration + 3 : f.mo.final + 3);
  const lastBar = Math.floor((length - 1.2 - f.offset) / bar);
  const B = f.bars;
  const finalBar = Math.min(B.final ?? Math.max(B.outro ?? 0, lastBar), lastBar);
  const outro = Math.min(B.outro ?? finalBar, finalBar);
  const full = ["piano", "kick", "snare", "hats", "bass"];
  const s = [[0, B.drop, ["piano_soft"]], [Math.max(0, B.drop - 2), B.drop, ["hats"]]];
  // body: drop -> (lift) -> (breakdown -> back) -> outro
  const pts = [["drop", B.drop], ...(B.lift !== undefined ? [["lift", B.lift]] : []), ...(B.breakdown !== undefined ? [["breakdown", B.breakdown]] : []), ...(B.back !== undefined ? [["back", B.back]] : []), ["outro", outro]]
    .filter(([, b]) => b <= outro)
    .sort((a, b) => a[1] - b[1]);
  let lifted = false;
  let broken = false;
  for (let i = 0; i < pts.length - 1; i++) {
    const [k, a] = pts[i];
    const z = pts[i + 1][1];
    if (z <= a) continue;
    if (k === "lift") lifted = true;
    if (k === "breakdown") broken = true;
    if (k === "back") broken = false;
    s.push([a, z, broken ? ["piano_soft", "pad"] : lifted && k !== "back" ? [...full, "arp"] : full]);
  }
  if (finalBar > outro) s.push([outro, finalBar, ["piano_soft", "hats", "bass", "kick"]]);
  const at = (b) => +(f.offset + b * bar).toFixed(3);
  const risers = [B.drop, B.back].filter((b) => b !== undefined && b <= outro).map(at);
  const why = `fitted by compose.mjs: ${f.bpm} BPM, bar = ${bar.toFixed(3)} s from ${f.offset.toFixed(3)} s. ` + pts.map(([k, b]) => `${k} bar ${b} = ${at(b).toFixed(2)} s (asked ${f.mo[k]?.toFixed(2)} s)`).join(", ") + `, final chord bar ${finalBar} = ${at(finalBar).toFixed(2)} s. ${plan.why ?? ""}`;
  return { title: plan.title ?? `${slug} (Eravue original)`, generatedFrom: `${slug}.plan.json`, bpm: f.bpm, offset: +f.offset.toFixed(3), length: +length.toFixed(2), swing: mood.swing, chords: mood.chords.map(chord), sections: s, risers, finalBar, finalChord: chord(mood.final), why };
}

// ---------- build ----------
let spec;
let engine = "lofi";
if (fs.existsSync(planFile)) {
  const plan = readJson(planFile);
  engine = plan.engine ?? "lofi";
  if (engine !== "lofi") throw new Error(`plans support engine "lofi"; for "${engine}" write ${rel(specFile)} by hand`);
  const f = fit(plan);
  spec = arrange(plan, f);
  write(specFile, spec);
  console.log(spec.why);
  const worst = Object.entries(f.bars).filter(([k]) => k !== "final").map(([k, b]) => [k, Math.abs(f.offset + b * (240 / f.bpm) - f.mo[k])]).sort((a, b) => b[1] - a[1])[0];
  if (worst && worst[1] > 0.25) console.warn(`! "${worst[0]}" lands ${worst[1].toFixed(2)} s off its line. Fine for a breakdown/outro; move the moment or allow a wider "bpm" range if it matters.`);
} else if (fs.existsSync(specFile)) {
  spec = readJson(specFile);
  engine = spec.engine ?? (Array.isArray(spec.sections) && spec.sections[0]?.a !== undefined ? "paper" : "lofi");
} else throw new Error(`No ${rel(planFile)} or ${rel(specFile)}. Start with: pnpm compose ${slug} --init`);

const trackId = `${slug}-original`;
fs.mkdirSync(MUSIC_DIR, { recursive: true });
const out = path.join(MUSIC_DIR, `${trackId}.wav`).replace(/\\/g, "/");
const script = path.join(ROOT, "scripts", engine === "paper" ? "compose-paper.py" : "compose-lofi.py");
execFileSync(PY, ["-I", script, specFile, out], { stdio: "inherit" });

// register the track + bed, and the licence row
const bedsFile = path.join(ROOT, "music/beds.json");
const beds = readJson(bedsFile);
beds.tracks[trackId] = {
  file: out,
  bpm: spec.bpm ?? 100,
  firstBeat: spec.offset ?? 0,
  map: `Eravue original (scripts/${path.basename(script)} + music/compositions/${slug}.json). ${spec.why ?? spec.map ?? ""}`.trim(),
};
beds.beds[slug] = { ...(beds.beds[slug] ?? {}), track: trackId, trimStart: 0, segments: [[null, null]], why: beds.beds[slug]?.why ?? "Original track composed for this video: section changes already land on the story moments (see the track map), so it plays straight through." };
write(bedsFile, beds);
const lic = path.join(ROOT, "music/LICENSES.md");
const licText = fs.readFileSync(lic, "utf8");
if (!licText.includes(`music/compositions/${slug}.json`)) {
  const d = new Date();
  const day = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  fs.appendFileSync(lic, `| ${spec.title ?? trackId} | Eravue (synthesised by \`scripts/${path.basename(script)}\`, arrangement \`music/compositions/${slug}.json\`) | n/a: generated in-house, no samples | Owned by Eravue | ${day} | yes | yes | none | ${slug} |
`);
}
console.log(`track -> ${out}; registered as "${trackId}" in music/beds.json and music/LICENSES.md`);

if (!args.includes("--no-bed")) {
  if (!fs.existsSync(p.voice)) console.warn(`no ${rel(p.voice)} yet, so no ducked bed. After the voice: node scripts/music-bed.mjs ${slug}`);
  else execFileSync("node", [path.join(ROOT, "scripts/music-bed.mjs"), slug], { stdio: "inherit" });
}
