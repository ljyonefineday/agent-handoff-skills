---
name: creating-agent-handoffs
description: Use when transferring incomplete coding work to another agent or session, approaching context limits, pausing before completion, or preserving an executable continuation point
---

# Creating Agent Handoffs

## Overview

Create an executable continuation artifact, not a conversation summary. The core principle is: **transfer repository truth, verification evidence, decisions, and one precise next action.**

Typical invocation: `/handoff-out`.

## Preflight

If `.handoff/config.yaml` or `.handoff/template.md` is missing, use `initializing-agent-handoffs` first, then continue. Do not block an urgent handoff merely because initialization was forgotten.

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
5. Run the smallest relevant validations plus configured commands that are reasonable for the current state. Record the exact command, result, and meaningful failure detail.
6. Preserve the worktree. Never use `reset`, `clean`, destructive checkout, or unrequested stash. Create a checkpoint commit only when explicitly authorized.
7. If an active `HANDOFF.md` exists, copy it to the configured history directory before replacing it. Never delete history.
8. Write `HANDOFF.md` using `.handoff/template.md`, set status to `ready`, and include a unique handoff ID and timestamp.
9. Re-read the artifact against the actual repository state before declaring it ready.

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

The final action must be singular and executable:

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
- Constraints and rejected alternatives are recorded when they affect continuation.
- The receiver can begin with one exact command without reconstructing the conversation.

## Red Flags

- “Almost done,” “continue working,” or other non-testable status.
- Treating a suspected cause as confirmed.
- Listing files without explaining what changed and why.
- Hiding failed or unrun validations.
- Altering implementation merely to make the handoff look cleaner.
