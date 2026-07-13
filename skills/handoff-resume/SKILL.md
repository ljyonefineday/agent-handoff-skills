---
name: handoff-resume
description: Use when continuing coding work from another agent or session from a HANDOFF.md, checkpoint branch, patch, or partially changed repository, including explicit requests to pick up previous work (e.g. /handoff-resume)
---

# Handoff Resume

## Overview

Resume from a handoff without blindly trusting it. The core principle is: **the handoff is a map; the repository and current execution results are ground truth.**

Typical explicit invocation: `/handoff-resume`.

## Safety Rule

Inspect before modifying. Do not reset, clean, stash, switch branches, overwrite files, or discard inherited changes merely to match `HANDOFF.md`.

## Required Workflow

1. Read applicable project instructions, `.handoff/config.yaml`, `.handoff/template.md`, and the configured active handoff when it exists. Use `HANDOFF.md` only as the default when configuration is absent.
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
7. Produce the intake report below. Continue only after the Completion Gate passes and unless the user requested inspection only or a discrepancy makes the next action unsafe.
8. Apply the Acceptance Semantics below. Preserve the original handoff content rather than rewriting its history.

## Acceptance Semantics

`Status: accepted` means the receiver completed intake and recorded current evidence; it does not endorse every handoff claim, resolve discrepancies, or mark implementation complete.

If the active handoff exists, is writable, has `Status: ready`, and the task permits edits, change that status to `accepted` and append the intake report under `## Intake`. If its status differs, preserve it and record the mismatch instead of forcing a transition.

If no active handoff exists, return the intake report from repository evidence and do not create an artifact merely to mark it accepted. For inspection-only work or a read-only artifact, report intake without modifying files.

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
| No handoff artifact exists at all | Say so; reconstruct objective and state from Git history and the worktree, and mark everything else unknown. |

## Continuation Rules

- Prefer extending verified working code over rewriting it for stylistic reasons.
- Preserve constraints and invariants until code or tests prove they are obsolete.
- Convert hypotheses into facts only through inspection or reproducible validation.
- Update the configured active handoff with material new findings when the task permits edits so another handoff remains possible.
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
- Marking a handoff accepted before classifying discrepancies and attempting current validation.
