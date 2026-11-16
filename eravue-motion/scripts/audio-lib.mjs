// Shared helpers for the eravue-motion audio scripts. No npm dependencies: needs the full
// ffmpeg/ffprobe build on PATH (loudnorm, sidechaincompress, deesser, afftdn).
import { spawnSync, execFileSync } from "node:child_process";

/** Decode any audio/video file to mono float32 samples at `rate` Hz. */
export function decode(file, rate = 48000) {
  const r = spawnSync("ffmpeg", ["-v", "error", "-i", file, "-vn", "-ac", "1", "-ar", String(rate), "-f", "f32le", "-"], {
    maxBuffer: 1024 * 1024 * 1024,
  });
  if (r.status !== 0) throw new Error(`ffmpeg decode failed for ${file}:\n${r.stderr}`);
  const buf = r.stdout;
  return new Float32Array(buf.buffer, buf.byteOffset, Math.floor(buf.byteLength / 4));
}

/** In-place iterative radix-2 FFT. re/im are Float64Array of length 2^k. */
export function fft(re, im) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      [re[i], re[j]] = [re[j], re[i]];
      [im[i], im[j]] = [im[j], im[i]];
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = (-2 * Math.PI) / len;
    const wr = Math.cos(ang), wi = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let cr = 1, ci = 0;
      for (let k = 0; k < len / 2; k++) {
        const a = i + k, b = a + len / 2;
        const tr = re[b] * cr - im[b] * ci, ti = re[b] * ci + im[b] * cr;
        re[b] = re[a] - tr; im[b] = im[a] - ti;
        re[a] += tr; im[a] += ti;
        const ncr = cr * wr - ci * wi;
        ci = cr * wi + ci * wr; cr = ncr;
      }
    }
  }
}

export const hann = (n) => Float64Array.from({ length: n }, (_, i) => 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / (n - 1)));
export const db = (x) => 10 * Math.log10(Math.max(x, 1e-20));
export const percentile = (arr, p) => {
  const s = Float64Array.from(arr).sort();
  return s[Math.min(s.length - 1, Math.max(0, Math.round((p / 100) * (s.length - 1))))];
};

/** ffmpeg loudnorm measurement (integrated LUFS, true peak, LRA, threshold, offset). */
export function measureLoudness(file, extraFilter = "") {
  const af = (extraFilter ? extraFilter + "," : "") + "loudnorm=print_format=json";
  const r = spawnSync("ffmpeg", ["-hide_banner", "-nostats", "-i", file, "-vn", "-af", af, "-f", "null", "-"], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) throw new Error(r.stderr);
  const j = JSON.parse(r.stderr.slice(r.stderr.lastIndexOf("{"), r.stderr.lastIndexOf("}") + 1));
  return { I: +j.input_i, TP: +j.input_tp, LRA: +j.input_lra, thresh: +j.input_thresh, offset: +j.target_offset, raw: j };
}

export function duration(file) {
  const r = spawnSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file], { encoding: "utf8" });
  return +(+r.stdout.trim()).toFixed(3);
}

export function ffmpeg(args) {
  execFileSync("ffmpeg", ["-hide_banner", "-v", "error", ...args], { stdio: "inherit" });
}
