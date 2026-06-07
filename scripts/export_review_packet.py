#!/usr/bin/env python3
"""Export a compact Markdown review packet for a problem draft."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from disk."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("problem JSON must be an object")
    return data


def read_reviews(paths: list[Path]) -> list[str]:
    """Read review files as Markdown sections."""
    chunks: list[str] = []
    for path in paths:
        chunks.append(f"## Review: {path.name}\n\n{path.read_text(encoding='utf-8').strip()}")
    return chunks


def build_packet(problem: dict[str, Any], reviews: list[str]) -> str:
    """Build a Markdown packet for human review."""
    tests = problem.get("test_cases", {}).get("python", [])
    constraints = problem.get("constraints", [])
    lines = [
        f"# Human Review Packet: {problem.get('id', '<missing-id>')}",
        "",
        f"**Title:** {problem.get('title', '')}",
        f"**Difficulty:** {problem.get('difficulty', '')}",
        f"**Pattern family:** {problem.get('pattern_family', '')}",
        f"**Primary skill:** {problem.get('primary_skill', '')}",
        f"**Expected time:** {problem.get('expected_time_minutes', '')} minutes",
        "",
        "## Description",
        "",
        str(problem.get("description_md", "")).strip(),
        "",
        "## Constraints",
        "",
        "\n".join(f"- {item}" for item in constraints),
        "",
        "## Test summary",
        "",
        f"Python tests: {len(tests) if isinstance(tests, list) else 0}",
        "",
        "## Agent reviews",
        "",
    ]
    lines.extend(reviews or ["No review files provided."])
    lines.extend(
        [
            "",
            "## Human decision",
            "",
            "Decision: accept | revise | reject | park",
            "",
            "Required notes:",
            "- Is this original enough?",
            "- Would you ask this in a senior interview?",
            "- Does it train the stated pattern?",
            "- Are remaining risks acceptable?",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("problem", type=Path)
    parser.add_argument("--review", action="append", type=Path, default=[])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    packet = build_packet(read_json(args.problem), read_reviews(args.review))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(packet, encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
