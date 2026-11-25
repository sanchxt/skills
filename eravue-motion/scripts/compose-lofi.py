"""Original lo-fi piano bed, synthesised from scratch (no samples, so no licence questions: Eravue owns it).

    python scripts/compose-lofi.py music/compositions/<slug>.json <out.wav>

The arrangement JSON gives bpm, offset (s of bar 0), the chord per bar (cycled), a list of sections
[fromBar, toBar, [parts]] (bars may be fractional, e.g. 15.5) and the final chord bar. Parts:
piano, piano_soft, hats, kick, snare, bass, arp, pad, riser, crackle. Needs numpy only.
Bar lines are planned against timing.json so drops land on story moments (see music/beds.json "why").
"""
import json
import sys

import numpy as np

SR = 48000
rng = np.random.default_rng(7)

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def hz(name):
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((NOTE[n] + 12 * (o + 1) - 69) / 12)


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    s = 0.0
    # vectorised enough for our sizes via lfilter-like loop in chunks
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s
        y[i] = s
    return y


def lp_fft(x, fc, order=2):
    """Zero-phase-ish lowpass in the frequency domain (fast for long buffers)."""
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


def env_adr(n, a=0.004, rel=0.25, total=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    if total is not None:
        e *= np.clip((total + rel - t) / rel, 0, 1)
    return e


def piano(f, dur, vel):
    """Felt-ish piano: inharmonic partials with per-partial decay, two detuned strings, soft hammer."""
    length = dur + 1.2
    n = int(length * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    B = 0.00035
    bright = 0.6 + 0.4 * vel
    for k in range(1, 10):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 7000:
            break
        amp = (1 / k ** 1.7) * (bright ** (k - 1))
        dec = np.exp(-t * (0.9 + 0.55 * k) * (f / 260) ** 0.35)
        for det in (-0.7, 0.7):
            out += amp * dec * np.sin(2 * np.pi * fk * (1 + det / 1731) * t + rng.uniform(0, 6.28))
    hammer = rng.standard_normal(int(0.012 * SR)) * np.exp(-np.arange(int(0.012 * SR)) / (0.003 * SR)) * 0.08
    out[: len(hammer)] += hammer
    out *= env_adr(n, 0.006, 0.35, dur)
    return out * vel * 0.18


def pluck(f, vel):
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    x = sum((1 / k ** 2) * np.sin(2 * np.pi * k * f * t) for k in (1, 3, 5)) * np.exp(-t * 7)
    return x * env_adr(n, 0.003) * vel * 0.07


def pad(fs, dur):
    n = int((dur + 1.0) * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in fs:
        for det in (-4, 0, 4):
            x += np.sin(2 * np.pi * f * (1 + det / 1731) * t) + 0.25 * np.sin(4 * np.pi * f * (1 + det / 1731) * t)
    e = np.clip(t / 1.2, 0, 1) * np.clip((dur + 1.0 - t) / 1.0, 0, 1)
    return x * e * 0.012


def kick(vel=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 46 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t * 7.5) + 0.25 * rng.standard_normal(n) * np.exp(-t * 250)
    return np.tanh(x * 1.6) * vel * 0.42


def snare(vel=1.0):
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    noise = hp_fft(lp_fft(noise, 5200), 900)
    x = noise * np.exp(-t * 16) * 0.5 + np.sin(2 * np.pi * 185 * t) * np.exp(-t * 30) * 0.35
    return x * vel * 0.32


def hat(vel=1.0):
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    x = hp_fft(rng.standard_normal(n), 7000) * np.exp(-t * 70)
    return x * vel * 0.07


def bass(f, dur, vel=1.0):
    n = int((dur + 0.2) * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(4 * np.pi * f * t)
    x *= np.exp(-t * 1.2) * env_adr(n, 0.01, 0.12, dur)
    return np.tanh(x * 1.3) * vel * 0.30


def reverb_ir(seconds=1.8, seed=3):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = r.standard_normal((2, n)) * np.exp(-t * 3.4)
    ir = np.stack([lp_fft(ir[0], 3800), lp_fft(ir[1], 3800)])
    ir[:, : int(0.012 * SR)] = 0
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))


def convolve(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[: len(x)]
    return y


def main():
    cfg = json.load(open(sys.argv[1]))
    out_path = sys.argv[2]
    bpm, off = cfg["bpm"], cfg["offset"]
    beat = 60 / bpm
    bar = beat * 4
    total = cfg["length"]
    N = int(total * SR)
    bus = {k: np.zeros((2, N)) for k in ("piano", "drums", "bass", "arp", "pad", "fx")}
    chords = cfg["chords"]  # [{ "bass": "F2", "notes": ["F3","A3","C4","E4"] }]

    def at(b):
        return off + b * bar

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

    def parts_at(b):
        ps = set()
        for a, z, parts in cfg["sections"]:
            if a <= b < z:
                ps |= set(parts)
        return ps

    swing = cfg.get("swing", 0.06) * beat
    nbars = int(np.ceil((total - off) / bar))
    for bi in range(-1, nbars):
        ch = chords[bi % len(chords)]
        for step in range(8):  # eighth notes
            b = bi + step / 8
            ps = parts_at(b)
            t = at(b) + (swing if step % 2 else 0)
            vel_h = 0.9 if step % 2 == 0 else 0.6
            if "hats" in ps:
                add("drums", hat(vel_h), t + rng.normal(0, 0.003), 0.3)
            if "kick" in ps and step in (0, 5):
                add("drums", kick(1.0 if step == 0 else 0.8), t)
            if "snare" in ps and step in (2, 6):
                add("drums", snare(0.95 if step == 2 else 1.0), t + rng.normal(0, 0.004), -0.05)
            if "bass" in ps and step in (0, 5):
                f = hz(ch["bass"])
                add("bass", bass(f, beat * (2.4 if step == 0 else 1.4)), t)
            if "arp" in ps:
                notes = ch["notes"] + [ch["notes"][1]]
                f = hz(notes[step % len(notes)]) * 2
                add("arp", pluck(f, 0.9 if step % 2 == 0 else 0.6), t, 0.35 if step % 2 else -0.35)
            soft = "piano_soft" in ps
            if ("piano" in ps or soft) and step in (0, 3, 6):
                v = (0.55 if soft else 0.75) * (1.0 if step == 0 else 0.55)
                notes = ch["notes"] if step == 0 else ch["notes"][1:]
                dur = beat * (1.4 if step == 0 else 0.9)
                for k, nm in enumerate(notes):
                    roll = k * 0.018 if step == 0 else k * 0.006
                    add("piano", piano(hz(nm), dur, v * rng.uniform(0.9, 1.05)), t + roll, -0.4 + 0.8 * k / max(1, len(notes) - 1))
            if "pad" in ps and step == 0:
                add("pad", pad([hz(n) for n in ch["notes"]], bar), t)

    # riser into each drop
    for t_drop in cfg.get("risers", []):
        d = 1.6
        n = int(d * SR)
        tt = np.arange(n) / SR
        x = rng.standard_normal(n)
        x = hp_fft(lp_fft(x, 2500), 300) * (tt / d) ** 2.2 * 0.09
        add("fx", x, t_drop - d)

    # final chord
    fb = cfg["finalBar"]
    fch = cfg["finalChord"]
    for k, nm in enumerate(fch["notes"]):
        add("piano", piano(hz(nm), 3.0, 0.7), at(fb) + k * 0.03, -0.4 + 0.8 * k / (len(fch["notes"]) - 1))
    add("bass", bass(hz(fch["bass"]), 2.5, 0.9), at(fb))

    # mix
    ir = reverb_ir()
    def verb(st, mix):
        wet = np.stack([convolve(st[0], ir[0]), convolve(st[1], ir[1])])
        return st + wet * mix

    piano_b = verb(bus["piano"], 0.32)
    arp_b = verb(bus["arp"], 0.45)
    pad_b = verb(bus["pad"], 0.5)
    drums = bus["drums"]
    drums = np.stack([lp_fft(drums[0], 6500), lp_fft(drums[1], 6500)])  # dusty top
    mix = piano_b * 1.0 + drums * 0.9 + bus["bass"] * 0.9 + arp_b * 0.8 + pad_b + bus["fx"]

    # lo-fi: gentle tape wow (tiny time-varying delay), soft saturation, crackle + hiss
    t = np.arange(N) / SR
    wow = (0.0016 * np.sin(2 * np.pi * 0.55 * t) + 0.0006 * np.sin(2 * np.pi * 3.1 * t)) * SR
    idx = np.clip(np.arange(N) - 80 - wow, 0, N - 1)
    i0 = idx.astype(int)
    fr = idx - i0
    i1 = np.minimum(i0 + 1, N - 1)
    mix = mix[:, i0] * (1 - fr) + mix[:, i1] * fr
    mix = np.tanh(mix * 1.4) / 1.4
    if cfg.get("crackle", True):
        cr = np.zeros(N)
        k = rng.integers(0, N, int(total * 9))
        cr[k] = rng.uniform(-1, 1, len(k)) * rng.uniform(0.2, 1, len(k)) ** 3
        cr = hp_fft(lp_fft(cr, 5000), 800) * 0.25
        hiss = hp_fft(lp_fft(rng.standard_normal(N), 9000), 2000) * 0.0025
        mix += cr + hiss
    mix = np.stack([lp_fft(mix[0], 11000), lp_fft(mix[1], 11000)])
    mix = np.stack([hp_fft(mix[0], 35), hp_fft(mix[1], 35)])
    # fade tail
    fade = np.clip((total - t) / 2.0, 0, 1)
    mix *= fade
    mix /= np.max(np.abs(mix)) / 0.89
    pcm = (mix.T * 32767).astype(np.int16)

    import wave
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"wrote {out_path}: {total:.2f}s, {bpm} BPM, bar {bar:.3f}s from {off}s")


if __name__ == "__main__":
    main()
