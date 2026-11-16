#!/usr/bin/env python3
"""Eravue growth ledger: one place for every number that matters.

Files (all CSV/JSON, diff-friendly, committed to the private repo):
  .growth/metrics.csv   date,metric,value,source,note      time series of any metric
  .growth/deals.csv     won clients and what they pay
  .growth/payments.csv  cash actually received
  .growth/content.csv   every post/reel/article and its performance
  .growth/targets.json  {"metric": {"target": n, "by": "YYYY-MM-DD", "label": "..."}}
  .growth/config.json   umami/ssh settings

Pulls:
  pull umami   site traffic + conversion events from the self-hosted Umami DB over SSH (read-only)
  pull leads   outreach funnel from .outreach/leads.csv + log.csv (eravue-outreach tracker)
  pull money   MRR, cash, active clients from deals/payments
  pull all     all of the above

Standard library only. Run from anywhere.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
GROWTH = Path(os.environ.get("ERAVUE_GROWTH_DIR", REPO / ".growth"))
OUTREACH = Path(os.environ.get("ERAVUE_OUTREACH_DIR", REPO / ".outreach"))

METRIC_FIELDS = ["date", "metric", "value", "source", "note"]
DEAL_FIELDS = ["id", "date", "client", "lead_id", "service", "market", "source_channel",
               "currency", "setup", "monthly", "status", "ended", "notes"]
PAY_FIELDS = ["date", "deal_id", "amount", "currency", "note"]
CONTENT_FIELDS = ["id", "date", "platform", "account", "format", "pillar", "title", "url",
                  "status", "views", "likes", "comments", "shares", "saves", "follows",
                  "profile_visits", "leads", "updated", "notes"]
CONTENT_NUMS = ["views", "likes", "comments", "shares", "saves", "follows", "profile_visits", "leads"]
DEAL_STATUSES = ["active", "paused", "ended", "one_off"]

DEFAULT_CONFIG = {
    "ssh_host": "sanchxt@46.62.153.22",
    "umami_container": "umami-db",
    "umami_website_id": "095f079d-cbe5-4c84-b4d8-aa5e5e067ed7",
    # Most "visitors" from these countries are crawlers/bots (checked 2026-11-11: SG+CN were ~80% of sessions).
    "bot_countries": ["SG", "CN"],
    "ignore_events": ["scroll-depth", "web-vital"],
}

# Lead stages in order; a lead counts for every stage up to the furthest it has reached.
STAGES = ["contacted", "replied", "call_booked", "proposal", "won"]
# Headline metrics for `report --brief` (daily runs).
BRIEF = re.compile(r"^(money\.(mrr|cash_30d|clients_active)|pipeline\.(touches_7d|replies_7d|calls_7d|proposal_total|won_total|"
                   r"open_followups)|site\.(visitors_human_7d|conversions_7d|search_visits_28d|ai_visits_28d)|"
                   r"search\.gsc_(clicks|impressions)_28d|social\..*\.followers)")
STAGE_OF = {"contacted": 0, "no_reply": 0, "replied": 1, "call_booked": 2, "proposal": 3, "won": 4}


# ---------- io ----------

def today() -> dt.date:
    o = os.environ.get("ERAVUE_TODAY")
    return dt.date.fromisoformat(o) if o else dt.date.today()


def read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)


def config() -> dict:
    p = GROWTH / "config.json"
    cfg = dict(DEFAULT_CONFIG)
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8")))
    return cfg


def num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def fmt(v: float) -> str:
    return f"{int(v):,}" if float(v).is_integer() else f"{v:,.2f}"


def record_many(items: list[tuple[str, float, str, str]], date: str | None = None) -> None:
    """Upsert (metric, value, source, note) for one date: re-running a pull replaces that day's value."""
    path = GROWTH / "metrics.csv"
    rows = read(path)
    d = date or today().isoformat()
    index = {(r["date"], r["metric"]): r for r in rows}
    for metric, value, source, note in items:
        key = (d, metric)
        if key in index:
            index[key].update(value=fmt(value).replace(",", ""), source=source, note=note)
        else:
            r = {"date": d, "metric": metric, "value": fmt(value).replace(",", ""), "source": source, "note": note}
            rows.append(r)
            index[key] = r
    rows.sort(key=lambda r: (r["date"], r["metric"]))
    write(path, METRIC_FIELDS, rows)


def series(metric: str) -> list[tuple[str, float]]:
    return sorted((r["date"], num(r["value"])) for r in read(GROWTH / "metrics.csv") if r["metric"] == metric)


def latest(metric: str, on_or_before: str | None = None) -> tuple[str, float] | None:
    s = [x for x in series(metric) if not on_or_before or x[0] <= on_or_before]
    return s[-1] if s else None


# ---------- pulls ----------

def umami_query(sql: str, cfg: dict) -> list[list[str]]:
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", cfg["ssh_host"],
           f"docker exec -i {cfg['umami_container']} psql -U umami -d umami -At -F '|' -v ON_ERROR_STOP=1"]
    res = subprocess.run(cmd, input=sql, capture_output=True, text=True, timeout=90)
    if res.returncode != 0:
        sys.exit(f"Umami query failed (ssh {cfg['ssh_host']}): {res.stderr.strip()[:400]}")
    return [line.split("|") for line in res.stdout.strip().splitlines() if line]


def pull_umami(days: int) -> list[tuple[str, float, str, str]]:
    cfg = config()
    wid = cfg["umami_website_id"]
    if not re.fullmatch(r"[0-9a-f-]{36}", wid):
        sys.exit("umami_website_id in .growth/config.json looks wrong")
    bots = ",".join("'" + c.replace("'", "") + "'" for c in cfg["bot_countries"]) or "''"
    ignore = ",".join("'" + e.replace("'", "") + "'" for e in cfg["ignore_events"]) or "''"
    since = f"now() - interval '{int(days)} days'"
    sql = f"""
select 'pageviews', count(*) from website_event where website_id='{wid}' and event_type=1 and created_at > {since};
select 'visitors', count(distinct session_id) from website_event where website_id='{wid}' and created_at > {since};
select 'visitors_human', count(distinct e.session_id) from website_event e join session s using(session_id)
  where e.website_id='{wid}' and e.created_at > {since} and coalesce(s.country,'') not in ({bots});
select 'india_visitors', count(distinct e.session_id) from website_event e join session s using(session_id)
  where e.website_id='{wid}' and e.created_at > {since} and s.country='IN';
select 'search_visits', count(*) from website_event where website_id='{wid}' and event_type=1 and created_at > {since}
  and (referrer_domain ilike '%google.%' or referrer_domain ilike '%bing.%' or referrer_domain ilike '%duckduckgo%'
       or referrer_domain ilike '%googlequicksearchbox%' or referrer_domain ilike '%yahoo.%');
select 'ai_visits', count(*) from website_event where website_id='{wid}' and event_type=1 and created_at > {since}
  and (referrer_domain ilike '%chatgpt%' or referrer_domain ilike '%openai%' or referrer_domain ilike '%perplexity%'
       or referrer_domain ilike '%gemini%' or referrer_domain ilike '%copilot%' or referrer_domain ilike '%claude.ai%');
select 'social_visits', count(*) from website_event where website_id='{wid}' and event_type=1 and created_at > {since}
  and (referrer_domain ilike '%instagram%' or referrer_domain ilike '%linkedin%' or referrer_domain ilike '%facebook%'
       or referrer_domain ilike '%t.co' or referrer_domain ilike '%x.com' or referrer_domain ilike '%reddit%'
       or referrer_domain ilike '%youtube%' or referrer_domain ilike '%lnkd.in%');
select 'event.' || event_name, count(*) from website_event where website_id='{wid}' and event_type=2
  and created_at > {since} and event_name not in ({ignore}) group by event_name;
"""
    out = []
    note = f"last {days}d"
    for name, value in umami_query(sql, cfg):
        out.append((f"site.{name}_{days}d", num(value), "umami", note))
    # Conversions: anything that is a real enquiry action (see eravue-conversion tracking taxonomy).
    conv = sum(v for m, v, _, _ in out if re.search(r"event\.(lead-form-submit|contact-form-submit|whatsapp-click|"
                                                       r"whatsapp-chat-click|phone-click|email-click|book-call-click)", m))
    out.append((f"site.conversions_{days}d", conv, "umami", note + "; form+whatsapp+phone+email+book-call"))
    return out


def pull_leads() -> list[tuple[str, float, str, str]]:
    rows = read(OUTREACH / "leads.csv")
    log = read(OUTREACH / "log.csv")
    furthest: dict[str, int] = {}
    for r in rows:
        if r["status"] in STAGE_OF:
            furthest[r["id"]] = max(furthest.get(r["id"], -1), STAGE_OF[r["status"]])
    week_ago = (today() - dt.timedelta(days=7)).isoformat()
    week = Counter()
    for e in log:
        detail = e.get("detail", "")
        for st in re.findall(r"status=(\w+)", detail):
            if st in STAGE_OF:
                furthest[e["id"]] = max(furthest.get(e["id"], -1), STAGE_OF[st])
                if e["timestamp"][:10] > week_ago:
                    week[st] += 1
        if e["timestamp"][:10] > week_ago:
            if re.search(r"\btouch \d+", detail):
                week["touches"] += 1
            if e.get("action") == "add":
                week["new"] += 1
    out = [("pipeline.leads_total", len(rows), "outreach", "all tracked leads")]
    for i, st in enumerate(STAGES):
        out.append((f"pipeline.{st}_total", sum(1 for v in furthest.values() if v >= i), "outreach", "reached stage, ever"))
    out += [
        ("pipeline.new_leads_7d", week["new"], "outreach", "added in last 7d"),
        ("pipeline.touches_7d", week["touches"], "outreach", "messages sent in last 7d"),
        ("pipeline.replies_7d", week["replied"], "outreach", ""),
        ("pipeline.calls_7d", week["call_booked"], "outreach", ""),
        ("pipeline.proposals_7d", week["proposal"], "outreach", ""),
        ("pipeline.won_7d", week["won"], "outreach", ""),
        ("pipeline.open_followups", sum(1 for r in rows if r.get("next_due") and r["next_due"] <= today().isoformat()
                                       and r["status"] not in {"won", "lost", "no_reply", "skipped", "avoid", "do_not_contact"}),
         "outreach", "due today or overdue"),
    ]
    return out


def pull_money() -> list[tuple[str, float, str, str]]:
    deals = read(GROWTH / "deals.csv")
    pays = read(GROWTH / "payments.csv")
    mrr = defaultdict(float)
    for d in deals:
        if d["status"] == "active":
            mrr[d["currency"]] += num(d["monthly"])
    cash30 = defaultdict(float)
    cash_all = defaultdict(float)
    cutoff = (today() - dt.timedelta(days=30)).isoformat()
    for p in pays:
        cash_all[p["currency"]] += num(p["amount"])
        if p["date"] > cutoff:
            cash30[p["currency"]] += num(p["amount"])
    out = [("money.clients_active", sum(1 for d in deals if d["status"] == "active"), "deals", "recurring clients"),
           ("money.deals_won_total", len(deals), "deals", "")]
    for cur in sorted(set(mrr) | set(cash30) | set(cash_all) | {"INR"}):
        c = cur.lower()
        out += [(f"money.mrr_{c}", mrr[cur], "deals", "active monthly retainers"),
                (f"money.cash_30d_{c}", cash30[cur], "payments", ""),
                (f"money.cash_total_{c}", cash_all[cur], "payments", "")]
    return out


# ---------- commands ----------

def cmd_init(a) -> int:
    GROWTH.mkdir(parents=True, exist_ok=True)
    for name, fields in (("metrics.csv", METRIC_FIELDS), ("deals.csv", DEAL_FIELDS),
                         ("payments.csv", PAY_FIELDS), ("content.csv", CONTENT_FIELDS)):
        p = GROWTH / name
        if not p.exists():
            write(p, fields, [])
    for name, data in (("config.json", DEFAULT_CONFIG), ("targets.json", {})):
        p = GROWTH / name
        if not p.exists():
            p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"ready: {GROWTH}")
    return 0


def cmd_pull(a) -> int:
    items = []
    if a.source in ("umami", "all"):
        for d in a.days:
            items += pull_umami(d)
    if a.source in ("leads", "all"):
        items += pull_leads()
    if a.source in ("money", "all"):
        items += pull_money()
    if not a.dry_run:
        record_many(items)
    for m, v, s, n in items:
        print(f"{m:40} {fmt(v):>10}  {s}")
    return 0


def cmd_record(a) -> int:
    items = []
    for kv in a.pairs:
        if "=" not in kv:
            sys.exit(f"expected metric=value, got {kv}")
        k, v = kv.split("=", 1)
        if not re.fullmatch(r"[a-z0-9_.\-]+", k):
            sys.exit(f"metric names are lowercase dotted, e.g. social.ig_eravuedotcom.followers (got {k})")
        items.append((k, num(v.replace(",", "")), a.source, a.note or ""))
    record_many(items, a.date)
    print(f"recorded {len(items)} value(s) for {a.date or today().isoformat()}")
    return 0


def cmd_history(a) -> int:
    for d, v in series(a.metric)[-a.limit:]:
        print(f"{d}  {fmt(v)}")
    return 0


def next_id(rows: list[dict], prefix: str) -> str:
    n = max((int(r["id"][len(prefix):]) for r in rows if r.get("id", "").startswith(prefix)), default=0)
    return f"{prefix}{n + 1:04d}"


def cmd_deal(a) -> int:
    path = GROWTH / "deals.csv"
    rows = read(path)
    if a.action == "add":
        if not a.client:
            sys.exit("--client is required")
        r = {f: "" for f in DEAL_FIELDS}
        r.update(id=next_id(rows, "D"), date=a.date or today().isoformat(), client=a.client, lead_id=a.lead or "",
                 service=a.service or "", market=a.market or "", source_channel=a.channel or "",
                 currency=(a.currency or "INR").upper(), setup=str(a.setup or 0), monthly=str(a.monthly or 0),
                 status=a.status or ("active" if a.monthly else "one_off"), notes=a.note or "")
        rows.append(r)
        write(path, DEAL_FIELDS, rows)
        print(f"added {r['id']}: {r['client']} {r['currency']} setup {r['setup']} + {r['monthly']}/mo [{r['status']}]")
        print("Record cash when it lands: growth.py pay <deal> <amount>")
    elif a.action == "update":
        r = next((x for x in rows if x["id"] == a.id), None) or sys.exit(f"no deal {a.id}")
        if a.status:
            if a.status not in DEAL_STATUSES:
                sys.exit(f"status must be one of {DEAL_STATUSES}")
            r["status"] = a.status
            if a.status == "ended":
                r["ended"] = today().isoformat()
        if a.monthly is not None:
            r["monthly"] = str(a.monthly)
        if a.note:
            r["notes"] = (r["notes"] + " | " if r["notes"] else "") + f"{today()}: {a.note}"
        write(path, DEAL_FIELDS, rows)
        print(f"updated {r['id']}")
    else:
        for r in rows:
            print(f"{r['id']} {r['date']} {r['client']:<28} {r['service']:<14} {r['currency']} "
                  f"setup {r['setup']:>8} monthly {r['monthly']:>7} {r['status']}")
        if not rows:
            print("No deals yet.")
    return 0


def cmd_pay(a) -> int:
    deals = {d["id"]: d for d in read(GROWTH / "deals.csv")}
    if a.deal not in deals:
        sys.exit(f"no deal {a.deal}; add it first with: growth.py deal add --client ...")
    rows = read(GROWTH / "payments.csv")
    rows.append({"date": a.date or today().isoformat(), "deal_id": a.deal, "amount": str(a.amount),
                 "currency": (a.currency or deals[a.deal]["currency"]).upper(), "note": a.note or ""})
    write(GROWTH / "payments.csv", PAY_FIELDS, rows)
    print(f"payment recorded for {a.deal}: {a.amount}")
    return 0


def cmd_content(a) -> int:
    path = GROWTH / "content.csv"
    rows = read(path)
    if a.action == "add":
        r = {f: "" for f in CONTENT_FIELDS}
        r.update(id=next_id(rows, "C"), date=a.date or today().isoformat(), platform=a.platform or "",
                 account=a.account or "", format=a.format or "", pillar=a.pillar or "", title=a.title or "",
                 url=a.url or "", status=a.status or "posted", notes=a.note or "")
        rows.append(r)
        print(f"added {r['id']}")
    elif a.action == "update":
        r = next((x for x in rows if x["id"] == a.id), None) or sys.exit(f"no content {a.id}")
        for k in CONTENT_NUMS:
            v = getattr(a, k)
            if v is not None:
                r[k] = str(v)
        for k in ("url", "status", "title"):
            v = getattr(a, k)
            if v:
                r[k] = v
        if a.note:
            r["notes"] = (r["notes"] + " | " if r["notes"] else "") + f"{today()}: {a.note}"
        r["updated"] = today().isoformat()
        print(f"updated {r['id']}")
    else:
        since = (today() - dt.timedelta(days=a.days)).isoformat()
        for r in rows:
            if r["date"] >= since and (not a.platform or r["platform"] == a.platform):
                print(f"{r['id']} {r['date']} {r['platform']:<9} {r['account']:<20} {r['format']:<8} "
                      f"views {r['views'] or '-':>6} saves {r['saves'] or '-':>4} follows {r['follows'] or '-':>4} "
                      f"leads {r['leads'] or '-':>3}  {r['title'][:50]}")
        return 0
    write(path, CONTENT_FIELDS, rows)
    return 0


def cmd_target(a) -> int:
    p = GROWTH / "targets.json"
    t = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    if a.metric:
        t[a.metric] = {"target": a.value, "by": a.by, "label": a.label or a.metric}
        p.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for m, spec in load_targets().items():
        cur = latest(m)
        print(f"{spec['label']:<40} {fmt(cur[1]) if cur else '-':>8} / {fmt(spec['target'])}  by {spec['by']}")
    return 0


def delta(metric: str, days: int) -> str:
    cur = latest(metric)
    if not cur:
        return "-"
    prev = latest(metric, (dt.date.fromisoformat(cur[0]) - dt.timedelta(days=days)).isoformat())
    if not prev:
        return fmt(cur[1])
    d = cur[1] - prev[1]
    return f"{fmt(cur[1])} ({'+' if d >= 0 else ''}{fmt(d)})"


def cmd_report(a) -> int:
    metrics = sorted({r["metric"] for r in read(GROWTH / "metrics.csv")})
    lines = [f"# Eravue growth scoreboard, {today().isoformat()}", ""]
    targets = load_targets()
    if targets:
        lines += ["## Targets", "", "| Target | Now | Goal | By | Progress |", "|---|---|---|---|---|"]
        for m, spec in targets.items():
            cur = latest(m)
            v = cur[1] if cur else 0
            pct = f"{min(100, round(100 * v / spec['target']))}%" if spec["target"] else "-"
            lines.append(f"| {spec['label']} | {fmt(v)} | {fmt(spec['target'])} | {spec['by']} | {pct} |")
        lines.append("")
    groups = [("Money", "money."), ("Pipeline", "pipeline."), ("Website", "site."),
              ("Search", "search."), ("Social", "social."), ("Other", "")]
    if a.brief:
        metrics = [m for m in metrics if BRIEF.search(m)]
    shown = set()
    for title, prefix in groups:
        ms = [m for m in metrics if m.startswith(prefix) and m not in shown]
        if not ms:
            continue
        lines += [f"## {title}", "", f"| Metric | Latest (change vs {a.compare}d ago) | As of |", "|---|---|---|"]
        for m in ms:
            shown.add(m)
            cur = latest(m)
            lines.append(f"| {m} | {delta(m, a.compare)} | {cur[0]} |")
        lines.append("")
    content = [r for r in read(GROWTH / "content.csv") if r["date"] >= (today() - dt.timedelta(days=7)).isoformat()]
    if content:
        by = Counter(r["platform"] for r in content)
        lines += ["## Content, last 7 days", "", ", ".join(f"{k}: {v}" for k, v in by.items()),
                  f"Views {fmt(sum(num(r['views']) for r in content))}, follows {fmt(sum(num(r['follows']) for r in content))}, "
                  f"leads {fmt(sum(num(r['leads']) for r in content))}", ""]
    text = "\n".join(lines)
    print(text)
    if a.save:
        out = GROWTH / "reports" / f"{today().isoformat()}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
        print(f"\nsaved {out}")
    return 0


def load_targets() -> dict:
    """Targets keyed by metric; keys starting with '_' are notes, not targets."""
    p = GROWTH / "targets.json"
    t = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return {k: v for k, v in t.items() if not k.startswith("_")}


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252, which can't print ₹
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="create .growth/ files")

    pl = sub.add_parser("pull", help="pull metrics from Umami / outreach tracker / deals")
    pl.add_argument("source", choices=["umami", "leads", "money", "all"])
    pl.add_argument("--days", type=int, nargs="+", default=[7, 28], help="Umami windows (default 7 28)")
    pl.add_argument("--dry-run", action="store_true")

    r = sub.add_parser("record", help="record manual metrics: social.ig_eravuedotcom.followers=373 ...")
    r.add_argument("pairs", nargs="+")
    r.add_argument("--source", default="manual")
    r.add_argument("--note")
    r.add_argument("--date")

    h = sub.add_parser("history", help="time series of one metric")
    h.add_argument("metric")
    h.add_argument("--limit", type=int, default=30)

    d = sub.add_parser("deal", help="won clients: add | update | list")
    d.add_argument("action", choices=["add", "update", "list"])
    d.add_argument("id", nargs="?")
    for f in ("client", "lead", "service", "market", "channel", "currency", "status", "note", "date"):
        d.add_argument(f"--{f}")
    d.add_argument("--setup", type=float)
    d.add_argument("--monthly", type=float)

    pay = sub.add_parser("pay", help="record cash received for a deal")
    pay.add_argument("deal")
    pay.add_argument("amount", type=float)
    pay.add_argument("--currency")
    pay.add_argument("--date")
    pay.add_argument("--note")

    c = sub.add_parser("content", help="content log: add | update | list")
    c.add_argument("action", choices=["add", "update", "list"])
    c.add_argument("id", nargs="?")
    for f in ("platform", "account", "format", "pillar", "title", "url", "status", "note", "date"):
        c.add_argument(f"--{f}")
    for f in CONTENT_NUMS:
        c.add_argument(f"--{f.replace('_', '-')}", dest=f, type=int)
    c.add_argument("--days", type=int, default=30)

    t = sub.add_parser("target", help="set or show targets")
    t.add_argument("metric", nargs="?")
    t.add_argument("value", nargs="?", type=float)
    t.add_argument("--by", default="")
    t.add_argument("--label")

    rp = sub.add_parser("report", help="markdown scoreboard")
    rp.add_argument("--compare", type=int, default=7)
    rp.add_argument("--brief", action="store_true", help="headline metrics only")
    rp.add_argument("--save", action="store_true", help="also write .growth/reports/YYYY-MM-DD.md")

    a = p.parse_args()
    if a.cmd == "target" and a.metric and a.value is None:
        sys.exit("usage: growth.py target <metric> <value> --by YYYY-MM-DD --label '...'")
    if a.cmd in ("deal", "content") and a.action == "update" and not a.id:
        sys.exit("update needs an id")
    return {"init": cmd_init, "pull": cmd_pull, "record": cmd_record, "history": cmd_history, "deal": cmd_deal,
            "pay": cmd_pay, "content": cmd_content, "target": cmd_target, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
