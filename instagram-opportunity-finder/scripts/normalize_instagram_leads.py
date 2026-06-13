#!/usr/bin/env python3
"""Normalize, validate, dedupe, and sort Instagram lead CSV files."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


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

USERNAME_RE = re.compile(r"^[A-Za-z0-9._]{1,30}$")
SCORE_FIELDS = ("icp_fit_score", "urgency_score", "business_value_score")
FIT_ORDER = {
    "dm-worthy": 0,
    "email-worthy": 1,
    "comment-worthy": 2,
    "research-only": 3,
    "not-fit": 4,
    "avoid": 5,
}


def normalize_username(value: str) -> str:
    value = (value or "").strip()
    value = value.replace("https://www.instagram.com/", "")
    value = value.replace("https://instagram.com/", "")
    value = value.replace("http://www.instagram.com/", "")
    value = value.replace("http://instagram.com/", "")
    value = value.lstrip("@").strip().strip("/")
    if "/" in value:
        value = value.split("/", 1)[0]
    return value.lower()


def profile_url(username: str, existing: str = "") -> str:
    existing = (existing or "").strip()
    if existing:
        parsed = urlparse(existing if "://" in existing else f"https://{existing}")
        if "instagram.com" in parsed.netloc.lower():
            path = parsed.path.strip("/")
            if path:
                first = path.split("/", 1)[0]
                if first.lower() not in {"p", "reel", "reels", "stories", "explore"}:
                    return f"https://www.instagram.com/{first}/"
    return f"https://www.instagram.com/{username}/" if username else ""


def normalize_score(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    try:
        score = int(float(value))
    except ValueError:
        return ""
    return str(min(5, max(1, score)))


def normalize_fit(value: str) -> str:
    value = (value or "").strip().lower()
    aliases = {
        "dm": "dm-worthy",
        "dm worthy": "dm-worthy",
        "email": "email-worthy",
        "comment": "comment-worthy",
        "research": "research-only",
        "research only": "research-only",
        "not fit": "not-fit",
    }
    return aliases.get(value, value if value in FIT_ORDER else "")


def normalize_risk(value: str) -> str:
    value = (value or "").strip().lower()
    return value if value in {"low", "medium", "high"} else ""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def normalize_row(row: dict[str, str]) -> dict[str, str] | None:
    username = normalize_username(row.get("username") or row.get("handle") or row.get("account") or row.get("profile_url"))
    if not username or not USERNAME_RE.match(username):
        return None

    out = {field: (row.get(field, "") or "").strip() for field in FIELDNAMES}
    out["username"] = username
    out["profile_url"] = profile_url(username, out.get("profile_url", ""))
    out["outreach_fit"] = normalize_fit(out.get("outreach_fit", ""))
    out["sensitivity_risk"] = normalize_risk(out.get("sensitivity_risk", ""))
    for field in SCORE_FIELDS:
        out[field] = normalize_score(out.get(field, ""))
    return out


def row_sort_key(row: dict[str, str]) -> tuple[int, int, int, str]:
    fit_rank = FIT_ORDER.get(row.get("outreach_fit", ""), 99)
    total = sum(int(row.get(field) or 0) for field in SCORE_FIELDS)
    risk_penalty = {"low": 0, "medium": 1, "high": 5}.get(row.get("sensitivity_risk", ""), 2)
    return (fit_rank + risk_penalty, -total, -int(row.get("urgency_score") or 0), row["username"])


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Raw Instagram lead CSV")
    parser.add_argument("--output", required=True, type=Path, help="Normalized output CSV")
    args = parser.parse_args()

    rows = read_rows(args.input)
    by_username: dict[str, dict[str, str]] = {}
    dropped = 0
    for row in rows:
        normalized = normalize_row(row)
        if not normalized:
            dropped += 1
            continue
        existing = by_username.get(normalized["username"])
        if existing is None or row_sort_key(normalized) < row_sort_key(existing):
            by_username[normalized["username"]] = normalized

    output_rows = sorted(by_username.values(), key=row_sort_key)
    write_rows(args.output, output_rows)
    print(f"Wrote {len(output_rows)} normalized Instagram leads to {args.output}")
    if dropped:
        print(f"Dropped {dropped} rows with missing/invalid usernames", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
