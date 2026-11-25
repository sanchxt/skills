// Voice clean-up with the SAME filters and saved profiles as ReelStudio (its tools/voice.py + brand/voice-profiles.json).
// One set of voice settings for both projects: a profile saved here is saved in ReelStudio, and the other way round.
//
//   pnpm voice:profile list                                   the saved profiles
//   pnpm voice:profile <slug> <media> --profile warm          clean <media> (video or audio) with a profile -> public/<slug>/vo.wav
//   pnpm voice:profile <slug> <media> --profile crisp --set "clarity+=20 air=10"   profile + tone knobs on top
//   pnpm voice:profile <slug> <media> --profile keep          already finished (e.g. cut + cleaned in ReelStudio): only level it
//   pnpm voice:profile <slug> --set "warmth+=15"              re-tune the last run (no media needed)
//   pnpm voice:profile <slug> ab                              10 s before/after files to listen to (in ReelStudio's project)
//   pnpm voice:profile <slug> save <id> "description"         save the current settings as a new shared profile
//
// Knobs (percent, -100..100): clarity warmth presence air; processing: autoEq deess compression denoise target gate.
// The stem is levelled to -16 LUFS (the studio's voice standard) after ReelStudio's chain.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { paths, ensureDir, rel } from "./paths.mjs";

const RS = process.env.REELSTUDIO_DIR ?? "D:/projects/SOCIAL MEDIA/short-form-quick-edits";
const args = process.argv.slice(2);
const flag = (n) => {
  const i = args.indexOf(`--${n}`);
  return i === -1 ? undefined : args[i + 1];
};
const pos = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--")));
const py = (...a) => execFileSync("node", ["scripts/py.mjs", ...a], { cwd: RS, stdio: "inherit" });
const ff = (...a) => execFileSync("ffmpeg", ["-v", "error", "-y", ...a], { stdio: "inherit" });

if (pos[0] === "list" || pos[0] === "profiles") {
  py("voice", "profiles");
  process.exit(0);
}
const [slug, second, third, fourth] = pos;
const p = paths(slug);
const project = `eravue-${slug}`;
const pdir = path.join(RS, "projects", project);
const src = path.join(pdir, "source");

if (second === "ab") {
  py("voice", project, "ab");
  process.exit(0);
}
if (second === "save") {
  if (!third) throw new Error('Usage: pnpm voice:profile <slug> save <id> "description"');
  py("voice", project, "save-profile", third, ...(fourth ? [fourth] : []));
  process.exit(0);
}

const media = second;
const profile = flag("profile");
const set = flag("set");
ensureDir(p.voice);

if (media) {
  if (!fs.existsSync(media)) throw new Error(`No file ${media}`);
  // keep a raw copy next to the working files, so the voice can be redone any time
  const raw = path.join(p.vo, "raw.wav");
  ensureDir(raw);
  ff("-i", media, "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", raw);
  if (profile === "keep") {
    ff("-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", p.voice);
    console.log(`kept the sound as is, levelled to -16 LUFS -> ${rel(p.voice)}`);
    process.exit(0);
  }
  // a minimal ReelStudio project so its voice tool can run on this audio (same layout as its ingest)
  fs.mkdirSync(src, { recursive: true });
  fs.copyFileSync(raw, path.join(src, "audio.wav"));
  ff("-i", path.join(src, "audio.wav"), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", path.join(src, "audio16k.wav"));
  fs.writeFileSync(path.join(pdir, "notes.md"), `Voice-only project made by eravue-motion (pnpm voice:profile ${slug}). Safe to delete; it is rebuilt on the next run.\n`);
}
if (!fs.existsSync(path.join(src, "audio.wav"))) throw new Error(`No voice project for ${slug} yet. Pass the media: pnpm voice:profile ${slug} <file> --profile <id>`);

if (profile && profile !== "keep") py("voice", project, "profile", profile, ...(set ? ["--no-apply"] : []));
if (set) py("voice", project, "set", ...set.split(/\s+/).filter(Boolean));
if (!profile && !set) py("voice", project, "apply");

const clean = path.join(src, "audio_clean.wav");
if (!fs.existsSync(clean)) throw new Error("ReelStudio did not write audio_clean.wav; see the messages above.");
ff("-i", clean, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", p.voice);
fs.copyFileSync(path.join(pdir, "voice.json"), path.join(p.vo, "voice-settings.json"));
console.log(`\nvoice -> ${rel(p.voice)} (-16 LUFS). Report: ${path.join(src, "cleanup.md")}. Listen: pnpm voice:profile ${slug} ab`);
