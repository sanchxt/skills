// Render a finished video to platform-ready files in one command:
//
//   pnpm ship <slug> [--comp ElevenPm-V] [--crf 17] [--version v2] [--props '{"captionStyle":"reel:boxed"}']
//
// For each format registered for <slug> in src/Root.tsx (or just --comp):
//   render (Remotion, temp files on D:) -> H.264 yuv420p (Remotion writes full-range yuvj420p, which some apps
//   show washed out) -> pnpm master (-14 LUFS, -1 dBTP; the video stream is copied) -> master --check (the spec
//   report) -> a 6-frame contact sheet -> E:/video-edits/eravue-motion/<slug>/<slug>-<v|f|h>-<version>-final.mp4.
// The version counts up by itself (v1, v2, ...) unless --version is given. Look at the contact sheet before posting.
import "./tmp-dir.mjs";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { ROOT, paths, rel } from "./paths.mjs";

const OUT_DIR = process.env.ERAVUE_DELIVER_DIR ?? "E:/video-edits/eravue-motion";
const args = process.argv.slice(2);
const flag = (n, d) => {
  const i = args.indexOf(`--${n}`);
  return i === -1 ? d : args[i + 1];
};
const slug = args.find((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--")));
const p = paths(slug);
const run = (cmd, a) => execFileSync(cmd, a, { stdio: "inherit", cwd: ROOT });

// which compositions belong to this slug: the formats(...) line of the component imported from ./videos/<slug>/
const root = fs.readFileSync(path.join(ROOT, "src/Root.tsx"), "utf8");
let comps;
if (flag("comp")) comps = [flag("comp")];
else {
  const imp = root.match(new RegExp(`import \\{\\s*(\\w+)[^}]*\\} from "\\./videos/${slug}/`));
  if (!imp) throw new Error(`No composition imported from ./videos/${slug}/ in src/Root.tsx; pass --comp`);
  const reg = root.match(new RegExp(`formats\\("(\\w+)",\\s*${imp[1]},\\s*\\w+(?:,\\s*\\[([^\\]]*)\\])?\\)`));
  if (!reg) throw new Error(`${imp[1]} is not registered with formats(...) in src/Root.tsx`);
  const fm = reg[2] ? [...reg[2].matchAll(/"(\w)"/g)].map((m) => m[1]) : ["v", "f", "h"];
  comps = fm.map((f) => `${reg[1]}-${f.toUpperCase()}`);
}

const dest = path.join(OUT_DIR, slug);
fs.mkdirSync(dest, { recursive: true });
fs.mkdirSync(p.out, { recursive: true });
const version =
  flag("version") ??
  `v${1 + Math.max(0, ...fs.readdirSync(dest).map((f) => +(f.match(/-v(\d+)-final\.mp4$/)?.[1] ?? 0)))}`;

const done = [];
for (const comp of comps) {
  const fmt = comp.split("-").pop().toLowerCase();
  const base = path.join(p.out, `${slug}-${fmt}`);
  console.log(`\n=== ${comp} -> ${slug}-${fmt}-${version}-final.mp4`);
  run(process.execPath, [
    path.join(ROOT, "scripts/remotion.mjs"),
    "render",
    "src/index.ts",
    comp,
    `${base}-raw.mp4`,
    "--crf",
    flag("crf", "17"),
    ...(flag("props") ? ["--props", flag("props")] : []),
  ]);
  run("ffmpeg", ["-v", "error", "-y", "-i", `${base}-raw.mp4`, "-vf", "scale=in_range=full:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", flag("crf", "17"), "-preset", "slow", "-c:a", "copy", "-movflags", "+faststart", `${base}-420.mp4`]);
  const final = `${base}-${version}-final.mp4`;
  run(process.execPath, [path.join(ROOT, "scripts/master.mjs"), `${base}-420.mp4`, final]);
  run(process.execPath, [path.join(ROOT, "scripts/master.mjs"), final, "--check"]);
  // contact sheet: 6 frames across the video
  const dur = +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final]).toString().trim();
  const sheet = `${base}-${version}-sheet.jpg`;
  run("ffmpeg", ["-v", "error", "-y", "-i", final, "-vf", `fps=${(6 / dur).toFixed(5)},scale=360:-1,tile=6x1:padding=6:color=white`, "-frames:v", "1", sheet]);
  const to = path.join(dest, path.basename(final));
  fs.copyFileSync(final, to);
  for (const f of [`${base}-raw.mp4`, `${base}-420.mp4`]) fs.rmSync(f, { force: true });
  done.push([to, sheet]);
}
console.log("\nShipped:");
for (const [f, s] of done) console.log(`  ${f.replace(/\\/g, "/")}\n    contact sheet: ${rel(s)}`);
