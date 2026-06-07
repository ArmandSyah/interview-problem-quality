#!/usr/bin/env python3
"""Summarize accepted problem coverage by pattern family and difficulty."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read_problem(path: Path) -> dict[str, Any]:
    """Read one problem JSON object."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def find_problem_files(root: Path) -> list[Path]:
    """Return JSON problem files below a root directory."""
    if root.is_file():
        return [root]
    return sorted(path for path in root.rglob("*.json") if path.is_file())


def build_summary(paths: list[Path]) -> str:
    """Build a Markdown coverage summary from accepted problem files."""
    by_family: Counter[str] = Counter()
    by_difficulty: Counter[str] = Counter()
    by_family_and_difficulty: Counter[tuple[str, str]] = Counter()

    for path in paths:
        problem = read_problem(path)
        family = str(problem.get("pattern_family") or "<missing>")
        difficulty = str(problem.get("difficulty") or "<missing>")
        by_family[family] += 1
        by_difficulty[difficulty] += 1
        by_family_and_difficulty[(family, difficulty)] += 1

    lines = [
        "# Curriculum Summary",
        "",
        f"Problems counted: {len(paths)}",
        "",
        "## By pattern family",
        "",
    ]
    lines.extend(f"- {family}: {count}" for family, count in sorted(by_family.items()))
    lines.extend(["", "## By difficulty", ""])
    lines.extend(f"- {difficulty}: {count}" for difficulty, count in sorted(by_difficulty.items()))
    lines.extend(["", "## By pattern family and difficulty", ""])
    lines.extend(
        f"- {family} / {difficulty}: {count}"
        for (family, difficulty), count in sorted(by_family_and_difficulty.items())
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    files = find_problem_files(args.root)
    summary = build_summary(files)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(summary, encoding="utf-8")
        print(args.out)
    else:
        print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
