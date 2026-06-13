#!/usr/bin/env python3
"""
Initialize a persistent .reddit-growth workspace in a project directory.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re


PROJECT_PROFILE_TEMPLATE = """# {project_name} - Reddit Growth Profile

**Created:** {today}
**Last Updated:** {today}

## Product
- **Name:** {project_name}
- **URL:** 
- **Type:** 
- **One-line description:** 

## Audience
- **Primary ICP:** 
- **Secondary ICP:** 
- **Geography or language:** 

## Customer Pain
- 
- 
- 

## Offer and Conversion Goal
- **Primary goal:** 
- **Desired action:** 

## Positioning
- **Approved positioning:** 
- **Competitors or alternatives:** 
- **Keywords and pain phrases:** 

## Compliance Notes
- **Claims to avoid:** 
- **Disclosure requirements:** 
- **Approved links:** 

## Notes
- 
"""


ACTIVITY_LOG_TEMPLATE = """# Reddit Growth Activity Log

Track research sessions, drafts, approved posts, and early outcomes here.
"""


INSIGHTS_TEMPLATE = """# Reddit Growth Insights

Use this file to store patterns that should influence future Reddit research or drafting.
"""


DIRECTORIES = [
    "subreddits",
    "rules",
    "searches",
    "opportunities",
    "drafts",
    "posted",
    "rejected",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    return slug.strip("-") or "project"


def write_file(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def init_workspace(base_path: Path, project_name: str) -> Path:
    root = base_path / ".reddit-growth"
    root.mkdir(parents=True, exist_ok=True)

    for directory in DIRECTORIES:
        (root / directory).mkdir(exist_ok=True)

    today = date.today().isoformat()
    write_file(
        root / "project-profile.md",
        PROJECT_PROFILE_TEMPLATE.format(project_name=project_name, today=today),
    )
    write_file(root / "activity-log.md", ACTIVITY_LOG_TEMPLATE)
    write_file(root / "insights.md", INSIGHTS_TEMPLATE)

    return root


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a .reddit-growth directory for persistent Reddit research.",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Project directory where .reddit-growth should be created.",
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="Project or product name for the initial profile template.",
    )
    args = parser.parse_args()

    base_path = Path(args.path).resolve()
    base_path.mkdir(parents=True, exist_ok=True)

    project_name = args.project_name.strip()
    if not project_name:
        project_name = slugify(args.project_name).replace("-", " ").title()

    workspace_path = init_workspace(base_path, project_name)
    print(f"[OK] Initialized Reddit growth workspace at {workspace_path}")


if __name__ == "__main__":
    main()
