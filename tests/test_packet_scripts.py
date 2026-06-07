from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.export_review_packet import build_packet
from scripts.summarize_curriculum import build_summary


def problem(
    problem_id: str = "0001-signal-window",
    difficulty: str = "easy",
    pattern_family: str = "sliding-window",
) -> dict[str, Any]:
    return {
        "id": problem_id,
        "title": "Signal Window",
        "difficulty": difficulty,
        "pattern_family": pattern_family,
        "primary_skill": "Maintain a bounded window with a running aggregate.",
        "expected_time_minutes": 20,
        "description_md": "Find the maximum signal total for a fixed-size window.",
        "constraints": ["1 <= size <= len(signals)", "Signals may be negative."],
        "test_cases": {"python": [{"input": [[1, 2], 2], "expected": 3}]},
    }


def test_build_packet_includes_problem_review_and_decision_prompt() -> None:
    packet = build_packet(problem(), ["## Review: senior-roi.md\n\nWorth asking."])

    assert "# Human Review Packet: 0001-signal-window" in packet
    assert "**Pattern family:** sliding-window" in packet
    assert "- 1 <= size <= len(signals)" in packet
    assert "Python tests: 1" in packet
    assert "## Review: senior-roi.md" in packet
    assert "Decision: accept | revise | reject | park" in packet


def test_export_review_packet_cli_writes_markdown(tmp_path: Path) -> None:
    problem_path = tmp_path / "problem.json"
    review_path = tmp_path / "constraint-review.md"
    out_path = tmp_path / "packet.md"
    problem_path.write_text(json.dumps(problem()), encoding="utf-8")
    review_path.write_text("Constraints are clear.", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/export_review_packet.py",
            str(problem_path),
            "--review",
            str(review_path),
            "--out",
            str(out_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert str(out_path) in result.stdout
    assert "## Review: constraint-review.md" in out_path.read_text(encoding="utf-8")


def test_build_summary_counts_family_and_difficulty(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first.write_text(json.dumps(problem()), encoding="utf-8")
    second.write_text(
        json.dumps(problem("0002-cache-hit", "medium", "hash-map")),
        encoding="utf-8",
    )

    summary = build_summary([first, second])

    assert "Problems counted: 2" in summary
    assert "- hash-map: 1" in summary
    assert "- sliding-window: 1" in summary
    assert "- easy: 1" in summary
    assert "- medium: 1" in summary
    assert "- hash-map / medium: 1" in summary


def test_summarize_curriculum_cli_prints_summary() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/summarize_curriculum.py", "examples"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "# Curriculum Summary" in result.stdout
    assert "Problems counted: 1" in result.stdout
    assert "- sliding-window: 1" in result.stdout


def test_context_manifest_required_files_exist() -> None:
    manifest = yaml.safe_load(Path("context-manifest.yaml").read_text(encoding="utf-8"))
    required_files = [
        *manifest["required_references"],
        *manifest["required_prompts"],
        *manifest["required_scripts"],
    ]

    missing_files = [path for path in required_files if not Path(path).is_file()]

    assert missing_files == []
