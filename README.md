# Agent Handoff Skills

Three portable Agent Skills for transferring unfinished coding work across collaborators, sessions, or context windows without losing repository truth or continuation-critical context. They follow the open Agent Skills layout and contain only Markdown runtime instructions.

A handoff is an executable continuation artifact, not a conversation transcript. The receiver gets verified work state, material decisions and constraints, honest validation evidence, and exactly one next action.

Choose the route that fits how you want to work:

- **Section 1** is for people who want to understand, install, and operate the skills themselves.
- **Section 2** provides one prompt you can paste into an agent on another machine so it can install the skills for its own runtime.

## 1. For humans: introduction and instructions

Use this section when you want to choose the installation method and manage the skills yourself.

### Skills

| Skill | Use when |
|---|---|
| `handoff-init` | A repository needs the v2 config, template, and history directory, or old/partial setup must be preserved and replaced. |
| `handoff-create` | Incomplete work must transfer before a pause, session change, compaction, or context exhaustion. |
| `handoff-resume` | A new session must verify an active handoff against the live repository and continue safely. |

### Install the skills yourself

The recommended managed path uses the open `skills` CLI. From any directory, install the repository and choose global scope plus the agents that should receive the skills:

```bash
npx skills add ljyonefineday/agent-handoff-skills
```

For a non-interactive global install to Claude Code and Codex:

```bash
npx skills add ljyonefineday/agent-handoff-skills --global --agent claude-code --agent codex --yes
```

The CLI can also install project-local copies when `--global` is omitted. See the [skills CLI](https://github.com/vercel-labs/skills) for current flags.

#### Manual installation without Node

Clone the repository and keep that clone in place; the commands below create symlinks, so updates need only a Git pull.

```bash
git clone https://github.com/ljyonefineday/agent-handoff-skills.git
cd agent-handoff-skills
mkdir -p ~/.claude/skills ~/.agents/skills

ln -s "$PWD/skills/handoff-init" ~/.claude/skills/handoff-init
ln -s "$PWD/skills/handoff-create" ~/.claude/skills/handoff-create
ln -s "$PWD/skills/handoff-resume" ~/.claude/skills/handoff-resume

ln -s "$PWD/skills/handoff-init" ~/.agents/skills/handoff-init
ln -s "$PWD/skills/handoff-create" ~/.agents/skills/handoff-create
ln -s "$PWD/skills/handoff-resume" ~/.agents/skills/handoff-resume
```

Claude Code loads personal skills from `~/.claude/skills`. Codex loads personal skills from `~/.agents/skills`; repository-local Codex installation may instead use `.agents/skills`. Codex detects most skill changes automatically, but restart it if an installed skill does not appear.

### Invocation

Descriptions are trigger-focused, so natural language works in either agent:

- “Initialize the v2 handoff protocol for this repository.”
- “Create a handoff for the unfinished work in this checkout.”
- “Resume from the active handoff, verify it, and continue the safe next action.”

Claude Code slash examples:

```text
/handoff-init
/handoff-create
/handoff-resume
```

Codex explicit skill mentions:

```text
$handoff-init
$handoff-create
$handoff-resume
```

### Update and removal

For managed installations:

```bash
npx skills update handoff-init handoff-create handoff-resume --global
npx skills remove handoff-init handoff-create handoff-resume --global
```

For the manual symlink installation, update with `git pull --ff-only` inside the clone. Remove only the installed symlinks with:

```bash
unlink ~/.claude/skills/handoff-init
unlink ~/.claude/skills/handoff-create
unlink ~/.claude/skills/handoff-resume
unlink ~/.agents/skills/handoff-init
unlink ~/.agents/skills/handoff-create
unlink ~/.agents/skills/handoff-resume
```

### Protocol v2 lifecycle

1. **Initialize.** `handoff-init` writes:

   ```yaml
   version: 2
   active_file: HANDOFF.md
   history_directory: .handoff/history
   validation_commands: []
   checkpoint_policy: preserve-worktree
   ```

   It also writes the exact v2 template and creates `.handoff/history/`, but never fabricates an active handoff. A valid v2 setup is left unchanged. Partial, damaged, or non-v2 setup is incompatible: initialization archives detected old artifacts under a unique `.handoff/history/protocol-backup-*` directory before installing v2. If archival fails, existing content remains unchanged.

   New and repaired setup always starts with `validation_commands: []`. If any legacy artifact is known or suspected to contain a secret value, initialization stops before archival and leaves setup unchanged until the owner sanitizes the artifact and rotates any exposed secret.

2. **Create.** `handoff-create` inspects Git and relevant files, runs safe targeted validation, archives any superseded active artifact, and writes `HANDOFF.md` with `Status: ready`.

3. **Resume.** `handoff-resume` compares the artifact with live branch, HEAD, changes, and fresh execution evidence. It attempts exactly one fresh gating validation. Only then may it transition `ready → accepted` and append a compact `## Intake` delta.

4. **Continue or hand off again.** The receiver starts from the retained or replacement next action. If work pauses again, creation archives the accepted artifact and emits a new ready artifact.

`handoff-create` and `handoff-resume` do not interpret v1 artifacts. Run initialization to preserve and migrate incompatible setup first.

### Artifact shape

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

`Continuation Context` carries material decisions, constraints, rejected approaches, environment/services, and secret names or paths—never values. `Validation and Risks` distinguishes fresh `PASS`/`FAIL`/`NOT RUN` evidence, confirmed issues, and unverified hypotheses. `Next Action` has one action, target paths, first command, expected current result, and completion condition.

Use `None material` for a confirmed-empty category and `Unknown — reason` when evidence is unavailable.

### Adaptive size and economics

- Simple handoff soft target: **450 words**.
- Complex handoff soft target: **900 words**.
- Resume intake soft target: **200 words**.

These are soft targets, never caps that suppress critical context. A handoff is economical when the repository alone cannot recover decisions, user constraints, rejected approaches, dirty-work ownership, environment/service state, or mixed validation evidence.

Skip a handoff when work is complete or a tiny, reconstructible change has an obvious next step already captured in the repository or task tracker. In that case, the ceremony and intake cost are not worth more than the context they preserve.

### Safety boundaries

- `preserve-worktree` prohibits reset, clean, stash, branch switching, or discarding inherited changes.
- Creation changes only active/history handoff artifacts by default.
- History is append-only; collisions receive unique suffixes.
- Old validation never becomes a current pass without re-execution.
- Secret values never enter active or archived handoffs.
- The skills do not edit `.gitignore`, commit, push, or ship runtime scripts.

Whether a project commits `.handoff/` and `HANDOFF.md` remains the user's decision.

### Development

Repository tests and fresh-context evaluation fixtures are development assets; they are not installed with the runtime skills.

```bash
python3 -B -m unittest discover -s tests -v
```

### License

[MIT](LICENSE).

## 2. For agents: set up these skills for yourself

Paste the entire prompt below into the prompt line of an agent on the machine where you want the skills installed. The agent should install only for its own runtime; it should not configure this repository or run a handoff.

```text
Set up the Agent Handoff Skills from https://github.com/ljyonefineday/agent-handoff-skills for your own agent environment. This is an installation task only: do not change the current project.

First read that repository's README and the SKILL.md files for handoff-init, handoff-create, and handoff-resume. Detect which agent and runtime you are using, then install those three skills only into your own personal or global skills location. Prefer the README's recommended npx skills installation when npx is available, selecting only your current agent. Otherwise follow the documented no-Node manual method, adapting it to create links only for your current agent. If you need a clone, keep it outside the current project. If a skill is already installed, inspect it first and update it safely; do not overwrite user-modified content or remove anything without permission.

Do not run the installed handoff skills, initialize a handoff, edit project files, commit, or push as part of setup. Verify the installed files and, when possible, confirm that your runtime can discover all three skills. Report the installation method, resolved paths, verification result, and whether a restart is needed. Stop and ask before any overwrite, destructive action, or elevated permission.
```
