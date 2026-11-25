// Start a new video in one command. Everything that is the same for every video is done here, so the work left is
// only the storyboard and the new animations:
//
//   pnpm new <slug> <clip.mp4 | voice.wav> [--name CompName] [--look paper] [--voice default|keep|crisp|warm|broadcast|<saved>]
//            [--set "clarity+=20"] [--caption paper-card] [--formats v,f] [--handle @lifewithcofounders] [--no-check]
//
//  1. a video clip  -> public/<slug>/source.mp4 (footage mode: the clip sits in a ClipFrame, graphics around it)
//     an audio file -> voiceover mode (graphics only)
//  2. the voice is cleaned with a ReelStudio voice profile (pnpm voice:profile; --voice keep = only level it)
//     -> public/<slug>/vo.wav at -16 LUFS
//  3. pnpm vo:sync: word timings (large-v3-turbo on the GPU), script.json (one beat per sentence) and timing.json
//  4. a second model (Whisper XXL medium.en) transcribes it too; every place they disagree goes to vo/<slug>/check.md
//     (names, numbers and tool names are where the first model slips; fix script.json, then pnpm vo:align <slug>)
//  5. src/videos/<slug>/<Name>.tsx + cues.ts from scripts/templates (kit imports, ClipFrame, Captions, LookBg, EndCard,
//     music, SFX and SafeZone already wired), registered in src/Root.tsx as <Name>-V/-F/-H
//  6. music/compositions/<slug>.plan.json (pnpm compose <slug> --init) for the original music
// Re-running on an existing slug redoes steps 1-4 (the media) and leaves your code alone.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { ROOT, paths, readJson, rel } from "./paths.mjs";

const args = process.argv.slice(2);
const flag = (n, d) => {
  const i = args.indexOf(`--${n}`);
  return i === -1 ? d : args[i + 1];
};
const pos = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--") && !["--no-check"].includes(args[i - 1])));
const [slug, media] = pos;
if (!slug || !media) throw new Error("usage: pnpm new <slug> <clip.mp4|voice.wav> [--name X] [--look paper] [--voice default] [--caption paper-card] [--formats v,f] [--handle @x]");
if (!fs.existsSync(media)) throw new Error(`No file ${media}`);
const p = paths(slug);
const pascal = slug.replace(/(^|-)([a-z0-9])/g, (_, __, c) => c.toUpperCase());
const name = flag("name", /^[0-9]/.test(pascal) ? `V${pascal}` : pascal);
const CONST = `${name.replace(/([a-z0-9])([A-Z])/g, "$1_$2").toUpperCase()}_FRAMES`;
const look = flag("look", "paper");
const voice = flag("voice", "default");
const formats = flag("formats", "v,f").split(",").map((s) => s.trim());
const lookFile = path.join(ROOT, "src/looks", `${look}.ts`);
if (!fs.existsSync(lookFile)) throw new Error(`No look "${look}" (src/looks: ${fs.readdirSync(path.join(ROOT, "src/looks")).filter((f) => !["index.ts", "types.ts"].includes(f)).map((f) => f.replace(".ts", "")).join(", ")})`);
const run = (cmd, a, opts = {}) => execFileSync(cmd, a, { stdio: "inherit", cwd: ROOT, ...opts });
const node = (script, a) => run(process.execPath, [path.join(ROOT, "scripts", script), ...a]);
const probe = (f) => JSON.parse(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height", "-of", "json", f]).toString());
const step = (n, s) => console.log(`\n[${n}/6] ${s}`);

// 1. media
const info = probe(media);
const isVideo = info.streams.some((s) => s.codec_type === "video" && !["mjpeg", "png"].includes(s.codec_name));
fs.mkdirSync(p.pub, { recursive: true });
let clipDur = null;
if (isVideo) {
  step(1, "footage -> public/" + slug + "/source.mp4");
  const dst = path.join(p.pub, "source.mp4");
  const v = info.streams.find((s) => s.codec_type === "video");
  if (path.extname(media).toLowerCase() === ".mp4" && v.codec_name === "h264") fs.copyFileSync(media, dst);
  else run("ffmpeg", ["-v", "error", "-y", "-i", media, "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", dst]);
  clipDur = +info.format.duration;
} else step(1, "voiceover mode (no clip)");

// 2. voice
step(2, `voice: profile "${voice}"`);
node("voice-profile.mjs", [slug, media, "--profile", voice, ...(flag("set") ? ["--set", flag("set")] : [])]);

// 3. timings
step(3, "word timings (vo:sync)");
node("sync-vo.mjs", [slug]);
const timing = readJson(p.timing);

// 4. second-model check
const checkFile = path.join(p.vo, "check.md");
if (!args.includes("--no-check")) {
  step(4, "second model cross-check -> " + rel(checkFile));
  const bak = [p.words, p.timing].map((f) => [f, fs.readFileSync(f)]);
  try {
    node("sync-vo.mjs", [slug, "--engine", "xxl"]);
    fs.copyFileSync(p.words, path.join(p.vo, "words-check.json"));
    writeCheck(readJson(path.join(p.vo, "words-check.json")));
  } catch (e) {
    console.warn(`! second model failed (${e.message.split("\n")[0]}); skipped the check`);
  } finally {
    for (const [f, b] of bak) fs.writeFileSync(f, b);
  }
} else step(4, "check skipped");

// 5. scaffold
step(5, "scaffold");
const tsx = path.join(p.dir, `${name}.tsx`);
const cuesFile = path.join(p.dir, "cues.ts");
if (fs.existsSync(tsx) || fs.existsSync(cuesFile)) console.log(`${rel(p.dir)} already has code; left it alone`);
else {
  const fill = (tpl, map) => Object.entries(map).reduce((s, [k, v]) => s.split(`__${k}__`).join(v), fs.readFileSync(path.join(ROOT, "scripts/templates", tpl), "utf8"));
  const beats = timing.beats.map((b) => `  ${/^[a-z_$][\w$]*$/i.test(b.id) ? b.id : JSON.stringify(b.id)}: cue(${JSON.stringify(b.id)}), // ${b.words.slice(0, 7).map((w) => w.w).join(" ")}`).join("\n");
  const common = { SLUG: slug, NAME: name, CONST, LOOK: look };
  fs.writeFileSync(
    cuesFile,
    fill("cues.ts.tpl", {
      ...common,
      BEATS: beats,
      VIDEO_END: clipDur ? `Math.round(${clipDur.toFixed(2)} * FPS)` : `Math.round(${timing.duration.toFixed(2)} * FPS)`,
      END_WHY: clipDur ? `the source clip's length, ${clipDur.toFixed(2)} s` : `the end of the voice, ${timing.duration.toFixed(2)} s`,
    }),
  );
  fs.writeFileSync(
    tsx,
    fill("Video.tsx.tpl", {
      ...common,
      CAPTION: flag("caption", look === "paper" ? (isVideo ? "paper-card" : "editorial") : "chunk"),
      SOURCE: isVideo ? JSON.stringify(`${slug}/source.mp4`) : "null",
      END_HEADLINE: "TODO headline",
      END_CTA: "TODO",
      HANDLE: flag("handle", "@eravuedotcom"),
    }),
  );
  // register in Root.tsx
  const rootFile = path.join(ROOT, "src/Root.tsx");
  let root = fs.readFileSync(rootFile, "utf8");
  if (!root.includes(`./videos/${slug}/`)) {
    const imp = `import { ${name}, ${CONST} } from "./videos/${slug}/${name}";\n`;
    const lines = root.split("\n");
    const last = lines.map((l, i) => (l.startsWith("import ") && l.includes("./videos/") ? i : -1)).filter((i) => i >= 0).pop();
    lines.splice(last + 1, 0, imp.trimEnd());
    root = lines.join("\n");
    const reg = `    {formats("${name}", ${name}, ${CONST}, [${formats.map((f) => JSON.stringify(f)).join(", ")}])}\n`;
    const marker = root.indexOf("    {/* new videos go here");
    root = marker >= 0 ? root.slice(0, marker) + reg + root.slice(marker) : root.replace("  </>\n);", `${reg}  </>\n);`);
    fs.writeFileSync(rootFile, root);
  }
  console.log(`wrote ${rel(tsx)}, ${rel(cuesFile)}; registered ${formats.map((f) => `${name}-${f.toUpperCase()}`).join(", ")}`);
}

// 6. music plan
step(6, "music plan");
if (!fs.existsSync(path.join(ROOT, "music/compositions", `${slug}.plan.json`)) && !fs.existsSync(path.join(ROOT, "music/compositions", `${slug}.json`))) node("compose.mjs", [slug, "--init"]);

console.log(`
Ready. Next:
  1. read ${rel(checkFile)} (if any) and fix script.json spellings, then: pnpm vo:align ${slug}
  2. storyboard the beats in cues.ts; build scenes from the kit (KIT.md) in ${rel(tsx)}
  3. set the music moments in music/compositions/${slug}.plan.json, then: pnpm compose ${slug}
  4. pnpm stills ${name}-V <frames> --safe   ->   pnpm ship ${slug}`);

// ---------- helpers ----------
function writeCheck(other) {
  const norm = (s) => s.toLowerCase().replace(/[’']/g, "").replace(/[^a-z0-9]+/g, "");
  const A = readJson(p.words).map((w) => ({ ...w, n: norm(w.word) })).filter((w) => w.n);
  const B = other.map((w) => ({ ...w, n: norm(w.word) })).filter((w) => w.n);
  // LCS alignment, then report each run where the two disagree
  const n = A.length;
  const m = B.length;
  const L = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i][j] = A[i].n === B[j].n ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
  const diffs = [];
  let i = 0;
  let j = 0;
  let cur = null;
  const flush = () => {
    if (cur && (cur.a.length || cur.b.length)) diffs.push(cur);
    cur = null;
  };
  while (i < n || j < m) {
    if (i < n && j < m && A[i].n === B[j].n) {
      flush();
      i++;
      j++;
    } else {
      cur ??= { t: (A[i] ?? B[j] ?? A[n - 1]).start, a: [], b: [] };
      if (j >= m || (i < n && L[i + 1][j] >= L[i][j + 1])) cur.a.push(A[i++].word.trim());
      else cur.b.push(B[j++].word.trim());
    }
  }
  flush();
  const t = (s) => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, "0")}`;
  const body = diffs.length
    ? diffs.map((d) => `| ${t(d.t)} | ${d.a.join(" ") || "(nothing)"} | ${d.b.join(" ") || "(nothing)"} |`).join("\n")
    : "| | (the two models agree on every word) | |";
  fs.writeFileSync(
    checkFile,
    `# ${slug}: transcript check\n\nturbo (used) vs Whisper XXL medium.en. Agreement ${Math.round((L[0][0] / Math.max(n, 1)) * 100)}% of ${n} words. Listen at each time and fix script.json if turbo is wrong (spelling always comes from script.json), then \`pnpm vo:align ${slug}\`.\n\n| at | turbo (in script.json) | medium.en |\n|---|---|---|\n${body}\n`,
  );
  console.log(`${diffs.length} disagreement(s) -> ${rel(checkFile)}`);
}
