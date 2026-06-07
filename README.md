# interview-problem-quality

Portable skill, prompts, rubrics, and deterministic checks for generating and
reviewing original coding interview problems.

This repo is the quality/tooling layer. It does not store private drafts or the
runtime MCP server.

## Load the skill in an agent harness

Use this repo as explicit context whenever an agent generates, reviews, revises,
or validates interview problems.

Core files:

- `SKILL.md`: main skill instructions and workflow.
- `context-manifest.yaml`: required context contract.
- `references/`: schema, hint rules, source-use policy, test rules, lifecycle,
  and review rubrics.
- `prompts/`: role prompts for authoring and adversarial review.
- `scripts/`: deterministic validators and packet/summary tools.

### Codex

Open the repo that stores your private content, then tell Codex where this skill
repo is mounted.

Prompt shape:

```text
Use the interview-problem-quality skill from:
  <quality-repo>/SKILL.md

Before generating or reviewing, verify the required context from:
  <quality-repo>/context-manifest.yaml

Task:
  Read the full pattern spec at <ops-repo>/batches/<batch>/pattern-specs/<spec>.md.
  Generate 3 candidate problem concepts.
  Do not write files yet.
  Stop after recommending the strongest concept.
```

### Claude Code

Mount or open both repos in the same workspace:

- the private content repo, usually `interview-mcp-ops`
- this quality repo, `interview-problem-quality`

Then point Claude to the skill explicitly:

```text
Use <quality-repo>/SKILL.md and the required files in
<quality-repo>/context-manifest.yaml.

Read the full pattern spec:
  <ops-repo>/batches/<batch>/pattern-specs/<spec>.md

Generate 3 candidate concepts only. Do not save files yet.
```

For high-token or multi-agent Claude workflows, give each agent one narrow role:

- pattern designer
- problem author
- originality reviewer
- constraint reviewer
- test breaker
- hint leakage reviewer
- senior ROI reviewer
- revision agent

Do not let the same role generate, approve, and promote a problem.

### Other harnesses

Any harness can use the repo if it can read files and run Python scripts.
Provide these inputs explicitly:

```text
Quality repo:
  <quality-repo>

Private content repo:
  <ops-repo>

Required skill:
  <quality-repo>/SKILL.md

Required manifest:
  <quality-repo>/context-manifest.yaml
```

If required context is missing, the harness should stop and report the missing
file instead of continuing from memory.

## Generate a question from a pattern spec

Question generation is a staged workflow. Do not jump straight from a pattern
spec to an accepted problem.

### 1. Generate candidates

```text
Use the interview-problem-quality skill.

Read the full pattern spec:
  <ops-repo>/batches/<batch>/pattern-specs/<spec>.md

Generate 3 candidate problem concepts.
Do not write files yet.
Stop after recommending the strongest concept.
```

### 2. Create one selected draft

After a human chooses a concept:

```text
Create one problem JSON draft from the selected concept.

Save it to:
  <ops-repo>/problems/drafts/<problem-id>.json

Fix only mechanical validator errors.
Stop after validation passes.
```

Validate:

```bash
python <quality-repo>/scripts/validate_problem_json.py \
  <ops-repo>/problems/drafts/<problem-id>.json \
  --stage draft
```

### 3. Run adversarial review

```text
Run adversarial review for:
  <ops-repo>/problems/drafts/<problem-id>.json

Use these roles:
- originality
- constraints
- test-breaker
- hint-leakage
- senior-roi
- source-similarity if public-risk or clone-risk is suspected

Write reports to:
  <ops-repo>/reviews/agent/

Apply only tracked revisions for concrete findings.
Re-run validation.
Do not create human decisions.
```

### 4. Export a human packet

```bash
python <quality-repo>/scripts/export_review_packet.py \
  <ops-repo>/problems/drafts/<problem-id>.json \
  --review <ops-repo>/reviews/agent/<problem-id>.merged.md \
  --review <ops-repo>/reviews/agent/<problem-id>.originality.md \
  --review <ops-repo>/reviews/agent/<problem-id>.test-breaker.md \
  --review <ops-repo>/reviews/agent/<problem-id>.hint-leakage.md \
  --review <ops-repo>/reviews/agent/<problem-id>.senior-roi.md \
  --out <ops-repo>/reviews/packets/<problem-id>.md
```

After packet export, the agent must stop. A human reads the packet and provides
`accept`, `revise`, `reject`, or `park`.

## Human-review boundary

Agents may not create `reviews/human/*.md`, mark human decisions as complete, or
promote problems based on their own judgment unless the human decision text is
provided explicitly.

If a human decision is `revise`, send the draft back through a tracked revision
and validation loop. Do not silently rewrite during human review.

## Scripts

Validate a draft:

```bash
python scripts/validate_problem_json.py <problem.json> --stage draft
```

Validate an accepted problem:

```bash
python scripts/validate_problem_json.py <problem.json> --stage accepted
```

Export a human packet:

```bash
python scripts/export_review_packet.py <problem.json> \
  --review <review.md> \
  --out <packet.md>
```

Summarize accepted curriculum coverage:

```bash
python scripts/summarize_curriculum.py <accepted-problems-dir>
```
