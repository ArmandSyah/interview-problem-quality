# Claude Code instructions

Before generating or reviewing any interview problem, read `context-manifest.yaml`.
Then load the required references for the task.

Use this repo as the quality system only. Store actual drafts, reviews, and
human decisions in `interview-mcp-ops`. Do not add content-generation code to
`interview-mcp` unless explicitly requested for runtime behavior.

Before marking any problem review-ready, run:

```bash
python scripts/validate_problem_json.py path/to/problem.json --stage draft
```

Before marking any problem accepted, run:

```bash
python scripts/validate_problem_json.py path/to/problem.json --stage accepted
```

If any required reference is unavailable, stop and report the missing files.
