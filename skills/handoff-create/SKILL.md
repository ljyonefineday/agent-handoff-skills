---
name: handoff-create
description: Use when incomplete coding work must transfer to another agent or session because context is nearly exhausted, compaction or session end is approaching, work is pausing, or the user explicitly requests a handoff (e.g. /handoff-create)
---

# Handoff Create

## Overview

Create an executable continuation artifact, not a conversation summary. The core principle is: **transfer repository truth, verification evidence, decisions, and one precise next action.**

Typical explicit invocation: `/handoff-create`.

## Preflight

If `.handoff/config.yaml` or `.handoff/template.md` is missing, run `handoff-init` first, then continue. If context is too limited to initialize, use `handoff-init`'s exact default active path, history path, and Template Contract; do not invent fallback paths or headings.

Read project instructions and inspect:

```bash
git status --short
git branch --show-current
git log -5 --oneline
git diff --stat
git diff --cached --stat
```

If the directory is not a Git repository, record that fact and continue with available filesystem evidence.

## Required Workflow

1. Determine the objective and measurable completion criteria from the user request, code, and current session.
2. Inspect changed and relevant files. Describe behavior and impact, not only filenames.
3. Separate status into completed, partially completed, and not started.
4. Separate verified facts, observations, and unverified hypotheses.
5. Record session-only knowledge the repository cannot show: user instructions and preferences stated in conversation, rejected approaches and why, and environment specifics such as running services or required environment variables (reference secret names, never values).
6. Run the smallest relevant validations plus configured commands that are safe and reasonable for the current state. Record the exact command, result, and meaningful failure detail.
7. Stay within the Mutation Budget below. Preserve the worktree and create a checkpoint only when the user or repository policy explicitly authorizes that specific operation.
8. If an active handoff exists, copy it to the configured history directory using its ID or timestamp before replacement. If that destination exists, add a unique suffix; never overwrite history.
9. Write the active file at the configured path using `.handoff/template.md`. Fill `Metadata` per `handoff-init`, with `Status: ready`.
10. Re-read the artifact against the actual repository state before declaring it ready.

## Mutation Budget

Handoff creation may change only the handoff artifacts by default:

- Archive the existing active handoff in the configured history directory.
- Write the new active handoff at the configured path.

Leave implementation files and untracked files in place. Do not switch or create branches, alter the index, move or quarantine files, commit, tag, stash, reset, or clean unless that exact operation is explicitly authorized. If a file may contain a secret, record only its path, the risk, and the required owner action; never copy its value into the handoff or history.

## Required Repository State

Record at minimum:

- Repository root and current branch
- HEAD commit and base/reference commit when known
- Staged, unstaged, and untracked changes
- Relevant paths
- Whether a checkpoint commit exists
- Any branch or commit mismatch that the receiver must know

Do not paste a full diff into `HANDOFF.md`. Summarize it and preserve the real worktree; include a patch path only when one was actually created.

## Validation Result Format

```markdown
| Command | Result | Evidence |
|---|---|---|
| `pnpm test auth` | PASS | 18 tests passed |
| `pnpm lint` | FAIL | Existing error in `src/x.ts:42` |
| Integration tests | NOT RUN | Required service unavailable |
```

Only `PASS`, `FAIL`, or `NOT RUN` are allowed. Never imply success for an unexecuted command.

## Next Action Contract

The final action must be singular and executable: one action, not a checklist or multi-step plan.

```markdown
## Next Recommended Action

- Action: Fix refresh-token reuse returning HTTP 500.
- Target files: `src/auth/refresh.ts`, `tests/auth/refresh.test.ts`
- First command: `pnpm test tests/auth/refresh.test.ts`
- Expected current result: Reuse case fails with HTTP 500.
- Completion condition: Reuse case returns HTTP 401 and related tests pass.
```

## Completion Gate

A handoff is ready only when:

- Every claimed change exists in the repository.
- All validation claims match actual command results.
- Uncommitted work is preserved and clearly described.
- Constraints, user-stated instructions, and rejected alternatives are recorded when they affect continuation.
- The receiver can begin with one exact command without reconstructing the conversation.

## Context-Pressure Rationalizations

Most bad handoffs are written in the last 5% of context. These excuses mean STOP:

| Excuse | Reality |
|---|---|
| "No context left to run validations" | Record `NOT RUN` honestly. A fabricated PASS costs the receiver hours. |
| "The receiver can read the diff" | The diff shows what changed, not why. Decisions die with the session. |
| "A conversation summary is enough" | Summaries transfer narrative; handoffs transfer executable state. |
| "Tests passed earlier" | Earlier ≠ current worktree. Re-run, or record `NOT RUN` noting the stale result. |
| "I'll skip sections to save tokens" | A short honest handoff beats a complete-looking fabricated one. Write `UNKNOWN` in gaps. |

## Red Flags

- “Almost done,” “continue working,” or other non-testable status.
- Treating a suspected cause as confirmed.
- Listing files without explaining what changed and why.
- Hiding failed or unrun validations.
- Altering implementation merely to make the handoff look cleaner.
- Inventing an archive path, moving an untracked file, or creating a branch or commit outside the Mutation Budget.
