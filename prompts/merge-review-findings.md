# Merge Review Findings

Before working, verify access to `context-manifest.yaml` and required references.

Your job is to merge multiple review reports into one actionable review packet.

Input:

- validator output
- originality review
- source-similarity review
- constraint review
- test breaker review
- hint leakage review
- senior ROI review

Return:

- `overall_status`: pass | needs_revision | human_review_required | reject | park
- `blocking_findings`: list
- `minor_findings`: list
- `accepted_revision_tasks`: list
- `reviewer_disagreements`: list
- `human_review_triggers`: list
- `notes`: short synthesis

Do not rewrite the problem. Do not approve the problem. Preserve reviewer disagreement instead of
smoothing it away.
