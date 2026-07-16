---
name: handoff-init
description: Use when a repository needs handoff setup before work can transfer safely across sessions or collaborators.
---

# Handoff Init

Install protocol v2 once and keep valid setup unchanged. Project policy belongs here; live work belongs in the active handoff.

## Safety

Work from the repository root and read applicable project instructions first. Both configured paths must be repository-relative, not absolute, contain no `..`, and resolve within the repository root. Stop before following an unsafe path.

`checkpoint_policy: preserve-worktree` forbids reset, clean, stash, branch switch, or discard. Do not commit, edit `.gitignore`, expose secret values, or create `HANDOFF.md`. Record secret names or paths only when material.

## Normal Workflow

1. Inspect `.handoff/config.yaml`, `.handoff/template.md`, `.handoff/history/`, and any active file without modifying them.
2. If no setup exists, do not discover or add validation commands. New and repaired setup must write `validation_commands: []` unchanged. Never run or install an unknown command.
3. Create `.handoff/history/` and write the exact contracts below. Do not approximate headings or add runtime scripts.
4. If setup is already safe v2, verify it and make no cosmetic rewrite. Preserve a user-authored nonempty validation list only when every entry has traceable repository evidence and is non-destructive; otherwise treat setup as damaged.
5. Read [recovery guidance](references/recovery.md) only when setup is partial, damaged, non-v2, or either configured path is observably unsafe.
6. Re-read both files, verify the directory exists, and report created, preserved, changed, and unresolved items. State whether the files are Git-ignored; their tracking is the user's choice.

## Configuration Contract

```yaml
version: 2
active_file: HANDOFF.md
history_directory: .handoff/history
validation_commands: []
checkpoint_policy: preserve-worktree
```

Initialization itself always writes the empty list shown above. A repository owner may later add command strings run from the repository root; each requires traceable evidence that it validates rather than deploys or mutates.

## Template Contract

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

`Metadata` carries a unique ID, ISO 8601 timestamp, sender or session, branch, HEAD, and status. Creation sets `ready`; verified intake changes it to `accepted`. A later creation archives the superseded artifact. `## Intake` is the only sanctioned trailing section and is appended by resume, never added to the template.

Confirmed-empty content uses `None material`; unavailable evidence uses `Unknown — reason`.
