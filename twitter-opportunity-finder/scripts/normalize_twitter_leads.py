#!/usr/bin/env python3
"""Dedupe and sort X/Twitter opportunity CSVs."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


SCORE_FIELDS = ("relevance_score", "freshness_score", "engagement_score")
REQUIRED_FIELDS = ("url", "type", "evidence_summary", "outreach_fit")


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    url = url.replace("https://twitter.com/", "https://x.com/")
    url = re.sub(r"[?&](s|t|utm_[^=]+)=[^&]+", "", url)
    url = url.rstrip("?&/")
    return url


def parse_score(value: str) -> int:
    try:
        score = int(str(value).strip())
    except ValueError:
        return 0
    return max(0, min(score, 5))


def row_sort_key(row: dict[str, str]) -> tuple[int, int, int, str]:
    relevance = parse_score(row.get("relevance_score", "0"))
    freshness = parse_score(row.get("freshness_score", "0"))
    engagement = parse_score(row.get("engagement_score", "0"))
    fit_bonus = 1 if row.get("outreach_fit", "").strip() == "reply-worthy" else 0
    return (fit_bonus, relevance, freshness + engagement, row.get("url", ""))


def normalize(input_path: Path, output_path: Path) -> tuple[int, int]:
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        missing = [field for field in REQUIRED_FIELDS if field not in fieldnames]
        if missing:
            raise SystemExit(f"Missing required columns: {', '.join(missing)}")

        rows = []
        seen: set[str] = set()
        for row in reader:
            row["url"] = normalize_url(row.get("url", ""))
            if not row["url"] or row["url"] in seen:
                continue
            seen.add(row["url"])
            for field in SCORE_FIELDS:
                if field in fieldnames:
                    row[field] = str(parse_score(row.get(field, "0")))
            rows.append(row)

    rows.sort(key=row_sort_key, reverse=True)

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(seen), len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    unique_count, written_count = normalize(args.input_csv, args.output_csv)
    print(f"Unique URLs: {unique_count}")
    print(f"Rows written: {written_count}")


if __name__ == "__main__":
    main()
