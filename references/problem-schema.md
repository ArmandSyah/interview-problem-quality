# Problem schema

Preferred fields:

- `id`
- `title`
- `difficulty`
- `tags`
- `pattern_tags`
- `pattern_family`
- `primary_skill`
- `secondary_skills`
- `interview_signal`
- `expected_time_minutes`
- `description_md`
- `examples`
- `constraints`
- `starter_code`
- `test_cases`
- `canonical_solution_md`
- `fallback_hints`
- `common_mistakes`
- `follow_up_questions`
- `suboptimal_solutions`
- `source_inspiration`
- `do_not_publish_reason`

Accepted problems must be executable by the current Python runner:

- `starter_code.python` defines one clear top-level function.
- `test_cases.python[*].input` is a list of positional arguments.
- Expected output is deterministic and JSON-compatible.
- Equality-based checking is sufficient.
- If multiple outputs are valid, reject or park the problem until custom checkers exist.

Required stage expectations:

- Drafts may have incomplete review metadata, but must be coherent enough to validate.
- Accepted problems must include Python starter code, 6-10 Python tests, exactly 3 fallback hints,
  common mistakes, follow-up questions, and prose-only canonical solution notes.
- Public candidates must include a clear originality note and a human approval decision.
