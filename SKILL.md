---
name: interview-problem-quality
description: Use this skill when generating, reviewing, revising, or quality-checking original coding interview problems for interview-mcp. It applies pattern-first authoring, source-use limits, senior-level ROI standards, hint leakage rules, deterministic JSON validation, adversarial review rubrics, and human review packet conventions. Use it for problem JSON, curriculum coverage, test design, fallback hints, canonical solution prose, source-use review, and promotion from draft to accepted content.
---

# Interview Problem Quality

Use this skill for coding-interview problem authoring and review.

## Required workflow

1. Confirm required context from `context-manifest.yaml` is available.
2. Identify the task type: pattern spec, draft generation, adversarial review,
   test breaking, hint leakage review, revision, or human review packet.
3. Load only the relevant references for that task.
4. Enforce originality: sources may inspire patterns, not wording, examples,
   solution prose, distinctive framing, or code.
5. Prefer pattern-first, senior-ROI problems with explicit constraints and tests.
6. Never place solution code in hints or canonical solution prose.
7. Run deterministic validators before marking a problem review-ready.
8. If required context is missing, stop and report what is missing.

## Reference map

- Schema and fields: `references/problem-schema.md`
- Source use: `references/source-use-policy.md`
- Hints: `references/hint-rules.md`
- Tests: `references/test-design-rules.md`
- Senior ROI: `references/senior-roi-patterns.md`
- Adversarial review: `references/adversarial-review-rubric.md`
- Human review: `references/human-review-rubric.md`
- Lifecycle: `references/lifecycle.md`