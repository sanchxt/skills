#!/usr/bin/env python3
"""Deduplicate, validate, and sort Reddit lead CSVs."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


COLUMNS = [
    "url",
    "type",
    "subreddit",
    "title_or_context",
    "date_or_age",
    "pain_category",
    "evidence_summary",
    "relevance_score",
    "freshness_score",
    "outreach_fit",
    "rule_risk",
    "sensitivity_risk",
    "suggested_angle",
    "notes",
]

REQUIRED_COLUMNS = set(COLUMNS)


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    parts = urlsplit(url)
    scheme = parts.scheme or "https"
    netloc = parts.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = parts.path.rstrip("/")
    return urlunsplit((scheme, netloc, path, "", ""))


def int_score(row: dict[str, str], column: str) -> int:
    try:
        return int(str(row.get(column, "")).strip())
    except ValueError:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    with args.input_csv.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            print("Input CSV has no header row.", file=sys.stderr)
            return 2

        missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
        if missing:
            print("Missing required columns: " + ", ".join(missing), file=sys.stderr)
            return 2

        best_by_url: dict[str, dict[str, str]] = {}
        for row in reader:
            normalized = normalize_url(row.get("url", ""))
            if not normalized:
                continue
            row["url"] = normalized
            previous = best_by_url.get(normalized)
            if previous is None:
                best_by_url[normalized] = row
                continue

            current_key = (
                int_score(row, "relevance_score"),
                int_score(row, "freshness_score"),
            )
            previous_key = (
                int_score(previous, "relevance_score"),
                int_score(previous, "freshness_score"),
            )
            if current_key > previous_key:
                best_by_url[normalized] = row

    rows = sorted(
        best_by_url.values(),
        key=lambda row: (
            int_score(row, "relevance_score"),
            int_score(row, "freshness_score"),
            row.get("outreach_fit", ""),
            row.get("subreddit", ""),
        ),
        reverse=True,
    )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in REQUIRED_COLUMNS})

    print(f"Wrote {len(rows)} unique leads to {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
