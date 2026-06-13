# Week 3 Batch Report Example

## Summary

- Drafts generated: 10
- Drafts mechanically valid: 10
- Agent-reviewed: 10
- Accepted: 8
- Rejected: 1
- Parked: 1
- Public examples exported: 5

## Coverage

- Pattern families represented: graph, sliding-window, heap, intervals, dynamic-programming
- Overrepresented families: sliding-window
- Missing families: binary-search, union-find, trie, monotonic-stack

## Review metrics

- Average agent findings per problem: 1.6 Major or Minor findings
- Major finding rate: 30% of drafts had at least one Major finding
- Rejection rate: 10%
- Human packets generated: 10
- Human average review time: 5 minutes per packet

## Common defect classes

- Originality risk: story framing too close to common examples
- Ambiguous constraints: missing bounds for secondary state
- Weak tests: missing directed-edge, tie-breaking, or greedy-failure cases
- Hint leakage: hints drifted toward implementation details
- Generic follow-ups: follow-ups sometimes tested trivia instead of design trade-offs

## Process changes for next batch

1. Require each pattern spec to name one known-bad clone risk before drafting.
2. Require every reviewer Major finding to link to the exact review file and section.
3. Record human decisions only in review files, never only in chat.

## Automation candidates

- Safe to automate now: schema validation, packet export, curriculum summary, missing-file checks
- Needs more manual examples first: source-similarity scoring and senior-ROI scoring
- Should remain human-reviewed: public export approval and final accept/reject decisions

## Evidence

- Validation logs: `batches/<batch>/validation-log.md`
- Agent review files: `reviews/agent/<problem-id>.*.md`
- Human review records: `reviews/human/<problem-id>.md`
- Promotion records: `batches/<batch>/promotion-summary.md`
- Export records: runtime repo PR or export summary
