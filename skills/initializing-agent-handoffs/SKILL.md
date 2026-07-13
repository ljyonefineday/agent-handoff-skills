---
name: initializing-agent-handoffs
description: Use when a coding repository has no established handoff format, storage location, validation policy, or continuation protocol for work transferred between agents or sessions — typically before the first handoff, or when .handoff/ setup is missing, stale, or damaged (e.g. /handoff-init)
---

# Initializing Agent Handoffs

## Overview

Initialize a repository-level handoff protocol once, then keep it safe to re-run. The core principle is: **persistent project policy belongs in initialization; live work state belongs in the handoff artifact.**

Typical invocation: `/handoff-init`.

## When to Use

- The repository will be continued across agents, sessions, or context windows.
- No `.handoff/config.yaml` exists.
- Existing handoff setup is incomplete, stale, or damaged.

Do not use this to transfer current work. Use `creating-agent-handoffs` for that.

## Required Workflow

1. Locate the repository root and read applicable project instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, manifests, task runners, and CI configuration.
2. Inspect any existing `.handoff/` files. Preserve user-authored values and history.
3. Discover validation commands from repository evidence. Never invent commands. Record uncertain commands as unverified.
4. Create or reconcile this structure:

```text
.handoff/
├── config.yaml
├── template.md
└── history/
```

Do **not** create an active `HANDOFF.md`; only `creating-agent-handoffs` creates one.

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

Populate `validation_commands` only with commands supported by repository files or successfully executed discovery. `checkpoint_policy: preserve-worktree` means handoff commands must not reset, clean, or discard inherited changes. A checkpoint commit may be created only when explicitly authorized by the user or repository policy.

## Template Contract

Create `.handoff/template.md` with these required headings, in this order:

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

`Metadata` must include: a unique handoff ID, ISO 8601 timestamp, author agent or session, branch, HEAD commit, and `Status`. Status lifecycle: `ready` (set by the creator) → `accepted` (set by the receiver after verification); replaced handoffs move to the history directory.

`Next Recommended Action` must contain one concrete action, target files, first command, expected current result, and completion condition.

## Idempotency Rules

| Existing state | Required behavior |
|---|---|
| No setup | Create the contract files and history directory. |
| Valid setup | Verify it; make no cosmetic rewrite. |
| Missing fields | Add only missing required fields. |
| User-customized values | Preserve them unless invalid or unsafe. |
| Unknown validation command | Mark unverified; do not guess. |
| Existing `HANDOFF.md` | Preserve it untouched. |

## Completion Gate

Initialization is complete only when:

- Configuration and template agree on paths and required sections.
- Validation commands have traceable repository evidence.
- Re-running initialization would not erase user changes or history.
- No active handoff was fabricated.

## Red Flags

- Overwriting `.handoff/` because regeneration is easier.
- Creating a blank `HANDOFF.md` that looks active.
- Guessing `test`, `lint`, `build`, or `typecheck` commands.
- Adding automatic commits, resets, stashes, or cleans without authorization.
- Silently adding `.handoff/` to `.gitignore` or committing it unasked.
