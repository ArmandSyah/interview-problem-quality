# interview-problem-quality

Portable skill, prompts, rubrics, and deterministic checks for generating and
reviewing original coding interview problems.

This repo is the quality/tooling layer. It does not store private drafts or the
runtime MCP server.

## What this repo is for

Use this repo when an agent needs to:

- generate candidate coding-interview problems from pattern specs
- write problem JSON drafts
- validate problem JSON mechanically
- run adversarial review roles
- revise drafts with traceable changes
- export human review packets
- summarize accepted curriculum coverage

Private drafts, review reports, packets, and accepted content belong in the
private content repo, usually `interview-mcp-ops`. Runtime MCP server code
belongs in `interview-mcp`.

## Core files

- `SKILL.md`: primary skill instructions.
- `context-manifest.yaml`: required context contract.
- `references/`: schema, source-use policy, hint rules, test rules, lifecycle,
  and review rubrics.
- `prompts/`: role prompts for authoring and adversarial review.
- `scripts/`: deterministic validators, packet export, and curriculum summary.
- `AGENTS.md`: simple agent instructions for tools that read `AGENTS.md`.
- `CLAUDE.md`: Claude Code repo instructions.
- `.kiro/steering/interview-problem-quality.md`: Kiro workspace steering.

## Claude Code

Claude Code skills are directories that contain a required `SKILL.md`. The
directory name becomes the slash command. Claude Code supports personal skills
at `~/.claude/skills/<skill-name>/SKILL.md` and project skills at
`.claude/skills/<skill-name>/SKILL.md`.

### Option A: personal skill

Use this when you want the skill available across projects.

```bash
mkdir -p ~/.claude/skills/interview-problem-quality
cp -R <quality-repo>/* ~/.claude/skills/interview-problem-quality/
```

Then start Claude Code from the private content repo:

```bash
cd <ops-repo>
claude
```

Invoke the skill:

```text
/interview-problem-quality

Read the full pattern spec:
batches/<batch>/pattern-specs/<spec>.md

Generate 3 candidate problem concepts.
Do not write files yet.
Stop after recommending the strongest concept.
```

### Option B: project skill

Use this when you want the skill tied to one workspace.

```bash
mkdir -p <ops-repo>/.claude/skills/interview-problem-quality
cp -R <quality-repo>/* <ops-repo>/.claude/skills/interview-problem-quality/
```

Then:

```bash
cd <ops-repo>
claude
```

Invoke:

```text
/interview-problem-quality
```

Do not commit copied skill files into the private content repo unless that is an
intentional team decision.

### Option C: additional directory

Claude Code's `--add-dir` grants file access to another directory. Skills inside
an added directory are only loaded automatically when that directory contains a
`.claude/skills/...` layout. Granting file access is not the same as installing a
skill.

Use this shape if you keep shared skills elsewhere:

```text
<shared-dir>/.claude/skills/interview-problem-quality/SKILL.md
```

Then:

```bash
cd <ops-repo>
claude --add-dir <shared-dir>
```

## Codex

Codex uses `AGENTS.md` as repo guidance. This repo includes `AGENTS.md`, but the
reusable workflow itself lives in `SKILL.md`.

Practical setup:

1. Open the private content repo in Codex.
2. Put an `AGENTS.md` in that repo that points Codex to this quality repo.
3. Make sure Codex can read this quality repo.
4. If your Codex surface exposes a Skills installer, install this repo as a
   skill there. If not, explicitly point Codex at `SKILL.md` in the prompt.

Prompt shape:

```text
Use the quality workflow from:
  <quality-repo>/SKILL.md

Before generating or reviewing, verify:
  <quality-repo>/context-manifest.yaml

Read the full pattern spec:
  batches/<batch>/pattern-specs/<spec>.md

Generate 3 candidate problem concepts.
Do not write files yet.
Stop after recommending the strongest concept.
```

If using only `AGENTS.md`, place an agent instruction file in the private
content repo root that points Codex to this quality repo and says when to read
`SKILL.md`.

## Kiro

Kiro uses steering files for persistent project knowledge. Workspace steering
files live under:

```text
<repo>/.kiro/steering/
```

Global steering files live under:

```text
~/.kiro/steering/
```

This repo already includes:

```text
.kiro/steering/interview-problem-quality.md
```

To use this workflow in Kiro for the private content repo, copy or adapt that
file into the ops repo:

```bash
mkdir -p <ops-repo>/.kiro/steering
cp <quality-repo>/.kiro/steering/interview-problem-quality.md \
  <ops-repo>/.kiro/steering/interview-problem-quality.md
```

Then open the ops repo in Kiro. Kiro should pick up workspace steering from
`.kiro/steering/`. For a one-off task, also explicitly tell Kiro:

```text
Use <quality-repo>/SKILL.md and verify <quality-repo>/context-manifest.yaml.
Read the full pattern spec at batches/<batch>/pattern-specs/<spec>.md.
Generate 3 candidate concepts only. Do not save files yet.
```

## Cursor

Cursor supports project rules in `.cursor/rules`, user rules in settings,
`AGENTS.md` in the project root, and legacy `.cursorrules`.

For this workflow, use `AGENTS.md` for the simple repo-level instruction, or a
project rule if you want Cursor-specific metadata.

### Simple setup with AGENTS.md

Copy or adapt this repo's `AGENTS.md` into the private content repo root:

```bash
cp <quality-repo>/AGENTS.md <ops-repo>/AGENTS.md
```

Then add a short line to the copied file:

```markdown
For problem generation and review, read `<quality-repo>/SKILL.md` and
`<quality-repo>/context-manifest.yaml` before working.
```

### Project rule setup

Create a Cursor project rule from Cursor with `New Cursor Rule`, or create a
rule under:

```text
<ops-repo>/.cursor/rules/
```

Use it to point Cursor at:

```text
<quality-repo>/SKILL.md
<quality-repo>/context-manifest.yaml
```

Do not use `.cursorrules` for new setup unless you are maintaining legacy
Cursor configuration.

## Generic harness

Any agent harness can use this repo if it can read files and run Python scripts.
Provide these paths explicitly:

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

If any required context is missing, the harness must stop and report the missing
file instead of continuing from memory.

## Question-generation workflow

### 1. Generate candidate concepts

Use the full pattern spec as context. Do not slice the file unless you are only
previewing it in a terminal.

```text
Use the interview-problem-quality workflow.

Read the full pattern spec:
  batches/<batch>/pattern-specs/<spec>.md

Generate 3 candidate problem concepts.
Do not write files yet.
Stop after recommending the strongest concept.
```

### 2. Create one selected draft

After a human chooses a concept:

```text
Create one problem JSON draft from the selected concept.

Save it to:
  problems/drafts/<problem-id>.json

Fix only mechanical validator errors.
Stop after validation passes.
```

Validate:

```bash
python <quality-repo>/scripts/validate_problem_json.py \
  problems/drafts/<problem-id>.json \
  --stage draft
```

Mechanical validation checks structure, parseable starter code, test shape, and
obvious code leakage. It does not prove originality, interview value, or public
safety.

### 3. Run adversarial review

```text
Run adversarial review for:
  problems/drafts/<problem-id>.json

Use these roles:
- originality
- constraints
- test-breaker
- hint-leakage
- senior-roi
- source-similarity if public-risk or clone-risk is suspected

Write reports to:
  reviews/agent/

Apply only tracked revisions for concrete findings.
Re-run validation.
Do not create human decisions.
```

### 4. Export a human review packet

```bash
python <quality-repo>/scripts/export_review_packet.py \
  problems/drafts/<problem-id>.json \
  --review reviews/agent/<problem-id>.merged.md \
  --review reviews/agent/<problem-id>.originality.md \
  --review reviews/agent/<problem-id>.test-breaker.md \
  --review reviews/agent/<problem-id>.hint-leakage.md \
  --review reviews/agent/<problem-id>.senior-roi.md \
  --out reviews/packets/<problem-id>.md
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

## Sources checked

- Claude Code skills docs: https://code.claude.com/docs/en/skills
- Claude custom skills help: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- Kiro steering docs: https://kiro.dev/docs/steering/
- Cursor rules docs: https://docs.cursor.com/context/rules-for-ai
- OpenAI Codex `AGENTS.md` docs: https://github.com/openai/codex/blob/main/docs/agents_md.md
- AGENTS.md format repository: https://github.com/agentsmd/agents.md
