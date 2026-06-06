#!/usr/bin/env python3
"""Validate interview-mcp problem JSON drafts.

This is authoring-time content CI. It intentionally checks deterministic
properties only: schema presence, ID shape, parseable starter code, test counts,
and obvious code leakage in prose/hints.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

SAFE_ID = re.compile(r"^\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_DIFFICULTIES = {"easy", "medium", "hard"}
REQUIRED_FIELDS = [
    "id",
    "title",
    "difficulty",
    "tags",
    "pattern_tags",
    "pattern_family",
    "primary_skill",
    "secondary_skills",
    "interview_signal",
    "expected_time_minutes",
    "description_md",
    "examples",
    "constraints",
    "starter_code",
    "test_cases",
    "canonical_solution_md",
    "fallback_hints",
    "common_mistakes",
    "follow_up_questions",
    "suboptimal_solutions",
    "source_inspiration",
    "do_not_publish_reason",
]
CODE_LEAK_PATTERNS = [
    re.compile(r"```"),
    re.compile(r"\bdef\s+[a-zA-Z_]"),
    re.compile(r"\bclass\s+[a-zA-Z_]"),
    re.compile(r"\breturn\s+"),
    re.compile(r"\bfor\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\b"),
    re.compile(r"^\s*while\s+", re.MULTILINE),
]


def load_problem(path: Path) -> dict[str, Any]:
    """Load a problem JSON file and require an object at the top level."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data


def first_function_name(code: str) -> str:
    """Return the single top-level Python function name in starter code."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        raise ValueError(f"starter_code.python does not parse: {exc}") from exc

    function_names = [
        node.name for node in tree.body if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    ]
    if len(function_names) != 1:
        raise ValueError("starter_code.python must define exactly one top-level function")
    return function_names[0]


def contains_code_like_text(text: str) -> bool:
    """Return true when prose appears to contain code or a code fence."""
    return any(pattern.search(text) for pattern in CODE_LEAK_PATTERNS)


def validate(data: dict[str, Any], *, stage: str) -> list[str]:
    """Return deterministic validation errors for a problem draft."""
    errors: list[str] = []
    min_tests = 6 if stage == "accepted" else 3

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")
    if errors:
        return errors

    if not isinstance(data["id"], str) or not SAFE_ID.fullmatch(data["id"]):
        errors.append("id must match 0000-lowercase-slug")
    if data["difficulty"] not in VALID_DIFFICULTIES:
        errors.append("difficulty must be easy, medium, or hard")

    if len(data.get("constraints", [])) < 2:
        errors.append("constraints must contain at least 2 explicit constraints")
    if len(data.get("examples", [])) < 1:
        errors.append("examples must contain at least 1 example")

    starter = data.get("starter_code", {})
    if not isinstance(starter, dict) or "python" not in starter:
        errors.append("starter_code.python is required")
    else:
        try:
            first_function_name(str(starter["python"]))
        except ValueError as exc:
            errors.append(str(exc))

    raw_test_cases = data.get("test_cases")
    tests = raw_test_cases.get("python") if isinstance(raw_test_cases, dict) else None
    if not isinstance(tests, list):
        errors.append("test_cases.python must be a list")
    elif len(tests) < min_tests:
        errors.append(
            f"test_cases.python must contain at least {min_tests} tests for stage={stage}"
        )
    else:
        for index, test in enumerate(tests):
            if not isinstance(test, dict):
                errors.append(f"test {index} must be an object")
                continue
            if not isinstance(test.get("input"), list):
                errors.append(f"test {index}.input must be a list of positional arguments")
            if "expected" not in test:
                errors.append(f"test {index}.expected is required")

    canonical = str(data.get("canonical_solution_md", ""))
    if not canonical.strip():
        errors.append("canonical_solution_md is required")
    elif contains_code_like_text(canonical):
        errors.append("canonical_solution_md appears to contain code or code fences")

    hints = data.get("fallback_hints")
    if not isinstance(hints, list):
        errors.append("fallback_hints must be a list")
    else:
        if len(hints) != 3:
            errors.append("fallback_hints must contain exactly 3 hints")
        for index, hint in enumerate(hints):
            if contains_code_like_text(str(hint)):
                errors.append(f"fallback_hints[{index}] appears to contain code or code fences")

    follow_ups = data.get("follow_up_questions", [])
    if not isinstance(follow_ups, list) or len(follow_ups) < 3:
        errors.append("follow_up_questions should contain at least 3 interviewer questions")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--stage", choices=["draft", "accepted"], default="draft")
    args = parser.parse_args()

    try:
        errors = validate(load_problem(args.path), stage=args.stage)
    except Exception as exc:
        print(f"ERROR: {args.path}: {exc}")
        return 1

    if errors:
        print(f"FAIL: {args.path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
