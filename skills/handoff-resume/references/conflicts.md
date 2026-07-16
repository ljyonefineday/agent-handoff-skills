# Handoff Resume Conflicts

Load this reference only after observing a branch, HEAD, worktree-status, lifecycle-status, version, or artifact-presence conflict.

## Branch, HEAD, or changed-file drift

Report claimed and live values side by side. Do not switch branches, reset to the claimed commit, clean, stash, discard, or overwrite extra changes. Inspect relevant history and files, then mark each mismatch as a discrepancy. Live state and fresh results win.

If claimed implementation is absent, inspect history before concluding it was lost. If extra work exists, identify and preserve it before continuing. If an old validation now fails, record the stale claim and current failure separately. Replace an obsolete or unsafe action with the smallest action supported by current evidence.

## Lifecycle conflict

Only `Status: ready` may become `accepted`, and only after the core intake gate. For any other value, read-only artifact, duplicate intake, or malformed status, preserve it and report the mismatch. Never rewrite history to manufacture a valid transition.

## No usable artifact

For a missing active artifact, reconstruct only what repository evidence proves and return an intake report to the user; do not create an artifact merely to accept it. Mark unavailable objective, decisions, constraints, and validation as unknown with reasons.

For a non-v2 artifact, do not interpret or accept it. Report that initialization must preserve and migrate the old setup before resume can use it. Never follow an active/history path outside the repository root.

Continue only when inherited work is protected, the discrepancy is understood well enough to choose a safe singular action, and a fresh gating validation or explicit `NOT RUN` blocker is recorded.
