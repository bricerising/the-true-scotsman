# LangChain CLIs (enterprise-software-playbook)

A small set of LangChain-based CLIs that run **enterprise-software-playbook** workflows:

- `code-review`: rigorous, multi-stage, multi-agent review (`review-protocol`)
- `feature-ideate`: propose next feature ideas (spec-aware)
- `feature-progress`: generate stakeholder-friendly progress updates from a diff
- `spec-align`: judge implementation alignment with a project’s `specs/` folder

All tools write artifacts into `.codex/` in the target repo, and treat repo text as **untrusted** (prompt injection guardrail).

## What they do

- `code-review`: `.codex/review-protocol/<HEAD_SHA>/<REVIEW_TYPE>/` with `1-critique.txt` → `5-report.md`
- `feature-ideate`: `.codex/feature-ideation/<HEAD_SHA>/` with `1-ideas.md`
- `feature-progress`: `.codex/feature-progress/<HEAD_SHA>/` with `1-update.md`
- `spec-align`: `.codex/spec-alignment/<HEAD_SHA>/` with `1-alignment.md`

## Install

Homebrew Python on macOS is often an “externally managed environment” (PEP 668), so install into an isolated env.

### Option A: `venv` (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e tools/langchain_clis
```

### Option B: `pipx` (good for CLIs)

```bash
brew install pipx
pipx install --editable tools/langchain_clis
```

## Environment

- `OPENAI_API_KEY` (for the default OpenAI-backed LangChain model)
- Optional: `ESB_SKILLS_DIR` (path to this skills repo root). If omitted, the CLI tries to auto-detect.

## Usage

### Code review (`code-review`)

Run a general review of the current repo’s uncommitted changes (default behavior uses `git diff HEAD`):

```bash
code-review run --review-type general
```

Review a PR-style range (merge-base to head):

```bash
code-review run --git-base origin/main --git-head HEAD --review-type general
```

Security-focused review:

```bash
code-review run --review-type security --git-base origin/main
```

Dry-run (write prompts/context to the output dir, but do not call the model):

```bash
code-review run --dry-run --review-type general
```

### Feature ideation (`feature-ideate`)

Propose spec-aware feature ideas (reads `<repo>/specs` if present):

```bash
feature-ideate run --focus "observability" --num-ideas 8
```

### Progress updates (`feature-progress`)

Generate a progress update from a PR-style diff:

```bash
feature-progress run --feature "billing export" --git-base origin/main
```

Slack-friendly format:

```bash
feature-progress run --format slack --git-base origin/main
```

### Spec alignment (`spec-align`)

Check whether implementation changes align with specs:

```bash
spec-align run --git-base origin/main
```

## Notes

- These tools are intentionally strict about output formats (they will request rewrites if off-contract).
- For `spec-align`, missing/insufficient specs will result in `Alignment: PARTIAL` with concrete follow-ups.
