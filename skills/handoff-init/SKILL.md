---
name: handoff-init
description: Use when a coding repository lacks a reliable handoff format, storage location, validation policy, or continuation protocol, especially before its first handoff or when .handoff/ setup is missing, stale, or damaged (e.g. /handoff-init)
---

# Handoff Init

## Overview

Initialize a repository-level handoff protocol once, then keep it safe to re-run. The core principle is: **persistent project policy belongs in initialization; live work state belongs in the handoff artifact.**

Typical explicit invocation: `/handoff-init`.

## When to Use

- The repository will be continued across agents, sessions, or context windows.
- No `.handoff/config.yaml` exists.
- Existing handoff setup is incomplete, stale, or damaged.

Do not use this to transfer current work. Use `handoff-create` for that.

## Required Workflow

1. Locate the repository root and read applicable project instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, manifests, task runners, and CI configuration.
2. Inspect any existing `.handoff/` files. Preserve user-authored values and history.
3. Discover validation commands from repository evidence. Do not add an uncertain or potentially destructive command. Preserve an existing unverified command unless it is proven unsafe, do not execute it, and report it as unresolved.
4. Create or reconcile this structure. When a contract file is missing, write the exact contract below rather than approximating it:

```text
.handoff/
├── config.yaml
├── template.md
└── history/
```

Do **not** create an active `HANDOFF.md`; only `handoff-create` creates one.

5. Verify all paths and commands, note whether `.handoff/` is Git-ignored, then report created, preserved, changed, and unresolved items. Whether handoff files are committed is the user's decision; do not edit `.gitignore`.

## Configuration Contract

Create `.handoff/config.yaml` with this minimal shape:

```yaml
version: 1
active_file: HANDOFF.md
history_directory: .handoff/history
validation_commands: []
checkpoint_policy: preserve-worktree
require_next_action: true
require_fact_hypothesis_separation: true
```

Each `validation_commands` entry is a shell command string run from the repository root. Add a command only when repository files support it and its expected effect is validation rather than deployment or mutation. For an existing unverified entry, preserve the value, skip execution, and report the uncertainty; remove it only when repository evidence proves it invalid or unsafe. `checkpoint_policy: preserve-worktree` means handoff commands must not reset, clean, or discard inherited changes. A checkpoint commit may be created only when explicitly authorized by the user or repository policy.

## Template Contract

Create `.handoff/template.md` with these required headings, in this order. If the file is missing or lacks required headings, preserve any compatible user-authored content and write the exact contract below. Never invent substitute headings or a smaller fallback template.

```markdown
# Agent Handoff

## Metadata
## Objective
## Completion Criteria
## Current Status
### Completed
### Partially Completed
### Not Started
## Repository State
## Implemented Changes
## Decisions and Rationale
## Constraints and Invariants
## Validation Results
## Known Issues
## Unverified Hypotheses
## Next Recommended Action
```

`Metadata` must include: a unique handoff ID, ISO 8601 timestamp, author agent or session, branch, HEAD commit, and `Status`. Status lifecycle: `ready` (set by `handoff-create`) → `accepted` (set by `handoff-resume` after intake); replaced handoffs move to the configured history directory.

`Next Recommended Action` must contain one concrete action, target files, first command, expected current result, and completion condition.

## Idempotency Rules

| Existing state | Required behavior |
|---|---|
| No setup | Create the contract files and history directory. |
| Valid setup | Verify it; make no cosmetic rewrite. |
| Missing fields | Add only missing required fields. |
| User-customized values | Preserve them unless invalid or unsafe. |
| Existing unknown validation command | Preserve it, do not execute it, and report it as unverified. |
| Existing `HANDOFF.md` | Preserve it untouched. |

## Completion Gate

Initialization is complete only when:

- Configuration and template agree on paths and required sections.
- New validation commands have traceable repository evidence; existing unverified commands are preserved, skipped, and reported.
- Re-running initialization would not erase user changes or history.
- No active handoff was fabricated.

## Red Flags

- Overwriting `.handoff/` because regeneration is easier.
- Inventing alternative template headings instead of repairing the defined contract.
- Creating a blank `HANDOFF.md` that looks active.
- Guessing `test`, `lint`, `build`, or `typecheck` commands.
- Adding automatic commits, resets, stashes, or cleans without authorization.
- Silently adding `.handoff/` to `.gitignore` or committing it unasked.
