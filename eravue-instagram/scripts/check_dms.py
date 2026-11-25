#!/usr/bin/env python3
"""Validate an Instagram lead/DM batch JSON before it reaches the founders.

Usage:  python check_dms.py <leads.json> [--legacy]
Exit 0 = pass. Exit 1 = errors (fix them and re-run). Warnings never fail the run.

Every subagent that drafts DMs must run this and get a PASS before handing back.
--legacy skips the fields added on 2026-11-17 (last_post, ad_text) for older files.

Each lead is an object:
  h, name, niche, service, loc, score (1-5), via, signal, angle,
  A: [label, text], B: [label, text], ready, reply, verify,
  last_post: "YYYY-MM-DD" (date of the newest organic post you actually read),
  ad_text: "the ad line you read, or '' if no ad"
"""
import csv, difflib, json, re, sys
from datetime import date, datetime
from pathlib import Path

LEADS_CSV = Path("D:/projects/eravue-portfolio/.outreach/leads.csv")
REQUIRED = ["h", "name", "niche", "service", "loc", "score", "via", "signal", "angle", "A", "B", "ready", "reply", "verify"]
NEW_REQUIRED = ["last_post", "ad_text"]
SERVICES = {"ai-chat-agents", "ai-voice-agents", "lead-followup", "ai-automation", "crm", "erp-internal-tools", "website",
            "apps", "brand-design", "social-media", "video-editing", "ai-content", "seo", "other"}
SENSITIVE = re.compile(r"spell|black magic|vashikaran|love problem|tantrik|casino|betting|loan|crypto|escort|massage parlou?r", re.I)
MOJIBAKE = re.compile(r"[\u00c2\u00c3\u00e2][\u0080-\u00bf\u201a\u201e\u0152\u2122\u20ac]|\ufffd")


def strip_quotes(t):
    """Remove quoted ad/caption lines so their words don't trip style rules."""
    return re.sub(r"(?<!\w)'.{3,}?'(?!\w)|\"[^\"]{3,}\"|\u2018[^\u2019]{3,}\u2019|\u201c[^\u201d]{3,}\u201d", " ", t)


def tracked_handles():
    out = set()
    if LEADS_CSV.exists():
        for r in csv.DictReader(open(LEADS_CSV, encoding="utf-8")):
            for k in ("handle", "url"):
                v = (r.get(k) or "").lower().strip().rstrip("/").split("/")[-1].lstrip("@")
                if v:
                    out.add(v)
    return out


def check_dm(t):
    errs, warns = [], []
    n = len(t)
    bare = strip_quotes(t)
    if not 120 <= n <= 230:
        errs.append(f"length {n} (must be 120-230)")
    if t.count("?") > 1:
        errs.append(f"{t.count('?')} question marks (max 1 question per DM)")
    if t.count("?") == 0:
        warns.append("no question: end with one clear question")
    if re.search(r"https?://|www\.|\.(com|in|io|co)\b|wa\.me|@\w", t, re.I):
        errs.append("link, domain or @mention (no links in a first DM)")
    if re.search(r"(\+?91[\s-]?)?\b\d{10}\b|\b\d{5}[\s-]\d{5}\b", t):
        errs.append("phone number in DM")
    if re.search(r"\b(we|we've|we're|our|ours|us)\b", bare, re.I):
        errs.append("uses we/our/us outside a quote (founders write as 'I')")
    if re.search(r"\u20b9|\brs\.?\s?\d|\binr\b|\$\s?\d|\bprice list\b", bare, re.I):
        errs.append("price or currency in DM")
    if MOJIBAKE.search(t):
        errs.append("broken characters (encoding); write UTF-8 and avoid symbols")
    if len(re.findall(r"\bfree\b", bare, re.I)) > 1:
        errs.append("'free' used twice (say it once: 'a free mockup, no strings attached')")
    if re.search(r"\bI(?:'ve)? (made|built|created|prepared|designed) (you|a|an|one|this|your|something)\b", bare, re.I) and \
            not re.search(r"demo", t, re.I):
        errs.append("claims a sample already exists; offer it instead ('I can make...')")
    if re.search(r"\b(dm|message) (me|us) (back )?(at|on)\b|call me", bare, re.I):
        warns.append("asks them to contact elsewhere; keep it in the DM")
    if re.search(r"^(hi|hey|hello) team [a-z]", t):
        errs.append("greeting 'hi team <name>' reads oddly; use 'hi <Brand> team' with the brand capitalised")
    if not re.match(r"(?i)(hi|hey|hello|helloo|namaste)\b", t):
        warns.append("doesn't open with a greeting (founders always greet)")
    if re.search(r"\b(must|surely|definitely) (pour|be flooded|get tons|vary a lot)", bare, re.I):
        warns.append("guesses about their business; state what you saw instead")
    if re.search(r"amazing|stunning|gorgeous|love your|lovely", bare, re.I):
        warns.append("generic compliment: make it specific or drop it")
    return errs, warns


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    path, legacy = Path(sys.argv[1]), "--legacy" in sys.argv
    raw = path.read_bytes()
    if raw[:3] == b"\xef\xbb\xbf":
        print("ERROR file has a UTF-8 BOM; write plain UTF-8"); sys.exit(1)
    data = json.loads(raw.decode("utf-8"))
    tracked, seen = tracked_handles(), {}
    n_err = n_warn = 0
    for i, x in enumerate(data, 1):
        h = str(x.get("h", "")).lstrip("@").lower()
        errs, warns = [], []
        for k in REQUIRED + ([] if legacy else NEW_REQUIRED):
            if k not in x or x[k] in (None, "") and k not in ("verify", "ad_text"):
                errs.append(f"missing field {k}")
        if h in tracked:
            errs.append("already in the tracker (leads.py)")
        if h in seen:
            errs.append(f"duplicate of lead #{seen[h]}")
        seen[h] = i
        if not isinstance(x.get("score"), int) or not 1 <= x["score"] <= 5:
            errs.append("score must be an integer 1-5")
        elif x["score"] < 3:
            errs.append("score below 3: drop the lead")
        bad = [s for s in str(x.get("service", "")).split("|") if s and s not in SERVICES]
        if bad:
            errs.append(f"unknown service slug {bad}")
        blob = " ".join(str(x.get(k, "")) for k in ("name", "niche", "signal", "angle", "verify"))
        if SENSITIVE.search(blob):
            errs.append("sensitive/off-limits business (occult, gambling, loans, adult...): drop")
        if MOJIBAKE.search(json.dumps(x, ensure_ascii=False)):
            errs.append("broken characters somewhere in the lead (encoding)")
        if not legacy and x.get("last_post"):
            try:
                age = (date.today() - datetime.strptime(x["last_post"], "%Y-%m-%d").date()).days
                if age > 60:
                    errs.append(f"last organic post {age} days ago (max 60): drop")
                elif age > 30:
                    warns.append(f"last organic post {age} days ago")
            except ValueError:
                errs.append("last_post must be YYYY-MM-DD (the date you actually read)")
        texts = {}
        for k in "AB":
            v = x.get(k)
            if not (isinstance(v, list) and len(v) == 2 and isinstance(v[1], str)):
                errs.append(f"{k} must be [label, text]"); continue
            texts[k] = v[1]
            e, w = check_dm(v[1])
            errs += [f"DM {k}: {m}" for m in e]
            warns += [f"DM {k}: {m}" for m in w]
        if len(texts) == 2:
            ratio = difflib.SequenceMatcher(None, texts["A"].lower(), texts["B"].lower()).ratio()
            if ratio > 0.75:
                errs.append(f"A and B too similar ({ratio:.2f}); use a different hook/offer")
        for e in errs:
            print(f"ERROR #{i} @{h}: {e}")
        for w in warns:
            print(f"warn  #{i} @{h}: {w}")
        n_err += len(errs); n_warn += len(warns)
    print(f"\n{len(data)} leads, {n_err} errors, {n_warn} warnings -> {'PASS' if n_err == 0 else 'FAIL'}")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
