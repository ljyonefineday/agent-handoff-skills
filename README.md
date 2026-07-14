# Agent Handoff Skills

Three Claude Code skills for transferring **in-progress coding work** between agents,
sessions, or context windows without losing repository truth, decisions, or momentum.

A handoff here is not a conversation summary — it is an **executable continuation artifact**.
The receiving agent can resume from one precise next command instead of reconstructing the
prior conversation.

## The three skills

| Skill | Invoke | Use when |
|---|---|---|
| `handoff-init` | `/handoff-init` | A repo will be continued across agents/sessions and has no `.handoff/` protocol yet, or its setup is stale/damaged. Run **once** per repo. |
| `handoff-create` | `/handoff-create` | Work is incomplete and must transfer — context is nearly exhausted, compaction or session end is near, work is pausing, or the user asks for a handoff. |
| `handoff-resume` | `/handoff-resume` | Picking up work from a `HANDOFF.md`, checkpoint branch, patch, or partially-changed repo left by a previous agent or session. |

## Lifecycle

```
  ┌──────────────┐      once per repo
  │ handoff-init │  ── sets up .handoff/ (config + template + history)
  └──────┬───────┘
         │
         ▼            work pauses / context runs low
  ┌────────────────┐
  │ handoff-create │ ── writes an executable HANDOFF.md (Status: ready)
  └──────┬─────────┘
         │
         ▼            a new agent / session picks up
  ┌────────────────┐
  │ handoff-resume │ ── verifies HANDOFF.md against the live repo,
  └──────┬─────────┘     records intake (Status: accepted), continues
         │
         └──▶ when work pauses again, run handoff-create for the next leg
```

`handoff-create` auto-runs `handoff-init` first if the protocol is missing, so in practice you
can start with either `/handoff-create` or `/handoff-resume`.

## Repository layout it manages

```
.handoff/
├── config.yaml     # protocol settings (see below)
├── template.md     # required headings for every HANDOFF.md
└── history/        # append-only archive of superseded handoffs
HANDOFF.md          # the current active handoff (created by handoff-create)
```

`config.yaml` is intentionally small:

```yaml
version: 1
active_file: HANDOFF.md
history_directory: .handoff/history
validation_commands: []          # only commands with real repo evidence; validation, not deploy
checkpoint_policy: preserve-worktree
```

Whether `.handoff/` and `HANDOFF.md` are committed is your call — the skills never edit
`.gitignore` or commit on your behalf.

## What a handoff carries

Repository truth (branch, HEAD, staged/unstaged/untracked changes), what changed and **why**,
verified facts kept separate from unverified hypotheses, honest validation results
(`PASS` / `FAIL` / `NOT RUN` only — never a fabricated pass), session-only knowledge the repo
can't show (user instructions, rejected approaches, required env/services), and exactly **one**
concrete next action with its first command and completion condition.

## Safety guarantees

- **Worktree is preserved.** `checkpoint_policy: preserve-worktree` — no reset, clean, stash,
  branch switch, or discard of inherited changes to make a handoff look tidy. A checkpoint commit
  happens only with explicit authorization.
- **Strict mutation budget.** `handoff-create` changes only the handoff artifacts; it leaves
  implementation and untracked files in place.
- **History is never overwritten.** Superseded handoffs are archived (append-only) with a unique
  suffix on collision.
- **No blind trust on resume.** `handoff-resume` treats the repo and fresh command results as
  ground truth, re-runs validation rather than trusting an old `PASS`, and reports discrepancies
  and unknowns explicitly.
- **Secrets stay out.** Only secret *paths* and required owner actions are recorded — never values.

## Installing

These are standard Claude Code skills — each lives in `skills/<name>/SKILL.md`. Make them
available by placing them where your Claude Code loads skills (for example, copy or symlink the
`skills/handoff-*` directories into `~/.claude/skills/`), then invoke with `/handoff-init`,
`/handoff-create`, or `/handoff-resume`.

## License

[MIT](LICENSE).
