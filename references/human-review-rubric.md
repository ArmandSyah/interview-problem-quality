# Human review rubric

Humans review filtered risk, not every raw draft.

Require human review for:

- First accepted problem in a new pattern family.
- Any major, reject, or parked finding from an agent.
- Any disagreement between reviewers about originality or ambiguity.
- Public example candidates.
- One in five otherwise clean accepted-by-agents problems.

Human decisions:

- `accept`: ready for accepted private library.
- `revise`: specific changes required before another validation pass.
- `reject`: not worth further work.
- `park`: useful idea, blocked by runtime, curriculum, or product constraints.

Human review should focus on product value, originality risk, ambiguity, and whether the problem
would create a useful interview conversation. It should not become a copy-editing pass for every
sentence unless clarity blocks acceptance.
