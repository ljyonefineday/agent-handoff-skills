---
name: resuming-agent-handoffs
description: Use when continuing coding work from another agent or session, inheriting a handoff document, checkpoint branch, patch, or repository containing partially completed changes
---

# Resuming Agent Handoffs

## Overview

Resume from a handoff without blindly trusting it. The core principle is: **the handoff is a map; the repository and current execution results are ground truth.**

Typical invocation: `/handoff-in`.

## Safety Rule

Inspect before modifying. Do not reset, clean, stash, switch branches, overwrite files, or discard inherited changes merely to match `HANDOFF.md`.

## Required Workflow

1. Read applicable project instructions, `.handoff/config.yaml`, `.handoff/template.md`, and `HANDOFF.md`.
2. Capture the actual repository state before editing:

```bash
git status --short
git branch --show-current
git log -5 --oneline
git diff --stat
git diff --cached --stat
```

3. Compare the active branch, HEAD, changed files, and stated implementation with the handoff.
4. Classify each material claim as:
   - **Confirmed** — supported by code, Git state, or a current command result.
   - **Discrepancy** — conflicts with the current repository.
   - **Unknown** — not yet verified.
5. Inspect the files named in `Implemented Changes` and `Next Recommended Action` before changing them.
6. Re-run the smallest relevant validation. Use configured commands where applicable, but do not convert an old `PASS` into a current fact without execution.
7. Produce the intake report below. After the report, continue with the recorded next action unless the user requested inspection only or a discrepancy makes that action unsafe.
8. Once the handoff is understood and minimum verification is complete, update its status from `ready` to `accepted`. Preserve the original content and append intake findings rather than rewriting history.

## Required Intake Report

```markdown
## Handoff Intake

### Understood Objective
[One concise objective and completion criteria]

### Verified Repository State
[Branch, HEAD, changed files, preserved work]

### Confirmed
[Claims verified against repository or execution]

### Discrepancies
[Conflicts; write `None found` only after checking]

### Unknown
[Important claims not yet verified]

### Current Validation
[Exact commands and fresh results]

### First Implementation Step
[Action, target files, command, and completion condition]
```

## Conflict Policy

| Situation | Required response |
|---|---|
| Branch or HEAD differs | Report it; do not switch automatically. |
| Extra uncommitted changes exist | Preserve and identify them before editing. |
| Claimed implementation is absent | Mark discrepancy and inspect history; do not pretend it exists. |
| Old PASS now fails | Treat the current failure as truth and record both results. |
| Next action is unsafe or obsolete | Replace it with the smallest verified action and explain why. |
| Handoff lacks required sections | Reconstruct only from repository evidence; mark gaps unknown. |

## Continuation Rules

- Prefer extending verified working code over rewriting it for stylistic reasons.
- Preserve constraints and invariants until code or tests prove they are obsolete.
- Convert hypotheses into facts only through inspection or reproducible validation.
- Update `HANDOFF.md` with material new findings so another handoff remains possible.
- Before claiming completion, run the relevant test, lint, typecheck, or build commands and record actual results.

## Completion Gate

Intake is complete only when:

- Inherited changes are protected.
- Repository state and handoff claims have been compared.
- At least one relevant current validation has been attempted or a concrete blocker recorded.
- Discrepancies and unknowns are explicit.
- The first implementation step is safe, specific, and testable.

## Red Flags

- Starting implementation before checking `git status`.
- Assuming the prior agent's explanation is authoritative.
- Re-running no validation because the handoff says tests passed.
- Removing unexplained changes to obtain a clean worktree.
- Reimplementing existing work without first understanding it.
