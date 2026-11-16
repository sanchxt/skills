#!/usr/bin/env node
// Voiceover analysis + measured clean-up for eravue-motion videos.
//
//   node voice.mjs analyze <in> [--json r.json]        print a report and the chain it would apply
//   node voice.mjs process <in> <out.wav> [options]    analyse, build the chain, render, A/B, re-check
//
// Options for process:
//   --lufs -16        voice stem loudness (default -16; the final mix is mastered to -14 by master.mjs)
//   --tighten 0.45    shorten every pause longer than ~0.6 s to this many seconds (changes timing:
//                     do it BEFORE word alignment / captions)
//   --no-eq           only rumble cut, denoise (if needed), compression and loudness
//   --eq-strength 0.7 how much of the measured tonal difference to correct (0-1)
//   --ab <file.wav>   where to write the before/after (default <out>.ab.wav)
//   --words <file>    word timings JSON ([{w,t}] or a timing file with beats[].words) for a WPM figure
//
// Every move is measured, small and capped, so it stays the same voice. The A/B file is
// loudness-matched (louder always sounds "better", so never compare unmatched).
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { decode, fft, hann, db, percentile, measureLoudness, duration, ffmpeg } from "./audio-lib.mjs";

const SR = 48000, N = 4096, HOP = 2048;
const CENTERS = [63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500];
// Target tonal balance, dB per 1/3 octave relative to the 400-630 Hz average. Shaped on the long-term
// average speech spectrum (Byrne et al. 1994, male / female) with a small "polished voiceover" lift in
// presence (2.5-5 kHz) and air (8-10 kHz). It is a reference, not a law: the script only corrects part
// of any difference (eq-strength) and caps every move. Pick with --voice male|female (default male).
const TARGETS = {
  male: [-20, -15, -6, -2, -2, -1, 0, 0, 0, 0, -1, -3, -5, -8, -9, -10, -11, -12, -12, -13, -14, -15, -16, -18],
  female: [-28, -24, -18, -12, -6, -2, 0, 0, 0, 0, -1, -3, -5, -7, -8, -9, -10, -11, -11, -12, -13, -14, -15, -17],
};
let TARGET = TARGETS.male;
const idx = (f) => CENTERS.indexOf(f);

function analyze(file, wordsFile) {
  const x = decode(file, SR);
  const win = hann(N);
  const re = new Float64Array(N), im = new Float64Array(N);
  const bin = SR / N;
  const edges = CENTERS.map((c) => [Math.ceil((c * 2 ** (-1 / 6)) / bin), Math.floor((c * 2 ** (1 / 6)) / bin)]);
  const frames = [];
  let clipped = 0;
  for (let i = 0; i < x.length; i++) if (Math.abs(x[i]) >= 0.999) clipped++;
  for (let s = 0; s + N <= x.length; s += HOP) {
    let e = 0;
    for (let i = 0; i < N; i++) {
      const v = x[s + i];
      e += v * v;
      re[i] = v * win[i];
      im[i] = 0;
    }
    fft(re, im);
    const p = new Float64Array(N / 2);
    for (let k = 0; k < N / 2; k++) p[k] = re[k] * re[k] + im[k] * im[k];
    const sum = (a, b) => {
      let t = 0;
      for (let k = Math.max(1, Math.round(a / bin)); k <= Math.min(N / 2 - 1, Math.round(b / bin)); k++) t += p[k];
      return t;
    };
    frames.push({
      t: s / SR,
      rms: db(e / N),
      bands: edges.map(([a, b]) => {
        let t = 0;
        for (let k = a; k <= b; k++) t += p[k];
        return t;
      }),
      lf: sum(20, 90),
      mid: sum(500, 4000),
      sib: sum(5000, 10000),
      all: sum(30, 16000),
    });
  }
  const rmsAll = frames.map((f) => f.rms);
  const loud = percentile(rmsAll, 95);
  // noise floor from the quietest frames; a tightly edited stem has no real silence, so flag that
  const noise = percentile(rmsAll, 3);
  const noiseMeasurable = percentile(rmsAll, 50) - noise > 20;
  const gate = Math.max(noise + 10, loud - 28);
  const active = frames.filter((f) => f.rms > gate);
  const activeRms = active.map((f) => f.rms);
  const speechLevel = percentile(activeRms, 50);

  // long-term average spectrum over speech frames, relative to 400-630 Hz
  const ltas = CENTERS.map((_, b) => db(active.reduce((t, f) => t + f.bands[b], 0) / active.length));
  const ref = (ltas[idx(400)] + ltas[idx(500)] + ltas[idx(630)]) / 3;
  const rel = ltas.map((v) => +(v - ref).toFixed(1));
  const dev = rel.map((v, b) => +(v - TARGET[b]).toFixed(1));
  const region = (fs_) => +(fs_.reduce((t, f) => t + dev[idx(f)], 0) / fs_.length).toFixed(1);

  // sibilance: how far the loudest S's (97th pct of 5-10 kHz energy) sit above typical vowel energy (median 0.5-4 kHz)
  const sibRatio = percentile(active.map((f) => db(f.sib)), 97) - percentile(active.map((f) => db(f.mid)), 50);
  // plosive/handling bumps: speech frames whose 20-90 Hz energy jumps 12 dB over its usual level
  const lfMed = percentile(active.map((f) => db(f.lf)), 50);
  const plosive = active.filter((f) => db(f.lf) > lfMed + 12).length / active.length;
  // band-limited (phone codecs, some apps): almost nothing above 10 kHz
  const bandLimited = rel[idx(12500)] < -38;

  // pauses: runs of non-speech frames
  const pauses = [];
  let runStart = null;
  for (const f of frames) {
    const silent = f.rms < Math.max(noise + 8, gate - 6);
    if (silent && runStart === null) runStart = f.t;
    if (!silent && runStart !== null) {
      const d = f.t - runStart;
      if (d >= 0.7) pauses.push([+runStart.toFixed(2), +d.toFixed(2)]);
      runStart = null;
    }
  }

  const L = measureLoudness(file);
  const dur = duration(file);
  const gainToStem = -16 - L.I;
  const out = {
    file: path.resolve(file),
    duration: dur,
    loudness: { integratedLUFS: L.I, truePeak: L.TP, LRA: L.LRA },
    levels: { noiseMeasurable, noiseFloorDb: +noise.toFixed(1), speechDb: +speechLevel.toFixed(1), snrDb: +(speechLevel - noise).toFixed(1), noiseAfterNormalisationDb: +(noise + gainToStem).toFixed(1) },
    clippedSamples: clipped,
    speechRatio: +(active.length / frames.length).toFixed(2),
    longPauses: pauses,
    tone: {
      thirdOctave: Object.fromEntries(CENTERS.map((c, b) => [c, { level: rel[b], target: TARGET[b], diff: dev[b] }])),
      regions: {
        rumble_63_100: region([63, 80, 100]),
        warmth_125_160: region([125, 160]),
        mud_200_315: region([200, 250, 315]),
        nasal_1k_1k6: region([1000, 1250, 1600]),
        presence_2k5_4k: region([2500, 3150, 4000]),
        sibilance_5k_6k3: region([5000, 6300]),
        air_8k_10k: region([8000, 10000]),
      },
      bandLimited,
    },
    sibilancePeakDb: +sibRatio.toFixed(1),
    plosiveFrameShare: +plosive.toFixed(3),
  };
  if (wordsFile) {
    const j = JSON.parse(fs.readFileSync(wordsFile, "utf8"));
    const words = Array.isArray(j) ? j : (j.beats ?? []).flatMap((b) => b.words);
    if (words.length > 1) {
      const span = words[words.length - 1].t - words[0].t;
      out.pace = { words: words.length, wpm: Math.round((words.length / span) * 60) };
    }
  }
  return out;
}

function buildChain(a, { eq = true, strength = 0.7 } = {}) {
  const r = a.tone.regions;
  const notes = [];
  const f = [];
  // 1. rumble / plosives
  const hp = r.rumble_63_100 > 4 || a.plosiveFrameShare > 0.15 ? 95 : 80;
  f.push(`highpass=f=${hp}:p=2`);
  if (hp !== 80) notes.push(`rumble/plosive energy (${r.rumble_63_100} dB over, ${(a.plosiveFrameShare * 100).toFixed(1)}% plosive frames): high-pass at ${hp} Hz`);
  // 2. noise
  const nAfter = a.levels.noiseAfterNormalisationDb;
  if (!a.levels.noiseMeasurable) notes.push("noise floor not measurable (almost no pauses: an already-edited stem?), so no denoise. Analyse the raw take instead");
  else if (nAfter > -62) {
    const nf = Math.max(-80, Math.min(-20, Math.round(a.levels.noiseFloorDb)));
    const nr = nAfter > -50 ? 18 : 12;
    f.push(`afftdn=nf=${nf}:nr=${nr}:tn=1`);
    notes.push(`noise floor would sit at ${nAfter} dBFS after levelling: afftdn ${nr} dB`);
    if (nAfter > -45) notes.push("NOISY: consider re-recording closer to the mic in a soft room, or a local AI denoise (DeepFilterNet) / Adobe Podcast Enhance before this step");
  }
  if (a.clippedSamples > 50) notes.push(`CLIPPING: ${a.clippedSamples} clipped samples. Lower the input gain and re-record if it's audible; nothing downstream can fully fix it`);
  const cuts = [], boosts = [];
  if (eq) {
    const k = strength;
    const move = (d, max) => +Math.max(-max, Math.min(max, -d * k)).toFixed(1);
    if (r.warmth_125_160 > 2.5) cuts.push([`equalizer=f=140:t=o:w=1:g=${move(r.warmth_125_160, 3)}`, `boomy 125-160 Hz (+${r.warmth_125_160})`]);
    if (r.mud_200_315 > 1.5) {
      // centre the cut on the worst third-octave in the mud region
      const worst = [200, 250, 315].reduce((m, c) => (a.tone.thirdOctave[c].diff > a.tone.thirdOctave[m].diff ? c : m), 250);
      cuts.push([`equalizer=f=${worst}:t=o:w=1.2:g=${move(r.mud_200_315, 5)}`, `muddy low-mids around ${worst} Hz (+${r.mud_200_315})`]);
    }
    if (r.nasal_1k_1k6 > 2.5) cuts.push([`equalizer=f=1150:t=o:w=1:g=${move(r.nasal_1k_1k6, 3)}`, `nasal/honky 1-1.6 kHz (+${r.nasal_1k_1k6})`]);
    if (r.presence_2k5_4k > 3) cuts.push([`equalizer=f=3200:t=o:w=1.2:g=${move(r.presence_2k5_4k, 3)}`, `harsh presence (+${r.presence_2k5_4k})`]);
    if (r.presence_2k5_4k < -1.5) boosts.push([`equalizer=f=3500:t=o:w=1.3:g=${move(r.presence_2k5_4k, 4)}`, `dull presence (${r.presence_2k5_4k}): clarity boost at 3.5 kHz`]);
    if (r.air_8k_10k < -2 && !a.tone.bandLimited) boosts.push([`treble=f=8000:t=s:w=0.6:g=${move(r.air_8k_10k, 3)}`, `little air (${r.air_8k_10k}): shelf from 8 kHz`]);
    if (a.tone.bandLimited) notes.push("band-limited recording (phone codec?): no air boost, it would only lift hiss");
    for (const [, n] of [...cuts, ...boosts]) notes.push(n);
  }
  // 3. dynamics: gentle; loudnorm handles the overall level
  const ratio = a.loudness.LRA > 8 ? 3 : 2;
  const thrDb = Math.min(-10, a.levels.speechDb + 4);
  const comp = `acompressor=threshold=${Math.pow(10, thrDb / 20).toFixed(4)}:ratio=${ratio}:attack=8:release=140:knee=4:detection=rms`;
  // 4. sibilance: always light when we brighten, stronger when it measures hot
  const brightened = boosts.length > 0;
  const hotS = a.sibilancePeakDb > 0 || a.tone.regions.sibilance_5k_6k3 > 3;
  const deess = hotS ? "deesser=i=0.45:m=0.6:f=0.5" : brightened ? "deesser=i=0.3:m=0.5:f=0.5" : null;
  if (hotS) notes.push(`hot S's (S peaks ${a.sibilancePeakDb} dB vs vowels, S-band ${a.tone.regions.sibilance_5k_6k3}): stronger de-esser`);
  const chain = [...f, ...cuts.map((c) => c[0]), comp, ...boosts.map((b) => b[0]), ...(deess ? [deess] : [])];
  notes.push(`compression ${ratio}:1 above ${thrDb.toFixed(0)} dBFS (LRA ${a.loudness.LRA} LU)`);
  return { chain, notes };
}

function render(input, output, chain, lufs, tighten) {
  const pre = [];
  if (tighten) {
    const a = analyze(input);
    const thr = Math.round(Math.max(a.levels.noiseFloorDb + 10, a.levels.speechDb - 30));
    pre.push(`silenceremove=start_periods=1:start_threshold=${thr}dB:start_silence=0.15:stop_periods=-1:stop_duration=0.6:stop_threshold=${thr}dB:stop_silence=${tighten}:detection=rms`);
  }
  const base = [...pre, ...chain].join(",");
  // Static gain to the target, then a peak limiter at -2 dBFS (so the gain is never held back by
  // peaks, which is what loudnorm's linear mode does), then one correction pass.
  let gain = lufs - measureLoudness(input, base).I;
  for (let pass = 0; pass < 3; pass++) {
    const af = `${base},volume=${gain.toFixed(2)}dB,alimiter=limit=0.794:attack=3:release=60:level=false,aresample=48000`;
    ffmpeg(["-y", "-i", input, "-vn", "-af", af, "-ac", "1", "-c:a", "pcm_s24le", output]);
    const got = measureLoudness(output).I;
    if (Math.abs(got - lufs) <= 0.3) break;
    gain += lufs - got;
  }
}

function abFile(input, chain, lufs, out, dur) {
  const len = Math.min(10, Math.max(4, dur * 0.25));
  const st = Math.max(0, Math.min(dur - len, dur * 0.3));
  const fc = [
    `[0:a]atrim=${st}:${st + len},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,loudnorm=I=${lufs}:TP=-1.5,aresample=48000[a]`,
    `[0:a]atrim=${st}:${st + len},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,${chain.join(",")},loudnorm=I=${lufs}:TP=-1.5,aresample=48000[b]`,
    `anullsrc=r=48000:cl=mono,atrim=0:0.8[gap]`,
    `[a][gap][b]concat=n=3:v=0:a=1[out]`,
  ].join(";");
  ffmpeg(["-y", "-i", input, "-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s16le", out]);
  return { start: +st.toFixed(1), len: +len.toFixed(1) };
}

function printReport(a, title = "Voice report") {
  const r = a.tone.regions;
  const sign = (v) => (v > 0 ? `+${v}` : `${v}`);
  console.log(`\n${title}: ${path.basename(a.file)} (${a.duration}s)`);
  console.log(`  loudness   ${a.loudness.integratedLUFS} LUFS, true peak ${a.loudness.truePeak} dBTP, LRA ${a.loudness.LRA} LU`);
  console.log(`  noise      floor ${a.levels.noiseFloorDb} dBFS, speech ${a.levels.speechDb} dBFS, SNR ${a.levels.snrDb} dB (floor after levelling to -16: ${a.levels.noiseAfterNormalisationDb})`);
  console.log(`  tone vs target (dB):  rumble ${sign(r.rumble_63_100)} | warmth ${sign(r.warmth_125_160)} | mud ${sign(r.mud_200_315)} | nasal ${sign(r.nasal_1k_1k6)} | presence ${sign(r.presence_2k5_4k)} | S-band ${sign(r.sibilance_5k_6k3)} | air ${sign(r.air_8k_10k)}${a.tone.bandLimited ? "  [band-limited]" : ""}`);
  console.log(`  sibilance  S peaks ${a.sibilancePeakDb} dB vs vowels   plosive frames ${(a.plosiveFrameShare * 100).toFixed(1)}%   clipped samples ${a.clippedSamples}`);
  console.log(`  pacing     speech ${Math.round(a.speechRatio * 100)}% of the time, ${a.longPauses.length} pauses >= 0.7 s${a.pace ? `, ${a.pace.wpm} wpm` : ""}`);
}

// ---------------------------------------------------------------- CLI
const argv = process.argv.slice(2);
const flags = {};
const pos = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith("--")) {
    const k = argv[i].slice(2);
    const v = argv[i + 1];
    if (v === undefined || v.startsWith("--") || ["no-eq"].includes(k)) flags[k] = true;
    else flags[k] = argv[++i];
  } else pos.push(argv[i]);
}
const [cmd, input, output] = pos;
const opt = (name, def) => (flags[name] === undefined ? def : flags[name]);
if (!cmd || !input || !["analyze", "process"].includes(cmd)) {
  console.log("usage: node voice.mjs analyze <in> [--voice male|female] [--words w.json] [--json r.json]\n       node voice.mjs process <in> <out.wav> [--voice male|female] [--lufs -16] [--tighten 0.45] [--no-eq] [--eq-strength 0.7] [--ab file] [--words w.json]");
  process.exit(1);
}
TARGET = TARGETS[opt("voice", "male")] ?? TARGETS.male;
if (cmd === "analyze") {
  const a = analyze(input, opt("words"));
  printReport(a);
  const { chain, notes } = buildChain(a, { strength: +opt("eq-strength", 0.7) });
  console.log("\n  suggested fixes:");
  for (const n of notes) console.log(`   - ${n}`);
  console.log(`
  chain: ${chain.join(",")}`);
  if (opt("json")) fs.writeFileSync(opt("json"), JSON.stringify({ analysis: a, chain, notes }, null, 2));
} else {
  if (!output) throw new Error("process needs <out.wav>");
  const lufs = +opt("lufs", -16);
  const tighten = flags.tighten === undefined ? 0 : flags.tighten === true ? 0.45 : +flags.tighten;
  const a = analyze(input, opt("words"));
  printReport(a, "Before");
  const { chain, notes } = buildChain(a, { eq: !flags["no-eq"], strength: +opt("eq-strength", 0.7) });
  console.log("\n  applying:");
  for (const n of notes) console.log(`   - ${n}`);
  fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
  render(input, output, chain, lufs, tighten);
  const ab = opt("ab", output.replace(/\.wav$/i, "") + ".ab.wav");
  const w = abFile(input, chain, lufs, ab, a.duration);
  const after = analyze(output);
  printReport(after, "After");
  console.log(`
  wrote ${output}${tighten ? ` (pauses tightened to ${tighten}s: ${a.duration}s -> ${after.duration}s)` : ""}`);
  console.log(`  A/B: ${ab} = ${w.len}s from ${w.start}s, BEFORE, short gap, AFTER (both at ${lufs} LUFS)`);
  fs.writeFileSync(output.replace(/\.wav$/i, "") + ".voice.json", JSON.stringify({ before: a, chain, notes, after, lufs, tighten }, null, 2));
}
