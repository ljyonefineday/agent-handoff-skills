---
name: handoff-resume
description: Use when continuing work from a handoff or inherited repository state that must be verified before editing.
---

# Handoff Resume

Treat the handoff as a map; the repository and fresh execution evidence are ground truth.

## Safety and Intake

Read project instructions, v2 config/template, and the configured active artifact. Both configured paths must be repository-relative, not absolute, contain no `..`, and resolve within the repository root. Stop before following an unsafe path. Do not interpret v1 or any non-v2 artifact.

When an artifact is missing or non-v2, use the conflict reference: read [conflict guidance](references/conflicts.md) only when branch, HEAD, worktree status, lifecycle status, or artifact presence conflicts with the handoff.

`checkpoint_policy: preserve-worktree` forbids reset, clean, stash, branch switch, or discard. Preserve inherited changes and secret-bearing files. Never copy secret values; record only material secret names or paths.

Before editing, capture:

```bash
git status --short
git branch --show-current
git log -5 --oneline
git diff --stat
git diff --cached --stat
```

If Git is unavailable, record that and use filesystem evidence.

## Workflow

1. Compare live branch, HEAD, staged/unstaged/untracked changes, relevant files, objective, and work claims with the artifact. Inspect every path named by current work or its Next Action.
2. Classify material claims as confirmed, discrepant, or unknown. Use `None material` only after checking; use `Unknown — reason` when evidence is unavailable. Keep hypotheses unknown until evidence verifies them.
3. Attempt exactly one fresh gating validation: choose the smallest safe command that determines whether continuation may begin. Record its exact scope, command, evidence, and one result from `PASS`, `FAIL`, or `NOT RUN`. A stale `PASS` is never current; re-run it or report the present blocker.
4. Decide whether to retain or replace the artifact's Next Action. A replacement is required when it is unsafe, obsolete, or conflicts with live evidence, and must satisfy the original exactly-one-action contract.
5. Transition `ready → accepted` only after verification: inherited work is protected, comparison is complete, exactly one gating result is recorded, discrepancies are explicit, and the retained or replacement action is safe. Acceptance records intake; it does not endorse every claim.
6. When the active artifact is writable and status is `ready`, change only that status and append the delta below. Otherwise do not force a transition. Continue from the selected action unless the request is inspection-only or a discrepancy makes continuation unsafe.

## Intake Delta

Append exactly one `## Intake`; preserve all earlier content. Target 200 words. This is a soft target, not a hard cap: never omit material discrepancies or safety evidence. Write a delta only; do not duplicate confirmed handoff content.

```markdown
## Intake
- Receiver: ...
- Timestamp: ...
- Verified state: ...
- Gating validation: `command` — PASS|FAIL|NOT RUN — evidence
- Discrepancies: ...
- Next Action: Retained — ... | Replacement — ... and reason
```

Include current branch, HEAD, and changed paths in verified state. Discrepancies distinguish confirmed conflicts from unknowns. The retained or replacement Next Action remains singular, with target paths, first command, expected current result, and completion condition available in the artifact or delta.
