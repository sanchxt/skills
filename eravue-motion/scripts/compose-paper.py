"""Original "paper" bed: marimba, felt keys, music box, pizzicato bass, brushes and a wooden clock tick.
Synthesised from scratch (numpy only, no samples), so Eravue owns it and it is cleared for ads too.

    python -I scripts/compose-paper.py music/compositions/<slug>.json <out.wav>

Unlike compose-lofi.py this one has NO fixed tempo. The arrangement lists sections with their real start
and end times (taken from timing.json), and a number of beats per section; every section's tempo is
(end - start) / beats, so a section change lands exactly on the story moment it belongs to. Keep the
beats chosen so the tempo stays within about 92-108 BPM and the join is inaudible under a voice.

Section: { name, a, b, beats, prog: [chord per bar, cycled], layers: [[fromBar, toBar, [parts]]],
           melody?: [[beat, note, beats], ...] (marimba), box?: [[beat, note], ...] (music box) }
Parts: pad bass kick brush shaker tick comp arp keys fill
Top level: length, sections, finalAt (s), finalChord, hits: [[t, kind]] kinds: boom chime, risers: [t_hit, ...]
"""
import json
import sys
import wave

import numpy as np

SR = 48000
rng = np.random.default_rng(11)
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def hz(name):
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((NOTE[n] + 12 * (o + 1) - 69) / 12)


CHORDS = {
    "Cmaj7": ("C2", ["G3", "B3", "E4", "G4"]),
    "Am7": ("A2", ["C4", "E4", "G4", "A4"]),
    "Fmaj7": ("F2", ["A3", "C4", "E4", "G4"]),
    "G6": ("G2", ["B3", "D4", "E4", "G4"]),
    "Em7": ("E2", ["G3", "B3", "D4", "G4"]),
    "Dm7": ("D2", ["A3", "C4", "F4", "A4"]),
    "Am9": ("A2", ["C4", "E4", "G4", "B4"]),
    "Cadd9": ("C2", ["G3", "D4", "E4", "G4"]),
}


def lp_fft(x, fc, order=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / fc) ** (2 * order))
    return np.fft.irfft(X, len(x))


def hp_fft(x, fc, order=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    with np.errstate(divide="ignore"):
        g = 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order))
    X *= g
    return np.fft.irfft(X, len(x))


def atk(n, a):
    return np.minimum(1, np.arange(n) / SR / max(a, 1e-4))


def marimba(f, vel=1.0, dur=1.3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 5.2)
    x += 0.42 * np.sin(2 * np.pi * 4.0 * f * t) * np.exp(-t * 20)
    x += 0.10 * np.sin(2 * np.pi * 9.8 * f * t) * np.exp(-t * 45)
    click = rng.standard_normal(int(0.006 * SR)) * np.exp(-np.arange(int(0.006 * SR)) / (0.0015 * SR)) * 0.06
    x[: len(click)] += click
    return x * atk(n, 0.002) * vel * 0.22


def keys(f, vel=1.0, dur=2.2):
    """Felt piano-ish: a few harmonics, soft hammer, slow decay."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k, a in ((1, 1.0), (2, 0.42), (3, 0.2), (4, 0.08)):
        for det in (-0.5, 0.5):
            x += a * np.sin(2 * np.pi * k * f * (1 + det / 1731) * t) * np.exp(-t * (1.1 + 0.9 * k))
    x = lp_fft(x, 2600)
    return x * atk(n, 0.008) * np.clip((dur - t) / 0.4, 0, 1) * vel * 0.16


def box(f, vel=1.0, dur=2.6):
    """Music box: bell partials 1 / 2.76 / 5.4 with long, soft decay."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.6)
    x += 0.30 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 4.2)
    x += 0.10 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 9)
    return x * atk(n, 0.003) * vel * 0.15


def pizz(f, dur, vel=1.0):
    n = int((dur + 0.15) * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6)
    x *= np.exp(-t * 3.6) * atk(n, 0.006) * np.clip((dur + 0.15 - t) / 0.12, 0, 1)
    return np.tanh(x * 1.2) * vel * 0.30


def pad(notes, dur):
    n = int((dur + 1.2) * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for nm in notes:
        f = hz(nm)
        for det in (-5, 0, 5):
            ph = rng.uniform(0, 6.28)
            x += np.sin(2 * np.pi * f * (1 + det / 1731) * t + ph) + 0.2 * np.sin(4 * np.pi * f * (1 + det / 1731) * t + ph)
    x = lp_fft(x, 1700)
    e = np.clip(t / 0.9, 0, 1) * np.clip((dur + 1.2 - t) / 1.1, 0, 1)
    return x * e * 0.0105


def kick(vel=1.0):
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    f = 44 + 70 * np.exp(-t * 30)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    return np.tanh(x * 1.3) * vel * 0.34


def brush(vel=1.0):
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    x = hp_fft(lp_fft(rng.standard_normal(n), 7000), 1800)
    e = np.minimum(1, t / 0.012) * np.exp(-t * 17)
    return x * e * vel * 0.20


def shaker(vel=1.0):
    n = int(0.07 * SR)
    t = np.arange(n) / SR
    x = hp_fft(rng.standard_normal(n), 6500)
    return x * np.minimum(1, t / 0.008) * np.exp(-t * 55) * vel * 0.05


def tick(vel=1.0, tock=False):
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    f = 1050 if tock else 1500
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 70) + 0.5 * np.sin(2 * np.pi * f * 1.51 * t) * np.exp(-t * 110)
    x += rng.standard_normal(n) * np.exp(-t * 400) * 0.25
    return x * vel * 0.16


def chime(f, vel=1.0):
    n = int(2.4 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.9) + 0.35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 4.5)
    return x * atk(n, 0.002) * vel * 0.12


def boom(vel=1.0):
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 66 * t) * np.exp(-t * 2.6) + 0.3 * lp_fft(rng.standard_normal(n), 400) * np.exp(-t * 6)
    return np.tanh(x) * atk(n, 0.01) * vel * 0.34


def riser(d):
    n = int(d * SR)
    t = np.arange(n) / SR
    s = t / d
    x = hp_fft(lp_fft(rng.standard_normal(n), 3000), 400) * s ** 2.4 * 0.08
    f = 260 + 620 * s ** 2
    x += np.sin(2 * np.pi * np.cumsum(f) / SR) * s ** 3 * 0.035
    return x


def reverb_ir(seconds=1.9, seed=5):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = r.standard_normal((2, n)) * np.exp(-t * 3.2)
    ir = np.stack([lp_fft(ir[0], 4200), lp_fft(ir[1], 4200)])
    ir[:, : int(0.014 * SR)] = 0
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))


def convolve(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[: len(x)]


def main():
    cfg = json.load(open(sys.argv[1]))
    out_path = sys.argv[2]
    total = cfg["length"]
    N = int(total * SR)
    bus = {k: np.zeros((2, N)) for k in ("mal", "keys", "box", "drums", "bass", "pad", "fx")}

    def add(name, sig, t0, pan=0.0):
        i = int(round(t0 * SR))
        if i >= N or i + len(sig) <= 0:
            return
        j = min(N, i + len(sig))
        s = sig[: j - i] if i >= 0 else sig[-i : j - i]
        i = max(i, 0)
        lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        bus[name][0, i : i + len(s)] += s * lg * 1.414
        bus[name][1, i : i + len(s)] += s * rg * 1.414

    for sec in cfg["sections"]:
        a, b, nb = sec["a"], sec["b"], sec["beats"]
        beat = (b - a) / nb
        bt = lambda x: a + x * beat  # noqa: E731  (beat position within the section -> seconds)
        nbars = int(np.ceil(nb / 4))
        prog = sec["prog"]
        sw = 0.05 * beat

        def parts_at(bar):
            ps = set()
            for fr, to, parts in sec["layers"]:
                if fr <= bar < to:
                    ps |= set(parts)
            return ps

        for bi in range(nbars):
            ch = CHORDS[prog[bi % len(prog)]]
            ps = parts_at(bi)
            bar_beats = min(4, nb - bi * 4)
            if "pad" in ps:
                add("pad", pad(ch[1][:3] + [ch[0].replace("2", "3")], bar_beats * beat), bt(bi * 4), 0)
            for step in range(int(bar_beats * 2)):  # eighths
                bpos = bi * 4 + step / 2
                t = bt(bpos) + (sw if step % 2 else 0)
                downbeat = step % 2 == 0
                if "shaker" in ps:
                    add("drums", shaker(0.9 if downbeat else 0.55), t + rng.normal(0, 0.002), 0.25)
                if "kick" in ps and step in (0, 4):
                    add("drums", kick(1.0 if step == 0 else 0.7), t)
                if "brush" in ps and step in (2, 6):
                    add("drums", brush(1.0), t + rng.normal(0, 0.003), -0.1)
                if "tick" in ps and downbeat:
                    add("fx", tick(0.8, tock=(step // 2) % 2 == 1), t, -0.2 if (step // 2) % 2 == 0 else 0.2)
                if "bass" in ps and step in (0, 5):
                    add("bass", pizz(hz(ch[0]), beat * (1.6 if step == 0 else 0.9), 1.0 if step == 0 else 0.75), t)
                if "arp" in ps:
                    notes = [hz(n_) * 2 for n_ in ch[1]]
                    pat = [0, 1, 2, 3, 2, 1, 2, 1]
                    add("mal", marimba(notes[pat[step % 8]], 0.85 if downbeat else 0.55), t, -0.4 if downbeat else 0.4)
                if "comp" in ps and step in (0, 3, 6):
                    v = 0.65 if step == 0 else 0.42
                    for k, nm in enumerate(ch[1][1:] if step else ch[1]):
                        add("mal", marimba(hz(nm) * 2, v * rng.uniform(0.9, 1.05), 1.1), t + k * 0.012, -0.3 + 0.2 * k)
                if "keys" in ps and step in (0, 4):
                    for k, nm in enumerate(ch[1]):
                        add("keys", keys(hz(nm), (0.75 if step == 0 else 0.5) * rng.uniform(0.92, 1.05), beat * 2.6), t + k * 0.016, -0.35 + 0.23 * k)
            if "fill" in ps and bi == nbars - 1:
                for k in range(4):  # quick rising marimba fill into the next section
                    nm = ch[1][k % 4]
                    add("mal", marimba(hz(nm) * 2 * (1 if k < 3 else 2), 0.6), bt(nb - 1.5 + k * 0.375), -0.3 + 0.2 * k)
        for bpos, nm, dur in sec.get("melody", []):
            add("mal", marimba(hz(nm), 0.9, 1.4), bt(bpos), 0.15)
        for bpos, nm in sec.get("box", []):
            add("box", box(hz(nm), 0.9), bt(bpos), 0.2)

    for t_hit in cfg.get("risers", []):
        d = 1.5
        add("fx", riser(d), t_hit - d)
    for t_h, kind in cfg.get("hits", []):
        if kind == "boom":
            add("fx", boom(), t_h)
        else:
            add("fx", chime(hz("C6")), t_h, 0.2)

    ft = cfg["finalAt"]
    for k, nm in enumerate(["C3", "G3", "E4", "B4", "G5"]):
        add("keys", keys(hz(nm), 0.9, 3.6), ft + k * 0.03, -0.4 + 0.2 * k)
    add("bass", pizz(hz("C2"), 2.4, 0.9), ft)

    ir = reverb_ir()

    def verb(st, mix):
        wet = np.stack([convolve(st[0], ir[0]), convolve(st[1], ir[1])])
        return st + wet * mix

    mix = (
        verb(bus["mal"], 0.34) * 1.0
        + verb(bus["keys"], 0.30) * 1.0
        + verb(bus["box"], 0.5) * 1.0
        + bus["drums"] * 0.85
        + bus["bass"] * 0.9
        + verb(bus["pad"], 0.5)
        + verb(bus["fx"], 0.35)
    )
    mix = np.tanh(mix * 1.15) / 1.15
    mix = np.stack([lp_fft(mix[0], 12000), lp_fft(mix[1], 12000)])
    mix = np.stack([hp_fft(mix[0], 58, 3), hp_fft(mix[1], 58, 3)])
    t = np.arange(N) / SR
    mix *= np.clip((total - t) / 1.2, 0, 1) * np.clip(t / 0.05, 0, 1)
    mix /= np.max(np.abs(mix)) / 0.89
    pcm = (mix.T * 32767).astype(np.int16)
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"wrote {out_path}: {total:.2f}s")


if __name__ == "__main__":
    main()
