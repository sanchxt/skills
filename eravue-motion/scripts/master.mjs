#!/usr/bin/env node
// Final check + loudness master for a rendered video.
//
//   node master.mjs <in.mp4> [out.mp4] [--lufs -14] [--tp -1] [--check]
//
// --check only reports. Otherwise the audio is brought to the target (static gain + true-peak-safe
// limiter, re-measured) and the video stream is copied untouched. The report covers the specs
// platforms care about: size/ratio, fps, codec, length, audio rate/loudness/peaks.
import { spawnSync } from "node:child_process";
import { measureLoudness, ffmpeg } from "./audio-lib.mjs";

const args = process.argv.slice(2);
const pos = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--") && args[i - 1] !== "--check"));
const flag = (n, d) => {
  const i = args.indexOf(`--${n}`);
  return i === -1 ? d : args[i + 1];
};
const [input, outArg] = pos;
if (!input) {
  console.log("usage: node master.mjs <in.mp4> [out.mp4] [--lufs -14] [--tp -1] [--check]");
  process.exit(1);
}
const lufs = +flag("lufs", -14), tp = +flag("tp", -1);
const probe = JSON.parse(
  spawnSync("ffprobe", ["-v", "error", "-show_streams", "-show_format", "-of", "json", input], { encoding: "utf8" }).stdout,
);
const v = probe.streams.find((s) => s.codec_type === "video");
const a = probe.streams.find((s) => s.codec_type === "audio");
const dur = +(+probe.format.duration).toFixed(2);
const warn = [];
console.log(`\n${input}`);
if (v) {
  const [n, d] = v.r_frame_rate.split("/").map(Number);
  const fps = +(n / d).toFixed(2);
  const ratio = v.width / v.height;
  const name = Math.abs(ratio - 9 / 16) < 0.01 ? "9:16" : Math.abs(ratio - 4 / 5) < 0.01 ? "4:5" : Math.abs(ratio - 1) < 0.01 ? "1:1" : Math.abs(ratio - 16 / 9) < 0.01 ? "16:9" : ratio.toFixed(3);
  console.log(`  video  ${v.width}x${v.height} (${name}), ${fps} fps, ${v.codec_name} ${v.pix_fmt}, ${Math.round(+probe.format.bit_rate / 1000)} kb/s total, ${dur}s`);
  if (v.codec_name !== "h264" && v.codec_name !== "hevc") warn.push(`video codec ${v.codec_name}: export H.264 for uploads`);
  if (v.pix_fmt !== "yuv420p") warn.push(`pixel format ${v.pix_fmt}: use yuv420p or some players show it wrong`);
  if (name === "9:16" && v.width < 1080) warn.push("vertical below 1080x1920");
  if (![24, 25, 30, 60, 29.97, 59.94].includes(fps)) warn.push(`unusual frame rate ${fps}`);
} else warn.push("no video stream");
if (!a) {
  warn.push("no audio stream");
} else {
  const L = measureLoudness(input);
  console.log(`  audio  ${a.codec_name} ${a.sample_rate} Hz ${a.channels}ch, ${L.I} LUFS, true peak ${L.TP} dBTP, LRA ${L.LRA} LU`);
  const off = Math.abs(L.I - lufs) > 0.5 || L.TP > tp;
  if (args.includes("--check")) {
    if (off) warn.push(`loudness ${L.I} LUFS / ${L.TP} dBTP vs target ${lufs} / ${tp}: run without --check to master it`);
  } else {
    const out = outArg ?? input.replace(/(\.\w+)$/, "-master$1");
    let gain = lufs - L.I;
    for (let pass = 0; pass < 3; pass++) {
      // limiter ceiling 1 dB under the true-peak target leaves room for inter-sample peaks
      const lim = Math.pow(10, (tp - 1) / 20).toFixed(3);
      ffmpeg(["-y", "-i", input, "-map", "0:v?", "-map", "0:a", "-c:v", "copy", "-af", `volume=${gain.toFixed(2)}dB,alimiter=limit=${lim}:attack=2:release=50:level=false,aresample=48000`, "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", out]);
      const M = measureLoudness(out);
      console.log(`  pass ${pass + 1}: ${M.I} LUFS, ${M.TP} dBTP`);
      if (Math.abs(M.I - lufs) <= 0.3 && M.TP <= tp + 0.1) break;
      gain += lufs - M.I;
    }
    console.log(`  wrote ${out}`);
  }
}
for (const w of warn) console.log(`  ! ${w}`);
if (!warn.length) console.log("  specs OK");
