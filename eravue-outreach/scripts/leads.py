#!/usr/bin/env python3
"""Eravue outreach lead tracker.

One CSV ledger (.outreach/leads.csv) for every channel, so nobody is pitched twice
and follow-ups don't slip. Every change is appended to .outreach/log.csv.
Standard library only. Run from anywhere; data lives at <repo>/.outreach/ unless
--data-dir or ERAVUE_OUTREACH_DIR says otherwise.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

FIELDS = [
    "id", "added", "channel", "kind", "service", "market", "name", "company",
    "handle", "url", "email", "phone", "location", "signal", "angle", "score",
    "status", "owner", "touches", "last_touch", "next_due", "notes",
]
LOG_FIELDS = ["timestamp", "id", "action", "detail"]

STATUSES = [
    "new", "shortlisted", "contacted", "replied", "call_booked", "proposal",
    "won", "lost", "no_reply", "skipped", "avoid", "do_not_contact",
]
TERMINAL = {"won", "lost", "no_reply", "skipped", "avoid", "do_not_contact"}
PRE_CONTACT = {"new", "shortlisted"}
KINDS = ["inbound", "outbound", "warm", "partner"]
MARKETS = ["IN", "INTL"]
SERVICES = [
    "ai-chat-agents", "ai-voice-agents", "lead-followup", "ai-automation", "crm",
    "erp-internal-tools", "website", "apps", "brand-design", "social-media",
    "video-editing", "ai-content", "seo", "other",
]
# Days until the next follow-up after touch 1, 2, 3. After the 4th touch: suggest no_reply.
CADENCE = [3, 4, 7]
MAX_TOUCHES = len(CADENCE) + 1

# Hosts where the URL identifies a post/profile, not a business: dedupe on full URL.
PLATFORM_HOSTS = {
    "reddit.com", "x.com", "twitter.com", "instagram.com", "linkedin.com",
    "facebook.com", "fb.com", "upwork.com", "contra.com", "fiverr.com",
    "freelancer.com", "peopleperhour.com", "truelancer.com", "youtube.com",
    "youtu.be", "threads.net", "threads.com", "news.ycombinator.com",
    "indiehackers.com", "wellfound.com", "quora.com", "google.com",
    "maps.google.com", "goo.gl", "maps.app.goo.gl", "wa.me", "linktr.ee",
    "discord.com", "craigslist.org", "medium.com", "github.com",
}
HANDLE_CHANNELS = {"x": "x", "twitter": "x", "instagram": "instagram",
                   "reddit": "reddit", "linkedin": "linkedin", "threads": "threads"}


# ---------- paths & io ----------

def data_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg).resolve()
    env = os.environ.get("ERAVUE_OUTREACH_DIR")
    if env:
        return Path(env).resolve()
    # <repo>/.claude/skills/eravue-outreach/scripts/leads.py -> parents[4] == <repo>
    return Path(__file__).resolve().parents[4] / ".outreach"


def today() -> dt.date:
    override = os.environ.get("ERAVUE_TODAY")  # for tests
    return dt.date.fromisoformat(override) if override else dt.date.today()


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in FIELDS:
            r.setdefault(k, "")
            if r[k] is None:
                r[k] = ""
    return rows


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".leads-", suffix=".csv")
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


def log(ddir: Path, lead_id: str, action: str, detail: str = "") -> None:
    path = ddir / "log.csv"
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerow({"timestamp": dt.datetime.now().isoformat(timespec="seconds"),
                    "id": lead_id, "action": action, "detail": detail})


# ---------- normalisation & dedupe ----------

def norm_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    if "://" not in url:
        url = "https://" + url
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    for prefix in ("www.", "m.", "old.", "new.", "mobile."):
        if host.startswith(prefix):
            host = host[len(prefix):]
    if host == "twitter.com":
        host = "x.com"
    path = parts.path.rstrip("/").lower()
    if host == "redd.it" and path:
        return f"reddit.com/comments{path}"
    if host == "reddit.com":
        # /r/<sub>/comments/<post>[/<slug>[/<comment>]] -> reddit.com/comments/<post>[/<comment>]
        m = re.match(r"(?:/r/[^/]+)?/comments/([a-z0-9]+)(?:/[^/]*(?:/([a-z0-9]+))?)?", path)
        if m:
            return "reddit.com/comments/" + m.group(1) + (f"/{m.group(2)}" if m.group(2) else "")
    if host == "x.com":
        m = re.match(r"/[^/]+/status/(\d+)", path)
        if m:
            return f"x.com/status/{m.group(1)}"
    return f"{host}{path}"


def url_host(normalised: str) -> str:
    return normalised.split("/", 1)[0]


def is_platform(host: str) -> bool:
    return any(host == h or host.endswith("." + h) for h in PLATFORM_HOSTS)


def norm_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    return digits[-10:] if len(digits) >= 10 else digits


def norm_handle(handle: str) -> str:
    return handle.strip().lstrip("@").lower().removeprefix("u/")


def keys_for(row: dict) -> set[str]:
    keys: set[str] = set()
    u = norm_url(row.get("url", ""))
    if u:
        host = url_host(u)
        if is_platform(host):
            keys.add("url:" + u)
        else:
            keys.add("domain:" + host)  # same business website, any page
    email = row.get("email", "").strip().lower()
    if email:
        keys.add("email:" + email)
    phone = norm_phone(row.get("phone", ""))
    if len(phone) >= 7:
        keys.add("phone:" + phone)
    handle = norm_handle(row.get("handle", ""))
    if handle:
        platform = HANDLE_CHANNELS.get(row.get("channel", "").lower(), row.get("channel", "").lower() or "any")
        keys.add(f"handle:{platform}:{handle}")
    return keys


def probe_keys(value: str) -> set[str]:
    """Keys for a bare value passed to `check` (url, email, phone or @handle)."""
    v = value.strip()
    if "@" in v and not v.startswith("@") and "/" not in v:
        return {"email:" + v.lower()}
    if v.startswith("@") or v.lower().startswith("u/"):
        h = norm_handle(v)
        return {f"handle:{p}:{h}" for p in set(HANDLE_CHANNELS.values()) | {"any"}}
    digits = re.sub(r"\D", "", v)
    if digits and len(digits) >= 7 and re.fullmatch(r"[\d\s+()-]+", v):
        return {"phone:" + norm_phone(v)}
    return keys_for({"url": v})


def index(rows: list[dict]) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for r in rows:
        for k in keys_for(r):
            idx.setdefault(k, r)
    return idx


def find_dupe(row: dict, idx: dict[str, dict]) -> dict | None:
    for k in keys_for(row):
        if k in idx:
            return idx[k]
    return None


def next_id(rows: list[dict]) -> str:
    nums = [int(r["id"][1:]) for r in rows if re.fullmatch(r"L\d+", r.get("id", ""))]
    return f"L{(max(nums) + 1 if nums else 1):04d}"


# ---------- validation ----------

def parse_due(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if re.fullmatch(r"\+\d+", value):
        return (today() + dt.timedelta(days=int(value[1:]))).isoformat()
    return dt.date.fromisoformat(value).isoformat()


def validate(row: dict) -> list[str]:
    errs = []
    if row.get("status") and row["status"] not in STATUSES:
        errs.append(f"status '{row['status']}' not in {STATUSES}")
    if row.get("kind") and row["kind"] not in KINDS:
        errs.append(f"kind '{row['kind']}' not in {KINDS}")
    if row.get("market") and row["market"] not in MARKETS:
        errs.append(f"market '{row['market']}' not in {MARKETS}")
    if row.get("service"):
        bad = [s for s in row["service"].split("|") if s not in SERVICES]
        if bad:
            errs.append(f"service {bad} not in {SERVICES} (join several with |)")
    if row.get("score") and row["score"] not in {"1", "2", "3", "4", "5"}:
        errs.append("score must be 1-5")
    if not (row.get("url") or row.get("email") or row.get("phone") or row.get("handle")):
        errs.append("need at least one of url, email, phone, handle (for dedupe and contact)")
    if not row.get("channel"):
        errs.append("channel is required")
    return errs


def prepare(raw: dict) -> dict:
    row = {k: str(raw.get(k, "") or "").strip() for k in FIELDS}
    row["market"] = row["market"].upper()
    row["status"] = row["status"] or "new"
    row["touches"] = row["touches"] or "0"
    row["channel"] = row["channel"].lower()
    if row["next_due"]:
        row["next_due"] = parse_due(row["next_due"])
    return row


# ---------- commands ----------

def cmd_init(args, ddir: Path) -> int:
    ddir.mkdir(parents=True, exist_ok=True)
    (ddir / "daily").mkdir(exist_ok=True)
    leads = ddir / "leads.csv"
    if not leads.exists():
        write_rows(leads, [])
    print(f"Tracker ready at {ddir}")
    return 0


def add_rows(raws: list[dict], ddir: Path, dry_run: bool) -> int:
    path = ddir / "leads.csv"
    rows = read_rows(path)
    idx = index(rows)
    added, dupes, invalid = [], [], []
    for raw in raws:
        row = prepare(raw)
        errs = validate(row)
        if errs:
            invalid.append((row.get("name") or row.get("url") or "?", errs))
            continue
        dupe = find_dupe(row, idx)
        if dupe:
            dupes.append((row.get("name") or row.get("url"), dupe))
            continue
        row["id"] = next_id(rows)
        row["added"] = today().isoformat()
        rows.append(row)
        for k in keys_for(row):
            idx.setdefault(k, row)
        added.append(row)
    if not dry_run and added:
        write_rows(path, rows)
        for r in added:
            log(ddir, r["id"], "add", f"{r['channel']} {r['service']} {r['name'] or r['url']}")
    verb = "Would add" if dry_run else "Added"
    for r in added:
        print(f"{verb} {r['id']}: {r['name'] or r['company'] or r['url']} [{r['channel']}/{r['service']}]")
    for name, d in dupes:
        flag = "  ** DO NOT CONTACT **" if d["status"] == "do_not_contact" else ""
        print(f"DUPLICATE {name} -> {d['id']} ({d['status']}, added {d['added']}){flag}")
    for name, errs in invalid:
        print(f"INVALID {name}: {'; '.join(errs)}")
    print(f"Summary: {len(added)} {'to add' if dry_run else 'added'}, {len(dupes)} duplicates, {len(invalid)} invalid")
    return 1 if invalid and not added else 0


def cmd_add(args, ddir: Path) -> int:
    raw = {k: getattr(args, k, "") or "" for k in FIELDS if hasattr(args, k)}
    return add_rows([raw], ddir, args.dry_run)


def cmd_import(args, ddir: Path) -> int:
    src = Path(args.file)
    if src.suffix.lower() == ".json":
        data = json.loads(src.read_text(encoding="utf-8"))
        raws = data if isinstance(data, list) else [data]
    else:
        with src.open(newline="", encoding="utf-8-sig") as f:
            raws = list(csv.DictReader(f))
    defaults = {k: v for k, v in {"channel": args.channel, "kind": args.kind, "service": args.service,
                                  "market": args.market, "owner": args.owner}.items() if v}
    raws = [{**defaults, **{k: v for k, v in r.items() if v}} for r in raws]
    return add_rows(raws, ddir, args.dry_run)


def cmd_check(args, ddir: Path) -> int:
    idx = index(read_rows(ddir / "leads.csv"))
    found_any = False
    for value in args.values:
        v = value.strip()
        if v.startswith("@") or v.lower().startswith("u/"):
            h = ":" + norm_handle(v)
            hit = next((r for k, r in idx.items() if k.startswith("handle:") and k.endswith(h)), None)
        else:
            hit = next((idx[k] for k in probe_keys(v) if k in idx), None)
        if hit:
            found_any = True
            flag = "  ** DO NOT CONTACT **" if hit["status"] == "do_not_contact" else ""
            print(f"KNOWN  {value} -> {hit['id']} {hit['status']} (touches {hit['touches']}, "
                  f"next {hit['next_due'] or '-'}){flag}")
        else:
            print(f"NEW    {value}")
    return 0 if not found_any else 3


def get_lead(rows: list[dict], lead_id: str) -> dict:
    lead_id = lead_id.upper()
    for r in rows:
        if r["id"] == lead_id:
            return r
    sys.exit(f"No lead {lead_id}")


def cmd_update(args, ddir: Path) -> int:
    path = ddir / "leads.csv"
    rows = read_rows(path)
    changes = []
    for lead_id in args.ids:
        r = get_lead(rows, lead_id)
        detail = []
        if args.touch:
            n = int(r["touches"] or 0) + 1
            r["touches"] = str(n)
            r["last_touch"] = today().isoformat()
            if r["status"] in PRE_CONTACT:
                r["status"] = "contacted"
            detail.append(f"touch {n}")
            if r["status"] == "contacted":
                if n <= len(CADENCE):
                    r["next_due"] = (today() + dt.timedelta(days=CADENCE[n - 1])).isoformat()
                else:
                    r["next_due"] = ""
                    detail.append("cadence done, mark no_reply if still silent")
        if args.status:
            if args.status not in STATUSES:
                sys.exit(f"status must be one of {STATUSES}")
            r["status"] = args.status
            detail.append(f"status={args.status}")
            if args.status in TERMINAL:
                r["next_due"] = ""
            elif args.status == "replied" and not args.next_due:
                r["next_due"] = today().isoformat()  # answer replies the same day
        if args.next_due is not None:
            r["next_due"] = parse_due(args.next_due)
            detail.append(f"next_due={r['next_due'] or 'cleared'}")
        for kv in args.set or []:
            if "=" not in kv:
                sys.exit(f"--set expects field=value, got {kv}")
            k, v = kv.split("=", 1)
            if k not in FIELDS or k in {"id", "added"}:
                sys.exit(f"cannot set field {k}")
            r[k] = v
            detail.append(f"{k}={v}")
        if args.note:
            stamp = today().isoformat()
            r["notes"] = (r["notes"] + " | " if r["notes"] else "") + f"{stamp}: {args.note}"
            detail.append(f"note: {args.note}")
        errs = validate(r)
        if errs:
            sys.exit(f"{r['id']}: {'; '.join(errs)}")
        changes.append((r, "; ".join(detail)))
    write_rows(path, rows)
    for r, d in changes:
        log(ddir, r["id"], "update", d)
        print(f"{r['id']} -> {r['status']}, touches {r['touches']}, next {r['next_due'] or '-'}"
              + (f"  ({d})" if d else ""))
    return 0


def fmt_table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "(none)"
    def cell(r, c):
        v = r.get(c, "") or ""
        if c == "who":
            v = r.get("name") or r.get("company") or r.get("handle") or r.get("email") or ""
        limit = 60 if c in {"url", "signal"} else 28
        return v if len(v) <= limit else v[: limit - 1] + "…"
    widths = {c: max(len(c), *(len(cell(r, c)) for r in rows)) for c in cols}
    lines = ["  ".join(c.ljust(widths[c]) for c in cols)]
    lines.append("  ".join("-" * widths[c] for c in cols))
    for r in rows:
        lines.append("  ".join(cell(r, c).ljust(widths[c]) for c in cols))
    return "\n".join(lines)


def emit(rows: list[dict], fmt: str, cols: list[str]) -> None:
    if fmt == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif fmt == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    else:
        print(fmt_table(rows, cols))


def cmd_due(args, ddir: Path) -> int:
    limit = parse_due(args.date) if args.date else today().isoformat()
    rows = [r for r in read_rows(ddir / "leads.csv")
            if r["next_due"] and r["next_due"] <= limit and r["status"] not in TERMINAL
            and (not args.channel or r["channel"] == args.channel.lower())]
    rows.sort(key=lambda r: (r["status"] != "replied", r["next_due"], r["id"]))
    print(f"Due on or before {limit}: {len(rows)}")
    emit(rows, args.format, ["id", "status", "next_due", "touches", "channel", "service", "who", "url"])
    stale = [r for r in read_rows(ddir / "leads.csv")
             if r["status"] == "contacted" and int(r["touches"] or 0) >= MAX_TOUCHES and not r["next_due"]]
    if stale:
        print(f"\n{len(stale)} lead(s) finished the cadence with no reply; consider --status no_reply: "
              + ", ".join(r["id"] for r in stale))
    return 0


def cmd_list(args, ddir: Path) -> int:
    rows = read_rows(ddir / "leads.csv")
    for field in ("status", "channel", "kind", "market", "owner"):
        want = getattr(args, field)
        if want:
            rows = [r for r in rows if r[field] == want]
    if args.service:
        rows = [r for r in rows if args.service in r["service"].split("|")]
    if args.min_score:
        rows = [r for r in rows if r["score"] and int(r["score"]) >= args.min_score]
    if args.search:
        q = args.search.lower()
        rows = [r for r in rows if q in " ".join(r.values()).lower()]
    rows.sort(key=lambda r: (-(int(r["score"]) if r["score"] else 0), r["id"]))
    if args.limit:
        rows = rows[: args.limit]
    emit(rows, args.format, ["id", "score", "status", "channel", "service", "market", "who", "signal"])
    return 0


def cmd_show(args, ddir: Path) -> int:
    r = get_lead(read_rows(ddir / "leads.csv"), args.id)
    width = max(len(k) for k in FIELDS)
    for k in FIELDS:
        if r[k]:
            print(f"{k.ljust(width)}  {r[k]}")
    return 0


def cmd_stats(args, ddir: Path) -> int:
    rows = read_rows(ddir / "leads.csv")
    if not rows:
        print("No leads yet.")
        return 0
    status = Counter(r["status"] for r in rows)
    print(f"Total leads: {len(rows)}")
    print("By status: " + ", ".join(f"{s} {status[s]}" for s in STATUSES if status[s]))
    reached = {"contacted", "replied", "call_booked", "proposal", "won", "lost", "no_reply", "do_not_contact"}
    responded = {"replied", "call_booked", "proposal", "won", "lost", "do_not_contact"}
    calls = {"call_booked", "proposal", "won", "lost"}

    def funnel(group_key):
        g = defaultdict(list)
        for r in rows:
            for key in (r[group_key].split("|") if group_key == "service" else [r[group_key]]):
                g[key or "-"].append(r)
        out = []
        for key, items in sorted(g.items(), key=lambda kv: -len(kv[1])):
            sent = sum(r["status"] in reached for r in items)
            rep = sum(r["status"] in responded for r in items)
            cal = sum(r["status"] in calls for r in items)
            won = sum(r["status"] == "won" for r in items)
            rate = f"{rep / sent:.0%}" if sent else "-"
            out.append({"group": key, "leads": str(len(items)), "contacted": str(sent),
                        "replied": str(rep), "reply_rate": rate, "calls": str(cal), "won": str(won)})
        return out

    for key in ("channel", "service", "kind"):
        print(f"\nBy {key}:")
        print(fmt_table(funnel(key), ["group", "leads", "contacted", "replied", "reply_rate", "calls", "won"]))
    due = sum(1 for r in rows if r["next_due"] and r["next_due"] <= today().isoformat()
              and r["status"] not in TERMINAL)
    print(f"\nFollow-ups due now: {due}")
    return 0


# ---------- cli ----------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Eravue outreach lead tracker")
    p.add_argument("--data-dir", help="defaults to <repo>/.outreach")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create the .outreach folder and empty ledger")

    a = sub.add_parser("add", help="add one lead (skips duplicates)")
    a.add_argument("--channel", required=True, help="reddit, x, linkedin, upwork, instagram, google-maps, email, whatsapp, ...")
    a.add_argument("--kind", choices=KINDS, default="inbound")
    a.add_argument("--service", default="", help="|-separated: " + ", ".join(SERVICES))
    a.add_argument("--market", default="", help="IN or INTL")
    for f in ("name", "company", "handle", "url", "email", "phone", "location", "signal", "angle", "notes"):
        a.add_argument(f"--{f}", default="")
    a.add_argument("--score", default="", help="1-5")
    a.add_argument("--status", default="new", choices=STATUSES)
    a.add_argument("--owner", default="", help="sanchit or sanchita")
    a.add_argument("--next-due", dest="next_due", default="", help="YYYY-MM-DD or +N days")
    a.add_argument("--dry-run", action="store_true")

    i = sub.add_parser("import", help="bulk add from .csv or .json using the same field names")
    i.add_argument("file")
    for f in ("channel", "kind", "service", "market", "owner"):
        i.add_argument(f"--{f}", default="", help=f"default {f} for rows that lack one")
    i.add_argument("--dry-run", action="store_true")

    c = sub.add_parser("check", help="is a url / email / phone / @handle already tracked? (exit 3 if any known)")
    c.add_argument("values", nargs="+")

    u = sub.add_parser("update", help="record a touch, status change, note or follow-up date")
    u.add_argument("ids", nargs="+", help="one or more lead ids, e.g. L0004 L0007")
    u.add_argument("--touch", action="store_true", help="a message was sent: count it and schedule the next follow-up")
    u.add_argument("--status", choices=STATUSES)
    u.add_argument("--note")
    u.add_argument("--next-due", dest="next_due", help="YYYY-MM-DD, +N days, or '' to clear")
    u.add_argument("--set", action="append", metavar="FIELD=VALUE", help="set any other field")

    d = sub.add_parser("due", help="follow-ups due (replies first)")
    d.add_argument("--date", help="YYYY-MM-DD or +N (default today)")
    d.add_argument("--channel", help="only this channel, e.g. instagram")
    d.add_argument("--format", choices=["table", "csv", "json"], default="table")

    li = sub.add_parser("list", help="filter and list leads")
    for f in ("status", "channel", "kind", "market", "owner", "service", "search"):
        li.add_argument(f"--{f}")
    li.add_argument("--min-score", dest="min_score", type=int)
    li.add_argument("--limit", type=int)
    li.add_argument("--format", choices=["table", "csv", "json"], default="table")

    s = sub.add_parser("show", help="all fields for one lead")
    s.add_argument("id")

    sub.add_parser("stats", help="funnel by channel, service and kind")
    return p


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    args = build_parser().parse_args(argv)
    ddir = data_dir(args.data_dir)
    if args.cmd != "init" and not (ddir / "leads.csv").exists():
        cmd_init(args, ddir)
    handler = {"init": cmd_init, "add": cmd_add, "import": cmd_import, "check": cmd_check,
               "update": cmd_update, "due": cmd_due, "list": cmd_list, "show": cmd_show,
               "stats": cmd_stats}[args.cmd]
    return handler(args, ddir)


if __name__ == "__main__":
    sys.exit(main())
