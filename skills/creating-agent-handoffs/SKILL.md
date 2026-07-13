---
name: creating-agent-handoffs
description: Use when transferring incomplete coding work to another agent or session — context nearly exhausted or about to be compacted, session ending, work pausing before completion, or the user asks to hand off current work (e.g. /handoff-out)
---

# Creating Agent Handoffs

## Overview

Create an executable continuation artifact, not a conversation summary. The core principle is: **transfer repository truth, verification evidence, decisions, and one precise next action.**

Typical invocation: `/handoff-out`.

## Preflight

If `.handoff/config.yaml` or `.handoff/template.md` is missing, run `initializing-agent-handoffs` first, then continue. If there is no time or context left to initialize, write the artifact anyway using the section list from that skill's Template Contract — never skip the handoff because setup is missing.

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
6. Run the smallest relevant validations plus configured commands that are reasonable for the current state. Record the exact command, result, and meaningful failure detail.
7. Preserve the worktree. Never use `reset`, `clean`, destructive checkout, or unrequested stash. Create a checkpoint commit only when explicitly authorized.
8. If an active `HANDOFF.md` exists, copy it to the configured history directory (named by its ID or timestamp) before replacing it. Never delete history.
9. Write the active file at the configured path using `.handoff/template.md`. Fill `Metadata` per the contract in `initializing-agent-handoffs`, with `Status: ready`.
10. Re-read the artifact against the actual repository state before declaring it ready.

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
