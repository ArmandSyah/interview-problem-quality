# Adversarial review rubric

Reviewers should attack the draft, not polish it.

Severity levels:

- `pass`: no meaningful issue.
- `minor`: small clarity, metadata, or test improvement.
- `major`: blocks acceptance until revised.
- `reject`: core idea is unsafe, too derivative, ambiguous, or low value.
- `park`: potentially useful, but blocked by missing runtime support or unresolved product choice.

Review dimensions:

- Originality: known-problem clone risk, copied framing, copied examples, copied constraints.
- Clarity: unambiguous task, explicit tie-breaking, readable examples.
- Runtime fit: Python starter code, positional JSON inputs, deterministic expected output.
- Test strength: catches common wrong approaches and edge cases.
- Hint safety: no code leakage or implementation-by-prose.
- Senior ROI: meaningful invariant, trade-off, or system of constraints.

A review finding should include the severity, evidence, why it matters, and the minimum change that
would resolve it.
