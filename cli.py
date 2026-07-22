"""Command-line interface for the Autonomous Workflow Agent.

Usage:
    python cli.py
    python cli.py --lead data/lead.json
    python cli.py --output outputs/result.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from workflow.runner import run

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def load_lead(path: Path) -> dict:
    if not path.exists():
        logger.error("Lead file not found: %s", path)
        sys.exit(1)
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in lead file: %s", exc)
        sys.exit(1)


def save_output(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("Result saved to %s", path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Autonomous Workflow Agent — qualify a B2B lead and generate a proposal email.",
    )
    parser.add_argument(
        "--lead",
        type=Path,
        help="Path to a JSON file describing the lead. Uses a default synthetic lead if omitted.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to write the full workflow JSON result.",
    )
    parser.add_argument(
        "--email-only",
        action="store_true",
        help="Print only the generated email instead of the full JSON result.",
    )
    args = parser.parse_args()

    lead = load_lead(args.lead) if args.lead else None

    result = run(lead)

    if args.email_only:
        proposal = result["proposal"]
        print(f"Subject: {proposal['subject']}\n")
        print(proposal["body"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.output:
        save_output(args.output, result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
