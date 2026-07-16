---
name: handoff-create
description: Use when incomplete coding work must transfer to another session or collaborator without losing continuation-critical context.
---

# Handoff Create

Create a compact, executable continuation artifact from repository truth and current evidence.

## Safety and Preflight

Read project instructions and the v2 config/template. Both configured paths must be repository-relative, not absolute, contain no `..`, and resolve within the repository root. Stop on an unsafe path. Do not interpret v1 or any non-v2 artifact.

When setup is missing or non-v2, use the emergency reference: read [emergency guidance](references/emergency.md) only when setup is missing, incompatible, or an archive destination already exists.

`checkpoint_policy: preserve-worktree` forbids reset, clean, stash, branch switch, or discard. By default mutate only handoff artifacts: archive the old active artifact and write the new one. Never alter implementation, the index, branches, commits, tags, or untracked files.

Capture live state first:

```bash
git status --short
git branch --show-current
git log -5 --oneline
git diff --stat
git diff --cached --stat
```

If Git is unavailable, record that and use filesystem evidence.

## Workflow

1. Derive the objective and completion boundary from the request, code, and current session. Inspect every changed or next-action path; summarize behavior and impact, not a full diff.
2. Classify work as completed, in progress, or remaining. Record staged, unstaged, and untracked paths; branch, HEAD, base when known, and checkpoint status.
3. Preserve only material continuation context: decisions, constraints, rejected approaches and reasons, environment and services, and secret names or paths, never values. Never copy secret values into active or archived artifacts.
4. Run the smallest relevant safe validations plus supported configured commands. A stale or earlier `PASS` is not fresh; re-run it or record `NOT RUN`.
5. Before archival, if the active artifact is known or suspected to contain a secret value, stop. Keep it and all work unchanged; ask the owner to sanitize it and rotate any exposed secret. Otherwise archive it before replacement and never overwrite history.
6. Write the configured active file with a unique ID, ISO 8601 timestamp, sender/session, branch, HEAD, and `Status: ready`. Re-read every claim against the repository.

Aim for 450 words on simple handoffs and 900 words on complex handoffs. These are soft targets, not a hard cap: never omit critical material to meet them. Use `None material` only after confirming a category is empty; use `Unknown — reason` when evidence is unavailable.

## Exact Output Contract

```markdown
# Agent Handoff

## Metadata
## Objective
## Work State
### Completed
### In Progress
### Remaining
## Repository State
## Continuation Context
## Validation and Risks
## Next Action
```

`Validation and Risks` must separate fresh evidence from confirmed issues and unverified hypotheses. For each attempted or unavailable check, record the command/scope, exactly one result from `PASS`, `FAIL`, or `NOT RUN`, and concise evidence. Keep hypotheses unverified until evidence confirms them.

`Next Action` contains exactly one action, not a checklist, in this order:

```markdown
- Action: ...
- Target paths: ...
- First command: ...
- Expected current result: ...
- Completion condition: ...
```

The expected result describes the current evidence, not the hoped-for fix. The completion condition must be observable.
