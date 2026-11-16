#!/usr/bin/env node
// Beat grid + section map for a music track, so cuts and reveals can land on the music.
//
//   node beats.mjs <track.mp3> [--json out.json] [--bpm 75] [--bars 4]
//
// Prints BPM, the first beat, and a bar-by-bar energy map with the likely drops (big energy
// rise), breakdowns (big fall) and the outro. Use the result to fill music/beds.json (bpm,
// firstBeat, segments) for music-bed.mjs. If the BPM looks half/double of what you hear, pass
// --bpm to force it (the grid phase is still detected). Always confirm the drops by ear.
import fs from "node:fs";
import path from "node:path";
import { decode, fft, hann, db, percentile } from "./audio-lib.mjs";

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith("--") && !/^-?\d/.test(a));
const flag = (n) => {
  const i = args.indexOf(`--${n}`);
  return i === -1 ? undefined : args[i + 1];
};
if (!file) {
  console.log("usage: node beats.mjs <track> [--json out.json] [--bpm N] [--bars 4]");
  process.exit(1);
}
const SR = 22050, N = 1024, HOP = 256;
const fps = SR / HOP;
const x = decode(file, SR);
const win = hann(N);
const re = new Float64Array(N), im = new Float64Array(N);
let prev = new Float64Array(N / 2);
const env = [], rms = [], low = [];
for (let s = 0; s + N <= x.length; s += HOP) {
  let e = 0;
  for (let i = 0; i < N; i++) {
    const v = x[s + i];
    e += v * v;
    re[i] = v * win[i];
    im[i] = 0;
  }
  fft(re, im);
  let flux = 0, lowE = 0;
  const mag = new Float64Array(N / 2);
  for (let k = 1; k < N / 2; k++) {
    mag[k] = Math.log1p(100 * Math.hypot(re[k], im[k]));
    const d = mag[k] - prev[k];
    if (d > 0) flux += d;
    if (k * (SR / N) < 150) lowE += re[k] * re[k] + im[k] * im[k];
  }
  prev = mag;
  env.push(flux);
  rms.push(e / N);
  low.push(lowE);
}
// detrend the onset envelope (subtract a ~0.5 s moving mean) and half-wave rectify
const W = Math.round(fps * 0.5);
const on = env.map((v, i) => {
  let t = 0, c = 0;
  for (let j = Math.max(0, i - W); j <= Math.min(env.length - 1, i + W); j++) (t += env[j]), c++;
  return Math.max(0, v - t / c);
});
const at = (t) => {
  // linear interpolation of the envelope at fractional frame t
  const i = Math.floor(t), f = t - i;
  return i + 1 < on.length ? on[i] * (1 - f) + on[i + 1] * f : 0;
};
// comb score of a (period, phase) pair: mean envelope on the beat grid
const comb = (P, phi) => {
  let t = 0, c = 0;
  for (let k = phi; k < on.length - 1; k += P) (t += at(k)), c++;
  return t / c;
};
const bestPhase = (P) => {
  let best = [0, -1];
  for (let phi = 0; phi < P; phi += 0.25) {
    const sc = comb(P, phi);
    if (sc > best[1]) best = [phi, sc];
  }
  return best;
};

let bpm;
const forced = flag("bpm");
const candidates = [];
if (forced) bpm = +forced;
else {
  // autocorrelation over 60-180 BPM with a mild preference for 80-130
  const acf = (lag) => {
    let t = 0;
    const L = Math.floor(lag), f = lag - L;
    for (let i = 0; i + L + 1 < on.length; i++) t += on[i] * (on[i + L] * (1 - f) + on[i + L + 1] * f);
    return t;
  };
  for (let b = 60; b <= 180; b += 0.5) {
    const lag = (60 / b) * fps;
    const prior = Math.exp(-0.5 * Math.pow(Math.log2(b / 105) / 0.9, 2));
    // reward lags whose double also correlates (true beat periods repeat)
    candidates.push({ bpm: b, score: (acf(lag) + 0.5 * acf(lag * 2)) * prior });
  }
  candidates.sort((a, b) => b.score - a.score);
  bpm = candidates[0].bpm;
}
// refine tempo finely with the comb (precision matters across a 2-minute track)
let best = { bpm, phi: 0, sc: -1 };
for (let b = bpm * 0.985; b <= bpm * 1.015; b += 0.02) {
  const P = (60 / b) * fps;
  const [phi, sc] = bestPhase(P);
  if (sc > best.sc) best = { bpm: b, phi, sc };
}
bpm = +best.bpm.toFixed(2);
const beatSec = 60 / bpm;
let firstBeat = best.phi / fps;
const beatsPerBar = +(flag("bars") ?? 4);

// energy per bar
const dur = x.length / SR;
const nBeats = Math.floor((dur - firstBeat) / beatSec);
const bars = [];
for (let b = 0; b + beatsPerBar <= nBeats; b += beatsPerBar) {
  const t0 = firstBeat + b * beatSec, t1 = t0 + beatsPerBar * beatSec;
  const i0 = Math.floor(t0 * fps), i1 = Math.floor(t1 * fps);
  let e = 0, l = 0, o = 0;
  for (let i = i0; i < i1; i++) (e += rms[i]), (l += low[i]), (o += on[i]);
  bars.push({ bar: b / beatsPerBar, beat: b, t: +t0.toFixed(2), db: +db(e / (i1 - i0)).toFixed(1), lowDb: +db(l / (i1 - i0)).toFixed(1), hits: +(o / (i1 - i0)).toFixed(2) });
}
const loudBar = percentile(bars.map((b) => b.db), 90);
// outro: from the last bar where it stays 6 dB under the loud level
let outro = null;
for (let i = bars.length - 1; i >= 0 && bars[i].db < loudBar - 6; i--) outro = bars[i];
const raw = [];
for (let i = 1; i < bars.length; i++) {
  if (outro && bars[i].beat >= outro.beat) break;
  const before = bars.slice(Math.max(0, i - 2), i);
  const avg = before.reduce((t, b) => t + b.db, 0) / before.length;
  const avgLow = before.reduce((t, b) => t + b.lowDb, 0) / before.length;
  const d = bars[i].db - avg, dl = bars[i].lowDb - avgLow;
  if (d > 3 || dl > 6) raw.push({ type: "drop", i, ...bars[i], change: +d.toFixed(1) });
  else if (d < -3 || dl < -6) raw.push({ type: "breakdown", i, ...bars[i], change: +d.toFixed(1) });
}
// a change usually spans 2-3 bars: a drop is reported at its biggest rise (with where the build
// started), a breakdown at its first bar
const events = [];
for (let k = 0; k < raw.length; ) {
  let j = k;
  while (j + 1 < raw.length && raw[j + 1].type === raw[k].type && raw[j + 1].i === raw[j].i + 1) j++;
  const run = raw.slice(k, j + 1);
  if (raw[k].type === "drop") {
    const peak = run.reduce((m, e) => (e.change > m.change ? e : m));
    events.push({ ...peak, buildFrom: run[0].beat < peak.beat ? run[0].t : undefined });
  } else events.push(run[0]);
  k = j + 1;
}
if (outro) events.push({ type: "outro", ...outro });
for (const e of events) delete e.i;

const report = {
  track: path.resolve(file),
  duration: +dur.toFixed(2),
  bpm,
  firstBeat: +firstBeat.toFixed(3),
  beatSec: +beatSec.toFixed(4),
  beatsPerBar,
  altBpm: forced ? undefined : [+(bpm / 2).toFixed(2), +(bpm * 2).toFixed(2)],
  candidates: forced ? undefined : candidates.slice(0, 5).map((c) => c.bpm),
  bars,
  events,
};
console.log(`${path.basename(file)}: ${report.duration}s, ${bpm} BPM (beat ${report.beatSec}s, bar ${(beatSec * beatsPerBar).toFixed(2)}s), first beat ${report.firstBeat}s`);
if (!forced) console.log(`  other tempo readings: ${report.candidates.join(", ")} (half/double: ${report.altBpm.join(" / ")})`);
console.log("\n  bar  beat     time   level  bass   hits");
const evAt = new Map(events.map((e) => [e.beat, e]));
for (const b of bars) {
  const e = evAt.get(b.beat);
  const bar = "#".repeat(Math.max(0, Math.round((b.db - (loudBar - 24)) / 1.5)));
  console.log(`  ${String(b.bar).padStart(3)}  ${String(b.beat).padStart(4)}  ${b.t.toFixed(2).padStart(7)}s  ${b.db.toFixed(1).padStart(6)}  ${b.lowDb.toFixed(1).padStart(6)}  ${b.hits.toFixed(2).padStart(5)}  ${bar.padEnd(16)} ${e ? "<- " + e.type.toUpperCase() + (e.buildFrom !== undefined ? ` (build from ${e.buildFrom}s)` : "") : ""}`);
}
if (flag("json")) fs.writeFileSync(flag("json"), JSON.stringify(report, null, 2));
