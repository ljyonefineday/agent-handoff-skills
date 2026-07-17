# Agent Handoff Skills

Three portable Agent Skills for transferring unfinished coding work across sessions, collaborators, or context windows without losing repository truth or continuation-critical context. A handoff is an executable continuation artifact, not a conversation transcript: the receiver gets verified work state, material decisions and constraints, honest validation evidence, and exactly one next action.

The runtime bundle is Markdown-only and harness-neutral. Any agent that follows the open Agent Skills layout — or can simply read a `SKILL.md` and run shell commands — can be the sender or the receiver; no step depends on a specific model or vendor. Section 1 covers installing and operating the skills, Section 2 the protocol, Section 3 a prompt an agent can run to install the skills for its own runtime, and Section 4 a Korean translation. (한국어 안내는 문서 끝에 있습니다.)

## 1. Install and use

| Skill | Use when |
|---|---|
| `handoff-init` | A repository needs the v2 config, template, and history directory, or old/partial setup must be preserved and replaced. |
| `handoff-create` | Incomplete work must transfer before a pause, session change, compaction, or context exhaustion. |
| `handoff-resume` | A new session must verify an active handoff against the live repository and continue safely. |

### Managed installation (recommended)

The [skills CLI](https://github.com/vercel-labs/skills) installs to 20+ agent harnesses (Claude Code, Codex, Cursor, Gemini CLI, opencode, and more). From any directory:

```bash
npx skills add ljyonefineday/agent-handoff-skills
```

Non-interactive global install to Claude Code and Codex:

```bash
npx skills add ljyonefineday/agent-handoff-skills --global --agent claude-code --agent codex --yes
```

Omit `--global` for a project-local install. Update and remove with:

```bash
npx skills update handoff-init handoff-create handoff-resume --global
npx skills remove handoff-init handoff-create handoff-resume --global
```

### Manual installation without Node

Clone the repository, keep the clone in place, and symlink each skill folder into your harness's skills directory — updating is then a `git pull --ff-only` inside the clone. Claude Code loads personal skills from `~/.claude/skills`; Codex loads from `~/.agents/skills` (repository-local Codex may use `.agents/skills`); other harnesses follow the same pattern with their own skills directory. Restart the harness if an installed skill is not discovered.

```bash
git clone https://github.com/ljyonefineday/agent-handoff-skills.git
cd agent-handoff-skills
mkdir -p ~/.claude/skills ~/.agents/skills
for s in handoff-init handoff-create handoff-resume; do
  ln -s "$PWD/skills/$s" ~/.claude/skills/$s
  ln -s "$PWD/skills/$s" ~/.agents/skills/$s
done
```

Remove by unlinking the same paths.

### Invocation

Descriptions are trigger-focused, so natural language works in any harness — "Create a handoff for the unfinished work in this checkout." Explicit forms: `/handoff-init`, `/handoff-create`, `/handoff-resume` in Claude Code; `$handoff-init`, `$handoff-create`, `$handoff-resume` in Codex.

## 2. Protocol v2

### Lifecycle

1. **Initialize.** `handoff-init` writes the exact config and template below and creates `.handoff/history/`. It never fabricates an active handoff and leaves a valid v2 setup unchanged. Partial, damaged, or non-v2 setup is archived under a unique `.handoff/history/protocol-backup-*` directory before v2 is installed; if a legacy artifact may contain a secret value, initialization stops before archival. New and repaired setup always starts with `validation_commands: []`.

   ```yaml
   version: 2
   active_file: HANDOFF.md
   history_directory: .handoff/history
   validation_commands: []
   checkpoint_policy: preserve-worktree
   ```

2. **Create.** `handoff-create` inspects Git and relevant files, runs safe targeted validation fresh, archives any superseded active artifact, and writes `HANDOFF.md` with `Status: ready`.

3. **Resume.** `handoff-resume` compares the artifact with the live branch, HEAD, and changes, attempts exactly one fresh gating validation, and only then transitions `ready → accepted` and appends a compact `## Intake` delta.

4. **Continue or hand off again.** The receiver starts from the retained or replacement next action; a later creation archives the accepted artifact and emits a new ready one.

`handoff-create` and `handoff-resume` do not interpret v1 artifacts — run initialization to preserve and migrate incompatible setup first.

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

`Continuation Context` carries material decisions, constraints — including any whose only source is a runtime-specific instruction file — rejected approaches, environment/services, and secret names or paths, never values. `Validation and Risks` separates fresh `PASS`/`FAIL`/`NOT RUN` evidence from confirmed issues and unverified hypotheses. `Next Action` is exactly one action with target paths, first command, expected current result, and completion condition. Use `None material` for a confirmed-empty category and `Unknown — reason` when evidence is unavailable.

### Size and economics

Soft targets, never caps that suppress critical context: 450 words for a simple handoff, 900 for a complex one, 200 for a resume intake. Skip a handoff when work is complete or a tiny, reconstructible change is already captured by the repository or task tracker — there the ceremony costs more than the context it preserves.

### Safety boundaries

- `preserve-worktree` prohibits reset, clean, stash, branch switching, and discarding inherited changes.
- Creation mutates only active/history handoff artifacts; history is append-only with unique suffixes.
- Old validation never becomes a current pass without re-execution.
- Secret values never enter active or archived handoffs.
- The skills do not edit `.gitignore`, commit, push, or ship runtime scripts.

Whether a project commits `.handoff/` and `HANDOFF.md` remains the user's decision.

### Development

Tests and fresh-context evaluation fixtures are development assets, not installed with the runtime skills. Evaluation evidence, including a cross-runtime (Claude-creates, Codex-resumes) check, lives in `tests/EVALUATION_RESULTS.md`.

```bash
python3 -B -m unittest discover -s tests -v
```

Licensed under [MIT](LICENSE).

## 3. For agents: set up these skills for yourself

Paste the entire prompt below into the prompt line of an agent on the machine where you want the skills installed. The agent should install only for its own runtime; it should not configure this repository or run a handoff.

```text
Set up the Agent Handoff Skills from https://github.com/ljyonefineday/agent-handoff-skills for your own agent environment. This is an installation task only: do not change the current project.

First read that repository's README and the SKILL.md files for handoff-init, handoff-create, and handoff-resume. Detect which agent and runtime you are using, then install those three skills only into your own personal or global skills location. Prefer the README's recommended npx skills installation when npx is available, selecting only your current agent. Otherwise follow the documented no-Node manual method, adapting it to create links only for your current agent. If you need a clone, keep it outside the current project. If a skill is already installed, inspect it first and update it safely; do not overwrite user-modified content or remove anything without permission.

Do not run the installed handoff skills, initialize a handoff, edit project files, commit, or push as part of setup. Verify the installed files and, when possible, confirm that your runtime can discover all three skills. Report the installation method, resolved paths, verification result, and whether a restart is needed. Stop and ask before any overwrite, destructive action, or elevated permission.
```

## 4. 한국어 안내 (Korean)

미완료 코딩 작업을 세션·협업자·컨텍스트 윈도우를 넘어 안전하게 인계하기 위한, 이식 가능한 세 개의 Agent Skills입니다. 핸드오프는 대화 기록이 아니라 실행 가능한 연속 작업 아티팩트입니다: 수신자는 검증된 작업 상태, 핵심 결정과 제약, 정직한 검증 증거, 그리고 정확히 하나의 다음 행동을 전달받습니다. 런타임 번들은 Markdown만으로 구성되어 특정 모델이나 하네스에 묶이지 않습니다. 열린 Agent Skills 레이아웃을 따르는 하네스든, 단순히 `SKILL.md`를 읽고 셸 명령을 실행할 수 있는 에이전트든, 보내는 쪽과 받는 쪽 모두가 될 수 있습니다. 이 절은 요약 번역이며 내용이 다를 경우 영문판을 기준으로 합니다.

### 스킬

| 스킬 | 사용 시점 |
|---|---|
| `handoff-init` | 저장소에 v2 설정·템플릿·히스토리 디렉터리가 필요할 때, 또는 오래되었거나 불완전한 설정을 보존한 뒤 교체해야 할 때 |
| `handoff-create` | 일시 중지, 세션 교체, 컴팩션, 컨텍스트 고갈 전에 미완료 작업을 인계해야 할 때 |
| `handoff-resume` | 새 세션이 활성 핸드오프를 라이브 저장소와 대조 검증한 뒤 안전하게 이어가야 할 때 |

### 설치

권장 방식은 열린 skills CLI로, 20개 이상의 에이전트 하네스(Claude Code, Codex, Cursor, Gemini CLI 등)에 설치할 수 있습니다:

```bash
npx skills add ljyonefineday/agent-handoff-skills
```

Node 없이 설치하려면 저장소를 클론한 뒤 각 스킬 폴더를 사용하는 하네스의 스킬 디렉터리에 심볼릭 링크하세요(Claude Code: `~/.claude/skills`, Codex: `~/.agents/skills`, 다른 하네스도 같은 방식). 이후 업데이트는 클론 안에서 `git pull --ff-only`만 실행하면 됩니다. 새로 설치한 스킬이 보이지 않으면 하네스를 재시작하세요.

### 호출

스킬 설명이 트리거 중심이라 자연어로 동작합니다 — "이 체크아웃의 미완료 작업에 대한 핸드오프를 만들어줘." 명시적 호출은 Claude Code에서 `/handoff-create`, Codex에서 `$handoff-create` 형식입니다.

### 프로토콜 v2 요약

1. **초기화** — `handoff-init`이 정확한 v2 설정(`version: 2`)과 템플릿, `.handoff/history/`를 만듭니다. 유효한 v2 설정은 그대로 두고, 호환되지 않는 기존 설정은 `.handoff/history/protocol-backup-*`에 보관한 뒤 설치합니다. 레거시 아티팩트에 비밀 값이 있을 수 있으면 보관 전에 중단합니다. 활성 핸드오프를 지어내지 않습니다.
2. **생성** — `handoff-create`가 Git과 관련 파일을 점검하고, 안전한 검증을 새로 실행하고, 기존 활성 아티팩트를 보관한 뒤 `Status: ready` 상태의 `HANDOFF.md`를 작성합니다.
3. **재개** — `handoff-resume`이 아티팩트를 라이브 브랜치·HEAD·변경 사항과 대조하고, 정확히 한 번의 게이팅 검증을 새로 실행한 뒤에만 `ready → accepted`로 전환하고 간결한 `## Intake` 델타를 덧붙입니다.
4. **계속 또는 재인계** — 수신자는 유지되거나 교체된 다음 행동에서 시작합니다. 작업이 다시 멈추면 생성 단계가 수락된 아티팩트를 보관하고 새 ready 아티팩트를 만듭니다.

`handoff-create`와 `handoff-resume`은 v1 아티팩트를 해석하지 않습니다. 먼저 초기화를 실행해 기존 설정을 보존·이전하세요.

### 아티팩트 구조와 크기

아티팩트의 섹션 구조는 영문 2절의 코드 블록과 동일합니다. `Continuation Context`에는 핵심 결정, 제약(런타임 전용 지시 파일에만 존재하는 제약 포함), 기각된 접근과 그 이유, 환경/서비스, 그리고 비밀의 이름·경로만 — 값은 절대 — 기록합니다. `Validation and Risks`는 신선한 `PASS`/`FAIL`/`NOT RUN` 증거, 확인된 문제, 미검증 가설을 구분합니다. `Next Action`은 대상 경로, 첫 명령, 현재 예상 결과, 완료 조건을 갖춘 단 하나의 행동입니다. 확인된 빈 항목은 `None material`, 증거가 없으면 `Unknown — reason`을 사용합니다.

크기는 소프트 타깃입니다(단순 450 단어, 복잡 900, 재개 인테이크 200). 절대 상한이 아니며, 중요한 컨텍스트를 잘라내면서까지 맞추지 않습니다. 작업이 완료되었거나 저장소·트래커만으로 복원 가능한 사소한 변경이라면 핸드오프 자체를 생략하세요 — 그 경우 절차 비용이 보존되는 컨텍스트보다 큽니다.

### 안전 경계

- `preserve-worktree`: reset, clean, stash, 브랜치 전환, 상속받은 변경 폐기 금지.
- 생성은 기본적으로 핸드오프 아티팩트만 변경하며, 히스토리는 추가 전용입니다.
- 오래된 PASS는 재실행 없이 현재 통과로 승격되지 않습니다.
- 비밀 값은 활성·보관 아티팩트에 절대 들어가지 않습니다.
- 스킬은 `.gitignore` 수정, 커밋, 푸시, 런타임 스크립트 배포를 하지 않습니다.

`.handoff/`와 `HANDOFF.md`의 Git 추적 여부는 사용자의 선택입니다.

### 에이전트 자가 설치와 개발

다른 머신의 에이전트에게 설치를 맡기려면 영문 3절의 프롬프트를 그대로 붙여넣으세요. 에이전트는 자신의 런타임에만 설치해야 하며, 현재 프로젝트를 변경하거나 핸드오프를 실행해서는 안 됩니다. 테스트와 평가 픽스처는 개발 자산이며 런타임 스킬과 함께 설치되지 않습니다. 교차 런타임(Claude 생성, Codex 재개) 검증 결과는 `tests/EVALUATION_RESULTS.md`에 있습니다. 라이선스: [MIT](LICENSE).
