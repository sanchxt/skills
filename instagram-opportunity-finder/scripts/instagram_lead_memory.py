#!/usr/bin/env python3
"""Persistent SQLite memory for Instagram outreach leads."""

from __future__ import annotations

import argparse
import csv
import os
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DB = Path(os.environ.get("INSTAGRAM_LEAD_MEMORY_DB", Path.home() / ".codex" / "instagram_lead_memory" / "instagram_leads.sqlite3"))

FIELDNAMES = [
    "username",
    "profile_url",
    "display_name",
    "account_type",
    "niche",
    "location",
    "website_url",
    "followers",
    "activity_recency",
    "discovered_from",
    "evidence_summary",
    "content_gap_summary",
    "website_gap_summary",
    "service_fit_summary",
    "icp_fit_score",
    "urgency_score",
    "business_value_score",
    "outreach_fit",
    "sensitivity_risk",
    "suggested_dm",
    "suggested_comment",
    "suggested_email",
    "notes",
]

STATUSES = {"found", "shortlisted", "contacted", "replied", "ignored", "avoided", "not-fit"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_username(username: str) -> str:
    username = (username or "").strip().lower().lstrip("@").strip("/")
    if username.startswith("https://"):
        username = username.replace("https://www.instagram.com/", "").replace("https://instagram.com/", "")
    if username.startswith("http://"):
        username = username.replace("http://www.instagram.com/", "").replace("http://instagram.com/", "")
    return username.split("/", 1)[0]


def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS instagram_leads (
            id INTEGER PRIMARY KEY,
            campaign TEXT NOT NULL,
            username TEXT NOT NULL,
            profile_url TEXT,
            display_name TEXT,
            account_type TEXT,
            niche TEXT,
            location TEXT,
            website_url TEXT,
            followers TEXT,
            activity_recency TEXT,
            discovered_from TEXT,
            evidence_summary TEXT,
            content_gap_summary TEXT,
            website_gap_summary TEXT,
            service_fit_summary TEXT,
            icp_fit_score INTEGER,
            urgency_score INTEGER,
            business_value_score INTEGER,
            outreach_fit TEXT,
            sensitivity_risk TEXT,
            suggested_dm TEXT,
            suggested_comment TEXT,
            suggested_email TEXT,
            status TEXT NOT NULL DEFAULT 'found',
            notes TEXT,
            first_found_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL,
            last_status_at TEXT NOT NULL,
            UNIQUE(campaign, username)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS status_events (
            id INTEGER PRIMARY KEY,
            lead_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(lead_id) REFERENCES instagram_leads(id)
        )
        """
    )
    conn.commit()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = FIELDNAMES + ["existing_status", "first_found_at", "last_seen_at"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def get_existing(conn: sqlite3.Connection, campaign: str, username: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM instagram_leads WHERE campaign = ? AND username = ?",
        (campaign, username),
    ).fetchone()


def as_int(value: str) -> int | None:
    try:
        return int(value) if str(value).strip() else None
    except ValueError:
        return None


def record_found(conn: sqlite3.Connection, campaign: str, row: dict[str, str]) -> None:
    now = utc_now()
    username = normalize_username(row.get("username", ""))
    conn.execute(
        """
        INSERT INTO instagram_leads (
            campaign, username, profile_url, display_name, account_type, niche, location,
            website_url, followers, activity_recency, discovered_from, evidence_summary,
            content_gap_summary, website_gap_summary, service_fit_summary, icp_fit_score,
            urgency_score, business_value_score, outreach_fit, sensitivity_risk,
            suggested_dm, suggested_comment, suggested_email, status, notes,
            first_found_at, last_seen_at, last_status_at
        ) VALUES (
            :campaign, :username, :profile_url, :display_name, :account_type, :niche, :location,
            :website_url, :followers, :activity_recency, :discovered_from, :evidence_summary,
            :content_gap_summary, :website_gap_summary, :service_fit_summary, :icp_fit_score,
            :urgency_score, :business_value_score, :outreach_fit, :sensitivity_risk,
            :suggested_dm, :suggested_comment, :suggested_email, 'found', :notes,
            :now, :now, :now
        )
        ON CONFLICT(campaign, username) DO UPDATE SET
            profile_url = COALESCE(NULLIF(excluded.profile_url, ''), instagram_leads.profile_url),
            display_name = COALESCE(NULLIF(excluded.display_name, ''), instagram_leads.display_name),
            account_type = COALESCE(NULLIF(excluded.account_type, ''), instagram_leads.account_type),
            niche = COALESCE(NULLIF(excluded.niche, ''), instagram_leads.niche),
            location = COALESCE(NULLIF(excluded.location, ''), instagram_leads.location),
            website_url = COALESCE(NULLIF(excluded.website_url, ''), instagram_leads.website_url),
            followers = COALESCE(NULLIF(excluded.followers, ''), instagram_leads.followers),
            activity_recency = COALESCE(NULLIF(excluded.activity_recency, ''), instagram_leads.activity_recency),
            discovered_from = COALESCE(NULLIF(excluded.discovered_from, ''), instagram_leads.discovered_from),
            evidence_summary = COALESCE(NULLIF(excluded.evidence_summary, ''), instagram_leads.evidence_summary),
            content_gap_summary = COALESCE(NULLIF(excluded.content_gap_summary, ''), instagram_leads.content_gap_summary),
            website_gap_summary = COALESCE(NULLIF(excluded.website_gap_summary, ''), instagram_leads.website_gap_summary),
            service_fit_summary = COALESCE(NULLIF(excluded.service_fit_summary, ''), instagram_leads.service_fit_summary),
            icp_fit_score = COALESCE(excluded.icp_fit_score, instagram_leads.icp_fit_score),
            urgency_score = COALESCE(excluded.urgency_score, instagram_leads.urgency_score),
            business_value_score = COALESCE(excluded.business_value_score, instagram_leads.business_value_score),
            outreach_fit = COALESCE(NULLIF(excluded.outreach_fit, ''), instagram_leads.outreach_fit),
            sensitivity_risk = COALESCE(NULLIF(excluded.sensitivity_risk, ''), instagram_leads.sensitivity_risk),
            suggested_dm = COALESCE(NULLIF(excluded.suggested_dm, ''), instagram_leads.suggested_dm),
            suggested_comment = COALESCE(NULLIF(excluded.suggested_comment, ''), instagram_leads.suggested_comment),
            suggested_email = COALESCE(NULLIF(excluded.suggested_email, ''), instagram_leads.suggested_email),
            notes = COALESCE(NULLIF(excluded.notes, ''), instagram_leads.notes),
            last_seen_at = excluded.last_seen_at
        """,
        {
            **{field: row.get(field, "") for field in FIELDNAMES},
            "campaign": campaign,
            "username": username,
            "icp_fit_score": as_int(row.get("icp_fit_score", "")),
            "urgency_score": as_int(row.get("urgency_score", "")),
            "business_value_score": as_int(row.get("business_value_score", "")),
            "now": now,
        },
    )
    conn.commit()


def filter_rows(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    init_db(conn)
    fresh: list[dict[str, str]] = []
    repeats: list[dict[str, str]] = []
    skipped = Counter()

    for row in read_rows(args.input):
        username = normalize_username(row.get("username", ""))
        if not username:
            continue
        row["username"] = username
        existing = get_existing(conn, args.campaign, username)
        if existing:
            enriched = dict(row)
            enriched["existing_status"] = existing["status"]
            enriched["first_found_at"] = existing["first_found_at"]
            enriched["last_seen_at"] = existing["last_seen_at"]
            repeats.append(enriched)
            skipped[existing["status"]] += 1
        else:
            fresh.append(row)
            if args.record_found:
                record_found(conn, args.campaign, row)

    write_rows(args.fresh_output, fresh)
    write_rows(args.repeats_output, repeats)
    if skipped:
        summary = ", ".join(f"{count} {status}" for status, count in sorted(skipped.items()))
        print(f"Skipped {sum(skipped.values())} previously seen Instagram accounts: {summary}.")
    else:
        print("Skipped 0 previously seen Instagram accounts.")
    print(f"Wrote {len(fresh)} fresh accounts to {args.fresh_output}")
    print(f"Wrote {len(repeats)} repeat accounts to {args.repeats_output}")
    return 0


def mark(args: argparse.Namespace) -> int:
    if args.status not in STATUSES:
        raise SystemExit(f"Invalid status '{args.status}'. Use one of: {', '.join(sorted(STATUSES))}")
    username = normalize_username(args.username)
    conn = connect(args.db)
    init_db(conn)
    existing = get_existing(conn, args.campaign, username)
    now = utc_now()
    if existing is None:
        conn.execute(
            """
            INSERT INTO instagram_leads (
                campaign, username, profile_url, status, notes, first_found_at, last_seen_at, last_status_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (args.campaign, username, f"https://www.instagram.com/{username}/", args.status, args.note or "", now, now, now),
        )
        lead_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    else:
        lead_id = existing["id"]
        note = args.note if args.note else existing["notes"]
        conn.execute(
            "UPDATE instagram_leads SET status = ?, notes = ?, last_status_at = ?, last_seen_at = ? WHERE id = ?",
            (args.status, note, now, now, lead_id),
        )
    conn.execute(
        "INSERT INTO status_events (lead_id, status, note, created_at) VALUES (?, ?, ?, ?)",
        (lead_id, args.status, args.note or "", now),
    )
    conn.commit()
    print(f"Marked @{username} as {args.status} for campaign '{args.campaign}'.")
    return 0


def export(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    init_db(conn)
    rows = conn.execute(
        "SELECT * FROM instagram_leads WHERE campaign = ? ORDER BY last_seen_at DESC, username",
        (args.campaign,),
    ).fetchall()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["campaign", *FIELDNAMES, "status", "first_found_at", "last_seen_at", "last_status_at"]
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))
    print(f"Exported {len(rows)} Instagram leads to {args.output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help=f"SQLite database path (default: {DEFAULT_DB})")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the database")

    filter_parser = subparsers.add_parser("filter", help="Split input CSV into fresh and repeat accounts")
    filter_parser.add_argument("--campaign", required=True)
    filter_parser.add_argument("--input", required=True, type=Path)
    filter_parser.add_argument("--fresh-output", required=True, type=Path)
    filter_parser.add_argument("--repeats-output", required=True, type=Path)
    filter_parser.add_argument("--record-found", action="store_true")

    mark_parser = subparsers.add_parser("mark", help="Mark an account status")
    mark_parser.add_argument("--campaign", required=True)
    mark_parser.add_argument("--username", required=True)
    mark_parser.add_argument("--status", required=True)
    mark_parser.add_argument("--note", default="")

    export_parser = subparsers.add_parser("export", help="Export one campaign to CSV")
    export_parser.add_argument("--campaign", required=True)
    export_parser.add_argument("--output", required=True, type=Path)

    args = parser.parse_args()
    if args.command == "init":
        conn = connect(args.db)
        init_db(conn)
        print(f"Initialized Instagram lead database at {args.db}")
        return 0
    if args.command == "filter":
        return filter_rows(args)
    if args.command == "mark":
        return mark(args)
    if args.command == "export":
        return export(args)
    raise SystemExit("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
