# Problem lifecycle

States:

1. `draft`
2. `mechanically_valid`
3. `agent_reviewed`
4. `needs_revision`
5. `human_review_required`
6. `human_approved`
7. `accepted`
8. `rejected`
9. `parked`

Promotion rules:

- `draft` -> `mechanically_valid`: deterministic validator passes.
- `mechanically_valid` -> `agent_reviewed`: adversarial review, test breaker,
  source-similarity review, and hint leakage review complete.
- Any major or reject finding -> `needs_revision` or `human_review_required`.
- First problem in a new pattern family requires human review.
- Public candidates require human review.
- One in five otherwise clean accepted-by-agents problems requires random human spot-check.
- Max two revision cycles before reject or park.

Artifacts should move by scripts or harness actions, not manual copy-paste. The lifecycle is a state
machine for content quality, not a reason to make humans shuffle files by hand.
