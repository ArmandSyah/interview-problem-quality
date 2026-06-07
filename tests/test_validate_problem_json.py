from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validate_problem_json import validate


def valid_problem() -> dict[str, Any]:
    return {
        "id": "0001-signal-window",
        "title": "Signal Window",
        "difficulty": "easy",
        "tags": ["array"],
        "pattern_tags": ["sliding-window"],
        "pattern_family": "sliding-window",
        "primary_skill": "Maintain a running window aggregate.",
        "secondary_skills": ["Boundary handling"],
        "interview_signal": "Candidate can maintain a moving invariant.",
        "expected_time_minutes": 20,
        "description_md": "Find the best fixed-size signal window.",
        "examples": [{"input": "signals=[1,2], size=2", "output": "3", "explanation": ""}],
        "constraints": ["1 <= size <= len(signals)", "Signals may be negative."],
        "starter_code": {
            "python": "def max_signal_window(signals: list[int], size: int) -> int:\n    pass\n"
        },
        "test_cases": {
            "python": [
                {"input": [[2, -1, 4, 3], 2], "expected": 7},
                {"input": [[5], 1], "expected": 5},
                {"input": [[-4, -2, -7], 2], "expected": -6},
                {"input": [[1, 2, 3, 4], 4], "expected": 10},
                {"input": [[3, 3, 3], 2], "expected": 6},
                {"input": [[10, -10, 10], 1], "expected": 10},
            ]
        },
        "canonical_solution_md": (
            "Maintain the total for the current fixed-size window. Slide one position "
            "at a time while preserving the invariant that the total matches the current window."
        ),
        "fallback_hints": [
            "Avoid recomputing overlapping windows from scratch.",
            "Track the sum of the current fixed-size window.",
            "Remove the leaving value, add the entering value, and update the best total.",
        ],
        "common_mistakes": ["Initializing the answer incorrectly for negative values."],
        "follow_up_questions": [
            "How does this change for a stream?",
            "What happens when all values are negative?",
            "What if the window size can vary?",
        ],
        "suboptimal_solutions": [
            {
                "name": "Recompute every window",
                "complexity": "O(n * size)",
                "description": "Repeats work for overlapping windows.",
            }
        ],
        "source_inspiration": [],
        "do_not_publish_reason": "",
    }


def test_valid_problem_passes_accepted_stage() -> None:
    assert validate(valid_problem(), stage="accepted") == []


def test_missing_field_fails() -> None:
    problem = valid_problem()
    del problem["title"]

    assert validate(problem, stage="draft") == ["missing required field: title"]


def test_bad_id_fails() -> None:
    problem = valid_problem()
    problem["id"] = "Signal Window"

    assert "id must match" in "\n".join(validate(problem, stage="draft"))


def test_draft_requires_three_tests() -> None:
    problem = valid_problem()
    problem["test_cases"]["python"] = problem["test_cases"]["python"][:2]

    assert "at least 3 tests" in "\n".join(validate(problem, stage="draft"))


def test_accepted_requires_six_tests() -> None:
    problem = valid_problem()
    problem["test_cases"]["python"] = problem["test_cases"]["python"][:5]

    assert "at least 6 tests" in "\n".join(validate(problem, stage="accepted"))


def test_code_in_canonical_solution_fails() -> None:
    problem = valid_problem()
    problem["canonical_solution_md"] = "Use this:\n```python\nreturn best\n```"

    assert "canonical_solution_md appears to contain code" in "\n".join(
        validate(problem, stage="accepted")
    )


def test_code_in_fallback_hint_fails() -> None:
    problem = valid_problem()
    problem["fallback_hints"][1] = "Write: return best"

    assert "fallback_hints[1] appears to contain code" in "\n".join(
        validate(problem, stage="accepted")
    )


def test_starter_code_with_two_functions_fails() -> None:
    problem = valid_problem()
    problem["starter_code"]["python"] = "def a():\n    pass\n\ndef b():\n    pass\n"

    assert "exactly one top-level function" in "\n".join(validate(problem, stage="accepted"))


def test_test_input_must_be_argument_list() -> None:
    problem = valid_problem()
    problem["test_cases"]["python"][0]["input"] = "not a list"

    assert "test 0.input must be a list" in "\n".join(validate(problem, stage="accepted"))


def test_cli_passes_good_example() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate_problem_json.py",
            "examples/good-problem.json",
            "--stage",
            "accepted",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "PASS: examples/good-problem.json" in result.stdout


def test_cli_fails_bad_problem(tmp_path: Path) -> None:
    problem = deepcopy(valid_problem())
    problem["fallback_hints"][0] = "```python\nreturn 1\n```"
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(problem), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate_problem_json.py",
            str(path),
            "--stage",
            "accepted",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "FAIL:" in result.stdout
    assert "fallback_hints[0] appears to contain code" in result.stdout
